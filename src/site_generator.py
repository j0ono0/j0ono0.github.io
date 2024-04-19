from pathlib import Path
import os
from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)
import markdown
from utilities import copy_dir


BUILD_PATH = Path("../")
COMPONENT_PATH = Path("./components")
TEMPLATE_PATH = Path("./templates")
CONTENT_PATH = Path("./content")

# Ensure paths exist
BUILD_PATH.mkdir(parents=True, exist_ok=True)


tplt_dirs = ["templates", "components"]
templates = Environment(
    loader=FileSystemLoader(tplt_dirs),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)


#### copy assets from template themes to build dir #######################################
theme_list = [d for d in TEMPLATE_PATH.iterdir() if d.is_dir()]
for dir in theme_list:
    dst = BUILD_PATH / "assets" / dir.name
    src = Path(dir, "assets")
    if src.is_dir():
        copy_dir(src, dst)

#### copy media from content to build dir #######################################
content_list = [d for d in CONTENT_PATH.iterdir() if d.is_dir()]
for dir in content_list:
    dst = BUILD_PATH / "media" / dir.name
    src = Path(dir, "media")
    if src.is_dir():
        copy_dir(src, dst)


def parse_md_file(path):
    md = markdown.Markdown(extensions=["meta"])
    with open(path) as f:
        html = md.convert(f.read())
        meta = {key: ", ".join(val) for (key, val) in md.Meta.items()}
    return (html, meta)


#### build some common components ######################################
analytics_html = templates.get_template("analytics.jinja").render()

navdata = {
    "class": "sitenav",
    "items": [
        {"text": "home", "slug": "index.html"},
        {"text": "blocks", "slug": "3-section-blocks.html"},
    ],
}

sitenav_tplt = templates.get_template("nav.jinja")


### build page #########################

# page template
page_tplt = templates.get_template("minima/minima.jinja")
context = {
    "slug": "index.html",
    "doc_title": "Genie-rator",
    "head": [analytics_html],
    "body": [],
    "navdata": navdata,
}


# extra content for page head (some in minima template already!)
context["head"].append(
    templates.get_template("html_meta.jinja").render(
        meta={
            "author": "j0ono0",
            "description": "A static site generator experiment using Python.",
        }
    )
)

# content for page body

section_tplt = templates.get_template("minima/section.jinja")
for mdfile in ["intro.md", "ideas.md"]:
    md_html, md_meta = parse_md_file(Path("content", mdfile))
    context["body"].append(section_tplt.render(content=md_html, **md_meta))

# Render template with context
with open(BUILD_PATH / "index.html", "w") as f:
    f.write(page_tplt.render(context))


########################################################################

# Build another page, see if some patterns appear?
page_tplt = templates.get_template("minima/minima.jinja")
context = {
    "slug": "3-section-blocks.html",
    "doc_title": "3 content blocks",
    "head": [analytics_html],
    "body": [],
    "navdata": navdata,
}

# Add head content
context["head"].append(
    templates.get_template("html_meta.jinja").render(
        meta={
            "author": "j0ono0",
            "description": "3 content blocks assembled with a static site generator.",
        }
    )
)

# Add body content
for mdfile in ["block_01.md", "block_02.md", "block_03.md"]:
    html, meta = parse_md_file(Path("content", mdfile))
    context = {**context, **meta}
    context["body"].append(html)

# render content to final layout and save as html file
with open(BUILD_PATH / "3-section-blocks.html", "w") as f:
    f.write(page_tplt.render(context))

print("\nGenie generation complete\n")
