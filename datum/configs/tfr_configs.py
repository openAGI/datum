# coding=utf-8
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

from collections import Callable

import tensorflow as tf

from datum.configs.config_base import ConfigBase, create_config


class TFRWriteConfigs(ConfigBase):
  """TF Record writer configuration.

  A TFRWriteCOnfigs object can be used to control the parameter required for data generation,
  features type information, splits information and splitwise number of examples.
  """
  generator = create_config(name='generator',
                            ty=object,
                            docstring='Generator class instance, it should have a __call__ method.')
  serializer = create_config(
      name='serializer',
      ty=object,
      docstring='Serializer class instance, it should have a __call__ method.')
  sparse_features = create_config(name='sparse_features',
                                  ty=list,
                                  docstring='A list of sparse features name in the dataset.')
  splits = create_config(name='splits',
                         ty=dict,
                         docstring='A dict of split names as keys and \
      split attributes as values in the dataset.')
  num_train_examples = create_config(name='num_train_examples',
                                     ty=int,
                                     docstring='Num of train examples in the dataset.')
  num_val_examples = create_config(name='num_val_examples',
                                   ty=int,
                                   docstring='Num of val examples in the dataset.')

  num_test_examples = create_config(name='num_test_examples',
                                    ty=int,
                                    docstring='Num of test examples in the dataset.')


class TFRReadConfigs(ConfigBase):
  """TF Record Reader configuration.

  A TFRReadconfigs object can be used to control the parameter required to read tfrecord files to
  construct a tf.data.Dataset.
  """

  experimental_interleave_sort_fn = create_config(name='experimental_interleave_sort_fn',
                                                  ty=Callable,
                                                  docstring='Dataset interleave sort function.')

  shuffle_reshuffle_each_iteration = create_config(
      name='shuffle_reshuffle_each_iteration',
      ty=bool,
      docstring='Shuffle files each iteration before reading.',
      default_factory=lambda: True,
  )

  interleave_cycle_length = create_config(
      name='interleave_cycle_length',
      ty=int,
      docstring='The number of input elements that will be processed concurrently',
      default_factory=lambda: -1,
  )

  interleave_block_length = create_config(
      name='interleave_block_length',
      ty=int,
      docstring='The number of consecutive elements to produce from each input element before \
          cycling to another input element',
      default_factory=lambda: 1,
  )
  seed = create_config(
      name='seed',
      ty=int,
      docstring='Random seed for tfrecord files based randomness.',
      default_factory=lambda: 6052020,
  )

  options = create_config(
      name='options',
      ty=tf.data.Options,
      docstring='Tensorflow data api options for dataset prep and reading..',
      default_factory=lambda: tf.data.Options(),
  )


class BucketConfigs(ConfigBase):
  """Bucket configuration used for bucketing sprase data into a batch.

  A BucketConfigs object can be used to control the bucket boundaries and batch sizes.
  """
  bucket_boundaries = create_config(
      name='bucket_boundaries',
      ty=list,
      docstring='Upper length boundaries of the buckets.',
      default_factory=lambda: [0],
  )
  bucket_batch_sizes = create_config(
      name='bucket_batch_sizes',
      ty=list,
      docstring='Batch size per bucket. Length should be len(bucket_boundaries) + 1.',
      default_factory=lambda: [32, 32],
  )


