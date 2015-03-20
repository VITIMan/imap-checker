# -*- coding: utf-8 -*-

# python imports
import re
import os
from setuptools import setup

base_dir = os.path.dirname(os.path.abspath(__file__))


def get_version(filename="imap_checker/__init__.py"):
    with open(os.path.join(base_dir, filename)) as initfile:
        for line in initfile.readlines():
            m = re.match("__version__ *= *['\"](.*)['\"]", line)
            if m:
                return m.group(1)


# conditional_dependencies = {
# }

setup(name='imap-checker',
      version=get_version(),
      description='Imap mail checker',
      url='https://github.com/VITIMan/imap-checker',
      install_requires=[
          'python-daemon>=1.6.1',  # 2.0.5 tests
          'pidfile>=0.1.0',  # 0.1.1 tests
      ],
      entry_points={
          "console_scripts": [
              "imap_checker = imap_checker:run",
          ]
      },
      author='Victoriano Navarro',
      author_email='vitiman@gmail.com',
      license='MIT',
      packages=['imap_checker'],
      keywords="imap notify email imap-checker".split(),
      zip_safe=False)
