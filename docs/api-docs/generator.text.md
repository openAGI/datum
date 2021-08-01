<!-- markdownlint-disable -->

<a href="../../datum/generator/text.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `generator.text`






---

<a href="../../datum/generator/text.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TextJsonDatumGenerator`
Text problem datum generator from json file. 

This can be used for classification or generative modeling. This expect data to be in json format with each of the examples keyed using an unique id. Each example should have two mandatory attributes: `text` and `label` (it is a nested attribute). 

Input path should have json files for training/development/validation. By default the generator search for json file named after split name, but it can be configured by using the keyword argument `json_path` to `__call__`. 

+ data_path 
    - train.json (json file containing the training data)  For example a sample json file would looks as follows: ```
           {1: {'text': 'I am the one', 'label': {'polarity': 1}},
           ...
           N: {'text': 'Such a beautiful day', 'label': {'polarity': 2}}
           }
      ``` 


    - val.json (json file containing the val data) 
    - test.json (json file containing the test data) 

Following are the supported keyword arguments: 



**Kwargs:**
 
 - <b>`split`</b>:  name of the split 
 - <b>`json_path`</b>: name of the json file for that split, this is a relative path with respect to  parent `self.path`. 




---

<a href="../../datum/generator/text.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `generate_datum`

```python
generate_datum(
    **kwargs: Any
) → Generator[Union[str, int, Dict], NoneType, NoneType]
```

Returns a generator to get datum from the input source. 



**Args:**
 
 - <b>`kwargs`</b>:  optional keyword arguments for customization. 

Following are the supported keyword arguments: 


 - <b>`split`</b>:  name of the split 
 - <b>`json_path`</b>: name of the json file for that split, this is a relative path with respect to  parent `self.path`. 



**Returns:**
 a tuple of a unique id and a dictionary with feature names as keys and feature values as  values. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
