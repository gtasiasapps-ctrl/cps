/* ══════════════════════════════════════════════════════════
   LOADER — overlay με το λογότυπο ώσπου να φορτώσει η σελίδα
   ══════════════════════════════════════════════════════════ */
(function(){
  const el = document.getElementById('loader');
  if (!el) return;
  const MIN = 650;                      // ελάχιστη διάρκεια (να μη «αστράφτει»)
  const t0 = performance.now();
  let done = false;
  function hide(){
    if (done) return; done = true;
    const wait = Math.max(0, MIN - (performance.now() - t0));
    setTimeout(() => {
      el.classList.add('off');
      document.documentElement.classList.remove('cps-loading');
      setTimeout(() => { if (el.parentNode) el.parentNode.removeChild(el); }, 800);
    }, wait);
  }
  if (document.readyState === 'complete') hide();
  else window.addEventListener('load', hide);
  setTimeout(hide, 4500);               // δίχτυ ασφαλείας
  window.__cpsLoaderHide = hide;
})();

/* ══════════════════════════════════════════════════════════
   ΠΑΝΤΑ ΑΠΟ ΤΗΝ ΑΡΧΗ ΣΤΟ REFRESH
   → σε refresh/revisit ξεκινάμε από το hero,
     ΕΚΤΟΣ αν το URL έχει #section (τότε πάμε στην ενότητα).
   ══════════════════════════════════════════════════════════ */
(function(){
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  const isReload = !!window.__CPS_RELOAD;
  function goTop(){
    if (location.hash && !isReload) return;    // κλικ σε #section → σεβόμαστε το anchor
    const de = document.documentElement;
    const prev = de.style.scrollBehavior;
    de.style.scrollBehavior = 'auto';          // χωρίς smooth animation
    window.scrollTo(0, 0);
    de.style.scrollBehavior = prev;
  }
  goTop();
  window.addEventListener('load', goTop);
  window.addEventListener('pageshow', (e) => { if (e.persisted) goTop(); });
  // τα anchors μέσα στη σελίδα (#projects) να δουλεύουν κανονικά
})();

/* ══════════════════════════════════════════════════════════
   C.P.S — κοινό script (index.html + project.html)
   Απαιτεί: assets/cps-data.js (I18N, PROJECTS)
   ══════════════════════════════════════════════════════════ */
let LANG = (localStorage.getItem('cps-lang') === 'en') ? 'en' : 'el';
// ?lang=en / ?lang=el στο URL (για hreflang + shareable links) — κερδίζει του localStorage
(function(){
  const q = new URLSearchParams(location.search).get('lang');
  if (q === 'en' || q === 'el'){ LANG = q; localStorage.setItem('cps-lang', q); }
})();
const t = k => (I18N[LANG] && I18N[LANG][k] != null) ? I18N[LANG][k] : k;

/* ─────────── SEO: δυναμικά canonical / OG / hreflang ─────────── */
const SITE_URL = 'https://cps-solutions.gr';
const pageFile = () => (location.pathname.split('/').pop() || 'index.html');
const isProjectPage = () => pageFile().indexOf('project.html') === 0;
function currentSlug(){
  if (!isProjectPage() || typeof PROJECTS === 'undefined' || !PROJECTS.length) return null;
  const s = new URLSearchParams(location.search).get('p');
  return PROJECTS.some(p => p.slug === s) ? s : PROJECTS[0].slug;
}
function pageUrl(slug){
  const f = pageFile();
  const base = SITE_URL + '/' + (f === 'index.html' ? '' : f);
  const q = [];
  if (slug) q.push('p=' + encodeURIComponent(slug));
  if (LANG === 'en') q.push('lang=en');
  return base + (q.length ? '?' + q.join('&') : '');
}
function syncMeta(slug){
  const url = pageUrl(slug);
  const el = document.querySelector('link[rel="canonical"]'); if (el) el.href = url;
  const og = document.querySelector('meta[property="og:url"]'); if (og) og.setAttribute('content', url);
  const loc = document.querySelector('meta[property="og:locale"]'); if (loc) loc.setAttribute('content', LANG === 'en' ? 'en_US' : 'el_GR');
  const alt = document.querySelector('meta[property="og:locale:alternate"]'); if (alt) alt.setAttribute('content', LANG === 'en' ? 'el_GR' : 'en_US');
  const base = SITE_URL + '/' + (pageFile() === 'index.html' ? '' : pageFile());
  const q = slug ? '?p=' + encodeURIComponent(slug) : '';
  document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(l=>{
    const h = l.getAttribute('hreflang');
    l.href = h === 'en' ? base + q + (q ? '&' : '?') + 'lang=en' : base + q;
  });
}

