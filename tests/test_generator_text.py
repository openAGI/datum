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
