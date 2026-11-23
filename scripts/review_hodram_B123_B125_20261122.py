"""Review Maria's Sao Jorge confrontation, Benazir's lead, and the figurehead."""

from scripts import review_hodram_B120_B122_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B123_B125_contextual_v1.json"
GLYPHS = {"DK4_MES_B123_R0127", "DK4_MES_B123_R0142"}
CONTEXTS = {
    123: "A stone tablet looks out of place near the mud mosque. Maria and Xien confront the attackers of Sao Jorge. Maria hears their grievance, challenges their reprisals, and invites the leader to sail with them. He tells her about the object hidden in the ruins.",
    124: "Benazir offers a clue in return for a gift. She recommends a building in India and tells Hodram a map is needed to find it.",
    125: "The crew notices a statue that looks out of place. Different crew voices speculate about a figurehead, with one suggesting its use and another arriving at a firm conclusion.",
}
DECISIONS = {
    123: """
SC1_B123_STYLE_16_0|Admiral, please look at this!|please look at this!|This source call is the polite version. Please restores that distinction from the more direct second body.
SC1_B123_STYLE_16_28|||The second body gets the admiral's attention with a plain, direct request.
SC1_B123_STYLE_16_48|||Take a look fits the more familiar source and speaks to the admiral directly.
SC1_B123_STYLE_16_74|Admiral, you'd best look at this!|you'd best look at this!|This older, more forceful voice insists the admiral look. Its register differs from both the polite and casual calls.
SC1_B123_STYLE_16_100|Admiral! Look at this!|Look at this!|The short initial call reflects the stretched attention-getter and makes the youthful voice distinct.
29|||Hodram identifies the unexpected object. His simple response lets Gerhard question its significance.
33|||Gerhard asks what is wrong rather than taking the stone tablet's importance for granted.
37|There's no stone around here. They even built the mosque out of mud. What's a stone tablet doing here?|built the mosque out of mud.;a stone tablet|Hodram points to the lack of local stone and the mosque's mud construction. His rhetorical question conveys why a tablet seems out of place.
41|||Gerhard draws the conclusion that the tablet came from somewhere else. He keeps the flash of recognition.
51|||The speakerless caption introduces people whispering before they are recognized. Its soft repetition suits the cue.
55|||Maria reacts briefly as the conversation shifts. Preserve the separated silent question.
59|We've got a problem. With things like this, there's no way we can make a move...|We've got a problem.;make a move...|The bandit says the situation keeps them from acting. The nearby exchange explains the defenses, so the line can stay unspecific.
62|||Maria asks whether these are the people attacking Sao Jorge. She has yet to hear an admission.
65|W-what?! Who the hell are you?|Who the hell are you?|The bandit startles and answers with a coarse demand. His stammer and register contrast with Maria's direct question.
68|||Maria gives her faction affiliation by the original company-name substitution.
72|What?! You're the ones helping guard the town! You've made our lives hell!|helping guard the town!;made our lives hell!|The bandit recognizes the crew's role and angrily complains about the consequences to his group.
76|Thanks to you, we can't raid the town! How are we supposed to eat?!|can't raid the town!;supposed to eat?!|The bandit complains that the defenses have cut off his band's living. His question uses the source's food image without implying literal starvation as a fact.
79|That's rich, coming from bandits! We won't leave those people to fend for themselves!|coming from bandits!;fend for themselves!|Xien rejects the bandit's indignation. He makes defending the townspeople the reason for the crew's involvement.
83|||The bandit angrily blames the Europeans for what happened to his village. Keep the accusation in his voice.
86|||He vows revenge regardless of what the crew says. The concise declaration conveys his determination.
89|Wait. Blame the crooked merchants who trade in slaves here in Africa and the ruthless soldiers who plunder it.|crooked merchants;trade in slaves;ruthless soldiers|Maria names the slave traders and plundering soldiers as the people responsible. Her correction preserves the specific wrongdoing and its location.
92|If you hate every European and attack people at random, you're no better than the people who wronged you. You're guilty of the same thing.|attack people at random,;people who wronged you.;guilty of the same thing.|Maria distinguishes the specific perpetrators from indiscriminate targets and says the bandits would be equally guilty.
95|||The bandit rejects her argument as self-assured talk from an outsider. His short retort keeps his anger alive.
99|Give up on revenge. What good will it do? It can't give you back the life you had.|Give up on revenge.;What good will it do?;the life you had.|Maria says revenge will accomplish nothing and cannot restore the happiness the villagers have lost.
103|All it will do is start the fighting over again, and more of your people will suffer.|the fighting over again,;your people will suffer.|She explains that reprisals will renew the fighting and bring suffering to still more of his group.
107|||The bandit asks what else they can do. His stammer is the first sign that he is listening.
110|||Maria links conflict at sea to the rivalry among European powers and says that rivalry has to end.
114|||The bandit's separate startled punctuation gives room for the scope of her proposal.
118|||The great powers are trying to divide the world. Maria explains that her crew collects the Proofs to stop them from using those objects as a pretext.
121|||The bandit asks if she is serious about stopping the great powers. The broken question preserves his disbelief.
124|I wouldn't bluff about this. We've extended our reach all the way to Africa. I'm confident we can match them, maybe even beat them.|I wouldn't bluff about this.;all the way to Africa.;maybe even beat them.|Maria points to her crew's reach as proof of their ability to confront those powers at least as equals.
127|...||The bandit falls silent as Maria's answer sinks in. Restore the ordinary English dots for the same pause.
131|What do you say? Will you trust us with your revenge?|What do you say?;with your revenge?|Maria reframes his desire for vengeance as something he can entrust to their cause. Her original provocation earns his next question.
134|||The bandit is startled by the unexpected offer. Keep the terse reaction before Maria explains it.
138|Come sail with us. With that kind of resolve, I know you can do it.|Come sail with us.;kind of resolve,;I know you can do it.|Maria invites him to sea and expresses confidence in what he can do with the resolve he has already shown.
142|...||He takes another beat to weigh her invitation. Use the ordinary dots here just as in his earlier speechless response.
146|||The bandit realizes staying in place will change nothing. The pause makes the decision his own.
149|||He decides to stake his future on Maria's offer. The idiom and direct address fit his acceptance.
153|||Maria welcomes him. The brief answer follows his decision without adding a promise or a new relationship.
160|||The new ally tells Maria the object was hidden in the ruins. Keep his uncertainty about whether it relates to the Proof.
163|||Maria recognizes the shape of a stone tablet in a short question. The exchange leaves its significance open.
""",
    124: """
6|||Benazir calls after the departing crew. The brief opening draws their attention.
10|||The runtime-selected wordless question leaves room for Benazir to explain why she called.
14|I can't just take your gift and give you nothing in return. Let me tell you something useful.|nothing in return.;something useful.|Benazir reciprocates the gift with information. Her explanation sounds personal without implying a further relationship.
18|||She recommends a magnificent building in India and says it is worth visiting after coming so far. The site remains unnamed here.
22|The catch is, you'll need a map to find it. I hope you get to see it.|need a map to find it.;get to see it.|Benazir explains the practical barrier and warmly encourages the trip. She does not provide the map herself in this line.
25|||Hodram acknowledges the lead and says he will go if he has a chance. Preserve the qualifier.
""",
    125: """
6|||The crew member starts to point out the statue before saying what seems wrong with it. Preserve the dynamic voice and unfinished address.
10|||Hodram's brief response lets the crewmate explain the observation.
SC1_B125_STYLE_54_0|||This attentive voice singles out the statue's design as the part that seems out of place.
SC1_B125_STYLE_54_46|||The measured source variant mentions the design and says it does not suit the building. Keep the formal wording.
SC1_B125_STYLE_54_92|||The crew member asks whether the other person shares the impression that it is out of place. Keep the colloquial question.
SC1_B125_STYLE_54_132|||The casual observation that it does not go with the building fits this register.
SC1_B125_STYLE_54_170|||The more blunt voice asks whether the statue simply looks wrong for the building. Retain that directness.
SC1_B125_STYLE_54_214|||The thoughtful voice expresses a tentative feeling that the statue does not belong. Its qualification belongs to this slot.
SC1_B125_STYLE_54_268|||The casual question tag asks for agreement. Keep its friendly phrasing and check that the tag stays together onscreen.
SC1_B125_STYLE_54_300|||This more courteous voice asks for confirmation and makes the design explicit. Keep the separate body.
32|||Hodram considers the observation after it is pointed out. The unfinished sentence sets up the crew's explanation.
SC1_B125_STYLE_450_0|||The speaker first identifies the shape and then tentatively asks if it originally was a figurehead.
SC1_B125_STYLE_450_52|||The speaker changes from noticing the resemblance to considering its original purpose. The short Wait carries that change.
SC1_B125_STYLE_450_106|||Two questions convey the hesitant path from resemblance to identification. Keep the casual I mean.
SC1_B125_STYLE_450_182|||The surprised reconsideration gives this voice a distinct second beat. Its conclusion remains a question.
SC1_B125_STYLE_450_238|||The clipped speech and hesitation fit this less formal variant. It still treats identification as uncertain.
SC1_B125_STYLE_450_304|It has the shape of a figurehead. Wait, it was a figurehead all along.|the shape of a figurehead.;all along.|This voice shifts from resemblance to certainty. The language preserves the firm conclusion without making the crewmate's age a story fact.
SC1_B125_STYLE_450_366|||This voice sees a way to use the statue as a figurehead. Keep the demonstration and the distinct lack of a claim about its past.
SC1_B125_STYLE_450_394|||The more formal final voice wonders whether it originally served as a figurehead. Preserve that tentative distinction.
53|||Hodram's brief acknowledgment follows the identification or suggestion in each native variant.
""",
}
review = checked_text(previous.review, {"len(records) == 51": "len(records) == 67"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::Sao-Jorge-and-ruins", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

