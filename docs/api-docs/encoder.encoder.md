<!-- markdownlint-disable -->

<a href="../../datum/encoder/encoder.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `encoder.encoder`





---

<a href="../../datum/encoder/encoder.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `datum_name_to_encoder`

```python
datum_name_to_encoder(datum: Dict, problem_type: str) → Dict[str, Encoder]
```

Automatically identify encoder based on data values and problem type. 



**Args:**
 
 - <b>`datum`</b>:  a dict with feature name as keys and feature data as values. 
 - <b>`problem_type`</b>:  type of the problem. Whether the problem is related to image/text/grpah etc. 



**Returns:**
 a dict, mapping feature name to encoder object. 


---

<a href="../../datum/encoder/encoder.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Encoder`
Feature Encoder abstract interface. Derived classes have to implement the encode method for encoding. 



**Args:**
 
 - <b>`kwargs`</b>:  Optional arguments required to implement encode method. 

<a href="../../datum/encoder/encoder.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(**kwargs: Any)
```








---

<a href="../../datum/encoder/encoder.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `encode`

```python
encode(
    inputs: Union[int, float, str, bytes, List[Union[int, float, str]]]
) → Union[int, float, str, bytes, List[Union[int, float, str]]]
```

Encode input data to required format. 



**Args:**
 
 - <b>`inputs`</b>:  inputs data to encode. 



**Returns:**
 encoded data. 


---

<a href="../../datum/encoder/encoder.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ImageEncoder`




<a href="../../datum/encoder/encoder.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(**kwargs: Any)
```








---

<a href="../../datum/encoder/encoder.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `encode`

```python
encode(
    inputs: Union[int, float, str, bytes, List[Union[int, float, str]]]
) → Union[int, float, str, bytes, List[Union[int, float, str]]]
```

Image encoder. 



**Args:**
 
 - <b>`inputs`</b>:  input image absolute path. 



**Returns:**
 a bytes string representation of the input image. 


---

<a href="../../datum/encoder/encoder.py#L75"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `NumberEncoder`




<a href="../../datum/encoder/encoder.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(**kwargs: Any)
```








---

<a href="../../datum/encoder/encoder.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `encode`

```python
encode(
    inputs: Union[int, float, str, bytes, List[Union[int, float, str]]]
) → Union[int, float, str, bytes, List[Union[int, float, str]]]
```

Encode integer or floating point number. 

Currently returns inputs as outputs, as no processing required. 


---

<a href="../../datum/encoder/encoder.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `StringEncoder`
String encoder. 

For image related problems it will just return the input text. The main objective of this encoder is to comvert input string to vector representation, which will be implemented on a go forward basis. 

<a href="../../datum/encoder/encoder.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(**kwargs: Any)
```








---

<a href="../../datum/encoder/encoder.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `encode`

```python
encode(
    inputs: Union[int, float, str, bytes, List[Union[int, float, str]]]
) → Union[int, float, str, bytes, List[Union[int, float, str]]]
```

String encoder. 

Currently it doesnt implement any encoder. 

**Args:**
 
 - <b>`inputs`</b>:  input string. 



**Returns:**
 encoded output. 


---

<a href="../../datum/encoder/encoder.py#L109"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GraphEncoder`
Graph data encoder. 

This encoder can be used convert graph data into matrix and vector, list representation. 

<a href="../../datum/encoder/encoder.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(**kwargs: Any)
```








---

<a href="../../datum/encoder/encoder.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `encode`

```python
encode(
    inputs: Union[int, float, str, bytes, List[Union[int, float, str]]]
) → Union[int, float, str, bytes, List[Union[int, float, str]]]
```

Graph data encoder. 

Currently it doesnt implement any encoder. 



**Args:**
 
 - <b>`inputs`</b>:  input graph data. 



**Returns:**
 encoded graph data. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
