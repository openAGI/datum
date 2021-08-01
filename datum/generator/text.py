# coding=utf-8
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

import json
import os
from ast import literal_eval
from typing import Any

import tensorflow as tf

from datum.generator.generator import DatumGenerator
from datum.utils.types_utils import GeneratorReturnType


class TextJsonDatumGenerator(DatumGenerator):
  """Text problem datum generator from json file.

  This can be used for classification or generative modeling. This expect data to be in json
  format with each of the examples keyed using an unique id. Each example should have two
  mandatory attributes: `text` and `label` (it is a nested attribute).

  Input path should have json files for training/development/validation.
  By default the generator search for json file named after split name, but it can be configured
  by using the keyword argument `json_path` to `__call__`.

  + data_path
      - train.json (json file containing the training data)
        For example a sample json file would looks as follows:
        ```
            {1: {'text': 'I am the one', 'label': {'polarity': 1}},
            ...
            N: {'text': 'Such a beautiful day', 'label': {'polarity': 2}}
            }
        ```

      - val.json (json file containing the val data)
      - test.json (json file containing the test data)

  Following are the supported keyword arguments:

  Kwargs:
    split: name of the split
    json_path:name of the json file for that split, this is a relative path with respect to
      parent `self.path`.
  """

  def generate_datum(self, **kwargs: Any) -> GeneratorReturnType:
    """Returns a generator to get datum from the input source.

    Args:
      kwargs: optional keyword arguments for customization.

      Following are the supported keyword arguments:

      split: name of the split
      json_path:name of the json file for that split, this is a relative path with respect to
        parent `self.path`.

    Returns:
      a tuple of a unique id and a dictionary with feature names as keys and feature values as
         values.
    """
    split = kwargs.get('split')
    if not split:
      raise ValueError('Pass a valid split name to generate data `__call__` method.')
    json_path = kwargs.get('json_path', split + '.json')
    with tf.io.gfile.GFile(os.path.join(self.path, json_path)) as json_f:
      for key, value in json.load(json_f).items():
        datum = {'text': value['text']}
        for label_key, val in value['label'].items():
          try:
            datum[label_key] = literal_eval(val)
          except ValueError:
            datum[label_key] = val
        yield key, datum
