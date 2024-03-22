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

from collections.abc import Generator
from typing import Callable, Union

import numpy as np
import tensorflow as tf

ValueType = Union[int, float, str, bytes, list[Union[int, float, str]]]
DatumType = dict[str, Union[str, int, bytes, float, list[int], list[float], list[str], np.ndarray]]
GeneratorReturnType = Generator[Union[Union[str, int], dict], None, None]
DatasetType = tf.data.Dataset
FileInstructionDict = dict[str, Union[str, int]]
ParseFn = Callable[[tf.train.Example], dict[str, tf.Tensor]]
