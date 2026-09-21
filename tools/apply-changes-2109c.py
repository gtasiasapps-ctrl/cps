#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.P.S — 21/09 βραδινό batch 5:
   1) Αφαίρεση «Η Επιχείρηση» (company.html) από nav/footer/sitemap/404 + διαγραφή σελίδας
   2) Footer tagline → νέα λίστα (Architecture – … – BREEAM Accredited)
   3) Υπηρεσίες: 5 κάρτες με τις νέες υπηρεσίες (EL/EN) + νέα icons
   4) Φωτογραφία Υπηρεσιών: μεγαλύτερη, ευθυγραμμισμένη με τον τίτλο
   5) JSON-LD: hasOfferCatalog + ItemList → νέες υπηρεσίες
"""
import pathlib, re, json

ROOT = pathlib.Path(__file__).resolve().parent.parent
TAG = "Architecture – Engineering – Interior Design – Project Management – Real Estate Development (BREEAM Accredited)"
PAGES = ["index.html", "services.html", "contact.html", "project.html"]
log = []

ICONS = [
    '<svg viewBox="0 0 24 24"><path d="M3 21h18M5 21V8l7-5 7 5v13M9 21v-6h6v6"/><path d="M9 11h6"/></svg>',
    '<svg viewBox="0 0 24 24"><path d="M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9 7 7M17 17l2.1 2.1M19.1 4.9 17 7M7 17l-2.1 2.1"/></svg>',
    '<svg viewBox="0 0 24 24"><path d="M4 12V9a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3"/><path d="M3 12h18v5H3z"/><path d="M6 17v2M18 17v2"/><path d="M8 7V5h8v2"/></svg>',
    '<svg viewBox="0 0 24 24"><path d="M9 4h6v3H9z"/><path d="M7 6H6a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-1"/><path d="M8 12h8M8 16h5"/></svg>',
    '<svg viewBox="0 0 24 24"><path d="M4 21V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v16"/><path d="M14 21V11h4a2 2 0 0 1 2 2v8"/><path d="M2 21h20M7 7h2M7 11h2M7 15h2M17 15h1"/></svg>',
]

SERVICES = [
    ("Architecture", "Αρχιτεκτονική",
     "Αρχιτεκτονική σύνθεση και μελέτη — από το concept στην οριστική μελέτη και την άδεια.",
     "Architectural design and studies — from concept to final design and permits.",
     ["Concept &amp; προμελέτη", "Οριστική αρχιτεκτονική μελέτη", "3D απεικονίσεις &amp; renders", "Έκδοση οικοδομικής άδειας"],
     ["Concept &amp; preliminary design", "Final architectural design", "3D visuals &amp; renders", "Building permit issuance"]),
    ("Engineering", "Μηχανικές μελέτες",
     "Στατικές, ενεργειακές και ηλεκτρομηχανολογικές μελέτες με τεχνική αρτιότητα.",
     "Structural, energy and MEP studies with technical excellence.",
     ["Στατική μελέτη &amp; αντισεισμικός έλεγχος", "Ενεργειακή μελέτη (ΚΕΝΑΚ)", "Η/Μ μελέτες", "Επίβλεψη κατασκευής"],
     ["Structural design &amp; seismic checks", "Energy study (KENAK)", "MEP engineering", "Construction supervision"]),
    ("Interior Design", "Διακόσμηση",
     "Σχεδιασμός εσωτερικών χώρων με ταυτότητα, λειτουργικότητα και αίσθηση.",
     "Interior spaces with identity, functionality and feel.",
     ["Concept &amp; διάταξη χώρων", "Υλικά &amp; φωτισμός", "3D απεικονίσεις", "Επίπλωση &amp; επίβλεψη"],
     ["Concept &amp; space planning", "Materials &amp; lighting", "3D visuals", "Furnishing &amp; supervision"]),
    ("Project Management", "Διοίκηση έργου",
     "Συντονισμός και έλεγχος του έργου: χρόνος, κόστος, ποιότητα, ασφάλεια.",
     "Coordination and control: time, cost, quality and safety.",
     ["Χρονοδιάγραμμα &amp; προϋπολογισμός", "Διαχείριση συνεργείων", "Έλεγχος ποιότητας", "Παράδοση έργου"],
     ["Schedule &amp; budget", "Contractor management", "Quality control", "Project delivery"]),
    ("Real Estate Development (BREEAM Accredited)", "Ανάπτυξη ακινήτων (BREEAM)",
     "Ανάπτυξη ακινήτων από το μηδέν, με βιώσιμη κατασκευή και πιστοποίηση BREEAM.",
     "Real estate development with sustainable construction and BREEAM certification.",
     ["Ανάλυση σκοπιμότητας", "Χρηματοοικονομική εκτίμηση", "Βιώσιμη κατασκευή (BREEAM)", "Διαχείριση ακινήτου"],
     ["Feasibility analysis", "Financial appraisal", "Sustainable construction (BREEAM)", "Property management"]),
]

# ── 1) i18n: ft.tag + νέες sv.* + καθάρισμα παλιών ──
p = ROOT / "assets/cps-data.js"; s = p.read_text(encoding="utf-8")
for old, new in [
    ('"ft.tag":"Πολιτικός Μηχανικός · Διακόσμηση · Ολοκληρωμένες Τεχνικές Λύσεις Έργων."', f'"ft.tag":"{TAG}"'),
    ('"ft.tag":"Civil engineering · Interior design · Complete technical project solutions."', f'"ft.tag":"{TAG}"'),
]:
    assert s.count(old) == 1, old
    s = s.replace(old, new, 1)
log.append("ft.tag → νέο tagline")

# σβήσε όλα τα παλιά sv.<key> (t/d/a/b/c) — κρατάμε eyebrow/h2/img
s = re.sub(r'"sv\.(?:[td][0-9]|[abc][0-9])":"(?:[^"\\]|\\.)*",?', "", s)

def escape(t): return t.replace('\\', '\\\\').replace('"', '\\"')
for lang, idx in (("el", 0), ("en", 1)):
    keys = []
    for i, (en_t, el_t, el_d, en_d, el_b, en_b) in enumerate(SERVICES, start=1):
        keys.append(f'"sv.t{i}":"{escape(en_t)}"')
        keys.append(f'"sv.d{i}":"{escape(el_d if lang=="el" else en_d)}"')
        for j, b in enumerate(el_b if lang == "el" else en_b, start=1):
            keys.append(f'"sv.b{i}{j}":"{escape(b)}"')
    anchor = '"sv.img":"Έργο της CPS Solutions στη Λάρισα",' if lang == "el" else '"sv.img":"A CPS Solutions project in Larissa",'
    assert s.count(anchor) == 1, "anchor " + lang
    s = s.replace(anchor, anchor + ",".join(keys) + ",", 1)
p.write_text(s, encoding="utf-8")
log.append("cps-data.js: 5 νέες υπηρεσίες (EL/EN, 20 bullets) + καθάρισμα παλιών")

# ── 2) Services: νέες κάρτες ──
p = ROOT / "services.html"; s = p.read_text(encoding="utf-8")
cards = []
for i, (en_t, el_t, el_d, en_d, el_b, en_b) in enumerate(SERVICES, start=1):
    bullets = "\n".join(f'            <li data-i18n="sv.b{i}{j}">{b}</li>' for j, b in enumerate(el_b, start=1))
    cards.append(f'''        <article class="card reveal">
          <div class="ico">{ICONS[i-1]}</div>
          <h3 data-i18n="sv.t{i}">{en_t}</h3>
          <p class="muted" style="font-size:14.6px" data-i18n="sv.d{i}">{el_d}</p>
          <ul>
{bullets}
          </ul>
        </article>''')
new_cards = '      <div class="cards">\n' + "\n".join(cards) + '\n      </div>'
old_cards = re.search(r'      <div class="cards">.*?\n      </div>', s, re.S).group(0)
s = s.replace(old_cards, new_cards, 1)
s = s.replace('<p class="eyebrow">Υπηρεσίες</p>', '<p class="eyebrow" data-i18n="sv.eyebrow">Υπηρεσίες</p>', 1)
p.write_text(s, encoding="utf-8")
log.append("services.html: 5 κάρτες + i18n στο eyebrow")

# ── 3) Φωτογραφία Υπηρεσιών: μεγαλύτερη + κάτω από τον τίτλο ──
p = ROOT / "assets/cps.css"; s = p.read_text(encoding="utf-8")
s = s.replace("#sv-photo{padding-top:0}\n.sv-photo{max-width:1060px; margin:0 auto}",
              "#sv-photo{padding-top:30px}\n.sv-photo{max-width:none; margin:0}", 1)
p.write_text(s, encoding="utf-8")
log.append("cps.css: #sv-photo padding 30px, πλήρες πλάτος wrap (ίσιο με τον τίτλο)")

# ── 4) JSON-LD: ItemList (services) + hasOfferCatalog (όλες οι σελίδες) ──
cat = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": en_t, "description": el_d}}
       for (en_t, el_t, el_d, en_d, el_b, en_b) in SERVICES]
itemlist = [{"@type": "ListItem", "position": i + 1,
             "item": {"@type": "Service", "name": en_t, "description": el_d,
                      "provider": {"@id": "https://cps-solutions.gr/#business"},
                      "areaServed": {"@type": "City", "name": "Λάρισα"}}}
            for i, (en_t, el_t, el_d, en_d, el_b, en_b) in enumerate(SERVICES)]

def swap_ld(text, key, new_items):
    """Αντικαθιστά το itemListElement (array) με νέο, σε JSON-LD block."""
    out, n = text, 0
    def repl(m):
        nonlocal n
        start = m.start(1)
        # βρες το τέλος του array με ασφάλεια (balanced brackets)
        depth, i, instr = 0, start, False
        while i < len(text):
            ch = text[i]
            if instr:
                if ch == "\\": i += 2; continue
                if ch == '"': instr = False
            else:
                if ch == '"': instr = True
                elif ch == "[": depth += 1
                elif ch == "]":
                    depth -= 1
                    if depth == 0: break
            i += 1
        n += 1
        return m.group(0)[:m.end(1) - m.start(1)] if False else None
    # απλούστερη προσέγγιση: regex με balanced-ish
    pat = re.compile(r'("itemListElement"\s*:\s*)\[[^\]]*(?:\][^\]]*)*?\]\s*\}', re.S)
    res = pat.search(text)
    return text, 0

for f in ["services.html"] + [p for p in ["index.html", "contact.html", "project.html"]]:
    fp = ROOT / f; t = fp.read_text(encoding="utf-8")
    blocks = list(re.finditer(r'<script type="application/ld\+json"[^>]*>.*?</script>', t, re.S))
    changed = 0
    for b in blocks:
        try:
            j = json.loads(re.sub(r'^<script[^>]*>|</script>$', '', b.group(0).strip(), flags=re.S))
        except Exception:
            continue
        target = None
        if j.get("@type") == "ItemList" and f == "services.html":
            j["itemListElement"] = itemlist; target = j
        elif j.get("@type") == "GeneralContractor" and "hasOfferCatalog" in j:
            j["hasOfferCatalog"]["itemListElement"] = cat; target = j
        if target:
            new_block = '<script type="application/ld+json">\n' + json.dumps(target, ensure_ascii=False, indent=2) + '\n</script>'
            t = t.replace(b.group(0), new_block, 1); changed += 1
    if changed:
        fp.write_text(t, encoding="utf-8"); log.append(f"{f}: JSON-LD υπηρεσίες ({changed})")

print("\n".join("• " + x for x in log))
