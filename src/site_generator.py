from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown
from pathlib import Path


BUILD_PATH = Path("../")
COMPONENT_PATH = Path("templates/temp_components")

# Ensure paths exist
COMPONENT_PATH.mkdir(parents=True, exist_ok=True)
BUILD_PATH.mkdir(parents=True, exist_ok=True)


tplt_env = Environment(
    loader=FileSystemLoader("templates"), autoescape=select_autoescape()
)

template = tplt_env.get_template("base.jinja")

page_list = ["content/index.md", "content/page01.md"]


# Build site navigation content
site_nav = []
for page in page_list:
    md = markdown.Markdown(extensions=["meta"])
    nav_item = {}
    with open(page) as f:
        md.convert(f.read())
    for key in md.Meta:
        nav_item[key] = ", ".join(md.Meta[key])
    site_nav.append(nav_item)


# Build the pages
for page in page_list:

    template = tplt_env.get_template("base.jinja")
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
