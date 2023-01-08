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
from absl.testing import absltest

from datum.configs import DatasetConfigs
from datum.reader.dataset import Dataset
from tests.utils import (_test_create_clf_records, _test_create_det_records,
                         _test_create_seg_records, _test_create_textjson_records)


class TestClfDataset(absltest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    _test_create_clf_records(self.tempdir)
    configs = DatasetConfigs()
    configs.batch_size_train = 1
    configs.batch_size_val = 1
    configs.drop_remainder = True
    configs.drop_remainder_val = True
    configs.deterministic_val = True
    self._dataset = Dataset(self.tempdir, configs)

  def tearDown(self):
    rmtree(self.tempdir)

  def test_train_fn(self):
    ds = self._dataset.train_fn('train', False)
    batch = next(iter(ds))
    self.assertEqual(batch['image'].shape, [1, 2670, 2870, 3])
    self.assertEqual(batch['label_test1'], 1)

  def test_train_fn_shuffle(self):
    ds = self._dataset.train_fn('train', True)
    batch = next(iter(ds))
    self.assertEqual(batch['image'].shape, [1, 2670, 2870, 3])
    self.assertEqual(batch['label_test1'], 1)

  def test_val_fn(self):
    ds = self._dataset.train_fn('val', False)
    batch = next(iter(ds))
    self.assertEqual(batch['image'].shape, [1, 2670, 2870, 3])
    self.assertEqual(batch['label_test1'], 1)

  def test_padded_shapes(self):
    exp = {
        'image': [None] * 3,
        'label_test1': [],
        'label_test2': [],
        'label_test3': [],
        'label_test4': []
    }
    self.assertEqual(self._dataset.padded_shapes, exp)

  def test_dataset_configs_prop(self):
    configs = self._dataset.dataset_configs
    self.assertEqual(configs.batch_size_train, 1)
    self.assertEqual(configs.batch_size_val, 1)
    configs.batch_size_train = 16
    configs.batch_size_val = 16
    self._dataset.dataset_configs = configs
    configs = self._dataset.dataset_configs
    self.assertEqual(configs.batch_size_train, 16)
    self.assertEqual(configs.batch_size_val, 16)


class TestDetDataset(absltest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    _test_create_det_records(self.tempdir)
    configs = DatasetConfigs()
    configs.batch_size_train = 1
    configs.batch_size_val = 1
    self._dataset = Dataset(self.tempdir, configs)

  def tearDown(self):
    rmtree(self.tempdir)

  def test_train_fn(self):
    ds = self._dataset.train_fn('train', False)
    batch = next(iter(ds))
    self.assertEqual(batch['image'].shape, [1, 281, 500, 3])
    np.array_equal(batch['xmin'].numpy(), np.array([0.208, 0.266, 0.39, 0.052], dtype=np.float32))
    np.array_equal(batch['pose'],
                   np.asarray([[b'frontal', b'left', b'rear', b'rear']], dtype=np.unicode_))


class TestSegDataset(absltest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    _test_create_seg_records(self.tempdir)
    configs = DatasetConfigs()
    configs.batch_size_train = 1
    configs.batch_size_val = 1
    self._dataset = Dataset(self.tempdir, configs)

  def tearDown(self):
    rmtree(self.tempdir)

  def test_train_fn(self):
    ds = self._dataset.train_fn('train', False)
    batch = next(iter(ds))
    self.assertEqual(batch['image'].shape, [1, 281, 500, 3])
    self.assertEqual(batch['label'].shape, [1, 281, 500, 3])


class TestTextJsonDataset(absltest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    self.configs = DatasetConfigs()
    self.configs.batch_size_train = 3

  def tearDown(self):
    rmtree(self.tempdir)

  def test_train_fn_json(self):
    expected_data = _test_create_textjson_records(self.tempdir, use_two_files=False)
    self._dataset = Dataset(self.tempdir, self.configs)
    ds = self._dataset.train_fn('train', False)
    batch = next(iter(ds))
    self.assertEqual(batch['text'].shape, [3])
    self.assertEqual(batch['polarity'].shape, [3])
    batch_data = {}
    for idx, text_val in enumerate(batch["text"].numpy()):
      batch_data[idx] = {
          "text": text_val.decode("utf-8"),
          "label": {
              "polarity": batch["polarity"].numpy()[idx],
              "question": batch["question"].numpy()[idx].decode("utf-8"),
          }
      }
    for _, value in batch_data.items():
      assert value in list(expected_data.values())

  def test_train_fn_two_files(self):
    expected_data = _test_create_textjson_records(self.tempdir, use_two_files=True)
    self.configs.batch_size_train = 6
    self._dataset = Dataset(self.tempdir, self.configs)
    ds = self._dataset.train_fn('train', False)
    batch = next(iter(ds))
    self.assertEqual(batch['text'].shape, [6])
    self.assertEqual(batch['polarity'].shape, [6])
    batch_data = {}
    for idx, text_val in enumerate(batch["text"].numpy()):
      batch_data[idx] = {
          "text": text_val.decode("utf-8"),
          "label": {
              "polarity": batch["polarity"].numpy()[idx],
              "question": batch["question"].numpy()[idx].decode("utf-8"),
          }
      }
    for _, value in batch_data.items():
      assert value in list(expected_data.values())
