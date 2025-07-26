# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


project = 'gatenet'
copyright = '2025, MJ Anglin'
author = 'MJ Anglin'
release = '0.9.0'  # Update to the latest version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',       # Pulls in docstrings from your code
    'sphinx.ext.napoleon',      # Supports Google-style and NumPy-style docstrings
    'sphinx.ext.viewcode',      # Adds links to highlighted source code
    'sphinx.ext.githubpages',   # For GitHub Pages (optional if you're not using it)
    'sphinx_sitemap',           # Generates sitemap.xml for SEO
    'sphinxext.opengraph',      # Adds OpenGraph/meta tags for SEO
    "sphinx_autodoc_typehints", # Adds type hints to the documentation
    'myst_parser',              # Enables Markdown support (for CHANGELOG.md)
    'sphinx_copybutton',        # Adds "Copy" buttons to code blocks
    'sphinx_inline_tabs',       # Enables inline tabbed content
    'sphinx_design',            # Adds design elements and utilities
    'sphinxcontrib.mermaid',    # Enables Mermaid diagrams
]

html_baseurl = "https://gatenet.readthedocs.io/en/latest/"

# -- SEO and OpenGraph metadata --
ogp_site_url = html_baseurl
ogp_description_length = 200
ogp_image = "https://gatenet.readthedocs.io/en/latest/_static/logo.png"
ogp_type = "website"
ogp_custom_meta_tags = [
    '<meta name="keywords" content="python, networking, diagnostics, microservices, async, gatenet, sockets, http, tcp, udp, service discovery, bandwidth, ping, traceroute, dns, geoip, open source">',
    '<meta name="author" content="MJ Anglin">',
    '<meta name="robots" content="index, follow">',
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
# Ensure htmlcov and coverage_html are included in the built docs if present
_static_htmlcov = os.path.join(os.path.dirname(__file__), '_static', 'htmlcov')
_coverage_html = os.path.join(os.path.dirname(__file__), 'coverage_html')
html_static_path = ['_static']
if os.path.exists(_static_htmlcov):
    html_static_path.append('_static/htmlcov')
if os.path.exists(_coverage_html):
    html_static_path.append('coverage_html')

# Remove htmlcov and coverage_html from exclude_patterns if present
exclude_patterns = [p for p in exclude_patterns if 'htmlcov' not in p and 'coverage_html' not in p]




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
def run_coverage_summary(_):
    """Generate coverage_summary.rst from coverage.xml before docs build."""
    import subprocess
    import pathlib
    docs_dir = pathlib.Path(__file__).parent
    script = docs_dir / "gen_coverage_table.py"
    if script.exists():
        try:
            subprocess.run([sys.executable, str(script)], check=True)
        except Exception as e:
            print(f"[sphinx] Could not generate coverage summary: {e}")

def setup(app):
    # Add as many CSS files as you want here (must be in _static/)
    app.add_css_file('style.css')
    # app.add_css_file('animations.css')
    # Add JS and manifest as before
    app.add_js_file('site.webmanifest', type='application/manifest+json')
    app.add_js_file('network-footer.js')
    app.connect('builder-inited', run_coverage_summary)

# Example: To use a custom template, add HTML files to _templates/ and reference them in your .rst files.

# Example: To change autodoc member order, you can add this to autodoc_default_options:
# 'member-order': 'bysource',

