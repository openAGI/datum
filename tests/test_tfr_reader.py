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

from absl.testing import absltest

from datum.configs import TFRReadConfigs
from datum.reader.tfrecord_reader import Reader
from tests.utils import _test_create_clf_records


class TestTFRReader(absltest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    _test_create_clf_records(self.tempdir)
    configs = TFRReadConfigs()
    self._reader = Reader(self.tempdir, configs)

  def tearDown(self):
    rmtree(self.tempdir)

  def test_read(self):
    ds = self._reader.read('train', False)
    batch = next(iter(ds))
    self.assertEqual(batch['image'].shape, [2670, 2870, 3])
    self.assertEqual(batch['label_test1'], 1)
