<div>
  <h3 align="center"><img src="https://raw.githubusercontent.com/gaetanlhf/franceactu/main/themes/franceactu/static/img/favicon.png" width="100"/><br>franceactu</h3>
</div>

[![Deploy to GitHub Pages](https://github.com/gaetanlhf/franceactu/actions/workflows/github-pages.yml/badge.svg)](https://github.com/gaetanlhf/franceactu/actions/workflows/github-pages.yml)

# Introduction
franceactu is the aggregator of French public service news websites.  
It retrieves, thanks to RSS feeds, news from different sources and organizing them into different categories.  
The regeneration of the static website is done periodically, in order to have always the freshest news available (maximum twelve hours after publication).  
franceactu is designed to be easy to use.  

**NOTE: franceactu is only available in French.**

# Build
Periodically and on push/pull request via [Github Actions](https://github.com/gaetanlhf/franceactu/blob/main/.github/workflows/github-pages.yml) or manually:

- Install dependencies: ```pip install -r requirements.txt```

- Generate static website: ```python update.py --static ./build```

# Credits
franceactu is built around a modified version of [MakeMake](https://framagit.org/makemake/makemake), a dwarf Planet for your feeds.

***

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see http://www.gnu.org/licenses/.
