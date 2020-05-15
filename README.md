# datum

Datum provides APIs to create tfrecord daatsets and read tfrecord as `tf.data.Datasets`

## Introduction

TFRecord enables efficient handling of small or large datasets. Samples of datasets are stored in serialized binary string format.
The purpose of this library to make it easier for end-user to create and read tfrecord datasets effortlessly.


## Getting Started

### Installation

#### Using pip
```Shell
pip install datum
```

#### For development
```Shell
git clone https://github.com/openagi/datum.git
cd datum
conda env create -f environment.yml
conda activate datum
```

### Create tfeecord dataset 
Dataset can be created by using the following command
```Shell
python datum/create_tfrecord.py --input_path <input_data path> --output_path <output_path> --config_path <path to config file>
```

`config_path` can be used to set problem specific generator and serializer for that dataset. Sample configs can be found in `configs` dir.

you can create your own config file, for example:
```Python
# test_config.py
# a config file for generating tfrecord for image classification data
import tensorflow as tf

from datum.encoder.encoder import datum_name_to_encoder
from datum.generator.image import ClfDatumGenerator
from datum.serializer.serializer import DatumSerializer
from datum.utils.common_utils import AttrDict

config = {
    'generator': ClfDatumGenerator,
    'sprase_features': [],
    'serializer': DatumSerializer('image', datum_name_to_encoder_fn=datum_name_to_encoder),
    'splits': ['train', 'val'],
    'num_examples': {
        'train': 2000,
        'val': 1000,
    },
cnf = AttrDict(config)
```


### Load tfrecord dataset as tf.data.Dataset
Datset can be loaded as tf.data.Dataset as follows

```Python
from datum.reader import load

# Load data
dataset = load(<path_to_tfrecord_dir>)
   
# Get training dataset iterator
train_dataset = dataset.train_fn('train', shuffle=True)

# access the data
for batch in train_dataset:
  # pass to training loop

# Read config can be changed by accesing the dataset_configs attribute
dataset_configs = dataset.dataset_configs
dataset_configs.batch_size_train = 32

# sample can be processed using `pre_batching_callback` and `post_batch_callback` fns.
datset_configs.pre_batching_callback = lambda example: <your_callback_fn(example, <*kwargs>)>
# this callback fucntion should be able to handle batch of examples
datset_configs.post_batching_callback = lambda examples: <your_callback_fn(examples, <*kwargs>)>

# update configs before iterating over the dataset
dataset.daatset_configs = dataset_configs
train_dataset = dataset.train_fn('train', False)
```


## Want a certain feature?

Request a feature by opening an issue


*`datum` is Apache 2.0 licensed. See the LICENSE file.*
