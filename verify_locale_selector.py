"""Verify that every fully localized public route uses the shared selector source."""

from __future__ import annotations

from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
LOCALE_DIRS = ("", "ko", "ja", "zh-cn", "zh-tw", "es", "fr", "de", "it", "pt-br", "id", "th", "vi", "tr", "hi", "pl")
SITE_JS = ROOT / "assets/js/site.js"


def sitemap_routes() -> set[str]:
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    document = ET.parse(ROOT / "sitemap.xml")
    routes: set[str] = set()
    for location in document.findall("sm:url/sm:loc", namespace):
        value = (location.text or "").removeprefix("https://ursusloft.com/")
        if not value:
            routes.add("index.html")
        elif value.endswith("/") or "." not in value.rsplit("/", 1)[-1]:
            routes.add(f"{value.rstrip('/')}/index.html")
        else:
            routes.add(value)
    return routes


def localized_route(route: str) -> bool:
    return all((ROOT / directory / route).is_file() for directory in LOCALE_DIRS)


def selector_routes(source: str) -> set[str]:
    match = re.search(r"fullyLocalizedRoutes\s*=\s*new Set\(\[(.*?)\]\);", source, re.S)
    if match is None:
        raise ValueError("Could not find fullyLocalizedRoutes in assets/js/site.js")
    return set(re.findall(r"'([^']+)'", match.group(1)))


def main() -> int:
    source = SITE_JS.read_text(encoding="utf-8")
    routes = sitemap_routes()
    expected = {route for route in routes if localized_route(route)}
    configured = selector_routes(source)
    errors: list[str] = []

    if len(re.findall(r"\['(?:en|ko|ja|zh-CN|zh-TW|es|fr|de|it|pt-BR|id|th|vi|tr|hi|pl)'", source)) != 16:
        errors.append("assets/js/site.js does not define exactly 16 locale entries")

    missing = sorted(expected - configured)
    stale = sorted(configured - expected)
    if missing:
        errors.append(f"fully localized routes missing from selector: {', '.join(missing)}")
    if stale:
        errors.append(f"selector routes without 16 locale files: {', '.join(stale)}")

    html_files = list(ROOT.rglob("*.html"))
    for page in html_files:
        content = page.read_text(encoding="utf-8")
        relative = page.relative_to(ROOT).as_posix()
        if "assets/js/site.js" not in content:
            errors.append(f"{relative}: shared selector script is missing")
        selector = re.search(r'<details class="language-selector">(.*?)</details>', content, re.S)
        if selector and "<a" in selector.group(1):
            errors.append(f"{relative}: legacy locale links remain in HTML")

    print(
        f"html_pages={len(html_files)} fully_localized_routes={len(expected)} "
        f"fully_localized_pages={len(expected) * len(LOCALE_DIRS)} errors={len(errors)}"
    )
    print("\n".join(errors))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
