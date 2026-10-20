/* After 12 data for the shared table engine (assets/js/paths.js).
   Hand-written and deliberately free of fees and dates (they change yearly). Edit rows in D below. */
(function () {
  var ALL = ["M", "B", "C", "A"];
  var SL = { M: "PCM", B: "PCB", C: "Commerce", A: "Arts" };
  var CATS = ["Engineering & Tech", "Medical & Health", "Science & Research", "Commerce & Finance", "Law", "Arts & Media", "Design & Creative", "Aviation, Sea & Hospitality", "Defence & Govt jobs", "Teaching", "Global & Other paths"];

  // n: name, c: field, s: streams, d: duration text, y: years for sorting, e: how you get in, o: where it leads, x: note, u: key into links (practice link shown under "How you get in")
  var D = [
    { n: "B.E. / B.Tech", c: CATS[0], s: ["M"], d: "4 years", y: 4, e: "JEE Main (NITs, IITs via JEE Advanced, IIITs), state CETs, BITSAT, VITEEE and other private-university tests", o: "Software, civil, mechanical, electrical and electronics roles; M.Tech via GATE, PSU jobs, MBA", x: "Physics and Maths are compulsory at most colleges" },
    { n: "B.Arch (Architecture)", c: CATS[0], s: ["M"], d: "5 years", y: 5, e: "NATA, or JEE Main Paper 2", o: "Architect, urban planner, landscape and interior design", x: "Maths is required" },
    { n: "BCA / B.Sc Computer Science / B.Sc IT", c: CATS[0], s: ["M", "C"], d: "3 to 4 years", y: 3, e: "CUET (UG), university tests such as IPU CET, or merit", o: "Software and web developer, data and cloud roles; MCA or M.Sc", x: "Most colleges ask for Maths in Class 12", u: "cuet" },
    { n: "B.Sc / B.Tech in Data Science & AI", c: CATS[0], s: ["M"], d: "3 to 4 years", y: 3, e: "JEE Main for B.Tech; CUET (UG) or university tests for B.Sc", o: "Data analyst, machine-learning and analytics roles; M.Sc, M.Tech, business analytics", u: "cuet" },

    { n: "MBBS", c: CATS[1], s: ["B"], d: "5.5 years incl. 1-year internship", y: 5.5, e: "NEET (UG), then MCC or state counselling", o: "Doctor; specialist after NEET PG; public health and research" },
    { n: "BDS (Dentistry)", c: CATS[1], s: ["B"], d: "5 years incl. internship", y: 5, e: "NEET (UG), then counselling", o: "Dentist; dental surgeon after MDS" },
    { n: "BAMS / BHMS / BUMS (AYUSH)", c: CATS[1], s: ["B"], d: "5.5 years incl. internship", y: 5.5, e: "NEET (UG), then AYUSH counselling", o: "Ayurveda, homoeopathy or Unani doctor; clinics, hospitals and government AYUSH posts" },
    { n: "B.V.Sc & A.H. (Veterinary)", c: CATS[1], s: ["B"], d: "5 years incl. internship", y: 5, e: "NEET (UG), then counselling", o: "Veterinary doctor; livestock and dairy sector; research" },
    { n: "B.Sc Nursing", c: CATS[1], s: ["B"], d: "4 years", y: 4, e: "State or institute entrance, or merit; rules differ by state", o: "Staff nurse, nurse educator; many work abroad after licensing" },
    { n: "BPT (Physiotherapy)", c: CATS[1], s: ["B"], d: "4.5 years incl. internship", y: 4.5, e: "State or university entrance, or merit", o: "Physiotherapist in hospitals, sports and rehab centres" },
    { n: "B.Pharm", c: CATS[1], s: ["B", "M"], d: "4 years", y: 4, e: "State CETs or merit", o: "Pharmacist, pharma industry, drug regulation; M.Pharm via GPAT" },
    { n: "Allied health (lab technology, radiology, optometry, OT)", c: CATS[1], s: ["B"], d: "3 to 4 years", y: 3, e: "Merit or state and institute entrance", o: "Lab technologist, radiographer, optometrist, hospital technician" },

    { n: "BS-MS (IISER, NISER, IISc)", c: CATS[2], s: ["M", "B"], d: "5 years", y: 5, e: "IISER Aptitude Test (IAT), NEST, JEE Advanced; IISc also accepts JEE Main and NEET", o: "Research scientist, professor, PhD in India or abroad" },
    { n: "B.Stat / B.Math (ISI) and CMI", c: CATS[2], s: ["M"], d: "3 years", y: 3, e: "ISI Admission Test; CMI Entrance Exam", o: "Statistics, data science, research, finance; M.Stat and PhD", x: "Maths-heavy and highly competitive" },
    { n: "B.Sc Mathematics / Statistics", c: CATS[2], s: ["M", "C"], d: "3 years", y: 3, e: "CUET (UG) or merit", o: "Statistician, data analyst, teacher; M.Sc, ISI or CMI, actuarial and finance roles", x: "Maths in Class 12", u: "cuet" },
    { n: "B.Sc (Physics, Chemistry, Biology and others)", c: CATS[2], s: ["M", "B"], d: "3 years (4 with honours)", y: 3, e: "CUET (UG) or merit", o: "M.Sc, PhD, lab and research jobs, teaching, civil services", x: "Subjects must match your Class 12 subjects at most colleges", u: "cuet" },
    { n: "B.Sc Biotechnology / Microbiology / Life Sciences", c: CATS[2], s: ["B"], d: "3 years", y: 3, e: "CUET (UG), university tests or merit", o: "Biotech, pharma and research labs; M.Sc, PhD", x: "A few colleges also accept PCM", u: "cuet" },
    { n: "B.Sc Agriculture / Horticulture / Forestry", c: CATS[2], s: ["B", "M"], d: "4 years", y: 4, e: "CUET (UG) or state agricultural-university tests", o: "Agri-officer, agri-business, research, forest service", u: "cuet" },

    { n: "B.Com / B.Com (Hons)", c: CATS[3], s: ["C"], d: "3 years (4 with honours)", y: 3, e: "CUET (UG) or merit", o: "Accounts, banking, taxation, finance; base for CA, CS, CMA and MBA", x: "Many universities also accept other streams", u: "cuet" },
    { n: "BBA / BMS / BBM", c: CATS[3], s: ALL, d: "3 years", y: 3, e: "CUET (UG), NPAT (NMIMS), SET (Symbiosis) and other university tests", o: "Management trainee, sales and marketing, operations; MBA", u: "cuet" },
    { n: "Integrated MBA (IPM)", c: CATS[3], s: ALL, d: "5 years", y: 5, e: "IPMAT (IIM Indore, IIM Rohtak) and JIPMAT (IIM Bodh Gaya, IIM Jammu)", o: "BBA and MBA in one programme; management careers", x: "Aptitude-based entrance with Quant and verbal sections" },
    { n: "Chartered Accountant (CA)", c: CATS[3], s: ALL, d: "4.5 to 5 years", y: 5, e: "ICAI exams: Foundation, Intermediate, practical training, Final", o: "Audit, tax and finance roles; CFO; own practice", x: "Open to every stream" },
    { n: "Company Secretary (CS)", c: CATS[3], s: ALL, d: "3.5 to 4 years", y: 4, e: "ICSI: CSEET, Executive, Professional", o: "Compliance, corporate law and governance roles" },
    { n: "Cost & Management Accountant (CMA)", c: CATS[3], s: ALL, d: "About 4 years", y: 4, e: "ICMAI: Foundation, Intermediate, Final, with practical training", o: "Costing, management accounting, finance and PSU roles" },
    { n: "ACCA (global accountancy)", c: CATS[3], s: ALL, d: "3 to 4 years", y: 3, e: "ACCA exams; can also be done alongside a degree", o: "Audit, accounting and finance careers in India and abroad" },
    { n: "Actuarial Science", c: CATS[3], s: ["M", "C"], d: "3 to 5 years", y: 4, e: "ACET entrance, then Institute of Actuaries of India exams", o: "Actuary in insurance, pensions and risk", x: "Strong Maths needed; exam-heavy" },
    { n: "BA / B.Sc Economics (Hons)", c: CATS[3], s: ALL, d: "3 to 4 years", y: 3, e: "CUET (UG) or merit", o: "Economist, analyst, banking, consulting; MA Economics, MBA, UPSC", x: "Maths in Class 12 helps and some colleges need it", u: "cuet" },

    { n: "5-year integrated law (BA LLB, BBA LLB, B.Com LLB)", c: CATS[4], s: ALL, d: "5 years", y: 5, e: "CLAT (NLUs), AILET (NLU Delhi), LSAT-India, state law CETs", o: "Advocate, corporate counsel, judicial services, legal advisor" },

    { n: "BA (Hons) in History, Political Science, Sociology, English, Geography and more", c: CATS[5], s: ALL, d: "3 years (4 with honours)", y: 3, e: "CUET (UG) or merit", o: "Civil services, teaching, research, journalism; MA, NET, PhD", x: "Subject requirements vary by college", u: "cuet" },
    { n: "BA / B.Sc Psychology", c: CATS[5], s: ALL, d: "3 years", y: 3, e: "CUET (UG) or merit", o: "Counsellor, HR, research; clinical psychologist after postgraduate study and a licence", u: "cuet" },
    { n: "Journalism & Mass Communication (BJMC)", c: CATS[5], s: ALL, d: "3 years", y: 3, e: "CUET (UG), university or institute tests", o: "Journalist, anchor, content and PR roles, digital media", u: "cuet" },
    { n: "Foreign languages (BA in French, German, Japanese and more)", c: CATS[5], s: ALL, d: "3 years", y: 3, e: "CUET (UG) or university tests", o: "Translator, interpreter, tourism, embassies and global-support roles", u: "cuet" },
    { n: "BSW (Social Work)", c: CATS[5], s: ALL, d: "3 years", y: 3, e: "CUET (UG) or merit", o: "NGO, CSR and development roles; MSW", u: "cuet" },

    { n: "B.Des (Design)", c: CATS[6], s: ALL, d: "4 years", y: 4, e: "UCEED (IITs), NID DAT, NIFT entrance, private-university tests", o: "Product, UX, fashion, communication and interior designer" },
    { n: "BFA / Performing arts (music, dance, theatre)", c: CATS[6], s: ALL, d: "3 to 4 years", y: 3, e: "University entrance plus portfolio or audition", o: "Artist, musician, dancer, theatre and film roles, teaching" },
    { n: "Animation, VFX & Game design", c: CATS[6], s: ALL, d: "3 years", y: 3, e: "Portfolio or institute entrance test", o: "Animator, VFX artist, game designer; studios and OTT" },

    { n: "Hotel Management (BHM)", c: CATS[7], s: ALL, d: "3 to 4 years", y: 3, e: "NCHM JEE, or university and institute tests", o: "Hotels, airlines, cruise lines, events, chef" },
    { n: "Commercial Pilot (CPL)", c: CATS[7], s: ["M"], d: "1.5 to 3 years", y: 2, e: "Flying-school admission, DGCA exams and a Class 1 medical", o: "Airline or charter pilot, flight instructor", x: "Physics and Maths in Class 12; training is costly" },
    { n: "Merchant Navy (B.Tech Marine Engineering, B.Sc Nautical Science)", c: CATS[7], s: ["M"], d: "3 to 4 years", y: 3, e: "IMU CET and other maritime-institute tests", o: "Deck or engine officer on ships; shore-based marine jobs", x: "Medical fitness and eyesight rules apply" },

    { n: "NDA / NA (Army, Navy, Air Force)", c: CATS[8], s: ALL, d: "3 years at NDA, then service academy", y: 3, e: "UPSC NDA/NA exam, then SSB interview and medical", o: "Commissioned officer in the Army, Navy or Air Force", x: "Army wing: any stream. Navy and Air Force wings: Physics and Maths. Age limits apply." },
    { n: "Technical Entry (Army TES, Navy B.Tech Cadet)", c: CATS[8], s: ["M"], d: "4-year degree plus training", y: 4, e: "JEE Main score, then SSB and medical", o: "Technical officer in the Army or Navy" },
    { n: "Agniveer (Army, Navy, Air Force)", c: CATS[8], s: ALL, d: "4-year engagement", y: 4, e: "Online exam, physical tests and medical", o: "Soldier, sailor or airman; some are retained after 4 years under the scheme", x: "Class 10 or 12 depending on role; subject rules differ (Navy SSR needs Maths and Physics)" },
    { n: "SSC CHSL and other Class 12-level government jobs", c: CATS[8], s: ALL, d: "Exam-based job, no course", y: null, e: "SSC CHSL tiers, railway (RRB) and state-police exams", o: "Clerk, assistant, data-entry and postal roles; study further while working" },

    { n: "ITEP (4-year integrated B.Ed)", c: CATS[9], s: ALL, d: "4 years", y: 4, e: "NCET (conducted by NTA)", o: "School teacher; later CTET and state TETs" },
    { n: "D.El.Ed / B.El.Ed (elementary teaching)", c: CATS[9], s: ALL, d: "2 to 4 years", y: 2, e: "State entrance or merit; rules differ by state", o: "Primary-school teacher after TET or CTET" },

    { n: "Undergraduate degree abroad", c: CATS[10], s: ALL, d: "3 to 4 years", y: 3, e: "SAT or ACT (US), IELTS or TOEFL, university applications 9 to 12 months ahead", o: "Global degrees and careers; check total cost, visa and work rules" },
    { n: "Drop year (re-attempt JEE, NEET or CLAT)", c: CATS[10], s: ALL, d: "1 year", y: 1, e: "The same entrance exam again", o: "A second attempt at your first-choice course", x: "Keep a backup admission in hand" },
    { n: "Skill and diploma courses (coding, digital marketing, design, cybersecurity, culinary)", c: CATS[10], s: ALL, d: "3 months to 2 years", y: 1, e: "Open admission, portfolio or interview", o: "Freelance and entry-level jobs; useful alongside a degree" },
    { n: "Apprenticeship, family business or startup", c: CATS[10], s: ALL, d: "Flexible", y: null, e: "Direct hiring or the government apprenticeship portal", o: "Earn while you learn; add a degree later through open learning" }
  ];

  window.PATHS = {
    streams: SL,
    who: { M: "PCM students", B: "PCB students", C: "Commerce students", A: "Arts students" },
    allWho: "all streams", anyLabel: "Any stream", allChip: "All streams",
    cats: CATS, rows: D, track: "after12",
    links: { cuet: { href: "cuet-practice.html", text: "Practise CUET (UG) on this site" } }
  };
})();
