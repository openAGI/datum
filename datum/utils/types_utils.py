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

from typing import Callable, Dict, Generator, List, Union

import numpy as np
import tensorflow as tf

ValueType = Union[int, float, str, bytes, List[Union[int, float, str]]]
DatumType = Dict[str, Union[str, int, bytes, float, List[int], List[float], List[str], np.ndarray]]
GeneratorReturnType = Generator[Union[Union[str, int], Dict], None, None]
DatasetType = tf.data.Dataset
FileInstructionDict = Dict[str, Union[str, int]]
ParseFn = Callable[[tf.train.Example], Dict[str, tf.Tensor]]
