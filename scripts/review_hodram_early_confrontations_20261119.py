"""Review Hodram's confrontations, battle tutorial and preserved opaque cries."""

from inspect import getsource
from pathlib import Path

from scripts import prepare_hodram_early_confrontations_20261119 as paired
from scripts import review_story_short_phrase_wraps_20261119 as workflow

base, native, parent = paired.base, paired.native, paired.parent
ROOT, SOURCE = paired.ROOT, paired.SOURCE
OUTPUT = ROOT / "contextual_review_v2.json"
NAMES = workflow.NAMES
PRIOR = Path("translations/hodram_B0_B41_registered_review_v1.json")
GLYPHS = NAMES.with_name("remaining_dialogue_glyphs_20261119_v1.json")

CONTEXTS = {
    28: "After the sea-creature encounter, a companion urges Hodram to report the outcome to the Malacca guild.",
    29: "Speyer's ships fire on Hodram before answering his signal. Hodram gives Charles control of gunnery, Gerhard asks for the boarding post, and the system explains the controls.",
    30: "Hayreddin warns Hodram away from the southern Mediterranean. His threat, the crew's advice, and the fight or retreat choice have separate outcomes.",
    31: "When Hodram presses the issue, Hayreddin agrees to face him himself. One outcome also hints at a man more dangerous than Hayreddin.",
    32: "Maldonado insults the European fleet, fresh ships appear astern, and officers recognize the relief force as Escante's.",
    33: "After Maldonado's defeat, Escante asks to keep the agreement. Gerhard privately weighs the African threat before Hodram decides.",
    34: "Clifford mocks his challengers before the battle. The blunt reply turns his confidence against him.",
    35: "The opposing commander claims the Indian Ocean routes for Muslims in his battle challenge.",
    36: "Kurushima treats the arrival of foreign fighters in Ming service as a provocation and threatens them.",
    37: "Hodram and Gerhard discuss a slave ship and the limits of their authority. The choice and ensuing timing order frame the attack.",
    38: "Lil believes Maria sent the enemy fleet. Camille identifies Kuhn's deception, Hodram orders fire, and Kuhn withdraws.",
    39: "A lookout spots the fleet. The opponent invokes the spirit of Yamato, and Hodram identifies the iron-plated ship.",
    40: "Pasha surrounds Hodram and threatens an execution. Fire from town disrupts the attack. Two opaque cries precede Pasha's retreat orders and Hodram's challenge.",
}

