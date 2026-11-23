"""Review the Christian ruins, the blocked path, and the Market requests."""

from scripts import review_hodram_B292_B293_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = previous.base, previous.ROOT
OUTPUT = ROOT / "B294_B299_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    294: "The crew needs a map to reach the hidden ruins. On the route they discuss the community that might have lived here, then find human remains. The decision to investigate can bring harmful smoke and leave Hodram struggling to speak. The other response keeps the party moving.",
    295: "The hostess flirts with Hodram and shares an unconfirmed story about a Christian village near town.",
    296: "A rockfall appears to block the way. Gerhard and Hodram prepare to turn back, but Charles suggests reclaiming the route and sends the crew to buy cargo at the Market.",
    297: "Hodram checks for Charles and remembers the first Market request. Charles distinguishes three inventory outcomes, then explains what cargo they need next. Gerhard says the town does not sell it.",
    298: "Hodram repeats the reminder about timber. Charles checks how much they brought, then asks for the final commodity. Gerhard gives an Indian Ocean lead, and Hodram reacts to the distance.",
    299: "The final Market request resolves once enough cargo is brought. Charles finishes his work, directs the party to shelter in town, then gives the countdown.",
}
DECISIONS = {
    294: """
SC1_B294_STYLE_28_0|Admiral, we can't go any farther without a map.|go any farther;without a map.|The speaker gives a polite warning that the party cannot continue without a map.
SC1_B294_STYLE_28_40|Admiral, we need a map to proceed.|a map to proceed.|This measured crew member states the requirement plainly. Proceed keeps a slightly formal voice.
SC1_B294_STYLE_28_78|||The casual crew member says they need a map to get farther. The phrasing sounds like conversation.
SC1_B294_STYLE_28_112|||This speaker stresses that going on is impossible without a map. The direct delivery sets her apart.
SC1_B294_STYLE_28_146|||The rougher crew member calls for a halt and explains the map requirement without a formal address.
SC1_B294_STYLE_28_184|||The older voice delivers the same requirement as a firm decision.
SC1_B294_STYLE_28_216|||The youthful voice calls directly to the admiral and makes a short, emphatic request for a map.
SC1_B294_STYLE_28_244|Admiral, we can't continue past this point without a map.|past this point;without a map.|The measured voice explicitly marks this as the point beyond which the party needs a map.
43|||Hodram takes in how thick the forest is. The short observation sets up Gerhard's explanation.
47|||Gerhard draws a link between the dense forest and the place staying hidden. No wonder makes that inference sound natural.
58|I can't wait to get out of these woods.|get out of these woods.|Charles wants to get through the forest as soon as possible. The contraction suits his impatience.
64|||Gerhard wonders whether the Christians who lived here before Islamic rule descended from the Byzantines. Keep both the chronology and the uncertainty.
67|Centuries ago, then. I hope we find some clue to a Proof.|Centuries ago, then.;some clue to a Proof.|Hodram considers the age of the settlement and hopes for a lead to one of the Proofs of Conquest.
71|||Hodram reacts with genuine surprise on seeing human bones.
75|They must've come in the same way we did and died here...|the same way we did;and died here...|Gerhard infers that people entered as the party did and died in this place. Keep his inference and trailing unease.
78|||Gerhard cautiously suggests searching around the bones. The brief question fits the decision.
SC1_B294_CHOICE_820_0|||Yes accepts Gerhard's suggestion to search the area.
SC1_B294_CHOICE_820_1|||No declines the suggestion and continues the route.
93|||Gerhard accepts the decision and says the precaution is warranted. The short idiom fits the moment.
96|||Hodram notices smoke, then chokes and struggles to speak. The ellipses express that interruption.
99|That smoke...! FI, don't breathe it in! We need to get out of here, now!|don't breathe it in!;get out of here, now!|Gerhard recognizes the hazard and keeps Hodram's given-name token in his urgent warning.
103|||Gerhard checks that everyone has reached him. The terse question suits a head count.
107|||The sailor says everyone made it out safely before Gerhard notices how the admiral is doing.
111|Good. Oh, FI! Are you all right?|Are you all right?|Gerhard acknowledges the report, then suddenly notices Hodram's condition. Keep the given-name token exactly.
115|Y-yeah... I'm all right... What was that back there?|I'm all right...;What was that back there?|Hodram stammers through reassurance and asks what they just encountered. Keep the strain in his voice.
118|The smoke can hurt you if you breathe it in. I'd heard rumors, but I never thought I'd come across it here...|if you breathe it in.;I'd heard rumors,;come across it here...|Gerhard describes the smoke as harmful and says he knew it only by report. Trailing off leaves room for Hodram's weakening answer.
122|||The admiral manages only a few words. The original faltering delivery sets up Gerhard's alarm.
126|The admiral's in trouble! Come on, everyone! We need to get through, now!|The admiral's in trouble!;Come on, everyone!;get through, now!|Gerhard recognizes the danger to Hodram and urgently calls on everyone to pass through.
135|||The speakerless notice says the sailors appear confused. It gives no additional effect.
143|Hmm... No sense lingering in a place like this. Let's press on.|No sense lingering;in a place like this.;Let's press on.|Gerhard takes the unsettling surroundings as a good reason to move on promptly.
155|That's a shame... We might've found out what happened to those people.|That's a shame...;what happened to those people.|Charles regrets missing the chance to learn the story behind the remains.
167|||Hodram thinks they have reached the right place. The wording leaves the identification tentative.
""",
    295: """
6|||The hostess sounds pleasantly surprised as she welcomes Hodram.
10|||The hostess flirts after looking more closely and offers a tip. The compliment feels playful in context.
14|||She asks whether Hodram has heard about a nearby hidden Christian village. The community's identity stays explicit.
17|||Hodram plainly says he has not heard of it, leaving her to explain.
21|They say the people there live in houses carved right into the rock. Just a rumor, though.|the people there live;carved right into the rock.;Just a rumor, though.|She describes the unusual rock dwellings and signals that the story is unconfirmed.
""",
    296: """
5|||Hodram trails off when he sees what is blocking the way. The fragment belongs to that reaction.
9|There must've been a rockfall. There's no getting through this.|been a rockfall.;no getting through this.|Gerhard guesses that rocks fell and judges that the group cannot pass. The inference leaves the cause tentative.
12|||Hodram accepts they will likely have to turn back. The resignation fits the situation.
33|||Charles pauses to think while everyone prepares to leave. The pause makes his next suggestion sudden.
37|||Gerhard asks why Charles has stopped and tells him the group is returning.
40|||Charles makes a sudden, enthusiastic suggestion to blast the obstruction. Keep it as a short exclamation.
44|||Gerhard reacts with surprise and echoes Charles's suggestion as a question.
47|||Charles confirms that he means the rocks blocking the route. Straightforward confidence contrasts with Gerhard's doubt.
50|||Hodram challenges the idea and explains why he thinks it will be impractical.
54|||Gerhard says obtaining that much all at once is practically impossible. This is an assumption about supply.
57|Don't worry. We'll make what we need ourselves.|We'll make what we need ourselves.|Charles reassures them by suggesting the party can supply what it needs by doing the work themselves.
60|||Hodram asks if Charles can really do it. The short question sounds surprised after the confident offer.
63|Admiral... Have you forgotten what I've been studying? Bring me plenty of sulfur and I can make it anytime.|what I've been studying?;plenty of sulfur;I can make it anytime.|Charles reminds the admiral of his research and asks for the named in-game cargo. Give no production details beyond his line.
67|||Gerhard remembers the item is sold locally but speaks with modest uncertainty.
70|That's right. Buy it at the Market and bring it here.|Buy it at the Market;and bring it here.|Charles confirms the original shop label and says to transport the purchase back here.
73|All right. Let's go buy some sulfur.|Let's go buy some sulfur.|Hodram accepts the next step and repeats the cargo he will buy.
""",
    297: """
11|||Hodram regrets that Charles is unavailable. Keep the conditional response consistent with the later cargo steps.
33|||Hodram reminds himself of the current purchase. The commodity name matches the Market label.
213|||Charles says the amount is nowhere near sufficient. The emphatic voice distinguishes the result from a near miss.
232|We still need more.|We still need more.|Charles reports that the amount is still short. The restrained line contrasts with the lowest inventory case.
243|||Charles says the amount should be enough. His qualified approval closes the inventory check.
247|||Gerhard asks what happens next, picking up immediately after Charles's approval.
251|Next we'll need timber to make charcoal.|timber to make charcoal.|Charles identifies the next named cargo and why the party needs it. Keep the game commodity distinct from its use.
254|||Hodram echoes the new commodity in surprise. The short question cues Gerhard's next explanation.
258|||Gerhard explains that timber is unavailable in this town and must be bought somewhere else.
""",
    298: """
11|||Hodram regrets that Charles is unavailable, matching the corresponding response for the other steps.
33|||Hodram recalls that timber is the current purchase. Keep the established item spelling.
128|||The inventory is far below what Charles needs. Match his emphatic response for the same outcome.
147|We still need more.|We still need more.|Charles gives the matching understated response when the amount is short.
158|||Charles approves the amount with the same qualification as on the previous step.
161|||Charles starts his final request and lets it hang long enough for Hodram to interrupt.
165|||Hodram is surprised that there is another request. The short interruption suits the comic timing.
169|We're still missing the one thing we can't do without. Saltpeter.|the one thing;we can't do without.;Saltpeter.|Charles explains that the essential commodity is still missing and names it after the setup.
172|||Hodram repeats the unfamiliar shopping term. The brief echo makes room for Gerhard's lead.
176|One of the ports on the Indian Ocean should sell it.|on the Indian Ocean;should sell it.|Gerhard gives the region where the crew should look without naming a specific port or guaranteeing stock.
179|||Hodram reacts to how far the party will have to go. The unfinished cadence lets the objection linger.
""",
    299: """
11|||Hodram's line again indicates that the party needs Charles here. Keep the same conditional response.
33|||Hodram remembers the final purchase and uses the exact Market term.
229|||Charles again says there is nowhere near enough. Retain the strongest rejection for the lowest inventory case.
247|We still need more.|We still need more.|Charles gives the same short assessment for the intermediate inventory outcome.
258|Yes, this should be enough.|this should be enough.|Charles approves the amount with the same phrasing as in the earlier checks. Regular wrapping can handle this full sentence.
265|||Charles briefly announces that he has finished. The exclamation fits his energy.
269|||Charles says he will set the charge and asks the party to take shelter back in town. The exchange gives only the in-game action and destination.
278|||Charles starts the countdown at three, ending at zero. Preserve the exact beats and timing of the exclamation.
""",
}

review = checked_text(previous.review, {"len(records) == 18": "len(records) == 81"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::christian-ruins-and-market", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
