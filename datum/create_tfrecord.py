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

from pathlib import Path
from typing import Any

from absl import app, flags, logging

from datum.utils.common_utils import load_module
from datum.writer.tfrecord_writer import TFRecordWriter

flags.DEFINE_string('output_path', None, 'Path to store the tfrecord files.')
flags.DEFINE_string('input_path', None, 'Path to the input files.')
flags.DEFINE_string('splits', None,
                    'Single split name or comma seperated multiple split names for conversion.')
flags.DEFINE_string('config_path', None, 'Path to the configuration file for tfrecord conversion.')
FLAGS = flags.FLAGS


def main(_: Any) -> None:
  logging.info('Loading datum comversion configuration file.')
  config = load_module('config', FLAGS.config_path).cnf
  splits = config.splits
  if FLAGS.splits:
    splits = FLAGS.splits.split(',')
  generator = config.generator(FLAGS.input_path)
  Path(FLAGS.output_path).mkdir(parents=True, exist_ok=True)
  for split in splits:
    logging.info(f'Creating tfrecord writer for split: {split}.')
    tfr_writer = TFRecordWriter(generator,
                                config.serializer,
                                FLAGS.output_path,
                                split,
                                config.num_examples.get(split),
                                sparse_features=config.sparse_features,
                                **config.gen_kwargs)
    logging.info('Starting conversion process.')
    tfr_writer.create_records()
    logging.info(f'Completed tfrecord conversion for input split: {split}')


if __name__ == '__main__':
  logging.set_verbosity(logging.INFO)
  app.run(main)
