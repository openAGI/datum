"""OpenAGI datum is a library to create and load tfrecords as `tf.data.Dataset`.

Usage outside of TensorFlow is also supported. See the README on GitHub for further documentation.
"""

import os
import sys

from setuptools import find_packages, setup

project_name = 'datum'

version_path = os.path.join(os.path.dirname(__file__), 'datum')
sys.path.append(version_path)
from version import __version__ # isort:skip

with open('README.md') as fp:
  _LONG_DESCRIPTION = fp.read()

REQUIRED_PKGS = []

with open('requirements.txt', 'r') as f:
  ignore = 0
  for tentative_req in f.readlines():
    if tentative_req:
      if tentative_req.startswith('#'):
        ignore += 1
        if ignore > 1:
          break
      else:
        REQUIRED_PKGS.append(tentative_req.strip())

TESTS_REQUIRE = [
    'pytest',
    'pytest-xdist',
]

setup(
    name=project_name,
    version=__version__,
    description=_LONG_DESCRIPTION[0],
    long_description=_LONG_DESCRIPTION,
    author='OpenAGI',
    author_email='maintainer@openagi.io',
    url='https://github.com/openagi/datum',
    download_url='https://github.com/openagi/datum/tags',
    license='Apache 2.0',
    packages=find_packages(),
    scripts=[],
    install_requires=REQUIRED_PKGS,
    tests_require=TESTS_REQUIRE,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
    ],
    keywords='datum tensorflow tf.data datasets tfrecord',
)
