#!/usr/bin/python
# ==============================================================================
#
# Test that checks if we have any issues with case insensitive filesystems.

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))


def main():
  # Make sure BASE_DIR is project root.
  # If it doesn't, we probably computed the wrong directory.
  if not os.path.isdir(os.path.join(BASE_DIR, 'datum')):
    raise AssertionError('BASE_DIR = {} is not project root'.format(BASE_DIR))

  for dirpath, dirnames, filenames in os.walk(BASE_DIR, followlinks=True):
    lowercase_directories = [x.lower() for x in dirnames]
    lowercase_files = [x.lower() for x in filenames]

    lowercase_dir_contents = lowercase_directories + lowercase_files
    if len(lowercase_dir_contents) != len(set(lowercase_dir_contents)):
      raise AssertionError('Files with same name but different case detected '
                           'in directory: {}'.format(dirpath))


if __name__ == '__main__':
  main()
