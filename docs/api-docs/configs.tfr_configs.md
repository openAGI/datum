<!-- markdownlint-disable -->

<a href="../../datum/configs/tfr_configs.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `configs.tfr_configs`






---

<a href="../../datum/configs/tfr_configs.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TFRWriteConfigs`
TF Record writer configuration. 

A TFRWriteCOnfigs object can be used to control the parameter required for data generation, features type information, splits information and splitwise number of examples. 


---

#### <kbd>property</kbd> generator

Generator class instance, it should have a __call__ method. 

---

#### <kbd>property</kbd> num_test_examples

Num of test examples in the dataset. 

---

#### <kbd>property</kbd> num_train_examples

Num of train examples in the dataset. 

---

#### <kbd>property</kbd> num_val_examples

Num of val examples in the dataset. 

---

#### <kbd>property</kbd> serializer

Serializer class instance, it should have a __call__ method. 

---

#### <kbd>property</kbd> sparse_features

A list of sparse features name in the dataset. 

---

#### <kbd>property</kbd> splits

A dict of split names as keys and       split attributes as values in the dataset. 




---

<a href="../../datum/configs/tfr_configs.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TFRReadConfigs`
TF Record Reader configuration. 

A TFRReadconfigs object can be used to control the parameter required to read tfrecord files to construct a tf.data.Dataset. 


---

#### <kbd>property</kbd> experimental_interleave_sort_fn

Dataset interleave sort function. 

---

#### <kbd>property</kbd> interleave_block_length

The number of consecutive elements to produce from each input element before           cycling to another input element 

---

#### <kbd>property</kbd> interleave_cycle_length

The number of input elements that will be processed concurrently 

---

#### <kbd>property</kbd> options

Tensorflow data api options for dataset prep and reading.. 

---

#### <kbd>property</kbd> seed

Random seed for tfrecord files based randomness. 

---

#### <kbd>property</kbd> shuffle_reshuffle_each_iteration

Shuffle files each iteration before reading. 




---

<a href="../../datum/configs/tfr_configs.py#L102"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BucketConfigs`
Bucket configuration used for bucketing sprase data into a batch. 

A BucketConfigs object can be used to control the bucket boundaries and batch sizes. 


---

#### <kbd>property</kbd> bucket_batch_sizes

Batch size per bucket. Length should be len(bucket_boundaries) + 1. 

---

#### <kbd>property</kbd> bucket_boundaries

Upper length boundaries of the buckets. 




---

<a href="../../datum/configs/tfr_configs.py#L121"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DatasetConfigs`
Dataset configuration. 

A DatasetConfigs can be used to control the parameter for the output tf.data.Dataset. This is designed to give an extensive control of the dataset pre and post processsing operation to the end-user. 


---

#### <kbd>property</kbd> batch_size_test

Batch size for test data. 

---

#### <kbd>property</kbd> batch_size_train

Batch size for training data. 

---

#### <kbd>property</kbd> batch_size_val

Batch size for validation data. 

---

#### <kbd>property</kbd> bucket_fn

Function from element in Dataset to tf.int32, determines the length of the element          which will determine the bucket it goes into. 

---

#### <kbd>property</kbd> bucket_op

The sequence length based bucketing operation options. 

---

#### <kbd>property</kbd> buffer_size

Representing the number of elements from this dataset from which the           new dataset will sample. 

---

#### <kbd>property</kbd> cache

If true the first time the dataset is iterated over, its elements will be cached either in          the specified file or in memory. Subsequent iterations will use the cached data. 

---

#### <kbd>property</kbd> cache_filename

Representing the name of a directory on the file system to use for caching elements in           this Dataset. 

---

#### <kbd>property</kbd> echoing

Batch echoing factor, if not None, echoes batches. 

---

#### <kbd>property</kbd> full_dataset

Returns the dataset as a single batch if it has only one element, useful for          serving. 

---

#### <kbd>property</kbd> post_batching_callback_test

Processing operation to use on a batch of the dataset after batching. 

---

#### <kbd>property</kbd> post_batching_callback_train

Processing operation to use on a batch of the dataset after batching. 

---

#### <kbd>property</kbd> post_batching_callback_val

Processing operation to use on a batch of the dataset after batching. 

---

#### <kbd>property</kbd> pre_batching_callback_test

Preprocessing operation to use on a single case of the dataset before batching. 

---

#### <kbd>property</kbd> pre_batching_callback_train

Preprocessing operation to use on a single case of the dataset before batching. 

---

#### <kbd>property</kbd> pre_batching_callback_val

Preprocessing operation to use on a single case of the dataset before batching. 

---

#### <kbd>property</kbd> read_config

A TFRReadconfigs object can be used to control the parameter required to read        tfrecord files to construct a tf.data.Dataset. 

---

#### <kbd>property</kbd> reshuffle_each_iteration

If true indicates that the dataset should be pseudorandomly reshuffled each          time it is iterated over. 

---

#### <kbd>property</kbd> seed

Random seed for tfrecord files based randomness. 

---

#### <kbd>property</kbd> shuffle_files

Shuffle tfrecord input files. 






---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
