<!-- markdownlint-disable -->

<a href="../../datum/reader/loader.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reader.loader`





---

<a href="../../datum/reader/loader.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `load`

```python
load(path: str, dataset_configs: Optional[ConfigBase] = None) → DatasetV2
```

Load tfrecord dataset as `tf.data.Daatset`. 



**Args:**
 
 - <b>`path`</b>:  path to the storage location with tfrecord files and metadata. 
 - <b>`dataset_configs`</b>:  A DatasetConfigs can be used to control the parameter for  the output tf.data.Dataset. This is designed to give an extensive control of  the dataset pre and post processsing operation to the end-user. 

dataset_configs has the following configurable attributes. 


 - <b>`buffer_size`</b>:  Representing the number of elements from this dataset from which the  new dataset will sample, default - 100. 
 - <b>`seed`</b>:  Random seed for tfrecord files based randomness, default - 6052020. 
 - <b>`full_dataset`</b>:  'Returns the dataset as a single batch for dataset with only one element,  default - False. 
 - <b>`batch_size_train`</b>:  Batch size for training data, default - 32. 
 - <b>`batch_size_val`</b>:  Batch size for validation data, default - 32. 
 - <b>`batch_size_test`</b>:  Batch size for test data, default - 32. 
 - <b>`shuffle_files`</b>:  Shuffle tfrecord input files, default - True. 
 - <b>`reshuffle_each_iteration`</b>:  If true indicates that the dataset should be pseudorandomly  reshuffled each time it is iterated over, default - False. 
 - <b>`cache`</b>:  If true the first time the dataset is iterated over, its elements will be cached  either the specified file or in memory. Subsequent iterations will use the  cached data, default - False. 
 - <b>`cache_filename`</b>:  Representing the name of a directory on the file system to use for caching  elements in this Dataset, default - ''. 
 - <b>`bucket_op`</b>:  The sequence length based bucketing operation options. 
 - <b>`bucket_fn`</b>:  Function from element in Dataset to tf.int32, determines the length of the  element which will determine the bucket it goes into, default - None. 
 - <b>`pre_batching_callback_train`</b>:  Preprocessing operation to use on a single case of the dataset  before batching, default - None. 
 - <b>`post_batching_callback_train`</b>:  Processing operation to use on a batch of the dataset after  batching, default - None. 
 - <b>`pre_batching_callback_val`</b>:  Preprocessing operation to use on a single case of the dataset  before batching, default - None. 
 - <b>`post_batching_callback_val`</b>:  Processing operation to use on a batch of the dataset after  batching, default - None. 
 - <b>`pre_batching_callback_test`</b>:  Preprocessing operation to use on a single case of the dataset  before batching, default - None. 
 - <b>`post_batching_callback_test`</b>:  Processing operation to use on a batch of the dataset after  batching, default - None. 
 - <b>`read_config`</b>:  A TFRReadconfigs object can be used to control the parameter required to read  tfrecord files to construct a tf.data.Dataset. 

`bucket_op` supports the following sub attributes 


 - <b>`bucket_boundaries`</b>:  Upper length boundaries of the buckets, default - [0]. 
 - <b>`bucket_batch_sizes`</b>:  Batch size per bucket. Length should be len(bucket_boundaries) + 1,  default - [32, 32]. 

`read_config` supports the following sub atrributes 


 - <b>`experimental_interleave_sort_fn`</b>:  Dataset interleave sort function, default - None. 
 - <b>`shuffle_reshuffle_each_iteration`</b>:  Shuffle files each iteration before reading,  default - True. 
 - <b>`interleave_cycle_length`</b>:  The number of input elements that will be processed concurrently,  default - -1, 
 - <b>`interleave_block_length`</b>:  The number of consecutive elements to produce from each input  element before cycling to another input element, default - 1. 
 - <b>`seed`</b>:  Random seed for tfrecord files based randomness, default - 6052020. 
 - <b>`options`</b>:  Tensorflow data api options for dataset prep and reading,  default - tf.data.Options(), 



**Returns:**
 a `tf.data.Dataset`. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
