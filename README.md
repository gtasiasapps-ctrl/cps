# CPS Solutions — website

Site για την **C.P.S – Complete Project Solutions** (Λάρισα, από το 2002).
Μελέτη · κατασκευή · διαχείριση έργων — **Real Estate Development** & **Interior Design**.

**Στοιχεία επιχείρησης:** Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος, Λάρισα · τηλ. 2410 538740 · email **nickatsiouras@yahoo.gr**
(επίσημη επωνυμία στο μητρώο: *CPS – Κατσιούρας Νικόλαος Γ.*, πολιτικός μηχανικός).
Υπηρεσίες: **Πολιτικός Μηχανικός · Διακόσμηση · Ολοκληρωμένες Τεχνικές Λύσεις Έργων**.

**Θέμα:** αυστηρά **λευκό / μαύρο** (grayscale). Καμία χρωματική πινελιά —
ούτε στα γράμματα, ούτε στις εικόνες. Παλέτα στο `:root`: `--bg:#fff`, `--ink:#0a0a0a`,
`--muted:#6f6f6f` (ουδέτερο γκρι), `--line` (μαύρα borders με διαφάνεια).

## Δομή

```
cps/
├── index.html              ← ΑΡΧΙΚΗ: μόνο hero + επερχόμενα έργα
├── company.html            ← Η Επιχείρηση (+ statement + KPI)
├── services.html           ← Υπηρεσίες (+ CTA)
├── contact.html            ← Επικοινωνία (+ newsletter)
├── project.html            ← σελίδα έργου  →  project.html?p=<slug>
├── carousel/               ← ⭐ φωτογραφίες του hero carousel (01.jpg, 02.jpg …)
├── projects/               ← ⭐ ΕΝΑΣ ΦΑΚΕΛΟΣ ΑΝΑ ΕΡΓΟ
│   ├── house-pool/{cover,01,02}.jpg
│   └── … (12 φάκελοι)
├── assets/
│   ├── cps.css             όλα τα styles (όλων των σελίδων)
│   ├── cps-data.js         I18N (EL/EN) + PROJECTS + CAROUSEL   ← εδώ δηλώνεις
│   ├── cps.js              κοινό script (loader, 3D logo, carousel, nav, i18n, grid, lightbox)
│   ├── cps-lockup.png · cps-wordmark.png · wordmark-front.png · wordmark-depth.png
├── tools/
│   ├── new-project.sh      ← δημιουργεί φάκελο νέου έργου + snippet
│   └── make-demos.py       ← ξαναπαράγει τα demo projects/
└── preview/                ← screenshots
```

## Hero

- **Χωρίς κείμενο/κουμπιά/τίτλους.** Αριστερά: το 3D λογότυπο (με gutter `clamp(22px,3.4vw,52px)`).
  Δεξιά: **carousel έργων**, ακριβώς το δεξί μισό (φτάνει μέχρι τη δεξιά και την κάτω άκρη).
- Οι εικόνες είναι **σκέτες** — χωρίς πλαίσιο, border, radius, σκιά ή κείμενο από πάνω.
- Carousel: **παίζει πάντα** (ακόμα κι αν το σύστημα έχει «Reduce Motion» — τότε χωρίς zoom),
  crossfade 1,15s + αργό Ken Burns, αλλαγή κάθε 4,6s, pause στο hover, swipe σε touch,
  pause όταν το tab είναι κρυφό. (Χωρίς dots.)
- **Scroll effect του λογότυπου:** όσο κατεβαίνεις, το 3D λογότυπο **μεγαλώνει και
  μετακινείται στο κέντρο** (0 → 1 στα πρώτα 620px scroll)· ανεβαίνοντας **επιστρέφει**
  αριστερά. Μετά το hero ξεθωριάζει ως ~10% για να μη χαλάει την ανάγνωση.
  Σταθερές: `GROW_AT`, `scale = 1 + grow*0.72` στο `<script>`.
  Το κέντρο υπολογίζεται με **αντιστάθμιση της προοπτικής** (`dx(z)`) και η κλίση
  **dampάρει** όσο μεγαλώνει (`damp = 1 - grow*0.75`) ώστε να κάθεται σταθερό στο κέντρο.
- Τα έργα βγαίνουν από τον πίνακα `PROJECTS` (top of `<script>`) — **ίδιος πίνακας**
  τροφοδοτεί και το grid της ενότητας «Έργα».
- Navbar: **full-bleed** — lockup **τέρμα αριστερά**, links **απόλυτα κεντραρισμένα**,
  **EL / EN** δεξιά (+ CTA, κρύβεται <1080px).

### Σελίδες

