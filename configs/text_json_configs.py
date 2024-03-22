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

from datum.encoder.encoder import datum_name_to_encoder
from datum.generator.text import TextJsonDatumGenerator
from datum.serializer.serializer import DatumSerializer
from datum.utils.common_utils import AttrDict

_SEED = 5052020

config = {
    'generator': partial(TextJsonDatumGenerator, gen_config=None),
    'sprase_features': [],
    'serializer': DatumSerializer('text', datum_name_to_encoder_fn=datum_name_to_encoder),
    'splits': ['test'],
    'num_examples': {
        'train': 1,
        'val': 1,
    },
}

cnf = AttrDict(config)
