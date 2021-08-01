<!-- markdownlint-disable -->

<a href="../../datum/utils/binary_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.binary_utils`





---

<a href="../../datum/utils/binary_utils.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_binary_image`

```python
is_binary_image(string: Tensor) → Tuple[bool, str]
```

Determine image compression type using a binary string tensor/object. 



**Args:**
 
 - <b>`string`</b>:  binary string, can be `tf.Tensor` or python format.. 



**Returns:**
 a tuple containing a flag denoting whether input string is an image and the corresponding  extension (if its an image, else empty). 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
