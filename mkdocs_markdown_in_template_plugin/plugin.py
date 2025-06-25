import textwrap
import typing as t

import markdown
from jinja2 import Environment
from jinja2.ext import Extension
from jinja2.nodes import CallBlock, Node
from jinja2.parser import Parser
from mkdocs.config import Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files


class MarkdownJinjaExtension(Extension):
    tags = {"md"}

    def __init__(self, env: Environment) -> None:
        super().__init__(env)
        self.markdowner = markdown.Markdown(
            extensions=env.globals.get(
                "mkdocs_markdown_in_template_plugin_markdown_extensions", []
            ),
            extension_configs=env.globals.get(
                "mkdocs_markdown_in_template_plugin_mdx_configs", {}
            ),
        )
        env.extend(markdowner=self.markdowner)

    def parse(self, parser: Parser) -> t.Union[Node, t.List[Node]]:
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(("name:mdend",), drop_needle=True)
        return CallBlock(self.call_method("_render_markdown"), [], [], body).set_lineno(
            lineno
        )

    def _render_markdown(self, caller: t.Callable) -> str:
        text = self._dedent(caller())
        return self.markdowner.convert(text)

    def _dedent(self, text: str) -> str:
        return textwrap.dedent(text.strip("\n"))


class MarkdownInTemplatePlugin(BasePlugin):
    config_scheme = ()

    def __init__(self) -> None:
        self.enabled = True
        self.dirs = []

    def on_env(self, env: Environment, config: Config, files: Files) -> Environment:
        env.globals["mkdocs_markdown_in_template_plugin_markdown_extensions"] = (
            config.get("markdown_extensions", [])
        )
        env.globals["mkdocs_markdown_in_template_plugin_mdx_configs"] = config.get(
            "mdx_configs", {}
        )
        env.add_extension(MarkdownJinjaExtension)
        return env
