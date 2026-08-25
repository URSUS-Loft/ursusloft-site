"""Validate URSUS Link support routes, SEO metadata, and internal links."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("", "ko", "ja", "zh-cn", "zh-tw", "es", "fr", "de", "it", "pt-br", "id", "th", "vi", "tr", "hi", "pl")
HREFLANG = ("en", "ko", "ja", "zh-CN", "zh-TW", "es", "fr", "de", "it", "pt-BR", "id", "th", "vi", "tr", "hi", "pl")


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.values.append(value)


def root_for(locale: str) -> Path:
    return ROOT / locale if locale else ROOT


def public_url(locale: str) -> str:
    return f"https://ursusloft.com/{locale + '/' if locale else ''}support/ursus-link.html"


def local_target(page: Path, value: str) -> Path | None:
    parts = urlsplit(value)
    if parts.scheme or value.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    target = ROOT / parts.path.lstrip("/") if parts.path.startswith("/") else page.parent / parts.path
    target = target.resolve()
    if target.is_dir():
        target /= "index.html"
    return target


def main() -> int:
    errors: list[str] = []
    broken: list[str] = []
    css = (ROOT / "assets/css/styles.css").read_text(encoding="utf-8")
    js = (ROOT / "assets/js/site.js").read_text(encoding="utf-8")
    if not re.search(r"\.product-card-icon--ursus-link\s*\{\s*border-color:\s*#fff;\s*\}", css):
        errors.append("URSUS Link icon border is not white")
    if "'support/ursus-link.html'" not in js:
        errors.append("support route missing from shared locale selector")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for locale in LOCALES:
        page = root_for(locale) / "support/ursus-link.html"
        index = root_for(locale) / "support/index.html"
        if not page.is_file() or not index.is_file():
            errors.append(f"missing route: {locale or 'en'}")
            continue
        source = page.read_text(encoding="utf-8")
        index_source = index.read_text(encoding="utf-8")
        expected = public_url(locale)
        if f'<link rel="canonical" href="{expected}">' not in source:
            errors.append(f"canonical: {locale or 'en'}")
        for language in HREFLANG:
            if f'hreflang="{language}"' not in source:
                errors.append(f"hreflang {language}: {locale or 'en'}")
        if 'hreflang="x-default"' not in source:
            errors.append(f"x-default: {locale or 'en'}")
        if f"<loc>{expected}</loc>" not in sitemap:
            errors.append(f"sitemap: {locale or 'en'}")
        if index_source.count('href="ursus-link.html"') != 1:
            errors.append(f"support card: {locale or 'en'}")
        if index_source.count("product-card-icon--ursus-link") != 1:
            errors.append(f"support icon: {locale or 'en'}")
        if source.count('<section><h2>') != 7 or source.count("<li>") != 7:
            errors.append(f"content structure: {locale or 'en'}")
        if "support@ursusloft.com" not in source or "../privacy/ursus-link/index.html" not in source:
            errors.append(f"support/privacy link: {locale or 'en'}")
        if re.search(r"100% secure|completely safe|unhackable|military-grade|always encrypted|complete NAS replacement|full NAS|cloud replacement", source, re.I):
            errors.append(f"forbidden claim: {locale or 'en'}")

        for owner, document in ((page, source), (index, index_source)):
            parser = Links()
            parser.feed(document)
            for value in parser.values:
                target = local_target(owner, value)
                if target is not None and not target.exists():
                    broken.append(f"{owner.relative_to(ROOT)} -> {value}")

    # Confirm the sitemap remains parseable and no route was inserted twice.
    ET.parse(ROOT / "sitemap.xml")
    for locale in LOCALES:
        if sitemap.count(f"<loc>{public_url(locale)}</loc>") != 1:
            errors.append(f"duplicate sitemap route: {locale or 'en'}")

    errors.extend(f"broken link: {value}" for value in sorted(set(broken)))
    print(
        f"support_cards={len(LOCALES)} support_pages={len(LOCALES)} "
        f"hreflang_per_page={len(HREFLANG)} broken_internal_links={len(set(broken))} errors={len(errors)}"
    )
    if errors:
        print("\n".join(errors))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
