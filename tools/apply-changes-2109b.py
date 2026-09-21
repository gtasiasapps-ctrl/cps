#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.P.S — 21/09 νύχτα (δεύτερο batch):
   1) Γ.Ε.ΜΗ. 186189540000 (footer + JSON-LD identifier)
   2) Tagline: «Πολιτικός Μηχανικός · Διακόσμηση …» → «Architecture – Engineering – Interior Design
      – Project Management – Real Estate Development (BREEAM Accredited)»
   3) Carousel πιο γρήγορο (3s οι φωτογραφίες, 4s το λογότυπο)
   4) Instagram link instagram.com/cps_redea (+ sameAs στο JSON-LD)
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
GEMI = "186189540000"
TAGLINE = "Architecture – Engineering – Interior Design – Project Management – Real Estate Development (BREEAM Accredited)"
GEMI_EN = f"Reg. no. {GEMI}"
PAGES = ["index.html", "company.html", "services.html", "contact.html", "project.html"]
log = []

# ── 1) i18n: ft.reg, co.line ──
p = ROOT / "assets/cps-data.js"; s = p.read_text(encoding="utf-8")
for old, new, label in [
    ('"ft.reg":"Γ.Ε.ΜΗ. 000000000000"', f'"ft.reg":"Γ.Ε.ΜΗ. {GEMI}"', "ft.reg EL"),
    ('"ft.reg":"Reg. no. 000000000000"', f'"ft.reg":"Reg. no. {GEMI}"', "ft.reg EN"),
    ('"co.line":"Πολιτικός Μηχανικός · Διακόσμηση · Ολοκληρωμένες Τεχνικές Λύσεις Έργων"',
     f'"co.line":"{TAGLINE}"', "co.line EL"),
    ('"co.line":"Civil engineering · Interior design · Complete technical project solutions"',
     f'"co.line":"{TAGLINE}"', "co.line EN"),
]:
    assert s.count(old) == 1, label
    s = s.replace(old, new, 1); log.append("cps-data.js: " + label)
p.write_text(s, encoding="utf-8")

# ── 2) Περιγραφές: «Πολιτικός μηχανικός, διακόσμηση …» → νέα λίστα ──
DESC_NEW = f"{TAGLINE} — Λάρισα, από το 2002."
for f in PAGES + ["tools/apply-seo.py"]:
    p = ROOT / f; s = p.read_text(encoding="utf-8"); n = 0
    # JSON-LD description (ίδιο σε όλες τις σελίδες)
    for old in [
        '"description": "Πολιτικός μηχανικός, διακόσμηση και ολοκληρωμένες τεχνικές λύσεις έργων στη Λάρισα, από το 2002.",',
        '        "description": "Πολιτικός μηχανικός, διακόσμηση και ολοκληρωμένες τεχνικές λύσεις έργων στη Λάρισα, από το 2002.",',
        '        "description": "Πολιτικός μηχανικός, διακόσμηση και ολοκληρωμένες τεχνικές λύσεις έργων στη Λάρισα, από το 2002.",',
    ]:
        if old in s:
            s = s.replace(old, old.split(': "')[0] + f': "{DESC_NEW}",', 1); n += 1; break
    # og/twitter description του index
    old_og = 'content="Πολιτικός μηχανικός, διακόσμηση και ολοκληρωμένες τεχνικές λύσεις έργων — από το 2002 στη Λάρισα."'
    if old_og in s:
        s = s.replace(old_og, f'content="{TAGLINE} — από το 2002 στη Λάρισα."'); n += 1
    # ogd του generate script
    old_ogd = 'ogd="Πολιτικός μηχανικός, διακόσμηση και ολοκληρωμένες τεχνικές λύσεις έργων — από το 2002 στη Λάρισα.",'
    if old_ogd in s:
        s = s.replace(old_ogd, f'ogd="{TAGLINE} — από το 2002 στη Λάρισα.",'); n += 1
    if n:
        p.write_text(s, encoding="utf-8"); log.append(f"{f}: {n} περιγραφές → νέο tagline")