NOTES = {
    28: """Hodram recognizes they have finally put an end to the problem.
The first eager companion proposes reporting immediately to the Malacca guild.
The formal companion expresses urgency as a duty.
The energetic alternative invites the crew to hurry and report.
The rough alternative's impatient 'already' keeps the push to move.
The older voice gives an emphatic order to report at once.
The friendly voice wants to hurry and tell the guild the result.
The courteous alternative puts the trip to the guild as a suggestion.""",
    29: """The lookout's discovery opens the confrontation.
Hodram asks whether the ship belongs to Speyer.
The Hanseatic cog identifies the ship for the lookout.
Gerhard explains that their enforcement authority is limited to their own waters.
The lookout stammers at the enemy firing without warning.
The companion suspects the gunfire could be a misunderstanding.
The abrupt command calls for an actual flag signal.
The acknowledgment asks for the content of Hodram's signal.
Hodram's official message gives a possible territorial violation without declaring it proven.
Hodram formally requests a stop so he can ask about the incident.
The unvoiced reaction registers the shock of the reply.
The brief cry belongs to the gunfire interruption.
The signal officer stammers and concludes they will not heed the flags.
Hodram distinguishes a deliberate attack from a misunderstanding.
Gerhard thinks they mean to get rid of the crew before trouble grows.
All hands, battle stations preserves the command and the choice to answer the aggression.
The rough retort insults their hastily assembled fleet and threatens a lesson in naval combat.
Hodram asks Charles for a plan.
Charles recommends the standard T formation by name.
The tactic preserves the enemy broadside hazard, both approaches, the player's broadside, and a single combined volley.
Hodram delegates gunnery to Charles in a clipped order.
Charles divides steering from his own work directing the gunners.
Charles is excited to test the new cannon in combat.
The speakerless instruction calls for ordinary steering and sail adjustment.
The notice states that the guns fire automatically once a target is in range.
Gerhard asks to be Boarding Leader and assigned to Quarters, matching the room and post.
The system tells the player where to change assignments for battle.
Retain X and the registered Deck menu name in the instructions.
The notice names the three useful battle stations without making the assignment compulsory.
The second assignment notice names Gerhard and Quarters directly.
The modal explains automatic boarding on contact and expresses confidence in Gerhard.
The final prompt asks Hodram for a heading.""",
    30: """Hayreddin's initial challenge names the southern Mediterranean and threatens the crew if they stay.
Hodram connects the threat to the man the port worker mentioned.
Barbarossa's name and the sense of recognition remain in the exclamation.
Hodram's short question asks whether the other speaker knows him.
The established full name and the explanation of the Barbarossa name both remain.
Hodram judges Hayreddin's skill from what he has just seen.
Gerhard calls him a monster figuratively and starts another thought.
The alliance variation preserves the same territorial warning and mentions their alliance.
Hodram again remembers the person at the port who identified this dangerous man.
Gerhard now recognizes whom that warning was about.
The first companion judges retreat advisable before the opportunity passes.
The sober alternative names the force and urges retreat.
The alarmed voice puts the retreat as a question.
The direct address and practical suggestion suit the fourth version.
The rough alternative uses a short, colloquial warning.
The elder companion regards retreat as the wisest course.
The youthful voice counts the ships by impression and wants to run.
The mature voice recommends retreat while they can.
The first label orders immediate battle preparation.
The second label chooses withdrawal without promising anything about the future.
Hayreddin relishes the first choice and threatens the fleet without asserting an outcome.
The retreat reply approves the decision and tells Hodram to earn his reputation in the Caribbean.
The last threat extends pursuit to the ends of the earth if Hodram returns to the Mediterranean.""",
    31: """Hayreddin calls Hodram persistent and decides to face him personally.
This version adds that Hayreddin wants to intervene before Hodram angers someone truly fearsome.""",
    32: """The first lookout reports Maldonado's fleet as spotted.
The next variant credits the crew with finding his fleet.
The assertive alternative says the speaker spotted the fleet.
The spontaneous cry identifies Maldonado's fleet without a full report.
Maldonado tells his men to show inexperienced Europeans how they fight in the Caribbean.
The first report notes the size of the force Maldonado brought.
The second version gives the same observation curtly.
The excited voice is struck by how many he brought.
The simple alternative counts the ships only in general.
The rough alternative acknowledges the size in a fragment.
The older voice adds the characteristic emphasis of 'all right.'
The youthful voice says only that there are many.
The measured variant notes the fair size of the force.
Hodram steadies them and orders their usual battle drill.
The first warning uses the nautical astern for more ships behind them.
The distressed voice stammers over its address to the admiral.
The rough voice reports that the extra ships have come up behind them.
The clipped version uses two quick exclamations for the rearward threat.
The last voice starts with a cry of renewed alarm.
Hodram reacts before he identifies the approaching flags.
The frightened appeal to God matches the source outcry.
The alarmed crew member stammers that the numbers make a fight impossible.
Charles explicitly appeals to logic while sharing the same alarm.
Hodram holds the crew's panic and asks whose flags he sees.
Escante offers aid immediately as their paths cross.
Hodram recognizes Escante's forces from the arrival.
The first crew voice is relieved they have been saved.
The alternative crew voice gives the same stammer of relief.
The other rescuer offers help in a friendly colloquial voice.
The alternate reply again identifies Escante's forces.
The first crew voice's relief works in this alternate rescue too.
The alternate crew voice keeps its breathless stammer.""",
    33: """Escante praises Hodram's conduct and says he can rely on him. The surname is a native substitution.
Maldonado has been dealt with while the English pirates still cause trouble.
Escante makes clear that he means to continue their existing agreement.
Hodram's silent pause gives space for the private advice.
Gerhard's aside reports Espinosa acting in Africa and urges quick action.
The short response keeps Hodram's hesitation private.
The advice favors accepting the offer without declaring his choice.
The first choice clearly accepts the agreement.
The second choice is a blunt refusal.
Escante says he looks forward to their exploits after acceptance.
The refusal makes Escante regret their decision and hope they never become enemies.""",
    34: """The fleet commander admires his opponent's nerve and looks forward to the entertainment.
The answering insult and bet turn his confidence against him without language about an actual wager.""",
    35: """Preserve the commander's sectarian insult and his claim to the Indian Ocean routes as his own words.""",
    36: """The opponent disparages the foreigners, names the Ming, and threatens anyone who gets in his way.""",
    37: """Gerhard asks the admiral to look at what he has spotted.
Hodram has yet to see what Gerhard means.
Gerhard identifies the apparent slave ship tentatively.
Hodram asks about the prohibition on slave trading.
Gerhard says it remains common and appeals to their role as a patrol fleet.
The first choice orders preparations to attack.
The other choice raises the risk of exceeding their authority.
Gerhard knows the crew has something to hide and argues that the ship is fair game whatever the pretext.
Hodram considers the argument with a quiet acknowledgment.
The battle order names the moment just before the slave ship reaches port.
Charles relishes the opportunity for a show in an amused aside.""",
    38: """Camille spots Lil's fleet and calls it out directly.
Lil addresses Maria by her established name and demands an explanation for the perceived grudge.
Hodram echoes Maria's name in disbelief.
Camille identifies the disguising fleet and cautions Lil.
Lil recognizes Camille in surprise.
Camille explains Kuhn's plan to set Lil and Maria against each other.
Lil starts to object before her certainty fails.
Hodram asks Camille to confirm his claim.
Camille knows Kuhn well and learned about the plot from Maria herself.
Hodram's short acknowledgment keeps the response tactical.
The order names the unidentified fleet straight ahead and calls for aim.
Camille challenges Kuhn to show himself.
Hodram gives the direct order to fire.
The brief native role battle cry keeps the sound of the response.
The profanity expresses the shot's disruption.
The company substitution stays attached to the sighting and Georg warns Kuhn of their disadvantage.
Kuhn accepts that the plan is over and orders the retreat.
Lil recognizes Kuhn and leaves her inference unfinished.""",
    39: """The lookout calls out the enemy fleet ahead.
The attacker's insult and invocation of Yamato belong to the character's challenge.
The first companion reacts to the unusual ship in shock.
The alternate speaker voices the same question.
Hodram identifies the iron plating, which is the design feature the crew sees.
The last voice marvels that such a ship exists.""",
    40: """The abrupt stop order opens the ambush.
Hodram's punctuation preserves a brief wordless shock.
The other ambusher's sardonic taunt tells them they are trapped.
Pasha addresses Hodram through his native surname and declares his exploits over.
Hodram realizes Pasha will never agree to share their sphere in the Mediterranean.
The formal voice stammers at encirclement by many fleets.
The terse alternative breaks the alarm into two short exclamations.
This alternative opens with an actual cry before the report.
The questioning alternative expresses disbelief while reporting many fleets.
The rough voice stammers twice over the size of the encirclement.
The elderly-voiced alternative stays direct while counting the enemy force by impression.
The youthful alternative conveys the quantity without adding a count.
The mature alternative retains the stammer and description of many fleets.
Hodram dismisses his opponents as a mob and orders a breakthrough.
Pasha laughs at Hodram's nerve and demands that his authority be taken seriously.
Hodram needles the general about his rough manners.
Pasha orders a public execution and then a charge by all ships.
The short scream marks the change when the first shots strike.
Pasha demands an explanation for the disruption.
The aide addresses Pasha and identifies incoming fire from town.
Pasha stammers, then demands to know why they are being fired upon.
The other aide still guesses the town batteries were seized.
Sera's short opaque cry stays exactly as the Japanese wrote it. It supplies no recoverable words or profanity.
Sirwood's longer opaque cry adds a prolonged sound in the source. Keep that contrast and both original exclamation marks.
Hodram recognizes something unexpected without naming it yet.
The longer second scream remains audibly distinct.
The first withdrawal command calls only on Mushari's fleet to answer the fire.
The alternate names both Mushari and Arnajud before the order to withdraw.
Hodram repeats the threat of public execution to draw Pasha into facing him.
Pasha answers the challenge and threatens to make Hodram cough up blood.""",
}

