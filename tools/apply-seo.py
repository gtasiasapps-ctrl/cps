#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C.P.S — SEO pass (mirrors το pattern του newfoundland project):
  • πλούσιο <head>: title/description/keywords/geo/robots/canonical/hreflang/icons/OG/Twitter
  • JSON-LD: GeneralContractor + WebSite + BreadcrumbList (+ ItemList/FAQPage/ContactPage/AboutPage)
  • robots.txt, sitemap.xml, 404.html, site.webmanifest
Idempotent: αν υπάρχει το marker <!-- SEO:auto --> δεν ξαναπερνάει.
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://cps-solutions.gr"
PHONE = "+302410538740"
MAIL = "cps.redea@gmail.com"
OG_IMG = f"{SITE}/assets/og-image.jpg"
KEYS = ("πολιτικός μηχανικός Λάρισα, μελέτη και κατασκευή έργων Λάρισα, οικοδομική άδεια Λάρισα, "
        "ανακαίνιση Λάρισα, διακόσμηση εσωτερικών χώρων Λάρισα, interior design Λάρισα, "
        "real estate development Λάρισα, ενεργειακή αναβάθμιση Λάρισα, θερμομόνωση, BREEAM, "
        "τεχνικό γραφείο Λάρισα, κατασκευαστική εταιρεία Λάρισα, επίβλεψη έργων, στατική μελέτη, "
        "C.P.S Complete Project Solutions, CPS Λάρισα, civil engineer Larissa, construction Larissa, "
        "interior design Larissa, energy upgrade Larissa")

PAGES = {
    "index.html": dict(
        title="CPS Solutions Λάρισα",
        desc="Η C.P.S – Complete Project Solutions (Λάρισα, από το 2002) αναλαμβάνει μελέτη, αδειοδότηση, "
             "κατασκευή και διαχείριση έργων: κατοικίες, επαγγελματικοί χώροι, διακόσμηση. Ζητήστε προσφορά.",
        og="CPS Solutions Λάρισα",
        ogd="Πολιτικός μηχανικός, διακόσμηση και ολοκληρωμένες τεχνικές λύσεις έργων — από το 2002 στη Λάρισα.",
        crumb=[("Αρχική", "/")],
    ),
    "company.html": dict(
        title="Η Επιχείρηση | CPS Solutions Λάρισα",
        desc="Από το 2002 στη Λάρισα: ομάδα μηχανικών με εμπειρία στη μελέτη, κατασκευή και διαχείριση έργων. "
             "Τεχνογνωσία σε νέα δομικά υλικά, άρτια διεκπεραίωση, συνέπεια στις παραδόσεις.",
        og="Η Επιχείρηση — CPS Solutions Λάρισα",
        ogd="Μηχανικοί με εμπειρία από τη μελέτη ως τη διαχείριση του έργου. Λάρισα, από το 2002.",
        crumb=[("Αρχική", "/"), ("Η Επιχείρηση", "/company.html")],
        page_type="AboutPage",
    ),
    "services.html": dict(
        title="Υπηρεσίες | CPS Solutions Λάρισα",
        desc="Real Estate Development, Interior Design και ολοκληρωμένες τεχνικές λύσεις: μελέτη, αδειοδότηση, "
             "κατασκευή, επίβλεψη, ενεργειακή αναβάθμιση. Λάρισα & Θεσσαλία.",
        og="Υπηρεσίες — CPS Solutions Λάρισα",
        ogd="Real Estate Development · Interior Design · Νέα δομικά συστήματα & ενεργειακή αναβάθμιση.",
        crumb=[("Αρχική", "/"), ("Υπηρεσίες", "/services.html")],
    ),
    "contact.html": dict(
        title="Επικοινωνία | CPS Solutions Λάρισα — 2410 538740",
        desc="Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος, Λάρισα · Τηλ. 2410 538740 · "
             "cps.redea@gmail.com · Δευ–Παρ 09:00–17:00. Στείλτε το αίτημά σας.",
        og="Επικοινωνία — CPS Solutions Λάρισα",
        ogd="Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος, Λάρισα · 2410 538740 · Δευ–Παρ 09:00–17:00.",
        crumb=[("Αρχική", "/"), ("Επικοινωνία", "/contact.html")],
        page_type="ContactPage",
    ),
    "project.html": dict(
        title="Έργα | CPS Solutions Λάρισα",
        desc="Επερχόμενα έργα της C.P.S στη Λάρισα: κατοικίες, επαγγελματικοί χώροι, φιλοξενία, καταστήματα. "
             "Μελέτη, κατασκευή και διαχείριση έργων από το 2002.",
        og="Έργα — CPS Solutions Λάρισα",
        ogd="Κατοικίες, επαγγελματικοί χώροι, φιλοξενία και καταστήματα — μελέτη, κατασκευή, διαχείριση.",
        crumb=[("Αρχική", "/"), ("Έργα", "/index.html#projects")],
    ),
}

