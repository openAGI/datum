# Copyright 2021 The OpenAGI Datum Authors.
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
import tensorflow as tf

from datum.configs import config_base


class _TestConfig(config_base.ConfigBase):
  x = config_base.create_config(name="x",
                                ty=int,
                                docstring="the answer to everything",
                                default_factory=lambda: 42)
  y = config_base.create_config(name="y",
                                ty=float,
                                docstring="a tasty pie",
                                default_factory=lambda: 3.14)


class _NestedTestConfig(config_base.ConfigBase):
  opts = config_base.create_config(name="opts", ty=_TestConfig, docstring="nested config_base")


class ConfigBaseTest(tf.test.TestCase):

  def test_docstring(self):
    self.assertEqual(_TestConfig.x.__doc__, "the answer to everything")
    self.assertEqual(_TestConfig.y.__doc__, "a tasty pie")

  def test_create_config(self):
    opts = _TestConfig()
    self.assertEqual(opts.x, 42)
    self.assertEqual(opts.y, 3.14)
    self.assertIsInstance(opts.x, int)
    self.assertIsInstance(opts.y, float)
    opts.x = 0
    self.assertEqual(opts.x, 0)
    with self.assertRaises(TypeError):
      opts.x = 3.14
    opts.y = 0.0
    self.assertEqual(opts.y, 0.0)
    with self.assertRaises(TypeError):
      opts.y = 42

  def test_merge_configs(self):
    config_base1, config_base2 = _TestConfig(), _TestConfig()
    with self.assertRaises(ValueError):
      config_base.merge_configs()
    merged_config_base = config_base.merge_configs(config_base1, config_base2)
    self.assertEqual(merged_config_base.x, 42)
    self.assertEqual(merged_config_base.y, 3.14)
    config_base1.x = 0
    config_base2.y = 0.0
    merged_config_base = config_base.merge_configs(config_base1, config_base2)
    self.assertEqual(merged_config_base.x, 0)
    self.assertEqual(merged_config_base.y, 0.0)

  def test_merge_nested_config(self):
    config_base1, config_base2 = _NestedTestConfig(), _NestedTestConfig()
    merged_config_base = config_base.merge_configs(config_base1, config_base2)
    self.assertEqual(merged_config_base.opts, None)
    config_base1.opts = _TestConfig()
    merged_config_base = config_base.merge_configs(config_base1, config_base2)
    self.assertEqual(merged_config_base.opts, _TestConfig())
    config_base2.opts = _TestConfig()
    merged_config_base = config_base.merge_configs(config_base1, config_base2)
    self.assertEqual(merged_config_base.opts, _TestConfig())
    config_base1.opts.x = 0
    config_base2.opts.y = 0.0
    merged_config_base = config_base.merge_configs(config_base1, config_base2)
    self.assertEqual(merged_config_base.opts.x, 0)
    self.assertEqual(merged_config_base.opts.y, 0.0)

  def test_merge_config_invalid(self):
    with self.assertRaises(TypeError):
      config_base.merge_configs(0)
    config_base1, config_base2 = _TestConfig(), _NestedTestConfig()
    with self.assertRaises(TypeError):
      config_base.merge_configs(config_base1, config_base2)

  def test_no_spurious_Attrs(self):
    test_config_base = _TestConfig()
    with self.assertRaises(AttributeError):
      test_config_base.wrong_attr = True
    with self.assertRaises(AttributeError):
      _ = test_config_base.wrong_attr


if __name__ == "__main__":
  tf.test.main()