# ── 3) Instagram link (5 σελίδες) ──
IG = 'https://www.instagram.com/cps_redea/'
for f in PAGES:
    p = ROOT / f; s = p.read_text(encoding="utf-8")
    old = '''<a href="#" target="_blank" rel="noopener" aria-label="Instagram" title="Instagram">'''
    if old in s:
        s = s.replace(old, f'<a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram" title="Instagram">', 1)
        s = s.replace("<!-- ▼▼ ΒΑΛΕ ΕΔΩ ΤΑ ΠΡΑΓΜΑΤΙΚΑ LINKS (facebook / instagram) ▼▼ -->",
                      "<!-- ▼▼ ΒΑΛΕ ΕΔΩ ΤΟ FACEBOOK LINK (το Instagram είναι συνδεδεμένο) ▼▼ -->", 1)
        p.write_text(s, encoding="utf-8"); log.append(f"{f}: Instagram → {IG}")
    else:
        log.append(f"⚠️ {f}: δεν βρέθηκε το Instagram link")

# ── 4) JSON-LD: identifier ΓΕΜΗ + sameAs Instagram ──
for f in PAGES + ["tools/apply-seo.py"]:
    p = ROOT / f; s = p.read_text(encoding="utf-8"); n = 0
    if '"slogan"' in s and '"sameAs"' not in s:
        if f.endswith(".py"):
            s = s.replace('        "slogan": "Μελέτη, κατασκευή & διαχείριση έργων",',
                          '        "slogan": "Μελέτη, κατασκευή & διαχείριση έργων",\n'
                          f'        "identifier": [{{"@type": "PropertyValue", "name": "Γ.Ε.ΜΗ.", "value": "{GEMI}"}}],\n'
                          f'        "sameAs": ["{IG}"],', 1); n += 1
        else:
            s = s.replace('  "slogan": "Μελέτη, κατασκευή & διαχείριση έργων",',
                          '  "slogan": "Μελέτη, κατασκευή & διαχείριση έργων",\n'
                          f'  "identifier": [{{"@type": "PropertyValue", "name": "Γ.Ε.ΜΗ.", "value": "{GEMI}"}}],\n'
                          f'  "sameAs": ["{IG}"],', 1); n += 1
    if n: p.write_text(s, encoding="utf-8"); log.append(f"{f}: JSON-LD identifier + sameAs")

# ── 5) Carousel: πιο γρήγορο ──
p = ROOT / "assets/cps.js"; s = p.read_text(encoding="utf-8")
old_dur = """  // Το slide του λογοτύπου μένει λίγο παραπάνω στην οθόνη
  const DUR = i => (SLIDES[i] && SLIDES[i].logo ? 6500 : 4600);"""
new_dur = """  // Διάρκεια κάθε slide (γρήγορο: 4s το λογότυπο, 3s οι φωτογραφίες)
  const DUR_LOGO = 4000, DUR_SLIDE = 3000;
  const DUR = i => (SLIDES[i] && SLIDES[i].logo ? DUR_LOGO : DUR_SLIDE);"""
assert s.count(old_dur) == 1, "DUR block"
s = s.replace(old_dur, new_dur, 1)
p.write_text(s, encoding="utf-8"); log.append("cps.js: carousel 3s/4s (DUR_LOGO/DUR_SLIDE)")

# ── 6) CSS: πιο γρήγορο crossfade + Ken Burns ──
p = ROOT / "assets/cps.css"; s = p.read_text(encoding="utf-8")
s = s.replace("  .slide{position:absolute; inset:0; opacity:0; transition:opacity 1.15s ease}",
              "  .slide{position:absolute; inset:0; opacity:0; transition:opacity .8s ease}", 1)
s = s.replace("  .slide img{width:100%; height:100%; object-fit:cover; transform:scale(1.06); transition:transform 8s linear}",
              "  .slide img{width:100%; height:100%; object-fit:cover; transform:scale(1.06); transition:transform 5.5s linear}", 1)
s = s.replace("  .reduce-motion .slide{transition:opacity .5s ease}",
              "  .reduce-motion .slide{transition:opacity .4s ease}", 1)
p.write_text(s, encoding="utf-8"); log.append("cps.css: crossfade .8s, Ken Burns 5.5s")

print("\n".join("• " + x for x in log))
