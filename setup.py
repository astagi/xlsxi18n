#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name="xlsxi18n",
      py_modules=['xlsxi18n'],
      version="0.0",
      description="Simple command line utility to generate Android language files for your app from xlsx files.",
      license="MIT",
      author="Andrea Stagi",
      author_email="stagi.andrea@gmail.com",
      url="https://github.com/atooma/xlsxi18n",
      keywords= "i18n app android test team script",
      install_requires=[
        "openpyxl",
      ],
      entry_points = {
        'console_scripts': [
            'xlsxi18n = xlsxi18n:main',
        ],
      },
      zip_safe = True)