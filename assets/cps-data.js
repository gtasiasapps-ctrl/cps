/* ══════════════════════════════════════════════════════════
   C.P.S — κοινά δεδομένα (κείμενα EL/EN + έργα)
   Φορτώνεται από index.html και project.html
   ══════════════════════════════════════════════════════════ */
const I18N = {
  el: {
    "nav.home":"Αρχική","nav.company":"Η Επιχείρηση","nav.services":"Υπηρεσίες","nav.projects":"Έργα",
    "nav.back":"Πίσω","nav.contact":"Επικοινωνία","nav.cta":"Ζητήστε προσφορά","co.line":"Architecture – Engineering – Interior Design – Project Management – Real Estate Development (BREEAM Accredited)",
    "st.kicker":"Οι πελάτες μας περιμένουν","st.big":"Το άρτιο","st.sub":"Αυτό επιδιώκουμε σε κάθε έργο",
    "k1b":"Πολιτικός Μηχανικός","k1s":"Μελέτη, κατασκευή & επίβλεψη έργων",
    "k2b":"Διακόσμηση","k2s":"Εσωτερικοί χώροι, υλικά & φωτισμός",
    "k3b":"Από το 2002","k3s":"Λάρισα · Ολοκληρωμένες τεχνικές λύσεις",
    "co.eyebrow":"Η Επιχείρηση",
    "co.h2":"Μηχανικοί με εμπειρία, από τη μελέτη ως τη διαχείριση του έργου",
    "co.p1":"Η <b>C.P.S – Complete Project Solutions</b> ιδρύθηκε στη Λάρισα το 2002 από μία ομάδα μηχανικών με πολυετή εμπειρία στη μελέτη, κατασκευή και διαχείριση έργων, κατοικιών και επαγγελματικών χώρων.",
    "co.p2":"Η εταιρία παρέχει ευρύ φάσμα υπηρεσιών και είναι σε θέση να ικανοποιήσει οποιαδήποτε ανάγκη βασίζεται στην από κοινού με τον πελάτη ανίχνευση και καταγραφή των αναγκών του — τόσο στο στάδιο της μελέτης όσο και κατά τη διάρκεια της κατασκευής.",
    "co.p3":"Βασικός μας στόχος είναι η άρτια διεκπεραίωση των έργων, με ευέλικτες οικονομικές προτάσεις και συνέπεια στην παράδοσή τους, εντός των προαπαιτούμενων χρονικών ορίων.",
    "co.f1":"Τεχνογνωσία σε νέα δομικά υλικά","co.f2":"Μοντέρνες σχεδιαστικές ιδέες",
    "co.f3":"Σύγχρονη αντίληψη κατασκευαστικών δεδομένων","co.f4":"Ποιότητα κατασκευής",
    "co.f5":"Συλλογική εργασία","co.f6":"Ορθολογική οικονομική διαχείριση",
    "sv.img":"Έργο της CPS Solutions στη Λάρισα","sv.t1":"Architecture","sv.d1":"Αρχιτεκτονική σύνθεση και μελέτη — από το concept στην οριστική μελέτη και την άδεια.","sv.b11":"Concept &amp; προμελέτη","sv.b12":"Οριστική αρχιτεκτονική μελέτη","sv.b13":"3D απεικονίσεις &amp; renders","sv.b14":"Έκδοση οικοδομικής άδειας","sv.t2":"Engineering","sv.d2":"Στατικές, ενεργειακές και ηλεκτρομηχανολογικές μελέτες με τεχνική αρτιότητα.","sv.b21":"Στατική μελέτη &amp; αντισεισμικός έλεγχος","sv.b22":"Ενεργειακή μελέτη (ΚΕΝΑΚ)","sv.b23":"Η/Μ μελέτες","sv.b24":"Επίβλεψη κατασκευής","sv.t3":"Interior Design","sv.d3":"Σχεδιασμός εσωτερικών χώρων με ταυτότητα, λειτουργικότητα και αίσθηση.","sv.b31":"Concept &amp; διάταξη χώρων","sv.b32":"Υλικά &amp; φωτισμός","sv.b33":"3D απεικονίσεις","sv.b34":"Επίπλωση &amp; επίβλεψη","sv.t4":"Project Management","sv.d4":"Συντονισμός και έλεγχος του έργου: χρόνος, κόστος, ποιότητα, ασφάλεια.","sv.b41":"Χρονοδιάγραμμα &amp; προϋπολογισμός","sv.b42":"Διαχείριση συνεργείων","sv.b43":"Έλεγχος ποιότητας","sv.b44":"Παράδοση έργου","sv.t5":"Real Estate Development (BREEAM Accredited)","sv.d5":"Ανάπτυξη ακινήτων από το μηδέν, με βιώσιμη κατασκευή και πιστοποίηση BREEAM.","sv.b51":"Ανάλυση σκοπιμότητας","sv.b52":"Χρηματοοικονομική εκτίμηση","sv.b53":"Βιώσιμη κατασκευή (BREEAM)","sv.b54":"Διαχείριση ακινήτου","sv.eyebrow":"Υπηρεσίες","sv.h2":"Ολοκληρωμένες λύσεις για κάθε χώρο",
    
    
    
    
    
    
    
    
    
    "pr.eyebrow":"Έργα","pr.h2":"Επερχόμενα έργα","pr.list":"Όλα τα επερχόμενα έργα",
    "pr.note":"Ενδεικτικά έργα (demo) — θα αντικατασταθούν με τις πραγματικές φωτογραφίες.",
    "pr.f.all":"Όλα","pr.f.res":"Κατοικίες","pr.f.com":"Επαγγελματικοί χώροι","pr.f.hosp":"Φιλοξενία","pr.f.retail":"Καταστήματα",
    "ct.eyebrow":"Επικοινωνία","ct.h2":"Ας μιλήσουμε για το επόμενο έργο σας",
    "ct.k1":"Διεύθυνση","ct.v1":"Κουμουνδούρου Αλέξανδρου 24, Άγιος Νικόλαος, 412 22 Λάρισα","ct.v1b":"","ct.v1b2":"",
    "ct.k2":"Τηλέφωνο","ct.k3":"Email","ct.k4":"Ωράριο","ct.v4":"Δευ, Τετ, Παρ · 09:00–14:00 & 18:00–21:00 · Τρι, Πεμ · 09:00–14:00",
    "fo.name":"Ονοματεπώνυμο","fo.namePh":"π.χ. Γιώργος Παπαδόπουλος","fo.tel":"Τηλέφωνο","fo.email":"Email",
    "fo.topic":"Ενδιαφέρομαι για","fo.o1":"Real Estate Development","fo.o2":"Interior Design",
    "fo.o3":"Νέα δομικά συστήματα / Ενεργειακή αναβάθμιση","fo.o4":"Άλλο",
    "fo.msg":"Μήνυμα","fo.msgPh":"Περιγράψτε σύντομα το έργο ή την ανάγκη σας…",
    "fo.submit":"Αποστολή αιτήματος","fo.note":"Θα λάβετε απάντηση εντός 1 εργάσιμης ημέρας.",
    "fo.err":"Συμπληρώστε τα υποχρεωτικά πεδία.","fo.sending":"Γίνεται αποστολή…","fo.done":"Ευχαριστούμε! Το αίτημά σας στάλθηκε — θα λάβετε απάντηση εντός 1 εργάσιμης ημέρας.","fo.fail":"Κάτι πήγε στραβά. Δοκιμάστε ξανά ή στείλτε μας email.","fo.ok":"Ευχαριστούμε! Ανοίγει το email σας για την αποστολή…",
    "fq.eyebrow":"Συχνές Ερωτήσεις","fq.h2":"Αυτά που μας ρωτούν πιο συχνά","fq.q1":"Πώς ξεκινάει ένα έργο μαζί σας;","fq.a1":"Με μια πρώτη συνάντηση όπου καταγράφουμε τις ανάγκες σας. Ακολουθεί η ανάλυση σκοπιμότητας, η μελέτη, οι αδειοδοτήσεις, η κατασκευή και η επίβλεψη, μέχρι την παράδοση του έργου.","fq.q2":"Αναλαμβάνετε την οικοδομική άδεια;","fq.a2":"Ναι. Αναλαμβάνουμε ολόκληρη τη διαδικασία αδειοδότησης — αρχιτεκτονική και στατική μελέτη, ενεργειακή μελέτη και όλες τις απαιτούμενες εγκρίσεις.","fq.q3":"Κάνετε ανακαινίσεις και διακόσμηση;","fq.a3":"Ναι. Αναλαμβάνουμε ανακαινίσεις κατοικιών και επαγγελματικών χώρων, με interior design, 3D απεικονίσεις και επίβλεψη της υλοποίησης.","fq.q4":"Πόσο κοστίζει μια μελέτη ή ένα έργο;","fq.a4":"Το κόστος εξαρτάται από τα τετραγωνικά, τη χρήση του χώρου και τις μελέτες που απαιτούνται. Μετά την πρώτη συνάντηση λαμβάνετε αναλυτική προσφορά — χωρίς καμία δέσμευση.","fq.q5":"Αναλαμβάνετε ενεργειακή αναβάθμιση;","fq.a5":"Ναι. Εφαρμόζουμε συστήματα υψηλής θερμομόνωσης, αναβαθμίζουμε το κέλυφος και επιλέγουμε πιστοποιημένα υλικά, με στόχο τη μείωση της κατανάλωσης.","fq.q6":"Σε ποιες περιοχές δραστηριοποιείστε;","fq.a6":"Η έδρα μας είναι στη Λάρισα και αναλαμβάνουμε έργα σε όλη τη Θεσσαλία και την Κεντρική Ελλάδα.",
    
    "ft.tag":"Architecture – Engineering – Interior Design – Project Management – Real Estate Development (BREEAM Accredited)",
    "ft.nav":"Πλοήγηση","ft.contact":"Επικοινωνία","ft.city":"Κουμουνδούρου Αλέξανδρου 24, Λάρισα",
    "ft.rights":"© 2026 C.P.S — Complete Project Solutions. Όλα τα δικαιώματα διατηρούνται.",
    "ft.reg":"Γ.Ε.ΜΗ. 186189540000","ft.cookies":"Πολιτική Cookies",
    "pd.back":"Όλα τα επερχόμενα έργα","pd.specs":"Στοιχεία έργου","pd.cat":"Κατηγορία","pd.loc":"Τοποθεσία","pd.status":"Κατάσταση","pd.year":"Παράδοση","pd.note":"Οι εικόνες είναι ενδεικτικές (demo) — θα αντικατασταθούν με τις πραγματικές.","pd.body":"Επερχόμενο έργο — {tag}, {loc}. Η C.P.S – Complete Project Solutions αναλαμβάνει τη μελέτη, την αδειοδότηση, την κατασκευή και τη διαχείριση: από τη σύλληψη της ιδέας έως την παράδοση.","pd.gallery":"Φωτογραφίες","pd.zoom":"Πατήστε σε μια φωτογραφία για μεγέθυνση","pd.prev":"Προηγούμενο έργο","pd.next":"Επόμενο έργο","pd.cta":"Ζητήστε προσφορά για το έργο σας","st.dev":"Υπό ανάπτυξη","st.des":"Υπό μελέτη","st.plan":"Προγραμματισμένο","mail.subject":"Αίτημα από το site","mail.name":"Όνομα","mail.phone":"Τηλέφωνο","mail.email":"Email","mail.topic":"Ενδιαφέρον"
  },
  en: {
    "nav.home":"Home","nav.company":"The Company","nav.services":"Services","nav.projects":"Projects",
    "nav.back":"Back","nav.contact":"Contact","nav.cta":"Request a quote","co.line":"Architecture – Engineering – Interior Design – Project Management – Real Estate Development (BREEAM Accredited)",
    "st.kicker":"Our clients expect","st.big":"The flawless","st.sub":"It is what we strive for in every project",
    "k1b":"Civil Engineer","k1s":"Design, construction & supervision",
    "k2b":"Interior Design","k2s":"Interiors, materials & lighting",
    "k3b":"Since 2002","k3s":"Larissa · Complete technical solutions",
    "co.eyebrow":"The Company",
    "co.h2":"Engineers with experience, from design to project management",
    "co.p1":"<b>C.P.S – Complete Project Solutions</b> was founded in Larissa in 2002 by a team of engineers with long-standing experience in the design, construction and management of projects, residences and commercial spaces.",
    "co.p2":"The company offers a wide range of services and can meet any need, based on identifying and recording the client's requirements together — both at the design stage and during construction.",
    "co.p3":"Our main goal is the flawless delivery of every project, with flexible cost proposals and on-time completion within the required deadlines.",
    "co.f1":"Expertise in new building materials","co.f2":"Modern design ideas",
    "co.f3":"A contemporary understanding of construction data","co.f4":"Construction quality",
    "co.f5":"Teamwork","co.f6":"Rational cost management",
    "sv.img":"A CPS Solutions project in Larissa","sv.t1":"Architecture","sv.d1":"Architectural design and studies — from concept to final design and permits.","sv.b11":"Concept &amp; preliminary design","sv.b12":"Final architectural design","sv.b13":"3D visuals &amp; renders","sv.b14":"Building permit issuance","sv.t2":"Engineering","sv.d2":"Structural, energy and MEP studies with technical excellence.","sv.b21":"Structural design &amp; seismic checks","sv.b22":"Energy study (KENAK)","sv.b23":"MEP engineering","sv.b24":"Construction supervision","sv.t3":"Interior Design","sv.d3":"Interior spaces with identity, functionality and feel.","sv.b31":"Concept &amp; space planning","sv.b32":"Materials &amp; lighting","sv.b33":"3D visuals","sv.b34":"Furnishing &amp; supervision","sv.t4":"Project Management","sv.d4":"Coordination and control: time, cost, quality and safety.","sv.b41":"Schedule &amp; budget","sv.b42":"Contractor management","sv.b43":"Quality control","sv.b44":"Project delivery","sv.t5":"Real Estate Development (BREEAM Accredited)","sv.d5":"Real estate development with sustainable construction and BREEAM certification.","sv.b51":"Feasibility analysis","sv.b52":"Financial appraisal","sv.b53":"Sustainable construction (BREEAM)","sv.b54":"Property management","sv.eyebrow":"Services","sv.h2":"Complete solutions for every space",
    
    
    
    
    
    
    
    
    
    "pr.eyebrow":"Projects","pr.h2":"Upcoming projects","pr.list":"All upcoming projects",
    "pr.note":"Indicative projects (demo) — to be replaced with the real photographs.",
    "pr.f.all":"All","pr.f.res":"Residential","pr.f.com":"Commercial","pr.f.hosp":"Hospitality","pr.f.retail":"Retail",
    "ct.eyebrow":"Contact","ct.h2":"Let's talk about your next project",
    "ct.k1":"Address","ct.v1":"Koumoundourou Alexandrou 24, Agios Nikolaos, 412 22 Larissa","ct.v1b":"","ct.v1b2":"",
    "ct.k2":"Phone","ct.k3":"Email","ct.k4":"Hours","ct.v4":"Mon, Wed, Fri · 09:00–14:00 & 18:00–21:00 · Tue, Thu · 09:00–14:00",
    "fo.name":"Full name","fo.namePh":"e.g. John Smith","fo.tel":"Phone","fo.email":"Email",
    "fo.topic":"I am interested in","fo.o1":"Real Estate Development","fo.o2":"Interior Design",
    "fo.o3":"New building systems / Energy upgrade","fo.o4":"Other",
    "fo.msg":"Message","fo.msgPh":"Briefly describe your project or need…",
    "fo.submit":"Send request","fo.note":"You will receive a reply within 1 business day.",
    "fo.err":"Please fill in the required fields.","fo.sending":"Sending…","fo.done":"Thank you! Your request has been sent — you will hear from us within 1 business day.","fo.fail":"Something went wrong. Please try again or email us directly.","fo.ok":"Thank you! Opening your email app…",
    "fq.eyebrow":"FAQ","fq.h2":"What we get asked most","fq.q1":"How does a project start?","fq.a1":"With a first meeting where we record your needs. Then comes the feasibility analysis, the design, the permits, the construction and the supervision, through to delivery.","fq.q2":"Do you handle the building permit?","fq.a2":"Yes. We handle the entire licensing process — architectural and structural design, energy studies and all required approvals.","fq.q3":"Do you do renovations and interior design?","fq.a3":"Yes. We take on renovations of homes and commercial spaces, with interior design, 3D visuals and supervision of the works.","fq.q4":"What does a study or a project cost?","fq.a4":"The cost depends on the square metres, the use of the space and the studies required. After the first meeting you receive a detailed quote — with no obligation.","fq.q5":"Do you undertake energy upgrades?","fq.a5":"Yes. We apply high-performance insulation systems, upgrade the building envelope and select certified materials, aiming at lower energy consumption.","fq.q6":"Which areas do you cover?","fq.a6":"We are based in Larissa and undertake projects across Thessaly and Central Greece.",
    
    "ft.tag":"Architecture – Engineering – Interior Design – Project Management – Real Estate Development (BREEAM Accredited)",
    "ft.nav":"Navigation","ft.contact":"Contact","ft.city":"Koumoundourou Alexandrou 24, Larissa",
    "ft.rights":"© 2026 C.P.S — Complete Project Solutions. All rights reserved.",
    "ft.reg":"Reg. no. 186189540000","ft.cookies":"Cookie Policy",
    "pd.back":"All upcoming projects","pd.specs":"Project details","pd.cat":"Category","pd.loc":"Location","pd.status":"Status","pd.year":"Delivery","pd.note":"Images are indicative (demo) — to be replaced with the real ones.","pd.body":"Upcoming project — {tag}, {loc}. C.P.S – Complete Project Solutions handles design, permitting, construction and management: from concept to handover.","pd.gallery":"Photos","pd.zoom":"Click a photo to enlarge","pd.prev":"Previous project","pd.next":"Next project","pd.cta":"Request a quote for your project","st.dev":"In development","st.des":"In design","st.plan":"Planned","mail.subject":"Website enquiry","mail.name":"Name","mail.phone":"Phone","mail.email":"Email","mail.topic":"Interest"
  }
};

