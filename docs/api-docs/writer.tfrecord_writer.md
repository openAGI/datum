<!-- markdownlint-disable -->

<a href="../../datum/writer/tfrecord_writer.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `writer.tfrecord_writer`






---

<a href="../../datum/writer/tfrecord_writer.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TFRecordWriter`
TFRecord writer interface. 

This module is used to convert data into serialized binary string and to write  data as tfrecords to disk. It uses a cache to shuffle and store intermediate serialized binary string tensors. 



**Args:**
 
 - <b>`generator`</b>:  an instance of a datum generator. 
 - <b>`serializer`</b>:  an instance of datum serializer. 
 - <b>`path`</b>:  absolute path to store the tfrecords data and metadata. 
 - <b>`split`</b>:  name of the split. 
 - <b>`total_examples`</b>:  number of examples to write. 
 - <b>`gen_kwargs`</b>:  optional keyword arguments to used when calling geenrator. 

<a href="../../datum/writer/tfrecord_writer.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    generator: Callable,
    serializer: Callable,
    path: str,
    split: str,
    total_examples: int,
    sparse_features: Optional[List[str]] = None,
    **gen_kwargs: Any
)
```

path = /tmp/test/ split = train/val/test 




---

<a href="../../datum/writer/tfrecord_writer.py#L95"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_shape_fields`

```python
add_shape_fields(
    datum: Dict[str, Union[str, int, bytes, float, List[int], List[float], List[str], ndarray]]
) → Dict[str, Union[str, int, bytes, float, List[int], List[float], List[str], ndarray]]
```

Add tensor shape information to dataset metadat json file and tfrecords. This is required when dealing wit sparse tensors. As we need to revert back the original shape of tensor, when tensor dimension >= 2. 



**Args:**
 
 - <b>`datum`</b>:  a dict, input datum. 



**Returns:**
 input dict updated with sprase tensors shape information. 

---

<a href="../../datum/writer/tfrecord_writer.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `cache_records`

```python
cache_records() → None
```

Write data to cache. 

---

<a href="../../datum/writer/tfrecord_writer.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_records`

```python
create_records() → None
```

Create tfrecords from given generator. 

---

<a href="../../datum/writer/tfrecord_writer.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `flush`

```python
flush() → None
```

Wirte tfrecord files to disk. 

---

<a href="../../datum/writer/tfrecord_writer.py#L119"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `flush_records`

```python
flush_records() → Tuple[Dict[str, Dict[str, int]], int]
```

Write tfrecord files to disk. 



**Returns:**
  a tuple containing a dict with shard info and the size of shuffler. 

---

<a href="../../datum/writer/tfrecord_writer.py#L144"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `save_shard_info`

```python
save_shard_info(shard_info: Dict[str, Dict[str, int]]) → None
```

Save shard info to disk. 



**Args:**
 
 - <b>`shard_info`</b>:  input shard info dict. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
