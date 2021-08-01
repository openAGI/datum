<!-- markdownlint-disable -->

<a href="../../datum/cache/bucket.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `cache.bucket`
To shuffle records (stable). 

**Global Variables**
---------------
- **MAX_MEM_BUFFER_SIZE**
- **BUCKETS_NUMBER**
- **HKEY_SIZE**
- **HKEY_SIZE_BYTES**

---

<a href="../../datum/cache/bucket.py#L71"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_bucket_number`

```python
get_bucket_number(hkey: int, shards_number: int) → int
```

Returns bucket (shard) number (int) for given hashed key (int). 


---

<a href="../../datum/cache/bucket.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DuplicatedKeysError`




<a href="../../datum/cache/bucket.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(item1: Optional[bytes] = None, item2: Optional[bytes] = None)
```









---

<a href="../../datum/cache/bucket.py#L170"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Shuffler`
Stores data in temp buckets, restitute it shuffled. 

<a href="../../datum/cache/bucket.py#L173"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(dirpath: str, hash_salt: str)
```

Initialize Shuffler. 



**Args:**
 
 - <b>`dirpath`</b> (string):  directory in which to store temporary files. 
 - <b>`hash_salt`</b> (string or bytes):  salt to hash keys. 


---

#### <kbd>property</kbd> bucket_lengths





---

#### <kbd>property</kbd> size

Return total size in bytes of records (not keys). 



---

<a href="../../datum/cache/bucket.py#L215"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add`

```python
add(key: int, data: bytes) → None
```

Add (key, data) to shuffler. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