const PROJECTS = [
  {slug:'house-pool',        cat:'res',    year:'2026', status:'dev',  dir:'projects/house-pool', cover:'cover.jpg', images:['01.jpg','02.jpg'],
   el:{tag:'Κατοικία',           title:'Μονοκατοικία με πισίνα',    loc:'Λάρισα'},
   en:{tag:'Residence',          title:'House with pool',           loc:'Larissa'}},
  {slug:'retail-store',      cat:'retail', year:'2026', status:'des',  dir:'projects/retail-store', cover:'cover.jpg', images:['01.jpg','02.jpg'],
   el:{tag:'Κατάστημα',          title:'Κατάστημα',                 loc:'Λάρισα'},
   en:{tag:'Retail',             title:'Retail store',              loc:'Larissa'}},
  {slug:'apartments',        cat:'res',    year:'2027', status:'dev',  dir:'projects/apartments', cover:'cover.jpg', images:['01.jpg','02.jpg'],
   el:{tag:'Ανάπτυξη',           title:'Συγκρότημα διαμερισμάτων',  loc:'Λάρισα'},
   en:{tag:'Development',        title:'Apartment complex',         loc:'Larissa'}},
  {slug:'apartment-110',     cat:'res',    year:'2026', status:'des',  dir:'projects/apartment-110', cover:'cover.jpg', images:['01.jpg','02.jpg'],
   el:{tag:'Κατοικία',           title:'Διαμέρισμα 110 τ.μ.',       loc:'Λάρισα'},
   en:{tag:'Residence',          title:'Apartment, 110 m²',         loc:'Larissa'}},
  {slug:'offices-industrial',cat:'com',    year:'2027', status:'plan', dir:'projects/offices-industrial', cover:'cover.jpg', images:['01.jpg','02.jpg'],
   el:{tag:'Γραφεία',            title:'Γραφεία',                   loc:'Βιοτεχνικό Πάρκο'},
   en:{tag:'Offices',            title:'Offices',                   loc:'Industrial Park'}},
  {slug:'hotel-trikala',     cat:'hosp',   year:'2027', status:'dev',  dir:'projects/hotel-trikala', cover:'cover.jpg', images:['01.jpg','02.jpg'],
   el:{tag:'Φιλοξενία',          title:'Ξενοδοχειακός χώρος',       loc:'Τρίκαλα'},
   en:{tag:'Hospitality',        title:'Hotel interiors',           loc:'Trikala'}},
  {slug:'cafe-central',      cat:'hosp',   year:'2026', status:'des',  dir:'projects/cafe-central', cover:'cover.jpg', images:['01.jpg','02.jpg'],
   el:{tag:'Εστίαση',            title:'Café',                      loc:'Κεντρική πλατεία'},
   en:{tag:'F&B',                title:'Café',                      loc:'Central square'}},
  {slug:'restaurant-larissa',cat:'hosp',   year:'2026', status:'dev',  dir:'projects/restaurant-larissa', cover:'cover.jpg', images:['01.jpg','02.jpg'],
   el:{tag:'Εστίαση',            title:'Εστιατόριο',                loc:'Λάρισα'},
   en:{tag:'F&B',                title:'Restaurant',                loc:'Larissa'}},
  {slug:'corporate-offices', cat:'com',    year:'2027', status:'plan', dir:'projects/corporate-offices', cover:'cover.jpg', images:['01.jpg','02.jpg'],
   el:{tag:'Γραφεία',            title:'Γραφεία εταιρείας',         loc:'Λάρισα'},
   en:{tag:'Offices',            title:'Corporate offices',         loc:'Larissa'}},
  {slug:'showroom',          cat:'retail', year:'2026', status:'des',  dir:'projects/showroom', cover:'cover.jpg', images:['01.jpg','02.jpg'],
   el:{tag:'Showroom',           title:'Showroom',                  loc:'Λάρισα'},
   en:{tag:'Showroom',           title:'Showroom',                  loc:'Larissa'}},
  {slug:'hillside',          cat:'res',    year:'2027', status:'dev',  dir:'projects/hillside', cover:'cover.jpg', images:['01.jpg','02.jpg'],
   el:{tag:'Κατοικία',           title:'Κατοικία σε πλαγιά',        loc:'Πήλιο'},
   en:{tag:'Residence',          title:'Hillside residence',        loc:'Pelion'}},
  {slug:'hotel-rooms',       cat:'hosp',   year:'2026', status:'plan', dir:'projects/hotel-rooms', cover:'cover.jpg', images:['01.jpg','02.jpg'],
   el:{tag:'Φιλοξενία',          title:'Δωμάτια ξενοδοχείου',       loc:'Λάρισα'},
   en:{tag:'Hospitality',        title:'Hotel rooms',               loc:'Larissa'}}
];

/* ══════════════════════════════════════════════════════════
   CAROUSEL (hero) — φωτογραφίες μέσα στον φάκελο carousel/
   • CAROUSEL_LOGO : το slide του λογοτύπου — παίζει **ΠΑΝΤΑ ΠΡΩΤΟ**
     μόλις μπει κάποιος στο site (δεν μπαίνει στον πίνακα CAROUSEL).
   • CAROUSEL      : οι υπόλοιπες φωτογραφίες, με τη σειρά που θα παίζουν.
   Άδειο [] → μετά το λογότυπο παίζουν οι καρτέλες των έργων.
   ══════════════════════════════════════════════════════════ */
const CAROUSEL_LOGO = 'logo-banner.jpg';
const CAROUSEL = [
  '01.jpg'
];
