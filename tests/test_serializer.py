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
import numpy as np
import tensorflow as tf
from absl.testing import absltest

from datum.serializer.serializer import (DatumSerializer, _item_to_tf_feature, serialize_datum)
from datum.utils.common_utils import is_string


class TestSerializer(absltest.TestCase):

  def setUp(self):
    self.datum = {
        'image': tf.io.gfile.GFile('tests/dummy_data/clf/train/image_232.jpg', mode="rb").read(),
        'label1': [1, 2, 3],
        'label2': 1,
        'label3': 1.1,
    }

  def test_serialize_datum(self):
    # smoke tests
    serialize_datum(self.datum)

  def test_is_string(self):
    values = {
        'image': True,
        'label1': False,
        'label2': False,
        'label3': False,
    }
    for key, val in self.datum.items():
      self.assertEqual(is_string(val), values[key])

  def test_item_to_tf_feature(self):
    values = {
        'image': 'bytes_list',
        'label1': 'int64_list',
        'label2': 'int64_list',
        'label3': 'float_list',
    }
    for key, val in self.datum.items():
      feature = _item_to_tf_feature(val)
      attr_key = values[key]
      assert getattr(feature, attr_key).value


class TestDatumSerializer(absltest.TestCase):

  def setUp(self):
    self.datum = {
        'image': 'tests/dummy_data/clf/train/image_232.jpg',
        'label1': [1, 2, 3],
        'label2': 1,
        'label3': 1.1,
        'label4': 'test',
    }
    self.serializer = DatumSerializer('image')

  def test_datum_serializer(self):
    values = {
        'image': 'bytes_list',
        'label1': 'int64_list',
        'label2': 'int64_list',
        'label3': 'float_list',
        'label4': 'bytes_list',
    }
    example = self.serializer(self.datum)
    features = {
        "image": tf.io.FixedLenFeature((), tf.string),
        "label4": tf.io.FixedLenFeature([], tf.string),
        'label1': tf.io.FixedLenFeature([3], tf.int64),
        'label2': tf.io.FixedLenFeature([], tf.int64),
        'label3': tf.io.FixedLenFeature([], tf.float32),
    }
    parsed_example = tf.io.parse_single_example(example, features)
    assert parsed_example['image'].numpy().startswith(b'\xFF\xD8\xFF'.lower())
    image_decoded = tf.io.decode_image(parsed_example['image'], 3)
    self.assertEqual([2670, 2870, 3], image_decoded.shape)
    self.assertEqual([1, 2, 3], list(parsed_example['label1'].numpy()))
    self.assertEqual(1, parsed_example['label2'].numpy())
    self.assertEqual('test', parsed_example['label4'].numpy().decode('utf-8'))
    self.assertEqual(np.array(1.1, dtype=np.float32), np.array(parsed_example['label3'].numpy()))
