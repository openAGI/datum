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

import os
from functools import partial

from datum.encoder.encoder import datum_name_to_encoder
from datum.generator.image import DetDatumGenerator
from datum.serializer.serializer import DatumSerializer
from datum.utils.common_utils import AttrDict

LABEL_NAMES_FILE = 'tests/dummy_data/det/voc/voc2012.names'

class_map = {
    name: idx + 1
    for idx, name in enumerate(open(os.path.join(LABEL_NAMES_FILE)).read().splitlines())
}
config = {
    'generator':
    partial(DetDatumGenerator, gen_config=AttrDict(has_test_annotations=True, class_map=class_map)),
    'sprase_features': [],
    'serializer':
    DatumSerializer('image', datum_name_to_encoder_fn=datum_name_to_encoder),
    'splits': ['train', 'val'],
    'num_examples': {
        'train': 1,
        'val': 1,
    }
}

cnf = AttrDict(config)
