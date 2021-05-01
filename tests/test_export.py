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
import os
import tempfile

import pytest

from datum.configs import TFRWriteConfigs
from datum.export import export
from datum.problem import types


@pytest.mark.parametrize(
    "problem_type,input_data",
    [
        (types.IMAGE_CLF, "tests/dummy_data/clf"),
        (types.IMAGE_DET, "tests/dummy_data/det/voc"),
        (types.IMAGE_SEG, "tests/dummy_data/seg/voc"),
    ],
)
def test_export_to_tfrecord(problem_type, input_data):
  with tempfile.TemporaryDirectory() as tempdir:
    write_configs = TFRWriteConfigs()
    write_configs.splits = {
        "train": {
            "num_examples": 1
        },
        "val": {
            "num_examples": 1
        },
    }
    export.export_to_tfrecord(input_data, tempdir, problem_type, write_configs)
    files = sorted(os.listdir(tempdir))
    assert [
        "datum_to_type_and_shape_mapping.json",
        "shard_info.json",
        "train-00000-of-00001.tfrecord",
        "val-00000-of-00001.tfrecord",
    ] == files
