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
import dataclasses
import math
import re
from typing import Dict, List, Optional

_SUB_SPEC_RE = re.compile(
    r'''
^
 (?P<split>\w+)
 (\[
  ((?P<from>-?\d+)
   (?P<from_pct>%)?)?
  :
  ((?P<to>-?\d+)
   (?P<to_pct>%)?)?
 \])?
$
''', re.X)

_ADDITION_SEP_RE = re.compile(r'\s*\+\s*')


@dataclasses.dataclass
class _AbsoluteInstruction(object):
  """A machine friendly slice: defined absolute positive boundaries."""
  splitname: str = 'test'
  from_: Optional[int] = None
  to: Optional[int] = None


@dataclasses.dataclass
class _RelativeInstruction(object):
  """Represents a single parsed slicing instruction, can use % and negatives."""
  splitname: str = 'test'
  from_: Optional[int] = None
  to: Optional[int] = None
  unit: Optional[str] = None
  rounding: str = 'closest'


def _pct_to_abs_pct1(boundary: int, num_examples: int) -> int:
  if num_examples < 100:
    raise AssertionError('Using "pct1_dropremainder" rounding on a split with less than 100 '
                         'elements is forbidden: it always results in an empty dataset.')
  return boundary * math.trunc(num_examples / 100.)


def _pct_to_abs_closest(boundary: int, num_examples: int) -> int:
  return int(round(boundary * num_examples / 100.))


def _rel_to_abs_instr(rel_instr: _RelativeInstruction, name2len: Dict[str,
                                                                      int]) -> _AbsoluteInstruction:
  """Returns _AbsoluteInstruction instance for given RelativeInstruction.

  Args:
    rel_instr: RelativeInstruction instance.
    name2len: dict {split_name: num_examples}.
  """
  pct_to_abs = (_pct_to_abs_closest if rel_instr.rounding == 'closest' else _pct_to_abs_pct1)
  split = rel_instr.splitname
  if split not in name2len:
    raise ValueError(f'Unknown split "{split}". Should be one of {list(name2len)}.')
  num_examples = name2len[split]
  from_ = rel_instr.from_
  to = rel_instr.to
  if rel_instr.unit == '%':
    from_ = 0 if from_ is None else pct_to_abs(from_, num_examples)
    to = num_examples if to is None else pct_to_abs(to, num_examples)
  else:
    from_ = 0 if from_ is None else from_
    to = num_examples if to is None else to
  if abs(from_) > num_examples or abs(to) > num_examples:
    raise AssertionError(
        f'Requested slice [{from_}:{to}] incompatible with {num_examples} examples.')
  if from_ < 0:
    from_ = num_examples + from_
  elif from_ == 0:
    from_ = None
  if to < 0:
    to = num_examples + to
  elif to == num_examples:
    to = None
  return _AbsoluteInstruction(split, from_, to)


class ReadInstruction(object):
  """Reading instruction for a dataset.

  Examples of usage: ```
  """

  def _init(self, relative_instructions: List[_RelativeInstruction]) -> None:
    self._relative_instructions = relative_instructions

  @classmethod
  def _read_instruction_from_relative_instructions(
      cls, relative_instructions: List[_RelativeInstruction]) -> List[_RelativeInstruction]:
    """Returns ReadInstruction obj initialized with relative_instructions."""
    # Use __new__ to bypass __init__ used by public API and not conveniant here.
    result = cls.__new__(cls)
    result._init(relative_instructions) # pylint: disable=protected-access
    return result

  def __init__(
      self,
      split_name: str,
      rounding: str = 'closest',
      from_: Optional[int] = None,
      to: Optional[int] = None,
      unit: Optional[str] = None,
  ):
    """Initialize ReadInstruction.
    Args:
      split_name (str): name of the split to read. Eg: 'train'.
      rounding (str): The rounding behaviour to use when percent slicing is
        used. Ignored when slicing with absolute indices.
        Possible values:
         - 'closest' (default): The specified percentages are rounded to the
           closest value. Use this if you want specified percents to be as
           much exact as possible.
         - 'pct1_dropremainder': the specified percentages are treated as
           multiple of 1%. Use this option if you want consistency. Eg:
             len(5%) == 5 * len(1%).
           Using this option, one might not be able to use the full set of
           examples, if the number of those is not a multiple of 100.
      from_ (int):
      to (int): alternative way of specifying slicing boundaries. If any of
        {from_, to, unit} argument is used, slicing cannot be specified as
        string.
      unit (str): optional, one of:
        '%': to set the slicing unit as percents of the split size.
        'abs': to set the slicing unit as absolute numbers.
    """
    if from_ is None and to is None and unit is None:
      unit = '%'
    self._init([_RelativeInstruction(split_name, from_, to, unit, rounding)])

  @classmethod
  def from_spec(cls, spec: str) -> object:
    """Creates a ReadInstruction instance out of a string spec.

    Args:
      spec (str): split(s) + optional slice(s) to read. A slice can be
            specified, using absolute numbers (int) or percentages (int). E.g.
              `test`: test split.
              `test + validation`: test split + validation split.
              `test[10:]`: test split, minus its first 10 records.
              `test[:10%]`: first 10% records of test split.
              `test[:-5%]+train[40%:60%]`: first 95% of test + middle 20% of
                                           train.
    Returns:
      ReadInstruction instance.
    """
    spec = str(spec) # Need to convert to str in case of `Split` instance.
    subs = _ADDITION_SEP_RE.split(spec)
    if not subs:
      raise AssertionError('No instructions could be built out of %s' % spec)
    instruction = _str_to_relative_instruction(subs[0])
    return sum([_str_to_relative_instruction(sub) for sub in subs[1:]], instruction)

  def __add__(self, other: object) -> object:
    """Returns a new ReadInstruction obj, result of appending other to self."""
    if not isinstance(other, ReadInstruction):
      msg = 'ReadInstruction can only be added to another ReadInstruction obj.'
      raise AssertionError(msg)
    other_ris = other._relative_instructions # pylint: disable=protected-access
    if self._relative_instructions[0].rounding != other_ris[0].rounding:
      raise AssertionError('It is forbidden to sum ReadInstruction instances '
                           'with different rounding values.')
    return self._read_instruction_from_relative_instructions(self._relative_instructions + other_ris)

  def __str__(self) -> str:
    return 'ReadInstruction(%s)' % self._relative_instructions

  def to_absolute(self, name2len: Dict[str, int]) -> List[_AbsoluteInstruction]:
    """Translate instruction into a list of absolute instructions.

    Those absolute instructions are then to be added together.
    Args:
      name2len: dict associating split names to number of examples.
    Returns:
      list of _AbsoluteInstruction instances (corresponds to the + in spec).
    """
    return [_rel_to_abs_instr(rel_instr, name2len) for rel_instr in self._relative_instructions]


def _str_to_relative_instruction(spec: str) -> ReadInstruction:
  """Returns ReadInstruction for given string."""
  res = _SUB_SPEC_RE.match(spec)
  if not res:
    raise AssertionError(f'Unrecognized instruction format: {spec}')
  unit = '%' if res.group('from_pct') or res.group('to_pct') else 'abs'
  return ReadInstruction(
      split_name=res.group('split'),
      rounding='closest',
      from_=int(res.group('from')) if res.group('from') else None,
      to=int(res.group('to')) if res.group('to') else None,
      unit=unit,
  )