| Σελίδα | Περιεχόμενο |
|---|---|
| **index.html** | **Μόνο** hero (3D λογότυπο + carousel) και **Επερχόμενα έργα** (φίλτρα + grid + λίστα) |
| **company.html** | Η Επιχείρηση: statement («ΤΟ ΑΡΤΙΟ»), KPI, κείμενο εταιρίας + 6 παράγοντες |
| **services.html** | Οι 3 υπηρεσίες + CTA προς επικοινωνία |
| **contact.html** | Στοιχεία επικοινωνίας, φόρμα, newsletter |
| **project.html** | Σελίδα έργου (`?p=<slug>`): βασική εικόνα, στοιχεία, φωτογραφίες + lightbox, prev/next |

Το **nav** και το **footer** είναι ίδια σε όλες τις σελίδες:
`Αρχική → index.html` · `Η Επιχείρηση → company.html` · `Υπηρεσίες → services.html` ·
`Έργα → index.html#projects` · `Επικοινωνία → contact.html`.

Στο **nav, τέρμα δεξιά**, υπάρχουν εικονίδια **Facebook & Instagram** (`.social`, inline SVG,
χωρίς εξωτερικές βιβλιοθήκες) — μετά το CTA και πριν το burger (mobile).

Οι **εσωτερικές σελίδες** έχουν `class="page"` στο `<body>` → `body.page::before` απλώνει
ένα λευκό gradient στην κορυφή ώστε οι τίτλοι να μένουν καθαροί πάνω από το 3D λογότυπο.

### Πηγές εικόνων

`projects/<slug>/cover.jpg` — 1300×1300 (1:1) ώστε να γεμίζουν το hero χωρίς μεγάλο crop.
Παράγονται από το `tools/make-demos.py` (demo). Αντικατέστησέ τες με πραγματικές φωτό
μέσα στον ίδιο φάκελο, με τα ίδια ονόματα → μηδέν αλλαγές στον κώδικα.

## Το 3D interactive λογότυπο

- **Fixed layer πίσω από το περιεχόμενο** (`#stage`, `z-index:0`, `pointer-events:none`)
  → δεν μπλοκάρει κλικ/nav/φόρμες. **Τέρμα αριστερά**, στο ύψος του hero.
- **22 στοιβαγμένα layers** σε διαφορετικό `translateZ` → πάχος/όγκος (extrusion).
- Interaction: `pointermove` (tilt + parallax), `deviceorientation` (gyro σε κινητό),
  auto-rotation μετά από ~3,2s αδράνειας, scroll fade (→ ~10%) ώστε να μη χαλάει
  την ανάγνωση των επόμενων ενοτήτων, μικρό «boost» όταν κινείς τον δείκτη.
- Όγκος: `.logo-shadow` (απαλή σκιά) + `drop-shadow` pulse.
- `prefers-reduced-motion` → χωρίς animation, μειωμένο πάχος.

Ρυθμίσεις στο 1ο `<script>`: `LAYERS`, `DEPTH`, `BASE` (ένταση).

## Γλώσσα (EL / EN)

- Το κουμπί **EL / EN** στο navbar αλλάζει όλο το site (nav, ενότητες, φόρμα, footer,
  τίτλους έργων). Η επιλογή αποθηκεύεται σε `localStorage` (`cps-lang`).
- Τα κείμενα είναι στο `I18N` object (πάνω-πάνω στο `<script>`) με keys τύπου `nav.home`,
  `co.p2`, `sv.a1`. Στο HTML μπαίνουν με `data-i18n="key"` (ή `data-i18n-html` για HTML,
  `data-i18n-ph` για placeholders, `data-i18n-aria` / `data-i18n-title` για `aria-label` / `title`).

## Σελίδες έργων (multi-page)

- **Κάθε έργο έχει δική του σελίδα**: `project.html?p=<slug>`
  (π.χ. `project.html?p=hotel-trikala`). Τα πλακίδια του grid ΚΑΙ οι γραμμές της λίστας
  «Όλα τα επερχόμενα έργα» οδηγούν εκεί.
- Η σελίδα έργου περιέχει: back link, tag/τίτλο/τοποθεσία, **βασική εικόνα** (46vh),
  περιγραφή, **στοιχεία έργου** (Κατηγορία / Τοποθεσία / Κατάσταση / Παράδοση),
  **μικρογραφίες φωτογραφιών 168×168** και **Προηγούμενο / Επόμενο** έργο.
- **Lightbox:** πατώντας οποιαδήποτε φωτογραφία ανοίγει μεγάλη (όπου κι αν είναι —
  βασική εικόνα ή μικρογραφία). Κλείνει με κλικ έξω / **Esc** · **← →** ή swipe για
  επόμενη/προηγούμενη · κλειδώνει το scroll της σελίδας όσο είναι ανοιχτό.
- Δουλεύει και σε **EL/EN** (τίτλος, κατάσταση, specs, prev/next) και το `document.title`
  ενημερώνεται. Άγνωστο/λάθος slug → πέφτει στο πρώτο έργο (χωρίς 404).
