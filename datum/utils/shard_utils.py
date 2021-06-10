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
import collections
from typing import Dict, Iterator, List, Sequence, Union

import tensorflow as tf
from absl import logging

MIN_SHARD_SIZE = 64 << 20 # 64 MiB
MAX_SHARD_SIZE = 1024 << 20 # 2 GiB

TFRECORD_REC_OVERHEAD = 16

# Spec to write a final tfrecord shard.
_ShardSpec = collections.namedtuple(
    "_ShardSpec",
    [
        # Index of shard.
        "shard_index",
        # The path where to write shard.
        "path",
        # Number of examples in shard
        "examples_number",
        # Reading instructions. Eg:
        # [dict(shard_index=1, skip=2, take=-1),
        #  dict(shard_index=2, skip=0, take=3)]
        "reading_instructions",
    ])


def raise_error_for_duplicated_keys(err: Exception) -> None:
  """Log information about the examples and raise an AssertionError."""
  msg = "Two records share the same hashed key!"
  logging.error(msg)
  logging.error(err)
  raise AssertionError(msg)


def get_shard_specs(num_examples: int, total_size: int, bucket_lengths: Sequence[int],
                    path: str) -> List[_ShardSpec]:
  """Returns list of _ShardSpec instances, corresponding to shards to write.

  Args:
    num_examples: number of examples in split.
    total_size: sum of example sizes.
    bucket_lengths: number of examples in each bucket.
    path: path to store tfrecord files.

  Retuns:
    a list of ShardSpec objects,
  """
  num_shards = _get_number_shards(total_size, num_examples)
  shard_boundaries = _get_shard_boundaries(num_examples, num_shards)
  shard_specs = []
  bucket_indexes = list(range(len(bucket_lengths)))
  from_ = 0
  for shard_index, to in enumerate(shard_boundaries):
    instructions = get_read_instructions(from_,
                                         to,
                                         bucket_indexes,
                                         bucket_lengths,
                                         shardref_name="bucket_index")
    shard_specs.append(
        _ShardSpec(
            shard_index=shard_index,
            path="%s-%05d-of-%05d.tfrecord" % (path, shard_index, num_shards),
            examples_number=to - from_,
            reading_instructions=instructions,
        ))
    from_ = to
  return shard_specs


def _get_shard_boundaries(num_examples: int, number_of_shards: int) -> List[int]:
  """Shard boundaries based on number of number of shards to generate."""
  if num_examples == 0:
    raise AssertionError("No examples were yielded.")
  if num_examples < number_of_shards:
    raise AssertionError("num_examples ({}) < number_of_shards ({})".format(
        num_examples, number_of_shards))
  return [
      round(num_examples * (float(i) / number_of_shards)) for i in range(1, number_of_shards + 1)
  ]


def write_tfrecord(path: str, iterator: Iterator) -> None:
  """Write single (non sharded) TFrecord file from iterator."""
  with tf.io.TFRecordWriter(path) as writer:
    for serialized_example in iterator:
      writer.write(serialized_example)
    writer.flush()


def _get_number_shards(total_size: int, num_examples: int) -> int:
  """Returns number of shards for num_examples of total_size in bytes. Each shard should be at least
  128MB.

  Args:
    total_size: the size of the data (serialized, not couting any overhead).
    num_examples: the number of records in the data.

  Returns:
    number of shards to use.
  """
  total_size += num_examples * TFRECORD_REC_OVERHEAD
  max_shards_number = total_size // MIN_SHARD_SIZE
  min_shards_number = total_size // MAX_SHARD_SIZE
  if min_shards_number <= 1024 <= max_shards_number and num_examples >= 1024:
    return 1024
  elif min_shards_number > 1024:
    i = 2
    while True:
      n = 1024 * i
      if n >= min_shards_number and num_examples >= n:
        return n
      i += 1
  else:
    for n in [512, 256, 128, 64, 32, 16, 8, 4, 2]:
      if min_shards_number <= n <= max_shards_number and num_examples >= n:
        return n
  return 1


def get_read_instructions(from_: int,
                          to: int,
                          filenames: Sequence[Union[str, int]],
                          shard_lengths: Sequence[int],
                          shardref_name: str = "filename") -> List[Dict]:
  """Returns a list of files (+skip/take) to read [from_:to] items from shards.

  Args:
    from_: int, Index (included) of element from which to read.
    to: int, Index (excluded) of element to which to read.
    filenames: list of strings or ints, the filenames of the shards. Not really
      used, but to place in result.
    shard_lengths: the number of elements in every shard.
    shardref_name: string, defaults to "filename". How to name the field holding
      the shard-reference in result dict.

  Returns:
    list of dict(filename, skip, take).
  """
  index_start = 0 # Beginning (included) of moving window.
  index_end = 0 # End (excluded) of moving window.
  files = []
  for filename, length in zip(filenames, shard_lengths):
    if not length:
      continue # Empty shard - can happen with temporary buckets.
    index_end += length
    if from_ < index_end and to > index_start: # There is something to take.
      skip = from_ - index_start if from_ > index_start else 0
      take = to - index_start - skip if to < index_end else -1
      if take == 0:
        continue
      files.append({shardref_name: filename, "skip": skip, "take": take})
    index_start += length
  return files
