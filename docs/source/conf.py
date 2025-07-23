# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


project = 'gatenet'
copyright = '2025, MJ Anglin'
author = 'MJ Anglin'
release = '0.8.9'  # Update to the latest version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',       # Pulls in docstrings from your code
    'sphinx.ext.napoleon',      # Supports Google-style and NumPy-style docstrings
    'sphinx.ext.viewcode',      # Adds links to highlighted source code
    'sphinx.ext.githubpages',   # For GitHub Pages (optional if you're not using it)
    "sphinx_autodoc_typehints", # Adds type hints to the documentation
]

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

highlight_language = 'python'
typehints_fully_qualified = False


templates_path = ['_templates']
exclude_patterns = []

autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'private-members': False,
    'show-inheritance': True,
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


# -- HTML output options --
html_theme = 'furo'  # Modern, clean theme. Alternatives: 'sphinx_rtd_theme', 'alabaster', etc.
html_static_path = ['_static']




# Logo and favicon
html_logo = "_static/apple-touch-icon.png"
html_favicon = "_static/favicon.ico"


# Theme options for Furo (see https://pradyunsg.me/furo/customisation/)
html_theme_options = {
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
    # Add more Furo options here as needed
}

# Add custom CSS and webmanifest for further style tweaks and PWA support
def setup(app):
    app.add_css_file('style.css')  # Place your custom CSS in _static/style.css
    app.add_js_file('site.webmanifest', type='application/manifest+json')
    app.add_js_file('network-footer.js')  # Adds animated networking footer

# Example: To use a custom template, add HTML files to _templates/ and reference them in your .rst files.

# Example: To change autodoc member order, you can add this to autodoc_default_options:
# 'member-order': 'bysource',