### ➕ Νέο έργο (2 βήματα)

```bash
# 1) φτιάξε τον φάκελο + πάρε έτοιμο το snippet
tools/new-project.sh villa-katerini
#    → ρίξε μέσα το projects/villa-katerini/cover.jpg (+ 01.jpg, 02.jpg ...)

# 2) κόλλησε το snippet στο PROJECTS (assets/cps-data.js)
```

Παράδειγμα εγγραφής:
```js
{slug:'villa-katerini', cat:'res', year:'2027', status:'dev',
 dir:'projects/villa-katerini', cover:'cover.jpg', images:['01.jpg','02.jpg'],
 el:{tag:'Κατοικία',  title:'Βίλα στην Κατερίνη', loc:'Κατερίνη'},
 en:{tag:'Residence', title:'Villa in Katerini',  loc:'Katerini'}},
```
- `dir` = ο φάκελος, `cover` = η κύρια φωτό, `images` = οι λεπτομέρειες (όσες θες · κενό `[]` = καμία).
- `cat`: `res` κατοικίες · `com` γραφεία · `hosp` φιλοξενία · `retail` καταστήματα
- `status`: `dev` Υπό ανάπτυξη · `des` Υπό μελέτη · `plan` Προγραμματισμένο

Grid, λίστα, carousel, φίλτρα **και** η σελίδα του έργου ενημερώνονται μόνα τους.

### ➖ Διαγραφή έργου
1. Σβήσε τον φάκελο: `projects/<slug>/`
2. Σβήσε τη γραμμή του από το `PROJECTS` (assets/cps-data.js)

Αυτό ήταν — τίποτα άλλο δεν δείχνει σε αυτό το έργο.

## Βελάκι «πίσω» (όλες οι σελίδες εκτός αρχικής)

- Σε `company.html`, `services.html`, `contact.html`, `project.html` υπάρχει **στρογγυλό
  βελάκι** πάνω-αριστερά, κάτω από το nav (`<a class="backtop" data-back href="index.html">`).
  Στην `index.html` **δεν** μπαίνει.
- **Συμπεριφορά:** κλικ → `history.back()` (πίσω στην προηγούμενη σελίδα, π.χ. έργο → λίστα).
  Αν δεν υπάρχει ιστορικό (direct visit), ακολουθεί το `href` → αρχική.
- **Styles:** `assets/cps.css` → `.backtop` (fixed, `z-index:60`, `top:calc(var(--nav-h) + 8px)`,
  `left:clamp(22px,3.4vw,52px)`). Κάτω από 720px γίνεται 38px / `left:14px` και τα
  `.page-head` / `#pdetail` παίρνουν έξτρα `padding-top` ώστε να μη πατάει ο τίτλος.
- **JS:** τελευταίο IIFE στο `assets/cps.js` (δένει το click). Το label είναι `nav.back`
  (Πίσω / Back) μέσω `data-i18n-aria` + `data-i18n-title`.
- ➕ Σε νέα εσωτερική σελίδα: αντέγραψε το `<a class="backtop" data-back …>` αμέσως μετά το `</header>`.

## Loader (πρώτη φόρτωση)

Overlay με **λευκό φόντο + το λογότυπο (wordmark) + λεπτή γραμμή προόδου**, που
εξαφανίζεται με fade μόλις φορτώσει η σελίδα. Υπάρχει σε **index.html** και **project.html**.

- Markup: `<div class="loader" id="loader">` στην αρχή του `<body>`
- Styles: `assets/cps.css` (`.loader*`, keyframes `loaderLogo`, `loaderBar`, `loaderFallback`)
- Λογική: `assets/cps.js` (πρώτο block) — κρύβει μετά το `load`, με **ελάχιστη διάρκεια 650ms**
  ώστε να μη «αστράφτει», και **δίχτυ ασφαλείας στα 4,5s**
- Όσο είναι ανοιχτό: `html.cps-loading` → `body{overflow:hidden}` (δεν σκρολάρει από κάτω)
- **Fallback χωρίς JS:** CSS animation `loaderFallback` (2,8s) το κρύβει μόνο του
- `prefers-reduced-motion` → χωρίς animations, logo + γραμμή αμέσως ορατά

## Συμπεριφορά στο refresh

`history.scrollRestoration = 'manual'` (inline script στο `<head>` + `assets/cps.js`):

- **Refresh / revisit οποιασδήποτε σελίδας** → ξεκινά **πάντα από την αρχή** (το hero),
  όχι από τη θέση που ήσουν — **ακόμα κι αν το URL έχει `#section`**. Ισχύει και για την
  επιστροφή από σελίδα έργου (bfcache).
