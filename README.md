# mkdocs-markdown-in-template-plugin

MkDocs plugin that allows to use Markdown in your theme’s Jinja2 templates

## Installation

```bash
python3 -m pip install git+https://github.com/twardoch/mkdocs-markdown-in-template-plugin
```

## Configuration

In `mkdocs.yaml` (as early as possible in the list of plugins):

```yaml
plugins:
  - markdown-in-template
```

## Usage

In any HTML template partial, you can now include Markdown enclosed in `{% md %}` and `{% mdend %}`:

```html
<article>
{% md %}
# Heading

Regular and **bold** text
{% mdend %}
</article>
```

Note: The plugin will remove any indentation equal to the indentation of the first line of the Markdown.

