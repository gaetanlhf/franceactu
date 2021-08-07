# encoding: utf-8
"""
MakeMake - a dwarf planet for your feeds.

This module updates feeds from sources.
"""

import argparse
from datetime import datetime, timedelta
from importlib import import_module
import json
import os
from time import localtime, mktime, strftime
import warnings


from bs4 import BeautifulSoup
import feedparser
from flask_frozen import Freezer
from slugify import slugify
import yaml


from makemake import application


# Argparse
parser = argparse.ArgumentParser(description="Update feeds from datas/sources.yml")
parser.add_argument("-v", "--verbose", action="store_true", help="Update will tell you much more.")
parser.add_argument("--static", help="Update normally then generate a static website.")
args = parser.parse_args()

# Disable BeautifulSoup specific warning
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

# Loading configuration
if args.verbose:
    print("Loading configuration")
dft_config = import_module("config")
config = {}
for variable in dft_config.__dir__():
    if variable[:2] != "__":
        config[variable] = getattr(dft_config, variable, "")
config["ENV"] = os.environ.get("FLASK_ENV", "production")
try:
    # Loading environment config
    env_config = import_module(f"config-{config['ENV']}")
    for variable in env_config.__dir__():
        if variable[:2] != "__":
            config[variable] = getattr(env_config, variable, "")
except Exception as e:
    if args.verbose:
        print(f"Starting without specific configuration file config-{config['ENV']}.py")

# Loading sources
sources = []
sources_path = os.path.join(os.getcwd(), "datas/sources.yml")
if not os.path.exists(sources_path):
    print("Sources file 'datas/sources.yml' is not existing.")
    print("  You can create one from the default one by copying it and editing it:")
    print("  cp datas/sources.default.yml datas/sources.yml")
    print("  vi datas/sources.yml")
    exit(-1)
with open(sources_path, encoding="utf-8") as f:
    sources = yaml.load(f, Loader=yaml.SafeLoader)

# Creating directories if necessary
if args.verbose:
    print("Creating directories if necessary")
os.makedirs(os.path.join(os.getcwd(), "datas/feed/"), exist_ok=True)

# Updating feeds
if args.verbose:
    print("Updating feeds")
for source in sources:
    if args.verbose:
        print(f" - {source['name']}")
    feed = feedparser.parse(source["feed"])

    # Getting feed informations
    feed_file = slugify(source["name"])
    feed_path = os.path.join(os.getcwd(), f"datas/feed/{feed_file}.json")

    # Loading known entries
    entries = []
    try:
        with open(feed_path) as f:
            entries = json.load(f)
        for entry in entries:
            # Convert date to time.struct_time
            entry["date"] = localtime(mktime(tuple(entry["date"])))
    except FileNotFoundError:
        # Creating empty file
        with open(feed_path, "w") as f:
            json.dump(entries, f)
    if args.verbose:
        print(f"     {len(entries)} old entries loaded")

    # Updating entries
    if args.verbose:
        print(f"     {len(feed.entries)} entries found")
    for entry in feed.entries:
        new_entry = {}
        if "title_detail" in entry:
            new_entry["title"] = entry["title_detail"]["value"]
        else:
            new_entry["title"] = entry["title"]
        new_entry["date"] = entry.get("published_parsed", entry["updated_parsed"])
        new_entry["link"] = entry["link"]
        if "summary_detail" in entry:
            if entry["summary_detail"].get("type", "") == "text/plain":
                new_entry["summary"] = "<br />".join(entry["summary_detail"]["value"].split("\n"))
            elif entry["summary_detail"].get("type", "") == "text/html":
                soup = BeautifulSoup(entry["summary_detail"]["value"], "html.parser")
                [script.extract() for script in soup.findAll("script")]
                new_entry["summary"] = str(soup)
            else:
                new_entry["summary"] = entry["summary_detail"]["value"]
        elif "summary" in entry:
            new_entry["summary"] = entry["summary"]
        new_entry["content"] = ""
        if "content" in entry:
            for content in entry["content"]:
                if content.get("type", "") == "text/plain":
                    new_entry["content"] = "<br />".join(content["value"].split("\n"))
                elif content.get("type", "") == "text/html":
                    soup = BeautifulSoup(content["value"], "html.parser")
                    [script.extract() for script in soup.findAll("script")]
                    new_entry["content"] = str(soup)
                else:
                    new_entry["content"] = content["value"]
        if new_entry["content"] == "" and "summary" in new_entry and new_entry["summary"] != "":
            new_entry["content"] = new_entry["summary"]

        # Filtering entries
        filtered = True
        for source_filter in source.get("filters", []):
            if "link" in source_filter:
                if source_filter["link"].lower() not in new_entry["link"].lower():
                    filtered = False
            if "title" in source_filter:
                if source_filter["title"].lower() not in new_entry["title"].lower():
                    filtered = False
            if "content" in source_filter:
                if source_filter["content"].lower() not in new_entry["content"].lower():
                    filtered = False

        if filtered:
            # Is this entry unknown ?
            known = False
            for idx, known_entry in enumerate(entries):
                if known_entry["link"] == new_entry["link"]:
                    known = True
                    # Update entry
                    entries[idx] = new_entry
            if not known:
                # New entry
                entries.append(new_entry)

    # Deleting old entries
    if config.get("MAKEMAKE_DELETE_OLDER", None) is not None:
        limit = datetime.now() - timedelta(days=config["MAKEMAKE_DELETE_OLDER"])
        entries = list(filter(lambda x: x["date"]>=limit.timetuple(), entries))

    if args.verbose:
        print(f"     {len(entries)} entries stored")

    # Sorting entries
    entries.sort(key=lambda x: x["date"], reverse=True)

    # Saving entries
    with open(feed_path, "w") as f:
        json.dump(entries, f, indent=2)

# Saving last update date
if args.verbose:
    print(f"Last update date {strftime('%Y-%m-%d %H:%M:%S', localtime())}")
with open(os.path.join(os.getcwd(), "datas/mm.json"), "w") as f:
    json.dump({"last_update": localtime()}, f)


# Generating website if asked
if args.static is not None:
    if args.verbose:
        print("Generating static files")
    else:
        application.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True
    # Generating website
    application.config["FREEZER_DESTINATION"] = args.static
    Freezer(application).freeze()

