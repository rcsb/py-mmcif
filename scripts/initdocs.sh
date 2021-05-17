#!/bin/bash
#
# File initdocs.sh
# Date: 17-Jan-2018 for py-mmcif
#
# Setup sphinx documentation tree, auto-generate api documentation, and render
# documentation as HTML  -
#
# Dependencies for Sphinx -
#pip install recommonmark
pip install myst-parser
pip install sphinx sphinxcontrib-napoleon sphinx_bootstrap_theme
#
THISDIR="$( builtin cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
topD="$(dirname ${THISDIR})"
#
# documentation entry point
srcD="mmcif"
#
if [ ! -d ${topD}/docs-sphinx ]
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
    --extensions=["sphinxcontrib.napoleon","myst_parser"] \
    ${topD}/docs-sphinx/
    echo "+++Created new docs directory adding local extensions"
    cat ${THISDIR}/docs-resources/conf-extra.py >> ${topD}/docs-sphinx/source/conf.py
    cp  ${THISDIR}/docs-resources/about.html           ${topD}/docs-sphinx/source/_templates/about.html
    cp  ${THISDIR}/docs-resources/navigation.html      ${topD}/docs-sphinx/source/_templates/navigation.html
    cp  ${THISDIR}/docs-resources/donate.html          ${topD}/docs-sphinx/source/_templates/donate.html
    #
    #cp  ${THISDIR}/docs-resources/markdown.md          ${topD}/docs-sphinx/source/testmd.md
fi
#
rm -rf ${topD}/docs-sphinx/build
mkdir ${topD}/docs-sphinx/build
#
#export SPHINX_APIDOC_OPTIONS="members,private-members,undoc-members,show-inheritance"
#cd ${topD}/docs-sphinx/; sphinx-apidoc --separate --no-toc --no-headings --module-first --private --force --output source/test ${topD}/${srcD}
#
cd ${topD}/docs-sphinx/; sphinx-apidoc --separate   --private  --module-first  --force --output source/${srcD} ${topD}/${srcD} "tests/*","modules/*","mmcif/modules/*","mmcif/core/*"
#
echo "Rendering HTML docs"
# Overwrite the index file -
#cp  ${THISDIR}/docs-resources/index.rst           ${topD}/docs-sphinx/source/index.rst
cd ${topD}/docs-sphinx/; make html
#
#