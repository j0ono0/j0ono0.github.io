title:   Site-Genie-rator, Introduction
authors: j0ono0
created:    2024-4-16
updated:   2024-4-17

## Python site generator is go

Built using Python, Jinja2, and Markdown. This page has been generated locally and pushed to github.

The biggest question in my mind is how to structure content, templates, and themes. Currently I'm thinking 'prose' is stored as markdown docs and 'configuration' data (page urls, navigation menus, tags, etc) stored as python lists and dictionaries. This content could then be applied to templates that result in chunks of HTML. The HTML chunks can, in turn, be applied to further templates until a final page is complete. 

I'm up to version 2 of how I might structure these things. Generally it's looking really promising with a balance between flexibility, neat content filing, easy authoring, and consistent styling.
