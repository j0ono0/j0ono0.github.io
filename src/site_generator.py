from pathlib import Path
from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)
import markdown
from utilities import copy_dir

BUILD_PATH = Path("../")
TEMPLATE_PATH = Path("./templates")
CONTENT_PATH = Path("./content")

# Ensure paths exist
BUILD_PATH.mkdir(parents=True, exist_ok=True)

# Jinja2 environment setup
tplt_dirs = [TEMPLATE_PATH]
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


#### Common components ######################################

site_nav = [
    {"text": "home", "slug": "index.html"},
    {"text": "blocks", "slug": "3-section-blocks.html"},
    {"text": "ideas", "slug": "ideas.html"},
    {"text": "decisions", "slug": "decisions.html"},
]

### assemble pages #########################

pages = [
    {
        "template": templates.get_template("minima/minima.jinja"),
        "slug": "index.html",
        "doc_title": "Genie-rator",
        "nav": site_nav,
        "head": [
            ("metatag", ("author", "j0ono0")),
            ("metatag", ("description", "A genie that generates static sites")),
            ("google_analytics", ()),
        ],
        "main": [
            ("md_section", (parse_md_file(Path("content", "intro.md")))),
            ("md_section", (parse_md_file(Path("content", "ideas.md")))),
        ],
        "footer": [],
    },
    {
        "template": templates.get_template("minima/minima.jinja"),
        "slug": "3-section-blocks.html",
        "doc_title": "Content collated into in blocks",
        "nav": site_nav,
        "head": [
            ("metatag", ("author", "j0ono0")),
            ("metatag", ("description", "3 content blocks assembled together.")),
            ("google_analytics", ()),
        ],
        "main": [
            ("md_section", (parse_md_file(Path("content", "block_01.md")))),
            ("md_section", (parse_md_file(Path("content", "block_02.md")))),
            ("md_section", (parse_md_file(Path("content", "block_03.md")))),
        ],
    },
    {
        "template": templates.get_template("minima/minima.jinja"),
        "slug": "ideas.html",
        "doc_title": "Ideas for Genie-rator",
        "nav": site_nav,
        "head": [
            ("metatag", ("author", "j0ono0")),
            ("metatag", ("description", "Ideas for Python genie-rator.")),
            ("google_analytics", ()),
        ],
        "main": [
            ("md_section", (parse_md_file(Path("content", "ideas.md")))),
        ],
    },
    {
        "template": templates.get_template("minima/minima.jinja"),
        "slug": "decisions.html",
        "doc_title": "Decisions for Genie-rator",
        "nav": site_nav,
        "head": [
            ("metatag", ("author", "j0ono0")),
            ("metatag", ("description", "Decisions for Python genie-rator.")),
            ("google_analytics", ()),
        ],
        "main": [
            ("md_section", (parse_md_file(Path("content", "decisions.md")))),
        ],
    },
]

for page in pages:
    with open(BUILD_PATH / page["slug"], "w") as f:
        f.write(page["template"].render(page))

print("\nGenie generation complete\n")
