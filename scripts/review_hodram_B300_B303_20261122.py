"""Review the snake, bog rescue, Colosseum clue, desert crossing, and Safia's tip."""

from scripts import review_hodram_B294_B299_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = previous.base, previous.ROOT
OUTPUT = ROOT / "B300_B303_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    300: "Before entering the bog, the crew warns Hodram about getting lost without a map. They meet a giant snake. Fighting and retreating have different consequences. On the retreat, Hodram gets stuck, and Gerhard may free him alone or need the sailors' help.",
    301: "The hostess tells the captain about the Colosseum and advises buying a map before setting out.",
    302: "The crew crosses a desert, notes the heat, and asks Hodram how to respond to a sandstorm. Two separate menus distinguish moving immediately from waiting and pushing through later. Fatigue, lost sailors and the passage of a day belong to specific choices.",
    303: "Safia thanks Hodram for helping her improve her dancing and shares the legend of a king honored at a mosque far inland.",
}
DECISIONS = {
    300: """
SC1_B300_STYLE_24_0|||The crew member addresses the admiral, politely warning that they will lose their way without a map.
SC1_B300_STYLE_24_34|Admiral, we'll lose our way if we go without a map.|we'll lose our way;without a map.|The measured voice gives the same warning in a plain statement suited to this crew member.
SC1_B300_STYLE_24_66|||This casual voice objects to continuing without a map. The contraction keeps the warning conversational.
SC1_B300_STYLE_24_98|||This crew member warns the admiral they'll get lost. The emphasis fits her concern.
SC1_B300_STYLE_24_134|||The rougher speaker draws out the warning in his own informal register.
SC1_B300_STYLE_24_170|||The older voice explains that they need the map to avoid getting lost. The direct warning suits him.
SC1_B300_STYLE_24_208|||The youthful crew member appeals to the admiral and says the party needs a map to continue.
SC1_B300_STYLE_24_242|||The formal speaker stresses that going without a map is sure to get them lost.
40|||Hodram has heard even the locals keep away. Preserve the qualified claim and the unresolved pause.
43|Something may be waiting for us out here. Let's be careful as we go.|may be waiting for us;Let's be careful|Gerhard suspects the place holds something and advises the group to proceed with great care.
46|||The sailor stammers the admiral's title on seeing the threat. The brief exclamation comes before identification.
50|A giant snake!|A giant snake!|Hodram abruptly recognizes the creature without adding a name or other detail.
54|What are your orders? That thing won't be easy to deal with.|What are your orders?;won't be easy to deal with.|Gerhard asks for a decision and anticipates that overcoming the snake will take effort.
SC1_B300_CHOICE_560_0|||Fight accepts the confrontation and leads to Hodram's engagement order.
SC1_B300_CHOICE_560_1|||Run chooses to disengage. The caption is short and direct.
68|||Hodram makes the terse decision to fight. The formality suits an order.
72|||Gerhard acknowledges the order and directs the group to move together.
75|||The sailor acknowledges immediately in an ordinary, familiar voice.
94|||Hodram observes that the creature is down. The breath after it fits the moment.
98|||Gerhard quietly agrees after the encounter.
110|||Charles calls the creature a tough opponent and says he is glad they brought the supplies.
119|||The notice reports possible injuries to some sailors. Keep both the uncertainty and unspecific number.
124|It'd be a mistake to fight here.|a mistake to fight here.|Hodram rules out fighting in this spot and prepares to move the party away.
128|Understood. Everyone, fall back! Keep up!|Everyone, fall back!;Keep up!|Gerhard accepts the decision, orders a retreat and warns the crew to stay together.
132|||The sailor acknowledges the retreat order with the same concise nautical reply used later.
137|||Gerhard takes a head count after the party has moved away. The question is brief and immediate.
141|Everyone's here!|Everyone's here!|The sailor says the whole party is accounted for. Use a quick spoken answer to Gerhard's head count.
148|||Hodram makes a short involuntary sound on getting into trouble.
152|||Gerhard immediately asks what happened, addressing Hodram with the original given-name token.
155|I think I'm stuck in a bog...|stuck in a bog...|Hodram identifies the hazard while he is still trapped. His surprise gives way to an unfinished explanation.
159|||Gerhard's startled question responds to the unexpected bog.
170|||Gerhard says he is about to pull Hodram out. The brief promise lets the action follow.
174|Nngh! I can't pull you out by myself... Everyone, give me a hand!|pull you out by myself...;give me a hand!|Gerhard strains, realizes he needs help and calls to the others. Keep the effort before the call.
178|||The sailor answers the request for help immediately, as in the retreat.
182|||Gerhard catches his breath and asks whether Hodram is all right. Keep the given-name token.
186|Yeah... Gerhard, you saved me.|Gerhard, you saved me.|Hodram answers weakly and credits Gerhard with saving him. His familiarity suits the moment.
194|I'll pull you out! Nngh!|I'll pull you out!;Nngh!|On this rescue path Gerhard immediately lifts him. Use the same nonverbal exertion as in the assisted path.
197|Hah... hah... Are you all right, FI?|Are you all right, FI?|Gerhard is out of breath and checks on Hodram with the existing name substitution.
201|Yeah... Thanks. I never thought there'd be a bog here.|I never thought;be a bog here.|Hodram answers, thanks Gerhard, and reacts to finding the same bog he just escaped.
208|||The notice says the sailors appear tired. The same wording suits the recurring fatigue panel.
SC1_B300_STYLE_1610_0|||The crew member spots something ahead and trails off before naming it.
SC1_B300_STYLE_1610_18|||The measured voice gives a short urgent call to look ahead.
SC1_B300_STYLE_1610_36|||Both crew styles stammer as they point out something ahead. Retain the shared line.
SC1_B300_STYLE_1610_56|||The rough crew member gets the admiral's attention with two short exclamations.
SC1_B300_STYLE_1610_70|||The older voice calls the admiral's attention to the thing they see.
SC1_B300_STYLE_1610_86|||The youthful crew member calls out in sudden recognition.
SC1_B300_STYLE_1610_108|||The restrained speaker gives only an exclamation of surprise, without specifying the find.
""",
    301: """
6|||The hostess welcomes Hodram by the given-name token and says he arrived at the right time.
9|||She asks whether he knows of the Colosseum. Keep the conventional English name.
13|||Hodram echoes the name, leaving her to explain why it matters.
17|It's a ruin from Roman times. I heard you were looking for ruins, so I figured I'd tell you about it.|a ruin from Roman times.;looking for ruins,;I'd tell you about it.|The hostess identifies the period and explains that she heard about Hodram's search. Her casual voice suits the tip.
21|Thanks. I'll go take a look right away.|go take a look right away.|Hodram appreciates the tip and decides to visit promptly.
24|||The hostess wishes him a safe trip and specifically reminds him to buy a map first.
""",
    302: """
SC1_B302_STYLE_24_0|Admiral, we might lose our way without a map...|might lose our way;without a map...|The crew member warns that they could lose their way and leaves room for the admiral's reply.
SC1_B302_STYLE_24_40|||The measured voice tells the admiral he needs a map in this place. The short statement fits.
SC1_B302_STYLE_24_68|||The casual speaker says continuing without actually consulting a map is impractical.
SC1_B302_STYLE_24_108|||This crew member proposes getting the map first to avoid becoming lost.
SC1_B302_STYLE_24_162|||The rougher voice calls proceeding without a map asking for trouble. The warning sounds direct.
SC1_B302_STYLE_24_204|||The older crew member says the party will lose its way without a map.
SC1_B302_STYLE_24_242|Admiral, we're gonna get lost without a map!|we're gonna get lost;without a map!|The youthful speaker stresses the prospect of getting lost in a drawn-out informal voice.
SC1_B302_STYLE_24_284|||The formal speaker warns they are sure to lose their way unless they bring a map.
SC1_B302_STYLE_392_0|||The speaker comments plainly on the oppressive heat.
SC1_B302_STYLE_392_24|||The terse reaction conveys heat and exhaustion with one word.
SC1_B302_STYLE_392_32|||The exhalation comes before the casual complaint about the heat.
SC1_B302_STYLE_392_48|||This crew member emphasizes just how hot it is. The natural sentence suits her observation.
SC1_B302_STYLE_392_70|||The rougher crew member complains in a short colloquial exclamation.
SC1_B302_STYLE_392_84|||The older voice remarks on the heat with its own familiar cadence.
SC1_B302_STYLE_392_102|Whew... It's so hot!|It's so hot!|The youthful crew member exhales and complains in a simple, natural turn.
SC1_B302_STYLE_392_120|||The formal voice exclaims at the heat without losing its measured phrasing.
71|||Hodram tells the crew to ration their water because they still have a long way to travel.
SC1_B302_STYLE_596_0|This sandstorm is bad. We could get lost if we keep going. What should we do?|This sandstorm is bad.;if we keep going.;What should we do?|The speaker judges the storm severe, warns about losing the route and asks for an order.
SC1_B302_STYLE_596_62|A bad sandstorm... We could lose our way if we keep going. Your orders, Admiral?|A bad sandstorm...;if we keep going.;Your orders, Admiral?|The measured voice hesitates at the storm and then asks the admiral what to do.
SC1_B302_STYLE_596_132|||The casual voice bluntly predicts getting lost and asks what comes next.
SC1_B302_STYLE_596_202|||The crew member says the storm worsened and worries about getting lost. She asks the admiral what they should do.
SC1_B302_STYLE_596_284|This storm's gotten bad. We could lose our way... Still want to go on?|This storm's gotten bad.;We could lose our way...;Still want to go on?|The rougher voice describes worsening conditions and directly checks whether to continue.
SC1_B302_STYLE_596_342|It's really blowing now. We could lose our way if we go on. What do you think?|really blowing now.;if we go on.;What do you think?|The older speaker sees the storm growing worse and asks the admiral for a decision.
SC1_B302_STYLE_596_434|Wow, this sandstorm sure got bad... I think we'll get lost if we go on. What do we do?|sure got bad...;if we go on.;What do we do?|The youthful voice is awed by how the storm worsened and thinks they will lose their way.
SC1_B302_STYLE_596_524|Quite a sandstorm. We're liable to lose our way in there. Shall we go on anyway?|Quite a sandstorm.;lose our way in there.;go on anyway?|The formal speaker considers losing the route nearly inevitable and asks whether they should continue anyway.
SC1_B302_CHOICE_1226_0|||Keep going continues through the existing storm immediately.
SC1_B302_CHOICE_1226_1|||Wait it out stays put to see whether the storm ends.
108|I doubt this sandstorm will let up. We'll press on.|will let up.;We'll press on.|Hodram expects the storm to continue and orders the party onward.
SC1_B302_STYLE_1320_0|||The speaker accepts the decision and cautiously suggests going ahead.
SC1_B302_STYLE_1320_36|||The formal voice hesitates and defers to the admiral before agreeing to proceed.
SC1_B302_STYLE_1320_76|||This crew member pauses, accepts the order and goes along with it.
SC1_B302_STYLE_1320_108|||The speaker quietly acknowledges the decision before suggesting they continue.
SC1_B302_STYLE_1320_140|||The rough speaker accepts with a brisk response and turns to action.
SC1_B302_STYLE_1320_172|||The older voice says he understands the admiral's thinking and is willing to try.
SC1_B302_STYLE_1320_216|||The youthful voice doubts the choice and then goes along anyway.
SC1_B302_STYLE_1320_252|||The formal reply signals understanding and willingness to proceed.
137|||The panel reports tired sailors and that some appear to be missing. Keep both outcomes and the reported uncertainty.
141|We'd better wait here and let it pass.|wait here;let it pass.|Hodram decides to ride out the storm here and wait a little.
SC1_B302_STYLE_1786_0|||The crew member says there is no sign the storm will let up, then asks what they should do.
SC1_B302_STYLE_1786_62|The sandstorm doesn't seem to be letting up. What do you suggest, Admiral?|doesn't seem to be letting up.;What do you suggest, Admiral?|The measured voice reports the weather has not improved and asks the admiral how to proceed.
SC1_B302_STYLE_1786_120|||The casual speaker thinks more waiting may not help and asks what to do next.
SC1_B302_STYLE_1786_184|||This crew member notes it is still blowing just as badly and requests a decision.
SC1_B302_STYLE_1786_240|Doesn't look like this sandstorm's letting up. What's the plan, Admiral?|this sandstorm's letting up.;What's the plan, Admiral?|The rougher voice explains the stall in a direct, colloquial tone and asks the admiral what to do.
SC1_B302_STYLE_1786_288|||The older voice hesitates, says the storm shows no sign of letting up and asks for the next move.
SC1_B302_STYLE_1786_348|Hmm... We could wait even longer and it still might not stop. What do we do?|wait even longer;still might not stop.;What do we do?|The youthful voice imagines waiting longer without success and asks for help deciding.
SC1_B302_STYLE_1786_412|||The formal voice says there is no sign the storm will stop and asks what they should do.
SC1_B302_CHOICE_2272_0|||Push through leaves the waiting spot and proceeds into the storm.
SC1_B302_CHOICE_2272_1|||Wait longer stays put a little longer. The caption is distinct from the first offer to wait.
180|||Hodram decides they have waited long enough and orders the party into the storm.
187|||The panel gives the sailors' apparent fatigue. It contains no separate loss-of-crew notice on this branch.
193|||Hodram decides the risk is too great and resolves to stay until the storm stops.
203|One day passed.|One day passed.|The time notice preserves the one-day delay and matches the same Japanese notice in the bear encounter.
207|||Hodram observes that the storm appears to have eased. Keep his judgment qualified.
SC1_B302_STYLE_2582_0|||The crew member thinks they should reach the edge of the desert shortly and trails off in uncertainty.
SC1_B302_STYLE_2582_40|||The measured voice expected to be through the desert already. By now distinguishes that from a prediction about soon.
SC1_B302_STYLE_2582_74|||The casual speaker says they should have reached the far side by now. The trailing doubt suits the situation.
SC1_B302_STYLE_2582_106|Shouldn't we be out of the desert by now...?|out of the desert;by now...?|The crew member wonders whether they should already be through. The single question keeps her uncertainty together.
SC1_B302_STYLE_2582_140|||The rougher voice thinks they should almost be out. The vernacular fits the individual delivery.
SC1_B302_STYLE_2582_176|We ought to be nearly through the desert...|nearly through the desert...|The older voice expects the crossing to end soon, despite the uncertainty.
SC1_B302_STYLE_2582_216|||The youthful voice thought the desert would end about here. The tentative statement fits the lookout exchange.
SC1_B302_STYLE_2582_254|I should think we're almost out of the desert...|almost out of the desert...|The measured speaker expects to emerge soon but leaves it open.
SC1_B302_STYLE_2900_0|||Two slots share this lookout's urgent instruction to look ahead.
SC1_B302_STYLE_2900_28|||The two casual voices share a short exclamation to draw the admiral's attention.
SC1_B302_STYLE_2900_48|||The rougher voice directs the admiral's attention to what they see.
SC1_B302_STYLE_2900_72|||The older voice calls out a simple imperative when he sees it.
SC1_B302_STYLE_2900_92|||The youthful crew member exclaims as soon as something appears.
SC1_B302_STYLE_2900_116|||The formal speaker cries out in an unfinished burst of recognition.
""",
    303: """
6|||Safia welcomes Hodram with an energetic greeting and uses his given-name token.
9|||She says his help has improved her dancing a great deal, in her own warm voice.
12|I have a little tip for you, by way of thanks.|a little tip for you,;by way of thanks.|Safia says the information is her way of thanking Hodram for his help.
16|||She says a mosque far inland honors a king from long ago and passes on the rumor that it holds a fine treasure.
20|||She repeats the legend that the king must find the seeker worthy. The friendly question encourages Hodram to try.
""",
}

review = checked_text(previous.review, {"len(records) == 81": "len(records) == 125"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::bog-and-desert-expeditions", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
