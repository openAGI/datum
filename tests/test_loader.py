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
import tempfile
from shutil import rmtree

import numpy as np
import tensorflow as tf
from absl.testing import absltest

from datum.reader.loader import load
from tests.utils import _test_create_det_records


class TestDataset(absltest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    _test_create_det_records(self.tempdir)
    self._dataset = load(self.tempdir)
    dataset_configs = self._dataset.dataset_configs
    dataset_configs.batch_size_train = 1
    dataset_configs.batch_size_val = 1
    self._dataset.daatset_configs = dataset_configs

  def tearDown(self):
    rmtree(self.tempdir)

  def test_train_fn(self):
    ds = self._dataset.train_fn('train', False)
    batch = next(iter(ds))
    self.assertEqual(batch['image'].shape, [1, 281, 500, 3])
    np.array_equal(batch['xmin'].numpy(), np.array([0.208, 0.266, 0.39, 0.052], dtype=np.float32))

  def test_full_dataset(self):
    dataset_configs = self._dataset.dataset_configs
    dataset_configs.full_dataset = True
    self._dataset.daatset_configs = dataset_configs
    with self.assertRaises(tf.errors.InvalidArgumentError):
      self._dataset.train_fn('train', False)

  def test_pre_batching_callback(self):

    def resize_image(example):
      example['image'] = tf.image.resize(example['image'], [224, 224])
      return example

    dataset_configs = self._dataset.dataset_configs
    dataset_configs.pre_batching_callback_train = resize_image
    dataset_configs.use_datum_padding = True
    self._dataset.daatset_configs = dataset_configs
    ds = self._dataset.train_fn('train', False)
    batch = next(iter(ds))
    self.assertEqual(batch['image'].shape, [1, 224, 224, 3])
    np.array_equal(batch['xmin'].numpy(), np.array([0.208, 0.266, 0.39, 0.052], dtype=np.float32))
    dataset_configs = self._dataset.dataset_configs
    dataset_configs.batch_size_train = 2
    self._dataset.daatset_configs = dataset_configs
    ds = self._dataset.train_fn('train', False)
    batch = next(iter(ds))
    self.assertEqual(batch['image'].shape, [2, 224, 224, 3])

  def test_post_batching_callback(self):

    def resize_image(example):
      example['image'] = tf.image.resize(example['image'], [224, 224])
      return example

    dataset_configs = self._dataset.dataset_configs
    dataset_configs.post_batching_callback_train = resize_image
    dataset_configs.batch_size_train = 2
    dataset_configs.use_datum_padding = True
    self._dataset.daatset_configs = dataset_configs
    ds = self._dataset.train_fn('train', False)
    batch = next(iter(ds))
    self.assertEqual(batch['image'].shape, [2, 224, 224, 3])

  def test_echoing(self):

    def resize_image(example):
      example['image'] = tf.image.resize(example['image'], [224, 224])
      return example

    dataset_configs = self._dataset.dataset_configs
    dataset_configs.post_batching_callback_train = resize_image
    dataset_configs.batch_size_train = 2
    dataset_configs.echoing = 2
    dataset_configs.use_datum_padding = True
    ds = iter(self._dataset.train_fn('train', False))
    batch_1 = next(ds)
    self.assertEqual(batch_1['image'].shape, [2, 224, 224, 3])
    batch_2 = next(ds)
    self.assertEqual(batch_2['image'].shape, [2, 224, 224, 3])
    with self.assertRaises(StopIteration):
      next(ds)
