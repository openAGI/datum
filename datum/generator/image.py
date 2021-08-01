# Copyright 2020 The OpenAGI Datum Authors.
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

import csv
import os
import xml.etree.ElementTree
from ast import literal_eval
from typing import Any, Dict, List, Tuple, no_type_check

import tensorflow as tf

from datum.generator import DatumGenerator
from datum.utils.types_utils import GeneratorReturnType


class ClfDatumGenerator(DatumGenerator):
  """Image classification problem data generator.

  An object of this class can be used to iterate over data stored in a specified folder
  in the host device in a specified format.

  Typically this generator expect the input data to be stored in the following format:

  + data_path
      - train (folder with training images, named after split)
      - val (folder with validation images, named after split)
      - test (folder with test images, named after split)
      - train.csv (csv file with columns data as label with respect to filename
            (filename without extension) )
        ```
          filename, label_name1, label_name2, ...., label_nameN
          test_image1, 1, 2, ..., 1.1
          test_image1, 1, 2, ..., 1.3
        ```

      - val.csv (csv file with columns data as label with respect to filename
            (filename without extension) )
      - test.csv (csv file with columns data as label with respect to filename
            (filename without extension) )

  It is not mandatory to have all the folders and csv files named after split name. You can control
  the folder name by passing it as input the `__call__` method.
  For a particular split, image folder name, labels csv fllename, data extension can be
  controlled by passing the following keyword arguments the `__call__` method.

  All sub directory path are relative to the root path.

  Following inputs for kwargs are accepted when calling the object:

  Kwargs:
    split: name of the split.
    extension: image extension, defualt is '.jpg'.
    image_dir: directroy name containing the image, default name is split name.
    csv_path: labels filename, default name is `<split>.csv`
  """

  def generate_datum(self, **kwargs: Any) -> GeneratorReturnType:
    """Yields Example instances from given CSV.

    Args:
      kwargs: Optional kwargs for further input data format customization.

      Following inputs for kwargs are accepted:

      split: name of the split.
      extension: image extension, defualt is '.jpg'.
      image_dir: directroy name containing the image, default name is split name.
      csv_path: labels filename, default name is `<split>.csv`

    Returns:
      a tuple of datum id and a dict with key as feature name and values as feature values.
    """
    split = kwargs.get('split')
    if not split:
      raise ValueError('Pass a valid split name to generate data.')
    extension = kwargs.get('extension', '.jpg')
    sub_dir = kwargs.get('image_dir', split)
    csv_path = kwargs.get('csv_path', split + '.csv')
    data_path = os.path.join(self.path, sub_dir)
    data: List[Dict] = []
    with tf.io.gfile.GFile(os.path.join(self.path, csv_path)) as csv_f:
      reader = csv.DictReader(csv_f)
      for row in reader:
        feature_dict = {}
        for feature_name, feature_value in row.items():
          if feature_name != 'filename':
            feature_dict[feature_name] = literal_eval(feature_value)
          else:
            feature_value = os.path.join(data_path, feature_value + extension)
            feature_dict['image'] = feature_value
        data.append(feature_dict)
    for idx, datum in enumerate(data):
      yield idx, datum


