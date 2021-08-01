<!-- markdownlint-disable -->

<a href="../../datum/reader/tfrecord_reader.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reader.tfrecord_reader`





---

<a href="../../datum/reader/tfrecord_reader.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `make_file_instructions`

```python
make_file_instructions(
    path: str,
    instruction: str
) → Tuple[List[int], List[Dict]]
```

Returns instructions of the split dict. 



**Args:**
 
 - <b>`path`</b>:  path to the dir with tfrecord metadata json file. 
 - <b>`instruction`</b>:  `ReadInstruction` or `str` 



**Returns:**
 a tuple containing a list of integer representing number of examples per shards and a list  of read instructions dict. 


---

<a href="../../datum/reader/tfrecord_reader.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Reader`
Build a tf.data.Dataset object out of Instruction instance(s). 

<a href="../../datum/reader/tfrecord_reader.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(path: str, read_config: ConfigBase, buffer_size: Optional[int] = None)
```

Initializes Reader. 



**Args:**
 
 - <b>`path`</b>:  path where tfrecords are stored. 
 - <b>`read_config`</b>:  tfrecord read configuration. 
 - <b>`buffer_size`</b>:  scalar representing the number of bytes in the read buffer. 




---

<a href="../../datum/reader/tfrecord_reader.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `read`

```python
read(
    instructions: Union[ReadInstruction, List[ReadInstruction], Dict[str, ReadInstruction]],
    shuffle_files: bool
) → Union[DatasetV2, List[DatasetV2], Dict[str, DatasetV2]]
```

Returns tf.data.Dataset instance(s). 



**Args:**
 
 - <b>`instructions`</b> (ReadInstruction, List[], Dict[]):  instruction(s) to read.  Instructions can be string and will then be passed to the Instruction  constructor as it. 
 - <b>`shuffle_files`</b> (bool):  If True, input files are shuffled before being read. 



**Returns:**
  a single tf.data.Dataset instance if instruction is a single  ReadInstruction instance. Otherwise a dict/list of tf.data.Dataset  corresponding to given instructions param shape. 

---

<a href="../../datum/reader/tfrecord_reader.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `read_files`

```python
read_files(
    file_instructions: List[Dict],
    num_examples_per_shard: List[int],
    shuffle_files: bool
) → DatasetV2
```

Returns single tf.data.Dataset instance for the set of file instructions. 



**Args:**
 
 - <b>`file_instructions`</b>:  The files information.  The filenames contains the relative path, not absolute. 
 - <b>`skip/take indicates which example read in the shard`</b>:  `ds.skip().take()` 
 - <b>`num_examples_per_shard`</b>:  A list of integer representing number of example per tfrecord  files. 
 - <b>`shuffle_files`</b>:  If True, input files are shuffled before being read. 



**Returns:**
  a tf.data.Dataset instance. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
