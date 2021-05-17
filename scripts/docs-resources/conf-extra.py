# -*- coding: utf-8 -*-
#
# File: conf-extra.py
#
#
# -----------------------------------------
#
# for markdown support --
from recommonmark.parser import CommonMarkParser

# The suffix of source filenames.
source_suffix = [".rst", ".md"]

source_parsers = {
    ".md": CommonMarkParser,
}
#


autoclass_content = "both"
autodoc_member_order = "bysource"
autodoc_default_flags = [
    "members",
    "undoc-members",
    "private-members",
    "special-members",
]


def Xautodoc_skip_member(app, what, name, obj, skip, options):
    exclusions = {"__weakref__", "__doc__", "__module__", "__dict__", "__init__"}
    exclude = name in exclusions or name.startswith("_abc_")
    # return skip or exclude
    return False


import sys


def autodoc_skip_member(app, what, name, obj, skip, options):
    ok = False
    if name.startswith("_abc_"):
        ok = True
        sys.stderr.write("Skipping %s\n" % str(name))

    return ok


def setup(app):
    app.connect("autodoc-skip-member", autodoc_skip_member)
    # app.add_stylesheet("styles-onedep.css")  # sphinx > 1.6


#
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import sys
import os

# sys.path.insert(0, os.path.abspath('../../mmcif'))
sys.path.insert(0, os.path.abspath("../.."))

# for markdown support --
# from recommonmark.parser import CommonMarkParser

extensions = ["sphinxcontrib.napoleon", "sphinx.ext.autodoc", "sphinx.ext.todo", "sphinx.ext.ifconfig", "sphinx.ext.viewcode", "myst_parser"]

#
html_sidebars = {}

source_suffix = [".rst", ".md"]

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = "index"

# General information about the project.
project = u"mmcif"
copyright = u"RCSB"
author = u"John Westbrook"

# The suffix of source filenames.
source_suffix = [".rst", ".md"]

# source_parsers = {
#    ".md": CommonMarkParser,
# }
#

import sphinx_bootstrap_theme

# Activate the theme.
html_theme = "bootstrap"
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()


# (Optional) Logo. Should be small enough to fit the navbar (ideally 24x24).
# Path should be relative to the ``_static`` files directory.
# html_logo = '_static/wwpdb-logo-20px.png'
html_logo = "_static/onedep-logo-45px.png"

# Theme options are theme-specific and customize the look and feel of a
# theme further.
html_theme_options = {
    # Navigation bar title. (Default: ``project`` value)
    "navbar_title": "mmcif",
    # Tab name for entire site. (Default: "Site")
    #    'navbar_site_name': "wwPDB",
    "navbar_site_name": "Modules",
    # A list of tuples containing pages or urls to link to.
    # Valid tuples should be in the following forms:
    #    (name, page)                 # a link to a page
    #    (name, "/aa/bb", 1)          # a link to an arbitrary relative url
    #    (name, "http://example.com", True) # arbitrary absolute url
    # Note the "1" or "True" value above as the third argument to indicate
    # an arbitrary url.
    #
    #'navbar_links': [
    #    ("Examples", "examples"),
    #    ("Link", "http://example.com", True),
    # ],
    "navbar_links": [],
    # Render the next and previous page links in navbar. (Default: true)
    "navbar_sidebarrel": "true",
    # Render the current pages TOC in the navbar. (Default: true)
    "navbar_pagenav": "",
    # Tab name for the current pages TOC. (Default: "Page")
    "navbar_pagenav_name": "",
    # Global TOC depth for "site" navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    "globaltoc_depth": 1,
    # Include hidden TOCs in Site navbar?
    #
    # Note: If this is "false", you cannot have mixed ``:hidden:`` and
    # non-hidden ``toctree`` directives in the same page, or else the build
    # will break.
    #
    # Values: "true" (default) or "false"
    "globaltoc_includehidden": "false",
    # HTML navbar class (Default: "navbar") to attach to <div> element.
    # For black navbar, do "navbar navbar-inverse"
    "navbar_class": "navbar",
    # Fix navigation bar to top of page?
    # Values: "true" (default) or "false"
    "navbar_fixed_top": "true",
    # Location of link to source.
    # Options are "nav" (default), "footer" or anything else to exclude.
    "source_link_position": "",
    # Bootswatch (http://bootswatch.com/) theme.
    #
    # Options are nothing (default) or the name of a valid theme
    # such as "amelia" or "cosmo".
    ## sandstone is reasonable
    # 'bootswatch_theme': "sandstone",
    # 'bootswatch_theme': "united",
    ## readable is awkward
    # 'bootswatch_theme': "readable",
    ##
    "bootswatch_theme": "spacelab",
    # Choose Bootstrap version.
    # Values: "3" (default) or "2" (in quotes)
    "bootstrap_version": "3",
}
