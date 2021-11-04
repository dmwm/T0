#!/bin/bash
#
# Script used to build each application from the WMCore repo and upload to pypi.
#
# Usage
# Build a single package:
# sh etc/build_pypi_packages.sh <package name>
# Build all WMCore packages:
# sh etc/build_pypi_packages.sh all
#

set -x

# package passed as parameter, can be one of PACKAGES or "all"
TOBUILD="t0"
# list of packages that can be built and uploaded to pypi
#PACKAGES="wmagent wmcore reqmon reqmgr2 reqmgr2ms global-workqueue acdcserver t0"
PACKAGES="t0"
PACKAGE_REGEX="^($(echo $PACKAGES | sed 's/\ /|/g')|all)$"

if [[ -z $TOBUILD ]]; then
  echo "Usage: sh etc/build_pypi_packages.sh <package name>"
  echo "Usage: sh etc/build_pypi_packages.sh all"
  exit 1
fi


# check to make sure a valid package name was passed
if [[ ! $TOBUILD =~ $PACKAGE_REGEX ]]; then
  echo "$TOBUILD is not a valid package name"
  echo "Supported packages are $PACKAGES"
  exit 1
fi

# update package list when building all packages
if [[ $TOBUILD == "all" ]]; then
  TOBUILD=$PACKAGES
fi

# loop through packages to build
for package in $TOBUILD; do
  echo "==========" $package "=========="
  released="$( curl -X GET https://pypi.org/pypi/${package}/json | jq -r '.releases' | jq 'keys' )"
  tag=$( grep -m 1 version ../T0/src/python/T0/__init__.py | sed -E "s/version|_|\ |=|'//g")
  if [[ ${released} =~ "\"${tag}\"" ]]; then
     echo "$package-$tag file already exists. See https://pypi.org/help/#file-name-reuse for more information."
     exit 0
  fi

  # make a copy of requirements.txt to reference for each build
  cp requirements.txt requirements.t0.txt

  # update the setup script template with package name
  sed "s/PACKAGE_TO_BUILD/$package/" setup_template.py > setup.py

  # build requirements.txt file
  awk "/($package$)|($package,)/ {print \$1}" requirements.t0.txt > requirements.txt

  # build the package
  python3 setup.py clean sdist
  if [[ $? -ne 0 ]]; then
    echo "Error building package $package"
    exit 1
  fi
  
  # upload the package to pypi
  echo "Uploading package $package to PyPI"
  #twine upload dist/$package-*
  twine upload --repository pypi dist/$package-*
  
  # replace requirements.txt contents
  cp requirements.t0.txt requirements.txt
done


