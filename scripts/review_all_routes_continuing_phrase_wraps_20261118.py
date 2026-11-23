"""Review the twenty-three flagged wraps and one name-order correction."""

from inspect import getsource

from scripts import register_all_routes_followup_phrase_wraps_20261118 as parent
from scripts import review_rafael_early_phrase_wraps_20261118 as common
from scripts.source_locked_derivation_v5118 import checked_text

base, TOKEN, logical, GATES = common.base, common.TOKEN, common.logical, common.GATES
ROOT = parent.stage.ROOT.parent.with_name("all_routes_continuing_phrase_wraps_20261118")
SOURCE, OUTPUT = ROOT / "paired_source_with_name.json", ROOT / "contextual_review_v3.json"
BLOCKS = ((234, 235, 237, 251, 252), (243, 250, 255, 292, 294), (82, 92, 121, 124, 127, 20), (48, 53, 54, 55, 87))
QUEUE = parent.stage.ROOT / "followup_wrap_queue.json"
CONTEXT = {
    234: "Gerhard explains how a story of Noritsune's courage moved him, and Rafael recognizes what it meant to him.",
    235: "Ian's letter recounts what a book says about Timur's mail and suggests an investigation. Rafael and Cesare discuss why Ian knows the history.",
    237: "Children are playing at being Charles Martel. Gerhard explains why people in the region remember his victory and tells Rafael his own deeds matter too.",
    251: "A woman describes the glass rose her father bought and reports a swindler rumor. Rafael and Clau discuss the difference between suspicion and a useful lead.",
    252: "The tavern keeper chases off the swindler, returns the object and says what he will do if the man comes back.",
    243: "The priest explains the strange figurehead, says that most people cannot take it safely, and offers the crew a chance to try.",
    250: "After settling the reward and expenses in Sofala, the guildmaster tells Hodram about a nearby ruin and a legend attached to it.",
    255: "The woman greets Hodram by name and answers his question about well-known ruins.",
    292: "The guildmaster hopes Hodram can hunt the creature fishermen blame for several lost ships. Hodram warns that finding it will take luck.",
    294: "In an overgrown site the group wants out of the forest, then tries to make sense of the evidence the previous visitors left.",
    82: "A sailor provokes Fernando by doubting Lil, then surprises him by defending people who believe in miracles. He apologizes and introduces his charm.",
    92: "Julio worries about Cristina despite Lil's reassurances. The comparison to Minerva reminds him of a legendary shield he would like her to have.",
    121: "Camille rejoins Lil and acknowledges Hodram and Maria. They move from polite thanks to teasing each other about what each did to help.",
    124: "Julian tells Lil what a friendly barmaid can tell a sailor. His advice about gifts sets up Lil's joke about his flirting.",
    127: "Fernando explains what insight does for a gambler and invites Camille to guess how it relates to luck.",
    20: "Gerhard recognizes the pirate who warned Lil out of his territory. Use the name order spoken elsewhere and shown in the corresponding portrait header.",
    48: "Rafael explains to Maria what he hopes for Portugal. She challenges his premises and he apologizes when he takes her approval for criticism.",
    53: "Maria has completed the collection. Xien wonders why nothing happens and the crew discusses whether anything else is needed.",
    54: "The parallel completion branch uses the same exchange about the collection and the absence of a spectacular effect.",
    55: "Bianca says goodbye and Angelo protests. She asks him to live for himself and reminds him that he has people around him.",
    87: "The Sphinx's riddle has two existing pages and original answer choices. Later Xien asks Maria to solve it and her arithmetic leads them to two adults.",
}
NOTES = {
    234: """
39|Noritsune disappeared into the strait in his armor with two enemy soldiers.|The reported account keeps the specific details that Rafael repeats.
42|Gerhard is struck by the warrior's courage.|The phrasing preserves Gerhard's viewpoint and the contrast he makes.
46|Rafael admires that courage.|The simple response follows Gerhard's emotional story.
51|Gerhard says such men are unusual now.|His brief agreement leaves Rafael room to address him directly.
55|Rafael notices how deeply Gerhard was moved.|Keep the personal address and the force of the emotion in a single thought.
59|Rafael repeats the image of the armor going into the strait.|The ellipsis keeps him still thinking about the story.
63|Gerhard realizes he went on at length and returns to work.|The practical close fits his reserved manner.
""",
    235: """
37|The mail was buried with Timur and stolen decades later.|The exact sequence keeps the burial distinct from the robbery.
40|The thieves died in the desert shortly before reaching sight of the sea.|The location clue remains tied to their attempted escape.
44|That fate stayed unknown and the mail has never been found.|The wording preserves the report's uncertainty and unresolved object.
48|Ian invites investigation if Rafael is interested and signs the letter.|A complete invitation stands above the same signature.
56|Rafael is surprised Ian knows Asian history.|His curiosity motivates Cesare's explanation.
68|The Mongol Empire ruled and was long an enemy of the Russian people.|The historical point stays in Cesare's explanation of Ian's interest.
71|Rafael compliments Cesare's knowledge.|The brief response closes the exchange naturally.
""",
    237: """
25|Gerhard names Charles Martel and dates him to more than eight centuries before.|Both facts answer Rafael's question.
28|Martel repelled an army that had advanced through Iberia.|Preserve the named places, direction and outcome as Gerhard recounts them.
31|Rafael asks why this particular victor is a hero.|The question calls for meaning beyond the outcome.
36|Gerhard says the significance of the victory is what matters.|Give him a clear lead-in to his explanation in the next turn.
40|Gerhard speculates about how Europe would have changed if Martel had lost.|The conditional belongs to the character's account.
44|Rafael understands why the children admire him.|The conclusion links the history to the opening game.
49|Gerhard says Rafael's deeds are worthy too.|The formal address keeps the compliment in his voice.
""",
    251: """
91|She says something she treasured was stolen.|The hesitation keeps the personal importance ahead of the object's price.
95|Rafael asks what it was.|His simple question lets her explain.
100|Her father bought her a glass ornament for her birthday because she loves roses.|Keep the uncertain monetary value, her father, the occasion and the roses without leaving a contraction dangling.
103|The ornament looks like a real rose frozen in glass and she loved it.|The image is revealed in the same turn as in the Japanese.
107|Clau asks who stole it.|His sympathy fits the turn from memories to recovery.
110|She doesn't know who did it.|The bare answer limits what they can conclude.
119|She heard of a Havana swindler who passes glass off as gems.|The secondhand link connects the rose to Havana without proving theft.
122|Clau doubts that being a swindler proves he stole the rose.|The distinction explains why Rafael has to argue for going.
126|Rafael thinks a trip to Havana may produce information.|The statement gives a reason without promising a result.
130|Clau objects to crossing the Atlantic on such a weak lead.|The sharp question keeps the distance and risk.
133|Rafael says waiting might be too late if the man is the thief.|The conditional preserves the reason to hurry.
138|Even if the theft is unrelated, the journey can catch a swindler.|Convey the fallback reason in ordinary spoken English.
143|Clau accepts the argument and wants to teach the crook a lesson.|The energetic reversal fits his voice.
147|She thanks them emotionally.|The stammer keeps the brief reply personal.
151|Clau cautions that they haven't found the rose yet.|The warning keeps the promise distinct from a result.
""",
    252: """
96|Clau is taken aback by the keeper's response.|Keep the stammer as a short reaction.
100|The crook threatens retaliation.|His interrupted curse still leads into the escape.
103|The keeper realizes the crook got away.|The abrupt reaction preserves his frustration.
106|He thanks them and says he was nearly fooled.|The question hands back the object the group came for.
111|Rafael confirms that this is what they wanted.|The brief affirmative gives the keeper the final instruction.
116|Return the object to its owner. The man must have other scams and will be reported if caught again.|Keep the instructions, suspicion and conditional threat together without a short second page.
""",
    243: """
25|Hodram asks about the figurehead's regal appearance.|Keep his interest distinct from belief in the story.
29|The priest knows no history but has something to add.|The unfinished thought gives Julio an opening.
32|Julio prompts him to finish.|The simple echo works in context.
36|Only people the figurehead likes can take it.|Keep the personification and the unusual rule in one thought.
40|Most of the people who tried left injured and without the figurehead.|Both consequences remain clear.
44|It returns when the person who took it dies.|The uncertainty about how it returns is preserved.
48|Hodram reacts thoughtfully.|The short pause leaves the choice with the priest.
52|The priest asks whether they want to try.|The straightforward invitation leads to the choice.
""",
    250: """
5|The guildmaster offers a reward and reimbursement.|Both purposes remain separate from the fixed payout notices.
52|The guildmaster asks if Hodram has visited the nearby ruins.|The question prepares the specific legend.
55|The ruins were once King Solomon's treasury according to legend.|Keep the ruler, the treasury and the legend together without certifying the rumor.
""",
    255: """
6|The woman greets Hodram by his given name.|The exact substitution stays in a short familiar greeting.
10|She is surprised he searches around the world and says this town has no especially famous ruins.|Keep the surprised question and the modest limit on the answer.
""",
    292: """
5|The guildmaster is glad Hodram came and has a favor to ask.|The familiar greeting introduces the job in his voice.
8|A monster has repeatedly appeared in nearby waters.|The speaker acknowledges that it is hard to believe.
12|Hodram echoes the word monster.|The short reaction prompts the explanation.
16|Fishermen call it a monster fish that bites and sinks ships.|Put the eyewitness term and the effect in separate readable sentences.
19|Several ships have already been attacked this year.|The number remains approximate and the danger specific.
22|The guildmaster asks if Hodram can hunt it.|The request follows the account of recent losses.
25|Hodram says finding it will take luck.|The frank warning keeps the result uncertain.
28|The guildmaster can wait and is counting on him.|His answer closes the agreement without guaranteeing a result.
""",
    294: """
43|Hodram remarks that the forest is dense.|The brief description sets up the explanation.
47|Gerhard infers why the site went unnoticed.|The causal reply follows what they can see.
58|Charles wishes they could leave the forest sooner.|Keep his discomfort and the specified place in one line.
64|Gerhard wonders if local Christians descended from Byzantines.|The question preserves uncertainty about the site.
67|Hodram hopes for a clue to a Proof.|The reference keeps their objective after the historical speculation.
71|Hodram is startled by human bones.|His question turns the conversation to the immediate evidence.
75|Gerhard thinks an earlier entrant died there.|The tentative explanation stays distinct from the sighting itself.
""",
    82: """
31|Fernando objects to the stranger's treatment of the admiral.|The existing warning fits as the start of the argument.
34|The sailor asks if he is wrong.|The brief challenge keeps the provocative tone.
38|Fernando protests indignantly.|The short outburst leaves the next wording to the sailor.
42|Some people who do not believe in miracles end up shipwrecked. He says Lil is better off.|Keep the surprising reversal and the qualification that this happens to some people.
46|Fernando is confused.|The brief reply gives the man room to apologize.
50|The sailor apologizes for shouting and says he meant no insult.|The plain apology sets up what he was really doing.
54|Fernando still cannot understand him.|The casual aside keeps his skepticism.
58|The sailor wanted a believing captain to have the item.|The sentence prepares the reveal without naming it too early.
""",
    92: """
24|Lil reassures Julio and compares his granddaughter to Athena.|The praise and source comparison set up Julio's later recollection.
27|Julio asks about Athena.|The echo lets Lil supply the explanation.
31|Lil identifies Athena as a Greek goddess and Minerva as the Roman name.|The comparison is explained in her words.
38|Julio thinks the name Minerva sounds familiar.|His uncertain memory prepares the reveal.
41|Lil reassures him again about Cristina.|Her simple confidence gives Julio a reason to explain his anxiety.
44|Julio is glad Lil trusts Cristina but worries as her grandfather.|Keep the warmth, family relation and gentle request for understanding.
47|Lil is silent.|The quiet response lets Julio remember the name.
51|Julio suddenly remembers.|The exclamation keeps the sudden turn.
54|Lil asks what happened.|Her stammer answers the sudden change.
58|Julio recalls the Minerva Shield.|The established name and his uncertainty stay explicit.
61|He heard a Mediterranean or Black Sea rumor and has never pursued it seriously.|Both possible regions and the qualified account remain clear.
64|The comparison to Minerva makes him want to find the shield for Cristina if it exists.|Give his revived interest and the condition separate beats.
67|Lil responds to Julio as he reflects on his granddaughter.|The given name avoids implying a second family relationship.
71|Julio calls his talk an old man's rambling and returns to work.|His self-deprecation closes the emotional moment.
""",
    121: """
485|Camille jokes that Lil is still a hard taskmaster.|The teasing follows Lil's demand that he work hard.
488|Lil privately feels relieved that Camille has returned.|The aside preserves her affection without adding a relationship.
498|Maria checks whether the misunderstanding is resolved.|The question prompts Camille's acknowledgment.
502|Camille answers yes and thanks both Hodram and Maria sincerely.|Keep both names and give his gratitude a natural spoken cadence.
506|Hodram asks whether the two have made up.|His direct question fits the moment.
510|Camille thanks Hodram again.|The reply singles out Hodram's role.
513|Hodram says Maria tricked him and all he did was bring Camille.|The understated claim gives Maria something to challenge.
517|Maria says Hodram had understood all along.|The rejoinder fits their familiar teasing.
""",
    124: """
9|Lil says there aren't that many cities where she's close to a barmaid.|Her hesitation answers Julian's assumption.
12|Julian says barmaids have information useful to adventurers.|The excited introduction gives his useful examples a point.
16|They may know treasure rumors, enemy fleet activity and the location of ruins only locals know.|Present the examples as one natural list and keep the last clue specific.
19|Julian jokes that adventurers should befriend girls everywhere.|The overstatement sets up Lil's skepticism.
23|Lil says friendship is not so easy to establish.|The quiet objection leads to Julian's preferred method.
26|A barmaid talks to many people and ordinary customer conversation will not stand out.|The advice keeps the social context of the exchange.
29|Julian recommends a thoughtful gift.|The suggestion motivates the list that follows.
""",
    127: """
50|Camille asks whether the last round showed what Fernando means by observing carefully.|The question connects the outcome to Fernando's lesson.
53|Fernando agrees and praises Camille for noticing.|The short answer fits his confident manner.
57|Luck and close observation are both required to win at gambling.|The concrete definition of insight stays in the lesson.
61|Fernando poses a question about getting luck on one's side.|Keep Camille's address and let the full question stand together.
65|Camille doubts whether it is even possible.|The hesitant answer gives Fernando his opening.
69|Fernando says to make winning a habit.|The compact maxim suits his delivery.
73|Camille echoes the maxim.|The question invites the explanation.
77|Fernando says luck favors winners.|The two short statements keep the order of his argument.
""",
    20: """
33|Gerhard recognizes and calls out to Barbarossa Hayreddin.|Use the clean Japanese order and the verified nameplate spelling. The recognition stays just as abrupt.
""",
    48: """
111|Maria targets people who rule by force and take wealth from others.|The pointed question explains what she wants to know about Rafael.
114|Clau insists their trade and living are honest.|The stammer and appeal fit his alarm at her accusation.
118|Rafael recalls Portugal's former global influence.|The line sets up both the loss and his future hopes.
142|Spain has taken Portugal's sovereignty but Rafael wants the country bustling with sailors again.|Give Portugal's situation and Rafael's hope distinct beats without stranding a conjunction.
146|Maria asks if Portugal should replace Spain as world ruler.|The challenge tests the implications of Rafael's dream.
150|Rafael rejects conquest like Spain's in the New World.|The stated distinction is the character's ambition.
155|Maria challenges his simple division of right and wrong.|The pointed question invites Rafael to qualify his view.
158|Rafael does not excuse Portugal's past.|The pause and his explicit qualification stay.
166|Rafael wants shipping to improve people's lives and sees that as his role.|The idea remains personal and practical.
171|Clau is surprised at what Rafael has considered.|The nickname remains in his familiar reaction.
174|Maria calls Rafael's ideal admirable.|The restrained approval leaves room for Rafael's misreading.
178|Rafael thinks he may have spoken presumptuously and apologizes.|Keep the hesitation and separate the question from the apology.
182|Maria says she meant that she wishes more sailors thought as he does.|The clarification preserves her genuine approval.
194|Maria shifts to the current situation in the Mediterranean.|The transition ends the introspection and starts a separate subject.
""",
    53: """
6|Maria says the Proof collection is complete.|Keep the full collection title together and match the parallel branch.
9|Xien notices that nothing appears to happen.|The pause and title address frame his surprise.
13|Maria acknowledges his observation.|The quiet agreement keeps her uncertainty.
25|A crew member wonders whether they need another key.|The tentative question does not establish another task.
35|A crewman dreads another search.|The exclamation gives the question an immediate response.
46|Maria says they don't need anything else.|The firm answer begins her explanation.
""",
    54: """
12|Maria says the Proof collection is complete.|Use the same wording as the parallel branch for the same source thought.
15|Xien sees that nothing has happened.|The repeated answer works in this branch too.
19|Maria acknowledges the lack of an effect.|Her quiet assent preserves the shared opening.
31|A crew member wonders whether another key is needed.|The question remains tentative.
41|A crewman protests the thought of hunting again.|Keep the quick comic response.
52|Maria says nothing else is needed.|The reply opens the meaning of the collection.
""",
    55: """
137|Angelo asks where Bianca is going.|The repetitions preserve his confusion.
144|Angelo repeats both goodbye and the idea she is going back.|The brief questions follow Bianca's statement exactly.
152|Angelo asks Bianca not to go and protests that this cannot be a joke.|Keep his disbelieving plea and put the protest on a complete line.
159|Angelo calls after her and says she is all he has.|The direct call preserves his desperation.
162|Angelo says they are each other's only family and asks whether she will leave him alone.|The two thoughts keep the weight of the familial relation.
168|Angelo is puzzled by Bianca's assurance.|The brief turn lets her explain.
175|Angelo repeats his friends, reviewing what she meant.|The hesitant echo preserves the transition.
183|Angelo begins to think of his friends as family.|The short realization sets up Bianca's last advice.
""",
    87: """
194|Maria finds the arithmetic tedious.|The terse observation prepares Xien's question.
198|Xien asks whether Maria can solve it and admits he is hopeless at such puzzles.|Keep his exact wording and name substitution. Put the complete admission on the second line.
204|Maria subtracts twenty feet from thirty-two points of contact.|The numbers and her identification of the remaining hands and sticks are precise.
208|Maria says equal groups imply two hands for each walking stick.|Her next step follows the equal numbers in the riddle.
212|Xien concludes that each pair contributes three contacts.|The exchange shows him following Maria's arithmetic.
216|Maria concludes that twelve contacts make four pairs.|Both totals stay explicit.
220|Xien says that means four elders and four babies.|The intermediate numbers lead directly to the answer.
223|Maria calculates that two of the ten must be adults.|The exact answer completes the puzzle.
""",
}
PROOFS = ("That's every Proof of Conquest...", ())
REVISIONS = {
    (234, 55): ("That really moved you, Gerhard.", ()),
    (235, 48): ("Perhaps you'd like to look into it. Ian Dukov", ("Perhaps you'd like to look into it.", "Ian Dukov")),
    (237, 36): ("It's what that victory meant.", ()),
    (251, 100): ("It may not be worth much. It's a glass ornament Dad got me for my birthday. He knows how much I love roses...", ("It may not be worth much.", "It's a glass ornament", "Dad got me for my birthday.", "He knows how much I love roses...")),
    (251, 138): ("Even if he didn't take the rose, we can still catch the swindler.", ("Even if he didn't take the rose,", "we can still catch the swindler.")),
    (252, 116): ("Give it back to its rightful owner. He's bound to have other scams. If I spot him, I'll turn him in to the governor's office!", ("Give it back to its rightful owner.", "He's bound to have other scams.", "If I spot him,", "I'll turn him in", "to the governor's office!")),
    (243, 36): ("It only goes with people it likes.", ()),
    (250, 55): ("That's King Solomon's old treasury, or so the legend goes. Have a look.", ("King Solomon's old treasury,", "or so the legend goes.")),
    (255, 10): ("You travel the world to find ruins? I'm afraid none here are famous.", ("You travel the world to find ruins?", "I'm afraid none here are famous.")),
    (292, 16): ("Fishermen call it a monster fish. It bites ships until they sink.", ("Fishermen call it a monster fish.", "It bites ships until they sink.")),
    (294, 58): ("I can't wait to leave this forest.", ()),
    (82, 42): ("Some men won't believe in miracles and wind up shipwrecked. You're better off than they are!", ("believe in miracles", "and wind up shipwrecked.", "You're better off than they are!")),
    (92, 44): ("I'm glad you trust her, Admiral. But she's my granddaughter. You know how an old man worries.", ("I'm glad you trust her, Admiral.", "But she's my granddaughter.", "You know how an old man worries.")),
    (92, 64): ("You said she's like Minerva. Now I'd love to find that shield. If it's real, I want it for her.", ("You said she's like Minerva.", "Now I'd love to find that shield.", "If it's real, I want it for her.")),
    (121, 502): ("Yes. Hodram, Maria... Thank you.", ()),
    (124, 16): ("They hear treasure rumors. They keep track of enemy fleets. They can even point you to ruins only the locals know about.", ("They hear treasure rumors.", "They keep track of enemy fleets.", "the locals know about.")),
    (127, 61): ("Here's one for you, Camille. How do you get luck on your side?", ("Here's one for you, Camille.", "How do you get luck on your side?")),
    (20, 33): ("You! Barbarossa Hayreddin!", ("Barbarossa Hayreddin!",)),
    (48, 142): ("Spain rules us now. But we dream of a Portugal alive with sailors again.", ("Spain rules us now.", "But we dream of a Portugal", "alive with sailors again.")),
    (48, 178): ("...Did I speak out of turn? Sorry if I sounded full of myself.", ("...Did I speak out of turn?", "Sorry if I sounded full of myself.")),
    (53, 6): PROOFS,
    (54, 12): PROOFS,
    (55, 152): ("Don't go... Come on. This isn't funny.", ("This isn't funny.",)),
    (87, 198): ("Can you solve it, FI? I'm hopeless at this sort of thing.", ("Can you solve it, FI?", "I'm hopeless at this sort of thing.")),
}


