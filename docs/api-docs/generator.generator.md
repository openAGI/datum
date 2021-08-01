<!-- markdownlint-disable -->

<a href="../../datum/generator/generator.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `generator.generator`






---

<a href="../../datum/generator/generator.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DatumGenerator`
Input data generator abstract interface. Derived classes have to implement geenrate_datum method, which returns a generator with two return values. 



**Args:**
 
 - <b>`path`</b>:  a path to the data store location. 
 - <b>`gen_config`</b>:  configs for generator. 

<a href="../../datum/generator/generator.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(path: str, gen_config: Union[AttrDict, ConfigBase] = None)
```








---

<a href="../../datum/generator/generator.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `generate_datum`

```python
generate_datum(
    **kwargs: Any
) → Generator[Union[str, int, Dict], NoneType, NoneType]
```

Returns a generator to iterate over the processed input data. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
