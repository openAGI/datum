# coding=utf-8
# Copyright 2020 The OpenAGI Datum Authors.
# Copyright 2020 The TensorFlow Datasets Authors.
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

# Lint as: python3
"""Wrapper around tqdm."""

import contextlib
from typing import Any, Callable, Iterator, List, no_type_check

from tqdm import auto as tqdm_lib


class EmptyTqdm(object):
  """Dummy tqdm which doesn't do anything."""

  def __init__(self, *args: Any, **kwargs: Any): # pylint: disable=unused-argument
    self._iterator = args[0] if args else None

  def __iter__(self) -> Iterator:
    return iter(self._iterator)

  def __getattr__(self, _: Any) -> Callable:
    """Return empty function."""

    def empty_fn(*args: Any, **kwargs: Any) -> Any: # pylint: disable=unused-argument
      return

    return empty_fn

  def __enter__(self) -> object:
    return self

  @no_type_check
  def __exit__(self, type_, value, traceback):
    return


_active = True


@no_type_check
def tqdm(*args, **kwargs):
  if _active:
    return tqdm_lib.tqdm(*args, **kwargs)
  else:
    return EmptyTqdm(*args, **kwargs)


@no_type_check
def async_tqdm(*args, **kwargs):
  if _active:
    return _async_tqdm(*args, **kwargs)
  else:
    return EmptyTqdm(*args, **kwargs)


@no_type_check
def disable_progress_bar():
  """Disabled Tqdm progress bar.

  Usage:

  tfds.disable_progress_bar()
  """
  # Replace tqdm
  global _active
  _active = False


@no_type_check
@contextlib.contextmanager
def _async_tqdm(*args, **kwargs):
  """Wrapper around Tqdm which can be updated in threads.

  Usage:

  ```
  with utils.async_tqdm(...) as pbar:
    # pbar can then be modified inside a thread
    # pbar.update_total(3)
    # pbar.update()
  ```

  Args:
    *args: args of tqdm
    **kwargs: kwargs of tqdm

  Yields:
    pbar: Async pbar which can be shared between threads.
  """
  with tqdm_lib.tqdm(*args, **kwargs) as pbar:
    pbar = _TqdmPbarAsync(pbar)
    yield pbar
    pbar.clear() # pop pbar from the active list of pbar
    print() # Avoid the next log to overlapp with the bar


class _TqdmPbarAsync(object):
  """Wrapper around Tqdm pbar which be shared between thread."""
  _tqdm_bars: List[tqdm_lib.tqdm] = []

  def __init__(self, pbar: tqdm_lib.tqdm):
    self._lock = tqdm_lib.tqdm.get_lock()
    self._pbar = pbar
    self._tqdm_bars.append(pbar)

  def update_total(self, n: int = 1) -> None:
    """Increment total pbar value."""
    with self._lock:
      self._pbar.total += n
      self.refresh()

  def update(self, n: int = 1) -> None:
    """Increment current value."""
    with self._lock:
      self._pbar.update(n)
      self.refresh()

  def refresh(self) -> None:
    """Refresh all."""
    for pbar in self._tqdm_bars:
      pbar.refresh()

  def clear(self) -> None:
    """Remove the tqdm pbar from the update."""
    self._tqdm_bars.pop()
