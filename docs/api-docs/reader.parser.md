<!-- markdownlint-disable -->

<a href="../../datum/reader/parser.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reader.parser`






---

<a href="../../datum/reader/parser.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DatumParser`
TFRecord Example parser. 

This api can be used to deserialize tfrecord example data. 



**Args:**
 
 - <b>`path`</b>:  path to the dir, where tfrecord metadata json file is stored. 

<a href="../../datum/reader/parser.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(path: str)
```








---

<a href="../../datum/reader/parser.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `decode_example`

```python
decode_example(parsed_example: Dict[str, Tensor]) → Dict[str, Tensor]
```

Decode deserialized example. Used to retrieve feature original shape and value. 



**Args:**
 
 - <b>`parsed_example`</b>:  parsed deserialize example. 



**Returns:**
 a dict, deserialized example data, feature name to value. 

---

<a href="../../datum/reader/parser.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_datum_type_shape_mapping`

```python
load_datum_type_shape_mapping(path: str) → Dict[str, Dict[str, Any]]
```

Load datum type and shape mapping. Feature shae and types are required to deserialize tfrecord serialized binary string data. 



**Args:**
 
 - <b>`path`</b>:  path to the dir, where tfrecord metadata json file is stored. 



**Returns:**
 a mapping, feature name to corresponding shape and data type. 

---

<a href="../../datum/reader/parser.py#L89"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `parse_fn`

```python
parse_fn(example: Example) → Dict[str, Tensor]
```

Parse a single example from serialized binary string. 



**Args:**
 
 - <b>`example`</b>:  input tf.train.Example. 



**Returns:**
 a dict, deserialized example data, feature name to value. 

---

<a href="../../datum/reader/parser.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `wrap_shape`

```python
wrap_shape(shape: List[int]) → List[int]
```

Convert a list of shape to a single element by multiplying all the entries. 



**Args:**
 
 - <b>`shape`</b>:  input shape. 



**Returns:**
 output reduced shape. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
