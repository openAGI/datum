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

from typing import Any, Callable, Dict

import numpy as np
import tensorflow as tf

from datum.encoder.encoder import Encoder, datum_name_to_encoder
from datum.utils.common_utils import is_string, try_reraise, zip_dict
from datum.utils.types_utils import DatumType


class DatumSerializer():
  """Datum serializer. Encode data into serialized binary string.

  Args:
    problem_type: type of the problem, e.g: image/text/graph etc.
    datum_name_to_encoder_fn: a callable used to get encoder object for each feature.
  """

  def __init__(self,
               problem_type: str,
               datum_name_to_encoder_fn: Callable[[DatumType, str], Dict[str, Encoder]] = None):
    self.problem_type = problem_type
    self.feature_converter = datum_name_to_encoder_fn or datum_name_to_encoder
    self.serializer = serialize_datum

  def __call__(self, datum: DatumType) -> bytes:
    """Convert a datum to serialized binary string.

    Args:
      a dict with feature name to value,

    Returns:
      a serialized binary string.
    """
    feature_to_encoder = self.feature_converter(datum, self.problem_type)
    encoded_datum = {key: value[0](value[1]) for key, value in zip_dict(feature_to_encoder, datum)}
    return self.serializer(encoded_datum)


def serialize_datum(encoded_datum: DatumType) -> bytes:
  """Serialize the given example.

  Args:
    datum: Nested `dict` containing the input to serialize.

  Returns:
    bytes, the serialized `tf.train.Example` string.
  """
  example = datum_to_tf_example(encoded_datum)
  return example.SerializeToString()


def datum_to_tf_example(datum: DatumType) -> tf.train.Example:
  """Builds tf.train.Example from (string -> int/float/str list) dictionary.

  Args:
    datum: `dict`, dict of values, tensor,...

  Returns:
    a `tf.train.Example`, the encoded example proto.
  """

  def run_with_reraise(fn: Callable, feature_key: str, feature_value: Any) -> tf.train.Feature:
    with try_reraise(f'Error while serializing feature {feature_key}: {feature_value}'):
      return fn(feature_value)

  example_dict = {
      feature_key: run_with_reraise(_item_to_tf_feature, feature_key, feature_value)
      for feature_key, feature_value in datum.items()
  }

  return tf.train.Example(features=tf.train.Features(feature=example_dict))


def _item_to_tf_feature(item: Any) -> tf.train.Feature:
  """Single item to a tf.train.Feature.

  Args:
    item: input value for encoding into `tf.train.Feature` object.

  Returns:
    an encoded `tf.train.Feature` object.

  Raises:
    ValueError: if the data type of input is not supported.
  """
  item = np.array(item)

  if item.dtype == np.bool_:
    item = item.astype(int)

  item = item.flatten()
  if np.issubdtype(item.dtype, np.integer):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=item))
  elif np.issubdtype(item.dtype, np.floating):
    return tf.train.Feature(float_list=tf.train.FloatList(value=item))
  elif is_string(item):
    item = [tf.compat.as_bytes(x) for x in item]
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=item))
  else:
    raise ValueError("Unsupported value: {}.\n"
                     "tf.train.Feature does not support type {}. "
                     "unsupported value as input.".format(repr(item), repr(type(item))))