function applyI18n(){
  document.documentElement.lang = LANG;
  document.querySelectorAll('[data-i18n]').forEach(el=>{ el.textContent = t(el.dataset.i18n); });
  document.querySelectorAll('[data-i18n-html]').forEach(el=>{ el.innerHTML = t(el.dataset.i18nHtml); });
  document.querySelectorAll('[data-i18n-ph]').forEach(el=>{ el.placeholder = t(el.dataset.i18nPh); });
  document.querySelectorAll('[data-i18n-aria]').forEach(el=>{ el.setAttribute('aria-label', t(el.dataset.i18nAria)); });
  document.querySelectorAll('[data-i18n-title]').forEach(el=>{ el.setAttribute('title', t(el.dataset.i18nTitle)); });
  document.querySelectorAll('.lang button').forEach(b=>b.classList.toggle('on', b.dataset.lang === LANG));
  if (typeof syncMeta === 'function') syncMeta(currentSlug());
}

function setLang(l){
  LANG = (l === 'en') ? 'en' : 'el';
  localStorage.setItem('cps-lang', LANG);
  applyI18n();
  if (typeof renderProjects === 'function') renderProjects();
  if (typeof renderProject === 'function') renderProject();
  if (typeof carouselGo === 'function') carouselGo(0);
  if (typeof carouselRestart === 'function') carouselRestart();
  if (typeof window.closeLightbox === 'function') window.closeLightbox();
}

/* ══════════════════════════════════════════════════════════
   0) ΑΠΟΣΤΟΛΗ ΦΟΡΜΑΣ → EMAIL
   ──────────────────────────────────────────────────────────
   Για να στέλνονται τα αιτήματα ΑΥΤΟΜΑΤΑ στο email (χωρίς να
   ανοίγει το πρόγραμμα email του επισκέπτη):
     • `formsubmit` (προεπιλογή) — ΔΩΡΕΑΝ, ΧΩΡΙΣ εγγραφή: μόνο
       το email πιο κάτω. Την 1η φορά που θα σταλεί αίτημα, το
       FormSubmit στέλνει ένα email επιβεβαίωσης στο inbox —
       πάτα το link μία φορά και τέλος.
     • `web3forms` — ΔΩΡΕΑΝ, χωρίς λογαριασμό: https://web3forms.com
       → βάλε το email σου → παίρνεις Access Key → paste στο key.
     • `formspree` — ΔΩΡΕΑΝ λογαριασμός: https://formspree.io →
       φτιάχνεις form → paste το form id (π.χ. 'xlejqwer').
   Αν κάτι δεν είναι ρυθμισμένο, η φόρμα πέφτει στο mailto:
   (ανοίγει το πρόγραμμα email του επισκέπτη), όπως πριν.
   ══════════════════════════════════════════════════════════ */
