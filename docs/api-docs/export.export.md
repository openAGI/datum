<!-- markdownlint-disable -->

<a href="../../datum/export/export.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `export.export`





---

<a href="../../datum/export/export.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `export_to_tfrecord`

```python
export_to_tfrecord(
    input_path: str,
    output_path: str,
    problem_type: str,
    write_configs: ConfigBase
) → None
```

Export data to tfrecord format. 



**Args:**
 
 - <b>`input_path`</b>:  Root path to input data folder. 
 - <b>`output_path`</b>:  Path to store output tfrecords and generated metadata. 
 - <b>`problem_type`</b>:  Type of the problem, see `datum.probelm.types` for available problems. 
 - <b>`write_configs`</b>:  Configuration for tfrecord writing. 

write_configs has the following configurable attributes: 


 - <b>`generator`</b>:  Generator class. 
 - <b>`serializer`</b>:  Serializer instance. 
 - <b>`splits`</b>:  A dict with split names as keys and split attributes as values. 

Following split attributes are supported: 


 - <b>`num_examples`</b>:  Number of examples in the split. 
 - <b>`extension`</b>:  Input image extension in case of image data, all input should have same  extension. Default - For image data, `.jpg` 
 - <b>`image_dir`</b>:  Name of the directory containing the data, used for image classification.  Default - split name, `train` for classification, for detection `JPEGImages` as per  VOC12 folder structure. 
 - <b>`csv_path`</b>:  Path to ground truths csv file, used for classification dataset.  Default - split name with .csv extension, example - `train.csv` 
 - <b>`set_dir`</b>:  In case of VOC12 style  datasets, image set information.  Default - `ImageSets` as per VOC12 dataset folder structure 
 - <b>`annotation_dir`</b>:  Directory with annotations, used for VOC12 style datasets.  Default - `Annotations` as per VOC12 dataset folder structure 
 - <b>`label_dir`</b>:  Directory with label images, used in segmentation.  Default - `SegmentationClass` for as per VOC12 folder structure. 
 - <b>`image_extension`</b>:  Extension of input images, used in segmentation.  Default - `.jpg` 
 - <b>`label_extension`</b>:  Extension of label images, used in segmentation.  Default - `.png` 



**Raises:**
 
   - <b>`ValueError`</b>:  If splits information is not in the dict format. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
