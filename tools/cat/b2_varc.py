"""CAT practice pack B2 — VARC: 2 original RC passages (4 Qs each) and 10 verbal-ability items, written for AptiSetu.
Every MCQ has exactly one defensible answer; the solution names the line that settles it and why each distractor fails."""
import re
from varc import html_passage, wc

RC1_T = "What de-extinction would restore"
RC1 = """Each time a team of geneticists announces progress towards reviving an extinct animal, the headlines tend to promise a homecoming: the woolly mammoth back on the tundra, the passenger pigeon darkening American skies again. What is actually on offer is more modest and, in some ways, more interesting. No laboratory can recover a complete genome from remains that have lain in permafrost or museum drawers for centuries; DNA breaks into fragments, and the gaps must be filled from living relatives. The likely product is therefore not a mammoth but an elephant edited to carry a few dozen mammoth traits, such as dense hair and a thick layer of fat.
Supporters argue that this distinction matters less than it seems. What an ecosystem notices, they say, is not an animal's pedigree but what it does. If cold-adapted elephants trampled snow and toppled shrubs as mammoths once did, they might help restore the grassland that once covered much of the far north, which, some ecologists argue, keeps the ground beneath it colder than forest does. On this view, de-extinction is a tool for reviving lost ecological functions, and the name is merely a piece of marketing.
Critics accept the functional framing but draw the opposite conclusion from it. If the aim is to restore what an animal did, they ask, why begin with the most expensive and uncertain route? Many lost functions can be partly supplied by species that still exist: horses and bison have been released onto Siberian grassland for exactly this purpose. More pointedly, the money and attention that flow to spectacular revival projects may come at the expense of species that are declining now and could be saved by ordinary means, such as protecting habitat. There is also a worry about moral hazard. If extinction comes to seem reversible, the urgency of preventing it may fade.
Neither side, it should be said, has much evidence to offer yet. No edited animal has yet been set loose in the ecosystem it is meant to restore, so claims about ecological benefit remain projections, and the fear that revival will drain funds from conservation assumes that the money would otherwise have gone there, which is far from certain; much of it comes from private investors drawn by the novelty of the technology itself.
What the debate does reveal is how unclear the goal of conservation has become. For most of its history the field could define success as keeping species from disappearing. Once a species can, in some sense, be rebuilt, that definition no longer settles very much. We are pushed to say what we were trying to preserve all along: particular lineages of living things, the work they did in the world, or our own sense of what a complete landscape looks like."""

RC2_T = "Why proverbs disagree"
RC2 = """Collections of proverbs are full of contradictions. 'Look before you leap' sits uneasily beside 'he who hesitates is lost'; 'many hands make light work' is flatly denied by 'too many cooks spoil the broth'. To the systematic mind this looks like an embarrassment. A body of advice that recommends both caution and boldness, both cooperation and its avoidance, seems to recommend nothing at all.
The embarrassment fades once we ask what proverbs are for. They are not premises from which conclusions can be deduced, still less laws that hold in all cases. They are closer to tools, each suited to a recurring kind of situation. A carpenter is not inconsistent for owning both a saw and a glue pot; the question is never which tool is correct in general, but which one this job needs. A proverb is summoned when a speaker has already sized up a situation and wants to name it compactly, and the name carries a recommendation with it. The recommendation is only as good as the sizing-up that came before it: describe a hasty plan as bold and the proverb about hesitation blesses it; describe it as reckless and the proverb about looking first condemns it.
This means that the real knowledge lies not in the proverbs but in the judgement that selects among them, and that judgement is precisely what proverbs cannot supply. No proverb tells you whether the moment calls for looking or for leaping. Seen in this light, the oddity is not that proverbs contradict each other but that anyone expected them not to. A culture that offered only one of each pair would be giving worse advice, not better, because it would be pretending that one kind of situation never occurs.
There is, however, a less flattering side to this flexibility. Because a proverb can be found to support almost any course of action, proverbs are well suited to justifying decisions after they have been made. The person who rushed in and succeeded quotes the saying about hesitation; had the venture failed, an onlooker would have been ready with the one about looking first. Used this way, the stock of proverbs becomes a device for making every outcome seem to have been foreseeable.
The two uses are hard to tell apart from the outside, since the same words serve both. The difference lies in timing and in honesty: whether the saying is brought to the situation before the choice, as a way of thinking about it, or fitted to the result afterwards, as a way of not having to. A simple test is to ask whether the speaker could have said in advance which saying they would reach for. If so, the proverb did some work; if the choice was settled only by how things turned out, it did none."""

