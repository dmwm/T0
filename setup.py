#!/usr/bin/env python

"""
Standard python setup.py file for T0 System.
To build    : python setup.py build
To install  : python setup.py install --prefix=<some dir>
To clean    : python setup.py clean
To run tests: python setup.py test
"""

__author__ = "Valentin Kuznetsov"

import sys
import os
from unittest import TextTestRunner, TestLoader
from glob import glob
from os.path import splitext, basename, join as pjoin
from distutils.core import setup
from distutils.cmd import Command
from distutils.command.install import INSTALL_SCHEMES

# add some path which will define the version,
# e.g. it can be done in T0/__init__.py
sys.path.append(os.path.join(os.getcwd(), 'src/python'))
try:
    from T0 import version as t0_version
except:
    t0_version = '1.0.0' # some default

required_python_version = '2.6'

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

    def initialize_options(self):
        """Init method"""
        self._clean_me = [ ]
        for root, dirs, files in os.walk('.'):
            for fname in files:
                if fname.endswith('.pyc'):
                    self._clean_me.append(pjoin(root, fname))

    def finalize_options(self):
        """Finalize method"""
        pass

    def run(self):
        """Run method"""
        for clean_me in self._clean_me:
            try:
                os.unlink(clean_me)
            except:
                pass

def dirwalk(relativedir):
    """
    Walk a directory tree and look-up for __init__.py files.
    If found yield those dirs. Code based on
    http://code.activestate.com/recipes/105873-walk-a-directory-tree-using-a-generator/
    """
    idir = os.path.join(os.getcwd(), relativedir)
    for fname in os.listdir(idir):
        fullpath = os.path.join(idir, fname)
        if  os.path.isdir(fullpath) and not os.path.islink(fullpath):
            for subdir in dirwalk(fullpath):  # recurse into subdir
                yield subdir
        else:
            initdir, initfile = os.path.split(fullpath)
            if  initfile == '__init__.py':
                yield initdir

def find_packages(relativedir):
    "Find list of packages in a given dir"
    packages = [] 
    for idir in dirwalk(relativedir):
        package = idir.replace(os.getcwd() + '/', '')
        package = package.replace(relativedir + '/', '')
        package = package.replace('/', '.')
        packages.append(package)
    return packages

def datafiles(idir, recursive=True):
    """Return list of data files in provided relative dir"""
    files = []
    if  idir[0] != '/':
        idir = os.path.join(os.getcwd(), idir)
    for dirname, dirnames, filenames in os.walk(idir):
        if  dirname != idir:
            continue
        if  recursive:
            for subdirname in dirnames:
                files.append(os.path.join(dirname, subdirname))
        for filename in filenames:
            if  filename[-1] == '~':
                continue
            files.append(os.path.join(dirname, filename))
    return files

def install_prefix(idir=None):
    "Return install prefix"
    inst_prefix = sys.prefix
    for arg in sys.argv:
        if  arg.startswith('--prefix='):
            inst_prefix = os.path.expandvars(arg.replace('--prefix=', ''))
            break
    if  idir:
        return os.path.join(inst_prefix, idir)
    return inst_prefix

def main():
    "Main function"
    version      = t0_version
    name         = "T0"
    description  = "CMS T0 System"
    url          = \
        "https://twiki.cern.ch/twiki/bin/viewauth/CMS/T0ASTDevelopmentPlan"
    readme       = "T0 CMS system %s" % url
    author       = "Dirk Hufnagel",
    author_email = "Dirk.Hufnagel [at] cern.ch>",
    keywords     = ["T0"]
    package_dir  = \
        {"T0": "src/python/T0", "T0Component": "src/python/T0Component"}
    packages     = find_packages('src/python')
    scriptfiles  = [] # list of scripts
    data_files   = [] # list of tuples whose entries are (dir, [data_files])
    data_files   = [(install_prefix('etc'), datafiles('etc', recursive=False)),
                    (install_prefix('bin'), datafiles('bin', recursive=False))]
    cms_license  = "CMS experiment software"
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

    # set default location for "data_files" to
    # platform specific "site-packages" location
    for scheme in list(INSTALL_SCHEMES.values()):
        scheme['data'] = scheme['purelib']

    setup(
        name                 = name,
        version              = version,
        description          = description,
        long_description     = readme,
        keywords             = keywords,
        packages             = packages,
        package_dir          = package_dir,
        data_files           = data_files,
        scripts              = scriptfiles,
        requires             = ['python (>=2.6)'],
        classifiers          = classifiers,
        cmdclass             = {'test': TestCommand, 'clean': CleanCommand},
        author               = author,
        author_email         = author_email,
        url                  = url,
        license              = cms_license,
    )

if __name__ == "__main__":
    main()
