"""CAT practice pack B16 — VARC: six original RC passages (4 Qs each) and verbal-ability items
(para-jumbles, para-summary, odd sentence out, para-completion), written for AptiSetu.
Every RC key is tied to a quoted line (asserted to occur in the passage); every para-jumble key is re-derived from
the shown order; every odd-sentence key is the position at which the odd sentence was inserted."""
import re
from varc import html_passage, wc
from b16_passages import P

def build(B):
    s = "varc"
    pos = iter([1, 3, 0, 2, 2, 0, 3, 1, 0, 2, 1, 3, 3, 1, 2, 0] * 6)
    def M(topic, diff, text, options, correct, solution, **k):
        o = [x for x in options if x != correct]; p = next(pos); o.insert(p, correct)
        assert not re.search(r"[Oo]ption \d|(first|second|third|fourth) option", solution), solution
        B.mcq(s, topic, diff, text, o, correct, solution, **k)
    T = lambda *a, **k: B.tita(s, *a, **k)
    for sid, (title, text) in P.items():
        assert 420 <= wc(text) <= 620, (sid, wc(text))
        B.add_set(sid, "passage", title, html_passage(title, text))
    RC = "Reading Comprehension"
    def R(sid, diff, q, opts, key, sol, quotes=()):
        for qt in quotes: assert qt in P[sid][1], (sid, qt)        # every line the solution relies on is really in the passage
        assert key in opts and len(set(opts)) == 4
        M(RC, diff, q, opts, key, sol, set_id=sid)

    # ---------------- RC1 introspection
    r = "b16-rc1"
    R(r,"Medium","The stockings experiment is used in the passage chiefly to show that:",
      ["people can sincerely give reasons for a choice that were not its actual cause",
       "people deliberately conceal the true reasons for their choices",
       "people prefer items placed on their right because of a habit of reading from left to right",
       "people cannot distinguish between products of similar quality"],
      "people can sincerely give reasons for a choice that were not its actual cause",
      "The choice 'was driven mostly by position', yet people cited softness or sheen and 'sincerely believed the reasons they gave'. 'Deliberately conceal' contradicts 'They were not lying'. The passage offers no explanation of the right-hand preference, and the point is not about telling products apart: the pairs were identical.",
      ["They were not lying. They sincerely believed the reasons they gave.", "driven mostly by position"])
    R(r,"Hard","Which of the following findings would most strengthen the view, described in the second paragraph, that we explain our own behaviour much as an outsider would?",
      ["Observers who merely read a description of an experiment predict the reasons participants will give about as accurately as the participants report them, and make the same errors.",
       "Participants who are told about position effects in advance no longer show them.",
       "People are usually accurate when they report which step of a calculation they are on.",
       "Participants give longer explanations for important decisions than for trivial ones."],
      "Observers who merely read a description of an experiment predict the reasons participants will give about as accurately as the participants report them, and make the same errors.",
      "The passage names the 'tell-tale sign': our explanations are 'no more accurate than the explanations a stranger would offer for us, and are wrong in the same ways'. The finding about observers matches that sign exactly. Removing the effect by warning people bears on the effect, not on how explanations are produced. Accuracy about steps in a sum is the passage's own example of genuine self-knowledge, which limits the thesis. Length of explanation is irrelevant.",
      ["no more accurate than the explanations a stranger would offer for us, and are wrong in the same ways"])
    R(r,"Medium","The author's reference to a person in pain and to someone working through a sum serves to:",
      ["limit the scope of the conclusion by giving cases where self-knowledge seems reliable",
       "show that the experiments were badly designed",
       "illustrate the kind of causes people fail to notice",
       "argue that introspection is more reliable than outside observation"],
      "limit the scope of the conclusion by giving cases where self-knowledge seems reliable",
      "The examples follow 'It would be easy to overstate the point' and show that the research does not make us 'wrong about everything inside us'. They qualify the claim rather than criticise the experiments. They are cases of knowledge, not of unnoticed causes, and the last paragraph treats outside evidence as the better guide, so the passage does not rank introspection higher.",
      ["It would be easy to overstate the point.", "A person in pain generally knows that she is in pain"])
    R(r,"Hard","It can be inferred that, according to the author, the reasons a job candidate gives for wanting a post are likely to reveal:",
      ["something about what the candidate and her culture regard as acceptable reasons, even if they misdescribe what moved her",
       "nothing at all, since self-reports are always false",
       "the candidate's true motives, provided she is sincere",
       "whether the candidate is lying, if her account is compared with a stranger's"],
      "something about what the candidate and her culture regard as acceptable reasons, even if they misdescribe what moved her",
      "Para 4: such answers 'tell us less about the person than we assume, and more about what that person, and the culture around her, regards as a respectable reason'. 'Nothing at all' and 'always false' overstate; the passage says explanations are 'partly constructions'. Sincerity does not secure accuracy (the stocking participants were sincere). Detecting lies is not discussed.",
      ["more about what that person, and the culture around her, regards as a respectable reason"])

    # ---------------- RC2 used clothing
    r = "b16-rc2"
    R(r,"Medium","The author's main purpose in the passage is to:",
      ["show that debates about the used-clothing trade confuse an empirical question about industry with a separate question about responsibility for waste",
       "argue that African governments should ban imports of used clothing",
       "defend the used-clothing trade as wholly beneficial to importing countries",
       "explain why textile factories in Africa were never competitive"],
      "show that debates about the used-clothing trade confuse an empirical question about industry with a separate question about responsibility for waste",
      "The final paragraph says 'A useful debate would separate these questions' and states each: harm to industry ('an empirical matter') and fairness of waste ('a question about responsibility'). The passage argues that a ban would likely fail, rejects 'benign' ('None of this makes the trade benign'), and never says the factories were never competitive.",
      ["A useful debate would separate these questions.", "None of this makes the trade benign."])
    R(r,"Hard","The critics' argument described in the second paragraph is most vulnerable to the objection that it:",
      ["infers that one development caused the factories' decline because the two happened at the same time, ignoring other causes in the same period",
       "relies on data from too few countries",
       "assumes that donors in wealthy countries act out of charity",
       "overlooks the fact that tariffs on used clothing have never been tried"],
      "infers that one development caused the factories' decline because the two happened at the same time, ignoring other causes in the same period",
      "The critics note that the decline 'coincided with' the flood of imports and 'draw the obvious conclusion'. Para 3 answers that 'The same decades saw other changes', such as tariff removal, unreliable power and cheap Asian clothing. That is the objection of inferring cause from coincidence while ignoring rivals. Sample size, donors' motives and untried tariffs are not the passage's objection.",
      ["coincided with a flood of imported second-hand clothing", "The same decades saw other changes"])
    R(r,"Medium","The comparison of the trade with 'a lottery' is meant to suggest that:",
      ["success in the trade depends on skill in managing uncertainty, not merely on chance",
       "traders are gamblers who usually lose money",
       "the trade should be regulated like gambling",
       "customers cannot know the quality of what they buy"],
      "success in the trade depends on skill in managing uncertainty, not merely on chance",
      "Right after the comparison: 'skill lies in judging suppliers, spotting quality and repairing what others would discard'. The uncertainty is the trader's, since no one knows a bale's contents until it is opened, and the point is that skill handles it. Losses, regulation, and customers' ignorance are not claimed.",
      ["the business resembles a lottery in which skill lies in judging suppliers"])
    R(r,"Hard","Which of the following best captures the author's view of the waste problem?",
      ["It reflects the scale of clothing consumption in donor countries, whose costs are shifted onto the importing countries",
       "It shows that Africans should stop buying used clothing",
       "It proves that the used-clothing trade has destroyed local industry",
       "It is caused mainly by careless disposal practices in the importing countries"],
      "It reflects the scale of clothing consumption in donor countries, whose costs are shifted onto the importing countries",
      "Para 5: importing countries 'bear the cost of disposing of clothes that the donors have, in effect, exported rather than thrown away', and 'The problem here is not that Africans buy used clothes but that rich countries consume clothing at a rate their own waste systems would struggle to absorb'. That rules out blaming buyers or local disposal, and the industry question is treated separately.",
      ["The problem here is not that Africans buy used clothes but that rich countries consume clothing"])

    # ---------------- RC3 wilderness
    r = "b16-rc3"
    R(r,"Medium","According to the passage, the 'error' of the park founders lay in:",
      ["equating protection with the absence of people and disregarding the inhabitants as part of what was protected",
       "trying to protect landscapes that were not in fact threatened",
       "allowing logging and mining inside the parks",
       "failing to draw boundaries around the parks"],
      "equating protection with the absence of people and disregarding the inhabitants as part of what was protected",
      "Para 3: 'The error lay in the idea that protection meant the absence of people, and in the assumption that the people who were there did not count as part of what was being protected.' The same paragraph says the threats 'were real', and the founders did draw boundaries.",
      ["The error lay in the idea that protection meant the absence of people"])
    R(r,"Hard","The example of grasslands turning to forest after burning stopped is used to support which claim?",
      ["Some landscapes valued as natural were maintained by human practices, so removing the people changed them.",
       "Fire is always beneficial to ecosystems.",
       "Early travellers were poor observers of nature.",
       "Forests are less valuable than grasslands."],
      "Some landscapes valued as natural were maintained by human practices, so removing the people changed them.",
      "Para 2 introduces the example to show 'how much of the 'wilderness' that visitors admire is the product of that management': when burning stopped, 'the very scenery the parks had been created to protect began to change'. The passage never says fire is always good, faults travellers, or ranks forests below grasslands.",
      ["the very scenery the parks had been created to protect began to change"])
    R(r,"Medium","The author draws attention to the word 'intact' in order to point out that:",
      ["the language of funding can carry an unstated assumption that human presence is damage",
       "funders prefer large projects to small ones",
       "communities inside parks have destroyed the habitats they live in",
       "conservationists have stopped using the word 'wilderness'"],
      "the language of funding can carry an unstated assumption that human presence is damage",
      "Para 4: funding flows to projects that keep areas 'intact', 'a word that quietly implies that human presence is a form of damage'. The passage says nothing about project size, says communities' practices may have helped shape habitats, and calls the 'wilderness' idea persistent rather than abandoned.",
      ["a word that quietly implies that human presence is a form of damage"])
    R(r,"Hard","Which of the following policies would the author be most likely to support?",
      ["Inviting a community expelled from a park to resume seasonal burning under its own guidance, with the park's support",
       "Abolishing protected areas and returning all land to private ownership",
       "Fencing parks more strictly to keep out every form of human use",
       "Allowing industrial logging inside parks to fund conservation"],
      "Inviting a community expelled from a park to resume seasonal burning under its own guidance, with the park's support",
      "Para 5: 'The alternative is not to abolish protected areas but to rethink what they are for', and some parks are 'restoring traditional burning under the guidance of the communities that once practised it'. Abolition is explicitly rejected, strict exclusion is the error the passage criticises, and industrial logging is one of the real threats the parks were right to resist.",
      ["The alternative is not to abolish protected areas", "restoring traditional burning under the guidance of the communities"])

    # ---------------- RC4 tipping
    r = "b16-rc4"
    R(r,"Medium","According to the passage, why have individual restaurants that abolished tipping often reverted?",
      ["Their prices looked higher than rivals' even when the final bill was similar, so customers chose the rivals",
       "Their staff provided worse service once tips were removed",
       "Laws required them to permit tipping",
       "Customers refused to pay for service at all"],
      "Their prices looked higher than rivals' even when the final bill was similar, so customers chose the rivals",
      "Para 3: a menu without tips must show prices 'about a fifth higher', customers 'tend to choose the restaurant that looks cheaper, even when the final bill would be the same', which is 'why such experiments have so often failed'. Worse service, legal requirements and refusal to pay are not mentioned.",
      ["A restaurant that abolishes tipping on its own therefore appears more expensive than its rivals"])
    R(r,"Hard","The evidence cited in the second paragraph most directly undermines which claim?",
      ["Tipping motivates servers to provide better service.",
       "Tipping makes prices on menus look lower.",
       "Customers enjoy feeling generous.",
       "Tips vary with servers' appearance."],
      "Tipping motivates servers to provide better service.",
      "Para 2 sets out 'the standard defence', that tipping rewards good service, and then finds 'only a small connection' between tips and rated service. That evidence targets the incentive claim. Price disguise and the pleasure of giving are later explanations the passage takes seriously, and variation with appearance is one of its own findings.",
      ["The standard defence of tipping is that it rewards good service.", "only a small connection between the two"])
    R(r,"Hard","The author mentions that a gift 'can be withheld' in order to:",
      ["explain why depending on tips exposes workers to customers' prejudices",
       "argue that customers should stop tipping",
       "show that tipping improves service",
       "suggest that servers prefer gifts to wages"],
      "explain why depending on tips exposes workers to customers' prejudices",
      "'A gift, unlike a wage, can be withheld, and those who depend on it are exposed to the prejudices as well as the generosity of strangers', supported by research on appearance, age and ethnicity. The passage does not urge customers to stop, contradicts the service claim, and says nothing about servers' preferences.",
      ["exposed to the prejudices as well as the generosity of strangers"])
    R(r,"Medium","Which of the following is consistent with the author's discussion of remedies?",
      ["If price disguise is the main cause, a rule requiring all restaurants to show all-inclusive prices at the same time would address it",
       "If customers value giving, tipping should be banned by law",
       "Market competition alone will eventually eliminate tipping",
       "A guaranteed base wage would increase the size of tips"],
      "If price disguise is the main cause, a rule requiring all restaurants to show all-inclusive prices at the same time would address it",
      "Para 5: if tipping 'survives mainly because it hides prices, then the solution lies in rules that require all-inclusive pricing for every restaurant at once'. If customers value giving, abolition 'may be neither achievable nor entirely desirable', so a ban does not follow. The last paragraph doubts that market pressure alone will end the custom, and a base wage is proposed to limit damage, not to raise tips.",
      ["require all-inclusive pricing for every restaurant at once", "unlikely to disappear through market pressure alone"])

    # ---------------- RC5 beauty
    r = "b16-rc5"
    R(r,"Medium","The example of circular orbits and ellipses is used by the sceptics to argue that:",
      ["standards of beauty change to fit successful theories, so beauty cannot independently test them",
       "ellipses are more beautiful than circles",
       "early astronomers had no interest in elegance",
       "simple theories are always false"],
      "standards of beauty change to fit successful theories, so beauty cannot independently test them",
      "Para 2: circles were admired, ellipses 'at first thought ugly', and 'If the standard of beauty shifts to accommodate whatever theories succeed, then beauty cannot be an independent test of success.' The other options misread the example or overstate it.",
      ["then beauty cannot be an independent test of success"])
    R(r,"Hard","On the 'more modest version' of the aesthetic criterion, elegance is valuable because:",
      ["theories with fewer adjustable parts make sharper predictions and are easier to refute",
       "nature itself is fundamentally beautiful",
       "beautiful theories are more likely to attract funding",
       "simple theories are easier to teach to students"],
      "theories with fewer adjustable parts make sharper predictions and are easier to refute",
      "Para 3: simplicity is preferred 'because a theory with fewer adjustable parts makes sharper predictions and is easier to refute', valuable 'not as a sign that nature itself is beautiful but as a practical virtue'. Funding and teaching are not the modest version's reasons.",
      ["makes sharper predictions and is easier to refute", "not as a sign that nature itself is beautiful"])
    R(r,"Hard","Which scientist's conduct would the author regard as having 'left science for something closer to taste'?",
      ["One who keeps defending a theory without any testable prediction because it is too elegant to be wrong",
       "One who prefers the simpler of two theories because it is easier to test",
       "One who abandons an elegant theory after an experiment refutes it",
       "One who pursues an elegant idea to see whether it yields testable predictions"],
      "One who keeps defending a theory without any testable prediction because it is too elegant to be wrong",
      "Para 5 contrasts using elegance 'as a tool' (preferring the easier-to-test theory) with believing a theory 'because it is too beautiful to be wrong', which makes elegance 'a substitute for the test'. Abandoning a refuted theory and pursuing an idea to test it are ordinary science, and preferring the testable theory is the passage's example of the tool.",
      ["too beautiful to be wrong", "something closer to taste"])
    R(r,"Medium","The passage suggests that the risk described in the final paragraph is greatest when:",
      ["decisive tests of competing theories never become possible",
       "experiments confirm an elegant theory",
       "physicists disagree about the meaning of beauty",
       "a theory has many adjustable parts"],
      "decisive tests of competing theories never become possible",
      "'If they never do, the field risks becoming a contest of aesthetic preferences'. If tests arrive, the theory 'will be confirmed or refuted like any other'. Disagreement about beauty and many adjustable parts are not identified as the condition for that risk.",
      ["If they never do, the field risks becoming a contest of aesthetic preferences"])

    # ---------------- RC6 octopus
    r = "b16-rc6"
    R(r,"Medium","The detail about a severed arm reaching for food is offered mainly to illustrate that:",
      ["much of the octopus's nervous control is distributed in its arms rather than centralised",
       "octopuses can regrow lost limbs",
       "octopuses feel pain in their arms",
       "the octopus brain is larger than once thought"],
      "much of the octopus's nervous control is distributed in its arms rather than centralised",
      "The example follows 'Most of an octopus's neurons are not in its central brain but in its arms, each of which can … respond … with a degree of independence.' Regrowth, pain and brain size are not what the detail shows.",
      ["Most of an octopus's neurons are not in its central brain but in its arms"])
    R(r,"Hard","How does the author respond to the critics who say that wound-tending behaviour does not prove feeling?",
      ["By conceding the point but noting that the same is true of the evidence we accept for other animals, so it does not settle the matter",
       "By rejecting it, since the behaviour proves sentience beyond doubt",
       "By arguing that machines also feel pain",
       "By pointing out that octopuses share our anatomy"],
      "By conceding the point but noting that the same is true of the evidence we accept for other animals, so it does not settle the matter",
      "'This is true, but it proves less than the critics hope. The same could be said of any animal other than oneself.' The author concedes, then generalises the objection. 'Beyond doubt' contradicts the concession, the passage never says machines feel, and it says the anatomical similarity 'is missing'.",
      ["This is true, but it proves less than the critics hope.", "In the octopus the anatomical similarity is missing"])
    R(r,"Medium","The 'increasingly influential' view described in the fifth paragraph holds that:",
      ["where suffering is a realistic possibility, those who would impose harmful conditions must justify them",
       "protection should await proof that an animal is sentient",
       "octopuses certainly feel pain as humans do",
       "farming octopuses is acceptable if painkillers are used"],
      "where suffering is a realistic possibility, those who would impose harmful conditions must justify them",
      "That view says that 'the burden of proof should fall on those who would subject it to conditions likely to cause suffering', and it 'does not claim to know what the octopus feels'. Waiting for proof is the opposing view; certainty and painkiller-based farming are not part of it.",
      ["the burden of proof should fall on those who would subject it to conditions likely to cause suffering"])
    R(r,"Hard","The final paragraph suggests that the octopus challenges us chiefly because:",
      ["it may have a rich mind that does not resemble ours, which calls into question our habit of extending concern by resemblance",
       "it is more intelligent than mammals",
       "science has proved that it is sentient",
       "its evolutionary history is unknown"],
      "it may have a rich mind that does not resemble ours, which calls into question our habit of extending concern by resemblance",
      "'We are used to extending moral concern along lines of resemblance. An animal whose mind may be rich but is certainly strange invites us to ask whether resemblance was ever the right guide.' The passage ranks no animal above mammals, stresses uncertainty rather than proof, and describes the octopus's evolutionary history.",
      ["whether resemblance was ever the right guide", "a test less of our science than of our habits of reasoning"])
    build_va(B, M, T)