const CONTACT_EMAIL = 'cps.redea@gmail.com';
const FORM = {
  provider: 'web3forms',       // 'web3forms' (access key) | 'formsubmit' (χωρίς key) | 'formspree' (form id)
  fallback: 'formsubmit',      // αν αποτύχει ο provider → δοκιμάζει αυτόν (0€, χωρίς key)
  to: CONTACT_EMAIL,           // email προορισμού (το χρησιμοποιεί ο provider 'formsubmit')
  key: '16876d94-9263-47be-bb3f-5f9882f292ca'   // ← web3forms access key
};
const needsKey = p => (p === 'web3forms' || p === 'formspree');
const providerReady = p => p === 'formsubmit' ? !!FORM.to : (needsKey(p) ? !!FORM.key : false);
const formReady = () => [FORM.provider, FORM.fallback].some(p => p && providerReady(p));
const okJSON = (j, r) => {
  if (!r.ok) return false;
  if (j == null) return true;
  if (j.error) return false;
  if (j.success !== undefined) return String(j.success) === 'true';   // web3forms (true) / formsubmit ("true")
  if (j.ok !== undefined) return j.ok === true;                       // formspree
  return true;
};

async function postOnce(provider, data){
  if (!providerReady(provider)) throw new Error('provider-not-configured:' + provider);
  const u = provider === 'formspree'  ? 'https://formspree.io/f/' + FORM.key
          : provider === 'web3forms'  ? 'https://api.web3forms.com/submit'
          : 'https://formsubmit.co/ajax/' + FORM.to;
  // FormData (multipart) → «απλό» request, χωρίς CORS preflight
  const fd = new FormData();
  if (provider === 'web3forms'){
    fd.append('access_key', FORM.key);
    fd.append('from_name', 'C.P.S — Ιστοσελίδα');
    fd.append('botcheck', '');
  } else if (provider === 'formspree'){
    fd.append('_subject', data.subject);
  } else {                                    // formsubmit
    fd.append('_subject', data.subject);
    fd.append('_template', 'table');
    fd.append('_captcha', 'false');
    fd.append('_replyto', data.email || '');
  }
  Object.keys(data).forEach(k => fd.append(k, data[k] == null ? '' : data[k]));
  const r = await fetch(u, { method: 'POST', headers: { 'Accept': 'application/json' }, body: fd });
  let j = null; try { j = await r.json(); } catch (e) {}
  if (!okJSON(j, r)) throw new Error((j && (j.message || j.error)) || ('HTTP ' + r.status));
  return provider;
}

/* Δοκιμάζει τον provider και, αν αποτύχει, τον fallback —
   ώστε ένα CORS/δικτυακό πρόβλημα να μην χάνει το αίτημα. */
async function postForm(data){
  const chain = [FORM.provider, FORM.fallback]
    .filter((p, i, a) => p && a.indexOf(p) === i && providerReady(p));
  if (!chain.length) throw new Error('form-not-configured');
  let lastErr = null;
  for (const p of chain){
    try { return await postOnce(p, data); }
    catch (e) { lastErr = e; }
  }
  throw lastErr || new Error('send-failed');
}

/* βοηθητικές διαδρομές εικόνων: projects/<slug>/cover.jpg κ.λπ. */
const coverOf = p => p.dir + '/' + p.cover;
const photosOf = p => (p.images || []).map(f => p.dir + '/' + f);

