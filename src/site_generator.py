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


def parse_markdown(template, src):
    md = markdown.Markdown(extensions=["meta"])
    ctx = {"src": src}
    with open(src) as f:
        ctx["content"] = md.convert(f.read())

    for key in md.Meta:
        ctx[key] = ", ".join(md.Meta[key])

    return template.render(ctx)


### build page #########################

# page template
page_tplt = templates.get_template("minima/minima.jinja")

# extra content for page head (some in minima template already!)
head = []
head.append(templates.get_template("analytics.jinja").render())
head.append(
    templates.get_template("html_meta.jinja").render(
        meta={
            "author": "j0ono0",
            "description": "A static site generator experiment using Python.",
        }
    )
)

# content for page body
body = []

section_tplt = templates.get_template("minima/section.jinja")
for mdfile in ["intro.md", "ideas.md"]:
    src_path = Path("content", mdfile)
    body.append(parse_markdown(section_tplt, src_path))

# add collated content to template
page_ctx = {"doc_title": "Genie-rator", "head": head, "body": body}

with open(BUILD_PATH / "index.html", "w") as f:
    f.write(page_tplt.render(page_ctx))

########################################################################


print("\nGenie generation complete\n")
