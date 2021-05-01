# Copyright 2021 The OpenAGI Datum Authors.
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
import tempfile
from ast import literal_eval
from shutil import rmtree

from absl.testing import absltest

from datum.generator import text


class TestTextJsonDatumGenerator(absltest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    self.data = {
        1: {
            'text': 'this is text file',
            'label': {
                'polarity': 1
            }
        },
        2: {
            'text': 'this is json file',
            'label': {
                'polarity': 2
            }
        },
        3: {
            'text': 'this is label file',
            'label': {
                'polarity': 0
            }
        },
    }
    with open(os.path.join(self.tempdir, 'train.json'), 'w') as f:
      json.dump(self.data, f)
    self.gen_from_json = text.TextJsonDatumGenerator(self.tempdir)

  def tearDown(self):
    rmtree(self.tempdir)

  def test_generate_datum(self):
    for key, datum in self.gen_from_json(split='train'):
      self.assertEqual(datum['text'], self.data[literal_eval(key)]['text'])
      self.assertEqual(datum['polarity'], self.data[literal_eval(key)]['label']['polarity'])
