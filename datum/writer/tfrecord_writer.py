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
from itertools import islice
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import tensorflow as tf
from absl import logging

from datum.cache.bucket import DuplicatedKeysError, Shuffler
from datum.utils import shard_utils
from datum.utils.common_utils import datum_to_type_and_shape
from datum.utils.tqdm_utils import tqdm
from datum.utils.types_utils import DatumType


class TFRecordWriter():
  """TFRecord writer interface.

  This module is used to convert data into serialized binary string and to write  data
  as tfrecords to disk. It uses a cache to shuffle and store intermediate serialized binary
  string tensors.

  Args:
    generator: an instance of a datum generator.
    serializer: an instance of datum serializer.
    path: absolute path to store the tfrecords data and metadata.
    split: name of the split.
    total_examples: number of examples to write.
    gen_kwargs: optional keyword arguments to used when calling geenrator.
  """

  def __init__(self,
               generator: Callable,
               serializer: Callable,
               path: str,
               split: str,
               total_examples: int,
               sparse_features: Optional[List[str]] = None,
               **gen_kwargs: Any):
    """ path = /tmp/test/
       split = train/val/test
    """
    self.generator = generator
    self.serializer = serializer
    self.shuffler = Shuffler(os.path.dirname(path), split)
    self._base_path = path
    self.path = os.path.join(path, split)
    self.current_examples = 0
    self.total_examples = total_examples
    self.split = split
    self.sparse_features = sparse_features or []
    self.gen_kwargs = gen_kwargs or {}
    self.gen_kwargs.update({'split': self.split})

  def cache_records(self) -> None:
    """Write data to cache."""
    for key, datum in tqdm(self.generator(**self.gen_kwargs),
                           unit=" examples",
                           total=self.total_examples,
                           leave=False):
      if self.sparse_features:
        logging.debug(f'Adding shapes info to datum for sparse features: {self.sparse_features}.')
        datum = self.add_shape_fields(datum)
      serialized_record = self.serializer(datum)
      self.shuffler.add(key, serialized_record)
      self.current_examples += 1
    with tf.io.gfile.GFile(os.path.join(self._base_path, 'datum_to_type_and_shape_mapping.json'),
                           'w') as js_f:
      logging.info(f'Saving datum type and shape metadata to {self._base_path}.')
      types_shapes = datum_to_type_and_shape(datum, self.sparse_features)
      json.dump(types_shapes, js_f)

  def create_records(self) -> None:
    """Create tfrecords from given generator."""
    logging.info('Caching serialized binary example to cache.')
    self.cache_records()
    logging.info('Writing data from cache to disk in `.tfrecord` format.')
    self.flush()

  def add_shape_fields(self, datum: DatumType) -> DatumType:
    """Add tensor shape information to dataset metadat json file and tfrecords. This is required when
    dealing wit sparse tensors. As we need to revert back the original shape of tensor, when tensor
    dimension >= 2.

    Args:
      datum: a dict, input datum.

    Returns:
      input dict updated with sprase tensors shape information.
    """
    new_fields = {}
    for sparse_key in self.sparse_features:
      if sparse_key in datum:
        value = np.asarray(datum[sparse_key])
        if len(value.shape) >= 2:
          new_fields[sparse_key + '_shape'] = list(value.shape)
    datum.update(new_fields)
    return datum

  def flush(self) -> None:
    """Wirte tfrecord files to disk."""
    self.flush_records()

  def flush_records(self) -> Tuple[Dict[str, Dict[str, int]], int]:
    """Write tfrecord files to disk.

    Returns:
      a tuple containing a dict with shard info and the size of shuffler.
    """
    logging.info(f"Shuffling and writing examples to {self.path}")
    shard_specs = shard_utils.get_shard_specs(self.current_examples, self.shuffler.size,
                                              self.shuffler.bucket_lengths, self.path)
    examples_generator = iter(
        tqdm(self.shuffler, total=self.current_examples, unit=" examples", leave=False))
    try:
      for shard_spec in shard_specs:
        iterator = islice(examples_generator, 0, shard_spec.examples_number)
        shard_utils.write_tfrecord(shard_spec.path, iterator)
    except DuplicatedKeysError as err:
      shard_utils.raise_error_for_duplicated_keys(err)
    shard_info = {
        self.split: {spec.path.split('/')[-1]: int(spec.examples_number)
                     for spec in shard_specs}
    }
    self.save_shard_info(shard_info)
    logging.info(f"Done writing {self.path}. Shard lengths: {list(shard_info[self.split].values())}")
    return shard_info, self.shuffler.size

  def save_shard_info(self, shard_info: Dict[str, Dict[str, int]]) -> None:
    """Save shard info to disk.

    Args:
      shard_info: input shard info dict.
    """
    if os.path.isfile(os.path.join(self._base_path, 'shard_info.json')):
      with tf.io.gfile.GFile(os.path.join(self._base_path, 'shard_info.json'), 'r') as si_f:
        prev_shard_info = json.load(si_f)
        shard_info.update(prev_shard_info)
    with tf.io.gfile.GFile(os.path.join(self._base_path, 'shard_info.json'), 'w') as si_f:
      json.dump(shard_info, si_f)