/* ─────────────── 2) CAROUSEL (μόνο στο hero) ─────────────── */
let carouselGo = null, carouselRestart = null;
(function(){
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) document.body.classList.add('reduce-motion');
  const slidesEl = document.getElementById('slides');
  if (!slidesEl) return;

  // 1ο slide = το λογότυπο (πάντα πρώτο) → μετά οι φωτογραφίες του carousel/
  // (αν ο πίνακας CAROUSEL είναι άδειος: οι καρτέλες των έργων)
  const LOGO_SRC = (typeof CAROUSEL_LOGO !== 'undefined' && CAROUSEL_LOGO) ? 'carousel/' + CAROUSEL_LOGO : null;
  const REST = (typeof CAROUSEL !== 'undefined' && CAROUSEL.length)
    ? CAROUSEL.filter(f => f !== CAROUSEL_LOGO).map(f => ({ src: 'carousel/' + f, project: null }))
    : PROJECTS.map(p => ({ src: coverOf(p), project: p }));
  const SLIDES = (LOGO_SRC ? [{ src: LOGO_SRC, logo: true, project: null }] : []).concat(REST);

  const N = SLIDES.length;
  if (!N) return;

  slidesEl.innerHTML = SLIDES.map((s,i)=>`
    <figure class="slide${i===0?' is-active':''}${s.logo?' is-logo':''}">
      <img src="${s.src}" alt="${s.logo ? 'C.P.S — Complete Project Solutions' : ''}" ${i<2?'':'loading="lazy"'} />
    </figure>`).join('');

  const slides = [...slidesEl.children];
  let cur = 0, timer = null, paused = false;
  // Το λογότυπο παίζει ΜΟΝΟ στην αρχή· μετά ο κύκλος συνεχίζει με τις φωτογραφίες
  const hasLogo = !!(SLIDES[0] && SLIDES[0].logo && N > 1);
  let from = 0;

  function alts(){
    slides.forEach((s,i)=>{
      if (SLIDES[i].logo) return;                 // το λογότυπο κρατά το alt του
      const pr = SLIDES[i].project;
      s.querySelector('img').alt = pr ? (pr[LANG].title + ' — ' + pr[LANG].loc) : '';
    });
  }
  function go(i){
    if (i > N - 1) i = from;                    // wrap-around → αρχή του κύκλου
    if (i < 0)     i = N - 1;
    slides[cur].classList.remove('is-active');
    cur = i;
    slides[cur].classList.add('is-active');
    alts();
    if (hasLogo && i > 0) from = 1;             // από 'δω και πέρα όχι ξανά λογότυπο
  }
  // Το slide του λογοτύπου μένει λίγο παραπάνω στην οθόνη
  const DUR = i => (SLIDES[i] && SLIDES[i].logo ? 6500 : 4600);
  function tickNext(){
    timer = setTimeout(()=>{
      if (!paused && !document.hidden) go(cur + 1);
      tickNext();
    }, DUR(cur));
  }
  function start(){ if (timer) return; tickNext(); }
  function stop(){ clearTimeout(timer); timer = null; }
  carouselGo = i => go(from + i);               // το 0 = «αρχή κύκλου» (μετά το splash: 1η φωτογραφία)
  carouselRestart = ()=>{ stop(); start(); };

  const car = document.getElementById('carousel');
  car.addEventListener('mouseenter', ()=> paused = true);
  car.addEventListener('mouseleave', ()=> paused = false);
  document.addEventListener('visibilitychange', ()=> { paused = document.hidden; });

  let sx = null;
  car.addEventListener('pointerdown', e => sx = e.clientX);
  car.addEventListener('pointerup', e => {
    if (sx === null) return;
    const d = e.clientX - sx; sx = null;
    if (Math.abs(d) > 40){ go(cur + (d < 0 ? 1 : -1)); carouselRestart(); }
  });
  car.addEventListener('pointercancel', ()=> sx = null);

  go(0); start();
})();

