"""Create the localized Privacy hub and point every footer Privacy link to it."""

from __future__ import annotations

from html import escape
from pathlib import Path
import os
import re


ROOT = Path(__file__).resolve().parents[1]
LOCALES = {
    "": ("en", "en"), "ko": ("ko", "ko"), "ja": ("ja", "ja"),
    "zh-cn": ("zh-CN", "zh-CN"), "zh-tw": ("zh-Hant", "zh-TW"),
    "es": ("es", "es"), "fr": ("fr", "fr"), "de": ("de", "de"),
    "it": ("it", "it"), "pt-br": ("pt-BR", "pt-BR"), "id": ("id", "id"),
    "th": ("th", "th"), "vi": ("vi", "vi"), "tr": ("tr", "tr"),
    "hi": ("hi", "hi"), "pl": ("pl", "pl"),
}
COPY = {
    "": ("Privacy Policy", "Choose a product to view its Privacy Policy."),
    "ko": ("개인정보처리방침", "제품을 선택하여 해당 개인정보처리방침을 확인하세요."),
    "ja": ("プライバシーポリシー", "製品を選択して、各プライバシーポリシーをご確認ください。"),
    "zh-cn": ("隐私政策", "请选择产品以查看对应的隐私政策。"),
    "zh-tw": ("隱私權政策", "請選擇產品以查看對應的隱私權政策。"),
    "es": ("Política de privacidad", "Elige un producto para consultar su Política de privacidad."),
    "fr": ("Politique de confidentialité", "Choisissez un produit pour consulter sa politique de confidentialité."),
    "de": ("Datenschutz", "Wählen Sie ein Produkt, um die zugehörige Datenschutzerklärung anzusehen."),
    "it": ("Informativa sulla privacy", "Scegli un prodotto per visualizzare la relativa informativa sulla privacy."),
    "pt-br": ("Política de privacidade", "Escolha um produto para consultar a respectiva Política de privacidade."),
    "id": ("Kebijakan Privasi", "Pilih produk untuk melihat Kebijakan Privasi yang sesuai."),
    "th": ("นโยบายความเป็นส่วนตัว", "เลือกผลิตภัณฑ์เพื่อดูนโยบายความเป็นส่วนตัวที่เกี่ยวข้อง"),
    "vi": ("Chính sách quyền riêng tư", "Chọn một sản phẩm để xem Chính sách quyền riêng tư tương ứng."),
    "tr": ("Gizlilik Politikası", "İlgili Gizlilik Politikasını görüntülemek için bir ürün seçin."),
    "hi": ("गोपनीयता नीति", "संबंधित गोपनीयता नीति देखने के लिए कोई उत्पाद चुनें।"),
    "pl": ("Polityka prywatności", "Wybierz produkt, aby wyświetlić jego politykę prywatności."),
}


def public_url(prefix: str) -> str:
    return f"https://ursusloft.com/{prefix + '/' if prefix else ''}privacy/index.html"


def alternates() -> str:
    links = [f'<link rel="alternate" hreflang="{hreflang}" href="{public_url(prefix)}">' for prefix, (_, hreflang) in LOCALES.items()]
    links.append(f'<link rel="alternate" hreflang="x-default" href="{public_url("")}">')
    return "\n  ".join(links)


def tag(source: str, name: str) -> str:
    match = re.search(rf"<{name}\b.*?</{name}>", source, re.S)
    if not match:
        raise ValueError(f"missing {name}")
    return match.group(0)


