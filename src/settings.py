# Settings for site generator

from pathlib import Path


# Source directories
CONTENT_PATH = Path("./content")
TEMPLATE_PATH = Path("./templates")
TEMPLATE_DIRS = [TEMPLATE_PATH]


# Build directories
BUILD_PATH = Path("../")
STATIC_ROOT = Path("assets")
MEDIA_ROOT = Path("media")
