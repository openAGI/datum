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
import os
from pathlib import Path
from shutil import rmtree

import numpy as np
import tensorflow as tf
from absl.testing import absltest

from datum.generator import image
from datum.reader.parser import DatumParser
from datum.serializer.serializer import DatumSerializer
from datum.utils.common_utils import AttrDict
from datum.writer.tfrecord_writer import TFRecordWriter


class TestClfDatumParser(absltest.TestCase):

  def setUp(self):
    self.tempdir = '/tmp/test/tfrecord_clf'
    self.serializer = DatumSerializer('image')
    Path(self.tempdir).mkdir(parents=True, exist_ok=True)
    CLF_GEN = image.ClfDatumGenerator('tests/dummy_data/clf')
    gen_kwargs = {'image_set': 'ImageSets'}
    sparse_features = [
        'xmin', 'xmax', 'ymin', 'ymax', 'labels', 'pose', 'is_truncated', 'is_difficult'
    ]
    self.writer = TFRecordWriter(CLF_GEN,
                                 self.serializer,
                                 self.tempdir,
                                 'train',
                                 1,
                                 sparse_features=sparse_features,
                                 **gen_kwargs)
    self.writer.create_records()
    self.parser = DatumParser(self.tempdir)

  def tearDown(self):
    rmtree(self.tempdir)

  def test_parser(self):
    dataset = tf.data.TFRecordDataset(tf.data.Dataset.list_files(self.tempdir + '/train-*.tfrecord'))
    dataset = dataset.map(self.parser.parse_fn)
    dataset = dataset.batch(1)
    for batch in dataset:
      self.assertEqual(list(batch.keys()),
                       ['image', 'label_test1', 'label_test2', 'label_test3', 'label_test4'])
      self.assertEqual(batch['image'].shape, [1, 2670, 2870, 3])
      self.assertEqual(batch['label_test1'].numpy(), [1])


class TestDetDatumParser(absltest.TestCase):

  def setUp(self):
    class_map = {
        name: idx + 1
        for idx, name in enumerate(
            open(os.path.join('tests/dummy_data/det/voc/voc2012.names')).read().splitlines())
    }
    self.tempdir = '/tmp/test/tfrecord_det'
    self.serializer = DatumSerializer('image')
    Path(self.tempdir).mkdir(parents=True, exist_ok=True)
    DET_GEN = image.DetDatumGenerator('tests/dummy_data/det/voc',
                                      gen_config=AttrDict(has_test_annotations=True,
                                                          class_map=class_map))
    gen_kwargs = {'image_set': 'ImageSets'}
    sparse_features = [
        'xmin', 'xmax', 'ymin', 'ymax', 'area', 'labels', 'pose', 'is_truncated', 'labels_difficult'
    ]
    self.writer = TFRecordWriter(DET_GEN,
                                 self.serializer,
                                 self.tempdir,
                                 'train',
                                 2,
                                 sparse_features=sparse_features,
                                 **gen_kwargs)
    self.writer.create_records()
    self.parser = DatumParser(self.tempdir)

  def tearDown(self):
    rmtree(self.tempdir)

  def test_parser(self):
    dataset = tf.data.TFRecordDataset(tf.data.Dataset.list_files(self.tempdir + '/train-*.tfrecord'))
    dataset = dataset.map(self.parser.parse_fn)
    dataset = dataset.batch(1)
    batch = next(iter(dataset))
    self.assertEqual(list(batch.keys()), [
        'area', 'is_truncated', 'labels', 'labels_difficult', 'pose', 'xmax', 'xmin', 'ymax', 'ymin',
        'image'
    ])
    self.assertEqual(batch['image'].shape, [1, 500, 486, 3])
    self.assertEqual(batch['xmin'].numpy(), np.asarray([0.3580247], dtype=np.float32))


class TestSegDatumParser(absltest.TestCase):

  def setUp(self):
    self.tempdir = '/tmp/test/tfrecord_seg'
    self.serializer = DatumSerializer('image')
    Path(self.tempdir).mkdir(parents=True, exist_ok=True)
    SEG_GEN = image.SegDatumGenerator('tests/dummy_data/seg/voc')
    gen_kwargs = {'image_set': 'ImageSets'}
    sparse_features = [
        'xmin', 'xmax', 'ymin', 'ymax', 'labels', 'pose', 'is_truncated', 'is_difficult'
    ]
    self.writer = TFRecordWriter(SEG_GEN,
                                 self.serializer,
                                 self.tempdir,
                                 'train',
                                 1,
                                 sparse_features=sparse_features,
                                 **gen_kwargs)
    self.writer.create_records()
    self.parser = DatumParser(self.tempdir)

  def tearDown(self):
    rmtree(self.tempdir)

  def test_parser(self):
    dataset = tf.data.TFRecordDataset(tf.data.Dataset.list_files(self.tempdir + '/train-*.tfrecord'))
    dataset = dataset.map(self.parser.parse_fn)
    dataset = dataset.batch(1)
    batch = next(iter(dataset))
    self.assertEqual(list(batch.keys()), ['image', 'label'])
    self.assertEqual(batch['image'].shape, [1, 366, 500, 3])
    self.assertEqual(batch['label'].shape, [1, 366, 500, 3])
