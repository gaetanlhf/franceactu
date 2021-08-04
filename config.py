# encoding: utf-8

SECRET_KEY = "This is NOT a secret key"

JINJA_ENV = {
    "TRIM_BLOCKS": True,
    "LSTRIP_BLOCKS": True,
}

# Planet website configuration
# Title
MAKEMAKE_TITLE = "MakeMake The Dwarf Planet"
# Link to itself
MAKEMAKE_LINK = "http://localhost:5000/"
# Logo
MAKEMAKE_LOGO = "makemake.png"
# Favicon - if None, logo will be used in place
MAKEMAKE_FAVICON = None
# Description
MAKEMAKE_DESCRIPTION = "MakeMake The Dwarf Planet is a feed agregator."


# Themes
# Theme to use; should be present in themes/ folder
MAKEMAKE_THEME = "basic"
# Not used for now, list all themes availables in themes/ folder
MAKEMAKE_DISCOVER_THEMES = True
# Not used for now, default list of themes
MAKEMAKE_THEMES = ["basic"]


# Pagination
# Use pagination
MAKEMAKE_PAGINATION = False
# If pagination used, how many articles to display
MAKEMAKE_PAGINATION_SIZE = 10

# Boolean used in themes to display (or not) sources used
MAKEMAKE_DISPLAY_SOURCES = True
# List of Planet feeds to generate (actualy, only RSS and ATOM are available)
MAKEMAKE_FEEDS = ["RSS", "ATOM"]
# Deleting old articles (in days)
MAKEMAKE_DELETE_OLDER = None

# Miscellaneous information that can be used by themes, you can specify whatever you
# want in there but it have to be used by the theme
MAKEMAKE_MISC = {
    # Those values are specified only for testing purpose
    "presentation": {
        "title": "MakeMake",
        "text": """
        <p>MakeMake is a <a href="https://en.wikipedia.org/wiki/Planet_(software)" alt="planet_software from wikipedia">planet software</a> making it simple to agregate multiple feeds.</p>

        <p>You can contribute to MakeMake by opening issues on <a href="https://framagit.org/makemake/makemake/-/issues">our issue tracker</a> or contacting us via IRC.</p>""",
    },
    "related": [
        {
            "name": "MakeMake Source code",
            "link": "https://framagit.org/makemake/makemake",
        },
        {
            "name": "IRC Contact",
            "link": "https://webchat.freenode.net?##makemake",
        },
    ],
}
