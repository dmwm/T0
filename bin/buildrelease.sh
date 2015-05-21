#!/bin/sh
set -e
##H buildrelease.sh [options] <version as string i.e. 1.9.19>
##H
##H options
##H --wmcore-tag      WMCore tag to build against, mandatory and no defaults
##H --skip-build      Tag but do not build rpm's.
##H --repo=REPO       Provide the repo file to update, defaults to comp.prereleases.
##H --remote=REMOTE   REMOTE repository to update, default to upstream.
##H
##H Tag & build a wmcore/wmagent release

TAG=true
BUILD=true
REPO=comp.prereleases
WMCORE_VERSION=
VERSION=
CVSROOT="cmscvs.cern.ch:/local/reps/CMSSW"
# use a tag so we only checkout a limited set,
# doesn't need to be recent as we do an update on the changed files to remove sticky tag
EXAMPLE_CMSDIST_TAG="builder_2011-08-02_16-19-02_wmagent"
REMOTE='upstream'

while [ $# -ge 1 ]; do
  case $1 in
    --wmcore-tag=*) WMCORE_VERSION=${1#*=}; shift;;
    --skip-build ) BUILD=false; shift ;;
    --skip-tag ) TAG=false; shift ;;
    --repo=* ) REPO=${1#*=}; shift;;
    --remote=* ) REMOTE=${1#*=}; shift;;
    -h ) perl -ne '/^##H/ && do { s/^##H ?//; print }' < $0 1>&2; exit 1 ;;
    -* ) echo "$0: unrecognised option $1, use -h for help" 1>&2; exit 1 ;;
    *  ) break ;;
  esac
done

if [ $# -lt 1 ]; then
  perl -ne '/^##H/ && do { s/^##H ?//; print }' < $0 1>&2
  exit 1
fi

VERSION=$1
GITBRANCH=$(git symbolic-ref HEAD 2>/dev/null)
GITBRANCH=${GITBRANCH##refs/heads/}

echo "Building new release of Tier0 $VERSION on ${GITBRANCH}"

# some sanity checks

if [ X${WMCORE_VERSION} == X ]; then
  echo "ABORTING - WMCore version needs to be specified"
  exit 4
fi

if ! echo ${GITBRANCH} | egrep -iq 'master|t0_' ; then
  echo "ABORTING - Can only release from master or a T0_X_Y_Z git checkout: ${GITBRANCH}"
  exit 4
fi

#if [ X"$(git status -s)" != X ]; then
#  git status
#  echo
#  echo "ABORTING - unclean working area"
#  exit 2
#fi

if [ X$(git rev-parse --show-toplevel) != X$PWD ]; then
  echo "ABORTING - not in root directory $(git rev-parse --show-toplevel)"
  exit 3
fi

# Check if tag exists
if git show-ref --verify --quiet -- "refs/tags/${VERSION}"; then
  echo "Tag $VERSION exists, skipping tag command"
  TAG=false
fi

if [ X${TAG} == Xtrue ]; then

  echo "Updating version string ..."
  perl -p -i -e "s{__version__ =.*}{__version__ = '$VERSION'}g" src/python/T0/__init__.py

  echo "Generating CHANGES file"
  LASTCOMMITLINE=$(git log -n1 --oneline -E --grep="^[0-9]+\.[0-9]+\.[0-9]+$")
  LASTCOMMIT=$(echo ${LASTCOMMITLINE} | awk '{print $1}')
  LASTVERSION=$(echo ${LASTCOMMITLINE} | awk '{print $2}')
  TMP=$(mktemp -t ${LASTVERSION}XXX)
  echo "${LASTVERSION} to ${VERSION}:" >> $TMP
  git log --pretty=format:'  - %s' ${LASTCOMMIT}.. >> $TMP
  echo "" >> $TMP
  echo "" >> $TMP
  cat CHANGES >> $TMP
  cp $TMP CHANGES
  ${EDITOR:-vi} CHANGES
  if [ $? -ne 0 ]; then
      echo "User cancelled CHANGES update"
      exit 9
  fi

  echo "committing local changes ..."
  git commit -a -s -m "$VERSION"

  echo "tagging release ..."
  git log --pretty=format:'  - %s' ${LASTCOMMIT}.. | git tag -a $VERSION -F -

  echo "pushing to ${REMOTE} ..."
  git push --tags ${REMOTE}

  echo "$VERSION tagged"
fi

echo
echo
echo
if [ X${BUILD} != Xtrue ]; then
  exit 0
fi

echo "About to request an rpm build, cancel me if any of the following are true:"
echo " *  You need an update to an external rpm i.e. couchdb, sqlalchemy etc."
echo " *  You need an updated HTTP group tag"
echo " *  You need a new external rpm dependency"
echo
echo "If so please request a build manually - see https://svnweb.cern.ch/trac/CMSDMWM/wiki/TagAndRelease"
sleep 10

echo "Requesting a builder agent build of $VERSION"
echo "Note: this may fail if the config files don't have all the necessary info in - if so see above for manual instructions"
#TODO : make sure any error here aborts the script
(set -e; \
 TMP=$(mktemp -dt XXX); \
 cd $TMP; \
 cvs -d ${CVSROOT} co -r ${EXAMPLE_CMSDIST_TAG} CMSDIST; \
 cd ${TMP}/CMSDIST; \
 cvs -d $CVSROOT update -A t0.spec wmagent.spec wmagent-dev.spec ${REPO}; \
 perl -p -i -e "s{### RPM.*}{### RPM cms t0 $VERSION}g" t0.spec; \
 perl -p -i -e "s{\+ HEAD/.*t0.spec}{+ HEAD/$VERSION t0.spec}g" ${REPO}; \
 perl -p -i -e "s{\+ HEAD/.*wmagent.spec}{+ HEAD/$WMCORE_VERSION wmagent.spec}g" ${REPO}; \
 cvs commit -m"t0 $VERSION" t0.spec ${REPO};
)
if [ $? -ne 0 ]; then
  echo "RPM Request failed - please request manually"
  exit 6
fi


echo "Requested rpm build - should take 30 mins"
echo "Will then appear at"
echo "https://twiki.cern.ch/twiki/bin/view/CMS/DMWMBuildsStatusPreReleases"
echo "or https://twiki.cern.ch/twiki/bin/viewauth/CMS/DMWMBuildsStatusReleases"

exit 0
