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
from pathlib import Path
from shutil import rmtree

from datum.generator import image, text
from datum.serializer.serializer import DatumSerializer
from datum.utils.common_utils import AttrDict
from datum.writer.tfrecord_writer import TFRecordWriter


def _test_create_clf_records(path):
  serializer = DatumSerializer('image')
  Path(path).mkdir(parents=True, exist_ok=True)
  clf_gen = image.ClfDatumGenerator('tests/dummy_data/clf')
  gen_kwargs = {'image_set': 'ImageSets'}
  writer = TFRecordWriter(clf_gen, serializer, path, 'train', 1, sparse_features=None, **gen_kwargs)
  writer.create_records()
  writer = TFRecordWriter(clf_gen, serializer, path, 'val', 1, sparse_features=None, **gen_kwargs)
  writer.create_records()


def _test_create_det_records(path):
  class_map = {
      name: idx + 1
      for idx, name in enumerate(
          open(os.path.join('tests/dummy_data/det/voc/voc2012.names')).read().splitlines())
  }
  serializer = DatumSerializer('image')
  Path(path).mkdir(parents=True, exist_ok=True)
  det_gen = image.DetDatumGenerator('tests/dummy_data/det/voc',
                                    gen_config=AttrDict(has_test_annotations=True,
                                                        class_map=class_map))
  gen_kwargs = {'image_set': 'ImageSets'}
  sparse_features = [
      'xmin', 'xmax', 'ymin', 'ymax', 'area', 'labels', 'pose', 'is_truncated', 'labels_difficult'
  ]
  writer = TFRecordWriter(det_gen,
                          serializer,
                          path,
                          'train',
                          2,
                          sparse_features=sparse_features,
                          **gen_kwargs)
  writer.create_records()
  writer = TFRecordWriter(det_gen,
                          serializer,
                          path,
                          'val',
                          1,
                          sparse_features=sparse_features,
                          **gen_kwargs)
  writer.create_records()


def _test_create_seg_records(path):
  serializer = DatumSerializer('image')
  Path(path).mkdir(parents=True, exist_ok=True)
  seg_gen = image.SegDatumGenerator('tests/dummy_data/seg/voc')
  gen_kwargs = {'image_set': 'ImageSets'}
  writer = TFRecordWriter(seg_gen, serializer, path, 'train', 1, **gen_kwargs)
  writer.create_records()
  writer = TFRecordWriter(seg_gen, serializer, path, 'val', 1, **gen_kwargs)
  writer.create_records()


def _test_create_textjson_records(path, use_two_files=False):
  tempdir = tempfile.mkdtemp()
  data = {
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
  num_examples = 3
  final_data = data
  if use_two_files:
    data_2 = {
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
    with open(os.path.join(tempdir, 'train_2.json'), 'w') as f:
      json.dump(data_2, f)
    num_examples = 6
    final_data = {**data, **data_2}
  with open(os.path.join(tempdir, 'train.json'), 'w') as f:
    json.dump(data, f)
  gen_from_json = text.TextJsonDatumGenerator(tempdir)
  serializer = DatumSerializer('text')
  Path(path).mkdir(parents=True, exist_ok=True)
  textjson_gen = text.TextJsonDatumGenerator(tempdir)
  writer = TFRecordWriter(textjson_gen, serializer, path, 'train', num_examples)
  writer.create_records()
  rmtree(tempdir)
  return final_data
