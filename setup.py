# -*- coding: utf-8 -*-

# A very simple setup script to create a single executable
#
# hello.py is a very simple 'Hello, world' type script which also displays the
# environment in which the script runs
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

import sys
from cx_Freeze import setup, Executable

base = None
#per la gui e basta
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('bottino4.py', base=base)
]

setup(name='il_bottino_di_samas',
      version='0.1',
      description='beh si allora',
      executables=executables
      )