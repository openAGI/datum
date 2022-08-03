# Copyright 2020 The OpenAGI Datum Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import contextlib
import copy
import importlib.util as module_util
import sys
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Tuple, no_type_check

import numpy as np
from tensorflow.python.util import tf_inspect

from datum.utils.types_utils import DatumType, ValueType


def load_module(module_name: str, module_path: str) -> object:
  """Load python module using a given path; the path can be absolute or relative.

  Args:
    module_name: a `str`, name of the module to load
    module_path: a `str`, absolute/relative path of the module to load

  Return:
    loaded python module
  """
  spec = module_util.spec_from_file_location(module_name, module_path)
  module = module_util.module_from_spec(spec)
  spec.loader.exec_module(module) # type: ignore
  return module


class AttrDict(dict):
  """Enables acessing dict items as attributes.

  Args:
    args: a `dict` object.
  """

  # pylint: disable=no-self-argument
  def __init__(__self, *args: Any, **kwargs: Any):
    object.__setattr__(__self, '__parent', kwargs.pop('__parent', None))
    object.__setattr__(__self, '__key', kwargs.pop('__key', None))
    for arg in args:
      if not arg:
        continue
      elif isinstance(arg, dict):
        for key, val in arg.items():
          __self[key] = __self._hook(val)
      elif isinstance(arg, tuple) and (not isinstance(arg[0], tuple)):
        __self[arg[0]] = __self._hook(arg[1])
      else:
        for key, val in iter(arg):
          __self[key] = __self._hook(val)

    for key, val in kwargs.items():
      __self[key] = __self._hook(val)

  def __setattr__(self, name: str, value: Any) -> None:
    if hasattr(self.__class__, name):
      raise AttributeError("'Dict' object attribute "
                           "'{0}' is read-only".format(name))
    else:
      self[name] = value

  def __setitem__(self, name: str, value: Any) -> None:
    super(AttrDict, self).__setitem__(name, value)
    try:
      p = object.__getattribute__(self, '__parent')
      key = object.__getattribute__(self, '__key')
    except AttributeError:
      p = None
      key = None
    if p is not None:
      p[key] = self
      object.__delattr__(self, '__parent')
      object.__delattr__(self, '__key')

  def __add__(self, other: Any) -> Any:
    if not self.keys():
      return other
    else:
      self_type = type(self).__name__
      other_type = type(other).__name__
      msg = "unsupported operand type(s) for +: '{}' and '{}'"
      raise TypeError(msg.format(self_type, other_type))

  @classmethod
  def _hook(cls: Any, item: Any) -> Any:
    if isinstance(item, dict):
      return cls(item)
    elif isinstance(item, (list, tuple)):
      return type(item)(cls._hook(elem) for elem in item)
    return item

  def __getattr__(self, item: Any) -> Any:
    return self.__getitem__(item)

  def __missing__(self, name: str) -> Any:
    return self.__class__(__parent=self, __key=name)

  def __delattr__(self, name: str) -> None:
    del self[name]

  def to_dict(self) -> Any:
    base = {}
    for key, value in self.items():
      if isinstance(value, type(self)):
        base[key] = value.to_dict()
      elif isinstance(value, (list, tuple)):
        base[key] = type(value)(item.to_dict() if isinstance(item, type(self)) else item
                                for item in value)
      else:
        base[key] = value
    return base

  def copy(self) -> Any:
    return copy.copy(self)

  def deepcopy(self) -> Any:
    return copy.deepcopy(self)

  def __deepcopy__(self, memo: Any) -> Any:
    other = self.__class__()
    memo[id(self)] = other
    for key, value in self.items():
      other[copy.deepcopy(key, memo)] = copy.deepcopy(value, memo)
    return other

  def update(self, *args: Any, **kwargs: Any) -> None:
    other: Dict[Any, Any] = {}
    if args:
      if len(args) > 1:
        raise TypeError()
      other.update(args[0])
    other.update(kwargs)
    for k, v in other.items():
      if ((k not in self) or (not isinstance(self[k], dict)) or (not isinstance(v, dict))):
        self[k] = v
      else:
        self[k].update(v)

  def __getnewargs__(self) -> Any:
    return tuple(self.items())

  def __getstate__(self) -> Any:
    return self

  def __setstate__(self, state: Any) -> None:
    self.update(state)

  def setdefault(self, key: Any, default: Optional[Any] = None) -> Any:
    if key in self:
      return self[key]
    else:
      self[key] = default
    return default


def add_metaclass(metaclass: abc.ABCMeta) -> Callable[[Any], object]:
  """Class decorator for creating a class with a metaclass.

  This supports creating metaclass with slots variable.
  """

  def wrapper(cls: Any) -> object:
    orig_vars = cls.__dict__.copy()
    slots = orig_vars.get("__slots__")
    if slots is not None:
      if isinstance(slots, str):
        slots = [slots]
      for slots_var in slots:
        orig_vars.pop(slots_var)
    orig_vars.pop("__dict__", None)
    orig_vars.pop("__weakref__", None)
    if hasattr(cls, "__qualname__"):
      orig_vars["__qualname__"] = cls.__qualname__
    return metaclass(cls.__name__, cls.__bases__, orig_vars)

  return wrapper


