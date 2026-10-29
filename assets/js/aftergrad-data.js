/* After Graduation data for the shared table engine (assets/js/paths.js).
   Hand-written and deliberately free of fees and dates (they change yearly). Edit rows in D below. */
(function () {
  // degree backgrounds: E engineering, S science, C commerce & management, A arts & humanities, M medical & health, L law
  var ALL = ["E", "S", "C", "A", "M", "L"];
  var SL = { E: "Engineering", S: "Science", C: "Commerce / BBA", A: "Arts", M: "Medical", L: "Law" };
  var CATS = ["Management (MBA)", "Engineering & Tech", "Science & Research", "Civil services & Govt jobs", "Banking & Finance", "Law", "Medical & Health", "Teaching", "Defence", "Arts, Media & Design", "Jobs, Skills & Abroad"];

  // n: name, c: field, s: degrees, d: duration text, y: years for sorting (null = job, no course), e: how you get in, o: where it leads, x: note, u: key into links
  var D = [
    { n: "MBA / PGDM", c: CATS[0], s: ALL, d: "2 years", y: 2, e: "CAT (IIMs and most top B-schools), XAT, CMAT, MAT, SNAP, NMAT, GMAT, then group discussion or written ability test and interview", o: "Management roles in marketing, finance, operations, HR, consulting and product", x: "Many students take the exam in their final year of college", u: "cat" },
    { n: "Specialised PGDM (HR, rural management, business analytics)", c: CATS[0], s: ALL, d: "2 years", y: 2, e: "XAT, CAT and institute-specific tests and interviews", o: "HR and industrial relations, rural and development management, analytics roles", u: "cat" },
    { n: "Executive MBA", c: CATS[0], s: ALL, d: "1 to 2 years", y: 1.5, e: "Several years of work experience, plus GMAT, GRE or an institute test and interview", o: "Senior and general-management roles", x: "Not for fresh graduates" },
    { n: "Master's in Management or MBA abroad", c: CATS[0], s: ALL, d: "1 to 2 years", y: 1.5, e: "GMAT or GRE, IELTS or TOEFL, and university applications", o: "Management careers in India or abroad; check total cost, visa and work rules" },

    { n: "M.Tech / M.E.", c: CATS[1], s: ["E"], d: "2 years", y: 2, e: "GATE (IITs, NITs, IIITs and others), state PG entrance tests, university tests", o: "R&D, design and specialist engineering roles, teaching, PhD" },
    { n: "PSU jobs through GATE", c: CATS[1], s: ["E"], d: "Exam-based job, no course", y: null, e: "GATE score, then interview or group discussion at the PSU", o: "Engineer or management-trainee posts at public-sector companies", x: "Only some PSUs recruit through GATE each year; check their notices" },
    { n: "UPSC Engineering Services (ESE)", c: CATS[1], s: ["E"], d: "Exam-based job, no course", y: null, e: "UPSC ESE: prelims, mains and personality test", o: "Group A engineering services in railways, defence production, telecom and more" },
    { n: "MS abroad (engineering, computer science)", c: CATS[1], s: ["E", "S"], d: "1.5 to 2 years", y: 2, e: "GRE (optional at many universities), IELTS or TOEFL, and applications", o: "Tech and research jobs abroad, PhD" },
    { n: "MCA", c: CATS[1], s: ["E", "S", "C"], d: "2 years", y: 2, e: "NIMCET (NITs), CUET PG (central universities), state and university tests", o: "Software developer, data and cloud roles", x: "Usually needs Maths in Class 12 or in graduation" },
    { n: "Software and IT jobs (campus or off-campus)", c: CATS[1], s: ["E", "S", "C"], d: "Job, no course", y: null, e: "Online aptitude test, coding round and interviews (for example TCS NQT, Infosys, Accenture)", o: "Developer, tester, support and analyst roles; IT services and product companies", u: "apt" },

    { n: "M.Sc", c: CATS[2], s: ["S"], d: "2 years", y: 2, e: "IIT JAM (IITs, IISc, NITs), CUET PG, university tests", o: "Research, teaching, industry labs; PhD; CSIR NET" },
    { n: "Integrated PhD / PhD", c: CATS[2], s: ["S", "E"], d: "5 to 6 years", y: 5, e: "JEST, GATE, IIT JAM, CSIR or UGC NET, plus institute interviews", o: "Scientist, professor, R&D roles", x: "Most PhDs need a master's first; integrated PhD starts after a bachelor's" },
    { n: "M.Stat / M.Math (ISI) and data science master's", c: CATS[2], s: ["S", "E"], d: "2 years", y: 2, e: "ISI Admission Test, CMI entrance and university tests", o: "Statistician, data scientist, quant and risk analyst, research" },

    { n: "UPSC Civil Services (IAS, IPS, IFS and others)", c: CATS[3], s: ALL, d: "Exam-based job, no course", y: null, e: "UPSC CSE: prelims, mains and interview", o: "All-India and central services: administration, police, foreign service, revenue and more", x: "Age limits and a fixed number of attempts apply" },
    { n: "State civil services (PCS)", c: CATS[3], s: ALL, d: "Exam-based job, no course", y: null, e: "State PSC exam: prelims, mains and interview", o: "State administrative, police and allied services" },
    { n: "SSC CGL", c: CATS[3], s: ALL, d: "Exam-based job, no course", y: null, e: "SSC CGL tiers (Quant, Reasoning, English, General Awareness)", o: "Central government Group B and C posts: inspector, auditor, assistant section officer and more", u: "cgl" },
    { n: "Railway graduate posts (RRB NTPC)", c: CATS[3], s: ALL, d: "Exam-based job, no course", y: null, e: "RRB NTPC computer-based tests and skill test where needed", o: "Station master, goods guard, clerk and other railway posts", u: "bank" },
    { n: "RBI Grade B, SEBI and NABARD Grade A", c: CATS[3], s: ALL, d: "Exam-based job, no course", y: null, e: "Phase 1 and Phase 2 exams, then interview", o: "Officer posts at the central bank and financial regulators", x: "Marks criteria apply; some streams have their own posts", u: "bank" },

    { n: "Bank PO (IBPS PO, SBI PO)", c: CATS[4], s: ALL, d: "Exam-based job, no course", y: null, e: "Prelims and mains (Quant, Reasoning, English), then interview", o: "Probationary officer, then bank branch and management roles", u: "po" },
    { n: "Bank Clerk (IBPS Clerk, SBI Clerk)", c: CATS[4], s: ALL, d: "Exam-based job, no course", y: null, e: "Prelims and mains (Quant, Reasoning, English)", o: "Clerical and customer-service posts; internal promotion to officer", u: "clerk" },
    { n: "Insurance officer (LIC AAO, NIACL AO and others)", c: CATS[4], s: ALL, d: "Exam-based job, no course", y: null, e: "Prelims, mains and interview", o: "Administrative officer posts at public-sector insurers", u: "bank" },
    { n: "CA, CS or CMA (graduate route)", c: CATS[4], s: ALL, d: "2.5 to 4 years", y: 3, e: "Graduates can enter at the Intermediate or Executive level, subject to each institute's marks rules", o: "Audit, tax, compliance and finance roles; own practice", x: "Commerce graduates find the syllabus most familiar" },
    { n: "CFA / FRM", c: CATS[4], s: ALL, d: "1.5 to 3 years", y: 2, e: "CFA Institute exams (three levels) or GARP FRM exams (two parts)", o: "Investment analysis, portfolio management, risk management" },
    { n: "M.Com", c: CATS[4], s: ["C"], d: "2 years", y: 2, e: "CUET PG or university merit", o: "Accounts, finance and teaching; NET for lectureship" },

    { n: "LLB (3-year law degree)", c: CATS[5], s: ALL, d: "3 years", y: 3, e: "CUET PG (Delhi University and others), state law CETs, LSAT-India, university tests", o: "Advocate, judiciary, corporate and legal advisory roles" },
    { n: "LLM", c: CATS[5], s: ["L"], d: "1 to 2 years", y: 1, e: "CLAT PG (NLUs), university tests", o: "Teaching, specialist practice; CLAT PG scores are also used by some PSUs to hire legal officers" },
    { n: "Judicial services (Civil Judge)", c: CATS[5], s: ["L"], d: "Exam-based job, no course", y: null, e: "State judicial services exam: prelims, mains and interview", o: "Civil judge, then higher judiciary", x: "Some states now require a few years of practice first; check the notice" },

    { n: "MD / MS / DNB", c: CATS[6], s: ["M"], d: "3 years", y: 3, e: "NEET PG, then counselling", o: "Specialist doctor; teaching in medical colleges", x: "For MBBS graduates" },
    { n: "MDS", c: CATS[6], s: ["M"], d: "3 years", y: 3, e: "NEET MDS, then counselling", o: "Specialist dentist; teaching", x: "For BDS graduates" },
    { n: "UPSC Combined Medical Services (CMS)", c: CATS[6], s: ["M"], d: "Exam-based job, no course", y: null, e: "UPSC CMS exam and interview", o: "Medical officer in railways, central health services and other government bodies", x: "For MBBS graduates" },
    { n: "Master of Public Health (MPH)", c: CATS[6], s: ["M", "S"], d: "2 years", y: 2, e: "Institute entrance tests and interviews", o: "Public health programmes, NGOs, research, health policy" },
    { n: "Hospital and healthcare management (MHA, MBA)", c: CATS[6], s: ["M", "S", "C"], d: "2 years", y: 2, e: "Institute tests, CAT or MAT scores, interviews", o: "Hospital administration and healthcare operations", u: "cat" },

    { n: "B.Ed", c: CATS[7], s: ALL, d: "1 to 2 years", y: 2, e: "State or university B.Ed entrance, or merit", o: "School teacher after CTET or state TET", x: "One-year B.Ed is returning from 2026-27 for four-year graduates and postgraduates; check NCTE rules" },
    { n: "Assistant professor or JRF (UGC NET, CSIR NET)", c: CATS[7], s: ALL, d: "2-year master's, then exam", y: 2, e: "UGC NET or CSIR NET (NTA)", o: "College lecturer, junior research fellowship, PhD admission", x: "Needs a master's, or a four-year degree with 75% marks" },

    { n: "CDS (Army, Navy, Air Force academies)", c: CATS[8], s: ALL, d: "Exam, then 1 to 1.5 years training", y: 1.5, e: "UPSC CDS exam, then SSB interview and medical", o: "Commissioned officer", x: "IMA and OTA: any graduate. Naval Academy: engineering. Air Force Academy: Physics and Maths in Class 12 or engineering. Age limits apply." },
    { n: "AFCAT (Indian Air Force)", c: CATS[8], s: ALL, d: "Exam, then training", y: 1.5, e: "AFCAT online test, then AFSB interview and medical", o: "Officer in flying, technical or ground duty branches", x: "Branch-wise degree and Class 12 subject rules apply" },
    { n: "SSC Technical Entry (Army)", c: CATS[8], s: ["E"], d: "Training, then service", y: 1, e: "Shortlisting on marks, then SSB interview and medical (no written exam)", o: "Technical officer in the Army" },
    { n: "CAPF Assistant Commandant", c: CATS[8], s: ALL, d: "Exam-based job, no course", y: null, e: "UPSC CAPF (AC) exam, physical tests, interview", o: "Officer in BSF, CRPF, CISF, ITBP or SSB" },

    { n: "MA (English, History, Political Science, Economics and more)", c: CATS[9], s: ["A", "S", "C"], d: "2 years", y: 2, e: "CUET PG, university tests or merit", o: "Teaching, research, civil services, writing and policy roles; NET" },
    { n: "Journalism and mass communication (IIMC PG diploma, MA)", c: CATS[9], s: ALL, d: "1 to 2 years", y: 1, e: "CUET PG (IIMC and central universities), university tests", o: "Journalist, editor, PR, advertising, digital content" },
    { n: "M.Des / PG design (IITs, NID)", c: CATS[9], s: ALL, d: "2 years", y: 2, e: "CEED (IITs, IISc), NID DAT (Master's), portfolio and interview", o: "UX, product, communication and interaction designer" },
    { n: "MSW (Social Work)", c: CATS[9], s: ALL, d: "2 years", y: 2, e: "CUET PG, TISS and university tests", o: "NGO, CSR, community development and HR roles" },
    { n: "MA / M.Sc Psychology", c: CATS[9], s: ["A", "S"], d: "2 years", y: 2, e: "CUET PG, university tests or merit", o: "Counsellor, HR, research", x: "Clinical practice needs further RCI-recognised training" },

    { n: "Corporate jobs for any graduate", c: CATS[10], s: ALL, d: "Job, no course", y: null, e: "Aptitude test, group discussion and interviews (campus or off-campus)", o: "Sales, operations, customer success, business analyst and management-trainee roles", u: "apt" },
    { n: "Master's abroad (non-engineering)", c: CATS[10], s: ALL, d: "1 to 2 years", y: 1.5, e: "IELTS or TOEFL; GRE or GMAT for some courses; applications 9 to 12 months ahead", o: "Global degrees and careers; check total cost, visa and work rules" },
    { n: "Skill certifications (data analytics, digital marketing, cloud, product)", c: CATS[10], s: ALL, d: "3 to 12 months", y: 0.5, e: "Open enrolment; build a portfolio of real projects", o: "Entry-level and freelance roles; useful alongside a job" },
    { n: "Startup, family business or freelancing", c: CATS[10], s: ALL, d: "Flexible", y: null, e: "No entrance; start small and learn by doing", o: "Own business; the degree still helps with credibility and loans" }
  ];

  window.PATHS = {
    streams: SL,
    who: { E: "engineering graduates", S: "science graduates", C: "commerce and BBA graduates", A: "arts graduates", M: "medical and health graduates", L: "law graduates" },
    allWho: "all graduates", anyLabel: "Any graduate", allChip: "All degrees",
    cats: CATS, rows: D, track: "aftergrad",
    links: {
      cat: { href: "cat.html", text: "Prepare for CAT on this site" },
      bank: { href: "practice.html?exam=general", text: "Practise Bank / SSC aptitude" },
      apt: { href: "placements.html", text: "Placement aptitude practice" },
      cgl: { href: "ssc-cgl.html", text: "SSC CGL pattern and practice" },
      po: { href: "ibps-po.html", text: "IBPS PO pattern and practice" },
      clerk: { href: "ibps-clerk.html", text: "IBPS Clerk pattern and practice" }
    }
  };
})();
