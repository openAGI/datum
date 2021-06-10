# Copyright 2021 The OpenAGI Datum Authors.
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
"""Default write configs for TFRecord export."""

import os
from functools import partial
from pathlib import Path
from typing import Optional

from datum.configs import ConfigBase, TFRWriteConfigs
from datum.encoder.encoder import datum_name_to_encoder
from datum.problem import problem
from datum.serializer.serializer import DatumSerializer
from datum.utils.common_utils import AttrDict


def get_default_write_configs(problem_type: str,
                              label_names_file: Optional[str] = None) -> ConfigBase:
  """Returns default write configs for a problem.

  Args:
    problem_type: Type of the problem,  any one from `datum.problems.types`.
    label_names_file: Path to the label name file, required for `IMAGE_DET` problem.

  Returns:
    A `ConfigBase` config object.

  Raises:
    ValueError: If label_names_file is not valid, raised only for `IMAGE_DET` problem.
  """
  serializer = DatumSerializer(problem.PROBLEM_PARAMS[problem_type]["serializer"],
                               datum_name_to_encoder_fn=datum_name_to_encoder)
  if problem_type == problem.IMAGE_DET:
    if not label_names_file:
      raise ValueError("label_names_file must be provided for `IMAGE_DET` problem.")
    if not Path(label_names_file).is_file():
      raise ValueError(f"Input {label_names_file} does not exist or not a file.")

    class_map = {
        name: idx + 1
        for idx, name in enumerate(open(os.path.join(label_names_file)).read().splitlines())
    }
    gen_config = AttrDict(has_test_annotations=True, class_map=class_map)
  else:
    gen_config = None
  generator = partial(problem.PROBLEM_PARAMS[problem_type]["generator"], gen_config=gen_config)
  write_configs = TFRWriteConfigs()
  write_configs.serializer = serializer
  write_configs.generator = generator
  return write_configs