def main():
    packet = base.load(SOURCE)
    groups = {g["block"]: {r["source_record_index"]: r for r in g["records"]} for g in packet["groups"]}
    assert groups[53][6]["source_body_hex"] == groups[54][12]["source_body_hex"]
    name = base.load(parent.stage.ROOT / "hayreddin_name_order_proposal.json")
    assert name["candidate_sha256"] == packet["candidate_sha256"]
    current = groups[20][33]
    historical = name["exact_source_current"]
    assert {k: v for k, v in current.items() if k not in {"current_offset", "current_command_offset"}} == {
        k: v for k, v in historical.items() if k not in {"current_offset", "current_command_offset"}}
    inventory = base.load(name["inventory"])
    assert base.digest(name["inventory"]) == name["inventory_sha256"]
    hit, = [r for r in inventory["current_literal_matches"] if r["shown_text"] == "Hayreddin Barbarossa"]
    assert (hit["file_path"], hit["block"], hit["offset"]) == (
        current["file_path"], current["block"],
        current["current_offset"] + 1 + bytes.fromhex(current["current_body_hex"]).index(b"Hayreddin Barbarossa"))
    assert name["proposal"]["english"] == REVISIONS[20, 33][0]
    source = checked_text(getsource(common.main), {
        "len(resolved) == 8": "len(resolved) == 23",
        "assert english != previous and english.isascii()": "assert (english != previous or phrases) and english.isascii()",
        'finding="prose" if key in REVISIONS else "retention",':
            'finding=("wrap" if english == previous else "prose") if key in REVISIONS else "retention",',
    })
    scope = vars(common) | globals()
    exec(compile(source, __file__ + "::contextual-review-ledger", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
