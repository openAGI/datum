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

from typing import Optional

import tensorflow as tf
from absl import logging

from datum.configs import ConfigBase, DatasetConfigs
from datum.reader.dataset import Dataset
from datum.utils.types_utils import DatasetType


def load(path: str, dataset_configs: Optional[ConfigBase] = None) -> DatasetType:
  """Load tfrecord dataset as `tf.data.Daatset`.

  Args:
    path: path to the storage location with tfrecord files and metadata.
    dataset_configs: A DatasetConfigs can be used to control the parameter for
      the output tf.data.Dataset. This is designed to give an extensive control of
      the dataset pre and post processsing operation to the end-user.

    dataset_configs has the following configurable attributes.

    buffer_size: Representing the number of elements from this dataset from which the
          new dataset will sample, default - 100.
    seed: Random seed for tfrecord files based randomness, default - 6052020.
    full_dataset: 'Returns the dataset as a single batch for dataset with only one element,
      default - False.
    batch_size_train: Batch size for training data, default - 32.
    batch_size_val: Batch size for validation data, default - 32.
    batch_size_test: Batch size for test data, default - 32.
    shuffle_files: Shuffle tfrecord input files, default - True.
    reshuffle_each_iteration: If true indicates that the dataset should be pseudorandomly
      reshuffled each time it is iterated over, default - False.
    cache: If true the first time the dataset is iterated over, its elements will be cached
      either the specified file or in memory. Subsequent iterations will use the
      cached data, default - False.
    cache_filename: Representing the name of a directory on the file system to use for caching
      elements in this Dataset, default - ''.
    bucket_op: The sequence length based bucketing operation options.
    bucket_fn: Function from element in Dataset to tf.int32, determines the length of the
      element which will determine the bucket it goes into, default - None.
    pre_batching_callback_train: Preprocessing operation to use on a single case of the dataset
      before batching, default - None.
    post_batching_callback_train: Processing operation to use on a batch of the dataset after
      batching, default - None.
    pre_batching_callback_val: Preprocessing operation to use on a single case of the dataset
      before batching, default - None.
    post_batching_callback_val: Processing operation to use on a batch of the dataset after
      batching, default - None.
    pre_batching_callback_test: Preprocessing operation to use on a single case of the dataset
      before batching, default - None.
    post_batching_callback_test: Processing operation to use on a batch of the dataset after
      batching, default - None.
    read_config: A TFRReadconfigs object can be used to control the parameter required to read
      tfrecord files to construct a tf.data.Dataset.

    `bucket_op` supports the following sub attributes

    bucket_boundaries: Upper length boundaries of the buckets, default - [0].
    bucket_batch_sizes: Batch size per bucket. Length should be len(bucket_boundaries) + 1,
      default - [32, 32].

    `read_config` supports the following sub atrributes

    experimental_interleave_sort_fn: Dataset interleave sort function, default - None.
    shuffle_reshuffle_each_iteration: Shuffle files each iteration before reading,
      default - True.
    interleave_cycle_length: The number of input elements that will be processed concurrently,
      default - -1,
    interleave_block_length: The number of consecutive elements to produce from each input
      element before cycling to another input element, default - 1.
    seed: Random seed for tfrecord files based randomness, default - 6052020.
    options: Tensorflow data api options for dataset prep and reading,
      default - tf.data.Options(),

  Returns:
    a `tf.data.Dataset`.
  """
  if not tf.io.gfile.isdir(path):
    logging.error(
        f'Input path: {path} is not a directory. Provide a path where tfrecord files metadata\
          are stored.')
    raise ValueError(
        f'Input path: {path} is not a directory. Provide a path where tfrecord files metadata\
          are stored.')
  if not dataset_configs:
    logging.info('Using default dataset configuration.')
    dataset_configs = DatasetConfigs()
  return Dataset(path, dataset_configs)
