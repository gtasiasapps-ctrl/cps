#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.P.S — 21/09 βραδινές αλλαγές:
   1) Αφαίρεση του newsletter (markup, JS, i18n, CSS)
   2) Ταχυδρομικός κώδικας 41222 σε όλες τις διευθύνσεις (site + JSON-LD)
   3) Νέο ωράριο: Δευ/Τετ/Παρ 09:00-14:00 & 18:00-21:00 · Τρι/Πεμ 09:00-14:00
   4) web3forms access key στη φόρμα (αντί formsubmit)
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKEN = "16876d94-9263-47be-bb3f-5f9882f292ca"
TK = "41222"

PAGES = ["index.html", "company.html", "services.html", "contact.html", "project.html"]

OLD_HOURS = '''  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday"
      ],
      "opens": "09:00",
      "closes": "17:00"
    }
  ],'''

NEW_HOURS = '''  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": [
        "Monday",
        "Wednesday",
        "Friday"
      ],
      "opens": "09:00",
      "closes": "14:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": [
        "Monday",
        "Wednesday",
        "Friday"
      ],
      "opens": "18:00",
      "closes": "21:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": [
        "Tuesday",
        "Thursday"
      ],
      "opens": "09:00",
      "closes": "14:00"
    }
  ],'''

OLD_ADDR = '''    "streetAddress": "Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος",
    "addressLocality": "Λάρισα",
    "addressRegion": "Θεσσαλία",
    "addressCountry": "GR"'''
NEW_ADDR = '''    "streetAddress": "Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος",
    "addressLocality": "Λάρισα",
    "addressRegion": "Θεσσαλία",
    "postalCode": "41222",
    "addressCountry": "GR"'''

log = []

# ── 1) JSON-LD σε όλες τις σελίδες (+ το script) ──
for f in PAGES + ["tools/apply-seo.py"]:
    p = ROOT / f; s = p.read_text(encoding="utf-8")
    n = 0
    if OLD_HOURS in s:
        s = s.replace(OLD_HOURS, NEW_HOURS, 1); n += 1
    elif NEW_HOURS not in s:
        log.append(f"⚠️ {f}: δεν βρέθηκε το παλιό ωράριο")
    if OLD_ADDR in s:
        s = s.replace(OLD_ADDR, NEW_ADDR, 1); n += 1
    elif '"postalCode": "41222"' in s:
        pass
    else:
        log.append(f"⚠️ {f}: δεν βρέθηκε η διεύθυνση")
    p.write_text(s, encoding="utf-8")
    if n: log.append(f"{f}: JSON-LD ενημερώθηκε ({n} αλλαγές)")

# ── 2) Newsletter: markup (contact.html) ──
p = ROOT / "contact.html"; s = p.read_text(encoding="utf-8")
m = re.search(r'\n  <section id="newsletter">.*?\n  </section>\n', s, re.S)
if m:
    s = s[:m.start()] + "\n" + s[m.end():]
    p.write_text(s, encoding="utf-8"); log.append("contact.html: αφαιρέθηκε η ενότητα newsletter")
else:
    log.append("⚠️ contact.html: δεν βρέθηκε η ενότητα newsletter")

# ── 3) Newsletter: JS ──
p = ROOT / "assets/cps.js"; s = p.read_text(encoding="utf-8")
start = s.index("  const nlForm = document.getElementById('nlForm');")
end = s.index("})();", start)
removed = s[start:end]
assert "nlMsg" in removed and len(removed) < 1500, len(removed)
s = s[:start] + s[end:]
# web3forms token
assert "provider: 'formsubmit'" in s
s = s.replace("""const FORM = {
  provider: 'formsubmit',      // 'formsubmit' (χωρίς key) | 'web3forms' | 'formspree'
  to: CONTACT_EMAIL,           // πού πάνε τα email
  key: ''                      // web3forms: access key · formspree: form id
};""",
f"""const FORM = {{
  provider: 'web3forms',       // 'web3forms' (access key) | 'formsubmit' (χωρίς key) | 'formspree' (form id)
  to: CONTACT_EMAIL,           // (χρησιμοποιείται μόνο από τον provider 'formsubmit')
  key: '{TOKEN}'               // ← web3forms access key
}};""", 1)
p.write_text(s, encoding="utf-8")
log.append(f"cps.js: αφαιρέθηκε ο κώδικας του newsletter · FORM → web3forms ({TOKEN[:8]}…)")

