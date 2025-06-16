#!/usr/bin/env python

# This setup script is used to build the T0 pypi package.
# The version number comes from T0/__init__.py and needs to
# follow PEP 440 conventions

from __future__ import print_function, division
import os
import sys
import imp
from setuptools import setup
from setup_build import list_packages, list_static_files, get_path_to_t0_root

# Obnoxiously, there's a dependency cycle when building packages. We'd like
# to simply get the current T0 version by using
# from T0 import __version__
# But PYTHONPATH isn't set until after the package is built, so we can't
# depend on the python module resolution behavior to load the version.
# Instead, we use the imp module to load the source file directly by
# filename.
t0_root = get_path_to_t0_root()
t0_package = imp.load_source('temp_module', os.path.join(t0_root,
                                                             'src',
                                                             'python',
                                                             'T0',
                                                             '__init__.py'))
t0_version = t0_package.__version__

# Requirements file for pip dependencies
requirements = "requirements.txt"


def parse_requirements(requirements_file):
    """
      Create a list for the 'install_requires' component of the setup function
      by parsing a requirements file
    """

    if os.path.exists(requirements_file):
        # return a list that contains each line of the requirements file
        return open(requirements_file, 'r').read().splitlines()
    else:
        print("ERROR: requirements file " + requirements_file + " not found.")
        sys.exit(1)


setup(name='t0',
      version=t0_version,
      maintainer='CMS DMWM Group',
      maintainer_email='cms-tier0-operations@cern.ch',
      package_dir={'': 'src/python/'},
      packages=list_packages(['src/python/T0',
                              'src/python/T0Component'
                             ]),
      data_files=list_static_files(),
      install_requires=parse_requirements(requirements),
      url="https://github.com/dmwm/T0",
      license="Apache License, Version 2.0",
      )
