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

import copy
import json
import os
from functools import partial
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import tensorflow as tf
from absl import logging

from datum.configs import ConfigBase
from datum.reader.parser import DatumParser
from datum.utils.common_utils import zip_dict
from datum.utils.reader_utils import ReadInstruction
from datum.utils.shard_utils import get_read_instructions
from datum.utils.types_utils import DatasetType


class Reader(object):
  """Build a tf.data.Dataset object out of Instruction instance(s)."""

  def __init__(self, path: str, read_config: ConfigBase, buffer_size: Optional[int] = None):
    """Initializes Reader.

    Args:
      path: path where tfrecords are stored.
      read_config: tfrecord read configuration.
      buffer_size: scalar representing the number of bytes in the read buffer.
    """
    self._path = path
    self._read_config = read_config
    self._parser = DatumParser(self._path)
    self._buffer_size = buffer_size or 8 << 20 # 8 MiB per file.

  def read(
      self,
      instructions: Union[ReadInstruction, List[ReadInstruction], Dict[str, ReadInstruction]],
      shuffle_files: bool,
  ) -> Union[DatasetType, List[DatasetType], Dict[str, DatasetType]]:
    """Returns tf.data.Dataset instance(s).

    Args:
      instructions (ReadInstruction, List[], Dict[]): instruction(s) to read.
        Instructions can be string and will then be passed to the Instruction
        constructor as it.
      shuffle_files (bool): If True, input files are shuffled before being read.

    Returns:
       a single tf.data.Dataset instance if instruction is a single
       ReadInstruction instance. Otherwise a dict/list of tf.data.Dataset
       corresponding to given instructions param shape.
    """

    def _read_instruction_to_ds(instruction: ReadInstruction) -> DatasetType:
      num_examples_per_shard, file_instructions = make_file_instructions(self._path, instruction)
      return self.read_files(
          file_instructions,
          num_examples_per_shard,
          shuffle_files=shuffle_files,
      )

    return tf.nest.map_structure(_read_instruction_to_ds, instructions)

  def read_files(
      self,
      file_instructions: List[Dict],
      num_examples_per_shard: List[int],
      shuffle_files: bool,
  ) -> DatasetType:
    """Returns single tf.data.Dataset instance for the set of file instructions.

    Args:
      file_instructions: The files information.
        The filenames contains the relative path, not absolute.
        skip/take indicates which example read in the shard: `ds.skip().take()`
      num_examples_per_shard: A list of integer representing number of example per tfrecord
        files.
      shuffle_files: If True, input files are shuffled before being read.

    Returns:
       a tf.data.Dataset instance.
    """
    if not file_instructions:
      raise AssertionError(f'Instruction {file_instructions} corresponds to no data')

    # Prepend path to filename
    files = copy.deepcopy(file_instructions)
    for f in files:
      f.update(filename=os.path.join(self._path, f['filename']))

    if self._read_config.experimental_interleave_sort_fn is not None:
      files = self._read_config.experimental_interleave_sort_fn(files)

    do_skip = any(f['skip'] > 0 for f in files)
    do_take = any(f['take'] > -1 for f in files)

    tensor_inputs = {
        k: list(vals) if k == 'filename' else np.array(vals, dtype=np.int64)
        for k, vals in zip_dict(*files)
    }

    instruction_ds = tf.data.Dataset.from_tensor_slices(tensor_inputs)
    if shuffle_files:
      instruction_ds = instruction_ds.shuffle(
          len(tensor_inputs['filename']),
          seed=self._read_config.seed,
          reshuffle_each_iteration=self._read_config.shuffle_reshuffle_each_iteration,
      )

    ds = instruction_ds.interleave(
        partial(self._get_dataset_from_filename, do_skip=do_skip, do_take=do_take),
        cycle_length=self._read_config.interleave_cycle_length,
        block_length=self._read_config.interleave_block_length,
        num_parallel_calls=tf.data.experimental.AUTOTUNE,
    )

    if (num_examples_per_shard and hasattr(tf.data.experimental, 'assert_cardinality')):
      cardinality = sum(num_examples_per_shard)
      ds = ds.apply(tf.data.experimental.assert_cardinality(cardinality))
    ds = ds.with_options(self._read_config.options)
    return ds.map(self._parser.parse_fn, num_parallel_calls=tf.data.experimental.AUTOTUNE)

  def _get_dataset_from_filename(self, filename_skip_take: Dict[str, Union[str, int]], do_skip: bool,
                                 do_take: bool) -> DatasetType:
    """Returns a tf.data.Dataset instance from given (filename, skip, take)."""
    filename, skip, take = (
        filename_skip_take['filename'],
        filename_skip_take['skip'],
        filename_skip_take['take'],
    )

    ds = tf.data.TFRecordDataset(
        filename,
        buffer_size=self._buffer_size,
        num_parallel_reads=1,
    )
    if do_skip:
      ds = ds.skip(skip)
    if do_take:
      ds = ds.take(take)
    return ds


def make_file_instructions(path: str, instruction: str) -> Tuple[List[int], List[Dict]]:
  """Returns instructions of the split dict.

  Args:
    path: path to the dir with tfrecord metadata json file.
    instruction: `ReadInstruction` or `str`

  Returns:
    a tuple containing a list of integer representing number of examples per shards and a list
      of read instructions dict.
  """
  with tf.io.gfile.GFile(os.path.join(path, 'shard_info.json'), 'r') as si_f:
    shard_info = json.load(si_f)

  # convert shard_info nested dict to single dict
  split2shard_props = {
      key: [list(filenames_examples.keys()),
            list(filenames_examples.values())]
      for key, filenames_examples in shard_info.items()
  }
  split2len = {
      split_name: sum(properties[1])
      for split_name, properties in split2shard_props.items()
  }
  if not isinstance(instruction, ReadInstruction):
    instruction = ReadInstruction.from_spec(instruction)
  # Create the absolute instruction (per split)
  absolute_instructions = instruction.to_absolute(split2len)

  return _make_file_instructions_from_absolutes(
      split2shard_props=split2shard_props,
      absolute_instructions=absolute_instructions,
  )


def _make_file_instructions_from_absolutes(
    split2shard_props: Dict,
    absolute_instructions: ReadInstruction,
) -> Tuple[List[int], List[Dict]]:
  """Returns the files instructions from the absolute instructions list.

  Args:
    split2shard_props: split to filenames and number of examples per shard.
    absolute_instructions: per split absolute read instructions.

  Returns:
    a tuple containing a list of integer representing number of examples per shards and a list
      of read instructions dict.
  """
  file_instructions: List[Dict] = []
  num_examples_per_shard = []
  for abs_instr in absolute_instructions:
    shard_filenames, shard_lengths = split2shard_props[abs_instr.splitname]
    if not shard_lengths:
      logging.error('Shard empty. This might means that dataset has not been generated.')
      raise ValueError('Shard empty. This might means that dataset has not been generated.')
    from_ = 0 if abs_instr.from_ is None else abs_instr.from_
    to = sum(shard_lengths) if abs_instr.to is None else abs_instr.to
    num_examples_per_shard.append(to - from_)
    single_file_instructions = get_read_instructions(from_, to, shard_filenames, shard_lengths)
    file_instructions.extend(single_file_instructions)
  return num_examples_per_shard, file_instructions
