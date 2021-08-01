<!-- markdownlint-disable -->

<a href="../../datum/generator/image.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `generator.image`






---

<a href="../../datum/generator/image.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ClfDatumGenerator`
Image classification problem data generator. 

An object of this class can be used to iterate over data stored in a specified folder in the host device in a specified format. 

Typically this generator expect the input data to be stored in the following format: 

+ data_path 
    - train (folder with training images, named after split) 
    - val (folder with validation images, named after split) 
    - test (folder with test images, named after split) 
    - train.csv (csv file with columns data as label with respect to filename  (filename without extension) ) ```
         filename, label_name1, label_name2, ...., label_nameN
         test_image1, 1, 2, ..., 1.1
         test_image1, 1, 2, ..., 1.3
      ``` 


    - val.csv (csv file with columns data as label with respect to filename  (filename without extension) ) 
    - test.csv (csv file with columns data as label with respect to filename  (filename without extension) ) 

It is not mandatory to have all the folders and csv files named after split name. You can control the folder name by passing it as input the `__call__` method. For a particular split, image folder name, labels csv fllename, data extension can be controlled by passing the following keyword arguments the `__call__` method. 

All sub directory path are relative to the root path. 

Following inputs for kwargs are accepted when calling the object: 



**Kwargs:**
 
 - <b>`split`</b>:  name of the split. 
 - <b>`extension`</b>:  image extension, defualt is '.jpg'. 
 - <b>`image_dir`</b>:  directroy name containing the image, default name is split name. 
 - <b>`csv_path`</b>:  labels filename, default name is `<split>.csv` 




---

<a href="../../datum/generator/image.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `generate_datum`

```python
generate_datum(
    **kwargs: Any
) → Generator[Union[str, int, Dict], NoneType, NoneType]
```

Yields Example instances from given CSV. 



**Args:**
 
 - <b>`kwargs`</b>:  Optional kwargs for further input data format customization. 

Following inputs for kwargs are accepted: 


 - <b>`split`</b>:  name of the split. 
 - <b>`extension`</b>:  image extension, defualt is '.jpg'. 
 - <b>`image_dir`</b>:  directroy name containing the image, default name is split name. 
 - <b>`csv_path`</b>:  labels filename, default name is `<split>.csv` 



**Returns:**
 a tuple of datum id and a dict with key as feature name and values as feature values. 


---

<a href="../../datum/generator/image.py#L106"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DetDatumGenerator`
Image object Detection problem data generator. 

This generator expect image data to be stored in the Pascal VOC data format in the input storage location. 

For each input example image, corresponding labels should be stored in a xml file, if labels loading is enabled. 

Input data should be stored in the following format 

+ data_dir 
     - JPEGImages (all images, any number of split, stored together) 
     - Annotations (All annotations for detection, .xml format) 
     - ImageSets (Splits file, txt files with split name, each line contain name of the  image to use use for that split  e.g. image1 image2 etc) 

While the overall directory levels should be as shown in the format, sub-directory names can be controlled by passing keyword argument to `__call__` method. 

Following inputs for kwargs are accepted when calling the object: 



**Kwargs:**
 
  - <b>`split`</b>:  name of the split. 
  - <b>`extension`</b>:  image extension. 
  - <b>`set_dir`</b>:  directory name where split files are stored. 
  - <b>`image_dir`</b>:  directory name where images are stored. 
  - <b>`annotation_dir`</b>:  directory name where xml annotation files are stored. 






---

<a href="../../datum/generator/image.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `generate_datum`

```python
generate_datum(
    **kwargs: Any
) → Generator[Union[str, int, Dict], NoneType, NoneType]
```

Generator to iterate over data stored in the data folder. 



**Args:**
 
 - <b>`kwargs`</b>:  optional, keyword arguments can be used to control folder names and image extension. 

Following kwargs are supported: 


 - <b>`split`</b>:  name of the split. 
 - <b>`extension`</b>:  image extension. 
 - <b>`set_dir`</b>:  directory name where split files are stored. 
 - <b>`image_dir`</b>:  directory name where images are stored. 
 - <b>`annotation_dir`</b>:  directory name where xml annotation files are stored. 



**Returns:**
 a tuple of datum id and a dict with key as feature name and values as feature values. 



**Raises:**
 
 - <b>`ValueError`</b>:  if inptut split name is not provided. 


---

<a href="../../datum/generator/image.py#L247"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SegDatumGenerator`
Generator for image Segmentation problem. 

This generator expects input data in the Pascal VOC segmentation data format. For each single image there should be a single segmentation map image with class id as pixel values. 

It expects a input data path with the following format: 

+ data_dir: 
    - JPEGImages (all input images for all the splits.) 
    - SegmentationClass (all segmentation label map images.) 

While the overall directory levels should be as shown in the format, sub-directory names can be controlled by passing keyword argument to `__call__` method. 

Following inputs for kwargs are accepted when calling the object: 



**Kwargs:**
 
 - <b>`split`</b>:  split name. 
 - <b>`image_dir`</b>:  name of the directory with input images. 
 - <b>`label_dir`</b>:  name of the directory with segmentation label map images. 
 - <b>`image_extension`</b>:  extension of the input images. 
 - <b>`label_extension`</b>:  extension of the label images. 




---

<a href="../../datum/generator/image.py#L273"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `generate_datum`

```python
generate_datum(
    **kwargs: Any
) → Generator[Union[str, int, Dict], NoneType, NoneType]
```

Single example generator from data in the storage path. 



**Args:**
 
 - <b>`kwargs`</b>:  Optional, keyword arguments to control directory names and exensions. 

Followings kwargs are supported: 


 - <b>`split`</b>:  split name. 
 - <b>`image_dir`</b>:  name of the directory with input images. 
 - <b>`label_dir`</b>:  name of the directory with segmentation label map images. 
 - <b>`image_extension`</b>:  extension of the input images. 
 - <b>`label_extension`</b>:  extension of the label images. 



**Returns:**
 a tuple containing an unique example id and a dict with keys as feature names and values as feature values. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
