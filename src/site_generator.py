from pathlib import Path
import os
from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)
import markdown
from utilities import copy_dir
import content.meta as meta
import copy

BUILD_PATH = Path("../")
COMPONENT_PATH = Path("./components")
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


#### copy assets from components to build dir #######################################
component_list = [d for d in COMPONENT_PATH.iterdir() if d.is_dir()]
for dir in component_list:
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


########build pages ################################################################


def generate(template, page):

    md = markdown.Markdown(extensions=["meta"])
    ctx = copy.copy(page)
    content_src = Path("content", page["content"])
    with open(content_src) as f:
        ctx["content"] = md.convert(f.read())
    ctx["site_nav"] = meta.site_nav

    for key in md.Meta:
        ctx[key] = ", ".join(md.Meta[key])

    filepath = BUILD_PATH / ctx["slug"]
    with open(filepath, "w") as f:
        f.write(template.render(ctx))


# Generate the pages
page_tplt = templates.get_template("page/page_template.jinja")
for page in meta.pages:
    generate(page_tplt, page)

# Generate the articles
article_tplt = templates.get_template("article/full.jinja")
for page in meta.articles:
    generate(article_tplt, page)


########################################################################
########################################################################
### test #####################################################################
article_list_tplt = templates.get_template("/article/link_list.jinja")
article_list_html = article_list_tplt.render({"items": meta.articles})
print(article_list_html)

########################################################################
########################################################################


print("Genie generation complete")
