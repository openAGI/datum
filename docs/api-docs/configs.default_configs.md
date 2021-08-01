<!-- markdownlint-disable -->

<a href="../../datum/configs/default_configs.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `configs.default_configs`
Default write configs for TFRecord export. 


---

<a href="../../datum/configs/default_configs.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_default_write_configs`

```python
get_default_write_configs(
    problem_type: str,
    label_names_file: Optional[str] = None
) → ConfigBase
```

Returns default write configs for a problem. 



**Args:**
 
 - <b>`problem_type`</b>:  Type of the problem,  any one from `datum.problems.types`. 
 - <b>`label_names_file`</b>:  Path to the label name file, required for `IMAGE_DET` problem. 



**Returns:**
 A `ConfigBase` config object. 



**Raises:**
 
 - <b>`ValueError`</b>:  If label_names_file is not valid, raised only for `IMAGE_DET` problem. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
