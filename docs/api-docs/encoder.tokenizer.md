<!-- markdownlint-disable -->

<a href="../../datum/encoder/tokenizer.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `encoder.tokenizer`






---

<a href="../../datum/encoder/tokenizer.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BaseTokenizer`







---

<a href="../../datum/encoder/tokenizer.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `decode`

```python
decode(*args, **kwargs)
```





---

<a href="../../datum/encoder/tokenizer.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `encode`

```python
encode(*args, **kwargs)
```






---

<a href="../../datum/encoder/tokenizer.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `InvertibleTokenizer`







---

<a href="../../datum/encoder/tokenizer.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `decode`

```python
decode(tokens)
```

Decode a list of tokens to a unicode string. 



**Args:**
 
 - <b>`tokens`</b>:  a list of Unicode strings 

**Returns:**
 a unicode string 

---

<a href="../../datum/encoder/tokenizer.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `encode`

```python
encode(text)
```

Encode a unicode string as a list of tokens. 



**Args:**
 
 - <b>`text`</b>:  a unicode string 

**Returns:**
 a list of tokens as Unicode strings 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
