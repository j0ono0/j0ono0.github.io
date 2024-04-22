from pathlib import Path
from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)
import markdown
from utilities import copy_dir
from settings import *

# Ensure paths exist
BUILD_PATH.mkdir(parents=True, exist_ok=True)

#  used for formatting html_tag.jinja
void_html_tags = [
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
]


# Jinja2 environment setup
templates = Environment(
    loader=FileSystemLoader(TEMPLATE_DIRS),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)

#### copy static assets from template themes to build dir ##############################
tplt_dirs = [d for d in TEMPLATE_PATH.iterdir() if d.is_dir()]
for dir in tplt_dirs:
    dst = STATIC_ROOT / dir.name
    src = Path(dir, "static")
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
        html = {"content": md.convert(f.read())}
        meta = {k: ", ".join(v) for (k, v) in md.Meta.items()}
        return {**html, **meta}


#### Common components ######################################

site_nav = [
    {"text": "home", "slug": "index.html"},
    {"text": "blocks", "slug": "3-section-blocks.html"},
    {"text": "ideas", "slug": "ideas.html"},
    {"text": "decisions", "slug": "decisions.html"},
]


#####################################################################
##  Gallery content ####################################

gallery_img_folder = CONTENT_PATH / "gallery" / "media" / "thumbnails"
gallery_ctx = {
    "title": "Studio photography",
    "images": [
        MEDIA_ROOT / "gallery" / "thumbnails" / src.name
        for src in gallery_img_folder.iterdir()
        if src.is_file()
    ],
}


### assemble templates (optional for neater code) #########################
section = templates.get_template("minima/section.jinja")
gallery = templates.get_template("gallery/thumbnail_gallery.jinja")
meta = templates.get_template("foundation/meta.jinja")
analytics = templates.get_template("foundation/analytics.jinja")
html_tag = templates.get_template("foundation/html_tag.jinja")
link = templates.get_template("foundation/link.jinja")
### assemble pages #########################
pages = [
    {
        "template": templates.get_template("minima/minima.jinja"),
        "slug": "index.html",
        "doc_title": "Genie-rator",
        "nav": site_nav,
        "head": [
            (meta, {"author": "j0ono0"}),
            (meta, {"description": "A site generator made with Python."}),
            (link, {"rel": "stylesheet", "href": "assets/gallery/gallery.css"}),
        ],
        "main": [
            (section, (parse_md_file(Path("content", "intro.md")))),
            (gallery, gallery_ctx),
            (section, (parse_md_file(Path("content", "ideas.md")))),
        ],
        "footer": [],
    },
    {
        "template": templates.get_template("minima/minima.jinja"),
        "slug": "3-section-blocks.html",
        "doc_title": "Content collated into in blocks",
        "nav": site_nav,
        "head": [
            (meta, {"author": "j0ono0"}),
            (meta, {"description": "3 blocks of content assembled into a single page"}),
            (analytics, {}),
        ],
        "main": [
            (section, (parse_md_file(Path("content", "block_01.md")))),
            (section, (parse_md_file(Path("content", "block_02.md")))),
            (section, (parse_md_file(Path("content", "block_03.md")))),
        ],
    },
    {
        "template": templates.get_template("minima/minima.jinja"),
        "slug": "ideas.html",
        "doc_title": "Ideas for Genie-rator",
        "nav": site_nav,
        "head": [
            (meta, {"author": "j0ono0"}),
            (meta, {"description": "Some ideas on my generator"}),
            (analytics, {}),
        ],
        "main": [
            (section, (parse_md_file(Path("content", "ideas.md")))),
        ],
    },
    {
        "template": templates.get_template("minima/minima.jinja"),
        "slug": "decisions.html",
        "doc_title": "Decisions for Genie-rator",
        "nav": site_nav,
        "head": [
            (meta, {"name": "author", "content": "j0ono0"}),
            (meta, {"name": "description", "content": "Some ideas on my generator"}),
            (analytics, {}),
            (
                html_tag,
                {"tag": "title", "content": "My page specific title"},
            ),
            (
                html_tag,
                {"tag": "meta", "attributes": {"author": "j0ono0"}},
            ),
        ],
        "main": [
            (section, (parse_md_file(Path("content", "decisions.md")))),
        ],
    },
]

for page in pages:
    with open(BUILD_PATH / page["slug"], "w") as f:
        # void tag list referenced in htnml_tag.jinja
        page["_helpers"] = {"void_tags": void_html_tags}
        f.write(page["template"].render(page))

print("\nGenie generation complete\n")
