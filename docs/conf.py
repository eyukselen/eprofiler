import sys
import os

sys.path.insert(0, os.path.abspath(".."))

import eprofiler


project = "eprofiler"
copyright = "2026, emre"
author = "emre"
release = eprofiler.__version__
source_suffix = ".rst"
master_doc = "index"
version = eprofiler.__version__

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

# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    'display_version': True,
    'logo_only': False,
}