class DetDatumGenerator(DatumGenerator):
  """Image object Detection problem data generator.

  This generator expect image data to be stored in the Pascal VOC data format in the
  input storage location.

  For each input example image, corresponding labels should be stored in a xml file, if
  labels loading is enabled.

  Input data should be stored in the following format

  + data_dir
      - JPEGImages (all images, any number of split, stored together)
      - Annotations (All annotations for detection, .xml format)
      - ImageSets (Splits file, txt files with split name, each line contain name of the
          image to use use for that split
          e.g. image1\n image2\n etc)

  While the overall directory levels should be as shown in the format, sub-directory names can
  be controlled by passing keyword argument to `__call__` method.

  Following inputs for kwargs are accepted when calling the object:

  Kwargs:
    split: name of the split.
    extension: image extension.
    set_dir: directory name where split files are stored.
    image_dir: directory name where images are stored.
    annotation_dir: directory name where xml annotation files are stored.
  """

  def generate_datum(self, **kwargs: Any) -> GeneratorReturnType:
    """Generator to iterate over data stored in the data folder.

    Args:
      kwargs: optional, keyword arguments can be used to control folder names and image extension.

      Following kwargs are supported:

      split: name of the split.
      extension: image extension.
      set_dir: directory name where split files are stored.
      image_dir: directory name where images are stored.
      annotation_dir: directory name where xml annotation files are stored.

    Returns:
      a tuple of datum id and a dict with key as feature name and values as feature values.

    Raises:
      ValueError: if inptut split name is not provided.
    """
    split = kwargs.get('split')
    if not split:
      raise ValueError('Pass a valid split name to generate data.')
    extension = kwargs.get('extension', '.jpg')
    set_dir = kwargs.get('set_dir', 'ImageSets')
    image_dir = kwargs.get('image_dir', 'JPEGImages')
    annon_dir = kwargs.get('annotation_dir', 'Annotations')
    set_filepath = os.path.join(self.path, set_dir, split + '.txt')
    with tf.io.gfile.GFile(set_filepath, "r") as f:
      for line in f:
        image_id = line.strip()
        example = self._generate_example(self.path, image_dir, annon_dir, image_id, extension,
                                         self.gen_config.has_test_annotations)
        yield image_id, example

  def _generate_example(self, data_path: str, image_dir: str, annon_dir: str, image_id: str,
                        extension: str, load_annotations: bool) -> Dict:
    """Generate a single example of the dataset.

    Args:
      data_path: input dataset storage path.
      image_dir: directory name with input images.
      annon_dir: directory name with input annotations xml files.
      image_id: id of the image, here the image name without extension.
      extension: image filename extension.
      load_annotations: whether to load annotations. True for training and validation.

    Returns:
      a dict with keys as feature names and values as feature values.
    """
    image_filepath = os.path.join(data_path, image_dir, image_id + extension)
    annon_filepath = os.path.join(data_path, annon_dir, image_id + '.xml')
    if load_annotations:
      xmin, xmax, ymin, ymax, label, pose, is_truncated, is_difficult = self._get_example_objects(
          annon_filepath)
    else:
      xmin = []
      xmax = []
      ymin = []
      ymax = []
      label = []
      pose = []
      is_truncated = []
      is_difficult = []
    return {
        "image": image_filepath,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "pose": pose,
        "labels": label,
        "is_truncated": is_truncated,
        "labels_difficult": is_difficult,
    }

  @no_type_check
  def _get_example_objects(self, annon_filepath: str) -> Tuple:
    """Function to get all the objects from the annotation XML file."""
    with tf.io.gfile.GFile(annon_filepath, "r") as f:
      root = xml.etree.ElementTree.parse(f).getroot()
      size = root.find("size")
      width = float(size.find("width").text)
      height = float(size.find("height").text)

      xmin: List[float] = []
      xmax: List[float] = []
      ymin: List[float] = []
      ymax: List[float] = []
      label: List[int] = []
      pose: List[str] = []
      is_truncated: List[bool] = []
      is_difficult: List[bool] = []
      for obj in root.findall("object"):
        class_id = obj.find("name").text.lower()
        if isinstance(class_id, str):
          label.append(self.gen_config.class_map[class_id])
        else:
          label.append(class_id)
        pose.append(obj.find("pose").text.lower())
        is_truncated.append((obj.find("truncated").text == "1"))
        is_difficult.append((obj.find("difficult").text == "1"))
        bndbox = obj.find("bndbox")
        xmax.append(float(bndbox.find("xmax").text) / width)
        xmin.append(float(bndbox.find("xmin").text) / width)
        ymax.append(float(bndbox.find("ymax").text) / height)
        ymin.append(float(bndbox.find("ymin").text) / height)
      return xmin, xmax, ymin, ymax, label, pose, is_truncated, is_difficult


class SegDatumGenerator(DatumGenerator):
  """Generator for image Segmentation problem.

  This generator expects input data in the Pascal VOC segmentation data format.
  For each single image there should be a single segmentation map image with class id as
  pixel values.

  It expects a input data path with the following format:

  + data_dir:
      - JPEGImages (all input images for all the splits.)
      - SegmentationClass (all segmentation label map images.)

  While the overall directory levels should be as shown in the format, sub-directory names can
  be controlled by passing keyword argument to `__call__` method.

  Following inputs for kwargs are accepted when calling the object:

  Kwargs:
    split: split name.
    image_dir: name of the directory with input images.
    label_dir: name of the directory with segmentation label map images.
    image_extension: extension of the input images.
    label_extension: extension of the label images.
  """

  def generate_datum(self, **kwargs: Any) -> GeneratorReturnType:
    """Single example generator from data in the storage path.

    Args:
      kwargs: Optional, keyword arguments to control directory names and exensions.

      Followings kwargs are supported:

      split: split name.
      image_dir: name of the directory with input images.
      label_dir: name of the directory with segmentation label map images.
      image_extension: extension of the input images.
      label_extension: extension of the label images.

    Returns:
     a tuple containing an unique example id and a dict with keys as feature names and
     values as feature values.
    """
    split = kwargs.get('split')
    if not split:
      raise ValueError('Pass a valid split name to generate data.')
    set_dir = kwargs.get('set_dir')
    image_dir = kwargs.get('image_dir', 'JPEGImages')
    label_dir = kwargs.get('label_dir', 'SegmentationClass')
    image_extension = kwargs.get('image_extension', '.jpg')
    label_extension = kwargs.get('label_extension', '.png')
    set_filepath = os.path.join(self.path, split + '.txt')
    if set_dir:
      set_filepath = os.path.join(self.path, set_dir, split + '.txt')
    with tf.io.gfile.GFile(set_filepath, "r") as f:
      data = [line.strip() for line in f]
    for image_id in data:
      datum = {
          'image': os.path.join(self.path, image_dir, image_id + image_extension),
          'label': os.path.join(self.path, label_dir, image_id + label_extension),
      }
      yield image_id, datum
