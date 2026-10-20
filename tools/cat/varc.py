"""CAT VARC: original passages and verbal-ability items, written for AptiSetu."""
import re

P1 = """For most of the twentieth century, a broken household object presented its owner with a simple calculation. A toaster, a radio or a pair of shoes was expensive relative to wages, while the labour needed to mend it was cheap. Repair shops lined the streets of every town, and the decision to fix rather than replace was so obvious that it hardly felt like a decision at all. Over the past few decades that arithmetic has quietly inverted. Manufacturing has become so efficient, and global supply chains so long, that a new appliance can cost less than an hour of a skilled technician's time. The repair shop has not been defeated by consumer laziness; it has been priced out.
Economists recognise this as a version of what is called the 'cost disease'. In sectors where productivity rises quickly, such as manufacturing, prices tend to fall; in sectors where it barely moves, such as hands-on services, wages must still keep pace with the rest of the economy, so prices rise. Repair belongs firmly to the second group. A technician diagnosing a faulty washing machine today works at roughly the same speed as one did fifty years ago, yet must be paid a modern wage. The relative price of fixing things therefore climbs year after year, regardless of anyone's intentions.
This framing matters because it changes what a sensible policy response looks like. If throwing things away were merely a cultural failing, the remedy would be exhortation: campaigns urging people to value what they own. But if the problem is mainly one of relative prices, moral appeals will achieve little. People respond to the costs in front of them, and most households cannot afford to pay more to keep an old machine running than to buy a new one, however virtuous that choice might be.
The more promising interventions therefore target the price gap directly. Some governments have experimented with lowering taxes on repair services, or with requiring manufacturers to sell spare parts and publish repair manuals for a set number of years. These right-to-repair rules are often described as consumer-protection measures, but their deeper effect is economic: by making parts available and designs easier to open, they reduce the hours a technician must spend on each job, and so attack the very cost that made repair uncompetitive.
None of this means that culture is irrelevant. Habits formed when repair was impractical can persist long after the economics improves, and a generation that has never had an object mended may not think to ask. But culture tends to follow prices more readily than it leads them. A society that wants its citizens to repair more would do better to make repair cheaper than to make them feel guilty."""

P2 = """Imagine two drivers who leave the same party, each having had a glass of wine too many. Both drive home along similar roads with the same degree of carelessness. On the first driver's route, nothing happens. On the second's, a child runs into the street, and the car cannot stop in time. Most of us judge the second driver far more harshly than the first; the law does too, imposing penalties of an entirely different order. Yet the two drivers did exactly the same thing. The only difference between them lies in something neither controlled: whether a child happened to step off the kerb.
Philosophers call this phenomenon moral luck, and the phrase is meant to sound uncomfortable. A widely shared intuition holds that we should be praised or blamed only for what is within our control. The careless drivers controlled how much they drank and whether they chose to drive, but not who crossed their path. If that intuition is right, then the two drivers deserve exactly the same blame, and our harsher verdict on the second is a kind of mistake.
The difficulty is that the control principle, applied consistently, threatens to swallow almost everything. We do not control the temperament we are born with, the upbringing that shaped our values, or the circumstances that test them. A person who would have collaborated with a tyrannical regime, had they lived under one, may live a blameless life simply because they were born elsewhere. If we strip away everything that luck has touched, it is not obvious that anything remains to be judged at all.
Some thinkers have responded by biting the bullet: moral assessment, they say, should attach only to the inner will, to intentions and choices, and outcomes are morally irrelevant. This view has the merit of consistency, but it struggles to explain experiences that seem central to moral life. The second driver will rightly feel something the first does not, a particular kind of regret that is more than mere sadness that a bad thing occurred. To tell him that his feelings rest on a confusion seems not merely unkind but false to what has happened.
Others argue that the right response is not to abolish moral luck but to accept it as a feature of our condition. On this view, we are not disembodied wills floating free of the world; we are agents whose actions spill into consequences we cannot fully foresee, and taking responsibility means owning those consequences, including the unlucky ones. The price of this acceptance is that morality becomes less tidy and, in a sense, less fair. But perhaps the demand that morality be perfectly fair was itself a fantasy, born of the hope that we could stand outside the world we act in."""