# ── 4) i18n: νέο ωράριο, ΤΚ, αφαίρεση nl.* ──
p = ROOT / "assets/cps-data.js"; s = p.read_text(encoding="utf-8")
reps = [
    ('"ct.v1":"Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος, Λάρισα"',
     '"ct.v1":"Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος, 412 22 Λάρισα"'),
    ('"ct.v1":"Koumoundourou Alexandrou 24, Agios Nikolaos, Larissa"',
     '"ct.v1":"Koumoundourou Alexandrou 24, Agios Nikolaos, 412 22 Larissa"'),
    ('"ct.v4":"Δευ – Παρ · 09:00 – 17:00"',
     '"ct.v4":"Δευ, Τετ, Παρ · 09:00–14:00 & 18:00–21:00 · Τρι, Πεμ · 09:00–14:00"'),
    ('"ct.v4":"Mon – Fri · 09:00 – 17:00"',
     '"ct.v4":"Mon, Wed, Fri · 09:00–14:00 & 18:00–21:00 · Tue, Thu · 09:00–14:00"'),
]
for old, new in reps:
    assert s.count(old) == 1, old
    s = s.replace(old, new, 1)
# αφαίρεση nl.* keys (EL + EN) — είναι σε μία γραμμή το καθένα
for k in ["nl.title", "nl.text", "nl.btn", "nl.err", "nl.ok"]:
    before = s
    s = re.sub(r'"' + k.replace(".", r"\.") + r'":"(?:[^"\\]|\\.)*",?', "", s)
    if s == before: log.append(f"⚠️ nl.{k} δεν βρέθηκε")
p.write_text(s, encoding="utf-8")
log.append("cps-data.js: ΤΚ + νέο ωράριο + αφαίρεση nl.* keys")

# ── 5) CSS: newsletter ──
p = ROOT / "assets/cps.css"; s = p.read_text(encoding="utf-8")
start = s.index("  /* newsletter */")
end = s.index("  footer{")
block = s[start:end]
assert ".nl-form" in block and len(block) < 1200, len(block)
s = s[:start] + s[end:]
s = s.replace(".two-col,.contact-grid,.nl{grid-template-columns:1fr; gap:30px}",
              ".two-col,.contact-grid{grid-template-columns:1fr; gap:30px}")
p.write_text(s, encoding="utf-8")
log.append("cps.css: αφαιρέθηκαν τα styles του newsletter")

# ── 6) contact.html: meta/OG περιγραφές (ΤΚ + ωράριο) ──
p = ROOT / "contact.html"; s = p.read_text(encoding="utf-8")
s = s.replace("Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος, Λάρισα · Τηλ. 2410 538740 · cps.redea@gmail.com · Δευ–Παρ 09:00–17:00. Στείλτε το αίτημά σας.",
              "Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος, 412 22 Λάρισα · Τηλ. 2410 538740 · cps.redea@gmail.com · Δευ/Τετ/Παρ 09:00–14:00 & 18:00–21:00, Τρι/Πεμ 09:00–14:00.")
s = s.replace("Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος, Λάρισα · 2410 538740 · Δευ–Παρ 09:00–17:00.",
              "Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος, 412 22 Λάρισα · 2410 538740 · Δευ/Τετ/Παρ 09:00–14:00 & 18:00–21:00")
p.write_text(s, encoding="utf-8")
log.append("contact.html: meta/OG με ΤΚ + νέο ωράριο")

# ── 7) .gitignore: ο φάκελος form/ (το τοπικό κλειδί) ──
p = ROOT / ".gitignore"; s = p.read_text(encoding="utf-8")
if "form/" not in s:
    s += "\n# τοπικά αρχεία με κλειδιά (δεν ανεβαίνουν)\nform/\n"
    p.write_text(s, encoding="utf-8"); log.append(".gitignore: + form/")

print("\n".join("• " + x for x in log))
