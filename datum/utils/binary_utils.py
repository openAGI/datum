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

from typing import Tuple

import tensorflow as tf


def is_binary_image(string: tf.Tensor) -> Tuple[bool, str]:
  """Determine image compression type using a binary string tensor/object.

  Args:
    string: binary string, can be `tf.Tensor` or python format..

  Returns:
    a tuple containing a flag denoting whether input string is an image and the corresponding
      extension (if its an image, else empty).
  """
  if not isinstance(string, (bytes, tf.Tensor)):
    raise ValueError(f'Input {string} is not a bytes string or `tf.Tensor`.')
  if isinstance(string, tf.Tensor):
    string = string.numpy()
  if string.startswith(b'\xff\xd8\xff'):
    return True, 'jpg'
  elif string.startswith(b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'):
    return True, 'png'
  elif string.startswith(b'bm'):
    return True, 'bmp'
  else:
    return False, ''
