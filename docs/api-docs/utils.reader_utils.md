<!-- markdownlint-disable -->

<a href="../../datum/utils/reader_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.reader_utils`






---

<a href="../../datum/utils/reader_utils.py#L100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ReadInstruction`
Reading instruction for a dataset. 

Examples of usage: ``` 

<a href="../../datum/utils/reader_utils.py#L118"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    split_name: str,
    rounding: str = 'closest',
    from_: Optional[int] = None,
    to: Optional[int] = None,
    unit: Optional[str] = None
)
```

Initialize ReadInstruction. 

**Args:**
 
 - <b>`split_name`</b> (str):  name of the split to read. Eg: 'train'. 
 - <b>`rounding`</b> (str):  The rounding behaviour to use when percent slicing is  used. Ignored when slicing with absolute indices.  Possible values: 
     - 'closest' (default): The specified percentages are rounded to the  closest value. Use this if you want specified percents to be as  much exact as possible. 
     - 'pct1_dropremainder': the specified percentages are treated as  multiple of 1%. Use this option if you want consistency. Eg:  len(5%) == 5 * len(1%).  Using this option, one might not be able to use the full set of  examples, if the number of those is not a multiple of 100. from_ (int): 
 - <b>`to`</b> (int):  alternative way of specifying slicing boundaries. If any of  {from_, to, unit} argument is used, slicing cannot be specified as  string. 
 - <b>`unit`</b> (str):  optional, one of: 
 - <b>`'%'`</b>:  to set the slicing unit as percents of the split size. 
 - <b>`'abs'`</b>:  to set the slicing unit as absolute numbers. 




---

<a href="../../datum/utils/reader_utils.py#L152"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_spec`

```python
from_spec(spec: str) → object
```

Creates a ReadInstruction instance out of a string spec. 



**Args:**
 
 - <b>`spec`</b> (str):  split(s) + optional slice(s) to read. A slice can be  specified, using absolute numbers (int) or percentages (int). E.g. 
 - <b>``test``</b>:  test split. 
 - <b>``test + validation``</b>:  test split + validation split. 
 - <b>``test[10`</b>: ]`: test split, minus its first 10 records. 
 - <b>``test[`</b>: 10%]`: first 10% records of test split. 
 - <b>``test[`</b>: -5%]+train[40%:60%]`: first 95% of test + middle 20% of  train. 

**Returns:**
 ReadInstruction instance. 

---

<a href="../../datum/utils/reader_utils.py#L189"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_absolute`

```python
to_absolute(name2len: Dict[str, int]) → List[_AbsoluteInstruction]
```

Translate instruction into a list of absolute instructions. 

Those absolute instructions are then to be added together. 

**Args:**
 
 - <b>`name2len`</b>:  dict associating split names to number of examples. 

**Returns:**
 list of _AbsoluteInstruction instances (corresponds to the + in spec). 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
