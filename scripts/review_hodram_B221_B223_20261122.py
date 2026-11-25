"""Review Ian's spear rumor and Julian's conversation with Lucia."""

from scripts import pair_hodram_B221_B240_20261122 as paired
from scripts import review_hodram_B217_B220_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B221_B223_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    221: "Ian brings Hodram a rumor about Ares's spear and other equipment associated with the Olympians. Hodram asks where to look and is surprised that Ian cares so much. Ian describes how the thought of finding an object from the myths makes the ancient world seem close.",
    223: "Julian flirts with Lucia and compares her to the empress from a rumor about protective clothing. Lucia questions the compliment and becomes interested in the empress's jewelry. Julian leaves abruptly, and she remarks that he always goes when she is about to ask for something.",
}
DECISIONS = {
    221: """
5|Admiral, I heard something in town about a remarkable weapon.|heard something in town;about a remarkable weapon.|Ian reports an interesting lead he picked up in town. The word order keeps the source of the story clear.
8|Oh? What's it called?|What's it called?|Hodram shows interest before asking the weapon's name. The short question follows Ian's opening.
11|||Ian names the Holy Spear of Ares and explains the legend that one of the twelve Olympians carried it. Preserve the established item name and specific number of gods.
14|||Hodram explicitly recognizes Ares as the god of war and asks where to find the spear. The interest and location question both belong to this reaction.
18|Rumor has it there may be armor lying near it, too, named for other Olympians.|Rumor has it;armor lying near it,;other Olympians.|Ian relays the possibility of other divine names on nearby armor. The armor is said to lie near the spear, and its presence remains uncertain.
21|Hold on. That doesn't answer my question.|doesn't answer my question.|Hodram points out that Ian still has not said where the spear itself is. His impatience follows the sidetrack.
24|From the way people in town talked, I'd guess it's somewhere nearby... I'd love to find it.|people in town talked,;somewhere nearby...;I'd love to find it.|Ian can only infer a rough location from the townspeople. His desire to find it becomes clear before Hodram reacts privately.
28|(Well, now. He really is interested.)|He really is interested.|Hodram privately notices Ian's interest. The quiet surprise sets up Ian noticing the look on his face.
32|||Ian sees Hodram looking at him oddly and asks whether his interest in legends is surprising. The questions give Hodram a direct reason to answer.
36|||Hodram plainly confirms that he is surprised. Leave the longer explanation to Ian.
40|I suppose so. Stories like that really do move me. Just think of all those gods from the myths, roaming this very land...|Stories like that;gods from the myths,;this very land...|Ian acknowledges the surprise and explains that mysterious legends move him. His image of the gods traveling through the land leads to the next turn.
43|Just thinking that weapons they might have used are still out there takes me right back to ancient times.|weapons they might have used;still out there;back to ancient times.|Ian imagines old weapons surviving into his own time. The thought carries him back in imagination, and the possibility stays qualified.
46|||Hodram takes in Ian's enthusiasm with a pause. The quiet acknowledgment suits the end of his explanation.
""",
    223: """
5|||Julian greets Lucia by name and says he travels here to see her noble, lovely eyes. The elaborate compliment suits his flirtatious opening.
8|||Lucia recognizes Julian's usual smooth talk and returns the greeting. The teasing is directed at him.
12|||Julian pauses as a thought occurs to him. The shift gives Lucia a reason to ask why he is staring.
16|||Lucia asks what is wrong and whether something is on her face. The familiar question is a natural response to his look.
19|I see it now... Maybe that legendary empress was a woman like you.|I see it now...;a woman like you.|Julian connects the empress in the rumor with what he sees in Lucia. He voices it as a possibility.
23|||Lucia asks what he means because he has brought up the empress without explanation.
27|Sorry, that came out of nowhere. I just heard about some armor called the Empress Gown, and it got me thinking.|came out of nowhere.;the Empress Gown,;got me thinking.|Julian acknowledges the abrupt comparison and explains what put it in his mind. Preserve the game item and its equipment category.
31|||Lucia repeats the name as a question. The brief reply keeps him speaking about the gown.
35|||Julian recounts the rumor of a beautiful Chinese empress who wore the gown and ruled as she pleased before a tragic end. Preserve the hearsay and the phrase Lucia picks up on.
39|She must have been frighteningly beautiful, the kind of woman who could steal a man's heart with one look. Doesn't that sound like you?|frighteningly beautiful,;steal a man's heart;with one look.;sound like you?|Julian imagines how beautiful the empress must have been and turns that idea into a compliment. Her effect on men remains his imagination.
42|If she ruled as she pleased, wouldn't that make her selfish and overbearing? Do you think I'm that mean?|ruled as she pleased,;selfish and overbearing?;think I'm that mean?|Lucia challenges the less flattering part of his comparison. Her wording echoes his account of the empress's rule.
46|Don't be silly. A woman's more charming when she wants her own way once in a while. Oh, about as often as you do.|wants her own way;once in a while.;as often as you do.|Julian tries to turn Lucia's objection into a playful compliment by praising just a little wilfulness. His last beat points the tease back at her.
50|||Julian returns to the idea of a gown meant to protect a beautiful woman and calls it romantic. The short tag checks whether Lucia shares his reaction.
53|||Lucia questions his romantic reading and says she would be more interested in the jewelry the empress wore. Preserve the rings and necklaces she names.
57|You mean what they were worth? You women are so practical! Oh, I'd better go. See you around.|what they were worth?;so practical!;See you around.|Julian assumes Lucia is thinking about price, teases her and abruptly makes his exit. The assumption is his, and her reply exposes the pattern.
61|||Lucia says goodbye before making her separate observation. Keep the brief farewell in the exchange.
65|Honestly... He always runs off just when I'm about to ask for something.|always runs off;about to ask for something.|Lucia observes that Julian tends to leave before she can ask for anything. Preserve the timing that makes his hasty departure the joke.
""",
}

review = checked_text(previous.review, {"len(records) == 48": "len(records) == 30"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::ian-and-lucia", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
