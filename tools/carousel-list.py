#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ξαναγράφει τον πίνακα CAROUSEL στο assets/cps-data.js διαβάζοντας ΟΛΕΣ τις
εικόνες μέσα στον φάκελο carousel/ (εκτός από το logo banner και το _src/).

    python3 tools/carousel-list.py

Έτσι, για να προσθέσεις φωτογραφίες στο hero: ρίξε τες στο carousel/ και τρέξε το.
"""
import os, re

ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDIR   = os.path.join(ROOT, "carousel")
DATAJS   = os.path.join(ROOT, "assets", "cps-data.js")
LOGO     = "logo-banner.jpg"
IMG_EXT  = (".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif")
# θορυβος που αγνοειται
SKIP     = {".ds_store", ".gitkeep"}


def main():
    logo, rest = None, []
    for name in sorted(os.listdir(CARDIR)):
        low = name.lower()
        if low.startswith(".") or low in SKIP:
            continue
        if not low.endswith(IMG_EXT):
            continue
        if "logo" in low and "banner" in low:
            logo = name
            continue
        rest.append(name)

    if not logo:
        logo = LOGO
    body = ",\n".join("  '%s'" % f for f in rest)

    src = open(DATAJS, encoding="utf-8").read()
    new, n = re.subn(
        r"const CAROUSEL_LOGO = '[^']*';\nconst CAROUSEL = \[[^\]]*\];",
        "const CAROUSEL_LOGO = '%s';\nconst CAROUSEL = [\n%s\n];" % (logo, body),
        src, count=1, flags=re.S)
    if not n:
        print("!! δεν βρέθηκε το μπλοκ CAROUSEL στο cps-data.js")
        return
    if new != src:
        open(DATAJS, "w", encoding="utf-8").write(new)
        print("ενημερώθηκε το cps-data.js")
    print("CAROUSEL_LOGO = %s" % logo)
    print("CAROUSEL      = %s" % (", ".join(rest) or "(κενό)"))


if __name__ == "__main__":
    main()