def reraise(prefix: Optional[str] = None, suffix: Optional[str] = None) -> None:
  """Reraise an exception with an additional message.

  Args:
    prefix: prefix to add to the current exception.
    suffix: suffix to add to the current exception.
  """
  exc_type, exc_value, exc_traceback = sys.exc_info()
  prefix = prefix or ""
  suffix = "\n" + suffix if suffix else ""
  msg = prefix + str(exc_value) + suffix
  six_reraise(exc_type, exc_type(msg), exc_traceback) # type: ignore


@contextlib.contextmanager
def try_reraise(*args: Any, **kwargs: Any) -> Any:
  """Reraise an exception with an additional message."""
  try:
    yield
  except Exception: # pylint: disable=broad-except
    reraise(*args, **kwargs)


@no_type_check
def six_reraise(tp, value, tb=None):
  try:
    if value is None:
      value = tp()
    if value.__traceback__ is not tb:
      raise value.with_traceback(tb)
    raise value
  finally:
    value = None
    tb = None


@no_type_check
def zip_dict(*dicts):
  """Iterate over items of dictionaries grouped by their keys."""
  for key in set(chain(*dicts)): # set merge all keys
    # Will raise KeyError if the dict don't have the same keys
    yield key, tuple(d[key] for d in dicts)


def item_to_type_and_shape(item: ValueType) -> Tuple[str, List]:
  """Datum item to type and shape."""
  item = np.array(item)

  shape = list(item.shape)
  if item.dtype == np.bool_:
    return 'int', shape
  item = item.flatten()
  if np.issubdtype(item.dtype, np.integer):
    return 'int', shape
  elif np.issubdtype(item.dtype, np.floating):
    return 'float', shape
  elif is_string(item):
    return 'string', check_and_image_shape(item, shape)
  else:
    raise ValueError(f'Unsupported value: {item}.')


def check_and_image_shape(item: ValueType, shape: List) -> List:
  """Check whether a string is image filename.

  Args:
    item: input string to check.

  Returns:
    a list, item shape.
  """
  if len(item.shape) > 0:
    item = str(item[0])
  if item.endswith(('.jpg', '.jpeg', '.png')):
    import cv2
    im = cv2.imread(item)
    if im is not None:
      return list(im.shape)
  return shape


def is_string(item: Any) -> bool:
  """Check if the object contains string or bytes."""
  if isinstance(item, (bytes, bytearray, str)):
    return True
  elif (isinstance(item, (tuple, list)) and all(is_string(x) for x in item)):
    return True
  elif (isinstance(item, np.ndarray) and # binary or unicode
        (item.dtype.kind in ("U", "S") or item.dtype == object)):
    return True
  return False


def datum_to_type_and_shape(datum: DatumType, sparse_features: Optional[List[str]] = None) -> Dict:
  """Get object type and shape from value."""
  if not isinstance(datum, dict):
    raise ValueError(f'Input type is not supported, datum: {datum}')
  outputs = {}
  for key, value in datum.items():
    otype, shape = item_to_type_and_shape(value)
    if sparse_features and key in sparse_features:
      outputs[key] = {'type': otype, 'shape': shape, 'dense': False}
    else:
      outputs[key] = {'type': otype, 'shape': shape, 'dense': True}
  return outputs


class memoized_property(property): # pylint: disable=invalid-name
  """Descriptor that mimics @property but caches output in member variable."""

  @no_type_check
  def __get__(self, obj, objtype=None):
    # See https://docs.python.org/3/howto/descriptor.html#properties
    if obj is None:
      return self
    if self.fget is None:
      raise AttributeError("unreadable attribute")
    attr = "__cached_" + self.fget.__name__
    cached = getattr(obj, attr, None)
    if cached is None:
      cached = self.fget(obj)
      setattr(obj, attr, cached)
    return cached


def deserialize_object(identifier: Any,
                       module_objects: Dict,
                       printable_module_name: str = 'object') -> object:
  """Deserialize object using name.

  Args:
    identifier: a string or function.
    module_objects: modules global objects.
    printable_module_name: name of the module,

  Returns:
    deserialized class.

  Raises:
    ValueError: if identifier does not exist or not supported.
  """
  if identifier is None:
    return None

  if isinstance(identifier, str):
    obj = module_objects.get(identifier)
    if obj is None:
      raise ValueError('Unknown ' + printable_module_name + ':' + identifier)
    return obj
  elif tf_inspect.isfunction(identifier):
    return identifier
  else:
    raise ValueError(f'Could not interpret serialized {printable_module_name}:{identifier}')
