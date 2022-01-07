# Copyright 2020 The OpenAGI Datum Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
from typing import Callable, Dict, List, Optional

import tensorflow as tf
from absl import logging

from datum.configs import ConfigBase
from datum.reader.tfrecord_reader import Reader
from datum.utils.common_utils import memoized_property
from datum.utils.types_utils import DatasetType


class Dataset():
  """Public API to read tfrecord as tf.data.Dataset.

  Args:
    path: path to the tfrecord files.
    dataset_configs: Optional configuration for data processing and reading.
  """

  def __init__(self, path: str, dataset_configs: ConfigBase):
    self._path = path
    self._dataset_configs = dataset_configs
    self._reader = Reader(self._path, self._dataset_configs.read_config)

  @property
  def dataset_configs(self) -> ConfigBase:
    """Returns current object dataset configs."""
    return self._dataset_configs

  @dataset_configs.setter
  def dataset_configs(self, configs: ConfigBase) -> None:
    """Reset dataset configs."""
    self._dataset_configs = configs

  def _read(self,
            instruction: str,
            batch_size: Optional[int] = None,
            repeat: Optional[int] = None,
            bucket_fn: Optional[Callable[[tf.train.Example], int]] = None,
            shuffle: bool = False,
            echoing: Optional[int] = None,
            full_dataset: bool = False,
            drop_remainder: bool = False,
            deterministic: bool = False,
            pre_batching_callback: Optional[Callable[[Dict], Dict]] = None,
            post_batching_callback: Optional[Callable[[Dict], Dict]] = None) -> DatasetType:
    """Read and process data from tfrecord files.

    Args:
      instruction: instructions to read data split. One single dataset can have data from more than
        one splits.
      batch_size: batch size.
      repeat: number of times to repeat the dataset.
      bucket_fn: element length computation fn for bucketing, for sporse inputs data can be
       batched based on element length.
      shuffle: whether to shuffle examples in the dataset.
      echoing: batch echoing factor, if not None perform batch_echoing.
      full_dataset: if true, return the dataset as a single batch for dataset with single element.
      drop_remainder: Whether the last batch should be dropped in the case it has fewer than
        `batch_size` elements.
      deterministic: When `num_parallel_calls` is specified, if this boolean is specified
        (True or False), it controls the order in which the transformation produces elements.
        If set to False, the transformation is allowed to yield elements out of order to trade
        determinism for performance. If not specified, the `tf.data.Options.deterministic`
        option (True by default) controls the behavior.
      pre_batching_callback: data processing to apply before batching.
      post_batching_callback: data processing to apply post batching. This fucntion should support
        batch processsing.

    Returns:
      a tf.data.Dataset object.
    """
    dataset = self._reader.read(instruction, self._dataset_configs.shuffle_files)
    if self._dataset_configs.cache:
      logging.info(f'Caching dataset to {self._dataset_configs.get("cache_filename", "memory")}')
      dataset = dataset.cache(self._dataset_configs.get('cache_filename', ''))
    if pre_batching_callback:
      logging.info('Applying pre batching callback.')
      dataset = dataset.map(pre_batching_callback)
    if shuffle:
      logging.info('Shuffling dataset examplas.')
      dataset = dataset.shuffle(
          self._dataset_configs.buffer_size,
          seed=self._dataset_configs.seed,
          reshuffle_each_iteration=self._dataset_configs.reshuffle_each_iteration)
    if bucket_fn:
      logging.info(
          f'Using bucketing to batch data, bucket_params: {self._dataset_configs.bucket_op}')
      dataset = dataset.bucket_by_sequence_length(
          bucket_fn,
          self._dataset_configs.bucket_op.bucket_boundaries,
          self._dataset_configs.bucket_op.bucket_batch_sizes,
          padded_shapes=tf.compat.v1.data.get_output_shapes(dataset),
          padding_values=None,
          drop_remainder=drop_remainder,
          pad_to_bucket_boundary=False)
    elif batch_size and not deterministic:
      dataset = dataset.padded_batch(batch_size,
                                     padded_shapes=self.padded_shapes,
                                     drop_remainder=drop_remainder)
    elif batch_size and deterministic:
      dataset = dataset.batch(batch_size,
                              drop_remainder=drop_remainder,
                              num_parallel_calls=self._dataset_configs.num_parallel_calls,
                              deterministic=deterministic)
    if echoing:
      dataset = dataset.flat_map(
          lambda example: tf.data.Dataset.from_tensors(example).repeat(echoing))
    if repeat:
      logging.info(f'Dataset repeat is enabled for: {repeat} times.')
      dataset = dataset.repeat(count=repeat)
    if post_batching_callback:
      logging.info('Applying post batching callback.')
      dataset = dataset.map(post_batching_callback)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    if full_dataset:
      logging.info('Returning full dataset as a single batch.')
      return tf.data.experimental.get_single_element(dataset)
    return dataset

  @memoized_property
  def padded_shapes(self) -> Dict[str, List]:
    """Returns padded shapes from dataset metadata."""
    with open(os.path.join(self._path, 'datum_to_type_and_shape_mapping.json'), 'r') as json_f:
      mapping = json.load(json_f)
    padded_shapes = {}
    for key, value in mapping.items():
      if len(value['shape']) > 0:
        padded_shapes[key] = [None] * len(value['shape'])
      else:
        padded_shapes[key] = []
    return padded_shapes

  def train_fn(self,
               instruction: str = 'train',
               repeat: Optional[int] = None,
               shuffle: bool = True) -> DatasetType:
    """Get training dataset.

    Args:
      instruction: instruction on how much data to read.
      repeat: number of times to repeat the dataset.
      shuffle: if true, shuffles examples of the dataset.

    Returns:
      a tf.data.Dataset object.
    """
    return self._read(instruction,
                      batch_size=self._dataset_configs.batch_size_train,
                      repeat=repeat,
                      bucket_fn=self._dataset_configs.bucket_fn,
                      shuffle=shuffle,
                      echoing=self._dataset_configs.echoing,
                      full_dataset=self._dataset_configs.full_dataset,
                      drop_remainder=self._dataset_configs.drop_remainder,
                      deterministic=self._dataset_configs.deterministic,
                      pre_batching_callback=self._dataset_configs.pre_batching_callback_train,
                      post_batching_callback=self._dataset_configs.post_batching_callback_train)

  def val_fn(self,
             instruction: str = 'val',
             repeat: Optional[int] = None,
             shuffle: bool = False) -> DatasetType:
    """Get validation dataset.

    Args:
      instruction: instruction on how much data to read.
      repeat: number of times to repeat the dataset.
      shuffle: if true, shuffles examples of the dataset.

    Returns:
      a tf.data.Dataset object.
    """
    return self._read(instruction,
                      batch_size=self._dataset_configs.batch_size_val,
                      repeat=repeat,
                      bucket_fn=self._dataset_configs.bucket_fn,
                      shuffle=shuffle,
                      echoing=None,
                      full_dataset=self._dataset_configs.full_dataset,
                      drop_remainder=self._dataset_configs.drop_remainder_val,
                      deterministic=self._dataset_configs.deterministic_val,
                      pre_batching_callback=self._dataset_configs.pre_batching_callback_val,
                      post_batching_callback=self._dataset_configs.post_batching_callback_val)

  def test_fn(self,
              instruction: str = 'test',
              repeat: int = 1,
              shuffle: bool = False) -> DatasetType:
    """Get test dataset.

    Args:
      instruction: instruction on how much data to read.
      repeat: number of times to repeat the dataset.
      shuffle: if true, shuffles examples of the dataset.

    Returns:
      a tf.data.Dataset object.
    """
    return self._read(instruction,
                      batch_size=self._dataset_configs.batch_size_test,
                      repeat=repeat,
                      bucket_fn=self._dataset_configs.bucket_fn,
                      shuffle=shuffle,
                      echoing=None,
                      full_dataset=self._dataset_configs.full_dataset,
                      drop_remainder=self._dataset_configs.drop_remainder_test,
                      deterministic=self._dataset_configs.deterministic_test,
                      pre_batching_callback=self._dataset_configs.pre_batching_callback_test,
                      post_batching_callback=self._dataset_configs.post_batching_callback_test)