P3 = """In the early 2010s, researchers in several fields began to confront an awkward possibility: that a substantial share of published findings might not hold up if the studies were simply run again. Large collaborative efforts set out to repeat well-known experiments in psychology, and later in economics and cancer biology, following the original methods as closely as possible. The results were sobering. In several of these projects, fewer than half of the repeated studies produced effects as strong as the originals, and some effects vanished altogether. The episode came to be known as the replication crisis.
It would be easy to read this as a story of fraud, but deliberate fabrication explains only a small part of it. The deeper causes are structural. Journals have long preferred to publish striking, positive results over null findings, and careers depend on publications. Under these pressures, researchers face many small decisions that seem individually harmless: which outliers to exclude, which of several measures to report, when to stop collecting data. Each choice can nudge a result across the conventional threshold of statistical significance. Taken together, such choices can make chance patterns look like real discoveries, even when no one intends to deceive.
The statistical threshold itself has come in for criticism. A result is conventionally called significant if, assuming there were no real effect, data at least as extreme would arise less than five per cent of the time. This is often misread as meaning that there is only a five per cent chance the finding is false. In reality, the probability that a significant result reflects a true effect depends heavily on how plausible the hypothesis was to begin with and on how much statistical power the study had. When many long-shot hypotheses are tested in small samples, a large fraction of the significant results can be false alarms.
Reformers have proposed a range of remedies. One of the most influential is preregistration, in which researchers publicly record their hypotheses and analysis plans before collecting data, so that later choices cannot be shaped by the results. Another is the registered report, a format in which a journal agrees to publish a study on the strength of its design, before the results are known, removing the incentive to produce a striking outcome. Larger samples, shared data and routine replication have also gained ground.
Some critics worry that these reforms may stifle exploratory research, the open-ended poking around that often precedes genuine breakthroughs. The reformers' usual reply is that exploration is welcome, provided it is labelled as such. The aim is not to forbid researchers from following hunches, but to stop hunches confirmed after the fact from being presented as predictions made in advance."""

P4 = """There is an old quip that poetry is what gets lost in translation. Like most quips, it contains a truth wrapped in an exaggeration. A poem is not simply a set of statements that could be restated in other words; it is a particular arrangement of sounds, rhythms and associations that belong to one language and no other. When a line in Urdu or Tamil depends on a word that means two things at once, or on a rhyme that exists only in that tongue, the translator faces a choice in which something must be given up.
Translators have broadly divided into two camps over how to make that sacrifice. The first holds that fidelity to meaning comes first: the translator's task is to carry across what the poem says, as precisely as possible, even if the result reads stiffly. The second argues that a poem which no longer works as a poem has not been translated at all, only paraphrased. For this camp, the translator must be willing to invent, to substitute a new rhyme or image that produces in the reader something like the effect the original produced in its first audience.
Each position has its characteristic failure. Strict fidelity can yield texts that are accurate in every particular and lifeless as a whole, like a pressed flower that preserves the shape of a bloom but none of its scent. Free recreation, on the other hand, risks replacing the original poet with the translator, so that readers praise a voice that was never really there. Some celebrated translations are admired precisely as poems in their own right, which is both a tribute to the translator and a quiet admission of distance from the source.
A third approach refuses to choose. Some translators publish the original alongside a literal version and a freer rendering, inviting readers to triangulate between them. Others add notes explaining the puns and allusions that could not survive the crossing. These methods ask more of the reader, but they treat the loss honestly rather than disguising it.
Perhaps the most useful way to see the problem is to abandon the idea that a translation could ever be a replacement for the original. A translation is better understood as a reading: one person's careful, partial and inevitably personal account of what a poem is and does. Seen this way, the existence of many competing translations is not a sign that the task has failed, but evidence of the poem's richness. Each version catches a different facet, and no single version, however skilled, can catch them all."""

