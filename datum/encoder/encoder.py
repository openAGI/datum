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

import abc
from typing import Any, Dict

import tensorflow as tf

from datum.utils.common_utils import add_metaclass
from datum.utils.types_utils import ValueType


@add_metaclass(abc.ABCMeta)
class Encoder():
  """Feature Encoder abstract interface. Derived classes have to implement the encode method for
  encoding.

  Args:
    kwargs: Optional arguments required to implement encode method.
  """

  def __init__(self, **kwargs: Any):
    self.kwargs = kwargs

  def __call__(self, inputs: ValueType) -> ValueType:
    """Encode input data to required format.

    Args:
      inputs: inputs data to encode.

    Returns:
      encoded data.
    """
    return self.encode(inputs)

  @abc.abstractmethod
  def encode(self, inputs: ValueType) -> ValueType:
    """Encode input data to required format.

    Args:
      inputs: inputs data to encode.

    Returns:
      encoded data.
    """
    raise NotImplementedError


class ImageEncoder(Encoder):

  def encode(self, inputs: ValueType) -> ValueType:
    """Image encoder.

    Args:
      inputs: input image absolute path.

    Returns:
      a bytes string representation of the input image.
    """
    with tf.io.gfile.GFile(inputs, 'rb') as image_f:
      return image_f.read()


class NumberEncoder(Encoder):

  def encode(self, inputs: ValueType) -> ValueType:
    """Encode integer or floating point number.

    Currently returns inputs as outputs, as no processing required.
    """
    return inputs


class StringEncoder(Encoder):
  """String encoder.

  For image related problems it will just return the input text. The main objective of this encoder
  is to comvert input string to vector representation, which will be implemented on a go forward
  basis.
  """

  def encode(self, inputs: ValueType) -> ValueType:
    """String encoder.

    Currently it doesnt implement any encoder.
    Args:
      inputs: input string.

    Returns:
      encoded output.
    """
    if self.kwargs.get('problem_type') == 'text':
      # in future a tokenizer maybe implemented if required.
      return inputs
    return inputs


class GraphEncoder(Encoder):
  """Graph data encoder.

  This encoder can be used convert graph data into matrix and vector, list representation.
  """

  def encode(self, inputs: ValueType) -> ValueType:
    """Graph data encoder.

    Currently it doesnt implement any encoder.

    Args:
      inputs: input graph data.

    Returns:
      encoded graph data.
    """
    return inputs


def datum_name_to_encoder(datum: Dict, problem_type: str) -> Dict[str, Encoder]:
  """Automatically identify encoder based on data values and problem type.

  Args:
    datum: a dict with feature name as keys and feature data as values.
    problem_type: type of the problem. Whether the problem is related to image/text/grpah etc.

  Returns:
    a dict, mapping feature name to encoder object.
  """
  return {key: _get_encoder_type(value, problem_type) for key, value in datum.items()}


def _get_encoder_type(value: ValueType, problem_type: str) -> Encoder: # type: ignore
  """Get feature encoder based on feature value and problem type.

  Args:
    value: input feature value.
    problem_type: type of the input problem.

  Returns:
    an Encoder object.

  Raises:
    ValueError, if value type is not supported.
  """
  if isinstance(value, (list, tuple)):
    return _get_encoder_type(value[0], problem_type)
  else:
    if isinstance(value, (int, float)):
      return NumberEncoder()
    elif isinstance(value, str):
      if value.endswith(('.png', '.jpg')):
        if problem_type == 'image':
          return ImageEncoder()
        return StringEncoder(problem_type=problem_type)
      elif problem_type in ('text', 'image'):
        return StringEncoder(problem_type=problem_type)
      elif problem_type == 'graph':
        return GraphEncoder()
    else:
      raise ValueError('Input object is not supported.')
