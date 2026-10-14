#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Παίρνει τις πραγματικές φωτογραφίες από τον φάκελο «cps yliko»
και φτιάχνει βελτιστοποιημένα JPEG μέσα σε projects/<slug>/
(cover.jpg + 01.jpg, 02.jpg ... — max 1920px, ποιότητα 78).

    python3 tools/prep-images.py
"""
import os, subprocess, shutil, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "cps yliko")
OUT  = os.path.join(ROOT, "projects")

MAXPX  = "1920"
QUALITY = "78"
IMG_EXT = (".jpg", ".jpeg", ".png", ".heic", ".tif", ".tiff", ".webp")

SKIP_NAMES = {"desktop.ini", "thumbs.db", "qrcode.png"}

# slug -> (υποφάκελος στο «cps yliko», προαιρετικός ακριβής υποφάκελος μέσα)
JOBS = {
    "cafe-detox":            "Cafe DETOX Leptokarya",
    "apartments-giannouli":  "Residential building_Apartments_giannouli larisa",
    "monokatoikia-averof":   "Residential building_MONOKATOIKIA_Averof_Larisa",
    "onera":                 ("Residential building_ONERA_Apartments_Averof_Larisa",
                              "FINAL_ΥΦΟΣ_ presentation_ 04_Concept_02"),
    "anakainisi-loutro":     "Residential_Refurbishment_Λουτρό- Λόκκας Γιώργος",
    "anakainisi-sofita":     "Residential_Refurbishment_διαμερίσματος τύπου σοφίτας_Larisa",
    "kdap-mazi-mou":         "Retail and office building ΚΔΑΠ ΜΑΖΙ ΜΟΥ giannouli larisa",
}

# αρχεία που δεν είναι φωτογραφίες (σχέδια/αρχεία που θέλουμε να προσπεράσουμε)
EXCLUDE_SUBSTR = ["Διαστάσεις μπάνιου"]


def collect(folder):
    files = []
    for name in sorted(os.listdir(folder)):
        low = name.lower()
        if low in SKIP_NAMES:
            continue
        if not low.endswith(IMG_EXT):
            continue
        if any(s.lower() in low for s in EXCLUDE_SUBSTR):
            continue
        p = os.path.join(folder, name)
        if os.path.isfile(p):
            files.append(p)
    return files


def convert(src, dst):
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False).name
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", QUALITY,
                    "-Z", MAXPX, src, "--out", tmp],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.move(tmp, dst)


def main():
    for slug, spec in JOBS.items():
        folder_name, *rest = (spec if isinstance(spec, tuple) else (spec,))
        folder = os.path.join(SRC, folder_name)
        if rest:
            folder = os.path.join(folder, rest[0])
        if not os.path.isdir(folder):
            print("!! λείπει:", folder)
            continue
        photos = collect(folder)
        if not photos:
            print("!! καμία φωτογραφία:", folder)
            continue
        dest = os.path.join(OUT, slug)
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        os.makedirs(dest)
        for i, src in enumerate(photos):
            name = "cover.jpg" if i == 0 else "%02d.jpg" % i
            convert(src, os.path.join(dest, name))
        print("%-22s %2d φωτογραφίες ← %s" % (slug, len(photos), folder_name))


if __name__ == "__main__":
    main()