def page(prefix: str) -> str:
    root = ROOT / prefix if prefix else ROOT
    source = (root / "privacy" / "scene-director.html").read_text(encoding="utf-8")
    if "<header" not in source or "<footer" not in source:
        source = (root / "privacy" / "persona-director.html").read_text(encoding="utf-8")
    header = tag(source, "header")
    footer = tag(source, "footer").replace('href="scene-director.html"', 'href="index.html"')
    title, intro = COPY[prefix]
    full_title = f"{title} — URSUS Loft"
    assets = "../../" if prefix else "../"
    return f'''<!doctype html>
<html lang="{LOCALES[prefix][0]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(full_title)}</title>
  <meta name="description" content="{escape(intro, quote=True)}">
  <meta property="og:title" content="{escape(full_title, quote=True)}">
  <meta property="og:description" content="{escape(intro, quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{public_url(prefix)}">
  <meta name="twitter:card" content="summary">
  <link rel="canonical" href="{public_url(prefix)}">
  {alternates()}
  <link rel="stylesheet" href="{assets}assets/css/styles.css">
  <script src="{assets}assets/js/site.js" defer></script>
</head>
<body>
  {header}
  <main>
    <section class="page-hero"><div class="container"><h1>{escape(title)}</h1></div></section>
    <section class="section"><div class="container privacy-hub"><p>{escape(intro)}</p><nav aria-label="{escape(title, quote=True)}"><a href="scene-director.html">Scene Director <span aria-hidden="true">→</span></a><a href="persona-director.html">Persona Director <span aria-hidden="true">→</span></a><a href="ursus-link/index.html">URSUS Link <span aria-hidden="true">→</span></a></nav></div></section>
  </main>
  {footer}
</body>
</html>
'''


def replace_footer_privacy_links() -> int:
    changed = 0
    for path in ROOT.rglob("*.html"):
        source = path.read_text(encoding="utf-8")
        footer_match = re.search(r"<footer\b.*?</footer>", source, re.S)
        if not footer_match:
            continue
        target = path.parents[1] / "privacy" / "index.html" if path.parent.name in {"support", "products", "legal", "guides"} else None
        relative = path.relative_to(ROOT)
        prefix = relative.parts[0] if relative.parts and relative.parts[0] in LOCALES and relative.parts[0] else ""
        site_root = ROOT / prefix if prefix else ROOT
        target = site_root / "privacy" / "index.html"
        hub_href = os.path.relpath(target, path.parent).replace("\\", "/")
        original_footer = footer_match.group(0)
        footer = original_footer
        if 'class="footer-nav"' not in footer:
            standard = (site_root / "index.html").read_text(encoding="utf-8")
            standard_nav = re.search(r'<nav\s+class="footer-nav".*?</nav>', standard, re.S)
            if not standard_nav:
                raise ValueError(f"missing standard footer navigation: {site_root}")
            nav = standard_nav.group(0)
            nav = re.sub(r'(<a\s+href=")[^"]*(")', rf'\g<1>{hub_href}\2', nav, count=1)
            footer = re.sub(r'(<img\b[^>]*>)(\s*<p\b)', rf'\1{nav}\2', footer, count=1)
        # Every shared footer has Privacy as its first navigation item. Replacing
        # that one anchor also corrects URSUS Link documents, whose prior link
        # was the document's own index.html.
        updated = re.sub(
            r'(<nav\s+class="footer-nav"[^>]*>\s*<a\s+href=")[^"]*(")',
            rf'\g<1>{hub_href}\2',
            footer,
            count=1,
        )
        support_href = os.path.relpath(site_root / "support" / "index.html", path.parent).replace("\\", "/")
        legal_href = os.path.relpath(site_root / "legal" / "scene-director-eula.html", path.parent).replace("\\", "/")
        updated = re.sub(r'href="(?:\.\./)*support/index\.html"', f'href="{support_href}"', updated)
        updated = re.sub(r'href="(?:\.\./)*legal/scene-director-eula\.html"', f'href="{legal_href}"', updated)
        if updated != original_footer:
            source = source[:footer_match.start()] + updated + source[footer_match.end():]
            path.write_text(source, encoding="utf-8")
            changed += 1
    return changed


def add_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    source = path.read_text(encoding="utf-8")
    additions = [f"  <url><loc>{public_url(prefix)}</loc></url>" for prefix in LOCALES if f"<loc>{public_url(prefix)}</loc>" not in source]
    path.write_text(source.replace("</urlset>", "\n".join(additions) + ("\n" if additions else "") + "</urlset>"), encoding="utf-8")


def main() -> None:
    for prefix in LOCALES:
        root = ROOT / prefix if prefix else ROOT
        (root / "privacy" / "index.html").write_text(page(prefix), encoding="utf-8")
    changed = replace_footer_privacy_links()
    add_sitemap()
    print(f"privacy_hubs={len(LOCALES)} footers_updated={changed}")


if __name__ == "__main__":
    main()
