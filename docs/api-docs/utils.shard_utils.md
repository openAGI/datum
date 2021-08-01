<!-- markdownlint-disable -->

<a href="../../datum/utils/shard_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.shard_utils`




**Global Variables**
---------------
- **MIN_SHARD_SIZE**
- **MAX_SHARD_SIZE**
- **TFRECORD_REC_OVERHEAD**

---

<a href="../../datum/utils/shard_utils.py#L42"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `raise_error_for_duplicated_keys`

```python
raise_error_for_duplicated_keys(err: Exception) → None
```

Log information about the examples and raise an AssertionError. 


---

<a href="../../datum/utils/shard_utils.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_shard_specs`

```python
get_shard_specs(
    num_examples: int,
    total_size: int,
    bucket_lengths: Sequence[int],
    path: str
) → List[_ShardSpec]
```

Returns list of _ShardSpec instances, corresponding to shards to write. 



**Args:**
 
 - <b>`num_examples`</b>:  number of examples in split. 
 - <b>`total_size`</b>:  sum of example sizes. 
 - <b>`bucket_lengths`</b>:  number of examples in each bucket. 
 - <b>`path`</b>:  path to store tfrecord files. 

Retuns: a list of ShardSpec objects, 


---

<a href="../../datum/utils/shard_utils.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `write_tfrecord`

```python
write_tfrecord(path: str, iterator: Iterator) → None
```

Write single (non sharded) TFrecord file from iterator. 


---

<a href="../../datum/utils/shard_utils.py#L135"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_read_instructions`

```python
get_read_instructions(
    from_: int,
    to: int,
    filenames: Sequence[Union[str, int]],
    shard_lengths: Sequence[int],
    shardref_name: str = 'filename'
) → List[Dict]
```

Returns a list of files (+skip/take) to read [from_:to] items from shards. 



**Args:**
 
 - <b>`from_`</b>:  int, Index (included) of element from which to read. 
 - <b>`to`</b>:  int, Index (excluded) of element to which to read. 
 - <b>`filenames`</b>:  list of strings or ints, the filenames of the shards. Not really  used, but to place in result. 
 - <b>`shard_lengths`</b>:  the number of elements in every shard. 
 - <b>`shardref_name`</b>:  string, defaults to "filename". How to name the field holding  the shard-reference in result dict. 



**Returns:**
 list of dict(filename, skip, take). 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
