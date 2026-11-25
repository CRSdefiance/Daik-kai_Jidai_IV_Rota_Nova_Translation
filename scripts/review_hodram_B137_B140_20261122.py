"""Review Camille's apology, the North Sea map, and Diogo's proposal."""

from scripts import review_hodram_B131_B132_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B137_B140_contextual_v1.json"
GLYPHS = {f"DK4_MES_B137_R{n:04d}" for n in (21,35,74)}
CONTEXTS = {
    137: "Camille returns to apologize for Lil. Charles reacts angrily, then Hodram accepts the apology and reassures Camille. The crew notices his promise and considers recruiting.",
    138: "Hodram recalls Lil's challenge. Gerhard proposes using Red Dye on the blank Old Parchment and the two recognize the map that appears.",
    139: "A port worker gives Hodram a warning about the southern Mediterranean and declines to say why.",
    140: "The guildmaster introduces Diogo de Escante. Diogo seeks help against Vasquez de Maldonado, whom he accuses of piracy. Hodram questions his motives before deciding whether to hear from Gerhard or accept directly.",
}
DECISIONS = {
    137: """
6|||Charles's brief reaction opens the unexpected meeting before he recognizes Camille.
10|Um... I wanted to apologize for earlier.|to apologize for earlier.|Camille hesitates, then apologizes for what happened earlier. His wording prepares for the longer apology after Charles recognizes him.
14|You're the one who was with that brat! What are you doing here?!|with that brat!;What are you doing here?!|Charles remembers Camille as the person accompanying Lil. His insult and demand keep his earlier anger alive.
17|||Camille says he came to apologize to all of them and condemns what Lil said. The repetition reflects his nervous sincerity.
21|...||Charles falls silent for a beat after Camille's apology. Restore the ordinary English dots and keep the original speaker selector.
25|||Camille distinguishes Lil's intent from how she actually came across. He does not deny that the crew was upset.
28|||Camille explains that Lil speaks this way when she thinks she is facing a business rival. The existing hesitation keeps the explanation personal.
32|She's kind, really. She just jumps to conclusions and gets carried away. Please forgive Lil!|She's kind, really.;jumps to conclusions;Please forgive Lil!|Camille defends Lil's kindness while admitting that she jumps to conclusions and acts on her assumptions. His plea still names her.
35|...||Gerhard's separate silence leaves room for Hodram's reply. Restore ordinary English punctuation without changing the beat.
39|Camille, was it?|Camille, was it?|Hodram checks his recollection of the name before responding to the apology. Preserve the approved name and the complete short tag.
43|||Camille is surprised to be addressed and confirms his name. The brief recovery fits Hodram's direct question.
47|||Hodram graciously accepts the apology and credits Camille with helping Lil make the most of her abilities.
50|||Camille stammers and protests the compliment. Keep his modesty audible.
54|||Hodram reassures Camille that neither of them will be harmed and asks him to pass the message on. His distinction between rivals and chosen enemies stays explicit.
58|||Camille sounds relieved and thanks them before excusing himself. The current succession of reactions fits his departure.
74|...||Hodram pauses after Camille leaves. Preserve the separate silence in regular English dots.
78|||Gerhard calls Camille promising. The terse assessment is appropriately warmer than the crew's initial reception.
82|||Hodram moves from Camille's potential to his own fleet's staffing. His thought is prompted by the conversation.
86|||Gerhard says the fleet needs more capable people to expand. Keep the condition and the distinction from replacing injured sailors.
89|||Gerhard cites maritime trade in the Mediterranean and suggests Lisbon and Seville as places to look. He treats recruitment as a possibility.
92|||Hodram agrees and proposes extending the fleet's routes to other Mediterranean towns as well.
""",
    138: """
5|||Hodram recalls the precise challenge about finding the treasure first. The line keeps the claim attributed to the earlier challenger.
8|Could the Red Dye have something to do with finding the Proof of Conquest?|the Red Dye;the Proof of Conquest?|Hodram suspects the dye may play a part in obtaining the Proof. He has yet to discover exactly how.
12|||Gerhard notes that the Old Parchment from the ruins looks blank. His concern is the reason for interrupting.
16|What do you mean?|What do you mean?|Hodram asks what Gerhard is getting at. The direct question gives him room to explain.
20|||Gerhard reasons that the earlier man's interest in the parchment means it must have a secret. The claim remains his inference.
23|What if we pour the Red Dye on it? That might reveal something...|we pour the Red Dye;reveal something...|Gerhard proposes applying the dye to the parchment. The suggested action and tentative result remain explicit.
26|||Hodram notices a change. Keep the brief reaction without naming what has appeared yet.
30|||Gerhard sees it too and stammers. His short reaction precedes recognition of the map.
34|||Hodram's pause preserves the moment of looking at the result before either speaks.
38|||Gerhard identifies what looks like a map, then leaves the inference for Hodram.
41|||Hodram confirms the implication in a few words. His certainty contrasts with Gerhard's earlier suggestion.
45|||Gerhard recognizes the route to the North Sea Proof. The excitement and exact region fit the reveal.
48|||Hodram orders preparations to sail right away. The command closes the exchange with a concrete next action.
""",
    139: """
7|||The port worker gives a plain warning tying the southern Mediterranean to the passage through Gibraltar. Keep both locations.
10|||Hodram wants a reason for the unsolicited advice. His question fits the short exchange.
14|||The port worker refuses to elaborate and repeats the warning as personal advice. The wording leaves his reasons unexplained.
""",
    140: """
5|||The guildmaster introduces someone Hodram has yet to meet. The brief lead gives the next line room to name the visitor.
9|||The guildmaster introduces Diogo by his full approved name and identifies his stated office as governor of Mexico.
13|A pleasure.|A pleasure.|Diogo offers a courteous, perfunctory greeting before Hodram asks why he is here.
17|||Hodram notes that the governor has come in person and presses him for his purpose. The edge in his words explains the interruption.
20|||The offended speaker sharply demands more respect. The existing idiom conveys the aggression and the issue of manners.
23|It's quite all right. There's something I'd like to discuss with you.|It's quite all right.;discuss with you.|Diogo dismisses the interruption and asks for a discussion, returning control of the meeting to himself.
26|||Hodram briefly registers that Diogo wants him specifically. The echo keeps the turn short.
30|||Diogo asks if Hodram knows the named man. Keep Vasquez de Maldonado's approved full form.
33|||Hodram confirms he knows of Maldonado. The brevity leaves Diogo to explain.
37|||Diogo says Maldonado has caused their side a great deal of trouble. This sets up Hodram's question about nationality.
40|||Hodram points out that both men are Spanish. The question exposes why the request is unusual.
43|||Diogo separates Maldonado's nominal post as acting governor of Cuba from his alleged operation as head of the Caribbean pirates.
46|||Diogo accuses Maldonado of having pirates attack merchant ships on the Spain to New World route and secretly taking a share. Keep the accusation attributed to him.
49|||Diogo calls Maldonado a hyena and claims Spanish rule will collapse unless action comes soon. The unfinished condition carries into the English threat.
52|||Diogo fears the English could take the Caribbean and the entire New World, shaking Spain's power. The threat remains his prediction.
55|That's why I'm asking you to join us against that traitor. What do you say?|join us against that traitor.;What do you say?|Diogo makes his request to join forces a consequence of that argument. The direct question invites Hodram's decision.
59|||Hodram calls the alleged conduct high treason if true and points out that it should be Spain's responsibility. Keep his conditional skepticism.
63|||Diogo says Spain lacks decisive proof and cannot simply attack a fellow Spaniard. This explains why he seeks an ally.
66|||Diogo offers support if the crew drives Maldonado out in Spain's place. Keep that condition in his promise.
70|||Hodram tests the offer by asking whether it still holds if his own fleet ends up controlling the Caribbean.
73|||Diogo says he would prefer friendly control to indiscriminate raids on merchant traffic. The contrast gives his apparent concession its practical logic.
76|||Hodram concludes Diogo would rather deal with him than England because he seems easier to handle. The sardonic reply keeps the suspicion his own.
80|I'd prefer you didn't read it that way.|didn't read it that way.|Diogo politely objects to Hodram's suspicion before explaining why an English alliance is unthinkable.
83|||Diogo says Spain and England are openly at war, making an open alliance impossible. Keep both countries explicit.
87|We're Protestants too. Wouldn't your king gladly see us dead?|We're Protestants too.;gladly see us dead?|Hodram points out that his crew belongs to the religious group the Spanish king despises as well. The question presses Diogo on the inconsistency.
90|Let Europe fight its own religious wars. I've no wish to bring that senseless conflict to the New World. But England is another matter!|religious wars.;the New World.;England is another matter!|Diogo rejects bringing religious wars to the New World while making a separate exception for England. The rising anger sets up his next speech.
93|||Diogo calls the English Spain's sworn enemies and recoils at the idea of their flag over those waters. The hostility remains his.
96|||Hodram does not answer the outburst immediately. Keep this independent silent response.
100|||Diogo says the deal benefits the crew because pursuing the Caribbean will eventually bring them up against Maldonado anyway.
103|He came up through piracy and he's a formidable admiral. He still commands a powerful fleet. You'd have a hard time facing him alone.|a formidable admiral.;commands a powerful fleet.;facing him alone.|Diogo describes Maldonado's background, current command and strength. He warns of difficulty without guaranteeing defeat.
SC1_B140_CHOICE_2334_0|||The direct answer accepts the reasoning and bypasses the request for advice. Preserve its original terse form.
SC1_B140_CHOICE_2334_1|||The second choice asks for Gerhard's view. The short menu wording and native slot remain distinct from accepting at once.
118|||Hodram recognizes the presented reasoning and begins to consider the chance to build strength. Keep the thought open before the paths converge.
123|||Gerhard privately argues that the division among Spanish holdings helps them build power, but taking on both sides would be a mistake. Parentheses preserve the private aside.
126|||Hodram considers Gerhard's recommendation in a short beat. The agreement comes in the following turn.
133|||Hodram accepts the proposal after considering it. The existing language suits his guarded assent.
136|I'm glad you see reason.|see reason.|Diogo expresses relief that Hodram agreed in a slightly condescending turn. The sentiment closes the negotiation.
""",
}
review = checked_text(previous.review, {"len(records) == 77": "len(records) == 74"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::apology-map-and-Diogo", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