- **Διάκριση:** το inline script διαβάζει `performance.getEntriesByType('navigation')[0].type`.
  Αν είναι `reload`, σβήνει το hash (`history.replaceState`) **πριν** διαβαστεί το `<body>`
  (ώστε ο browser να μην «πηδήξει» στην ενότητα) και το `assets/cps.js` κάνει `scrollTo(0,0)`.
  Αν είναι `navigate` (κλικ σε link), το `#section` **τιμάται** κανονικά.
- Στη σελίδα έργου δεν αλλάζει τίποτα άλλο: το `?p=<slug>` κρατά το σωστό έργο.

## Φόρμα επικοινωνίας → email

Η φόρμα του `contact.html` **στέλνει πραγματικά** (δεν ανοίγει πια `mailto:`).
Ρυθμίζεται από ένα config στην κορυφή του `assets/cps.js`:

```js
const FORM = {
  provider: 'formsubmit',   // 'formsubmit' | 'web3forms' | 'formspree'
  to: 'nickatsiouras@yahoo.gr',
  key: ''                   // web3forms: access key · formspree: form id
};
```

- **`formsubmit` (προεπιλογή)** — ΔΩΡΕΑΝ, **χωρίς εγγραφή**; μόνο το `to` email.
  («Setup is easy and free» — δεν υπάρχει paid πλάνο στο formsubmit.co· μόνο anti-spam/
  rate limits. ⚠️ Μη μπερδεύεις με `formsubmit.cc` / `formsubmit.site` που είναι **άλλες**,
  χρεούμενες υπηρεσίες με ίδιο όνομα.)
  ⚠️ Την **1η φορά** που κάποιος θα στείλει αίτημα, το FormSubmit στέλνει email
  ενεργοποίησης στο `to` — **πάτα «Activate Form»** και από κει και πέρα όλα τα
  αιτήματα έρχονται αυτόματα. (Μέχρι τότε ο επισκέπτης βλέπει το μήνυμα σφάλματος
  και του ανοίγει το `mailto:` σαν δίχτυ ασφάλειας.)
- **`web3forms`** — https://web3forms.com → γράψε το email → παίρνεις Access Key →
  `provider:'web3forms'`, `key:'…'`. Δωρεάν **250 submissions/μήνα**, χωρίς λογαριασμό.
- **`formspree`** — https://formspree.io → φτιάξε form → `provider:'formspree'`, `key:'το-id'`.
  Δωρεάν **μόνο 50/μήνα** (για testing)· μετά **$15/μήνα** (Personal). Έχει dashboard/ιστορικό.

**Τεχνικά:** `postForm()` στέλνει `FormData` (multipart) με `Accept: application/json`
→ *απλό* request, **χωρίς CORS preflight** (δουλεύει σε κάθε static host). Η επιτυχία
κρίνεται από το `okJSON()`: web3forms `success:true`, formsubmit `success:"true"`
(αλφαριθμητικό!), formspree `ok:true` / `error`. Αν αποτύχει → μήνυμα + `mailto:`.
Το ίδιο config τροφοδοτεί και τη **Newsletter**. Αν `key`/`to` λείπουν, η φόρμα
λειτουργεί όπως παλιά (μόνο `mailto:`).

## Τι μένει να συμπληρωθεί

- [x] **Διεύθυνση / τηλέφωνο** — ✅ Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος, Λάρισα · **2410 538740**
- [x] **Email** — ✅ `nickatsiouras@yahoo.gr` (στοιχεία, footer, `mailto:` φόρμας)
- [ ] **Facebook / Instagram links** — τα εικονίδια μπήκαν τέρμα δεξιά στο nav, ΑΛΛΑ με `href="#"`
      (σχόλιο `▼▼ ΒΑΛΕ ΕΔΩ ΤΑ ΠΡΑΓΜΑΤΙΚΑ LINKS ▼▼` μέσα στο `.social` σε κάθε σελίδα)
- [ ] **Γ.Ε.ΜΗ.** — placeholder `000000000000` στο footer
- [ ] **Ωράριο** — κρατήθηκε «Δευ – Παρ · 09:00 – 17:00» (δεν μου δόθηκε — πες μου το σωστό)
- [ ] **Πραγματικά έργα** — αντικατάσταση των `assets/works/*.jpg` με φωτογραφίες
      (ίδια ονόματα = μηδέν αλλαγές στον κώδικα) και ενημέρωση του `PROJECTS`
- [ ] **Φόρμα επικοινωνίας** — ✅ δουλεύει με `formsubmit` (χωρίς key) · θέλει **1 κλικ**
      στην ενεργοποίηση του πρώτου email που θα έρθει στο `nickatsiouras@yahoo.gr`
- [ ] Αγγλική έκδοση (αν χρειαστεί)

## Τοπικό preview

```
cd cps && python3 -m http.server 8000     # → http://localhost:8000
```

(Δουλεύει και με σκέτο διπλό-κλικ στο `index.html`.)
