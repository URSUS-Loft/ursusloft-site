"""Report untranslated English text nodes in localized URSUS Loft pages."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
LOCALES = ("ja", "zh-cn", "es", "fr", "pt-br", "de", "it", "id")
PAGES = (
    "index.html", "products/scene-director.html", "products/persona-director.html", "products/scene-director/guides/index.html",
    "products/scene-director/guides/image-to-image-prompt-workflow.html",
    "products/scene-director/guides/reference-image-order.html",
    "products/scene-director/guides/character-consistency.html", "support/index.html",
    "support/scene-director.html", "privacy/scene-director.html", "legal/scene-director-eula.html",
)
ALLOWED = {
    "URSUS Loft", "Scene Director", "BEAR Works", "Final Prompt", "Compact Prompt",
    "Microsoft Store", "Windows", "GitHub", "Image-to-Image", "Persona Director",
    "support@ursusloft.com", "© 2026 URSUS Loft", "English", "한국어", "日本語",
    "简体中文", "Español", "Français", "Português (Brasil)", "Deutsch", "Italiano",
    "Bahasa Indonesia", "Language", "Menu", "/", "→", "↓", ".", "01", "02", "03", "04", "05",
}

class TextNodes(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.nodes: list[str] = []

    def handle_data(self, data: str) -> None:
        value = " ".join(data.split())
        if value:
            self.nodes.append(value)

def nodes(path: Path) -> list[str]:
    parser = TextNodes()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.nodes

def source(relative_path: str) -> Path:
    return ROOT / relative_path.replace("character-consistency.html", "character-consistency.html")

def is_allowed(value: str) -> bool:
    return value in ALLOWED or value.startswith("%APPDATA%") or re.fullmatch(r"[0-9: ]+", value) is not None

def main() -> int:
    residuals: list[tuple[str, str]] = []
    for locale in LOCALES:
        for page in PAGES:
            for english, translated in zip(nodes(source(page)), nodes(ROOT / locale / page)):
                if english == translated and not is_allowed(english):
                    residuals.append((f"{locale}/{page}", english))
    for page, value in residuals:
        print(f"{page}: {value}")
    print(f"residuals={len(residuals)}")
    return 1 if residuals else 0

if __name__ == "__main__":
    raise SystemExit(main())
