#!/usr/bin/env python

# This template for the setup script is used to build several pypi packages
# from the WMCore codebase. The variable package_name controls which package
# is built. PACKAGE_TO_BUILD is manipulated via tools/build_pypi_packages.sh
# at build time.
#
# The version number comes from WMCore/__init__.py and needs to
# follow PEP 440 conventions

from __future__ import print_function, division
import os
import sys
import subprocess
from setuptools import setup, Command
from setup_build import list_static_files, things_to_build
from setup_dependencies import dependencies

# get the WMCore version (thanks rucio devs)
sys.path.insert(0, os.path.abspath('src/python'))
try:
  from T0 import version as t0_version
except:
  print("fail to import T0")
  import T0
t0_version=subprocess.check_output(['git','describe','--tags']).strip("\n")

# we need to override 'clean' command to remove specific files
class TestCommand(Command):
    """
    Class to handle unit tests
    """
    user_options = [ ]

    def initialize_options(self):
        """Init method"""
        self._dir = os.getcwd()

    def finalize_options(self):
        """Finalize method"""
        pass

    def run(self):
        """
        Finds all the tests modules in test/, and runs them.
        """
        # list of files to exclude,
        # e.g. [pjoin(self._dir, 'test', 'exclude_t.py')]
        exclude = []
        # list of test files
        testfiles = []
        for tname in glob(pjoin(self._dir, 'test', '*_t.py')):
            if  not tname.endswith('__init__.py') and \
                tname not in exclude:
                testfiles.append('.'.join(
                    ['test', splitext(basename(tname))[0]])
                )
        testfiles.sort()
        try:
            tests = TestLoader().loadTestsFromNames(testfiles)
        except:
            print("\nFail to load unit tests", testfiles)
            raise
        test = TextTestRunner(verbosity = 2)
        test.run(tests)

class CleanCommand(Command):
    """
    Class which clean-up all pyc files
    """
    user_options = [ ]

    #def initialize_options(self):
    #    """Init method"""
    #    self._clean_me = [ ]
    #    for root, dirs, files in os.walk('.'):
    #        for fname in files:
    #            if fname.endswith('.pyc'):
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system ('rm -rfv ./dist ./src/python/*.egg-info')

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

required_python_version = '2.6'
cms_license  = "CMS experiment software"
url = "https://github.com/dmwm/T0"
# the contents of package_name are modified via tools/build_pypi_packages.sh
package_name = "PACKAGE_TO_BUILD"
packages, py_modules = things_to_build(package_name, pypi=True)
data_files = list_static_files(dependencies[package_name])
classifiers  = [
        "Development Status :: 3 - Production/Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: CMS/CERN Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Database"
]
if  sys.version < required_python_version:
    msg = "I'm sorry, but %s %s requires Python %s or later."
    print(msg % (name, version, required_python_version))
    sys.exit(1)
setup(name=package_name,
      version=t0_version,
      package_dir={'': 'src/python/'},
      packages=packages,
      py_modules=py_modules,
      data_files=data_files,
      install_requires=parse_requirements("requirements.txt"),
      maintainer='CMS DMWM Group',
      maintainer_email='hn-cms-wmdevelopment@cern.ch',
      cmdclass={
          'test': TestCommand,
          'clean': CleanCommand,
      },
      url=url,
      license=cms_license,
      )
