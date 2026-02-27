# Configuration file for the Sphinx documentation builder.
import sys
import os


sys.path.insert(0, os.path.abspath(".."))

project = "eprofiler"
copyright = "2024, emre"
author = "emre"
release = "0.0.6"
source_suffix = ".rst"
master_doc = "index"
version = "0.0.6"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon"
]

napoleon_google_docstring = True
napoleon_use_param = True
napoleon_use_ivar = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.idea']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
