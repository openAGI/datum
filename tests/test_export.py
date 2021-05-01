import os
import tempfile

import pytest

from datum.configs import TFRWriteConfigs
from datum.export import export
from datum.problem import types


@pytest.mark.parametrize("problem_type,input_data", [(types.IMAGE_CLF, "tests/dummy_data/clf"),
                                                     (types.IMAGE_DET, "tests/dummy_data/det/voc"),
                                                     (types.IMAGE_SEG, "tests/dummy_data/seg/voc")])
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
    files = os.listdir(tempdir)
    assert [
        'val-00000-of-00001.tfrecord', 'train-00000-of-00001.tfrecord', 'shard_info.json',
        'datum_to_type_and_shape_mapping.json'
    ] == files
