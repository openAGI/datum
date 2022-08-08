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

from absl.testing import absltest

from datum.generator import image
from datum.utils.common_utils import AttrDict


class TestClfDatumGenerator(absltest.TestCase):

  def setUp(self):
    self.clf_gen = image.ClfDatumGenerator('tests/dummy_data/clf')

  def test_train_generator(self):
    for key, datum in self.clf_gen(split='train'):
      self.assertEqual(list(datum.keys()),
                       ['image', 'label_test1', 'label_test2', 'label_test3', 'label_test4'])
      self.assertEqual(list(datum.values()),
                       ['tests/dummy_data/clf/train/image_232.jpg', 1, 2, 1, 0])
    for key, datum in self.clf_gen(split='train', extension='.jpg'):
      self.assertEqual(list(datum.keys()),
                       ['image', 'label_test1', 'label_test2', 'label_test3', 'label_test4'])
      self.assertEqual(list(datum.values()),
                       ['tests/dummy_data/clf/train/image_232.jpg', 1, 2, 1, 0])
    for key, datum in self.clf_gen(split='train', extension='.jpg', csv_path='train.csv'):
      self.assertEqual(list(datum.keys()),
                       ['image', 'label_test1', 'label_test2', 'label_test3', 'label_test4'])
      self.assertEqual(list(datum.values()),
                       ['tests/dummy_data/clf/train/image_232.jpg', 1, 2, 1, 0])

  def test_val_generator(self):
    for key, datum in self.clf_gen(split='val'):
      self.assertEqual(list(datum.keys()),
                       ['image', 'label_test1', 'label_test2', 'label_test3', 'label_test4'])
      self.assertEqual(list(datum.values()), ['tests/dummy_data/clf/val/image_232.jpg', 1, 2, 1, 0])
    for key, datum in self.clf_gen(split='val', extension='.jpg'):
      self.assertEqual(list(datum.keys()),
                       ['image', 'label_test1', 'label_test2', 'label_test3', 'label_test4'])
      self.assertEqual(list(datum.values()), ['tests/dummy_data/clf/val/image_232.jpg', 1, 2, 1, 0])
    for key, datum in self.clf_gen(split='val', extension='.jpg', csv_path='val.csv'):
      self.assertEqual(list(datum.keys()),
                       ['image', 'label_test1', 'label_test2', 'label_test3', 'label_test4'])
      self.assertEqual(list(datum.values()), ['tests/dummy_data/clf/val/image_232.jpg', 1, 2, 1, 0])


class TestDetDatumGenerator(absltest.TestCase):

  def setUp(self):
    class_map = {
        name: idx + 1
        for idx, name in enumerate(
            open(os.path.join('tests/dummy_data/det/voc/voc2012.names')).read().splitlines())
    }
    self.det_gen = image.DetDatumGenerator('tests/dummy_data/det/voc',
                                           gen_config=AttrDict(has_test_annotations=True,
                                                               class_map=class_map))

  def test_train_generator(self):
    values = {
        '2007_000027': [
            'tests/dummy_data/det/voc/JPEGImages/2007_000027.jpg', [0.35802469135802467],
            [0.7181069958847737], [0.202], [0.702], [0.18004115226337447], ['unspecified'], [15],
            [False], [False]
        ],
        '2007_000032': [
            'tests/dummy_data/det/voc/JPEGImages/2007_000032.jpg', [0.208, 0.266, 0.39, 0.052],
            [0.75, 0.394, 0.426, 0.088],
            [0.2775800711743772, 0.31316725978647686, 0.6405693950177936, 0.6725978647686833],
            [0.6512455516014235, 0.4377224199288256, 0.8149466192170819, 0.8469750889679716],
            [0.2025266903914591, 0.01594306049822064, 0.006277580071174373, 0.006277580071174377],
            ['frontal', 'left', 'rear', 'rear'], [1, 1, 15, 15], [False, False, False, False],
            [False, False, False, False]
        ],
    }
    for key, datum in self.det_gen(split='train', set_dir='ImageSets'):
      self.assertEqual(list(datum.keys()), [
          'image', 'xmin', 'xmax', 'ymin', 'ymax', 'area', 'pose', 'labels', 'is_truncated',
          'labels_difficult'
      ])
      self.assertEqual(list(datum.values()), values[key])
    for key, datum in self.det_gen(split='train',
                                   set_dir='ImageSets',
                                   image_dir='JPEGImages',
                                   annotation_dir='Annotations'):
      self.assertEqual(list(datum.keys()), [
          'image', 'xmin', 'xmax', 'ymin', 'ymax', 'area', 'pose', 'labels', 'is_truncated',
          'labels_difficult'
      ])
      self.assertEqual(list(datum.values()), values[key])

  def test_val_generator(self):
    values = {
        '2007_000027': [
            'tests/dummy_data/det/voc/JPEGImages/2007_000027.jpg', [0.35802469135802467],
            [0.7181069958847737], [0.202], [0.702], [0.18004115226337447], ['unspecified'], [15],
            [False], [False]
        ],
    }
    for key, datum in self.det_gen(split='val', set_dir='ImageSets'):
      self.assertEqual(list(datum.keys()), [
          'image', 'xmin', 'xmax', 'ymin', 'ymax', 'area', 'pose', 'labels', 'is_truncated',
          'labels_difficult'
      ])
      self.assertEqual(list(datum.values()), values[key])
    for key, datum in self.det_gen(split='val',
                                   set_dir='ImageSets',
                                   image_dir='JPEGImages',
                                   annotation_dir='Annotations'):
      self.assertEqual(list(datum.keys()), [
          'image', 'xmin', 'xmax', 'ymin', 'ymax', 'area', 'pose', 'labels', 'is_truncated',
          'labels_difficult'
      ])
      self.assertEqual(list(datum.values()), values[key])


class TestSegDatumGenerator(absltest.TestCase):

  def setUp(self):
    self.seg_gen = image.SegDatumGenerator('tests/dummy_data/seg/voc')

  def test_train_generator(self):
    values = {
        '2007_000032': [
            'tests/dummy_data/seg/voc/JPEGImages/2007_000032.jpg',
            'tests/dummy_data/seg/voc/SegmentationClass/2007_000032.png'
        ],
        '2007_000033': [
            'tests/dummy_data/seg/voc/JPEGImages/2007_000033.jpg',
            'tests/dummy_data/seg/voc/SegmentationClass/2007_000033.png'
        ],
    }
    for key, datum in self.seg_gen(split='train'):
      self.assertEqual(list(datum.keys()), ['image', 'label'])
      self.assertEqual(list(datum.values()), values[key])

  def test_val_generator(self):
    values = {
        '2007_000033': [
            'tests/dummy_data/seg/voc/JPEGImages/2007_000033.jpg',
            'tests/dummy_data/seg/voc/SegmentationClass/2007_000033.png'
        ],
    }
    for key, datum in self.seg_gen(split='val'):
      self.assertEqual(list(datum.keys()), ['image', 'label'])
      self.assertEqual(list(datum.values()), values[key])
