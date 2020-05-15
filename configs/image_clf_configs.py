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

from functools import partial

import tensorflow as tf

from datum.encoder.encoder import datum_name_to_encoder
from datum.generator.image import ClfDatumGenerator
from datum.serializer.serializer import DatumSerializer
from datum.utils.common_utils import AttrDict

_SEED = 5052020

config = {
    'generator': partial(ClfDatumGenerator, gen_config=None),
    'sprase_features': [],
    'serializer': DatumSerializer('image', datum_name_to_encoder_fn=datum_name_to_encoder),
    'splits': ['train', 'val'],
    'num_examples': {
        'train': 1,
        'val': 1,
    },
    'dataset_config': {
        'buffer_size': 100,
        'seed': _SEED,
        'full_dataset': False,
        'batch_size_train': 32,
        'batch_size_val': 32,
        'batch_size_test': 32,
        'shuffle_files': True,
        'reshuffle_each_iteration': True,
        'cache': False,
        'cache_filename': '',
        'bucket_fn': None,
        'bucket_op': {
            'bucket_boundaries': [0],
            'bucket_batch_sizes': [32, 32],
        },
        'pre_batching_callback_train': None,
        'post_batching_callback_train': None,
        'pre_batching_callback_val': None,
        'post_batching_callback_val': None,
        'pre_batching_callback_test': None,
        'post_batching_callback_test': None,
        'read_config': {
            'experimental_interleave_sort_fn': None,
            'shuffle_reshuffle_each_iteration': False,
            'interleave_cycle_length': 1,
            'interleave_block_length': 1,
            'options': tf.data.Options(),
            'seed': _SEED,
        },
    }
}

cnf = AttrDict(config)
