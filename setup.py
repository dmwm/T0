#!/usr/bin/env python
"""
Build, clean and test the t0 package.
"""
from __future__ import print_function

import imp
import os
import os.path
from distutils.core import Command, setup
from os.path import join as pjoin

from setup_build import BuildCommand, InstallCommand, get_path_to_t0_root, list_packages, list_static_files


class CleanCommand(Command):
    description = "Clean up (delete) compiled files"
    user_options = []

    def initialize_options(self):
        self.cleanMes = []
        for root, dummyDirs, files in os.walk('.'):
            for f in files:
                if f.endswith('.pyc'):
                    self.cleanMes.append(pjoin(root, f))

    def finalize_options(self):
        pass

    def run(self):
        for cleanMe in self.cleanMes:
            try:
                os.unlink(cleanMe)
            except Exception:
                pass


class EnvCommand(Command):
    description = "Configure the PYTHONPATH, DATABASE and PATH variables to" + \
                  "some sensible defaults, if not already set. Call with -q when eval-ing," + \
                  """ e.g.:
                      eval `python setup.py -q env`
                  """

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if not os.getenv('COUCHURL', False):
            # Use the default localhost URL if none is configured.
            print('export COUCHURL=http://localhost:5984')
        here = get_path_to_t0_root()

        tests = here + '/test/python'
        source = here + '/src/python'
        # Stuff we want on the path
        exepth = [here + '/etc',
                  here + '/bin']

        pypath = os.getenv('PYTHONPATH', '').strip(':').split(':')

        for pth in [tests, source]:
            if pth not in pypath:
                pypath.append(pth)

        # We might want to add other executables to PATH
        expath = os.getenv('PATH', '').split(':')
        for pth in exepth:
            if pth not in expath:
                expath.append(pth)

        print('export PYTHONPATH=%s' % ':'.join(pypath))
        print('export PATH=%s' % ':'.join(expath))

        # We want the t0 root set, too
        print('export T0_ROOT=%s' % get_path_to_t0_root())
        print('export T0BASE=$T0_ROOT')

# The actual setup command, and the classes associated to the various options

# Need all the packages we want to build by default, this will be overridden in sub-system builds.
# Since it's a lot of code determine it by magic.
DEFAULT_PACKAGES = list_packages(['src/python/T0',
                                  'src/python/T0Component'
                                 ])

# Divine out the version of t0 from t0.__init__, which is bumped by
# "bin/buildrelease.sh"

# Obnoxiously, there's a dependency cycle when building packages. We'd like
# to simply get the current t0 version by using
# from t0 import __version__
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

setup(name='T0',
      version=t0_version,
      maintainer='CMS DMWM Group',
      maintainer_email='cms-tier0-operations@cern.ch',
      cmdclass={'deep_clean': CleanCommand,
                'coverage': CoverageCommand,
                'test': TestCommand,
                'env': EnvCommand,
                'build_system': BuildCommand,
                'install_system': InstallCommand},
      # base directory for all our packages
      package_dir={'': 'src/python/'},  # % get_path_to_t0_root()},
      packages=DEFAULT_PACKAGES,
      data_files=list_static_files(),
      url="https://github.com/dmwm/T0",
      license="Apache License, Version 2.0"
      )
