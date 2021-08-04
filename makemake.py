# encoding: utf-8
"""
MakeMake - a dwarf planet for your feeds.

Webserver module.
"""

from datetime import datetime
import json
from math import ceil
import os
import re
from time import localtime, mktime, strftime

from flask import Flask, g, make_response, redirect, render_template, request, url_for
from slugify import slugify
import yaml


MAKEMAKE_VERSION = "v0.1"


# Creating application
application = Flask(__name__, template_folder=".")
application.config.from_object("config")
try:
    application.config.from_object(f"config-{application.config['ENV']}")
except Exception:
    print(f"Starting without configuration file config-{application.config['ENV']}.py")

application.jinja_env.trim_blocks = application.config["JINJA_ENV"]["TRIM_BLOCKS"]
application.jinja_env.lstrip_blocks = application.config["JINJA_ENV"]["LSTRIP_BLOCKS"]


def pretty_date(time):
    now = datetime.now()
    diff = now - datetime.fromtimestamp(time)
    second_diff = diff.seconds
    day_diff = diff.days
    if day_diff < 0:
        return ""
    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 61:
            return f"{second_diff} seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3601:
            return f"{int(second_diff/60)} minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86401:
            return f"{int(second_diff/3600)} hours ago"
    if day_diff < 2:
        return "yesterday"
    if day_diff < 30:
        return f"{day_diff} days ago"
    if day_diff < 60:
        return "1 month ago"
    if day_diff < 365:
        return f"{int(day_diff/30)} months ago"
    if day_diff < 730:
        return "1 year ago"
    return f"{int(day_diff/365)} years ago"


def filtering_entry(entry):
    entry_filter = request.args.get("filter")
    if entry_filter is None:
        return True
    if (
        entry_filter in entry["source"]["name"].lower()
        or entry_filter in entry["title"].lower()
        or entry_filter in entry["content"].lower()
    ):
        return True
    return False

@application.before_request
def set_folders():
    # Theming
    template_folder = os.path.join(
        os.getcwd(), f"themes/{application.config['MAKEMAKE_THEME']}"
    )
    static_folder = os.path.join(os.getcwd(), f"{template_folder}/static")
    application.template_folder = template_folder
    application.static_folder = static_folder


@application.template_filter("date")
def date_filter(date, date_format):
    return strftime(date_format, date)


