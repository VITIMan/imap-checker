# -*- coding: utf-8 -*-

"""
Check you imap INBOX and notifies in your beautiful desktop.

Purpose
```````

I am trying different mail clients in my current companies and I want to keep
up to date. Searching in different resources I decided to implement a mail
notifier.

imap-checker works as a daemon polling your imap account and looking for
new emails and notifying in your desktop using `libnotify`.

Requirements
````````````

It works in any system with python 2.7.X and libnotify installed.


Installation
````````````

You have two options

- Using pip:

::

	pip install imap_checker

- Clone github repo and install dependencies in requirements.pip file:

::

	git clone https://github.com/VITIMan/imap-checker

Usage
`````

Simply copy imap_config.example and rename to .imap_conf in your home directory and change the host, user and password with your credentials.

Then execute:

::

	imap_checker

And that's it. If you want to stop, simply use:

::

    imap_checker --stop.

Links
`````

* `GitHub <https://github.com/vitiman/imap-checker>`_
"""

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


setup(name='imap-checker',
      version=get_version(),
      description='Check you imap inbox for new mails and notifies in your desktop',
      url='https://github.com/VITIMan/imap-checker',
      long_description=__doc__,
      install_requires=[
          'python-daemon>=1.6.1',
          'pidfile>=0.1.0',
      ],
      entry_points={
          "console_scripts": [
              "imap_checker = imap_checker:run",
          ]
      },
      author='Victoriano Navarro',
      author_email='vitiman@gmail.com',
      license='LICENSE',
      packages=['imap_checker'],
      keywords="imap notify email imap-checker".split(),
      zip_safe=False)
