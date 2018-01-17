#!/bin/bash
#
# File initdocs.sh
# Date: 17-Jan-2018 for py-mmcif
#
# Setup sphinx documentation tree, auto-generate api documentation, and render
# documentation as HTML  -
#
THISDIR="$( builtin cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
topD="$(dirname ${THISDIR})"
#
# documentation entry point
srcD="mmcif"
#
if [ ! -d ${topD}/docs ]
then
    sphinx-quickstart -q --sep --makefile --no-batchfile -v 0.1 \
    --project="Python mmCIF Access Library" \
    --author="John Westbrook" \
    --release="0.1" \
    --language="en" \
    --ext-autodoc   \
    --ext-doctest    \
    --ext-intersphinx \
    --ext-todo       \
    --ext-coverage    \
    --ext-ifconfig \
    --ext-viewcode \
    --extensions="sphinxcontrib.napoleon" \
    ${topD}/docs
    echo "+++Created new docs directory adding local extensions"
    cat ${THISDIR}/docs-resources/conf-extra.py >> ${topD}/docs/source/conf.py
    cp  ${THISDIR}/docs-resources/about.html           ${topD}/docs/source/_templates/about.html
    cp  ${THISDIR}/docs-resources/navigation.html      ${topD}/docs/source/_templates/navigation.html
    cp  ${THISDIR}/docs-resources/donate.html          ${topD}/docs/source/_templates/donate.html
    #
    #cp  ${THISDIR}/docs-resources/markdown.md          ${topD}/docs/source/testmd.md
fi
#
rm -rf ${topD}/docs/build
mkdir ${topD}/docs/build
#
#export SPHINX_APIDOC_OPTIONS="members,private-members,undoc-members,show-inheritance"
#cd ${topD}/docs; sphinx-apidoc --separate --no-toc --no-headings --module-first --private --force --output source/test ${topD}/${srcD}
#
cd ${topD}/docs; sphinx-apidoc --separate   --private  --module-first  --force --output source/${srcD} ${topD}/${srcD}
#
echo "Rendering HTML docs"
# Overwrite the index file -
#cp  ${THISDIR}/docs-resources/index.rst           ${topD}/docs/source/index.rst
cd ${topD}/docs; make html
#
#