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
const t = k => (I18N[LANG] && I18N[LANG][k] != null) ? I18N[LANG][k] : k;

function applyI18n(){
  document.documentElement.lang = LANG;
  document.querySelectorAll('[data-i18n]').forEach(el=>{ el.textContent = t(el.dataset.i18n); });
  document.querySelectorAll('[data-i18n-html]').forEach(el=>{ el.innerHTML = t(el.dataset.i18nHtml); });
  document.querySelectorAll('[data-i18n-ph]').forEach(el=>{ el.placeholder = t(el.dataset.i18nPh); });
  document.querySelectorAll('[data-i18n-aria]').forEach(el=>{ el.setAttribute('aria-label', t(el.dataset.i18nAria)); });
  document.querySelectorAll('[data-i18n-title]').forEach(el=>{ el.setAttribute('title', t(el.dataset.i18nTitle)); });
  document.querySelectorAll('.lang button').forEach(b=>b.classList.toggle('on', b.dataset.lang === LANG));
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
const CONTACT_EMAIL = 'nickatsiouras@yahoo.gr';
const FORM = {
  provider: 'formsubmit',      // 'formsubmit' (χωρίς key) | 'web3forms' | 'formspree'
  to: CONTACT_EMAIL,           // πού πάνε τα email
  key: ''                      // web3forms: access key · formspree: form id
};
const formReady = () => FORM.provider === 'formsubmit'
  ? !!FORM.to
  : !!(FORM.provider && FORM.key);
const okJSON = (j, r) => {
  if (!r.ok) return false;
  if (j == null) return true;
  if (j.error) return false;
  if (j.success !== undefined) return String(j.success) === 'true';   // web3forms (true) / formsubmit ("true")
  if (j.ok !== undefined) return j.ok === true;                       // formspree
  return true;
};

async function postForm(data){
  if (!formReady()) throw new Error('form-not-configured');
  const u = FORM.provider === 'formspree'  ? 'https://formspree.io/f/' + FORM.key
          : FORM.provider === 'web3forms'  ? 'https://api.web3forms.com/submit'
          : 'https://formsubmit.co/ajax/' + FORM.to;
  // FormData (multipart) → «απλό» request, χωρίς CORS preflight (δουλεύει παντού)
  const fd = new FormData();
  if (FORM.provider === 'web3forms'){
    fd.append('access_key', FORM.key);
    fd.append('from_name', 'C.P.S — Ιστοσελίδα');
    fd.append('botcheck', '');
  } else if (FORM.provider === 'formspree'){
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
  return true;
}

/* ─────────────── 1) 3D LOGO ─────────────── */
(function(){
  const stage = document.getElementById('stage');
  const logo  = document.getElementById('logo3d');
  if (!stage || !logo) return;

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const LAYERS = reduce ? 1 : 22;
  const DEPTH  = reduce ? 0 : 96;
  const BASE   = reduce ? 0.95 : (window.innerWidth < 860 ? 0.68 : 0.9);
  stage.style.setProperty('--stage-max', String(BASE));

  const frontEl = logo.querySelector('.logo-front');
  const frag = document.createDocumentFragment();
  for (let i = LAYERS - 1; i >= 1; i--){
    const el = document.createElement('img');
    el.className = 'logo-layer';
    el.src = 'assets/wordmark-depth.png';
    el.alt = ''; el.setAttribute('aria-hidden','true');
    const k = i / Math.max(1, LAYERS - 1);
    el.style.transform = `translateZ(${(-DEPTH * k).toFixed(1)}px)`;
    el.style.opacity = String((1 - k * 0.55).toFixed(3));
    el.style.filter = `brightness(${(0.94 + k * 0.20).toFixed(2)})`;
    frag.appendChild(el);
  }
  if (frontEl){ logo.insertBefore(frag, frontEl); } else { logo.appendChild(frag); }

  let tx = 0, ty = 0, cx = 0, cy = 0;
  let px = 0, py = 0, rx = 0, ry = 0;
  let scrollZ = 0, curScrollZ = 0;
  let grow = 0, curGrow = 0;
  let fade = 1, curFade = 1;
  let boost = 0, curBoost = 0;
  let lastMove = 0;
  const IDLE_MS = 3200, GROW_AT = 620;
  let gut = 0, persp = 1400, ox = 0;
  const measure = () => {
    const cs = getComputedStyle(stage);
    gut   = parseFloat(cs.paddingLeft) || 0;
    persp = parseFloat(cs.perspective) || 1400;
    ox    = parseFloat(cs.perspectiveOrigin) || 0;
  };
  measure(); window.addEventListener('resize', measure);
  const dx = (z) => {
    const f = persp / (persp + Math.max(0, z));
    const targetX = ox + ((window.innerWidth / 2 - ox) / f);
    return Math.max(0, targetX - (gut + logo.offsetWidth / 2));
  };

  function onPointer(e){
    const x = (e.clientX / window.innerWidth) - 0.5;
    const y = (e.clientY / window.innerHeight) - 0.5;
    tx = -y * 16; ty = x * 24; rx = -x * 24; ry = -y * 14;
    lastMove = performance.now(); boost = 0.08;
  }
  window.addEventListener('pointermove', onPointer, {passive:true});
  window.addEventListener('touchmove', (e)=>{ if (e.touches[0]) onPointer(e.touches[0]); }, {passive:true});
  window.addEventListener('deviceorientation', (e)=>{
    if (e.gamma == null || e.beta == null) return;
    tx = Math.max(-14, Math.min(14, (e.beta - 45) * 0.32));
    ty = Math.max(-22, Math.min(22, e.gamma * 0.55));
    lastMove = performance.now();
  }, {passive:true});

  function onScroll(){
    const y = window.scrollY || document.documentElement.scrollTop || 0;
    grow = Math.min(1, Math.max(0, y / GROW_AT));
    fade = y <= 700 ? 1 : Math.max(0.10, 1 - (y - 700) / 800);
    scrollZ = Math.min(240, y * 0.16);
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  const ease = 0.06;
  function tick(ts){
    const idle = ts - lastMove > IDLE_MS;
    let gx = 0, gy = 0;
    if (idle && !reduce){
      const s = ts * 0.00022;
      gy = Math.sin(s) * 15; gx = Math.cos(s * 0.8) * 6;
    }
    const damp = 1 - curGrow * 0.75;
    cx += ((tx + gx) * damp - cx) * ease;
    cy += ((ty + gy) * damp - cy) * ease;
    px += (rx - px) * ease;      py += (ry - py) * ease;
    curScrollZ += (scrollZ - curScrollZ) * 0.07;
    curGrow += (grow - curGrow) * 0.10;
    curFade += (fade - curFade) * 0.08;
    curBoost += (boost - curBoost) * 0.10;
    boost *= 0.965;
    stage.style.opacity = Math.min(1, curFade * (BASE + curBoost)).toFixed(3);

    const floatY = reduce ? 0 : Math.sin(ts * 0.00072) * 7;
    const s = 1 + curGrow * (window.innerWidth < 860 ? 0.35 : 0.72);
    const shift = dx(curScrollZ) * curGrow;
    logo.style.transform =
      `translate3d(${(px + shift).toFixed(2)}px, ${(py + floatY).toFixed(2)}px, ${(-curScrollZ).toFixed(1)}px) ` +
      `rotateX(${cx.toFixed(2)}deg) rotateY(${cy.toFixed(2)}deg) scale(${s.toFixed(3)})`;
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);

  const probe = new Image();
  probe.onerror = () => logo.classList.add('no-mask');
  probe.src = 'assets/wordmark-front.png';
})();

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

  // Πηγή: ο φάκελος carousel/ — αν είναι κενός, πέφτει στις καρτέλες των έργων
  const SLIDES = (typeof CAROUSEL !== 'undefined' && CAROUSEL.length)
    ? CAROUSEL.map(f => ({ src: 'carousel/' + f, project: null }))
    : PROJECTS.map(p => ({ src: coverOf(p), project: p }));

  const N = SLIDES.length;
  if (!N) return;

  slidesEl.innerHTML = SLIDES.map((s,i)=>`
    <figure class="slide${i===0?' is-active':''}">
      <img src="${s.src}" alt="" ${i<2?'':'loading="lazy"'} />
    </figure>`).join('');

  const slides = [...slidesEl.children];
  let cur = 0, timer = null, paused = false;

  function alts(){
    slides.forEach((s,i)=>{
      const pr = SLIDES[i].project;
      s.querySelector('img').alt = pr ? (pr[LANG].title + ' — ' + pr[LANG].loc) : '';
    });
  }
  function go(i){
    i = ((i % N) + N) % N;
    slides[cur].classList.remove('is-active');
    cur = i;
    slides[cur].classList.add('is-active');
    alts();
  }
  function start(){ if (timer) return; timer = setInterval(()=>{ if(!paused && !document.hidden) go(cur+1); }, 4600); }
  function stop(){ clearInterval(timer); timer = null; }
  carouselGo = go; carouselRestart = ()=>{ stop(); start(); };

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

  const nlForm = document.getElementById('nlForm');
  if (nlForm){
    const nlMsg = document.getElementById('nlMsg');
    const nlMail = document.getElementById('nlEmail');
    const nlBtn = nlForm.querySelector('button[type="submit"]');
    nlForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      if(!nlMail.checkValidity()){ nlMsg.textContent = t('nl.err'); return; }
      if (!formReady()){ nlMsg.textContent = t('nl.ok'); nlForm.reset(); return; }
      nlMsg.textContent = t('fo.sending');
      if (nlBtn) nlBtn.disabled = true;
      try {
        await postForm({
          subject: 'Newsletter — C.P.S', name: 'Newsletter',
          email: nlMail.value, message: 'Εγγραφή στο newsletter · ' + location.href
        });
        nlMsg.textContent = t('nl.ok'); nlForm.reset();
      } catch (err){
        nlMsg.textContent = t('fo.fail');
      } finally {
        if (nlBtn) nlBtn.disabled = false;
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

    document.title = `${L.title} — ${L.loc} | C.P.S`;

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
