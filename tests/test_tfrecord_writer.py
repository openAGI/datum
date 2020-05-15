import os
import tempfile
from pathlib import Path
from shutil import rmtree

from absl.testing import absltest, parameterized

from datum.generator import image
from datum.serializer.serializer import DatumSerializer
from datum.utils.common_utils import AttrDict
from datum.writer.tfrecord_writer import TFRecordWriter

CLF_GEN = image.ClfDatumGenerator('tests/dummy_data/clf')
class_map = {
    name: idx + 1
    for idx, name in enumerate(
        open(os.path.join('tests/dummy_data/det/voc/voc2012.names')).read().splitlines())
}
DET_GEN = image.DetDatumGenerator(
    'tests/dummy_data/det/voc', gen_config=AttrDict(has_test_annotations=True, class_map=class_map))
SEG_GEN = image.SegDatumGenerator('tests/dummy_data/seg/voc')


@parameterized.parameters([(CLF_GEN, 1), (DET_GEN, 2), (SEG_GEN, 2)])
class TestClfTFRecordWriter(absltest.TestCase):

  def setUp(self):
    self.serializer = DatumSerializer('image')
    self.tempdir = tempfile.mkdtemp()
    Path(self.tempdir).mkdir(parents=True, exist_ok=True)

  def tearDown(self):
    rmtree(self.tempdir)

  def test_cache_records(self, *args):
    generator, num_examples = args
    gen_kwargs = {'image_set': 'ImageSets'}
    self.writer = TFRecordWriter(generator, self.serializer, self.tempdir, 'train', num_examples,
                                 **gen_kwargs)
    self.writer.cache_records()
    self.assertEqual(self.writer.current_examples, num_examples)

  def test_flush(self, *args):
    generator, num_examples = args
    gen_kwargs = {'image_set': 'ImageSets'}
    self.writer = TFRecordWriter(generator, self.serializer, self.tempdir, 'train', num_examples,
                                 **gen_kwargs)
    self.writer.cache_records()
    self.writer.flush()
