"""Review the figurehead choice and the ice puzzle with every voice and branch."""

from scripts import pair_hodram_B241_B260_20261122 as paired
from scripts import review_hodram_B244_B250_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B251_B252_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    251: "Hodram and Cesare discover a strangely warm figurehead. If they take it, a voice promises to watch over them, but only Cesare reacts to it. If they leave it, they return to town while Cesare reflects on it. Each choice has its own pair of stat notices.",
    252: "Fernando finds a wall puzzle about floating ice. Each incorrect stone leads to a collapse warning and retreat. The correct stone opens the wall, where a statue speaks. Agreeing that they woke it leads to an offer of power and an order to leave. Disagreeing offends the voice and sends the crew running.",
}
DECISIONS = {
    251: """
5|||Cesare asks why Hodram stopped, using his usual address.
9|...Do you feel anything when you look at this statue? A strange sort of warmth...|look at this statue?;A strange sort of warmth...|Hodram pauses, asks what Cesare feels, and identifies the warmth as an impression.
15|||Cesare asks where the statue is. The double question shows that he has not noticed it yet.
18|||Hodram points out its position with the briefest possible reply.
22|Let's see...||Cesare leans in for a look. The pause cues the closer inspection.
26|Oh, it's a figurehead! Look at all that detail. Yes, I can feel something, too.|it's a figurehead!;all that detail.;I can feel something, too.|Cesare identifies it and remarks on the workmanship before confirming the same unusual sensation.
33|Do you think it's well known?|well known?|Hodram wonders whether the figurehead has a reputation. He has yet to name it.
37|I've never heard of it. Wait, are you thinking of taking it?|never heard of it.;thinking of taking it?|Cesare says he does not recognize it, then realizes what Hodram might be planning.
SC1_B251_CHOICE_432_0|||Exactly confirms Cesare's suspicion and continues toward moving the figurehead.
SC1_B251_CHOICE_432_1|||No declines that idea and leads to the separate departure.
53|It is a magnificent figurehead. It might bring us luck if we put it on the ship. But is it all right to take it without asking?|a magnificent figurehead.;if we put it on the ship.;to take it without asking?|Cesare sees a possible benefit but asks whether it is acceptable to take it. The luck is his expectation here.
56|What a waste to leave a figurehead this fine on land. Don't you think?|a figurehead this fine;Don't you think?|Hodram makes a practical case for taking it and asks Cesare to agree.
60|Oh, how very kind of you, Admiral! Well then, let's get it moving!|kind of you, Admiral!;let's get it moving!|Cesare dramatically praises the admiral's kindness and takes the decision as a cue to act.
64|Excuse us, figurehead. Would you mind coming with us?|Excuse us, figurehead.;coming with us?|Cesare pointedly apologizes to the figurehead and asks it to come along. Preserve his politeness to the object.
67|||The speakerless promise to watch over them answers Cesare. The voice remains unidentified in its panel.
70|W-what was that voice?!|W-what was that voice?!|Cesare stammers at the voice. The reaction leads to Hodram asking him to help.
73|||Hodram calls for a hand with the work. His response gives no sign that he heard the voice.
76|||Cesare insists he just heard a voice, then trails off.
80|Are you half asleep?|Are you half asleep?|Hodram wonders whether Cesare was dreaming or groggy. The mild tease follows Cesare's unexplained reaction.
85|||The notice preserves the playable captain's given-name substitution and one point of Luck.
89|||This separate notice credits Cesare, by name, with one point of Luck.
92|(Who was that? Such a warm, loving voice...)|Such a warm, loving voice...|Cesare privately wonders whose voice he heard and recalls its warmth and kindness.
99|||Cesare agrees aloud but feels disappointed. The thought stays in the parenthesis on the refusal branch.
103|||Hodram suggests returning to town. His brief direction keeps the scene moving.
110|Yes, let's. (It was a beautiful figurehead. Just looking at it seemed to cleanse my heart...)|a beautiful figurehead.;seemed to cleanse my heart...|Cesare agrees aloud, then recalls what simply looking at it seemed to do to him.
113|||The notice gives the playable captain one point of Charm on the refusal branch and preserves the original substitution.
117|||This separate notice gives Cesare one point of Charm on the same branch.
""",
    252: """
6|||Fernando calls over the admiral and points out the writing. His opening matches the urgency of the discovery.
9|A vessel is filled to the brim with water. A piece of ice floats on the surface. What happens to the water level when the ice melts?|to the brim;A piece of ice;on the surface.;when the ice melts?|The inscription gives a full vessel and one floating piece of ice, then asks what melting does to the level.
12|Press the front stone if it rises, the left stone if it falls, or the right stone if it stays the same.|the front stone;the left stone;the right stone;stays the same.|The inscription maps each answer to its distinct direction. Keep rise, fall, and unchanged in order.
SC1_B252_CHOICE_270_0|||Front stone matches the inscription's first direction and preserves its incorrect branch.
SC1_B252_CHOICE_270_1|||Left stone matches the second direction and preserves the other incorrect branch.
SC1_B252_CHOICE_270_2|||Right stone matches no change and the successful branch.
31|||Hodram commits to pressing the stone in front. His confidence makes the immediate reaction clear.
SC1_B252_STYLE_340_0|||This voice identifies the collapsing ceiling first, then warns of the danger here.
SC1_B252_STYLE_340_46|||This alarm puts danger first. The second sentence identifies the falling ceiling.
SC1_B252_STYLE_340_86|||This voice calls out urgently to the admiral and immediately says the ceiling is collapsing.
SC1_B252_STYLE_340_126|||This voice notices the danger and urges everyone to run. The escape instruction is part of this alternative.
SC1_B252_STYLE_340_176|||The brisk shout warns people to look out. The contraction fits the casual voice.
SC1_B252_STYLE_340_212|||The older voice observes that the ceiling is falling and advises leaving.
SC1_B252_STYLE_340_264|Aaaah! Th-the ceiling's coming down!|Th-the ceiling's coming down!|This voice cries out and stammers in panic. Preserve both features of the source.
SC1_B252_STYLE_340_298|||The measured voice gives the cause and warns against staying. It names the danger without adding another action.
53|||Hodram recognizes the wrong answer, identifies immediate danger, and orders a return to town.
68|||Hodram uses the same confident response before pressing the left stone.
SC1_B252_STYLE_822_0|||Repeat the same voice and danger assessment when the left stone is pressed.
SC1_B252_STYLE_822_46|||The caller again leads with danger and identifies the collapsing ceiling.
SC1_B252_STYLE_822_86|||This speaker gives the same direct alarm on the other wrong branch.
SC1_B252_STYLE_822_126|||This caller again includes the instruction to run. Each branch has its own stored voice object.
SC1_B252_STYLE_822_176|Look out! The ceiling's coming down!|The ceiling's coming down!|Match the identical casual source warning on the other failed attempt.
SC1_B252_STYLE_822_214|||The older voice observes the ceiling and advises leaving, as before.
SC1_B252_STYLE_822_266|Aaaah! Th-the ceiling's coming down!|Th-the ceiling's coming down!|Keep the same stammer and alarm as this voice's matching call.
SC1_B252_STYLE_822_300|||The measured voice repeats the warning that staying here is dangerous.
90|||Hodram repeats the same response to a wrong answer, including the return to town.
106|When floating ice melts, the water level stays the same.|floating ice melts,;the water level;stays the same.|Hodram explains the right answer under the floating-ice condition in the inscription.
112|||Fernando sees the wall opening. Keep his discovery separate from the reaction that follows.
116|||The punctuation is the original anonymous reaction. Keep its selector and nonverbal content.
120|||Fernando calls the admiral's attention to the strange statue. The short reaction fits the opening.
123|||Hodram asks where it is before Fernando shows him.
127|Right here. It looks like a figurehead...|looks like a figurehead...|Fernando points to it and offers a tentative identification.
130|||The speakerless double crack is an interruption, distinct from the voice.
134|W-what was that?!|W-what was that?!|Fernando reacts to the crack with the source stammer.
138|||The voice asks who woke it. The question has the dignity and abruptness of the original.
142|Whoa! A-Admiral!|A-Admiral!|Fernando reacts in fear and stammers the address to Hodram.
145|||The voice demands an answer. The one-word command fits its turn.
SC1_B252_CHOICE_1606_0|||Yes accepts responsibility for waking the voice and opens its offer.
SC1_B252_CHOICE_1606_1|||No denies it and leads to the voice's indignation.
160|||The voice offers to let them wield its power. Its formal tone fits the demand that preceded the answer.
164|||Fernando's puzzled response leaves room for the voice to explain.
168|||The voice gives permission to take the statue where its power dwells, then orders them to leave promptly.
174|...What was that? This thing won't curse us if we use it, will it?|won't curse us;if we use it,;will it?|Fernando asks what they encountered and worries the figurehead might curse them. The short tag keeps his uncertainty in voice.
178|Who knows? I have no idea either.|no idea either.|Hodram admits he does not know any more than Fernando. The dry reply closes the question.
184|||The voice is offended by the idea that it awoke of its own accord and threatens to prevent their departure.
195|||The noise is a drawn-out roar after the threat. Its speakerless panel preserves the sound.
207|A-Admiral! Let's get out of here!|A-Admiral!;get out of here!|Fernando stammers and urges the admiral to run before the group order.
212|||Hodram orders everyone to run. The source urgency suits the retreat.
223|Hah, hah, hah... Whew, that was close.|Hah, hah, hah...;that was close.|Fernando catches his breath after running and reacts to the narrow escape.
226|||Fernando notices a sudden heaviness in his body. Keep his sensation separate from the preceding relief.
""",
}

review = checked_text(previous.review, {"len(records) == 30": "len(records) == 77"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::figurehead-and-ice-puzzle", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
