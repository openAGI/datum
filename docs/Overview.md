### Create tfrecord for image classification problem

For image classification problem `datum` expects input data in the following format:

    * data_path
      * train (folder with training images, named after split)
      * val (folder with validation images, named after split)
      * test (folder with test images, named after split)
      * train.csv (csv file with columns data as label with respect to filename
        (filename without extension) )
	  a sample val.csv can have the following format:
				
	    filename, label_name1, label_name2, ...., label_nameN
	    test_image1, 1, 2, ..., 1.1
	    test_image1, 1, 2, ..., 1.3
				
      * val.csv (csv file with columns data as label with respect to filename
            (filename without extension) )
	  a sample val.csv can have the following format:
	
             filename, label_name1, label_name2, ...., label_nameN
	     test_image3, 4, 1, ..., 1.1
	     test_image4, 3, 0, ..., 0.1
			
      * test.csv (csv file with columns data as label with respect to filename
            (filename without extension) )	  
	  a sample val.csv can have the following format:
	
	     filename, label_name1, label_name2, ...., label_nameN
	     test_image5, 3, 2, ..., 0.2
	     test_image6, 5, 2, ..., 1.1

  It is not mandatory to have all the folders and csv files named after split name. You can control
  the folder name by passing it as input the __call__ method.
  For a particular split, image folder name, labels csv fllename, data extension can be
  controlled by passing the following keyword arguments the __call__ method.
  All sub directory path are relative to the root path.
    Following inputs for kwargs are accepted:
		
      * split: name of the split.
      * extension: image extension, defualt is '.jpg'.
      * image_dir: directory name containing the image, default name is split name.
      * csv_path: labels filename, default name is `<split>.csv`

#### create a config file 
a sample config file [image_clf_configs.py](https://github.com/openagi/datum/blob/master/configs/image_clf_configs.py) is
provided with datum.

This config file can be modified as per your requirements. If you want to use different folder name for a split or a
different csv_path that can be configured by using `gen_kwargs` in the config file.

```Python
config = {
    'generator': partial(ClfDatumGenerator, gen_config=None),
    'sprase_features': [],
    'gen_kwargs': {'image_dir': 'development', 'csv_path': 'development_labels.csv'},
    'serializer': DatumSerializer('image', datum_name_to_encoder_fn=datum_name_to_encoder),
    'splits': ['train', 'val'],
    'num_examples': {
        'train': 1,
        'val': 1,
    },
cnf = AttrDict(config)

```

### Create tfrecord for image object detection problem

For image object detection problem data to be stored in the Pascal VOC data format in the
  input storage location.

  For each input example image, corresponding labels should be stored in a xml file, if
  labels loading is enabled.
  Input data should be stored in the following format:
	
    * data_dir
      * JPEGImages (all images, any number of split, stored together)
      * Annotations (All annotations for detection, .xml format)
      * ImageSets (Splits file, txt files with split name, each line contain name of the
         image to use use for that split
         e.g: image1\n image2\n etc)
  it is not mandatory to keep the folder as it is. Folder names can be customized, but overall
  directory levels should be maintained - subfoldwers should exist under the root data dir.

  Subfolders and extension names can be controlled by passing kwargs in the __call__ method.
  Following kwargs are supported:
  
    * split: name of the split.
    * extension: image extension.
    * set_dir: directory name where split files are stored.
    * image_dir: directory name where images are stored.
    * annotation_dir: directory name where xml annotation files are stored.

#### create a config file 
a sample config file [image_det_configs.py](https://github.com/openagi/datum/blob/master/configs/image_det_configs.py) is
provided with datum.

This config file can be modified as per your requirements. If you want to use different folder name for image dir or a
different annotation labesl directory that can be configured by using `gen_kwargs` in the config file.

Labels names should be stored in a text file, each line having a single label name as follows
```Python
# LABEL_NAMES_FILE
person
car
phone
```

```Python
LABEL_NAMES_FILE = 'tests/dummy_data/det/voc/voc2012.names'

class_map = {
    name: idx + 1
    for idx, name in enumerate(open(os.path.join(LABEL_NAMES_FILE)).read().splitlines())
}
config = {
    'generator':
    partial(DetDatumGenerator, gen_config=AttrDict(has_test_annotations=True, class_map=class_map)),
    'sprase_features': [],
    'serializer':
    DatumSerializer('image', datum_name_to_encoder_fn=datum_name_to_encoder),
    'gen_kwargs': {'image_set': 'ImageSets', 'extension': '.jpg'},
    'splits': ['train', 'val'],
    'num_examples': {
        'train': 1,
        'val': 1,
    }
}

cnf = AttrDict(config)
```

### Create tfrecord for image segmentation problem

To create tfrecord for image segmentation problem,  input data should be in the Pascal VOC segmentation data format.
For each single image there should be a single segmentation map image with class id as pixel values.
  It expects a input data path with the following format:
	
    * data_dir:
        * JPEGImages (all input images for all the splits.)
        * SegmentationClass (all segmentation label map images.)
  While the overall directory levels should be as shown in the format, sub-directory names can
  be controlled by passing keyword argument to `__call__` method (gen_kwargs in the config file)
  Followings kwargs are supported:
	
    * split: split name.
    * image_dir: name of the directory with input images.
    * label_dir: name of the directory with segmentation label map images.
    * image_extension: extension of the input images.
    * label_extension: extension of the label images.

#### create a config file 
a sample config file [image_seg_configs.py](https://github.com/openagi/datum/blob/master/configs/image_seg_configs.py) is
provided with datum.

```Python
config = {
    'generator': partial(SegDatumGenerator, gen_config=None),
    'sprase_features': [],
    'serializer': DatumSerializer('image', datum_name_to_encoder_fn=datum_name_to_encoder),
    'gen_kwargs': {'image_dir': 'my_images', 'label_dir': 'my_labels'},
    'splits': ['train', 'val'],
    'num_examples': {
        'train': 1,
        'val': 1,
    }
}

cnf = AttrDict(config)
```

### Create tfrecord for text classification problem
To create tfreord for text classification or generative modeling data should be in json
  format with each of the examples keyed using an unique id. Each example should have two
  mandatory attributes: `text` and `label` (it is a nested attribute).
  For example a sample json file would looks as follows:
	
    train.json:
    {1: {'text': 'I am the one', 'label': {'polarity': 1}},
    ...
    N: {'text': 'Such a beautiful day', 'label': {'polarity': 2}}
    }

  Input path should have json files for training/development/validation.
  By default the generator search for json file named after split name, but it can be configured
  by using the keyword argument `json_path`.
  Following are the supported keyword arguments:
	
    * split: name of the split
    * json_path:name of the json file for that split, this is a relative path with respect to
      parent `self.path`.

#### create a config file 
a sample config file [text_json_configs.py](https://github.com/openagi/datum/blob/master/configs/text_json_configs.py) is
provided with datum.

```Python

config = {
    'generator': partial(TextJsonDatumGenerator, gen_config=None),
    'sprase_features': [],
    'serializer': DatumSerializer('text', datum_name_to_encoder_fn=datum_name_to_encoder),
    'gen_kwargs': {'json_path': 'train_data.json'},
    'splits': ['test'],
    'num_examples': {
        'train': 1,
        'val': 1,
    },
}

cnf = AttrDict(config)
```
