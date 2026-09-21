#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.P.S — FAQ section (services.html) + CSS + i18n keys (EL/EN)."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

FAQS = [
    ("Πώς ξεκινάει ένα έργο μαζί σας;",
     "Με μια πρώτη συνάντηση όπου καταγράφουμε τις ανάγκες σας. Ακολουθεί η ανάλυση σκοπιμότητας, η μελέτη, "
     "οι αδειοδοτήσεις, η κατασκευή και η επίβλεψη, μέχρι την παράδοση του έργου.",
     "How does a project start?",
     "With a first meeting where we record your needs. Then comes the feasibility analysis, the design, "
     "the permits, the construction and the supervision, through to delivery."),
    ("Αναλαμβάνετε την οικοδομική άδεια;",
     "Ναι. Αναλαμβάνουμε ολόκληρη τη διαδικασία αδειοδότησης — αρχιτεκτονική και στατική μελέτη, "
     "ενεργειακή μελέτη και όλες τις απαιτούμενες εγκρίσεις.",
     "Do you handle the building permit?",
     "Yes. We handle the entire licensing process — architectural and structural design, energy studies "
     "and all required approvals."),
    ("Κάνετε ανακαινίσεις και διακόσμηση;",
     "Ναι. Αναλαμβάνουμε ανακαινίσεις κατοικιών και επαγγελματικών χώρων, με interior design, "
     "3D απεικονίσεις και επίβλεψη της υλοποίησης.",
     "Do you do renovations and interior design?",
     "Yes. We take on renovations of homes and commercial spaces, with interior design, 3D visuals and "
     "supervision of the works."),
    ("Πόσο κοστίζει μια μελέτη ή ένα έργο;",
     "Το κόστος εξαρτάται από τα τετραγωνικά, τη χρήση του χώρου και τις μελέτες που απαιτούνται. "
     "Μετά την πρώτη συνάντηση λαμβάνετε αναλυτική προσφορά — χωρίς καμία δέσμευση.",
     "What does a study or a project cost?",
     "The cost depends on the square metres, the use of the space and the studies required. After the first "
     "meeting you receive a detailed quote — with no obligation."),
    ("Αναλαμβάνετε ενεργειακή αναβάθμιση;",
     "Ναι. Εφαρμόζουμε συστήματα υψηλής θερμομόνωσης, αναβαθμίζουμε το κέλυφος και επιλέγουμε "
     "πιστοποιημένα υλικά, με στόχο τη μείωση της κατανάλωσης.",
     "Do you undertake energy upgrades?",
     "Yes. We apply high-performance insulation systems, upgrade the building envelope and select certified "
     "materials, aiming at lower energy consumption."),
    ("Σε ποιες περιοχές δραστηριοποιείστε;",
     "Η έδρα μας είναι στη Λάρισα και αναλαμβάνουμε έργα σε όλη τη Θεσσαλία και την Κεντρική Ελλάδα.",
     "Which areas do you cover?",
     "We are based in Larissa and undertake projects across Thessaly and Central Greece."),
]

# ── 1) HTML section ──
items = "\n".join(
    f'        <details class="faq-item"><summary data-i18n="fq.q{i+1}">{q}</summary>'
    f'<p data-i18n="fq.a{i+1}">{a}</p></details>'
    for i, (q, a, _, _) in enumerate(FAQS))

section = f"""
  <section id="faq">
    <div class="wrap">
      <p class="eyebrow" data-i18n="fq.eyebrow">Συχνές Ερωτήσεις</p>
      <h2 data-i18n="fq.h2">Αυτά που μας ρωτούν πιο συχνά</h2>
      <div class="faq">
{items}
      </div>
    </div>
  </section>
"""

f = ROOT / "services.html"
s = f.read_text(encoding="utf-8")
if 'id="faq"' not in s:
    anchor = '  <section class="cta-band">'
    assert s.count(anchor) == 1
    s = s.replace(anchor, section + anchor, 1)
    f.write_text(s, encoding="utf-8")
    print("services.html: FAQ section ✅")
else:
    print("services.html: FAQ υπάρχει ήδη")

# ── 2) CSS ──
css = ROOT / "assets/cps.css"
c = css.read_text(encoding="utf-8")
if ".faq-item" not in c:
    c += """
/* ═══════════ FAQ (services.html) ═══════════ */
#faq{padding-top:0}
.faq{max-width:900px; margin:34px auto 0; border-top:1px solid var(--line)}
.faq-item{border-bottom:1px solid var(--line)}
.faq-item summary{
  cursor:pointer; list-style:none; padding:20px 0; display:flex; align-items:center; justify-content:space-between;
  gap:20px; font-size:1.02rem; font-weight:600; color:var(--ink); transition:padding .2s ease;
}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary::after{content:"+"; font-size:19px; line-height:1; color:var(--muted); transition:opacity .2s}
.faq-item[open] summary::after{content:"–"}
.faq-item summary:hover{padding-left:8px}
.faq-item p{margin:0 0 22px; color:var(--muted); font-size:14.8px; max-width:74ch}
@media (max-width:720px){
  .faq-item summary{font-size:.97rem; padding:17px 0}
  .faq-item summary:hover{padding-left:0}
}
"""
    css.write_text(c, encoding="utf-8")
    print("cps.css: FAQ styles ✅")

# ── 3) i18n keys ──
d = ROOT / "assets/cps-data.js"
t = d.read_text(encoding="utf-8")

def keys(lang):
    out = [f'"fq.eyebrow":"Συχνές Ερωτήσεις"' if lang == "el" else '"fq.eyebrow":"FAQ"',
           '"fq.h2":"Αυτά που μας ρωτούν πιο συχνά"' if lang == "el" else '"fq.h2":"What we get asked most"']
    for i, (q, a, qe, ae) in enumerate(FAQS):
        out.append(f'"fq.q{i+1}":{json_esc(qe if lang == "en" else q)}')
        out.append(f'"fq.a{i+1}":{json_esc(ae if lang == "en" else a)}')
    return ",".join(out)

def json_esc(x):
    return '"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"'

anchors = {
    "el": '"nl.text":"Νέα έργα, υλικά και ιδέες — μία φορά τον μήνα, χωρίς spam."',
    "en": '"nl.text":"New projects, materials and ideas — once a month, no spam."',
}
for lang, anc in anchors.items():
    if f'"fq.q1"' in t:
        print("i18n: fq.* υπάρχουν ήδη"); break
    assert t.count(anc) == 1, anc
    t = t.replace(anc, anc + "," + keys(lang), 1)
d.write_text(t, encoding="utf-8")
print("cps-data.js: fq.* keys ✅")
