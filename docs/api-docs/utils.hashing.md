<!-- markdownlint-disable -->

<a href="../../datum/utils/hashing.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.hashing`
Stable hashing function using md5. Note that the properties we are looking at here are: 1- Good distribution of hashes (random uniformity); 2- Speed; 3- Availability as portable library, giving the same hash independently of platform. Crypto level hashing is not a requirement. A bit of history: 
 - CityHash was first used. However the C implementation used complex instructions and was hard to compile on some platforms. 
 - Siphash was chosen as a replacement, because although being slower, it has a simpler implementation and it has a pure Python implementation, making it easier to distribute TFDS on Windows or MAC. However, the used library (reference C implementation wrapped using cffi) crashed the python interpreter on py3 with tf1.13. 
 - So md5, although being slower that the two above works everywhere and is still faster than a pure python implementation of siphash. Changing the hash function should be done thoughfully, as it would change the order of datasets (and thus sets of records when using slicing API). If done, all datasets would need to have their major version bumped. Note that if we were to find a dataset for which two different keys give the same hash (collision), a solution could be to append the key to its hash. The split name is being used as salt to avoid having the same keys in two splits result in same order. 



---

<a href="../../datum/utils/hashing.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Hasher`
Hasher: to initialize a md5 with salt. 

<a href="../../datum/utils/hashing.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(salt: str)
```








---

<a href="../../datum/utils/hashing.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `hash_key`

```python
hash_key(key: Union[bytes, str]) → int
```

Returns 128 bits hash of given key. 



**Args:**
 
 - <b>`key`</b> (bytes, string or anything convertible to a string):  key to be hashed.  If the key is a string, it will be encoded to bytes using utf-8.  If the key is neither a string nor bytes, it will be converted to a str,  then to bytes.  This means that `"1"` (str) and `1` (int) will have the same hash. The  intent of the hash being to shuffle keys, it is recommended that all  keys of a given set to shuffle use a single type. 

**Returns:**
 128 bits integer, hash of key. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
