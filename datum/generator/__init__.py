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

from datum.generator.generator import DatumGenerator
from datum.generator.image import (ClfDatumGenerator, DetDatumGenerator, SegDatumGenerator)
from datum.generator.text import TextJsonDatumGenerator
from datum.utils.common_utils import deserialize_object

# aliases
clf = CLF = ClfDatumGenerator
det = DET = DetDatumGenerator
seg = SEG = SegDatumGenerator
textjson = TEXTJSON = TextJsonDatumGenerator


def deserialize(name: str) -> DatumGenerator:
  """Deserializer for generator.

  Args:
    name: name of the generator class or aliases

  Returns:
    deserialized class representing the input name.
  """
  return deserialize_object(name, module_objects=globals(), printable_module_name='Generator class')
