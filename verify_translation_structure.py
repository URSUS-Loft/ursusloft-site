"""Compare translated pages against their English structural source."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
LOCALES = ("ja", "zh-cn", "es", "fr", "pt-br", "de", "it", "id")
PAGES = (
    "index.html", "products/scene-director.html", "products/persona-director.html", "products/scene-director/guides/index.html",
    "products/scene-director/guides/image-to-image-prompt-workflow.html",
    "products/scene-director/guides/reference-image-order.html",
    "products/scene-director/guides/character-consistency.html", "support/index.html",
    "support/scene-director.html", "privacy/scene-director.html", "legal/scene-director-eula.html",
)

class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.structure: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.structure.append(("start", tag, f"{values.get('class', '')}|{values.get('id', '')}"))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.structure.append(("void", tag, f"{values.get('class', '')}|{values.get('id', '')}"))

    def handle_endtag(self, tag: str) -> None:
        self.structure.append(("end", tag, ""))

def parse(path: Path) -> list[tuple[str, str, str]]:
    parser = StructureParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.structure

def english_source(relative_path: str) -> Path:
    return ROOT / relative_path.replace("character-consistency.html", "character-consistency.html")

def main() -> int:
    mismatches: list[str] = []
    for locale in LOCALES:
        for relative_path in PAGES:
            if parse(english_source(relative_path)) != parse(ROOT / locale / relative_path):
                mismatches.append(f"{locale}/{relative_path}")
    print(f"checked={len(LOCALES) * len(PAGES)} mismatches={len(mismatches)}")
    print("\n".join(mismatches))
    return 1 if mismatches else 0

if __name__ == "__main__":
    raise SystemExit(main())
