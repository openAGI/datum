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
    self.data_1 = {
        1: {
            'text': 'this is text file',
            'label': {
                'polarity': 1,
                'question': "meaning of this line?",
            }
        },
        2: {
            'text': 'this is json file',
            'label': {
                'polarity': 2,
                'question': "meaning of this sentence?",
            }
        },
        3: {
            'text': 'this is label file',
            'label': {
                'polarity': 0,
                'question': "meaning of this para?",
            }
        },
    }
    self.data_2 = {
        4: {
            'text': 'this is next text file',
            'label': {
                'polarity': 4,
                'question': "meaning of next line?",
            }
        },
        5: {
            'text': 'this is next json file',
            'label': {
                'polarity': 5,
                'question': "meaning of next sentence?",
            }
        },
        6: {
            'text': 'this is next label file',
            'label': {
                'polarity': 6,
                'question': "meaning of next para?",
            }
        },
    }
    self.data = {**self.data_1, **self.data_2}
    with open(os.path.join(self.tempdir, 'train.json'), 'w') as f:
      json.dump(self.data_1, f)
    self.gen_from_json = text.TextJsonDatumGenerator(self.tempdir)

  def tearDown(self):
    rmtree(self.tempdir)

  def test_generate_datum(self):
    for key, datum in self.gen_from_json(split='train'):
      self.assertEqual(datum['text'], self.data_1[literal_eval(key)]['text'])
      self.assertEqual(datum['polarity'], self.data_1[literal_eval(key)]['label']['polarity'])
      self.assertEqual(datum['question'], self.data_1[literal_eval(key)]['label']['question'])

  def test_generate_datum_multiple_files(self):
    with open(os.path.join(self.tempdir, 'train_2.json'), 'w') as f:
      json.dump(self.data_2, f)
    gen_from_json = text.TextJsonDatumGenerator(self.tempdir)
    for key, datum in self.gen_from_json(split='train'):
      self.assertEqual(datum['text'], self.data[literal_eval(key)]['text'])
      self.assertEqual(datum['polarity'], self.data[literal_eval(key)]['label']['polarity'])
      self.assertEqual(datum['question'], self.data[literal_eval(key)]['label']['question'])