SERVICES = [
    ("Real Estate Development", "Ανάπτυξη ακινήτων από το μηδέν: ανάλυση σκοπιμότητας, αρχιτεκτονική και στατική μελέτη, αδειοδοτήσεις, κατασκευή και επίβλεψη, παράδοση."),
    ("Interior Design / Διακόσμηση", "Σχεδιασμός εσωτερικών χωρών: concept και διάταξη, υλικά και φωτισμός, 3D απεικονίσεις, επίπλωση και επίβλεψη υλοποίησης."),
    ("Νέα δομικά συστήματα & Ενεργειακή αναβάθμιση", "Συστήματα υψηλής θερμομόνωσης, ενεργειακή αναβάθμιση κελύφους, BREEAM / βιώσιμη κατασκευή, πιστοποιημένα υλικά."),
    ("Μελέτες & Αδειοδοτήσεις", "Αρχιτεκτονική, στατική και ενεργειακή μελέτη, έκδοση οικοδομικών αδειών και πλήρης διεκπεραίωση διαδικασιών."),
]

FAQS = [
    ("Πώς ξεκινάει ένα έργο μαζί σας;",
     "Με μια πρώτη συνάντηση όπου καταγράφουμε τις ανάγκες σας. Ακολουθεί η ανάλυση σκοπιμότητας, η μελέτη, "
     "οι αδειοδοτήσεις, η κατασκευή και η επίβλεψη, μέχρι την παράδοση του έργου."),
    ("Αναλαμβάνετε την οικοδομική άδεια;",
     "Ναι. Αναλαμβάνουμε ολόκληρη τη διαδικασία αδειοδότησης — αρχιτεκτονική και στατική μελέτη, "
     "ενεργειακή μελέτη και όλες τις απαιτούμενες εγκρίσεις."),
    ("Κάνετε ανακαινίσεις και διακόσμηση;",
     "Ναι. Αναλαμβάνουμε ανακαινίσεις κατοικιών και επαγγελματικών χώρων, με interior design, "
     "3D απεικονίσεις και επίβλεψη της υλοποίησης."),
    ("Πόσο κοστίζει μια μελέτη ή ένα έργο;",
     "Το κόστος εξαρτάται από τα τετραγωνικά, τη χρήση του χώρου και τις μελέτες που απαιτούνται. "
     "Μετά την πρώτη συνάντηση λαμβάνετε αναλυτική προσφορά — χωρίς δέσμευση."),
    ("Αναλαμβάνετε ενεργειακή αναβάθμιση;",
     "Ναι. Εφαρμόζουμε συστήματα υψηλής θερμομόνωσης, αναβαθμίζουμε το κέλυφος και επιλέγουμε "
     "πιστοποιημένα υλικά, με στόχο τη μείωση της κατανάλωσης."),
    ("Σε ποιες περιοχές δραστηριοποιείστε;",
     "Η έδρα μας είναι στη Λάρισα και αναλαμβάνουμε έργα σε όλη τη Θεσσαλία και την Κεντρική Ελλάδα."),
]

MARK = "SEO:auto"


def business_ld():
    return {
        "@context": "https://schema.org",
        "@type": "GeneralContractor",
        "@id": f"{SITE}/#business",
        "name": "CPS Solutions Λάρισα",
        "alternateName": ["CPS Solutions", "C.P.S – Complete Project Solutions", "C.P.S Λάρισα"],
        "description": "Πολιτικός μηχανικός, διακόσμηση και ολοκληρωμένες τεχνικές λύσεις έργων στη Λάρισα, από το 2002.",
        "url": f"{SITE}/",
        "logo": f"{SITE}/assets/cps-lockup.png",
        "image": OG_IMG,
        "telephone": PHONE,
        "email": MAIL,
        "foundingDate": "2002",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος",
            "addressLocality": "Λάρισα",
            "addressRegion": "Θεσσαλία",
            "postalCode": "41222",
            "addressCountry": "GR",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 39.6390, "longitude": 22.4197},
        "areaServed": [
            {"@type": "City", "name": "Λάρισα"},
            {"@type": "AdministrativeArea", "name": "Θεσσαλία"},
            {"@type": "Country", "name": "Ελλάδα"},
        ],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Wednesday", "Friday"],
             "opens": "09:00", "closes": "14:00"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Wednesday", "Friday"],
             "opens": "18:00", "closes": "21:00"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Tuesday", "Thursday"],
             "opens": "09:00", "closes": "14:00"},
        ],
        "knowsLanguage": ["el", "en"],
        "slogan": "Μελέτη, κατασκευή & διαχείριση έργων",
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Υπηρεσίες C.P.S",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "description": d}}
                for n, d in SERVICES
            ],
        },
    }


