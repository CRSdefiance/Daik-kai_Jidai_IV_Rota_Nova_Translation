"""Review Mihwa's visit and the monk's directions to the clan guarding the map."""

from scripts import review_hodram_B300_B303_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = previous.base, previous.ROOT
OUTPUT = ROOT / "B304_B308_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    304: "Mihwa parts company with Hodram before the expedition. The party finds a swamp and can cross it as a shortcut or backtrack. Both paths lead to the destination after distinct effects.",
    305: "Mihwa invites Hodram to visit a temple. He asks about the golden temple on his map. Mihwa offers to accompany him partway and says he can follow the map after that.",
    306: "Hodram recalls the monk's request at Kinkaku-ji and identifies the Yuan emperor's keepsake by its exact item name.",
    307: "Hodram brings the keepsake to the monk. The monk gives precise directions to a village of map guardians far northeast of China and warns against both the voyage and misuse of the Proof.",
    308: "Each crew voice recalls the clan said to guard the map to the Proof and talks about visiting the village. The eight alternatives have different levels of urgency, familiarity and uncertainty.",
}
DECISIONS = {
    304: """
12|||Mihwa asks whether Hodram has a map. The short conversational question suits the moment before setting out.
16|Oh, I forgot it.|I forgot it.|Hodram suddenly remembers he left without the map. The brief response keeps that realization.
30|||Mihwa tells Hodram this is where they part, then wishes him a safe journey. The friendly sendoff fits their conversation.
35|Thanks. I appreciate it.|I appreciate it.|Hodram acknowledges the farewell with sincere thanks.
SC1_B304_STYLE_164_0|Come on, let's get going.|let's get going.|Three crew styles share this invitation to set out. The existing consumer remains the same.
SC1_B304_STYLE_164_20|||The casual voice energetically urges everyone to set out.
SC1_B304_STYLE_164_36|||The rough crew member's plain invitation suits the moment they move.
SC1_B304_STYLE_164_50|||The older crew member signals that they should leave in his measured voice.
SC1_B304_STYLE_164_68|||The youthful speaker exclaims with enthusiasm at setting out.
SC1_B304_STYLE_164_84|||The formal crew member politely asks whether it is time to go.
SC1_B304_STYLE_296_0|||The speaker points out the swamp ahead and asks what to do.
SC1_B304_STYLE_296_30|A swamp ahead... What should we do?|A swamp ahead...;What should we do?|The measured speaker pauses on recognizing the swamp before asking for a decision.
SC1_B304_STYLE_296_58|||The casual voice says they have run into a swamp and asks what to do.
SC1_B304_STYLE_296_92|||The speaker is mildly surprised to see a swamp before asking for a decision.
SC1_B304_STYLE_296_120|||The rougher crew member asks for a plan after recognizing the obstacle.
SC1_B304_STYLE_296_150|||The older voice considers the swamp and asks the admiral what to do.
SC1_B304_STYLE_296_176|Huh? A swamp! What are we gonna do?|What are we gonna do?|The youthful speaker is surprised to come up against a swamp and asks for help deciding.
SC1_B304_STYLE_296_220|||The formal speaker recognizes a swamp ahead and asks the group how to proceed.
SC1_B304_CHOICE_576_0|||Enter the swamp chooses to risk crossing it.
SC1_B304_CHOICE_576_1|||Go back chooses to take a different route around it.
98|We're going through the swamp.|through the swamp.|Hodram commits the group to moving through the swamp after the player's choice.
SC1_B304_STYLE_638_0|||The speaker is surprised to discover that the water is shallower than expected.
SC1_B304_STYLE_638_18|||The measured voice gives a plain comparison with what he expected.
SC1_B304_STYLE_638_40|||The casual speaker recognizes the shallow water and expresses relief.
SC1_B304_STYLE_638_66|||This crew member says it is shallower than expected and shares her relief.
SC1_B304_STYLE_638_94|||The rough crew member reacts in a short, informal turn.
SC1_B304_STYLE_638_112|||The older voice remarks with quiet surprise that the water looks shallower.
SC1_B304_STYLE_638_132|||The youthful crew member exclaims in surprise at the shallow water.
SC1_B304_STYLE_638_158|||The formal voice notes that even his estimate was too high.
129|That should have saved us quite a bit of time.|quite a bit of time.|Hodram thinks crossing directly gave them a considerable shortcut. Keep the estimated benefit.
133|||Gerhard agrees that they should now be near the destination.
137|Your sailors look tired.|Your sailors look tired.|The notice reports apparent sailor fatigue. Match the equivalent notice on the earlier expedition.
148|||Hodram judges that they cannot cross this swamp and chooses to go back and try another route.
155|One day passed.|One day passed.|The panel gives the original one-day delay in the same terms as the earlier expedition notices.
159|||Hodram notes the size of the detour after the party has taken it.
162|||Gerhard thinks they should be near the destination now but lets the lingering doubt stand.
168|||The lookout stammers while telling the admiral the party has found the place.
""",
    305: """
6|||Mihwa is glad to see the captain. Her greeting keeps the original given-name substitution.
10|||Mihwa says she is visiting a temple today and invites Hodram in her friendly voice.
13|||Hodram hesitantly explains he is not Buddhist. The pause leaves space for Mihwa to reassure him.
17|||She reassures him they can just look around. Her ease matches the light invitation.
20|||The unfinished thought shows Hodram has just remembered the temple marked on his map.
24|||He asks whether the golden temple on the map is near the temple Mihwa is visiting.
27|Golden? Oh, that temple! It's a fair way off...|Oh, that temple!;a fair way off...|Mihwa takes a moment to recognize the temple and explains it is not close to her destination.
31|Then let's walk together partway. After that, follow your map and you should get there.|walk together partway.;follow your map;you should get there.|She offers to accompany Hodram for part of the journey and thinks the map will guide him the rest of the way.
""",
    306: """
13|||Hodram recalls the request from the monk at Kinkaku-ji. The memento belonged to a Yuan emperor.
19|Kublai's Greatsword... This must be the Yuan emperor's keepsake the monk at Kinkaku-ji asked us to find.|Kublai's Greatsword...;the Yuan emperor's keepsake;at Kinkaku-ji|Hodram recognizes the exact named item as the keepsake the monk sought. Preserve the specific item and temple names.
""",
    307: """
12|||Hodram repeats the monk's request in the same terms as the earlier journal reminder.
16|||Gerhard says the item must be unequipped before it can be presented. Keep the established player-facing action.
30|Excuse me.|Excuse me.|Hodram announces himself politely. The brief address gives the monk the next turn.
34|||The monk recognizes the visitor and reacts with surprise that this is the very item he described.
38|||The monk judges that Hodram can handle what comes next. The tentative approval suits the following directions.
42|Look for a small village by the icy sea, far northeast of China. The clan that guards the map should live there.|a small village;far northeast of China.;the map should live there.|The monk gives the village size, the coast and its direction relative to China. He is fairly confident that the map's guardians are there.
45|||Hodram repeats the direction, letting its distance sink in before the monk refines it.
49|Look on the east coast near the base of a vast peninsula, at the foot of a high peak.|the east coast;the base of a vast peninsula,;at the foot of a high peak.|The monk supplies all three navigation clues together. Keep the coast, the base of the peninsula and the mountain's foot distinct.
52|||The monk warns that an ordinary ship may struggle to reach the remote place. He says a halfhearted attempt could cost their lives.
55|||Leave the pause after the danger warning. Hodram takes in what the monk has just said.
59|Never hand the Proof of Conquest to anyone with evil intentions. And don't let such desires take hold of you.|Proof of Conquest;with evil intentions.;take hold of you.|The monk says to keep the Proof from anyone with wrongful intentions and warns Hodram against the same temptation.
62|We'll take that to heart.|take that to heart.|Hodram promises to remember the warning in a respectful reply.
""",
    308: """
SC1_B308_STYLE_8_0|Admiral, we should visit the clan guarding the map to the Proof. Their village was far northeast of China, right?|the map to the Proof.;far northeast of China, right?|This crew member encourages the visit and checks the village's direction in a familiar question.
SC1_B308_STYLE_8_90|Admiral, let's go meet the clan guarding the map to the Proof as soon as we can. Their village is far northeast of China.|the map to the Proof;as soon as we can.;far northeast of China.|The more formal voice urges a prompt visit and recalls the direction as a statement.
SC1_B308_STYLE_8_192|Wonder what that clan's like, Admiral. The one guarding the map to the Proof. Way northeast of China, right? Let's go see!|that clan's like, Admiral.;the map to the Proof.;northeast of China, right?;Let's go see!|The casual crew member wonders about the clan and asks to go see them right away.
SC1_B308_STYLE_8_300|Admiral, let's go see the clan that guards the map to the Proof before we forget. Their village is far northeast of China, isn't it?|the map to the Proof;before we forget.;northeast of China, isn't it?|This speaker suggests acting before they forget and checks the monk's direction. Preserve the question tag as speech.
SC1_B308_STYLE_8_404|||The rough crew member calls for a quick visit, then confirms the location of the village beyond China.
SC1_B308_STYLE_8_498|Admiral, about that Proof... We ought to visit the clan guarding its map soon. Shall we head for that village far northeast of China?|about that Proof...;the clan guarding its map;far northeast of China?|The older crew member raises the Proof deliberately, then proposes heading to the distant village.
SC1_B308_STYLE_8_614|||The youthful speaker wants to meet the people who guard the map and proposes a trip to the village.
SC1_B308_STYLE_8_716|Admiral, I'm curious about the map to the Proof. Shall we visit the village where the clan guarding it is said to live? Far northeast of China, as I recall.|the map to the Proof.;is said to live?;northeast of China, as I recall.|The formal speaker wonders about the map, treats the clan's residence as a report and recalls the direction after a pause.
""",
}

review = checked_text(previous.review, {"len(records) == 125": "len(records) == 67"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::mihwa-and-map-guardians", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
