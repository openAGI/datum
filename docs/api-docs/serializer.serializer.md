<!-- markdownlint-disable -->

<a href="../../datum/serializer/serializer.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `serializer.serializer`





---

<a href="../../datum/serializer/serializer.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `serialize_datum`

```python
serialize_datum(
    encoded_datum: Dict[str, Union[str, int, bytes, float, List[int], List[float], List[str], ndarray]]
) → bytes
```

Serialize the given example. 



**Args:**
 
 - <b>`datum`</b>:  Nested `dict` containing the input to serialize. 



**Returns:**
 bytes, the serialized `tf.train.Example` string. 


---

<a href="../../datum/serializer/serializer.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `datum_to_tf_example`

```python
datum_to_tf_example(
    datum: Dict[str, Union[str, int, bytes, float, List[int], List[float], List[str], ndarray]]
) → Example
```

Builds tf.train.Example from (string -> int/float/str list) dictionary. 



**Args:**
 
 - <b>`datum`</b>:  `dict`, dict of values, tensor,... 



**Returns:**
 a `tf.train.Example`, the encoded example proto. 


---

<a href="../../datum/serializer/serializer.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DatumSerializer`
Datum serializer. Encode data into serialized binary string. 



**Args:**
 
 - <b>`problem_type`</b>:  type of the problem, e.g: image/text/graph etc. 
 - <b>`datum_name_to_encoder_fn`</b>:  a callable used to get encoder object for each feature. 

<a href="../../datum/serializer/serializer.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    problem_type: str,
    datum_name_to_encoder_fn: Callable[[Dict[str, Union[str, int, bytes, float, List[int], List[float], List[str], ndarray]], str], Dict[str, Encoder]] = None
)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
