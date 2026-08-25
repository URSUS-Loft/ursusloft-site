(function () {
  const localeRoutes = [
    ['en', '', 'English'],
    ['ko', 'ko', '한국어'],
    ['ja', 'ja', '日本語'],
    ['zh-CN', 'zh-cn', '简体中文'],
    ['zh-TW', 'zh-tw', '繁體中文'],
    ['es', 'es', 'Español'],
    ['fr', 'fr', 'Français'],
    ['de', 'de', 'Deutsch'],
    ['it', 'it', 'Italiano'],
    ['pt-BR', 'pt-br', 'Português (Brasil)'],
    ['id', 'id', 'Bahasa Indonesia'],
    ['th', 'th', 'ไทย'],
    ['vi', 'vi', 'Tiếng Việt'],
    ['tr', 'tr', 'Türkçe'],
    ['hi', 'hi', 'हिन्दी'],
    ['pl', 'pl', 'Polski']
  ];

  const pathParts = window.location.pathname.split('/').filter(Boolean);
  const knownPrefixes = new Set(localeRoutes.map((entry) => entry[1]).filter(Boolean));
  const currentPrefix = knownPrefixes.has(pathParts[0]) ? pathParts.shift() : '';
  const currentLocale = localeRoutes.find((entry) => entry[1] === currentPrefix) || localeRoutes[0];
  let currentRoute = pathParts.join('/');
  if (!currentRoute) currentRoute = 'index.html';
  if (!currentRoute.split('/').pop().includes('.')) currentRoute += '/index.html';
  const fullyLocalizedRoutes = new Set([
    'index.html',
    'products/scene-director.html',
    'products/persona-director.html',
    'products/scene-director/guides/index.html',
    'products/scene-director/guides/reference-image-order.html',
    'products/scene-director/guides/image-to-image-prompt-workflow.html',
    'products/scene-director/guides/character-consistency.html',
    'support/index.html',
    'support/scene-director.html',
    'support/persona-director.html',
    'support/ursus-link.html',
    'privacy/scene-director.html',
    'privacy/persona-director.html',
    'privacy/index.html',
    'legal/scene-director-eula.html',
    'privacy/ursus-link/index.html'
  ]);
  const availableLocales = fullyLocalizedRoutes.has(currentRoute)
    ? localeRoutes
    : localeRoutes.filter((entry) => entry[1] === currentPrefix || entry[1] === '');

  let languageSelector = document.querySelector('.language-selector');
  if (!languageSelector) {
    let navTools = document.querySelector('.nav-tools');
    if (!navTools) {
      const existingHeaderInner = document.querySelector('.site-header .header-inner');
      if (existingHeaderInner) {
        navTools = document.createElement('div');
        navTools.className = 'nav-tools';
        existingHeaderInner.appendChild(navTools);
      } else {
        const header = document.createElement('header');
        header.className = 'site-header locale-route-header';
        const homeHref = `/${currentPrefix ? `${currentPrefix}/` : ''}index.html`;
        header.innerHTML = `<div class="container header-inner"><a class="brand" href="${homeHref}" aria-label="URSUS Loft"><img class="brand-mark" src="/assets/images/ursus-loft-logo.png" alt="URSUS Loft"></a><div class="nav-tools"></div></div>`;
        document.body.insertBefore(header, document.body.firstChild);
        navTools = header.querySelector('.nav-tools');
      }
    }
    languageSelector = document.createElement('details');
    languageSelector.className = 'language-selector';
    languageSelector.innerHTML = '<summary>Language</summary><div class="language-selector__menu"></div>';
    navTools.appendChild(languageSelector);
  }

  const languageMenu = languageSelector.querySelector('.language-selector__menu');
  const languageSummary = languageSelector.querySelector('summary');
  if (languageSummary) {
    languageSummary.textContent = currentLocale[2];
    languageSummary.setAttribute('aria-label', `Language: ${currentLocale[2]}`);
  }
  if (languageMenu) {
    languageMenu.setAttribute('aria-label', 'Language options');
    languageMenu.replaceChildren(...availableLocales.map(([code, prefix, name]) => {
      const link = document.createElement('a');
      link.lang = code;
      link.textContent = name;
      link.href = `/${prefix ? `${prefix}/` : ''}${currentRoute}`;
      if (prefix === currentPrefix) link.setAttribute('aria-current', 'page');
      return link;
    }));
  }

  document.addEventListener('click', (event) => {
    if (languageSelector.open && !languageSelector.contains(event.target)) {
      languageSelector.removeAttribute('open');
    }
  });

  languageSelector.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      languageSelector.removeAttribute('open');
      languageSummary?.focus();
    }
  });

  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');

  if (header) {
    const updateHeader = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
    updateHeader();
    window.addEventListener('scroll', updateHeader, { passive: true });
  }

  if (!toggle || !nav) return;

  const closeMenu = () => {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  };

  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeMenu();
  });
}());
