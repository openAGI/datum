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
from typing import Any, Union

from datum.configs import ConfigBase
from datum.utils.common_utils import AttrDict, add_metaclass
from datum.utils.types_utils import GeneratorReturnType


@add_metaclass(abc.ABCMeta)
class DatumGenerator():
  """Input data generator abstract interface. Derived classes have to implement geenrate_datum
  method, which returns a generator with two return values.

  Args:
    path: a path to the data store location.
    gen_config: configs for generator.
  """

  def __init__(self, path: str, gen_config: Union[AttrDict, ConfigBase] = None):
    self.path = path
    self.gen_config = gen_config

  def __call__(self, **kwargs: Any) -> GeneratorReturnType:
    """Returns a generator to iterate over the processed input data."""
    return self.generate_datum(**kwargs)

  @abc.abstractmethod
  def generate_datum(self, **kwargs: Any) -> GeneratorReturnType:
    """Returns a generator to iterate over the processed input data."""
    raise NotImplementedError
