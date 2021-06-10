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
from functools import reduce
from typing import Any, Dict, List

import tensorflow as tf

from datum.utils.common_utils import memoized_property


class DatumParser():
  """TFRecord Example parser.

  This api can be used to deserialize tfrecord example data.

  Args:
    path: path to the dir, where tfrecord metadata json file is stored.
  """

  def __init__(self, path: str):
    self._path = path
    self.datum_to_type_shape = self.load_datum_type_shape_mapping(path)
    self.pytype_to_tftype = {
        'int': tf.int64,
        'float': tf.float32,
        'string': tf.string,
    }

  def load_datum_type_shape_mapping(self, path: str) -> Dict[str, Dict[str, Any]]:
    """Load datum type and shape mapping. Feature shae and types are required to deserialize tfrecord
    serialized binary string data.

    Args:
      path: path to the dir, where tfrecord metadata json file is stored.

    Returns:
      a mapping, feature name to corresponding shape and data type.
    """
    with tf.io.gfile.GFile(os.path.join(path, 'datum_to_type_and_shape_mapping.json'),
                           'r') as json_f:
      return json.load(json_f)

  @memoized_property
  def names_to_feature_type(self) -> Dict[str, tf.train.Feature]:
    """Feature name to feature type mapping, passed as input to example parsing fn.

    Returns:
      a mapping, feature name to tf.train.Feature type.
    """
    mapping = {}
    for key, value in self.datum_to_type_shape.items():
      if value['dense']:
        if value['type'] == 'string':
          mapping[key] = tf.io.FixedLenFeature([], self.pytype_to_tftype[value['type']])
        else:
          mapping[key] = tf.io.FixedLenFeature(self.wrap_shape(value['shape']),
                                               self.pytype_to_tftype[value['type']])
      else:
        mapping[key] = tf.io.VarLenFeature(self.pytype_to_tftype[value['type']])
    return mapping

  def wrap_shape(self, shape: List[int]) -> List[int]:
    """Convert a list of shape to a single element by multiplying all the entries.

    Args:
      shape: input shape.

    Returns:
      output reduced shape.
    """
    if shape:
      return reduce(lambda x, y: x * y, shape) # type: ignore
    return shape

  def parse_fn(self, example: tf.train.Example) -> Dict[str, tf.Tensor]:
    """Parse a single example from serialized binary string.

    Args:
      example: input tf.train.Example.

    Returns:
      a dict, deserialized example data, feature name to value.
    """
    parsed_example = tf.io.parse_single_example(example, self.names_to_feature_type)
    return self.decode_example(parsed_example)

  def decode_example(self, parsed_example: Dict[str, tf.Tensor]) -> Dict[str, tf.Tensor]:
    """Decode deserialized example. Used to retrieve feature original shape and value.

    Args:
      parsed_example: parsed deserialize example.

    Returns:
      a dict, deserialized example data, feature name to value.
    """
    deserialized_outputs = {}
    for key, value in parsed_example.items():
      dtype = self.pytype_to_tftype[self.datum_to_type_shape[key]['type']]
      if dtype == tf.string:
        if len(self.datum_to_type_shape[key]['shape']) == 2:
          deserialized_outputs[key] = tf.io.decode_jpeg(value, 1)
        elif len(self.datum_to_type_shape[key]['shape']) == 3:
          deserialized_outputs[key] = tf.io.decode_jpeg(value, 3)
        elif self.datum_to_type_shape[key]['dense']:
          deserialized_outputs[key] = value
        else:
          deserialized_outputs[key] = tf.sparse.to_dense(value)
      else:
        original_shape = self.datum_to_type_shape[key]['shape']
        if len(original_shape) >= 2:
          if key + '_shape' in parsed_example:
            deserialized_outputs[key] = tf.reshape(tf.sparse.to_dense(value),
                                                   parsed_example[key + '_shape'])
          else:
            if self.datum_to_type_shape[key]['dense']:
              deserialized_outputs[key] = tf.reshape(value, original_shape)
            else:
              deserialized_outputs[key] = tf.reshape(tf.sparse.to_dense(value), original_shape)
        else:
          if self.datum_to_type_shape[key]['dense']:
            deserialized_outputs[key] = value
          else:
            deserialized_outputs[key] = tf.sparse.to_dense(value)
    return deserialized_outputs
