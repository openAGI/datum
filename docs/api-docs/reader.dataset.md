<!-- markdownlint-disable -->

<a href="../../datum/reader/dataset.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reader.dataset`






---

<a href="../../datum/reader/dataset.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Dataset`
Public API to read tfrecord as tf.data.Dataset. 



**Args:**
 
 - <b>`path`</b>:  path to the tfrecord files. 
 - <b>`dataset_configs`</b>:  Optional configuration for data processing and reading. 

<a href="../../datum/reader/dataset.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(path: str, dataset_configs: ConfigBase)
```






---

#### <kbd>property</kbd> dataset_configs

Returns current object dataset configs. 



---

<a href="../../datum/reader/dataset.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `test_fn`

```python
test_fn(
    instruction: str = 'test',
    repeat: int = 1,
    shuffle: bool = False
) → DatasetV2
```

Get test dataset. 



**Args:**
 
 - <b>`instruction`</b>:  instruction on how much data to read. 
 - <b>`repeat`</b>:  number of times to repeat the dataset. 
 - <b>`shuffle`</b>:  if true, shuffles examples of the dataset. 



**Returns:**
 a tf.data.Dataset object. 

---

<a href="../../datum/reader/dataset.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `train_fn`

```python
train_fn(
    instruction: str = 'train',
    repeat: Optional[int] = None,
    shuffle: bool = True
) → DatasetV2
```

Get training dataset. 



**Args:**
 
 - <b>`instruction`</b>:  instruction on how much data to read. 
 - <b>`repeat`</b>:  number of times to repeat the dataset. 
 - <b>`shuffle`</b>:  if true, shuffles examples of the dataset. 



**Returns:**
 a tf.data.Dataset object. 

---

<a href="../../datum/reader/dataset.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `val_fn`

```python
val_fn(
    instruction: str = 'val',
    repeat: Optional[int] = None,
    shuffle: bool = False
) → DatasetV2
```

Get validation dataset. 



**Args:**
 
 - <b>`instruction`</b>:  instruction on how much data to read. 
 - <b>`repeat`</b>:  number of times to repeat the dataset. 
 - <b>`shuffle`</b>:  if true, shuffles examples of the dataset. 



**Returns:**
 a tf.data.Dataset object. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
