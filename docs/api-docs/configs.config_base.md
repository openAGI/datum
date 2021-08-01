<!-- markdownlint-disable -->

<a href="../../datum/configs/config_base.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `configs.config_base`





---

<a href="../../datum/configs/config_base.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_config`

```python
create_config(
    name: 'str',
    ty: 'Any',
    docstring: 'str',
    default_factory: 'Callable[[], Any]' = <function <lambda> at 0x16582a310>
) → property
```

Creates a type-checked property. 



**Args:**
 
 - <b>`name`</b>:  The name to use. 
 - <b>`ty`</b>:  The type to use. The type of the property will be validated when it  is set. 
 - <b>`docstring`</b>:  The docstring to use. 
 - <b>`default_factory`</b>:  A callable that takes no arguments and returns a default  value to use if not set. 

**Returns:**
 A type-checked property. 


---

<a href="../../datum/configs/config_base.py#L90"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `merge_configs`

```python
merge_configs(*configs_list: 'ConfigBase') → ConfigBase
```

Merges the given configs, returning the result as a new configs object. The input arguments are expected to have a matching type that derives from `ConfigBase` (and thus each represent a set of configs). The method outputs an object of the same type created by merging the sets of configs represented by the input arguments. The sets of configs can be merged as long as there does not exist an config with different non-default values. If an config is an instance of `ConfigBase` itself, then this method is applied recursively to the set of configs represented by this config. 

**Args:**
 
 - <b>`*configs_list`</b>:  configs to merge 

**Raises:**
 
 - <b>`TypeError`</b>:  if the input arguments are incompatible or not derived from  `ConfigBase` 
 - <b>`ValueError`</b>:  if the given configs cannot be merged 

**Returns:**
 A new configs object which is the result of merging the given configs. 


---

<a href="../../datum/configs/config_base.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ConfigBase`
Base class for representing a set of tf.data config. 



**Attributes:**
 
 - <b>`_configs`</b>:  Stores the config values. 

<a href="../../datum/configs/config_base.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="../../datum/configs/config_base.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `merge`

```python
merge(configs: 'ConfigBase') → ConfigBase
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
