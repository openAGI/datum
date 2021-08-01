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

from absl import logging

from datum.configs import ConfigBase
from datum.configs.default_configs import get_default_write_configs
from datum.problem import types
from datum.writer.tfrecord_writer import TFRecordWriter


def export_to_tfrecord(input_path: str, output_path: str, problem_type: str,
                       write_configs: ConfigBase) -> None:
  """Export data to tfrecord format.

  Args:
    input_path: Root path to input data folder.
    output_path: Path to store output tfrecords and generated metadata.
    problem_type: Type of the problem, see `datum.probelm.types` for available problems.
    write_configs: Configuration for tfrecord writing.

    write_configs has the following configurable attributes:

    generator: Generator class.
    serializer: Serializer instance.
    splits: A dict with split names as keys and split attributes as values.

    Following split attributes are supported:

    num_examples: Number of examples in the split.
    extension: Input image extension in case of image data, all input should have same
      extension. Default - For image data, `.jpg`
    image_dir: Name of the directory containing the data, used for image classification.
      Default - split name, `train` for classification, for detection `JPEGImages` as per
        VOC12 folder structure.
    csv_path: Path to ground truths csv file, used for classification dataset.
      Default - split name with .csv extension, example - `train.csv`
    set_dir: In case of VOC12 style  datasets, image set information.
      Default - `ImageSets` as per VOC12 dataset folder structure
    annotation_dir: Directory with annotations, used for VOC12 style datasets.
      Default - `Annotations` as per VOC12 dataset folder structure
    label_dir: Directory with label images, used in segmentation.
      Default - `SegmentationClass` for as per VOC12 folder structure.
    image_extension: Extension of input images, used in segmentation.
      Default - `.jpg`
    label_extension: Extension of label images, used in segmentation.
      Default - `.png`

    Raises:
      ValueError: If splits information is not in the dict format.
  """
  label_names_file = None
  if problem_type == types.IMAGE_DET:
    label_names_file = os.path.join(input_path, "classes.names")
  base_write_configs = get_default_write_configs(problem_type, label_names_file)
  write_configs = base_write_configs.merge(write_configs)
  splits = write_configs.splits
  if not isinstance(splits, dict):
    raise ValueError(f"Splits must be a dict in the input config: {write_configs}")
  generator = write_configs.generator(input_path)
  Path(output_path).mkdir(parents=True, exist_ok=True)
  for split, split_kwargs in splits.items():
    logging.info(f'Creating tfrecord writer for split: {split}.')
    tfr_writer = TFRecordWriter(generator,
                                write_configs.serializer,
                                output_path,
                                split,
                                split_kwargs["num_examples"],
                                sparse_features=write_configs.sparse_features,
                                **split_kwargs)
    logging.info('Starting conversion process.')
    tfr_writer.create_records()
    logging.info(f'Completed tfrecord conversion for input split: {split}')
