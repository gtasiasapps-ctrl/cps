#!/usr/bin/env bash
# Δημιουργεί φάκελο για νέο έργο και τυπώνει το snippet για το assets/cps-data.js
# Χρήση:  tools/new-project.sh <slug>       π.χ.  tools/new-project.sh villa-katerini

set -e
cd "$(dirname "$0")/.."          # ρίζα του site

slug="$1"
if [ -z "$slug" ]; then
  echo "Χρήση: tools/new-project.sh <slug>"
  echo "π.χ.   tools/new-project.sh villa-katerini"
  exit 1
fi

dir="projects/$slug"
mkdir -p "$dir"

if [ ! -f "$dir/cover.jpg" ]; then
  cat > "$dir/README.txt" <<'TXT'
Βάλε εδώ τις φωτογραφίες του έργου:

  cover.jpg   ← υποχρεωτικό. Η κύρια φωτογραφία (καρτέλα + carousel).
  01.jpg      ← προαιρετικό. Λεπτομέρειες (όσες θες: 01, 02, 03 ...)
  02.jpg

Μετά πρόσθεσε το έργο στο assets/cps-data.js (δες README.md → «Νέο έργο»).
TXT
fi

echo "✔ Ο φάκελος δημιουργήθηκε: $dir"
echo "  → ρίξε μέσα το cover.jpg (και όποια άλλα: 01.jpg, 02.jpg ...)"
echo
echo "Πρόσθεσε αυτό στο PROJECTS μέσα στο assets/cps-data.js:"
echo
cat <<EOF
  {slug:'$slug', cat:'res', year:'2027', status:'dev',
   dir:'projects/$slug', cover:'cover.jpg', images:['01.jpg','02.jpg'],
   el:{tag:'Κατοικία',  title:'Τίτλος έργου', loc:'Τοποθεσία'},
   en:{tag:'Residence', title:'Project title', loc:'Location'}},
EOF
echo
echo "cat: 'res' (κατοικίες) | 'com' (γραφεία) | 'hosp' (φιλοξενία) | 'retail' (καταστήματα)"
echo "status: 'dev' (υπό ανάπτυξη) | 'des' (υπό μελέτη) | 'plan' (προγραμματισμένο)"
