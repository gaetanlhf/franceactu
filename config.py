# encoding: utf-8

JINJA_ENV = {
    "TRIM_BLOCKS": True,
    "LSTRIP_BLOCKS": True,
}

# Planet website configuration
# Title
MAKEMAKE_TITLE = "franceactu"
# Logo
MAKEMAKE_LOGO = "img/franceactu.png"
# Favicon - if None, logo will be used in place
MAKEMAKE_FAVICON = "img/favicon.png"
# Description
MAKEMAKE_DESCRIPTION = "MakeMake The Dwarf Planet is a feed agregator."

# Themes
# Theme to use; should be present in themes/ folder
MAKEMAKE_THEME = "franceactu"
# Not used for now, default list of themes
MAKEMAKE_THEMES = ["franceactu"]

# Pagination
# Use pagination
MAKEMAKE_PAGINATION = False
# If pagination used, how many articles to display
MAKEMAKE_PAGINATION_SIZE = 10

# Boolean used in themes to display (or not) sources used
MAKEMAKE_DISPLAY_SOURCES = False
# List of Planet feeds to generate (actualy, only RSS and ATOM are available)
MAKEMAKE_FEEDS = False
# Deleting old articles (in days)
MAKEMAKE_DELETE_OLDER = 0.5