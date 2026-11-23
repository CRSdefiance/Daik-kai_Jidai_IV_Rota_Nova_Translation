"""Resolve the next set of contextual wrap leads across the four captains."""

from inspect import getsource

from scripts import register_rafael_next_phrase_wraps_20261118 as parent
from scripts import review_rafael_early_phrase_wraps_20261118 as prior
from scripts.source_locked_derivation_v5118 import checked_text

base, TOKEN, logical, GATES = prior.base, prior.TOKEN, prior.logical, prior.GATES
ROOT = parent.stage.ROOT.parent.with_name("all_routes_next_phrase_wraps_20261118")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v3.json"
BLOCKS = ((170, 178, 179), (72, 274, 277), (12, 63, 137), (6, 19, 31))
QUEUE = parent.stage.ROOT / "followup_wrap_queue.json"
CONTEXT = {
    170: "Carlo explains his family's deaths and his willingness to put others' health first. Rafael connects that to what he saw in town and asks Carlo to come aboard.",
    178: "Rafael asks Fernando how he usually wins at gambling. Fernando attributes it to insight and luck and demonstrates how he reads a couple's argument.",
    179: "Manuel admires the ship while inspecting her. His advice about treating ships as living things leads the crew to ask him to sail with them.",
    72: "Maria offers Hodram an opportunity in Japan if he deals with the pirates. They test each other's resolve with sarcasm before he accepts.",
    274: "The guildmaster confronts the captured smuggler. The man protests and the guildmaster tells him to make an honest living before rewarding Hodram.",
    277: "The guildmaster dismisses the captured man's claim to the cargo, thanks Hodram, pays him and offers a treasure lead. The money and market share notices retain their exact controls.",
    12: "Aziza's crew blames her for their losses and mocks her reason for pursuing the Shamshir. Lil and Al intervene. A separate choice branch bargains for Aziza's release.",
    63: "Lil puts the Ceremonial Knife in the Sun-Crest Sheath. The light gives way to a map. Fernando or a companion wonders if it leads to the New World's Proof of Conquest, and Lil remains unsure.",
    137: "A merchant mistakes Lil for a barmaid and treats her dismissively. Fernando tries to defend Lil and insults her in the same breath. Lil calls him on it before identifying herself.",
    6: "Aziza confronts the fleet again and calls on her crew to settle the score. The lines carry the confrontation into the next attack.",
    19: "Maria's fleet approaches after Aziza is betrayed. The crew repeats the accusation about the Shamshir that Lil can hear in her own route. Maria considers intervening.",
    31: "Kuhn's disguised ships are mistaken for Maria's fleet. Maria recognizes the trick and rushes to help Lil, as Hodram and Camille arrive to join the fight.",
}
NOTES = {
    170: """
229|Clau asks if Carlo's family would object to his going to sea.|The casual questions leave Carlo room to answer with the truth.
232|Carlo says his family died a year ago.|The brief disjointed reply preserves his grief and the exact timing.
235|Rafael falls silent.|Preserve the pause before Carlo continues.
248|Rafael addresses Carlo gently.|The established name fits the response without implying kinship.
253|Carlo says work felt empty after he put it ahead of family, and he values others' health now.|The contrast gives the confession its effect.
256|Rafael realizes why Carlo helped the shopkeeper.|Keep the realization and both pauses while letting the complete thought use the available width.
261|Rafael asks if Carlo will return home.|The quiet question leaves the decision open.
266|Carlo cannot live in Venice alone surrounded by happy memories.|His reason is personal, not a judgment about Venice.
270|Rafael listens silently.|Preserve the silence before his invitation.
275|Rafael again asks Carlo to join them and says he needs him.|The direct response fits the turn from grief to a concrete offer.
280|Carlo considers the proposal.|The moment of reflection gives Rafael time to explain.
284|Rafael thinks he could learn from Carlo and tells Clau.|The idea of learning is distinct from the earlier confession.
289|Clau reluctantly concedes.|The quiet assent introduces the collective invitation.
293|Carlo remains quiet.|The pause makes room for Julio's proposal.
297|Julio proposes that the crew become Carlo's new family.|The metaphor is explicitly in this conversation and prepares the response.
301|Rafael agrees and asks Carlo what he thinks.|The enthusiastic turn still leaves Carlo the decision.
305|Carlo thanks the crew and says he never expected the offer.|The warmth answers the invitation without committing him before he responds.
308|Clau treats the matter as settled and jokes about counting on Carlo's trading ability.|The practical tag brings Clau's voice back after the confession.
""",
    178: """
181|Fernando admits losing after a long winning run and offers the drink.|The grudging opening and direct offer set up Rafael's question.
192|Rafael declines for now and asks about Fernando's confidence.|The question clearly follows Fernando's remark about his winning streak.
196|Fernando says insight and luck are what matter in gambling.|The compact answer carries both factors into his boast.
199|Fernando claims both and says he was born to gamble.|The casual brag keeps the source's confidence.
203|Rafael doubts the claimed insight and is unsure about Fernando's luck.|The question asks for proof without ruling out his claim.
207|Fernando advises against judging by appearances.|The familiar saying sets up his demonstration.
211|Fernando points out a couple and asks what they are saying out of earshot.|The test preserves that he cannot hear and must observe.
214|Rafael guesses that they are talking about love.|The guess contrasts with what he will see.
218|Fernando says they are breaking up.|The blunt answer keeps his confidence.
222|Rafael is puzzled.|The short reaction gives Fernando a cue.
227|Fernando tells Rafael to watch.|The imperative turns the argument into a demonstration.
""",
    179: """
5|Manuel notices the ship is well looked after.|The observation anchors his unsolicited advice in what he actually sees.
8|Manuel thinks more work is possible and starts to give an example.|The short first sentence lets him trail off naturally while he is inspecting the ship.
11|Rafael asks if something is wrong with the ship.|The question makes the interruption sound concerned.
16|Janus politely asks if Manuel needs anything about their ship.|Both turns distinguish curiosity from concern.
20|Manuel realizes they own the ship and describes her as full of life.|The image prepares his remark that ships are living things.
24|Janus privately finds the expression unusual.|The parenthetical preserves the private aside.
27|Manuel advises caring for the ship because she is alive and will repay the care.|The wording follows naturally from his figurative praise.
30|Rafael pauses.|Preserve the quiet reaction before Manuel worries he overstepped.
35|Manuel excuses himself and says this is only his own view.|His polite retreat gives Janus a reason to stop him.
38|Janus asks him to wait.|The stammer preserves the sudden initiative.
42|Manuel asks what is wrong.|The short turn lets Janus explain.
46|Janus noticed how much Manuel loves ships.|The question stays respectful and lets Manuel volunteer his background.
50|Manuel tells them his name and that he once navigated ships.|The two details ground the invitation that follows.
""",
    72: """
73|Maria describes Hodram's suspicion as cynical and offers Japan trading rights.|The offer supplies the context for his dry answer.
77|Hodram reacts with sarcasm to her apparent generosity.|The dry brevity fits his skepticism.
81|Maria asks whether he would rather refuse.|The short question lets him make his own calculation.
85|Hodram wants results from the voyage but need not target Japan.|Both his ambition and his restraint stay explicit.
88|Maria is prepared for him to pick a fight with her instead.|The standing challenge gives Hodram reason to question her confidence.
91|Hodram wonders if her confidence is a bluff, says he currently has no quarrel and urges her to calm down.|Restore three clear beats so the appraisal, restraint and dry rejoinder read distinctly.
94|Maria is silent.|Keep the pause before Hodram openly accepts.
98|Hodram says accepting her proposal is plainly in his best interest.|His decision still follows from calculation.
102|Hodram calls Maria formidable and feels he is dancing to her tune.|The idiom carries his rueful recognition of her skill.
106|Hodram tells Maria to sit back while he takes on the pirates.|The boast hands the next turn back to Maria.
110|Maria questions his prediction that she will just watch.|The lightly teasing reply gives his next sarcastic line a cue.
114|Hodram says her smile makes it easy to make brave speeches.|The sarcasm in the compliment remains audible.
117|Maria recognizes his sarcasm.|Her brief response names the dynamic already evident.
121|Hodram taunts her for thinking he is easy to handle and leaves her to await the news.|The mimicked thought lets the scene end in his confident voice.
""",
    274: """
5|The guildmaster recognizes the smuggler and acknowledges his capture.|The direct opening identifies why the man is in front of him.
8|The smuggler insists the accusations are entirely mistaken and complains he is being hassled.|Keep his repetitive defense and self-pity as audible turns, with no split contraction.
11|The guildmaster says the smuggler talks well and should consider the people he inconvenienced.|The pointed answer turns the grievance back on him.
15|The smuggler wants to know what he should do.|The indignant question prompts the specific instruction.
19|The guildmaster tells him to do honest work and not claim he already has.|The direct instruction and warning preserve the rebuke.
22|The smuggler tentatively asks if that excuse is barred.|The hesitation lets his attempted evasion show through.
26|The guildmaster apologizes to Hodram and offers a small token.|The courtesy separates the reward from the admonishment.
""",
    277: """
5|The guildmaster acknowledges Hodram's return.|The short opening gives the prisoner room to protest.
9|The prisoner bemoans his cargo.|The trailing possessive prompts the guildmaster's correction.
13|The guildmaster says the cargo belonged to other people.|His brusque reply rejects the prisoner's claim.
16|The guildmaster thanks Hodram for the capture and hands him a modest reward.|The thanks and modest offer stay together without breaking the contraction.
62|The guildmaster has confidential or unusual information for Hodram.|The friendly introduction prepares the new lead.
66|Beyond the city gate there is reportedly a building with treasure hidden in it.|The route, location clue and hearsay remain clear.
77|Hodram should get a map before exploring.|The warning follows the gate directions as practical advice.
""",
    12: """
34|Fernando hears trouble aboard Aziza's ship.|The ship and apparent quarrel give Lil a reason to approach.
37|Lil wonders what is happening and suggests finding out.|The invitation retains her initiative.
41|The pirate blames Aziza for repeated losses without profit.|Use the same blunt accusation as the matching turn in Maria's route.
45|Aziza questions being held responsible.|The response picks up the pirate's accusation directly.
49|Another pirate asks why Aziza keeps chasing the company.|The company-name substitution keeps the target as the player organization.
53|A pirate says there must be a reason she will not share.|The taunt sets up what he reveals about the blade.
56|Aziza reacts in shock.|The punctuation preserves the quick speechless beat.
60|The pirate says Aziza's only aim is recovering the Shamshir from the company because it was her father's keepsake.|Match the Maria accusation and place the company substitution inside the sentence so its period never doubles.
64|Aziza denies that this was her intention.|The stammer keeps her defensive response unfinished.
68|The pirate says nobody will follow a chief who cannot make money and threatens her.|The reply explains why the losses matter to the crew.
72|Lil fears Aziza will be killed and asks what to do.|The urgent thought opens the intervention.
76|Al tells Lil to leave it to him.|The brief offer fits his protective action.
145|A pirate offers to settle the matter for money.|The offer remains conditional and establishes the terms of this choice branch.
148|Lil asks how much.|The short question moves directly to the bargaining.
152|Cristina is shocked that Lil would pay them.|The given name and question keep her alarm personal.
155|Lil says they can always earn more money.|The pragmatic answer explains her willingness to pay.
159|Aziza is moved that they would do this for her.|The hesitation separates her response from the pirates' haggling.
163|The pirate proposes a ransom of two million.|The exact opening price stays explicit before Lil counters.
167|Lil counters with one million.|The concise counteroffer carries her composure.
171|The pirate reluctantly agrees to one million for Aziza.|The stammer follows the unexpectedly lower counteroffer and keeps the final amount.
175|Lil accepts and tells Aziza to come with them.|The invitation completes this bargain.
178|Aziza says Lil's name and trails off.|The native name substitution keeps her gratitude personal.
""",
    63: """
27|Lil dismisses the danger, slips in the knife and cries out during the flash.|The interrupted action keeps the timing of her surprise.
36|Fernando reacts to the light.|The brief turn shares that surprise.
42|Another companion reacts to the light.|The separate reaction is preserved for its original branch.
49|Lil is dazzled and cannot tell what is happening.|The two exclamations preserve both senses of alarm.
59|Fernando thinks it is safe again and wonders what appeared.|His question introduces the map.
62|Lil sees a map and is baffled that it came from the knife.|The question preserves the surprising object change.
65|Fernando cannot explain it and guesses the map leads to the New World's Proof of Conquest.|Let the guess stay a question and keep the regional artifact title on one line.
69|Lil is still unsure, then says she is glad they found it.|The hesitation works after Fernando's tentative explanation.
74|The other companion thinks it is safe and asks what appeared.|The dialogue preserves the speaker-specific version of the same reaction.
77|Lil asks the same question about the knife and map in this branch.|The matching English supports the repeated Japanese.
80|The companion says he also cannot explain it and asks if it is a map to the regional Proof.|The turn keeps his uncertainty and speaker-specific response.
83|Lil responds in the same uncertain way in this branch.|The repeated punctuation supports the matching reaction.
""",
    137: """
126|Al voices his dislike of the merchant.|The blunt aside anticipates the merchant's treatment of Lil.
133|Lil calls out to the merchant.|The direct hailing fits her impatience.
137|The merchant thinks Lil is a new barmaid and rates her below the others.|The condescension sets up Lil's indignation and Fernando's joke.
141|He says she will do and calls her over.|The dismissive invitation keeps his assumption intact.
145|Lil objects to being ranked and says the merchant has no standing to judge her.|Both her shock and objection give Fernando something to answer.
156|Fernando calls the rating too low, then calls Lil just below average.|The supposed defense still contains the insult and can land in one line.
168|A companion agrees.|The fast agreement strengthens the comic insult.
175|Lil asks if they were praising or insulting her.|The reaction lands the joke without explaining it.
181|The merchant says she looks charming when angry, promises a tip and asks her name.|His response keeps the same mistaken relationship and patronizing tone.
192|A crew member objects to mockery of their admiral.|The stated title establishes the crew's indignation.
198|Lil corrects the mistake and expects him to recognize her name if he trades.|The name substitution and her offended pride remain.
201|The merchant does not know the name and cares only about his own money.|The emphasis keeps his priorities clear.
""",
    6: """
42|Aziza says she finally found them and will settle this confrontation.|The two shouts give the renewed threat its cadence.
45|A crew member cheers in reply.|The short acclamation answers the threat.
51|Aziza recognizes the company and threatens to send it to the bottom.|The threat preserves the company-name substitution and parallel bravado.
""",
    19: """
15|Aziza challenges the traitor to repeat himself.|The question keeps her disbelief before she hears the crew's reasons.
19|The pirate asks if she did not hear him.|The taunt leads into the open mutiny.
23|The pirate says no one aboard obeys her anymore.|The direct statement sets up her accusation of betrayal.
26|Aziza curses the crew for betraying her.|The anger carries naturally to Maria noticing the argument.
29|Maria sees that something is happening on the other vessel.|The uncertainty avoids assuming she already knows the cause.
33|Her companion senses a quarrel.|The uneasy tone motivates moving closer.
36|Maria asks to bring them alongside.|The order is firm and keeps her politeness.
40|The pirate blames Aziza for their losing streak and stagnant earnings.|Use the same grievance as the matching Lil turn, with the threat on its own.
44|Aziza challenges being blamed.|The incredulous question answers his accusation.
48|A pirate asks why she keeps pursuing the company.|The company-name substitution matches the target of her pursuit.
52|The other pirate taunts her about having a reason she cannot share.|The taunt prepares his specific claim about the sword.
55|Aziza reacts in shock.|The speechless response preserves the timing.
59|The pirate says Aziza wants only to take back her father's Shamshir from the company.|Match the Lil accusation and place the company substitution where its own punctuation works for either captain.
63|Aziza denies the accusation.|The hesitation gives the pirate the opening to continue.
67|The crew says it will not follow a boss who cannot make money and threatens her.|The threat completes the explanation that began with the losses.
71|Maria sees that Aziza's life is in danger.|The urgency follows the pirates' threat.
74|Her companion doubts whether outsiders should intervene.|The hesitation separates his judgment from Maria's desire to help.
""",
    31: """
8|The lookout reports that the player company's fleet has opened fire.|The company-name substitution preserves the apparent identity at the moment of the mistake.
11|Lil takes the firing as confirmation that Kuhn was right.|Her surprised conclusion gives Maria reason to answer.
15|Maria denies that her fleet is attacking and asks who the attackers are.|Her confusion and denial fit the deception.
18|Her companion identifies the disguised fleet Kuhn sent against the Argot Company.|The explanation makes the false flag and its target explicit.
21|Maria sees that Kuhn has revealed his intentions and insists they help Lil immediately.|The three beats preserve her realization and urgency without dangling a contraction.
25|Her companion sees another fleet approaching and interrupts.|His stammer and trailing recognition lead to the arrival.
30|Hodram believes they are in time.|The calm reply contrasts with the confusion that preceded it.
34|Camille shouts Lil's name.|The prolonged cry preserves his urgency.
38|Lil recognizes Camille and Hodram and asks why they are there.|The stammer and approved spellings keep her surprise clear.
42|Camille says Maria warned him that Kuhn's disguised fleet was attacking Lil.|The name substitution preserves who gave the warning.
45|Lil is shocked by the explanation.|The two questions keep her disbelief.
49|Maria says this shows Kuhn's nature and her crew will join the fight.|The commitment follows the earlier rush to help.
52|Lil apologizes for her mistaken judgment.|The given-name substitution and stammer keep the apology personal.
56|Maria is glad they are in time and tells Lil to face Kuhn.|The reassurance directly answers the apology before the change to action.
60|Hodram orders battle stations.|The recognized naval command closes the dialogue before action.
""",
}
PIRATE_LOSSES = ("Loss after loss, and no profit. You'll answer for that.",
                 ("Loss after loss, and no profit.", "You'll answer for that."))