def load_entries():
    # MakeMake specific values
    application.config["MAKEMAKE_NAME"] = "MakeMake The Dwarf Planet"
    application.config["MAKEMAKE_VERSION"] = MAKEMAKE_VERSION
    # MakeMake default config
    application.config["MAKEMAKE_TITLE"] = application.config.get(
        "MAKEMAKE_TITLE", "MakeMake"
    )
    application.config["MAKEMAKE_LINK"] = application.config.get(
        "MAKEMAKE_LINK", "http://localhost:5000/"
    )
    application.config["MAKEMAKE_LOGO"] = application.config.get(
        "MAKEMAKE_LOGO",
        "https://framagit.org/makemake/makemake/-/raw/master/makemake-logo.png",
    )
    application.config["MAKEMAKE_FAVICON"] = application.config.get(
        "MAKEMAKE_FAVICON", application.config["MAKEMAKE_LOGO"]
    )
    application.config["MAKEMAKE_DESCRIPTION"] = application.config.get(
        "MAKEMAKE_DESCRIPTION", "Description"
    )
    application.config["MAKEMAKE_DISCOVER_THEMES"] = application.config.get(
        "MAKEMAKE_DISCOVER_THEMES", False
    )
    application.config["MAKEMAKE_THEME"] = application.config.get(
        "MAKEMAKE_THEME", "basic"
    )
    application.config["MAKEMAKE_MISC"] = application.config.get("MAKEMAKE_MISC", {})
    application.config["MAKEMAKE_PAGINATION"] = application.config.get(
        "MAKEMAKE_PAGINATION", False
    )
    application.config["MAKEMAKE_PAGINATION_SIZE"] = application.config.get(
        "MAKEMAKE_PAGINATION_SIZE", 10
    )
    application.config["MAKEMAKE_DISPLAY_SOURCES"] = application.config.get(
        "MAKEMAKE_DISPLAY_SOURCES", True
    )
    application.config["MAKEMAKE_FEEDS"] = application.config.get(
        "MAKEMAKE_FEEDS", ["RSS", "ATOM"]
    )
    # MakeMake variables for templates
    mm = {
        "title": application.config["MAKEMAKE_TITLE"],
        "link": application.config["MAKEMAKE_LINK"],
        "logo": application.config["MAKEMAKE_LOGO"],
        "favicon": application.config["MAKEMAKE_FAVICON"],
        "description": application.config["MAKEMAKE_DESCRIPTION"],
        "last_update": "",
        "theme": application.config["MAKEMAKE_THEME"],
        "misc": application.config["MAKEMAKE_MISC"],
        "pagination": application.config["MAKEMAKE_PAGINATION"],
        "pagination_size": application.config["MAKEMAKE_PAGINATION_SIZE"],
        "themes": [],
        "sources": [],
        "entries": [],
        "makemake": {
            "version": MAKEMAKE_VERSION,
            "source": "https://framagit.org/Mindiell/makemake",
            "author": "Mindiell",
            "licence": "AGPLV3+",
        },
    }

    # Loading last update
    with open(os.path.join(os.getcwd(), "datas/mm.json")) as f:
        last_update = mktime(tuple(json.load(f)["last_update"]))
        mm["last_update_iso"] = datetime.fromtimestamp(last_update).isoformat()
        if len(mm["last_update_iso"]) < 20:
            mm["last_update_iso"] += "Z"
        mm["last_update"] = localtime(last_update)

    # Loading themes
    if application.config["MAKEMAKE_DISCOVER_THEMES"]:
        # Discover themes
        application.config["MAKEMAKE_THEMES"] = []
        for theme in os.listdir(os.path.join(os.getcwd(), "themes")):
            if os.path.isdir(os.path.join(os.getcwd(), "themes", theme)):
                # Theme should have at least an index.html and an info.yml file
                if "index.html" not in os.listdir(
                    os.path.join(os.getcwd(), "themes", theme)
                ):
                    continue
                if "info.yml" not in os.listdir(
                    os.path.join(os.getcwd(), "themes", theme)
                ):
                    continue
                application.config["MAKEMAKE_THEMES"].append(theme)
    for name in application.config["MAKEMAKE_THEMES"]:
        with open(
            os.path.join(os.getcwd(), f"themes/{name}/info.yml"), encoding="utf-8"
        ) as f:
            mm["themes"].append(yaml.load(f, Loader=yaml.SafeLoader))

    # Loading sources
    with open(os.path.join(os.getcwd(), "datas/sources.yml"), encoding="utf-8") as f:
        mm["sources"] = yaml.load(f, Loader=yaml.SafeLoader)

    # Loading feeds
    for source in mm["sources"]:
        feed_file = slugify(source["name"])
        feed_path = os.path.join(os.getcwd(), f"datas/feed/{feed_file}.json")
        if not os.path.exists(feed_path):
            continue
        with open(feed_path) as f:
            entries = json.load(f)
        # Add source information
        for entry in entries:
            entry["source"] = source
        mm["entries"].extend(entries)
    for entry in mm["entries"]:
        entry_date = mktime(tuple(entry["date"]))
        # Date in ISO 8601 (RFC 3339) format
        entry["date_iso"] = datetime.fromtimestamp(entry_date).isoformat()
        if len(entry["date_iso"]) < 20:
            entry["date_iso"] += "Z"
        # Convert date to time.struct_time
        entry["date"] = localtime(entry_date)
        # Compute time elapsed for humans
        entry["time_elapsed"] = pretty_date(int(mktime(tuple(entry["date"]))))
        # Expurge some tags from content
        for tag in ("</?html>","</?body>"):
            entry["content"] = re.sub(tag, "", entry["content"])
    # Sorting entries
    mm["entries"].sort(key=lambda x: x["date"], reverse=True)
    return mm


@application.route("/")
@application.route("/page_<int:page>.html")
def home(page=1):
    # Loading entries
    mm = load_entries()

    # Pagination
    if application.config["MAKEMAKE_PAGINATION"]:
        pages = ceil(
            len(mm["entries"]) / application.config["MAKEMAKE_PAGINATION_SIZE"]
        )
        if page < 1:
            page = 1
        elif page > pages:
            page = pages
        offset = application.config["MAKEMAKE_PAGINATION_SIZE"] * (page - 1)
        mm["pagination_offset"] = offset
        mm["pagination_page"] = page
        mm["pagination_pages"] = pages
        # Limiting entries
        mm["entries"] = mm["entries"][
            offset : offset + application.config["MAKEMAKE_PAGINATION_SIZE"]
        ]
    else:
        mm["pagination_offset"] = 0
        mm["pagination_page"] = 1
        mm["pagination_pages"] = 1

    # filtering entries
    mm["entries"] = filter(filtering_entry, mm["entries"])

    return render_template("index.html", mm=mm)


@application.route("/rss20.xml")
def rss20():
    # Loading entries
    mm = load_entries()
    response = make_response(render_template("rss20.xml", mm=mm))
    response.headers["Content-Type"] = "text/xml"

    return response


@application.route("/atom.xml")
def atom():
    # Loading entries
    mm = load_entries()
    response = make_response(render_template("atom.xml", mm=mm))
    response.headers["Content-Type"] = "text/xml"

    return response