def build_va(B, M, T):
    # ---------- Para-summary
    PS = "Para-summary"
    summaries = [
     ("Hard", "A ship's captain who runs aground in fog is judged harshly; one who takes the same route in the same fog and arrives safely is not judged at all. Inquiries into accidents therefore study only the voyages that went wrong, and conclude that the decisions taken on them were reckless. Yet if the same decisions were taken routinely on voyages that succeeded, they are not what distinguishes failure from success, and correcting them may achieve little. An honest inquiry would ask how often the fatal choice was made without consequence.",
      ["Inquiries that examine only failures may blame choices that were equally common in successes, and so misidentify what causes accidents.",
       "Captains who sail in fog are reckless whether or not they arrive safely.",
       "Accident inquiries should be abolished because they are biased.",
       "Successful voyages teach more than failed ones."], 0,
      "The paragraph's point is that studying only failures can blame decisions that also occurred in successes, and so misidentify causes; hence 'ask how often the fatal choice was made without consequence'. Calling all fog-sailing reckless reverses the point, abolition is never proposed, and the paragraph does not rank successes above failures."),
     ("Medium", "Planners laying out a new university campus once left the lawns between its buildings unpaved for a year. By the end of it, students had worn bare tracks across the grass along the routes they actually walked, and the planners paved those tracks. Paths designed in advance express a guess about how people will move; paths worn by use record how they do. Where a design can wait for that record, it can avoid the familiar sight of fenced-off lawns that people cross anyway.",
      ["Students prefer walking on grass to walking on paved paths.",
       "Designs that wait to observe how people actually behave can fit that behaviour better than designs based on advance guesses.",
       "Campus lawns should never be paved.",
       "Fences are an effective way to keep people off lawns."], 1,
      "The paragraph contrasts paths that 'express a guess' with paths that 'record how they do', and recommends waiting for the record. The option about observing actual behaviour states that lesson. The students walked on tracks that were later paved, so they did not prefer grass as such; 'never be paved' contradicts the planners' action; and the fenced lawns 'people cross anyway' show fences failing."),
     ("Hard", "Shops make a large share of their profit on electrical goods not from the goods but from extended warranties sold at the till. The warranties are profitable because the faults they cover are rare and the repairs cheap compared with the price charged. Customers buy them anyway, partly because a breakdown is easy to picture at the moment of purchase, and partly because a single large loss feels worse than many small payments of the same total. A buyer who could afford to replace the item would, on average, do better by taking the risk herself.",
      ["Electrical goods break down more often than customers expect.",
       "Shops should be prohibited from selling extended warranties.",
       "Warranties profit sellers because buyers overweight vivid but unlikely losses, so buyers who can bear the risk would usually do better to decline them.",
       "Most buyers cannot afford to replace electrical goods."], 2,
      "The paragraph explains why warranties are profitable (rare faults, cheap repairs), why people buy them (vivid breakdowns, dislike of one large loss), and concludes that a buyer who can bear the risk does better without one. The option about overweighted losses captures all three. Faults are said to be 'rare', a ban is never proposed, and the paragraph does not say most buyers cannot afford replacement."),
     ("Hard", "A company that measures customer service by how quickly calls are answered will soon have calls answered quickly. Whether customers are helped is another matter: an agent rewarded for speed has every reason to end a call before the problem is solved, and a customer who must call back three times generates three quickly answered calls. The number improves while the service it was meant to track gets worse.",
      ["Call centres should hire more agents to reduce waiting times.",
       "Customers prefer to have their calls answered quickly.",
       "Agents who are rewarded for speed are less skilled than others.",
       "When a measure becomes the target, people can improve the measure in ways that defeat the purpose it was meant to serve."], 3,
      "The example shows the number improving while 'the service it was meant to track gets worse', because agents optimise the metric itself. The option about a measure becoming the target generalises exactly that. Hiring and customer preference are not the point, and agents' skill is not discussed."),
     ("Medium", "Old farming terraces on steep hillsides can look like monuments to backbreaking toil, and in a sense they are. But they are also machines for managing water. Each level slows the runoff from the one above, letting rain soak into the soil instead of carrying it away. When terraces are abandoned and their walls collapse, the slopes below often suffer floods and landslides that the terraces had long prevented.",
      ["Terraced farming is too laborious to be worth continuing.",
       "Besides representing great labour, terraces perform a continuing function in controlling water, which is lost when they are abandoned.",
       "Hillside floods are caused mainly by heavy rainfall.",
       "Terraces were built mainly to increase the area of flat land."], 1,
      "The paragraph moves from terraces as 'monuments to backbreaking toil' to their role as 'machines for managing water', and shows what is lost when they collapse. The option about a continuing water-control function lost on abandonment captures both. The paragraph does not argue against terracing, blame rainfall alone, or discuss the area of flat land."),
     ("Hard", "A cinema that sells a small popcorn for ₹150 and a large one for ₹300 finds that most customers buy the small. When it adds a medium at ₹270, sales of the large rise sharply, though almost nobody buys the medium. The medium's job is not to be chosen but to make the large look like a bargain beside it. Choices that seem to be judgements of each option's worth are often judgements of how the options compare with one another.",
      ["Cinemas earn most of their profit from popcorn.",
       "Customers usually prefer medium-sized portions.",
       "Raising prices is an effective way of increasing sales.",
       "An option that few people choose can still change what they choose, because options are judged largely by comparison with the alternatives on offer."], 3,
      "The medium is almost never bought but shifts sales to the large, and the last sentence generalises: choices are 'judgements of how the options compare with one another'. The option about an unchosen option changing choices states this. Profit share is not discussed, 'almost nobody buys the medium' contradicts a preference for it, and no price was raised."),
    ]
    for diff, para, opts, k, why in summaries:
        M(PS, diff, f"<p>The passage given below is followed by four summaries. Choose the option that best captures the essence of the passage.</p><blockquote class='ps'>{para}</blockquote>", opts, opts[k], why)

    # ---------- Para-completion
    PC = "Para-completion"
    comps = [
     ("Hard", "In the 1840s a doctor in Vienna noticed that mothers whose babies were delivered by doctors died of fever far more often than those attended by midwives. He traced the difference to doctors who came to the ward straight from dissecting corpses, and when he required them to wash their hands in a chlorine solution, deaths fell sharply. ____ It took the germ theory of disease, decades later, to supply the explanation that made his practice impossible to ignore.",
      ["Yet many of his colleagues rejected the practice, partly because he could not explain why it worked.",
       "His method was at once adopted by hospitals across Europe.",
       "Midwives had always washed their hands more carefully than doctors.",
       "Chlorine had long been used to clean hospital floors."], 0,
      "The final sentence says a later theory made the practice 'impossible to ignore', so the gap must say that it was ignored or resisted for lack of an explanation. 'At once adopted' contradicts that; the claim about midwives is unsupported and does not lead to the explanation; the floor-cleaning sentence is irrelevant."),
     ("Hard", "A new species of beetle is often described from a single specimen in a museum drawer. ____ The result is that for many insects we know the shape of one individual in great detail and almost nothing about how the species lives: what it eats, where it breeds, or whether it is still found anywhere at all.",
      ["Beetles are the most numerous group of animals on earth.",
       "Museums have stopped collecting insects in recent decades.",
       "The specimen is measured, drawn and named, but the animal is seldom observed alive.",
       "Every specimen must be examined by at least two experts."], 2,
      "'The result is that' needs a cause: a detailed description of one dead individual without study of the living animal. The option about measuring and naming a specimen seldom seen alive supplies both halves of the contrast that follows. The other options do not explain why we know shape 'in great detail' but not behaviour."),
     ("Medium", "Speed bumps slow traffic, but drivers dislike them and some accelerate hard between them, adding noise and fumes. Planners have experimented with an alternative: narrowing the road with planters and parked cars so that it simply feels too tight for speed. ____ Drivers who would resent an obstacle adjust without complaint to a street that seems to require care.",
      ["Speed bumps are cheaper to build than planters.",
       "The narrower streets often slow traffic as much as bumps do, with less resentment.",
       "Many drivers prefer wide roads to narrow ones.",
       "Planters must be watered regularly."], 1,
      "The last sentence explains a success ('adjust without complaint'), so the gap must report that success: narrowing slows traffic as much as bumps 'with less resentment'. Cost, preference for wide roads and watering do not prepare the final explanation."),
     ("Medium", "After a walk in the hills, a Swiss engineer found burrs clinging to his trousers and to his dog's coat. Under a microscope he saw that each burr was covered in tiny hooks that caught on loops of fibre. ____ The fastener he developed from this observation, two strips of fabric covered in hooks and loops, is now found on everything from shoes to spacecraft.",
      ["He decided to study plants that spread their seeds by wind instead.",
       "Burrs are a nuisance to farmers and walkers alike.",
       "It occurred to him that the same arrangement, made artificially, could join two surfaces that could be pulled apart and closed again.",
       "Dogs with long coats collect more burrs than dogs with short ones."], 2,
      "The gap must link the microscope observation (hooks catching loops) to the invention that follows. Only the sentence about copying the arrangement to join and reopen two surfaces makes that link. Wind-borne seeds would lead away from the invention, and the other two sentences are side remarks."),
     ("Medium", "Students who reread their notes before an exam usually feel well prepared. The material looks familiar, and familiarity is easily mistaken for knowledge. ____ Those who instead test themselves, by closing the book and trying to recall what they have read, often feel less confident but remember more.",
      ["Rereading is therefore the most efficient way to study.",
       "Yet recognising something on the page is not the same as being able to recall it without help.",
       "Most students prefer studying in groups.",
       "Exams have become harder in recent years."], 1,
      "The gap must separate familiarity from knowledge before the paragraph introduces self-testing. The 'recognising is not recalling' sentence does that and sets up the contrast with recall. 'Most efficient' contradicts the paragraph, and group study and exam difficulty are off topic."),
     ("Hard", "Firms that offer unlimited paid holiday often find that employees take fewer days off than they did under a fixed allowance. ____ Without a number to aim at, people look to their colleagues for a sense of what is acceptable, and no one wants to be the person who takes the most.",
      ["Unlimited holiday is therefore a dishonest policy.",
       "Employees under fixed allowances never use all their days.",
       "Managers usually refuse requests for leave.",
       "The reason is that an allowance, as well as limiting leave, also tells people how much they are expected to take."], 3,
      "The sentence after the gap explains behaviour once the number is gone, so the gap must say what the number did: an allowance also signals how much leave is expected. Calling the policy dishonest is a judgement the paragraph does not make; 'never use all their days' and refusals by managers are not supported and do not lead to the explanation that follows."),
    ]
    for diff, para, opts, k, why in comps:
        assert para.count("____") == 1
        M(PC, diff, f"<p>There is a sentence that is missing in the paragraph below. Read the paragraph and choose the option that best completes it.</p><p>{para}</p>", opts, opts[k], why)

    # ---------- Odd sentence out
    OS = "Odd sentence out"
    odds = [
     ("Hard", ["Bridges in cold regions are fitted with expansion joints, gaps that let the deck lengthen in summer and shrink in winter.",
       "Without them, the steel or concrete would push against the supports with enormous force as temperatures rose.",
       "Over time this stress would crack the structure or bend it out of shape.",
       "The joints therefore allow a bridge to change size safely instead of resisting the change."],
      "Suspension bridges can span far greater distances than beam bridges of the same weight.", 4,
      "Sentences 1, 2, 3 and 5 explain expansion joints: what they are, the force they relieve, the damage avoided, and the conclusion. The sentence on suspension bridges concerns bridges but compares spans and plays no part in the thermal argument."),
     ("Medium", ["Seed banks store the seeds of crop varieties at low temperatures so that they remain alive for decades.",
       "Many of these varieties are no longer grown by farmers, who have switched to a few high-yielding types.",
       "If a disease attacks the high-yielding crops, breeders can search the stored varieties for genes that resist it.",
       "A seed bank is thus less a museum of old crops than an insurance policy for new ones."],
      "Supermarkets now stock a wider range of imported vegetables than they did a generation ago.", 3,
      "Sentences 1, 2, 4 and 5 explain what seed banks store, why those varieties matter now that farmers grow only a few, how breeders use them against disease, and the conclusion. The sentence on supermarket ranges concerns food variety for shoppers, not the conservation of crop genes."),
     ("Hard", ["A household that buys a more fuel-efficient car may end up driving more, because each journey now costs less.",
       "Economists call this the rebound effect.",
       "Its size varies: sometimes it eats up a small part of the expected saving, occasionally most of it.",
       "Policies built on efficiency alone should therefore expect smaller savings than the engineering figures suggest."],
      "Electric cars produce no exhaust emissions at the point of use.", 2,
      "Sentences 1, 3, 4 and 5 define the rebound effect, name it, describe its size and draw the policy conclusion. The electric-car sentence is about cars and emissions, but it introduces a different technology and claim and breaks the chain between the example and 'Economists call this'."),
     ("Medium", ["Parents often praise children for being clever when they solve a problem.",
       "Studies suggest that children praised this way may avoid harder tasks afterwards, for fear of losing the label.",
       "Children praised instead for the effort they made are more willing to attempt difficult problems.",
       "The kind of praise, not just its amount, appears to shape how children approach challenges."],
      "Children's vocabulary grows fastest between the ages of two and six.", 5,
      "Sentences 1–4 compare praise for cleverness with praise for effort and conclude that the kind of praise matters. The vocabulary sentence is about child development but has nothing to do with praise or challenge."),
     ("Medium", ["Cities that plan for floods have begun to design parks that can be safely submerged.",
       "In dry weather they serve as playgrounds and sports fields.",
       "During heavy rain they fill with water that would otherwise flood streets and homes.",
       "The same land thus does two jobs, each at a different time."],
      "Many of the oldest city parks in Europe began as private hunting grounds of the nobility.", 1,
      "Sentences 2–5 describe the floodable park: its design, its dry-weather use, its use in storms, and the conclusion about dual use. The sentence on hunting grounds is about parks but concerns their history, not flood design."),
     ("Hard", ["Some orchestras now audition players from behind a screen, so that judges hear the playing but cannot see the player.",
       "When such screens were introduced, the share of women hired rose noticeably.",
       "The change suggested that judges had been influenced by what they saw, not only by what they heard.",
       "Blind auditions thus offered a way to remove one source of bias without having to change the judges' minds."],
      "Violins made by famous craftsmen centuries ago are among the most expensive instruments in the world.", 4,
      "Sentences 1, 2, 3 and 5 describe screened auditions, their effect on hiring women, what that implied, and why the method works. The sentence on the price of old violins is about orchestral music but not about auditions or bias."),
    ]
    for diff, good, odd, p, why in odds:
        sents = good[:p-1] + [odd] + good[p-1:]
        assert len(sents) == 5 and sents[p-1] == odd and sents.index(odd) == p - 1
        body = "<p>Five jumbled sentences related to a topic are given below. Four of them can be put together to form a coherent paragraph. Identify the odd one out and key in its number.</p><ol class='pj'>" + "".join(f"<li>{x}</li>" for x in sents) + "</ol>"
        T(OS, diff, body, str(p), f"Odd sentence: {p}. {why}", kind="digit")

    # ---------- Para-jumbles (TITA). correct = sentences in the right order; shown = label shown for each, in that order
    PJ = "Para-jumbles"
    jumbles = [
     ("Medium", ["For centuries, sailors feared a disease that loosened their teeth and reopened old wounds on long voyages.",
       "Its cause, a lack of vitamin C, was not understood, and remedies ranged from vinegar to sea water.",
       "One of the few that worked, citrus juice, was repeatedly discovered and then forgotten.",
       "It was forgotten partly because boiling the juice to preserve it destroyed the very substance that made it effective."],
      [3, 1, 4, 2], "The disease is introduced first. 'Its cause … remedies ranged' follows. 'One of the few that worked' picks a remedy from that range. 'It was forgotten partly because' explains the forgetting just mentioned, so it must come last."),
     ("Medium", ["A forest fire seems to destroy everything in its path.",
       "Yet some trees depend on it: their cones open only in intense heat, releasing seeds onto ground cleared of competitors.",
       "For such species, preventing every fire can be as harmful as an unusually severe one.",
       "Fire managers have therefore begun to allow, and sometimes to set, small controlled burns."],
      [2, 4, 1, 3], "The common view opens. 'Yet some trees depend on it' qualifies it. 'For such species' refers back to those trees. 'Therefore … controlled burns' draws the practical conclusion and ends the paragraph."),
     ("Hard", ["Most of us assume that we would notice a large change in what we are looking at.",
       "In experiments, however, people often fail to see a person in a gorilla suit walk through a scene while they are counting passes in a ball game.",
       "This failure is not a defect of the eyes but a consequence of attention, which selects a small part of what the eyes take in.",
       "What we see, in other words, is shaped as much by what we are looking for as by what is there."],
      [4, 2, 3, 1], "The assumption comes first; 'however' introduces the experiment that contradicts it; 'This failure' explains the failure in the experiment; 'in other words' restates the explanation as a general conclusion."),
     ("Medium", ["Noise-cancelling headphones do not simply block sound; they add sound.",
       "A small microphone picks up the steady noise around the listener, such as the hum of an aircraft engine.",
       "The headphones then produce a sound wave that is its exact mirror image, so that the two cancel each other out.",
       "This works well for steady, low sounds but poorly for sudden ones such as voices, which change too quickly to be matched."],
      [4, 1, 3, 2], "The claim that the headphones 'add sound' opens. The microphone picking up noise comes next. 'then produce a sound wave that is its exact mirror image' needs that noise. 'This works well' evaluates the whole process and ends the paragraph."),
     ("Hard", ["When barcodes were first proposed for groceries, the technology was not the main obstacle.",
       "The obstacle was coordination: a barcode was useless to a shop unless manufacturers printed it, and manufacturers had no reason to print it until shops could read it.",
       "Each side was waiting for the other to move first.",
       "The deadlock was broken when an industry committee agreed on a single standard and large supermarket chains committed to installing scanners.",
       "Once enough products carried codes, the remaining manufacturers had to adopt them, and the problem of coordination turned into a pressure to conform."],
      [4, 2, 5, 3, 1], "'The technology was not the main obstacle' sets up 'The obstacle was coordination', which explains the mutual dependence. 'Each side was waiting' sums up that dependence. 'The deadlock was broken' needs the deadlock. 'Once enough products carried codes' describes what followed and ends the paragraph."),
     ("Hard", ["Hospitals once measured success mainly by whether patients survived an operation.",
       "As survival rates rose, that measure began to say less and less about the quality of care.",
       "Attention shifted to what happened afterwards: how long patients took to recover, and whether they could live as they had before.",
       "These later outcomes are harder to record, since they unfold over months and outside the hospital.",
       "But they are closer to what patients themselves care about, which is why many hospitals now try to track them."],
      [3, 5, 1, 4, 2], "The old measure opens. 'As survival rates rose, that measure' needs it. 'Attention shifted to what happened afterwards' introduces the new outcomes. 'These later outcomes are harder to record' refers to them. 'But they are closer to what patients care about' answers that difficulty and closes the paragraph."),
    ]
    for diff, correct, shown_pos, why in jumbles:
        n = len(correct); assert sorted(shown_pos) == list(range(1, n + 1))
        shown = sorted(range(n), key=lambda k: shown_pos[k])
        word = "four" if n == 4 else "five"; eg = "2143" if n == 4 else "21435"
        body = f"<p>The {word} sentences below, when properly sequenced, form a coherent paragraph. Enter the sequence of the {word} numbers (e.g. {eg}).</p><ol class='pj'>" + "".join(f"<li>{correct[k]}</li>" for k in shown) + "</ol>"
        ans = "".join(str(shown_pos[k]) for k in range(n))
        assert [correct[shown[int(c)-1]] for c in ans] == correct
        T(PJ, diff, body, ans, f"Correct order: {ans}. {why}", kind="sequence")