EXCHANGES = {(1, block): (0, notes) for block, notes in NOTES.items()}

CHANGES = {
    29: {
        16: ("We can only enforce the law in our own waters.", ("in our own waters.",)),
        38: ("We ask that you stop your ships. We have some questions for you.", ("We ask that you stop your ships.", "We have some questions for you.")),
        49: ("I-it's no use! They won't even look at our signal!", ("I-it's no use!", "look at our signal!")),
        62: ("Tch! What a nuisance. Show that cobbled-together fleet what a real sea battle's like!", ("a real sea battle's like!",)),
        67: ("Charles! What's your plan?", ("What's your plan?",)),
        71: ("Let's use the classic T formation.", ("the classic T formation.",)),
        74: ("Stay clear of their broadsides. Circle ahead or astern. Bring our broadside to bear and finish them with a volley!", ("Stay clear of their broadsides.", "Circle ahead or astern.", "Bring our broadside to bear", "finish them with a volley!")),
        85: ("Time to try out our new cannon!", ("our new cannon!",)),
        88: ("Steer and adjust the sails just as you do out of battle.", ("Steer and adjust the sails", "out of battle.")),
        116: ("Admiral, give us a heading!", ("give us a heading!",)),
    },
    30: {
        13: ("So that's who the port worker meant.", ("the port worker meant.",)),
        30: ("Yes. In a word, he's a monster. And that's not all...", ("he's a monster.", "And that's not all...")),
        40: ("So that's who the port worker meant.", ("the port worker meant.",)),
        43: ("So he meant Barbarossa!", ("he meant Barbarossa!",)),
    },
    31: {
        13: ("You really don't give up. Fine. I'll take you on myself.", ("don't give up.", "I'll take you on myself.")),
        18: ("You really don't give up. I'll take you on myself, before you cross a man you really ought to fear.", ("don't give up.", "I'll take you on myself,", "you really ought to fear.")),
    },
    32: {
        25: ("Listen up, you lot! Show those greenhorns from the edge of Europe how we do things in the Caribbean!", ("Listen up, you lot!", "the edge of Europe", "in the Caribbean!")),
        111: ("N-no... Logically, there's no way we can beat that many!", ("we can beat that many!",)),
        117: ("Wait. Whose flags are those?", ("Whose flags are those?",)),
        132: ("Good timing. We'll back you up.", ("We'll back you up.",)),
    },
    33: {
        5: ("Well fought, FA. You're someone I can count on.", ("I can count on.",)),
        8: ("Maldonado's out of the way, but the English pirates are still causing trouble.", ("the English pirates", "still causing trouble.")),
        12: ("I'd like our agreement to stand. What do you say?", ("I'd like our agreement to stand.", "What do you say?")),
    },
    34: {
        6: ("Ha ha ha! You've got guts, picking a fight with me! Now let's see if you can make this fun!", ("picking a fight with me!", "you can make this fun!")),
    },
    37: {
        21: ("It still happens all the time. How can our patrol fleet turn a blind eye?", ("all the time.", "turn a blind eye?")),
    },
    38: {
        28: ("What are you talking about? But... wait.", ("What are you talking about?",)),
        47: ("Kuhn! Show yourself!", ("Show yourself!",)),
        66: ("Tch. So much for that. Pull back!", ("Pull back!",)),
    },
    39: {
        34: ("A ship plated with iron...!", ("plated with iron...!",)),
    },
    40: {
        27: ("Pasha... So you won't share the Mediterranean with me.", ("the Mediterranean with me.",)),
        58: ("Bwahaha! You've got some nerve! Know who you're dealing with?", ("You've got some nerve!", "Know who you're dealing with?")),
        61: ("Some manners for a general.", ("Some manners for a general.",)),
        76: ("Pasha! Th-the town is firing on us!", ("Th-the town is firing on us!",)),
        79: ("W-what?! Why would they fire on us?", ("Why would they fire on us?",)),
        82: ("I-I don't know! Looks like someone's taken over the town's gun batteries!", ("I-I don't know!", "the town's gun batteries!")),
        125: ("What about my public execution? Come face me.", ("What about my public execution?", "Come face me.")),
    },
}
EDITS = {(1, block, record): decision for block, entries in CHANGES.items() for record, decision in entries.items()}


def main():
    packet = base.load(SOURCE)
    assert len(packet["groups"]) == 13 and sum(len(g["records"]) for g in packet["groups"]) == 177
    for group in packet["groups"]:
        assert len(group["records"]) == len(NOTES[group["block"]].splitlines()), group["block"]
    prior = base.load(PRIOR)
    opaque = {r["id"] for r in prior["records"] if "B40" in r["id"] and "○" in r["english"]}
    assert opaque == {"DK4_MES_B40_R0088", "DK4_MES_B40_R0092"}
    source = getsource(workflow.main).replace(
        '    assert edits_seen == EDITS.keys()',
        '    assert len(records) == 177 and edits_seen == EDITS.keys()',
    ).replace(
        'context=group["context"]',
        'context=CONTEXTS[block]',
    ).replace(
        'for p in (SOURCE, NAMES, parent.RELEASE)',
        'for p in (SOURCE, NAMES, parent.RELEASE, PRIOR, GLYPHS)',
    )
    env = vars(workflow) | globals() | {"LIL": ()}
    exec(compile(source, __file__ + "::paired-review", "exec"), env)
    env["main"]()


if __name__ == "__main__":
    main()