def website_ld():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "url": f"{SITE}/",
        "name": "CPS Solutions Λάρισα",
        "inLanguage": ["el", "en"],
        "publisher": {"@id": f"{SITE}/#business"},
    }


def crumbs_ld(crumb):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
            for i, (n, u) in enumerate(crumb)
        ],
    }


def faq_ld():
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": "el",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQS
        ],
    }


def services_ld():
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Υπηρεσίες",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "item": {"@type": "Service", "name": n, "description": d,
                      "provider": {"@id": f"{SITE}/#business"},
                      "areaServed": {"@type": "City", "name": "Λάρισα"}}}
            for i, (n, d) in enumerate(SERVICES)
        ],
    }


def ld_script(obj):
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2) + '\n</script>')


def head_block(p, file):
    canon = SITE + ("/" if file == "index.html" else "/" + file)
    return f"""<!-- {MARK} -->
<title>{p['title']}</title>
<meta name="description" content="{p['desc']}" />
<meta name="keywords" content="{KEYS}" />
<meta name="author" content="C.P.S – Complete Project Solutions" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
<meta name="theme-color" content="#ffffff" />
<meta name="language" content="el" />
<meta name="geo.region" content="GR-42" />
<meta name="geo.placename" content="Λάρισα, Θεσσαλία" />
<meta name="geo.position" content="39.6390;22.4197" />
<meta name="ICBM" content="39.6390, 22.4197" />
<link rel="canonical" href="{canon}" />
<link rel="alternate" hreflang="el" href="{canon}" />
<link rel="alternate" hreflang="en" href="{canon}?lang=en" />
<link rel="alternate" hreflang="x-default" href="{canon}" />
<link rel="sitemap" type="application/xml" title="Sitemap" href="sitemap.xml" />
<link rel="icon" href="favicon.ico" sizes="any" />
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png" />
<link rel="icon" type="image/png" sizes="96x96" href="assets/favicon-96x96.png" />
<link rel="icon" type="image/png" sizes="192x192" href="assets/favicon-192x192.png" />
<link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png" />
<link rel="manifest" href="site.webmanifest" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="CPS Solutions Λάρισα" />
<meta property="og:locale" content="el_GR" />
<meta property="og:locale:alternate" content="en_US" />
<meta property="og:title" content="{p['og']}" />
<meta property="og:description" content="{p['ogd']}" />
<meta property="og:url" content="{canon}" />
<meta property="og:image" content="{OG_IMG}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="C.P.S – Complete Project Solutions, Λάρισα" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{p['og']}" />
<meta name="twitter:description" content="{p['ogd']}" />
<meta name="twitter:image" content="{OG_IMG}" />
<meta name="google-site-verification" content="" />"""


def main():
    for file, p in PAGES.items():
        f = ROOT / file
        s = f.read_text(encoding="utf-8")
        if MARK in s:
            print("skip (έχει ήδη SEO):", file)
            continue
        # 1) πρώτα σβήνουμε τις παλιές γραμμές (title θα αντικατασταθεί με το block)
        s = re.sub(r'\n<meta name="description"[^>]*>', "", s, count=1)
        s = re.sub(r'\n<meta name="theme-color"[^>]*>', "", s, count=1)
        s = re.sub(r'\n<link rel="icon" href="assets/cps-wordmark\.png" />', "", s, count=1)
        # μετά αντικαθιστούμε το <title> με ολόκληρο το SEO block
        s = re.sub(r"<title>.*?</title>", head_block(p, file), s, count=1, flags=re.S)

        # 2) JSON-LD πριν το </head>
        lds = [ld_script(business_ld()), ld_script(website_ld()), ld_script(crumbs_ld(p["crumb"]))]
        if p.get("page_type"):
            lds.append(ld_script({
                "@context": "https://schema.org", "@type": p["page_type"],
                "@id": SITE + "/" + file, "url": SITE + "/" + file,
                "isPartOf": {"@id": f"{SITE}/#website"},
                "about": {"@id": f"{SITE}/#business"},
                "inLanguage": "el",
            }))
        if file == "services.html":
            lds += [ld_script(services_ld()), ld_script(faq_ld())]
        s = s.replace("</head>", "\n".join(lds) + "\n</head>", 1)
        f.write_text(s, encoding="utf-8")
        print("SEO head + JSON-LD →", file)

    # 3) διπλό <section id="services"> στο services.html
    sf = ROOT / "services.html"
    s = sf.read_text(encoding="utf-8")
    if s.count('<section id="services">\n<section id="services">'):
        s = s.replace('<section id="services">\n<section id="services">', '<section id="services">', 1)
        sf.write_text(s, encoding="utf-8")
        print("fix: διπλό <section id=\"services\">")


if __name__ == "__main__":
    main()