def html_passage(title, text):
    paras = text.split("\n")
    return f"<b>{title}</b>" + "".join(f"<p>{p}</p>" for p in paras)

def wc(t): return len(re.findall(r"[A-Za-z']+", t))

def build(B):
    s = "varc"
    M = lambda *a, **k: B.mcq(s, *a, **k)
    T = lambda *a, **k: B.tita(s, *a, **k)
    RC = "Reading Comprehension"
    for pid, title, text in [("cv-repair","Passage: The price of repair",P1),("cv-luck","Passage: Moral luck",P2),("cv-replication","Passage: The replication crisis",P3),("cv-translation","Passage: Translating poetry",P4)]:
        n = wc(text); assert 400 <= n <= 550, (pid, n)
        B.add_set(pid, "passage", title, html_passage(title, text))

    sid = "cv-repair"
    M(RC,"Medium","The passage primarily argues that:",
      ["consumers today repair less than earlier generations because they value their possessions less",
       "the decline of repair is driven mainly by shifting relative prices, so policy should narrow the cost gap rather than appeal to values",
       "right-to-repair rules are essentially consumer-protection measures",
       "manufacturing efficiency has made repair technicians less skilled over time"],
      "the decline of repair is driven mainly by shifting relative prices, so policy should narrow the cost gap rather than appeal to values",
      "The passage says repair 'has been priced out' (para 1), explains this through rising relative costs (para 2), and concludes that making repair cheaper beats making people feel guilty (paras 3–5). Option 1 is the view the author rejects ('not … consumer laziness'). Option 3 is described as how the rules are 'often described', and the author says their deeper effect is economic. Option 4 is never claimed: technicians work at the same speed, not with less skill.", set_id=sid)
    M(RC,"Medium","According to the passage, why has repair become relatively more expensive?",
      ["Repair technicians now demand higher wages than factory workers",
       "Repair productivity has barely changed, while wages must keep pace with an economy in which manufactured goods keep getting cheaper",
       "Long supply chains have made spare parts impossible to obtain",
       "Consumers increasingly prefer new models with more features"],
      "Repair productivity has barely changed, while wages must keep pace with an economy in which manufactured goods keep getting cheaper",
      "Paragraph 2: in low-productivity sectors 'wages must still keep pace with the rest of the economy, so prices rise', while manufacturing prices fall. A technician 'works at roughly the same speed … yet must be paid a modern wage'. There is no comparison of technicians' wages with factory wages (option 1). Supply chains are linked to cheap manufacturing, not missing parts (option 3). Consumer taste for features (option 4) is never mentioned.", set_id=sid)
    M(RC,"Hard","With which of the following would the author most likely agree?",
      ["A public campaign urging people to cherish their belongings would substantially raise repair rates",
       "A tax cut on repair services is likely to do more to increase repair than an awareness campaign",
       "Cultural habits have no influence on whether people choose to repair",
       "Households that replace broken appliances instead of repairing them are acting irrationally"],
      "A tax cut on repair services is likely to do more to increase repair than an awareness campaign",
      "The author says 'moral appeals will achieve little' and lists lower taxes on repair among the 'more promising interventions' that 'target the price gap directly'. Option 1 contradicts this. Option 3 contradicts 'None of this means that culture is irrelevant'. Option 4 contradicts the claim that people sensibly 'respond to the costs in front of them'.", set_id=sid)
    M(RC,"Hard","Which of the following, if true, would most weaken the author's argument?",
      ["In a region where subsidies made repair clearly cheaper than replacement, repair rates did not rise at all",
       "Repair technicians' real wages have risen over the past fifty years",
       "New appliances have become cheaper in real terms",
       "Some manufacturers have lobbied against right-to-repair rules"],
      "In a region where subsidies made repair clearly cheaper than replacement, repair rates did not rise at all",
      "The argument rests on prices being the main driver of repair decisions. If repair becoming cheaper changed nothing, that link is undercut. Options 2 and 3 are consistent with, and even support, the cost-disease explanation. Option 4 says nothing about whether prices drive behaviour.", set_id=sid)

    sid = "cv-luck"
    M(RC,"Medium","The example of the two drivers is used mainly to:",
      ["show that drink-driving penalties are too lenient",
       "illustrate a case in which our judgements of blame seem to depend on something outside the agents' control",
       "argue that the second driver deserves no blame at all",
       "demonstrate that intentions matter more than outcomes"],
      "illustrate a case in which our judgements of blame seem to depend on something outside the agents' control",
      "The paragraph ends: 'The only difference between them lies in something neither controlled', and the next paragraph names this 'moral luck'. The passage says nothing about the penalties being lenient (option 1). It never says the second driver is blameless (option 3). Option 4 is one view discussed later (the 'inner will' view), not the purpose of the example.", set_id=sid)
    M(RC,"Medium","According to the passage, the main difficulty with applying the control principle consistently is that it:",
      ["would make the law too harsh on careless drivers",
       "would leave little or nothing open to moral judgement, since so much that shapes us is beyond our control",
       "cannot account for the intentions of agents",
       "conflicts with the way courts assign penalties"],
      "would leave little or nothing open to moral judgement, since so much that shapes us is beyond our control",
      "Paragraph 3: the principle 'threatens to swallow almost everything' (temperament, upbringing, circumstances), and 'it is not obvious that anything remains to be judged'. Option 3 is the reverse: the principle focuses on what we control, including intentions. Options 1 and 4 concern the law, which isn't the stated difficulty.", set_id=sid)
    M(RC,"Medium","The author's attitude towards the view that only the 'inner will' should be judged is best described as:",
      ["wholehearted endorsement",
       "acknowledging its consistency while doubting that it fits our moral experience",
       "dismissive contempt",
       "strict neutrality, offering no evaluation"],
      "acknowledging its consistency while doubting that it fits our moral experience",
      "'This view has the merit of consistency, but it struggles to explain experiences that seem central to moral life.' The author grants a strength (so not contempt), raises a serious objection (so not endorsement), and clearly evaluates it (so not neutral).", set_id=sid)
    M(RC,"Hard","Which of the following can best be inferred about the author's own position?",
      ["The author thinks moral luck should be eliminated from our moral practices",
       "The author leans towards accepting moral luck, even if this makes morality less tidy and less fair",
       "The author believes the first driver is more blameworthy than the second",
       "The author regards the second driver's regret as irrational"],
      "The author leans towards accepting moral luck, even if this makes morality less tidy and less fair",
      "The final paragraph presents acceptance sympathetically and ends by suggesting that 'the demand that morality be perfectly fair was itself a fantasy', which signals agreement. Option 1 is the view the author resists. Option 3 has no support. Option 4 contradicts 'The second driver will rightly feel something'.", set_id=sid)

    sid = "cv-replication"
    M(RC,"Medium","According to the passage, the replication crisis is mainly explained by:",
      ["widespread deliberate fabrication of data",
       "publication incentives and many small analytical choices that can make chance patterns look like real findings",
       "outdated laboratory equipment",
       "journals refusing to publish psychology research"],
      "publication incentives and many small analytical choices that can make chance patterns look like real findings",
      "Paragraph 2: 'deliberate fabrication explains only a small part', and 'the deeper causes are structural': journals preferring striking results, plus 'many small decisions' that can 'make chance patterns look like real discoveries'. Options 3 and 4 are never mentioned.", set_id=sid)
    M(RC,"Hard","Which of the following statements about statistical significance is consistent with the passage?",
      ["A significant result means there is at most a five per cent chance that the finding is false",
       "Whether a significant result reflects a real effect depends partly on the hypothesis's prior plausibility and the study's statistical power",
       "Significance thresholds played no role in the replication crisis",
       "Testing many hypotheses in small samples makes false alarms rarer"],
      "Whether a significant result reflects a real effect depends partly on the hypothesis's prior plausibility and the study's statistical power",
      "Paragraph 3 says this almost word for word. Option 1 is the misreading the passage warns against. Option 3 contradicts 'The statistical threshold itself has come in for criticism' and the role of nudging results 'across the conventional threshold'. Option 4 is the reverse of the final sentence of paragraph 3.", set_id=sid)
    M(RC,"Medium","As described in the passage, the main purpose of a registered report is to:",
      ["speed up the publication of results",
       "make the decision to publish independent of whether the results turn out to be striking",
       "allow researchers to revise their analysis after seeing the data",
       "replace peer review with public registration"],
      "make the decision to publish independent of whether the results turn out to be striking",
      "The journal agrees to publish 'on the strength of its design, before the results are known, removing the incentive to produce a striking outcome'. Speed (option 1) isn't mentioned. Option 3 is what preregistration prevents. Option 4 is never stated.", set_id=sid)
    M(RC,"Hard","The reformers' reply in the final paragraph implies that:",
      ["exploratory research should be discouraged",
       "the problem is not exploration itself but presenting after-the-fact findings as if they had been predicted",
       "hunches rarely lead to genuine breakthroughs",
       "critics have misunderstood the statistics behind preregistration"],
      "the problem is not exploration itself but presenting after-the-fact findings as if they had been predicted",
      "'The aim is not to forbid researchers from following hunches, but to stop hunches confirmed after the fact from being presented as predictions made in advance.' Option 1 contradicts 'exploration is welcome'. Option 3 contradicts the critics' point that exploration 'often precedes genuine breakthroughs', which the reformers don't dispute. Option 4 isn't stated.", set_id=sid)

    sid = "cv-translation"
    M(RC,"Medium","The author's central claim is that:",
      ["poetry cannot be translated in any meaningful sense",
       "literal translations are always preferable to free ones",
       "a translation is best seen as one partial reading rather than a replacement, so many translations reflect a poem's richness rather than failure",
       "translators should always add explanatory notes"],
      "a translation is best seen as one partial reading rather than a replacement, so many translations reflect a poem's richness rather than failure",
      "The final paragraph states the author's conclusion: 'A translation is better understood as a reading', and many translations are 'evidence of the poem's richness'. Option 1 is called 'an exaggeration'. Option 2 ignores the failures of strict fidelity the author describes. Option 4 is only one method mentioned in paragraph 4, never a universal rule.", set_id=sid)
    M(RC,"Medium","The 'pressed flower' comparison suggests that strictly faithful translations can:",
      ["contain errors of detail",
       "keep a poem's form and particulars while losing its living effect",
       "become more beautiful than the original",
       "be impossible for ordinary readers to understand"],
      "keep a poem's form and particulars while losing its living effect",
      "Such translations are 'accurate in every particular and lifeless as a whole', like a flower keeping 'the shape of a bloom but none of its scent'. Option 1 contradicts 'accurate in every particular'. Options 3 and 4 have no support.", set_id=sid)
    M(RC,"Hard","What does the passage suggest about translations admired 'as poems in their own right'?",
      ["They prove that the translator stayed closest to the original",
       "Their being admired in this way hints that they may have moved away from the source poem",
       "They are rarely successful with readers",
       "They usually print the original and a literal version side by side"],
      "Their being admired in this way hints that they may have moved away from the source poem",
      "Such admiration is 'both a tribute to the translator and a quiet admission of distance from the source'. Option 1 is the opposite. Option 3 contradicts 'celebrated'. Option 4 describes the third approach, which is a different method.", set_id=sid)
    M(RC,"Medium","Which of the following would the author most likely consider an honest way of dealing with what is lost in translation?",
      ["Presenting a free recreation without mentioning the original's wordplay",
       "Publishing the original with a literal and a freer version, along with notes on puns and allusions",
       "Translating only poems that contain no wordplay",
       "Updating the poem's imagery for modern readers without comment"],
      "Publishing the original with a literal and a freer version, along with notes on puns and allusions",
      "Paragraph 4 says these methods 'treat the loss honestly rather than disguising it'. Options 1 and 4 disguise changes. Option 3 avoids the problem rather than dealing with it, and the passage never suggests it.", set_id=sid)

    # ---------- Para-jumbles (TITA sequence) ----------
    PJ = "Para-jumbles"
    jumbles = [
     (["The first printed maps of the world were as much works of imagination as of measurement.",
       "Where explorers had not yet reached, mapmakers filled the gaps with sea monsters, mythical islands and confident guesses.",
       "These inventions were not always idle decoration; some, copied from map to map, sent later sailors in search of lands that did not exist.",
       "Only with better instruments and systematic surveys did the blank spaces come to be admitted honestly as unknown."],
      [2,4,1,3], "The opener introduces imaginative maps. 'Where explorers had not yet reached…' explains how gaps were filled. 'These inventions' must follow the inventions (monsters, islands). 'Only with better instruments…' closes the history."),
     (["A city's street trees are often treated as ornaments, planted for beauty and removed when inconvenient.",
       "Yet they perform measurable work: shading pavements, absorbing rainwater and cooling the air around them.",
       "On hot afternoons, a tree-lined street can be noticeably cooler than a bare one a few blocks away.",
       "Putting a money value on that work has persuaded some councils to protect trees they once saw as expendable."],
      [3,1,4,2], "The 'ornament' view comes first. 'Yet' introduces the contrast (they do work). The hot-afternoon example illustrates the cooling. 'That work' in the last sentence refers back to the work described, so it comes last."),
     (["Early gramophone records could hold only about three minutes of music per side.",
       "Musicians adapted, trimming and arranging their pieces to fit within that span.",
       "Longer-playing formats eventually removed the limit.",
       "Yet the habit it had created proved durable, and the short pop song outlived the technology that shaped it."],
      [4,2,1,3], "Constraint → adaptation → the limit removed → 'Yet the habit it had created' ('it' = the limit), which needs the removal sentence just before it."),
     (["Honeybees tell their nest-mates where food is through a movement known as the waggle dance.",
       "The angle of the dance relative to the vertical indicates the direction of the food relative to the sun.",
       "The duration of the waggling run, meanwhile, signals how far away the food is.",
       "Together, these two cues let other foragers fly straight to a source they have never visited."],
      [1,3,4,2], "Introduce the dance, then cue 1 (angle = direction), then 'meanwhile' cue 2 (duration = distance), then 'Together, these two cues' summarises both."),
     (["In the 1950s and 1960s, many economists expected poorer countries to catch up steadily with richer ones.",
       "The reasoning was that capital would flow to where it was scarce and earned the highest returns.",
       "In practice, convergence happened in some regions but not in others, and the gap sometimes widened.",
       "This mixed record pushed researchers to look beyond capital, towards institutions, education and geography."],
      [2,1,3,4], "Expectation → 'The reasoning was…' (explains the expectation) → 'In practice…' (contrast with reality) → 'This mixed record…' (consequence)."),
     (["Chess programs now play far better than any human champion.",
       "Many feared that this would leave the game pointless for people.",
       "Instead, players began using the programs as training partners, and the standard of top-level play rose.",
       "The machines, in other words, ended up raising human standards rather than replacing human interest."],
      [4,3,2,1], "Fact → fear ('this' = machines being better) → 'Instead…' (what actually happened) → 'in other words' summarises the outcome."),
    ]
    for i, (correct_order, shown_pos, why) in enumerate(jumbles):
        # shown_pos[k] = the label (1-4) under which correct sentence k is shown
        assert sorted(shown_pos) == [1, 2, 3, 4]
        shown = sorted(range(4), key=lambda k: shown_pos[k])   # display order: label 1, 2, 3, 4
        body = "<p>The four sentences below, when properly sequenced, form a coherent paragraph. Enter the sequence of the four numbers (e.g. 2143).</p><ol class='pj'>" + "".join(f"<li>{correct_order[k]}</li>" for k in shown) + "</ol>"
        ans = "".join(str(shown_pos[k]) for k in range(4))
        # check: reading labels in 'ans' order reproduces the correct paragraph
        assert [correct_order[shown[int(c)-1]] for c in ans] == correct_order
        T(PJ, "Medium" if i % 2 == 0 else "Hard", body, ans, f"Correct order: {ans}. {why}", kind="sequence")

    # ---------- Para-summary ----------
    PS = "Para-summary"
    summaries = [
     ("Remote work was once imagined as a perk for a few; it is now a structural feature of many industries. Its advantages are real: saved commuting time, wider hiring pools and greater flexibility for carers. But organisations have discovered costs that are harder to measure. Newcomers learn more slowly when they cannot watch experienced colleagues, and the informal exchanges that spark ideas become rarer. The firms that seem to be adapting best are not those that have chosen one model wholesale, but those that decide deliberately which activities need people together and which do not.",
      ["Remote work has more costs than benefits, so firms should return to the office.",
       "Remote work brings clear benefits but subtler costs, and organisations do best by deliberately matching each activity to the right setting.",
       "New employees should always work from the office.",
       "Remote work spread mainly because of the needs of carers."],
      1, "The paragraph weighs real benefits against harder-to-measure costs and ends with its main point: the best firms decide deliberately activity by activity. Option 1 contradicts 'advantages are real'. Option 3 picks out one detail and turns it into a rule. Option 4 misreads one listed benefit as the cause."),
     ("Languages rarely die because they are banned. More often they fade through quiet calculation. When parents conclude that their children's prospects depend on a dominant language, they speak it at home, and within a generation or two the older tongue survives mainly among the elderly. Efforts at revival therefore succeed less through nostalgia than through making the language useful again, in schools, media, local government and work.",
      ["Languages mainly disappear because governments ban them.",
       "Language loss is driven largely by families' practical choices, so revival depends on making the language practically useful again.",
       "Elderly speakers bear the main responsibility for keeping languages alive.",
       "Nostalgia is the strongest force behind successful language revival."],
      1, "Both the cause (practical calculation by parents) and the remedy (usefulness, not nostalgia) are captured only by option 2. Option 1 contradicts the first sentence. Option 4 contradicts the last sentence. Option 3 is not claimed."),
     ("A well-designed default can shape behaviour as powerfully as a rule. When employees are automatically enrolled in a pension scheme and must opt out, participation is far higher than when they must actively opt in, even though the choice on offer is identical. Defaults work because people tend to stay with whatever requires no action. That gives the designers of forms and systems a quiet but considerable power, and with it a responsibility to set defaults in people's interest.",
      ["Pension schemes should be made compulsory for all employees.",
       "Because people tend to stick with defaults, those who set them hold real influence and should use it in people's interest.",
       "Defaults are more effective than laws in every situation.",
       "Most employees are indifferent to their pensions."],
      1, "The paragraph moves from evidence (auto-enrolment) to mechanism (inertia) to conclusion (power and responsibility). Option 2 has all three. Option 1 isn't argued. Option 3 overstates 'as powerfully as'. Option 4 is never stated: the point is inertia, not indifference."),
     ("Museums once displayed objects taken from colonies with little comment on how they had been acquired. Today many institutions add information about provenance, and some have returned items to the communities they came from. Critics say this politicises collections. Supporters reply that silence about origins was always a political choice too, merely an unexamined one.",
      ["Museums should return every object acquired during the colonial era.",
       "As museums add context about colonial-era objects, critics call this political, while supporters argue that the earlier silence was itself political.",
       "Critics have stopped museums from returning objects to their places of origin.",
       "Provenance information is of little interest to museum visitors."],
      1, "The paragraph describes a change in practice and the debate about it, ending with the supporters' rebuttal. Option 2 covers both sides accurately. Option 1 takes a position the paragraph doesn't. Options 3 and 4 are unsupported."),
     ("Sleep is often treated as time lost to productivity. Yet research on learning suggests that memories formed during the day are strengthened and reorganised during sleep, and that people deprived of it perform worse on tasks requiring both recall and judgement. Cutting sleep to gain working hours may therefore lower the quality of the very work it is meant to increase.",
      ["Everyone should sleep for more than eight hours a night.",
       "Because sleep supports memory and judgement, giving it up for extra working time can undermine the work itself.",
       "Sleep matters more than learning.",
       "Productivity is impossible to measure accurately."],
      1, "The paragraph's conclusion ('therefore…') is that cutting sleep can backfire on work quality because sleep supports memory and judgement. That is option 2. Option 1 gives a specific figure that isn't in the text. Options 3 and 4 are unrelated claims."),
    ]
    for i, (para, opts, k, why) in enumerate(summaries):
        M(PS, "Medium" if i % 2 else "Hard", f"<p>Choose the option that best captures the essence of the passage.</p><blockquote class='ps'>{para}</blockquote>", opts, opts[k], why)

    # ---------- Odd sentence out (TITA single digit) ----------
    OS = "Odd sentence out"
    odds = [
     (["Coral reefs cover a tiny fraction of the ocean floor yet support a remarkably large share of marine species.",
       "Their structure is built by colonies of small animals that secrete skeletons of calcium carbonate.",
       "Rising sea temperatures can cause corals to expel the algae living in their tissues, leaving them bleached.",
       "Repeated bleaching gives reefs too little time to recover, threatening the many species that depend on them."],
      "Deep-sea trenches remain among the least explored places on Earth.", 4,
      "Sentences 1, 2, 3 and 5 build a paragraph about coral reefs: their importance, their structure, bleaching, and its consequences. The deep-sea trenches sentence is about a different marine environment."),
     (["Street food in many Indian cities is sold from carts that move with the rhythms of the day.",
       "Breakfast vendors appear near railway stations early in the morning, and chaat sellers gather near markets in the evening.",
       "Office districts draw lunchtime stalls that vanish by late afternoon.",
       "This mobility lets vendors follow their customers rather than wait for customers to find them."],
      "The Indian Railways is one of the largest employers in the world.", 2,
      "The paragraph is about vendors moving through the day to follow customers (morning, lunch, evening, then 'This mobility'). The railways-as-employer sentence picks up the word 'railway' but is off-topic."),
     (["The printing press made books far cheaper to produce.",
       "As prices fell, reading spread beyond clergy and scholars to merchants and artisans.",
       "Wider literacy in turn created demand for pamphlets, almanacs and news sheets.",
       "Within a few generations, printed material had changed how ideas circulated across Europe."],
      "Many medieval manuscripts were decorated with gold leaf.", 3,
      "Sentences 1, 2, 4 and 5 form a cause-and-effect chain: cheaper books → wider reading → demand for new print → changed circulation of ideas. The gold-leaf sentence describes manuscript decoration and breaks the chain."),
     (["Many birds migrate thousands of kilometres every year.",
       "They navigate using several cues, including the positions of the sun and stars.",
       "Some species also appear able to sense the Earth's magnetic field.",
       "In some species, young birds on their first journey follow experienced adults and learn the route as they go."],
      "Penguins cannot fly but are strong swimmers.", 1,
      "Sentences 2–5 explain how migrating birds find their way: celestial cues, magnetism, learning from adults. The penguin sentence is about a flightless bird's swimming and has nothing to do with navigation."),
    ]
    for i, (good, odd, pos, why) in enumerate(odds):
        sents = good[:pos-1] + [odd] + good[pos-1:]
        assert len(sents) == 5 and sents[pos-1] == odd
        body = "<p>Five jumbled sentences are given. Four of them can form a coherent paragraph. Enter the number of the sentence that does not fit.</p><ol class='pj'>" + "".join(f"<li>{x}</li>" for x in sents) + "</ol>"
        T(OS, "Medium", body, str(pos), f"Odd sentence: {pos}. {why}", kind="digit")