PIRATE_KEEPSAKE = ("The Bloodstained Shamshir. You chase FO just to get it back. A keepsake from your old man!",
                   ("The Bloodstained Shamshir.", "You chase FO", "just to get it back.", "A keepsake from your old man!"))
REVISIONS = {
    (170, 256): ("Oh... So that's why you helped the shopkeeper...", ()),
    (178, 196): ("Sure. You need insight and luck.", ()),
    (179, 8): ("Still, she could use a little work. For instance...", ("For instance...",)),
    (72, 91): ("Confidence or a bluff? I wonder. I have no quarrel with you for now. No need to get worked up.",
                ("Confidence or a bluff? I wonder.", "I have no quarrel with you for now.", "No need to get worked up.")),
    (274, 8): ("They call me a smuggler. It's a mistake! A complete mistake! I'm the one being hassled here!",
               ("It's a mistake!", "A complete mistake!", "I'm the one being hassled here!")),
    (277, 16): ("Thanks for catching him. It's not much, but take this.", ("Thanks for catching him.", "It's not much, but take this.")),
    (12, 41): PIRATE_LOSSES,
    (12, 60): PIRATE_KEEPSAKE,
    (12, 163): ("Make it two million coins.", ()),
    (63, 65): ("Beats me. Could it be a map to the New World's Proof of Conquest?", ("the New World's Proof of Conquest?",)),
    (137, 156): ("Come on! She's just below average!", ()),
    (6, 42): ("Found you at last! This time, we settle the score!", ("Found you at last!", "This time, we settle the score!")),
    (19, 40): PIRATE_LOSSES,
    (19, 59): PIRATE_KEEPSAKE,
    (31, 21): ("Kuhn's fleet in disguise... He's shown his true colors at last. We have to help Lil now!",
               ("Kuhn's fleet in disguise...", "He's shown his true colors at last.", "We have to help Lil now!")),
}


def main():
    packet = base.load(SOURCE)
    groups = {(g["route"], g["block"]): {r["source_record_index"]: r for r in g["records"]}
              for g in packet["groups"]}
    for a, b in ((41, 40), (60, 59)):
        lil, maria = groups[(2, 12)][a], groups[(3, 19)][b]
        assert lil["selector"] == maria["selector"]
        assert lil["source_body_hex"] == maria["source_body_hex"]
    source = checked_text(getsource(prior.main), {
        "len(resolved) == 8": "len(resolved) == 13",
        "assert english != previous and english.isascii()": "assert (english != previous or phrases) and english.isascii()",
        'finding="prose" if key in REVISIONS else "retention",':
            'finding=("wrap" if english == previous else "prose") if key in REVISIONS else "retention",',
    })
    scope = vars(prior) | globals()
    exec(compile(source, __file__ + "::contextual-review-ledger", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
