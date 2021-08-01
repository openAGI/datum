<!-- markdownlint-disable -->

<a href="../../datum/utils/common_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.common_utils`





---

<a href="../../datum/utils/common_utils.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `load_module`

```python
load_module(module_name: str, module_path: str) → object
```

Load python module using a given path; the path can be absolute or relative. 



**Args:**
 
 - <b>`module_name`</b>:  a `str`, name of the module to load 
 - <b>`module_path`</b>:  a `str`, absolute/relative path of the module to load 

Return: loaded python module 


---

<a href="../../datum/utils/common_utils.py#L171"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `add_metaclass`

```python
add_metaclass(metaclass: ABCMeta) → Callable[[Any], object]
```

Class decorator for creating a class with a metaclass. 

This supports creating metaclass with slots variable. 


---

<a href="../../datum/utils/common_utils.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `reraise`

```python
reraise(prefix: Optional[str] = None, suffix: Optional[str] = None) → None
```

Reraise an exception with an additional message. 



**Args:**
 
 - <b>`prefix`</b>:  prefix to add to the current exception. 
 - <b>`suffix`</b>:  suffix to add to the current exception. 


---

<a href="../../utils/common_utils/try_reraise#L208"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `try_reraise`

```python
try_reraise(*args: Any, **kwargs: Any) → Any
```

Reraise an exception with an additional message. 


---

<a href="../../datum/utils/common_utils.py#L217"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `six_reraise`

```python
six_reraise(tp, value, tb=None)
```






---

<a href="../../datum/utils/common_utils.py#L230"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `zip_dict`

```python
zip_dict(*dicts)
```

Iterate over items of dictionaries grouped by their keys. 


---

<a href="../../datum/utils/common_utils.py#L238"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `item_to_type_and_shape`

```python
item_to_type_and_shape(
    item: Union[int, float, str, bytes, List[Union[int, float, str]]]
) → Tuple[str, List]
```

Datum item to type and shape. 


---

<a href="../../datum/utils/common_utils.py#L256"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `check_and_image_shape`

```python
check_and_image_shape(
    item: Union[int, float, str, bytes, List[Union[int, float, str]]],
    shape: List
) → List
```

Check whether a string is image filename. 



**Args:**
 
 - <b>`item`</b>:  input string to check. 



**Returns:**
 a list, item shape. 


---

<a href="../../datum/utils/common_utils.py#L275"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_string`

```python
is_string(item: Any) → bool
```

Check if the object contains string or bytes. 


---

<a href="../../datum/utils/common_utils.py#L287"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `datum_to_type_and_shape`

```python
datum_to_type_and_shape(
    datum: Dict[str, Union[str, int, bytes, float, List[int], List[float], List[str], ndarray]],
    sparse_features: Optional[List[str]] = None
) → Dict
```

Get object type and shape from value. 


---

<a href="../../datum/utils/common_utils.py#L319"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `deserialize_object`

```python
deserialize_object(
    identifier: Any,
    module_objects: Dict,
    printable_module_name: str = 'object'
) → object
```

Deserialize object using name. 



**Args:**
 
 - <b>`identifier`</b>:  a string or function. 
 - <b>`module_objects`</b>:  modules global objects. 
 - <b>`printable_module_name`</b>:  name of the module, 



**Returns:**
 deserialized class. 



**Raises:**
 
 - <b>`ValueError`</b>:  if identifier does not exist or not supported. 


---

<a href="../../datum/utils/common_utils.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AttrDict`
Enables acessing dict items as attributes. 



**Args:**
 
 - <b>`args`</b>:  a `dict` object. 

<a href="../../datum/utils/common_utils.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(_AttrDict__self, *args: Any, **kwargs: Any)
```








---

<a href="../../datum/utils/common_utils.py#L128"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `copy`

```python
copy() → Any
```





---

<a href="../../datum/utils/common_utils.py#L131"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `deepcopy`

```python
deepcopy() → Any
```





---

<a href="../../datum/utils/common_utils.py#L163"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `setdefault`

```python
setdefault(key: Any, default: Optional[Any] = None) → Any
```





---

<a href="../../datum/utils/common_utils.py#L116"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dict`

```python
to_dict() → Any
```





---

<a href="../../datum/utils/common_utils.py#L141"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update`

```python
update(*args: Any, **kwargs: Any) → None
```






---

<a href="../../datum/utils/common_utils.py#L301"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `memoized_property`
Descriptor that mimics @property but caches output in member variable. 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
