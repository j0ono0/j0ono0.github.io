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

# Ensure paths exist
BUILD_PATH.mkdir(parents=True, exist_ok=True)


tplt_dirs = ["templates", "components"]
templates = Environment(
    loader=FileSystemLoader(tplt_dirs),
    autoescape=select_autoescape(),
)


#### copy assets from components to build dir #######################################
component_list = [d for d in COMPONENT_PATH.iterdir() if d.is_dir()]
for dir in component_list:
    dst = BUILD_PATH / "assets" / dir.name
    src = Path(dir, "assets")
    if src.is_dir():
        copy_dir(src, dst)


# Build common components use by article and page templates: eg. site nav ####################################################################
site_nav = []
nav_list = ["content/index.md", "content/page01.md", "content/article_01.md"]
for link in nav_list:
    md = markdown.Markdown(extensions=["meta"])
    nav_item = {}
    with open(link) as f:
        md.convert(f.read())
    for key in md.Meta:
        nav_item[key] = ", ".join(md.Meta[key])
    site_nav.append(nav_item)


#### build articles ####################################################################

# TODO: allow files to be built into subfolders

article_list = ["content/article_01.md"]
for article in article_list:
    template = templates.get_template("article/article_full.jinja")
    md = markdown.Markdown(extensions=["meta"])

    with open(article) as f:
        content = md.convert(f.read())

    context = {"content": content, "site_nav": site_nav}
    for key in md.Meta:
        context[key] = ", ".join(md.Meta[key])

    filepath = BUILD_PATH / f'{context["slug"]}.html'
    with open(filepath, "w") as f:
        f.write(template.render(context))


########build pages ################################################################

page_list = ["content/index.md", "content/page01.md"]
# Build the pages
for page in page_list:

    template = templates.get_template("base.jinja")
    md = markdown.Markdown(extensions=["meta"])

    with open(page) as f:
        content = md.convert(f.read())

    context = {"content": content, "site_nav": site_nav}
    for key in md.Meta:
        context[key] = ", ".join(md.Meta[key])

    filepath = BUILD_PATH / f'{context["slug"]}.html'
    with open(filepath, "w") as f:
        f.write(template.render(context))

print("site generated")