/* ─────────────── 3) NAV / MENU / GRID / FORMS ─────────────── */
let renderProjects = function(){};
(function(){
  const nav = document.getElementById('nav');
  if (nav){
    const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 12);
    onScroll(); window.addEventListener('scroll', onScroll, {passive:true});
  }

  const burger = document.getElementById('burger');
  const links  = document.getElementById('links');
  if (burger && links){
    burger.addEventListener('click', ()=>{
      const open = links.classList.toggle('open');
      burger.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', String(open));
    });
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', ()=>{
      links.classList.remove('open'); burger.classList.remove('open');
      burger.setAttribute('aria-expanded','false');
    }));
  }

  const grid  = document.getElementById('projects-grid');
  const wlist = document.getElementById('works-list');
  renderProjects = function(){
    if (grid) grid.innerHTML = PROJECTS.map(p=>`
      <a class="proj reveal in" href="project.html?p=${p.slug}" data-cat="${p.cat}">
        <div class="thumb"><img src="${coverOf(p)}" alt="${p[LANG].title}" loading="lazy" /></div>
        <div class="cap">
          <span class="tag">${p[LANG].tag}</span>
          <h3>${p[LANG].title}</h3>
          <span class="loc">${p[LANG].loc}</span>
        </div>
      </a>`).join('');
    if (wlist) wlist.innerHTML = PROJECTS.map(p=>`
      <a href="project.html?p=${p.slug}"><span>${p[LANG].title}</span><span>${p[LANG].loc}</span></a>`).join('');
  };
  renderProjects();

  const filters = document.getElementById('filters');
  if (filters && grid) filters.addEventListener('click', (e)=>{
    const chip = e.target.closest('.chip'); if(!chip) return;
    document.querySelectorAll('#filters .chip').forEach(c=>c.classList.remove('active'));
    chip.classList.add('active');
    const cat = chip.dataset.cat;
    grid.querySelectorAll('.proj').forEach(el=>{
      el.style.display = (cat === 'all' || el.dataset.cat === cat) ? '' : 'none';
    });
  });

  document.querySelectorAll('.lang button').forEach(b=>{
    b.addEventListener('click', ()=> setLang(b.dataset.lang));
  });

  applyI18n();

  if ('IntersectionObserver' in window){
    const io = new IntersectionObserver((entries)=>{
      entries.forEach(en => { if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target);} });
    }, {threshold:.12, rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
  } else {
    document.querySelectorAll('.reveal').forEach(el=>el.classList.add('in'));
  }

  const form = document.getElementById('contactForm');
  if (form){
    const note = document.getElementById('formNote');
    const btn  = form.querySelector('button[type="submit"]');
    const setNote = (msg, ok) => { note.style.color = ok ? '' : 'var(--ink)'; note.style.fontWeight = ok ? '' : '600'; note.textContent = msg; };
    const byMail = (d) => {
      const body = encodeURIComponent(
        `${t('mail.name')}: ${d.get('name')}\n${t('mail.phone')}: ${d.get('phone')||'-'}\n${t('mail.email')}: ${d.get('email')}\n${t('mail.topic')}: ${d.get('topic')}\n\n${d.get('message')}`
      );
      window.location.href = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(t('mail.subject')+' — '+d.get('topic'))}&body=${body}`;
    };
    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      if(!form.checkValidity()){ setNote(t('fo.err'), false); return; }
      const d = new FormData(form);
      if (!formReady()){ setNote(t('fo.ok'), true); byMail(d); return; }   // mailto fallback
      setNote(t('fo.sending'), true);
      if (btn) btn.disabled = true;
      try {
        await postForm({
          subject: t('mail.subject') + ' — ' + d.get('topic'),
          name: d.get('name'), phone: d.get('phone') || '-', email: d.get('email'),
          topic: d.get('topic'), message: d.get('message'), page: location.href
        });
        form.reset();
        setNote(t('fo.done'), true);
      } catch (err){
        setNote(t('fo.fail'), false);
        byMail(d);      // δίχτυ ασφάλειας: ανοίγει το email
      } finally {
        if (btn) btn.disabled = false;
      }
    });
  }

})();

/* ─────────────── 4) ΣΕΛΙΔΑ ΕΡΓΟΥ (project.html) ─────────────── */
let renderProject = null;
(function(){
  const root = document.getElementById('pdetail');
  if (!root) return;

  const idxOf = () => {
    const slug = new URLSearchParams(location.search).get('p');
    const i = PROJECTS.findIndex(p => p.slug === slug);
    return i < 0 ? 0 : i;
  };

  renderProject = function(){
    const i = idxOf();
    const p = PROJECTS[i];
    const L = p[LANG];
    const prev = PROJECTS[(i - 1 + PROJECTS.length) % PROJECTS.length];
    const next = PROJECTS[(i + 1) % PROJECTS.length];

    document.title = `${L.title} — ${L.loc} | CPS Solutions`;

    // ── SEO: meta + structured data ανά έργο ──
    (function(){
      const canon = pageUrl(p.slug);
      const img   = SITE_URL + '/' + coverOf(p);
      const desc  = LANG === 'en'
        ? `${L.title} (${L.tag}) — ${L.loc}. A project by C.P.S – Complete Project Solutions: design, construction and project management in Larissa, Greece.`
        : `${L.title} (${L.tag}) — ${L.loc}. Έργο της C.P.S – Complete Project Solutions: μελέτη, κατασκευή και διαχείριση έργων στη Λάρισα.`;
      const setM = (sel, val) => { const el = document.querySelector(sel); if (el) el.setAttribute('content', val); };
      setM('meta[name="description"]', desc);
      setM('meta[property="og:title"]', `${L.title} — ${L.loc} | CPS Solutions`);
      setM('meta[property="og:description"]', desc);
      setM('meta[property="og:image"]', img);
      setM('meta[name="twitter:title"]', `${L.title} — ${L.loc} | CPS Solutions`);
      setM('meta[name="twitter:description"]', desc);
      setM('meta[name="twitter:image"]', img);
      syncMeta(p.slug);

      let ld = document.getElementById('ld-project');
      if (!ld){
        ld = document.createElement('script');
        ld.type = 'application/ld+json'; ld.id = 'ld-project';
        document.head.appendChild(ld);
      }
      ld.textContent = JSON.stringify({
        '@context': 'https://schema.org', '@type': 'ItemPage',
        'url': canon, 'name': `${L.title} — ${L.loc}`, 'inLanguage': LANG,
        'isPartOf': { '@id': SITE_URL + '/#website' },
        'primaryImageOfPage': { '@type': 'ImageObject', 'url': img },
        'about': { '@type': 'Service', 'name': L.title, 'description': desc,
                   'provider': { '@id': SITE_URL + '/#business' },
                   'areaServed': { '@type': 'City', 'name': L.loc } }
      }, null, 2);

      const bc = document.getElementById('ld-crumbs');
      if (bc) bc.textContent = JSON.stringify({
        '@context': 'https://schema.org', '@type': 'BreadcrumbList', 'inLanguage': LANG,
        'itemListElement': [
          { '@type': 'ListItem', 'position': 1, 'name': t('nav.home'), 'item': SITE_URL + '/' },
          { '@type': 'ListItem', 'position': 2, 'name': t('nav.projects'), 'item': SITE_URL + '/#projects' },
          { '@type': 'ListItem', 'position': 3, 'name': L.title, 'item': canon }
        ]
      }, null, 2);
    })();

    const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    set('pTag', L.tag);
    set('pTitle', L.title);
    set('pLoc', L.loc);
    set('pBody', t('pd.body').replace('{tag}', L.tag).replace('{loc}', L.loc));
    set('pCat', L.tag);
    set('pLoc2', L.loc);
    set('pStatus', t('st.' + p.status));
    set('pYear', p.year);
    set('pNote', t('pd.note'));

    const cap = L.title + ' — ' + L.loc;
    const photos = [coverOf(p), ...photosOf(p)];

    const hero = document.getElementById('pImg');
    if (hero){ hero.src = photos[0]; hero.alt = cap; }

    const gal = document.getElementById('pgallery');
    const rest = photos.slice(1);
    if (gal){
      gal.innerHTML = rest.map(f => `<figure><img src="${f}" alt="${cap}" loading="lazy" /></figure>`).join('');
      gal.style.display = rest.length ? '' : 'none';
    }

    // όλες οι φωτογραφίες ανοίγουν σε μεγάλη προβολή (lightbox)
    const items = photos.map(src => ({ src: src, alt: cap, cap: cap }));
    const zoomables = [hero].concat(gal ? [...gal.querySelectorAll('img')] : []).filter(Boolean);
    zoomables.forEach((im, k) => { im.onclick = () => window.openLightbox(items, k); });

    const pl = document.getElementById('pPrev');
    const pn = document.getElementById('pNext');
    if (pl){ pl.href = 'project.html?p=' + prev.slug; pl.querySelector('b').textContent = prev[LANG].title; }
    if (pn){ pn.href = 'project.html?p=' + next.slug; pn.querySelector('b').textContent = next[LANG].title; }
  };

  renderProject();
})();

/* ─────────────── 5) LIGHTBOX — μεγάλη προβολή φωτογραφίας ─────────────── */
(function(){
  let el = null, items = [], i = 0;

  function build(){
    if (el) return;
    el = document.createElement('div');
    el.className = 'lightbox';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-modal', 'true');
    el.innerHTML =
      '<button class="lb-btn lb-close" type="button" aria-label="Close">✕</button>' +
      '<button class="lb-btn lb-prev"  type="button" aria-label="Previous">‹</button>' +
      '<img class="lb-img" alt="" />' +
      '<button class="lb-btn lb-next"  type="button" aria-label="Next">›</button>' +
      '<div class="lb-cap"></div>';
    document.body.appendChild(el);

    el.addEventListener('click', (e)=>{
      if (e.target.closest('.lb-prev')) { go(i - 1); return; }
      if (e.target.closest('.lb-next')) { go(i + 1); return; }
      if (e.target.closest('.lb-img')) return;     // κλικ στην εικόνα = δεν κλείνει
      close();
    });
    document.addEventListener('keydown', (e)=>{
      if (!el.classList.contains('on')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft') go(i - 1);
      else if (e.key === 'ArrowRight') go(i + 1);
    });
    let sx = null;
    el.addEventListener('pointerdown', e => { sx = e.clientX; });
    el.addEventListener('pointerup', e => {
      if (sx === null) return;
      const d = e.clientX - sx; sx = null;
      if (Math.abs(d) > 40) go(i + (d < 0 ? 1 : -1));
    });
  }
  function paint(){
    const it = items[i] || {};
    el.querySelector('.lb-img').src = it.src || '';
    el.querySelector('.lb-img').alt = it.alt || '';
    el.querySelector('.lb-cap').textContent = it.cap || '';
    const many = items.length > 1 ? '' : 'hidden';
    el.querySelector('.lb-prev').style.visibility = many;
    el.querySelector('.lb-next').style.visibility = many;
  }
  function go(n){ if (!items.length) return; i = ((n % items.length) + items.length) % items.length; paint(); }
  function open(list, idx){
    build();
    items = list || []; i = idx || 0;
    paint();
    el.classList.add('on');
    document.documentElement.style.overflow = 'hidden';
  }
  function close(){
    if (!el) return;
    el.classList.remove('on');
    el.querySelector('.lb-img').src = '';
    document.documentElement.style.overflow = '';
  }
  window.openLightbox = open;
  window.closeLightbox = close;
})();

/* ══════════════════════════════════════════════════════════
   ΒΕΛΑΚΙ «ΠΙΣΩ» (company / services / contact / project)
   → πάει πίσω στην προηγούμενη σελίδα (history.back) αν
     προερχόμαστε από το ίδιο site, αλλιώς στην αρχική.
   ══════════════════════════════════════════════════════════ */
(function(){
  const b = document.querySelector('[data-back]');
  if (!b) return;
  b.addEventListener('click', (e)=>{
    if (history.length > 1){ e.preventDefault(); history.back(); }
    // αλλιώς (direct visit) → αφήνουμε το href="index.html" να δουλέψει
  });
})();
