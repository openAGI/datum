# coding=utf-8
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
import sys
import unicodedata

from datum.utils.common_utils import add_metaclass

# This set contains all letter and number characters.
_ALPHANUMERIC_CHAR_SET = set(
    chr(i) for i in range(sys.maxunicode)
    if (unicodedata.category(chr(i)).startswith("L") or unicodedata.category(chr(i)).startswith("N")
        ))


@add_metaclass(abc.ABCMeta)
class BaseTokenizer():

  @abc.abstractmethod
  def encode(self, *args, **kwargs):
    raise NotImplementedError

  @abc.abstractmethod
  def decode(self, *args, **kwargs):
    raise NotImplementedError


class InvertibleTokenizer(BaseTokenizer):

  def encode(self, text):
    """Encode a unicode string as a list of tokens.

    Args:
      text: a unicode string
    Returns:
      a list of tokens as Unicode strings
    """
    if not text:
      return []
    ret = []
    token_start = 0
    # Classify each character in the input string
    is_alnum = [c in _ALPHANUMERIC_CHAR_SET for c in text]
    for pos in range(1, len(text)):
      if is_alnum[pos] != is_alnum[pos - 1]:
        token = text[token_start:pos]
        if token != u" " or token_start == 0:
          ret.append(token)
        token_start = pos
    final_token = text[token_start:]
    ret.append(final_token)
    return ret

  def decode(self, tokens):
    """Decode a list of tokens to a unicode string.

    Args:
      tokens: a list of Unicode strings
    Returns:
      a unicode string
    """
    token_is_alnum = [t[0] in _ALPHANUMERIC_CHAR_SET for t in tokens]
    ret = []
    for i, token in enumerate(tokens):
      if i > 0 and token_is_alnum[i - 1] and token_is_alnum[i]:
        ret.append(u" ")
      ret.append(token)
    return "".join(ret)
