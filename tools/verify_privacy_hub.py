"""Verify the localized Privacy hub, shared footer entry points, and links."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import os
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("", "ko", "ja", "zh-cn", "zh-tw", "es", "fr", "de", "it", "pt-br", "id", "th", "vi", "tr", "hi", "pl")
HREFLANGS = ("en", "ko", "ja", "zh-CN", "zh-TW", "es", "es", "fr", "de", "it", "pt-BR", "id", "th", "vi", "tr", "hi", "pl")


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.values.append(value)


def page_root(locale: str) -> Path:
    return ROOT / locale if locale else ROOT


def public(locale: str, route: str) -> str:
    return f"https://ursusloft.com/{locale + '/' if locale else ''}{route}"


def target(page: Path, value: str) -> Path | None:
    parts = urlsplit(value)
    if parts.scheme or value.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    result = ROOT / parts.path.lstrip("/") if parts.path.startswith("/") else page.parent / parts.path
    result = result.resolve()
    return result / "index.html" if result.is_dir() else result


def main() -> int:
    errors: list[str] = []
    broken: set[str] = set()
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    ET.parse(ROOT / "sitemap.xml")
    js = (ROOT / "assets/js/site.js").read_text(encoding="utf-8")
    if "'privacy/index.html'" not in js:
        errors.append("privacy index missing from locale selector registry")

    for locale in LOCALES:
        root = page_root(locale)
        path = root / "privacy/index.html"
        source = path.read_text(encoding="utf-8") if path.is_file() else ""
        route = "privacy/index.html"
        expected = public(locale, route)
        if not source:
            errors.append(f"missing hub: {locale or 'en'}")
            continue
        if f'<link rel="canonical" href="{expected}">' not in source:
            errors.append(f"canonical: {locale or 'en'}")
        for href_lang in set(HREFLANGS):
            if f'hreflang="{href_lang}"' not in source:
                errors.append(f"hreflang {href_lang}: {locale or 'en'}")
        if f'hreflang="x-default" href="{public("", route)}"' not in source:
            errors.append(f"x-default: {locale or 'en'}")
        if sitemap.count(f"<loc>{expected}</loc>") != 1:
            errors.append(f"sitemap: {locale or 'en'}")
        for product in ("scene-director.html", "persona-director.html", "ursus-link/index.html"):
            if f'href="{product}"' not in source:
                errors.append(f"product link markup {product}: {locale or 'en'}")

    for path in ROOT.rglob("*.html"):
        source = path.read_text(encoding="utf-8")
        footer = re.search(r"<footer\b.*?</footer>", source, re.S)
        if footer:
            first_link = re.search(r'<nav\s+class="footer-nav"[^>]*>\s*<a\s+href="([^"]+)"', footer.group(0))
            relative = path.relative_to(ROOT)
            locale = relative.parts[0] if relative.parts and relative.parts[0] in LOCALES else ""
            expected_target = page_root(locale) / "privacy/index.html"
            if not first_link or target(path, first_link.group(1)) != expected_target.resolve():
                errors.append(f"footer privacy target: {relative.as_posix()}")
        parser = Links()
        parser.feed(source)
        for value in parser.values:
            resolved = target(path, value)
            if resolved is not None and not resolved.exists():
                broken.add(f"{path.relative_to(ROOT).as_posix()} -> {value}")

    print(f"privacy_hubs={len(LOCALES)} product_privacy_links={len(LOCALES) * 3} broken_internal_links={len(broken)} errors={len(errors)}")
    if errors:
        print("\n".join(errors))
    if broken:
        print("\n".join(sorted(broken)))
    return 1 if errors or broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
