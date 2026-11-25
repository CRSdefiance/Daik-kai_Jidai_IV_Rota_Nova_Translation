"""Review the village of believers and the Colosseum and urn puzzles."""

from scripts import review_hodram_B111_B114_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B117_B119_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    117: "An isolated village recognizes fellow believers. Hodram's question about the Proof prompts them to give him their village's lamp and ask him to keep the treasure from the Ottoman Empire.",
    118: "The Colosseum voice asks a doubling puzzle. On wrong-answer branches Gerhard admits he is stumped and Hodram guesses. On the successful branch Hodram sees the solution and the voice rewards him.",
    119: "Different crew voices announce a dead end. An inscription gives a clue involving an urn and the left hand. The original actions and reactions stay distinct, including the injury notice.",
}
DECISIONS = {
    117: """
6|||The villager asks who they are, then recognizes something about them and trails off. The following turn explains their excitement.
9|||The villager is relieved to have met people of the same faith after a long time. The line gives that recognition without naming a denomination.
12|||The speaker says the community fled Muslim rule and kept its faith while living quietly. Preserve this historical perspective in the villager's voice.
16|Forgive me for asking so suddenly. We're looking for a treasure called the Proof of Conquest. Does anyone here know the old legends?|asking so suddenly.;the Proof of Conquest.;the old legends?|Hodram acknowledges the abrupt question and asks about people who know old traditions. His manner remains polite while he names the treasure.
19|||The question and exclamation carry the villager's surprise followed by a conviction that God brought the crew. Preserve the attribution.
23|||Hodram asks if the villager knows the Proof. The brief question lets the response reveal more than mere knowledge.
27|More than that...|More than that...|The villager implies that the community has more to offer than information. The pause leads into the presentation of their lamp.
31|||The village has handed the lamp down and believes that a seeker will need it. The wording separates inherited lore from the community's decision to entrust the lamp to the crew.
36|||The villager pleads with them to keep the Proof from the Ottoman Empire. The request keeps the treasure and the named power explicit.
40|||Hodram promises their best efforts. The current wording makes a sincere commitment without guaranteeing success.
""",
    118: """
7|||The voice addresses Colosseum visitors and orders them to answer. The ceremonial opening preserves the place and command.
10|||Hodram's quiet astonishment makes the voice's interruption clear. His question repeats the key word.
14|||The voice introduces the riddle in a separate short notice. Keep the original pause before its setup.
18|||The voice describes the miraculous bean by doubling it each second. All three quantities and elapsed times remain explicit.
22|||The question keeps one bean filling the bag in 60 seconds and asks when it will fill if they start with two. Both starting quantities and the time limit support the puzzle.
25|||The terse direction introduces the three answer slots. It keeps the choice separate from the puzzle's premise.
SC1_B118_CHOICE_372_0|||The first caption offers one second and retains its own rejection branch.
SC1_B118_CHOICE_372_1|||The second offers 30 seconds and keeps its distinct rejection branch.
SC1_B118_CHOICE_372_2|||The third offers 59 seconds and leads to the correct response.
45|||Hodram asks Gerhard if he has an idea. The short question fits the uncertainty of this branch.
49|||Gerhard admits he is stumped and suggests guessing. He leaves the choice to Hodram.
52|||Hodram picks the one-second answer when reason fails him. The existing line preserves his brief deliberation before committing.
56|||The voice responds to the one-second guess with a short insult. Keep the original speakerless rejection.
66|||The same question recurs on the 30-second path. Keep its separate call and the same familiar tone.
70|||Gerhard's helpless response matches the first wrong-answer path and stays in its own branch.
73|||Hodram echoes the suggestion and commits to 30 seconds. The shorter deliberation is present in the source.
76|||The voice delivers the same insult after the different guess. The repetition belongs to the branches.
87|||Hodram addresses Gerhard with new confidence after solving the puzzle. The current line fits the change.
91|||Gerhard praises the success and asks for the answer. The two short clauses preserve his enthusiasm.
94|||Hodram gives the exact answer. Its plain delivery contrasts with the earlier guesses.
98|||The voice praises both wisdom and courage and presents a reward. Its ceremonial language gives the right weight to success.
""",
    119: """
SC1_B119_STYLE_16_0|||The first polite voice reports a dead end plainly and addresses the admiral.
SC1_B119_STYLE_16_24|||This formal variant reports that the group has reached a dead end. Preserve its distinct phrasing and slot.
SC1_B119_STYLE_16_46|||This voice reacts with a surprised question first. Keep the light response without adding the rank used elsewhere.
SC1_B119_STYLE_16_70|It's a dead end, Admiral.|It's a dead end, Admiral.|This voice observes the obstacle and addresses the admiral. Moving the address to the end gives its native slot a distinct conversational cadence without adding personality details.
SC1_B119_STYLE_16_92|||Whoa and the casual observation preserve this version's more informal register.
SC1_B119_STYLE_16_116|||This older-sounding voice addresses the admiral and concludes they are at a dead end. The final then suits its cadence.
SC1_B119_STYLE_16_142|||This version calls out to the admiral. The separate exclamation conveys the drawn-out source address.
SC1_B119_STYLE_16_170|||The introductory Well conveys the speaker's mild realization. This variant names no addressee.
33|||The narration identifies an urn-shaped stone tablet set into place. Its material and shape are available before the inscription.
36|||The inscription addresses a traveler and says to pour from the sacred urn with the left hand. Preserve the hand and the act precisely.
39|||The crew member puzzles out the hand and urn as a spoken question. Keep the same role selector and thinking pause.
SC1_B119_CHOICE_336_0|||Push is the simple first interaction label and preserves its native branch.
SC1_B119_CHOICE_336_1|||Turn right preserves the direction and remains distinct from the opposite action.
SC1_B119_CHOICE_336_2|||Turn left preserves the opposite action and its original choice position.
60|||The brief wordless shock belongs to this branch. Retain punctuation and dynamic speaker.
66|||The crew's inference links pouring with the left hand to a tilt to the right. Keep the physical reasoning tentative and the direction exact.
70|||The repeated punctuation conveys a fresh reaction at the corresponding source command. Keep its own role selector.
82|||The same reaction recurs under different conditions. Preserve this separate record and voice resolution.
89|||Hodram tells the crew to run. The lone command keeps the immediate danger and timing.
93|||The injured sailor's cry precedes the status notice. Leave it as a reaction without supplying a diagnosis.
100|||The impersonal notice states a sailor is hurt. No severity or rank is specified by the source.
""",
}
review = checked_text(previous.review, {
    "len(records) == 51": "len(records) == 52",
})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::village-and-puzzles", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

