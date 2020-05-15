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