def build(B):
    s = "varc"
    pos = iter([2, 0, 3, 1, 3, 2, 0, 1, 0, 3, 2])
    def M(topic, diff, text, options, correct, solution, **k):
        o = [x for x in options if x != correct]; p = next(pos); o.insert(p, correct)
        assert not re.search(r"[Oo]ption \d|(first|second|third|fourth) option", solution), solution
        B.mcq(s, topic, diff, text, o, correct, solution, **k)
    T = lambda *a, **k: B.tita(s, *a, **k)
    for sid, title, text in (("b2-rc1", RC1_T, RC1), ("b2-rc2", RC2_T, RC2)):
        assert 420 <= wc(text) <= 640, (sid, wc(text))
        B.add_set(sid, "passage", title, html_passage(title, text))
    RC = "Reading Comprehension"
    R1 = lambda *a, **k: M(RC, *a, set_id="b2-rc1", **k)
    R2 = lambda *a, **k: M(RC, *a, set_id="b2-rc2", **k)

    R1("Medium", "The central concern of the passage is to:",
       ["show that de-extinction is technically impossible and should be abandoned",
        "explain what de-extinction can realistically produce, set out the arguments about it, and draw out what the debate reveals about the aims of conservation",
        "argue that private investors should fund conservation rather than de-extinction",
        "prove that edited elephants would restore the grasslands of the far north"],
       "explain what de-extinction can realistically produce, set out the arguments about it, and draw out what the debate reveals about the aims of conservation",
       "The passage moves from what is realistically on offer (para 1), through supporters and critics (paras 2–3) and the lack of evidence (para 4), to what the debate reveals about conservation's goal (para 5). 'Technically impossible' overstates: the passage says the product is 'modest', not impossible. The investor and grassland options turn single details into the main point, and the grassland one contradicts para 4 ('claims about ecological benefit remain projections').")
    R1("Hard", "Supporters and critics of de-extinction, as described in the passage, agree that:",
       ["the revived animal would be genetically identical to the extinct one",
        "the money spent on revival would otherwise go to conventional conservation",
        "the value of reviving an animal should be judged by the ecological role it would play",
        "horses and bison are an adequate substitute for mammoths"],
       "the value of reviving an animal should be judged by the ecological role it would play",
       "Para 3 opens: 'Critics accept the functional framing but draw the opposite conclusion from it.' So both sides judge by function. Genetic identity is denied in para 1. The funding claim is the critics' assumption, which para 4 questions, not a shared view. The horses-and-bison claim is the critics' suggestion only, and they say substitutes supply functions 'partly'.")
    R1("Hard", "Which of the following, if true, would most weaken the critics' 'moral hazard' worry as described in the passage?",
       ["Surveys find that people told about revival projects become more willing, not less, to support protection of currently endangered species.",
        "The cost of editing elephant embryos is expected to fall sharply over the next decade.",
        "Bison released onto Siberian grassland have survived several winters.",
        "Some museum specimens yield longer DNA fragments than permafrost remains."],
       "Surveys find that people told about revival projects become more willing, not less, to support protection of currently endangered species.",
       "The moral-hazard worry is that if extinction seems reversible, 'the urgency of preventing it may fade'. Evidence that revival stories increase support for preventing extinction directly cuts against it. Falling costs bear on the expense argument, not on urgency. The bison and DNA-fragment options concern substitutes and technique, not public urgency.")
    R1("Medium", "The author's attitude towards the claims made by both sides is best described as:",
       ["dismissive, since both sides are said to be motivated by marketing",
        "cautious, since the author notes that the key claims on each side rest on projections or untested assumptions",
        "enthusiastic about revival, since the author calls it 'more interesting' than the headlines suggest",
        "hostile to critics, since their concern about funding is called absurd"],
       "cautious, since the author notes that the key claims on each side rest on projections or untested assumptions",
       "Para 4: 'Neither side … has much evidence to offer yet': ecological benefits 'remain projections' and the funding fear 'assumes' something 'far from certain'. That is caution, not dismissal or hostility. 'Marketing' is the supporters' remark about the name only. 'More interesting' (para 1) is about what is on offer, not an endorsement of revival.")

    R2("Medium", "According to the passage, the 'real knowledge' associated with proverbs lies in:",
       ["memorising as many proverbs as possible",
        "the judgement needed to decide which proverb fits a situation",
        "the logical rules from which proverbs are derived",
        "choosing the proverb that is correct in general"],
       "the judgement needed to decide which proverb fits a situation",
       "Para 3: 'the real knowledge lies not in the proverbs but in the judgement that selects among them'. Para 2 denies that proverbs are premises or general laws, which rules out 'logical rules' and 'correct in general'. Memorisation is never offered as the source of knowledge.")
    R2("Hard", "The carpenter analogy in the second paragraph is used chiefly to suggest that:",
       ["proverbs, like tools, wear out with use",
        "contradictory proverbs are no more inconsistent than a set of tools meant for different jobs",
        "proverbs are mainly useful for practical trades",
        "a person should own only the proverbs they actually need"],
       "contradictory proverbs are no more inconsistent than a set of tools meant for different jobs",
       "The analogy answers the charge of inconsistency: a carpenter 'is not inconsistent for owning both a saw and a glue pot', because each suits a different job. The other options import ideas the analogy never carries (wear, trades, owning fewer tools).")
    R2("Hard", "Which of the following best illustrates the 'less flattering' use of proverbs described in the fourth paragraph?",
       ["Before choosing a career, a student weighs 'look before you leap' against 'he who hesitates is lost' to decide how much research to do.",
        "A teacher explains to a class that the two proverbs about cooks and hands contradict each other.",
        "After an unplanned trip turns out well, a traveller says 'he who hesitates is lost', though he would have said 'look before you leap' had it gone badly.",
        "A manager refuses to quote proverbs in meetings because they are too vague."],
       "After an unplanned trip turns out well, a traveller says 'he who hesitates is lost', though he would have said 'look before you leap' had it gone badly.",
       "Para 4 describes proverbs fitted to outcomes 'after they have been made', so that 'every outcome seem[s] to have been foreseeable'. Only the traveller fits a saying to the result. The student uses proverbs before the choice, which is the honest use in the last paragraph. The teacher and manager options do not involve justifying a decision at all.")
    R2("Hard", "The author would most likely agree with which of the following?",
       ["A culture should discard one proverb from each contradictory pair to make its advice clearer.",
        "The same proverb can be used honestly or dishonestly, and its wording alone does not reveal which.",
        "Proverbs are worthless because they can support any course of action.",
        "Proverbs are best understood as general laws with occasional exceptions."],
       "The same proverb can be used honestly or dishonestly, and its wording alone does not reveal which.",
       "Last paragraph: the two uses 'are hard to tell apart from the outside, since the same words serve both'; the difference lies in timing and honesty. Discarding one of each pair is rejected in para 3 ('worse advice, not better'). 'Worthless' ignores the useful role set out in paras 2–3. 'General laws' is denied in para 2 ('still less laws that hold in all cases').")

    # ---------- Para-summary (Hard: distractors are partial or shift emphasis) ----------
    PS = "Para-summary"
    summaries = [
     ("Cities that widen roads to cure congestion usually find that, within a few years, traffic is as slow as before. The new capacity makes driving more attractive, so people who had been taking the train, travelling at other times or not making the trip at all begin to drive at peak hours. Capacity, in other words, does not simply serve demand; it helps create it. The more reliable way to keep traffic moving is to make road space less of a free good, through pricing or by giving it over to buses and cycles, so that the trips that remain are the ones people value most.",
      ["Road widening fails because cities build roads too slowly to keep up with population growth.",
       "Since added road capacity draws in new traffic, congestion is better managed by limiting or pricing road space than by expanding it.",
       "Public transport is always faster than driving in congested cities.",
       "Widening roads encourages people to travel at peak hours instead of off-peak hours."],
      1, "The paragraph's claim is that capacity 'helps create' demand, so the remedy is to make road space 'less of a free good'. The option about limiting or pricing road space has both the mechanism and the conclusion. The population-growth option gives a cause the paragraph never mentions. The public-transport claim is unstated. The peak-hours option is one part of the mechanism and leaves out the conclusion."),
     ("A museum guard who spends years in the same gallery often notices things that visiting experts miss: a crack that has lengthened, a colour that has faded under one particular window, the way visitors always stop at the same spot. Such knowledge comes from long, unhurried attention rather than from training, and it seldom appears in reports, because the people who have it are rarely asked. Institutions that want to understand what they hold would do well to treat this kind of observation as evidence, not anecdote.",
      ["Museum guards are better qualified than experts to care for collections.",
       "Long, close familiarity yields real but overlooked knowledge, which institutions should seek out and take seriously.",
       "Experts should spend more time in galleries.",
       "Visitors' habits reveal more about artworks than condition reports do."],
      1, "The paragraph says sustained attention produces knowledge that 'seldom appears in reports' because no one asks, and that institutions should treat it 'as evidence'. The option about overlooked knowledge from long familiarity captures both. 'Better qualified than experts' overstates: guards notice some things experts miss, not that they are better qualified. The options about experts' time in galleries and visitors' habits are not argued."),
     ("Early photographs of crowded streets often show them strangely empty. The long exposures of the time meant that anything moving left no trace, so only buildings and the occasional person standing still were recorded. To later viewers these images can suggest a quieter, emptier past, but the emptiness belongs to the technology, not to the city. The episode is a useful warning: before we read a record as a picture of the world, we need to ask what the recording method could and could not capture.",
      ["Nineteenth-century cities were much less crowded than modern ones.",
       "Early cameras could not record moving people because of long exposure times.",
       "Because a record reflects the limits of how it was made, we should understand those limits before treating it as a faithful picture of the past.",
       "Photographs are less reliable than written descriptions as historical evidence."],
      2, "The example (empty streets caused by long exposures) leads to a general lesson about understanding a method's limits before reading its records as reality. The option about understanding a record's limits states that lesson. The long-exposure option restates only the example. 'Less crowded' cities is the misreading the paragraph warns against. The photographs-versus-writing option compares photographs with writing, which the paragraph never does."),
    ]
    for para, opts, k, why in summaries:
        M(PS, "Hard", f"<p>Choose the option that best captures the essence of the passage.</p><blockquote class='ps'>{para}</blockquote>", opts, opts[k], why)

    # ---------- Odd sentence out (Hard: the odd sentence is on topic but breaks the argument) ----------
    OS = "Odd sentence out"
    odds = [
     (["Tea reached Britain in the seventeenth century as an expensive luxury.",
       "Over the next hundred years, falling import duties and growing trade made it affordable to ordinary households.",
       "By the nineteenth century it had become part of the daily routine of workers as well as the wealthy.",
       "Its spread from luxury to staple thus followed the steady fall in its price."],
      "Green tea and black tea are made from the leaves of the same plant.", 3,
      "Sentences 1, 2, 4 and 5 trace tea's change from luxury to staple as its price fell. Sentence 3 is about tea, but it is a botanical fact that plays no part in the price-and-spread argument."),
     (["A vaccine protects not only the person who receives it but also those around them.",
       "When enough people are immune, an infection struggles to find new hosts and outbreaks die out.",
       "This indirect protection matters most for those who cannot be vaccinated, such as newborns.",
       "The proportion of a population that must be immune for this effect depends on how contagious the disease is."],
      "Some vaccines must be stored at very low temperatures, which makes them hard to distribute.", 5,
      "Sentences 1–4 explain herd immunity: indirect protection, how it works, who benefits and the threshold it needs. The storage sentence is about vaccines but concerns logistics, not population immunity."),
     (["When a word is borrowed from another language, its meaning often narrows.",
       "The borrowing language usually already has a word for the general idea, so the newcomer takes a more specific sense.",
       "English, for instance, already had 'house', so the borrowed French 'mansion' came to mean a large and grand one.",
       "Narrowing in this way lets a borrowed word find a niche instead of competing with a native word."],
      "Some languages, such as Icelandic, prefer to coin new words from native roots rather than borrow foreign ones.", 1,
      "Sentences 2–5 explain why borrowed words narrow in meaning and give an example. The Icelandic sentence is about language and borrowing, but it describes avoiding borrowing, so it has no place in an account of what happens to words that are borrowed."),
    ]
    for good, odd, pos, why in odds:
        sents = good[:pos-1] + [odd] + good[pos-1:]
        assert len(sents) == 5 and sents[pos-1] == odd
        body = "<p>Five jumbled sentences are given. Four of them can form a coherent paragraph. Enter the number of the sentence that does not fit.</p><ol class='pj'>" + "".join(f"<li>{x}</li>" for x in sents) + "</ol>"
        T(OS, "Hard", body, str(pos), f"Odd sentence: {pos}. {why}", kind="digit")

    # ---------- Para-jumbles (TITA, 4 sentences; every link is forced by a pronoun, connective or definition) ----------
    PJ = "Para-jumbles"
    jumbles = [
     (["Every language has words that resist translation into another.",
       "Among the most discussed are terms for emotions, such as the Portuguese 'saudade', a longing for something absent.",
       "Such words are often taken as proof that speakers of different languages feel differently.",
       "Yet the fact that a single word is missing does not mean the feeling is; English speakers can describe saudade perfectly well, they simply need a phrase to do it."],
      [3, 1, 4, 2], "The general claim (untranslatable words) opens. 'Among the most discussed' gives the emotion example, saudade. 'Such words … taken as proof' reacts to that example. 'Yet … English speakers can describe saudade' rebuts the inference and must come last, since it refers back both to saudade and to the 'proof'."),
     (["A lock is only as strong as the habits of the people who use it.",
       "For example, the most sophisticated door is useless if residents prop it open for deliveries.",
       "Security designers, having watched expensive locks defeated by a wedge of cardboard, now study behaviour as closely as hardware.",
       "Their aim is to make the secure action the easy one, so that people need not choose between safety and convenience."],
      [2, 4, 1, 3], "The opening claim (security depends on habits) is followed by its illustration (the propped-open door). 'For example' ties the door to the opening claim. The designers 'having watched expensive locks defeated by a wedge of cardboard' refers back to the propped-open door, and 'Their aim' needs the designers before it."),
     (["In the early eighteenth century, sailors had no reliable way to measure longitude at sea.",
       "The difficulty was that longitude depends on time: to know how far east or west you are, you must know the time at a reference place as well as your local time.",
       "Pendulum clocks, which kept good time on land, were thrown off by the motion of a ship.",
       "The problem was finally solved by a marine chronometer, a clock robust enough to keep accurate time through storms and changes of temperature."],
      [4, 1, 3, 2], "The problem is stated (no way to find longitude). 'The difficulty was' explains why: it depends on knowing time. Pendulum clocks fail at sea, the obvious attempt and its flaw. 'Finally solved by a marine chronometer' answers the failure of ordinary clocks and closes the paragraph."),
     (["Bees communicate the location of food through a movement known as the waggle dance.",
       "The angle of the dance relative to vertical indicates the direction of the food relative to the sun.",
       "The duration of the waggling run, meanwhile, signals how far away the food lies.",
       "Taken together, these two pieces of information allow other bees to fly almost directly to a source they have never visited."],
      [3, 4, 2, 1], "The waggle dance is introduced first. Its angle encodes direction. 'Meanwhile' adds the second variable, duration for distance. 'Taken together, these two pieces of information' needs both before it and comes last."),
    ]
    for correct_order, shown_pos, why in jumbles:
        # shown_pos[k] = label (1-4) shown for the k-th sentence of the correct paragraph
        assert sorted(shown_pos) == [1, 2, 3, 4]
        shown = sorted(range(4), key=lambda k: shown_pos[k])
        body = "<p>The four sentences below, when properly sequenced, form a coherent paragraph. Enter the sequence of the four numbers (e.g. 2143).</p><ol class='pj'>" + "".join(f"<li>{correct_order[k]}</li>" for k in shown) + "</ol>"
        ans = "".join(str(shown_pos[k]) for k in range(4))
        assert [correct_order[shown[int(c)-1]] for c in ans] == correct_order
        T(PJ, "Hard", body, ans, f"Correct order: {ans}. {why}", kind="sequence")
