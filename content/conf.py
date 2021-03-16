# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../'))


# -- Project information -----------------------------------------------------

project = 'Solar Resource Assessment in Python'
copyright = '2021, Assessing Solar'
#author = 'Adam R. Jensen & Javier L. Lorente'

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = False


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',  # automatic documentation of functions
    'sphinx.ext.mathjax', # renders readable math live in the browser
    'sphinxcontrib.googleanalytics',  #
    'sphinx_thebe',  # converts static HTML pages into interactive pages with code cells run remotely by a Binder kernel
    'sphinx.ext.githubpages', # creates .nojekyll file necessary for GitHub
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive',
    'sphinx_togglebutton',
    'sphinx_copybutton',  # adds a little “copy” button to the right of code blocks
    'myst_nb',  #  tool for working with Jupyter Notebooks in the Sphinx ecosystem (build on nbsphinx)
    #'nbsphinx',  # Jupyter Notebook Tools for Sphinx, adds parser for .ipynb. Clashes with myst_nb
    #'nbclient',  # tool for running Jupyter Notebooks in different execution contexts
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# The name for this set of Sphinx documents.
# "<project> v<release> documentation" by default.
html_title = 'Assessing Solar'
# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The full version, including alpha/beta/rc tags
release = '0.0.1'
version = '2021'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
#todo_include_todos = True

# Google Analytics ID to enable tracking of site traffic
googleanalytics_id = "G-J6885V9EEK"
googleanalytics_enabled = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_book_theme'

html_theme_options = {
    "path_to_docs": "content/",
    "repository_url": "https://github.com/AssessingSolar/Solar-Resource-Assessment-in-Python",
    "use_repository_button": True,  # adds a link to your repository
    #"use_edit_page_button": True,  # adds a button to each page that will allow users to edit the page text directly and submit a pull request to update the documentation
    "use_issues_button": True,  # adds button to open an issue about the current page
    "use_download_button": True,  # adds a button to download files
    "repository_branch": "master",  # branch where the edit button will point to (default: Master)
    #"home_page_in_toc": True,  # adds the landing page of your site to the table of contents
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "notebook_interface": "jupyterlab",
        "thebe": True,
	"collapse_navigation" : False
    },
}

nb_render_plugin = "default"

html_logo = "graphics/assessing_solar_logo.png"
#html_favicon = "path/to/favicon.ico"
#extra_navbar = "<p>Your HTML</p>"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# Do not execute cells
jupyter_execute_notebooks = "off"