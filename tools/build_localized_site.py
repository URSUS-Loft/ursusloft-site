"""Extract and build localized HTML without changing the source DOM.

The script uses only Python's standard library.  Keys are page-scoped and
ordinal so translators can edit a JSON file without touching HTML.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "index.html",
    "products/scene-director.html",
    "products/persona-director.html",
    "products/scene-director/guides/index.html",
    "products/scene-director/guides/image-to-image-prompt-workflow.html",
    "products/scene-director/guides/reference-image-order.html",
    "products/scene-director/guides/character-consistency.html",
    "support/index.html",
    "support/scene-director.html",
    "privacy/scene-director.html",
    "legal/scene-director-eula.html",
)
TRANSLATABLE_ATTRS = {"title", "alt", "aria-label"}
META_KEYS = {"description", "og:title", "og:description"}
LOCALE_CODES = {
    "ja": "ja", "zh-cn": "zh-CN", "es": "es", "fr": "fr",
    "pt-br": "pt-BR", "de": "de", "it": "it", "id": "id",
}
SITE_LOCALES = frozenset(("ko",) + tuple(LOCALE_CODES))


def page_id(relative_path: str) -> str:
    return relative_path.removesuffix(".html").replace("/", ".").replace("-", "_")


class TextCatalog(HTMLParser):
    def __init__(self, relative_path: str) -> None:
        super().__init__(convert_charrefs=False)
        self.prefix = page_id(relative_path)
        self.items: dict[str, str] = {}
        self.text_index = 0
        self.attr_index = 0
        self.hidden_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.hidden_depth += 1
        values = dict(attrs)
        for name, value in attrs:
            if name in TRANSLATABLE_ATTRS and value:
                self.attr_index += 1
                self.items[f"{self.prefix}.attr.{name}.{self.attr_index:03d}"] = html.unescape(value)
        if tag == "meta":
            key = values.get("name") or values.get("property")
            value = values.get("content")
            if key in META_KEYS and value:
                self.attr_index += 1
                self.items[f"{self.prefix}.meta.{key.replace(':', '_')}.{self.attr_index:03d}"] = html.unescape(value)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.hidden_depth or not data.strip():
            return
        self.text_index += 1
        self.items[f"{self.prefix}.text.{self.text_index:03d}"] = html.unescape(data.strip())


def catalog(source_root: Path) -> dict[str, str]:
    items: dict[str, str] = {}
    for relative_path in PAGES:
        parser = TextCatalog(relative_path)
        parser.feed((source_root / relative_path).read_text(encoding="utf-8"))
        items.update(parser.items)
    return items


def write_english_json(output: Path) -> int:
    items = catalog(ROOT)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(items)


class LocalizedBuilder(HTMLParser):
    def __init__(self, relative_path: str, translations: dict[str, str]) -> None:
        super().__init__(convert_charrefs=False)
        self.prefix = page_id(relative_path)
        self.translations = translations
        self.output: list[str] = []
        self.text_index = 0
        self.attr_index = 0
        self.hidden_depth = 0

    def _key(self, kind: str, name: str | None, index: int) -> str:
        if kind == "text":
            return f"{self.prefix}.text.{index:03d}"
        if kind == "meta":
            return f"{self.prefix}.meta.{name.replace(':', '_')}.{index:03d}"
        return f"{self.prefix}.attr.{name}.{index:03d}"

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        raw = self.get_starttag_text()
        values = dict(attrs)
        replacements: list[tuple[str, str]] = []
        for name, value in attrs:
            if name in TRANSLATABLE_ATTRS and value:
                self.attr_index += 1
                replacements.append((name, self.translations.get(self._key("attr", name, self.attr_index), value)))
        if tag == "meta":
            name = values.get("name") or values.get("property")
            value = values.get("content")
            if name in META_KEYS and value:
                self.attr_index += 1
                replacements.append(("content", self.translations.get(self._key("meta", name, self.attr_index), value)))
        for name, value in replacements:
            pattern = rf'({re.escape(name)}\s*=\s*)(["\'])(.*?)(\2)'
            raw = re.sub(pattern, lambda m: m.group(1) + m.group(2) + html.escape(value, quote=True) + m.group(4), raw, count=1)
        self.output.append(raw)
        if tag in {"script", "style"}:
            self.hidden_depth += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        self.output.append(f"</{tag}>")
        if tag in {"script", "style"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.hidden_depth or not data.strip():
            self.output.append(data)
            return
        self.text_index += 1
        key = self._key("text", None, self.text_index)
        value = self.translations.get(key, data.strip())
        leading = data[: len(data) - len(data.lstrip())]
        trailing = data[len(data.rstrip()) :]
        self.output.append(leading + html.escape(value, quote=False) + trailing)

    def handle_entityref(self, name: str) -> None:
        self.output.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.output.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        self.output.append(f"<!--{data}-->")

    def handle_decl(self, decl: str) -> None:
        self.output.append(f"<!{decl}>")


def output_relative_path(relative_path: str, locale: str) -> str:
    if relative_path.endswith("character-consistency.html") and locale:
        return relative_path.replace("character-consistency.html", "character-consistency.html")
    return relative_path


def local_path(path: Path, locale: str) -> Path:
    try:
        relative = path.resolve().relative_to(ROOT)
    except ValueError:
        return path
    if relative.parts and relative.parts[0] == "assets":
        return ROOT / relative
    # A language-selector link already identifies its target locale.  Do not
    # nest it below the page currently being generated.
    if relative.parts and relative.parts[0] in SITE_LOCALES:
        return ROOT / relative
    return ROOT / locale / output_relative_path(relative.as_posix(), locale)


def localized_source(source: str, source_path: Path, target_path: Path, locale: str) -> str:
    def rewrite(match: re.Match[str]) -> str:
        name, value = match.group(1), match.group(2)
        if value.startswith(("http:", "https:", "mailto:", "tel:", "data:", "#", "javascript:")):
            return match.group(0)
        parts = urlsplit(value)
        if not parts.path:
            return match.group(0)
        resolved = ROOT / parts.path.lstrip("/") if parts.path.startswith("/") else source_path.parent / parts.path
        # A self-link in the English source is the English language-selector target.
        # Keep it on the English source page instead of localizing it back to the current locale.
        if resolved.resolve() == source_path.resolve():
            target = source_path.resolve()
        else:
            target = local_path(resolved, locale)
        relative = Path(__import__("os").path.relpath(target, target_path.parent)).as_posix()
        rebuilt = urlunsplit((parts.scheme, parts.netloc, relative, parts.query, parts.fragment))
        return f'{name}="{rebuilt}"'

    source = re.sub(r'((?:href|src))="([^"]+)"', rewrite, source)
    source = source.replace('<html lang="en">', f'<html lang="{LOCALE_CODES[locale]}">')
    source = re.sub(
        r'<link rel="canonical" href="[^"]+">',
        f'<link rel="canonical" href="https://ursusloft.com/{locale}/' + output_relative_path(source_path.relative_to(ROOT).as_posix(), locale) + '">',
        source,
    )
    localized_url = "https://ursusloft.com/" + locale + "/" + output_relative_path(source_path.relative_to(ROOT).as_posix(), locale)
    source = re.sub(
        r'(<meta property="og:url" content=")[^"]*(")',
        r'\g<1>' + localized_url + r'\2',
        source,
    )
    return source


def build(
    source_root: Path,
    translation_file: Path,
    output_root: Path,
    locale: str | None = None,
    pages: tuple[str, ...] = PAGES,
) -> None:
    translations = json.loads(translation_file.read_text(encoding="utf-8"))
    output_root = output_root.resolve()
    for relative_path in pages:
        source = (source_root / relative_path).read_text(encoding="utf-8")
        target_relative = output_relative_path(relative_path, locale or "")
        target = output_root / target_relative
        if locale:
            source = localized_source(source, source_root / relative_path, target, locale)
        builder = LocalizedBuilder(relative_path, translations)
        builder.feed(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("".join(builder.output), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    extract = sub.add_parser("extract")
    extract.add_argument("--output", type=Path, default=ROOT / "translations" / "en.json")
    build_cmd = sub.add_parser("build")
    build_cmd.add_argument("--translations", type=Path, required=True)
    build_cmd.add_argument("--output", type=Path, required=True)
    build_cmd.add_argument("--locale", choices=tuple(LOCALE_CODES))
    build_cmd.add_argument("--page", action="append", choices=PAGES)
    args = parser.parse_args()
    if args.command == "extract":
        print(f"extracted={write_english_json(args.output)}")
    else:
        build(ROOT, args.translations, args.output, args.locale, tuple(args.page or PAGES))
        print(f"built={args.output}")


if __name__ == "__main__":
    main()
