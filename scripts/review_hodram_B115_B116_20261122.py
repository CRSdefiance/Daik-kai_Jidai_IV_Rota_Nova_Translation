"""Review Hodram's village rescue and the voice who offers a mysterious seal."""

from scripts import review_hodram_B111_B114_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B115_B116_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    115: "The expedition overhears a self-proclaimed prophet inciting his followers against a village. Hodram and the others evacuate the villagers, stop the attackers, and arrange for the villagers to return.",
    116: "A speakerless voice asks about the sea creature and challenges Hodram's claim to rule. He answers honestly while acknowledging his ambition. The voice urges him to obtain a seal and the crew puzzles over a coin.",
}
DECISIONS = {
    115: """
6|||Hodram's short alert interrupts the expedition before anyone understands the sound.
10|||The leader begins with a prolonged sound that Gerhard initially mistakes for singing.
14|||The group's drawn-out response keeps the communal rhythm and leaves Gerhard puzzled.
18|||Gerhard asks whether the sound is music and registers its strangeness. The question suits the discovery.
21|||The leader calls his message a revelation and claims his named society will conquer the world. Keep its established pompous full name.
25|||The leader presents his followers as chosen, promises to dig up the written treasures, and denounces the people he hopes to rule.
28|||The group cheers the claim. The established elongated sound fits their part in the exchange.
32|...Sounds like trouble.|Sounds like trouble.|Gerhard suspects trouble after hearing the speech. His understatement leaves the next announcement to confirm the danger.
35|||The leader explicitly says the village is their first target. His personal grievance shows why the threat is immediate.
39|||The crowd's recurring exclamation backs the leader's resolve. Keep the rhythmic repetition.
43|||Gerhard's wordless shock immediately follows the threat to the villagers. Keep the combined question and exclamation.
47|||Hodram decides they can no longer let the matter go. The concise line shows him committing to intervene.
50|We need to get the villagers to safety. Now!|the villagers to safety.;Now!|Gerhard proposes immediate evacuation. The revised wording makes him urge action in front of the person who confirms it, without inventing rank or orders to others.
54|||Hodram approves the evacuation and orders everyone in the expedition to prepare. The direct response fits the urgency.
57|||Gerhard acknowledges the order in one beat. His quick reply gets them on with the evacuation.
62|||The leader orders his followers to set the village alight and show no mercy. Retain his unambiguous escalation.
65|||The group's short response mirrors the earlier refrain at the point when words turn into action.
77|||Charles's interruption stops the threatened attack. The line needs only his call to wait.
84|||Gerhard backs the interruption with a sharp command. The pair of interjections lets Hodram take over.
88|||The leader's silent punctuation keeps his surprise intact when the expedition steps in.
92|Surrender. We can still settle this peacefully. I doubt you want the army or the state church to try you.|settle this peacefully.;the state church;to try you.|Hodram offers a peaceful resolution and names both authorities before the leader refuses. The threat of trial remains conditional.
95|||The leader stammers at the challenge, insults them and orders his followers to capture them for sacrifice. His reversal keeps the proof of intent in his own words.
99|||The crowd again responds to the leader. The repeated cry fits their increasingly futile support.
103|||Hodram grants their courage and then plainly questions their judgment. The contrast sets up the comic reversal.
114|||Charles calmly tells them to watch their footing at the moment the plan begins. The pause fits his timing.
120|||A single communal cry follows the trip or fall. The English leaves the action to the scene.
132|||The joking guide tone fits the actual pit. The speaker invites the whole group onward in mock courtesy.
138|||The leader realizes what happened and calls his followers over to him. The interruption and profanity keep his loss of control.
143|Oh, that way's closed, too.|that way's closed, too.|Gerhard casually blocks the escape route. His smaller interjection carries the timing of the next reversal.
147|||The repeated pained cries stand on their own. Keep the original pacing between the warning and the capture.
159|||Emilio calls out when they are caught. The short line conveys his satisfaction without describing more action.
166|||Hodram orders the attackers bound after his crew stops them. The existing line is direct and accurately timed.
170|||The crowd's alarm follows the order. Keep the independent reaction in this part of the scene.
174|||The leader watches nearly a hundred of his followers fall in moments. Keep the approximate number and his disbelief.
178|||He asks directly who defeated him. The stammer shows the change from bluster to fear.
182|Why should I answer? You chose to face the army, and it won't show you mercy. Knowing who we are won't help you now.|Why should I answer?;it won't show you mercy.;won't help you now.|Hodram reminds him that he refused to settle and invited severe punishment. His refusal to identify the crew leaves their authority and affiliation as stated elsewhere.
185|||Gerhard notices an object during the capture. His question leaves its identity unstated.
189|||The leader pleads with him not to touch it and laments his failed mission. The stammer and final cry keep his unraveling distinct from earlier grandstanding.
196|Take them away. Once we've brought the villagers home, we'll pull out.|Take them away.;brought the villagers home;we'll pull out.|Hodram orders the prisoners removed and makes the expedition's departure conditional on bringing the villagers back.
200|||Gerhard's short assent closes the expedition's response.
""",
    116: """
6|||The formal voice asks whether Hodram killed the servant it sent out to sea. Keep that act of sending and the scale of the sea in the question.
9|||The captain identifies the servant as the monstrous fish, then admits killing it. Both recognition and admission belong in his reply.
13|||The voice asks whether Hodram then rules this sea. The question preserves its connection to the killing.
16|||Hodram repeats the idea of ruling the sea while considering his answer. The short pause fits the shift in tone.
20|No. I'm nothing so grand. But in a way, that is what we're aiming for...|I'm nothing so grand.;in a way,;what we're aiming for...|Hodram denies already having such standing while admitting that something like it is their goal. Preserve the qualification and the collective aim.
24|||The ceremonial call and injunction keep the reference to a seal. The present line names no location or extra condition.
30|||Hodram asks about the object after the voice's injunction. The abrupt question leaves its identification to the next speaker.
34|||Gerhard recognizes an ancient coin but does not identify a place or date.
38|||Hodram's question leaves the connection between the voice and the coin unresolved.
""",
}
review = checked_text(previous.review, {"len(records) == 51": "len(records) == 49"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::village-and-sea-voice", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

