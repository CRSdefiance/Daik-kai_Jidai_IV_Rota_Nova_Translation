"""Review Julian's tavern advice and the two sides of the Guiding Staff dispute."""

from scripts import pair_hodram_B131_B150_20261122 as paired
from scripts import review_hodram_B111_B114_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = previous.base, paired.ROOT
OUTPUT = ROOT / "B131_B132_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    131: "Julian recommends getting to know the women who work at taverns because they hear valuable information. Hodram takes the lesson seriously enough to question it, then teases Julian about his own flirting.",
    132: "Gerhard considers whether a rumored staff might improve the fleet's reputation. Charles challenges the need for it. Hodram can agree with Charles and gain Spirit, or agree with Gerhard and hear the limited clue about the staff near India. Both paths preserve the reconciliation.",
}
DECISIONS = {
    131: """
5|Admiral, you've sailed all over the world. You must know women at taverns in all sorts of ports, right?|all sorts of ports, right?|Julian starts from Hodram's travels and assumes he is on friendly terms with women who work at taverns. The conversational tag fits Julian's opening.
9|Where did that come from? We don't sail around the world to make friends at taverns.|Where did that come from?;make friends at taverns.|Hodram treats the topic as unexpected and denies that befriending the tavern women is the reason for their travels.
13|Come on, Admiral. The women at those taverns hear all sorts of things an adventurer needs to know.|women at those taverns;needs to know.|Julian insists the women know information useful to adventurers. Keep his playful protest ahead of his examples.
17|||The three examples remain treasure rumors, enemy fleets and unusual ruins known only to locals. The list makes Julian's real point.
20|What kind of adventurer would you be if you didn't make friends with women in ports all over the world?|What kind of adventurer;all over the world?|Julian exaggerates that getting to know tavern women is essential to adventure. The rhetorical question sets up Hodram's dry skepticism.
24|I suppose we are adventurers. But would they really tell us something that important so easily?|we are adventurers.;so easily?|Hodram accepts the description in passing but doubts that important information is so readily offered.
27|||Julian says ordinary customers blend together. The number of people the women talk to gives his next advice a reason.
30|Nothing does the trick like a gift she'll love.|a gift she'll love.|Julian recommends winning the woman's goodwill with a gift. The colloquial wording leaves the objective open between his practical advice and his flirtation.
33|They all like different things. Find out what she likes, then pick a gift she'll want.|They all like different things.;pick a gift she'll want.|Julian says preferences differ and tells Hodram to find out what a particular woman would like before offering a present.
41|||The example keeps Sakura in Osaka, the Snow-Silk Robe and the uncertain shop somewhere in the North Sea.
50|||Even someone who asks for very little will be pleased by a gift they want. The existing line fits Julian's persuasion.
54|So when you were flirting with every woman in every tavern, you were just doing your duty as an adventurer?|flirting with every woman;your duty as an adventurer?|Hodram sarcastically asks whether Julian's indiscriminate flirting was a professional obligation. Keep it as his teasing question.
57|||Julian's sudden stammer is the joke. The one short reply preserves his attempt to sound sure.
61|...I'll let you stick with that story.|stick with that story.|Hodram dryly lets Julian keep his excuse. The pause and phrasing make the joke explicit without accusing him of a new action.
65|||Julian returns the tease by saying the admiral could charm women if he made more effort. The closing line stays in Julian's voice.
""",
    132: """
5|||Hodram's silence puts him deep in thought before Gerhard calls.
9|Admiral.|Admiral.|Gerhard addresses Hodram by the title stated in the source. His brief call interrupts the silence without making him brusque.
13|||Hodram recognizes Gerhard after a pause. The short identification suits the distraction.
17|||Gerhard explains that he called several times without being heard. The trailing thought leaves Hodram to answer.
20|You did? Sorry, Gerhard.|Sorry, Gerhard.|Hodram realizes he missed Gerhard's calls and apologizes in his usual direct manner.
24|||Gerhard politely waves off the apology. The brief response suits both his manner and the transition to the report.
28|||Hodram asks whether something has happened. The plain question gives Gerhard room to bring up the lead.
32|A report caught my attention. I thought you should hear about it.|caught my attention.;hear about it.|Gerhard says he brought the report because it caught his interest. His second thought restores his purpose in coming over.
35|It caught your attention? That's unusual for you, Gerhard.|caught your attention?;unusual for you, Gerhard.|Hodram expresses surprise that Gerhard singled out this report. The mild tease remains familiar.
38|||Gerhard names the Guiding Staff as the subject of the report. Preserve the item title.
41|||Hodram echoes the title, giving Gerhard the next turn to explain it.
45|Legend says it guides people toward doing good.|guides people;doing good.|Gerhard reports the legend about being guided toward virtue. The revised line states the moral sense in ordinary spoken English.
49|Hm... But how could a staff show someone the right thing to do?|how could a staff;the right thing to do?|Hodram wonders how a staff could guide a person's conduct. His skepticism sets up Gerhard's practical argument.
53|Even if the legend isn't true, people believe it. If we had the staff, it would show the world that what we're doing is right.|people believe it.;show the world;what we're doing is right.|Gerhard distinguishes belief in the legend from the object proving anything itself. Its public reputation is what he thinks would help them.
56|||Hodram considers the argument and identifies at least one possible benefit, the crew's morale. Keep his answer qualified.
60|||Charles interrupts before they have reached a decision. The brief objection fits his entry.
64|||Gerhard identifies Charles in the form of a question. The short response preserves his surprise.
68|Since when do we need something unscientific to prove we're doing the right thing?|something unscientific;doing the right thing?|Charles objects to depending on something unscientific to justify their actions. His impatience contrasts with Gerhard's practical tone.
72|||Gerhard asks whether Charles was listening. The question gives Charles room to distinguish overhearing from intentionally listening in.
76|||Charles says he happened to overhear and asks for an answer. His direct insistence preserves the tension.
80|||Gerhard says being a military fleet already causes suspicion and friction. He suggests the staff might spare them misunderstandings. Keep that outcome tentative.
83|||Charles says the crew should follow the course it believes is right regardless of other people's judgment. The nautical phrasing fits both the point and his setting.
86|||Charles asks whether everyone else's agreement is necessary for Gerhard's satisfaction. The existing challenge sounds sharper than the earlier question.
90|||Gerhard asks what has gotten Charles so worked up. His concern shifts the exchange away from the abstract argument.
93|||Gerhard states his limited purpose and defers to Hodram. The existing formal phrasing fits his effort to steady the discussion.
96|||Charles appeals directly to the admiral through a familiar question tag. Keep the challenge and protect the short tag together during display review.
SC1_B132_CHOICE_1532_0|||The first caption agrees with Charles that the staff is unnecessary. The short answer fits the menu and preserves its branch.
SC1_B132_CHOICE_1532_1|||The second caption overrides Charles's appeal and agrees that the staff is needed. Keep its separate response branch.
110|||On this branch, Hodram concludes they have no need for the staff so long as they follow the course they believe is right.
114|||Charles quickly agrees after Hodram picks his side. The compact response suits his relief.
118|Sorry, Gerhard. You went to the trouble of bringing me that report.|Sorry, Gerhard.;bringing me that report.|Hodram acknowledges the work Gerhard put into the suggestion before setting it aside.
122|||Gerhard reassures Hodram and repeats that this was only one suggestion. His formal response fits his earlier deference.
126|Besides, I got to see again how much Charles cares about this fleet.|how much Charles cares;about this fleet.|Gerhard says the exchange reminded him of Charles's sincere feeling for the fleet. The compliment makes room for Charles's apology.
130|||Charles hesitates and admits he went too far. Preserve the moment in which his earlier urgency softens.
133|It's all right. Don't lose that honesty.|It's all right.;Don't lose that honesty.|Gerhard encourages Charles to keep his direct, sincere attitude even after an argument. His reassurance closes their dispute.
137|||Gerhard excuses them and asks Charles to come with him. Keep the change of audience in his two parts.
140|||Charles quietly agrees to go with Gerhard. The simple acknowledgment comes after the reconciliation.
145|||The speakerless notice raises the runtime-selected captain's Spirit by one. Preserve FI, the stat label and the amount.
151|||On the other branch Hodram says Gerhard is right. The short decision is a direct answer to Charles's appeal.
155|Admiral!|Admiral!|Charles uses the admiral's title in his startled objection, the same title he used when asking for support.
159|||Hodram recognizes Charles's point and explains that they represent their country because they are a royal navy. Keep that distinction from a private fleet.
163|||Hodram links the crew's reputation to the country's standing and argues that it needs recognition to extend its reach abroad. The reasoning remains political, not supernatural.
166|||Charles falls silent to consider Hodram's argument. Preserve his separate reaction.
170|Do you see what I mean, Charles?|what I mean, Charles?|Hodram checks that Charles understands his point. The full address stays with the question.
174|||Charles agrees that Hodram is right and apologizes. Keep his pause as he concedes.
178|||Charles then apologizes directly to Gerhard. The separate addressee matters after he has just spoken to Hodram.
182|Don't worry about it. People are bound to see a proposal like that differently.|Don't worry about it.;see a proposal|Gerhard accepts the apology and says differing views are ordinary for any proposal. His reassurance keeps the conversation from turning into a rebuke.
186|I'm glad you see it that way. Thank you.|see it that way.;Thank you.|Charles is relieved that Gerhard understands. The gratitude suits his shift from an argument to agreement.
189|||Gerhard asks whether the admiral wants to leave to search now. The question leads directly to the location clue.
192|||Hodram asks whether they know where it is. The short reply makes his requirement clear.
196|||Gerhard thinks it is somewhere around India. Preserve the vague geography and the qualification.
200|||Hodram commends the amount Gerhard has already learned. His comment prompts the provenance of the lead.
204|||Gerhard names the finder only as an Italian explorer. The line introduces the previous discovery without inventing a name.
207|Then how are we supposed to get our hands on it?|get our hands on it?|Hodram assumes the explorer already has the staff, so he questions how the fleet could obtain it.
210|||Gerhard explains that the explorer was apparently attacked by enemy soldiers while transporting it and lost the staff. Keep the report qualified.
214|||Hodram connects the place of the attack to the earlier clue about India. His reply remains a question.
218|||Gerhard confirms the connection in one beat.
222|||Hodram checks that Gerhard has no more precise location. The existing short question leaves room for the apology.
225|||Gerhard apologizes for the limits of the report. The polite wording suits him here.
229|||Hodram leaves the search for a time when they are closer. The vague clue remains insufficient for an immediate search.
233|||Gerhard acknowledges the admiral's decision. This assent stays separate from Charles's.
237|||Charles gives his own acknowledgment, closing the exchange after the reconciliation.
""",
}
review = checked_text(previous.review, {"len(records) == 51": "len(records) == 77"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::tavern-advice-and-guiding-staff", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

