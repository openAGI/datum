# Copyright 2020 The OpenAGI Datum Authors.
# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================

from __future__ import annotations # type: ignore

from typing import Any, Callable


class ConfigBase(object):
  """Base class for representing a set of tf.data config.

  Attributes:
    _configs: Stores the config values.
  """

  def __init__(self): # type: ignore
    object.__setattr__(self, "_configs", {})

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, self.__class__):
      return NotImplemented
    # pylint: disable=protected-access
    for name in set(self._configs) | set(other._configs): # type: ignore
      if getattr(self, name) != getattr(other, name):
        return False
    return True

  def __ne__(self, other: object) -> bool:
    if isinstance(other, self.__class__):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __setattr__(self, name: str, value: Any) -> None:
    if hasattr(self, name):
      object.__setattr__(self, name, value)
    else:
      raise AttributeError("Cannot set the property %s on %s." % (name, type(self).__name__))

  def merge(self, configs: ConfigBase) -> ConfigBase:
    return merge_configs(self, configs)


def create_config(name: str,
                  ty: Any,
                  docstring: str,
                  default_factory: Callable[[], Any] = lambda: None) -> property:
  """Creates a type-checked property.

  Args:
    name: The name to use.
    ty: The type to use. The type of the property will be validated when it
      is set.
    docstring: The docstring to use.
    default_factory: A callable that takes no arguments and returns a default
      value to use if not set.
  Returns:
    A type-checked property.
  """

  def get_fn(config: ConfigBase) -> Any:
    # pylint: disable=protected-access
    if name not in config._configs: # type: ignore
      config._configs[name] = default_factory() # type: ignore
    return config._configs.get(name) # type: ignore

  def set_fn(config: ConfigBase, value: Any) -> None:
    if not isinstance(value, ty):
      raise TypeError("Property \"%s\" must be of type %s, got: %r (type: %r)" %
                      (name, ty, value, type(value)))
    # pylint: disable=protected-access
    config._configs[name] = value # type: ignore

  return property(get_fn, set_fn, None, docstring)


def merge_configs(*configs_list: ConfigBase) -> ConfigBase:
  """Merges the given configs, returning the result as a new configs object.
  The input arguments are expected to have a matching type that derives from
  `ConfigBase` (and thus each represent a set of configs). The method outputs
  an object of the same type created by merging the sets of configs represented
  by the input arguments.
  The sets of configs can be merged as long as there does not exist an config
  with different non-default values.
  If an config is an instance of `ConfigBase` itself, then this method is
  applied recursively to the set of configs represented by this config.
  Args:
    *configs_list: configs to merge
  Raises:
    TypeError: if the input arguments are incompatible or not derived from
      `ConfigBase`
    ValueError: if the given configs cannot be merged
  Returns:
    A new configs object which is the result of merging the given configs.
  """
  if len(configs_list) < 1:
    raise ValueError("At least one configs should be provided")
  result_type = type(configs_list[0])

  for configs in configs_list:
    if not isinstance(configs, result_type):
      raise TypeError("Incompatible configs type: %r vs %r" % (type(configs), result_type))

  if not isinstance(configs_list[0], ConfigBase):
    raise TypeError("The inputs should inherit from `ConfigBase`")

  default_configs = result_type()
  result = result_type()
  for configs in configs_list:
    # Iterate over all set configs and merge the into the result.
    # pylint: disable=protected-access
    for name in configs._configs: # type: ignore
      this = getattr(result, name)
      that = getattr(configs, name)
      default = getattr(default_configs, name)
      if that == default:
        continue
      elif this == default:
        setattr(result, name, that)
      elif isinstance(this, ConfigBase):
        setattr(result, name, merge_configs(this, that))
      elif this != that:
        raise ValueError("Cannot merge incompatible values (%r and %r) of config: %s" %
                         (this, that, name))
  return result