class DatasetConfigs(ConfigBase):
  """Dataset configuration.

  A DatasetConfigs can be used to control the parameter for the output tf.data.Dataset. This is
  designed to give an extensive control of the dataset pre and post processsing operation to the
  end-user.
  """
  buffer_size = create_config(
      name='buffer_size',
      ty=int,
      docstring='Representing the number of elements from this dataset from which the\
           new dataset will sample.',
      default_factory=lambda: 100,
  )
  seed = create_config(
      name='seed',
      ty=int,
      docstring='Random seed for tfrecord files based randomness.',
      default_factory=lambda: 6052020,
  )
  full_dataset = create_config(
      name='full_dataset',
      ty=bool,
      docstring='Returns the dataset as a single batch if it has only one element, useful for\
          serving.',
      default_factory=lambda: False,
  )
  drop_remainder = create_config(
      name='drop_remainder',
      ty=bool,
      docstring='Whether the last batch should be dropped in the case it has fewer than\
          batch_size elements',
      default_factory=lambda: True,
  )
  drop_remainder_val = create_config(
      name='drop_remainder_val',
      ty=bool,
      docstring='Whether the last batch should be dropped in the case it has fewer than\
          batch_size elements',
      default_factory=lambda: False,
  )
  drop_remainder_test = create_config(
      name='drop_remainder_test',
      ty=bool,
      docstring='Whether the last batch should be dropped in the case it has fewer than\
          batch_size elements',
      default_factory=lambda: False,
  )
  deterministic = create_config(
      name='deterministic',
      ty=bool,
      docstring='When `num_parallel_calls` is specified, if this boolean is specified\
        (True or False), it controls the order in which the transformation produces elements.\
        If set to False, the transformation is allowed to yield elements out of order to trade\
        determinism for performance. If not specified, the `tf.data.Options.deterministic`\
        option (True by default) controls the behavior.',
      default_factory=lambda: False,
  )
  deterministic_val = create_config(
      name='deterministic_val',
      ty=bool,
      docstring='When `num_parallel_calls` is specified, if this boolean is specified\
        (True or False), it controls the order in which the transformation produces elements.\
        If set to False, the transformation is allowed to yield elements out of order to trade\
        determinism for performance. If not specified, the `tf.data.Options.deterministic`\
        option (True by default) controls the behavior.',
      default_factory=lambda: False,
  )
  deterministic_test = create_config(
      name='deterministic_test',
      ty=bool,
      docstring='When `num_parallel_calls` is specified, if this boolean is specified\
        (True or False), it controls the order in which the transformation produces elements.\
        If set to False, the transformation is allowed to yield elements out of order to trade\
        determinism for performance. If not specified, the `tf.data.Options.deterministic`\
        option (True by default) controls the behavior.',
      default_factory=lambda: False,
  )
  num_parallel_calls = create_config(
      name='num_parallel_calls',
      ty=int,
      docstring='The number of batches to compute asynchronously in parallel.',
      default_factory=lambda: 1,
  )
  batch_size_train = create_config(
      name='batch_size_train',
      ty=int,
      docstring='Batch size for training data.',
      default_factory=lambda: 32,
  )
  batch_size_val = create_config(
      name='batch_size_val',
      ty=int,
      docstring='Batch size for validation data.',
      default_factory=lambda: 32,
  )
  batch_size_test = create_config(
      name='batch_size_test',
      ty=int,
      docstring='Batch size for test data.',
      default_factory=lambda: 32,
  )
  echoing = create_config(
      name='echoing',
      ty=int,
      docstring='Batch echoing factor, if not None, echoes batches.',
      default_factory=lambda: None,
  )
  shuffle_files = create_config(
      name='shuffle_files',
      ty=bool,
      docstring='Shuffle tfrecord input files.',
      default_factory=lambda: True,
  )
  reshuffle_each_iteration = create_config(
      name='reshuffle_each_iteration',
      ty=bool,
      docstring='If true indicates that the dataset should be pseudorandomly reshuffled each\
          time it is iterated over.',
      default_factory=lambda: False,
  )
  cache = create_config(
      name='cache',
      ty=bool,
      docstring=
      'If true the first time the dataset is iterated over, its elements will be cached either in\
          the specified file or in memory. Subsequent iterations will use the cached data.',
      default_factory=lambda: False,
  )
  cache_filename = create_config(
      name='cache_filename',
      ty=str,
      docstring=
      'Representing the name of a directory on the file system to use for caching elements in \
          this Dataset.',
      default_factory=lambda: '',
  )

  bucket_op = create_config(
      name='bucket_op',
      ty=BucketConfigs,
      docstring='The sequence length based bucketing operation options.',
      default_factory=BucketConfigs,
  )
  bucket_fn = create_config(
      name='bucket_fn',
      ty=Callable,
      docstring='Function from element in Dataset to tf.int32, determines the length of the element\
          which will determine the bucket it goes into.',
  )
  pre_batching_callback_train = create_config(
      name='pre_batching_callback_train',
      ty=Callable,
      docstring='Preprocessing operation to use on a single case of the dataset before batching.',
  )
  post_batching_callback_train = create_config(
      name='post_batching_callback_train',
      ty=Callable,
      docstring='Processing operation to use on a batch of the dataset after batching.',
  )
  pre_batching_callback_val = create_config(
      name='pre_batching_callback_val',
      ty=Callable,
      docstring='Preprocessing operation to use on a single case of the dataset before batching.',
  )
  post_batching_callback_val = create_config(
      name='post_batching_callback_val',
      ty=Callable,
      docstring='Processing operation to use on a batch of the dataset after batching.',
  )
  pre_batching_callback_test = create_config(
      name='pre_batching_callback_test',
      ty=Callable,
      docstring='Preprocessing operation to use on a single case of the dataset before batching.',
  )
  post_batching_callback_test = create_config(
      name='post_batching_callback_test',
      ty=Callable,
      docstring='Processing operation to use on a batch of the dataset after batching.',
  )
  read_config = create_config(
      name='read_config',
      ty=TFRReadConfigs,
      docstring='A TFRReadconfigs object can be used to control the parameter required to read\
        tfrecord files to construct a tf.data.Dataset.',
      default_factory=TFRReadConfigs,
  )
