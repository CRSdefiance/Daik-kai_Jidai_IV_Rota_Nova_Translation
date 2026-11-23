"""Review both complete fog and jungle expeditions."""
from scripts import review_hodram_B312_B315_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text

base, ROOT = previous.base, previous.ROOT
OUTPUT = ROOT / "B316_B317_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    316: "The party meets fog while traveling. If they move, they confront a dead end and choose how to proceed. If they wait, the fog clears after a day.",
    317: "The crew enters a humid jungle and encounters a dark cave. The choice to feel a way forward leads to a snake, while lighting the cave reveals bats. Both routes lead on to the ruins.",
}
DECISIONS = {
    316: """
SC1_B316_STYLE_24_0|Admiral, we could lose our way without a map.|could lose our way;without a map.|The polite speaker warns that a missing map could leave them lost.
SC1_B316_STYLE_24_36|||The measured voice directly states what will happen without a map.
SC1_B316_STYLE_24_68|||The casual warning fits the crew member's familiar voice.
SC1_B316_STYLE_24_104|||The speaker gives her own tentative opinion about getting lost.
SC1_B316_STYLE_24_140|||The rough voice summarily dismisses proceeding without a map.
SC1_B316_STYLE_24_176|Admiral, we're bound to get lost without a map.|bound to get lost;without a map.|The older voice is certain they will get lost if they proceed.
SC1_B316_STYLE_24_214|||The youthful speaker directly asks the admiral to get a map first.
SC1_B316_STYLE_24_240|We'd surely lose our way without a map, Admiral.|surely lose our way;without a map, Admiral.|The formal voice is certain they will lose their way.
SC1_B316_STYLE_348_0|||The shared voice signals that it is time to set out.
SC1_B316_STYLE_348_22|||The measured speaker asks whether the group is ready to go.
SC1_B316_STYLE_348_40|||The casual voice urges the party to go in one enthusiastic line.
SC1_B316_STYLE_348_56|||The crew member says it is time to head out.
SC1_B316_STYLE_348_80|||The rougher voice briskly calls for departure.
SC1_B316_STYLE_348_100|Off we go, then! Keep your spirits up!|Keep your spirits up!|The older crew member urges the party to set out in good spirits.
SC1_B316_STYLE_348_124|||The youthful crew member makes an enthusiastic departure call.
SC1_B316_STYLE_520_0|||The speaker notices the fog rolling in.
SC1_B316_STYLE_520_20|||The measured voice observes the onset of fog.
SC1_B316_STYLE_520_40|||The casual voice notes that the weather is turning foggy.
SC1_B316_STYLE_520_56|||The crew member sees that it has gotten foggy.
SC1_B316_STYLE_520_76|||The rough voice calls out the thickness of the new fog.
SC1_B316_STYLE_520_96|||The older voice recognizes the fog coming in.
SC1_B316_STYLE_520_114|||The young speaker exclaims at how foggy it has become.
SC1_B316_CHOICE_674_0|||Keep going chooses to proceed despite the fog.
SC1_B316_CHOICE_674_1|||Wait for the fog to clear names the condition for resuming the journey.
104|||The captain suggests trying to move on for now.
SC1_B316_STYLE_754_0|||The polite voice recognizes what looks like a dead end.
SC1_B316_STYLE_754_26|||The measured voice pauses on discovering the dead end.
SC1_B316_STYLE_754_42|||The casual voice expresses frustration at reaching a dead end.
SC1_B316_STYLE_754_66|||The speaker quietly identifies the obstruction and trails off.
SC1_B316_STYLE_754_82|||The older voice calls it a dead end, with measured uncertainty.
SC1_B316_STYLE_754_108|||The youthful speaker sounds disappointed on finding the dead end.
SC1_B316_STYLE_754_132|Well, look at that. It's a dead end.|It's a dead end.|The formal voice reacts with mild surprise before identifying the obstruction.
SC1_B316_CHOICE_934_0|||Push on anyway chooses to continue through the obstruction.
SC1_B316_CHOICE_934_1|||Find a way around asks the party to look for another route.
144|Keep going, even if we have to cut through the trees.|cut through the trees.|The captain resolves to proceed even if clearing a way through the trees is required.
SC1_B316_STYLE_1010_0|I'll give it a try.|I'll give it a try.|The crew member volunteers to try after hearing the difficult order.
SC1_B316_STYLE_1010_14|||The measured voice agrees to give the proposed route a try.
SC1_B316_STYLE_1010_32|||The casual speaker calls the order crazy and reluctantly agrees to try it.
SC1_B316_STYLE_1010_72|||The crew member simply volunteers to try it.
SC1_B316_STYLE_1010_86|||The rough voice agrees enthusiastically to see the route through.
SC1_B316_STYLE_1010_112|||The older speaker doubts the plan but agrees to try it.
SC1_B316_STYLE_1010_152|||The youthful crew member protests that the plan is reckless before agreeing to go.
174|||The speakerless notice reports apparent fatigue after continuing through the trees.
179|Let's find a way around.|find a way around.|The captain orders an alternate route around the obstruction. Match the wording of the choice leading here.
SC1_B316_STYLE_1310_0|||The polite voice tells the admiral it found a fork.
SC1_B316_STYLE_1310_30|||The measured crew member reports the fork directly.
SC1_B316_STYLE_1310_58|||The casual lookout notices the fork on a closer look.
SC1_B316_STYLE_1310_94|||The crew member calls the admiral's attention to a path nearby.
SC1_B316_STYLE_1310_122|||The rougher voice draws attention to a path on this side.
SC1_B316_STYLE_1310_150|||The older speaker thinks this way may be passable.
SC1_B316_STYLE_1310_182|||The youthful speaker urgently calls the admiral over.
SC1_B316_STYLE_1310_210|||The formal crew member is surprised there is a path in this spot.
214|||The captain judges moving in the fog unsafe and suggests waiting for it to clear.
SC1_B316_STYLE_1634_0|||The polite crew member thinks waiting is the better choice.
SC1_B316_STYLE_1634_28|||The casual voice agrees to wait.
SC1_B316_STYLE_1634_42|||The crew member agrees in an understated line.
SC1_B316_STYLE_1634_56|||The rougher voice agrees and commits to waiting.
SC1_B316_STYLE_1634_78|||The older speaker sees no other reasonable option.
SC1_B316_STYLE_1634_104|||The youthful speaker readily agrees to wait.
SC1_B316_STYLE_1634_126|||The formal voice recognizes waiting would be safer.
243|||Keep the short silent beat during the wait.
247|||The longer silent beat continues the wait before the passage-of-time notice.
254|One day passed.|One day passed.|Give the same one-day notice as the other expeditions.
258|Looks like the fog has cleared. Let's get going.|the fog has cleared.;Let's get going.|The captain observes that the fog seems to have cleared and orders a departure.
SC1_B316_STYLE_1916_0|||The lookout announces the destination has come into view.
SC1_B316_STYLE_1916_18|||The casual crew member points out the destination as soon as it appears.
SC1_B316_STYLE_1916_32|||The rougher crew member gives a short recognition.
SC1_B316_STYLE_1916_46|||The questioning crew member is less certain of what has just appeared.
""",
    317: """
SC1_B317_STYLE_24_0|||The polite voice warns against wandering without a goal in this jungle.
SC1_B317_STYLE_24_52|||The casual crew member objects to wandering here without knowing which way to go.
SC1_B317_STYLE_24_106|||The crew member warns that wandering in the jungle without a clear direction is dangerous.
SC1_B317_STYLE_24_156|||The rough voice flatly refuses to wander around without a route.
SC1_B317_STYLE_24_214|||The older voice spells out that wandering in this jungle is dangerous.
SC1_B317_STYLE_24_266|||The youthful speaker mentions the missing map explicitly and objects to going without one.
SC1_B317_STYLE_24_326|Admiral, there's no safe way to wander blindly through this jungle.|wander blindly;through this jungle.|The formal voice warns against wandering through this jungle without a route.
SC1_B317_STYLE_446_0|||The crew member asks whether they should get going.
SC1_B317_STYLE_446_16|||The measured voice agrees it is time to leave.
SC1_B317_STYLE_446_36|||The casual speaker urges the crew to head out eagerly.
SC1_B317_STYLE_446_62|||The crew member gives a simple signal to get going.
SC1_B317_STYLE_446_84|||The rougher voice signals departure with a brief command.
SC1_B317_STYLE_446_100|Time to get going, then.|get going, then.|The older crew member prompts the group to depart in a measured voice.
63|Whew, it's humid here. I'm worried the crew's getting worn out...|it's humid here.;getting worn out...|The captain remarks on the high humidity and worries specifically about the party's fatigue.
SC1_B317_STYLE_654_0|||The shared voice is surprised to find a cave in this unlikely spot.
SC1_B317_STYLE_654_24|||The other voice notices the cave in a short, surprised turn.
89|||The captain notes that the cave is darker than he expected.
93|Admiral...|Admiral...|The crew member trails off addressing the captain by the same title used through the expedition.
SC1_B317_CHOICE_764_0|||Feel our way forward chooses to continue without lighting the cave.
SC1_B317_CHOICE_764_1|||Light a fire names the alternate choice in the original.
108|It's all right. We'll keep going.|We'll keep going.|The captain dismisses the concern about darkness and decides to continue anyway.
113|||The captain feels something in the dark. Preserve the question and unfinished recognition.
116|Admiral! A huge snake! Ah! It got one of us!|A huge snake!;It got one of us!|The caller identifies a giant snake and abruptly realizes a crew member is affected.
127|||The speaker tentatively identifies the Indian python. The parenthetical preserves his comic doubt.
133|||The captain recognizes the danger and quickly orders everyone to fall back.
141|||The notice reports an apparent injury to one sailor.
147|||The captain pauses and asks where they have ended up after retreating.
SC1_B317_STYLE_1114_0|||The speaker cannot say for certain and estimates their position is close to the ruins.
SC1_B317_STYLE_1114_46|||The measured speaker estimates that they are close to the ruins.
SC1_B317_STYLE_1114_76|||The casual voice is unsure at first and then guesses they are nearby.
SC1_B317_STYLE_1114_142|Uh... I think we're near the ruins.|near the ruins.|The hesitant voice checks the location and offers a tentative answer.
SC1_B317_STYLE_1114_180|||The rougher speaker reacts in surprise and asks whether they are right by the ruins.
SC1_B317_STYLE_1114_230|||The older voice is momentarily disoriented before realizing they exited near the ruins.
SC1_B317_STYLE_1114_286|||The youthful crew member guesses their whereabouts, then cheers at their luck.
SC1_B317_STYLE_1114_370|||The measured speaker pauses before describing the location as probable.
176|||The captain agrees to light a fire, leaving a quiet pause before the response.
180|Ugh! Bats?! Look at that swarm...|Bats?!;Look at that swarm...|The captain recoils at the number of bats. Preserve the scale without naming a specific count.
SC1_B317_STYLE_1648_0|||The shared voice urgently says there are too many bats.
SC1_B317_STYLE_1648_18|||The casual speaker emphasizes how greatly the bats outnumber the party.
SC1_B317_STYLE_1648_38|||The speaker screams and calls the number of bats abnormal.
SC1_B317_STYLE_1648_82|||The rougher voice gives a terse alarm about the number of bats.
SC1_B317_STYLE_1648_100|||The older speaker thinks they cannot get past so many bats.
SC1_B317_STYLE_1648_170|||The youthful voice screams, identifies bats and calls them disgusting.
206|||The captain tells the crew to ignore the bats and keep advancing.
214|||The notice reports apparent sailor fatigue as the expedition continues.
SC1_B317_STYLE_1974_0|||The speaker praises the captain and celebrates getting through the jungle.
SC1_B317_STYLE_1974_44|||The measured voice exclaims that they are through the jungle.
SC1_B317_STYLE_1974_66|We did it, Admiral! Out of the jungle!|Out of the jungle!|The casual voice celebrates with the direct address the Japanese supplies.
SC1_B317_STYLE_1974_102|||The crew member expresses relief at finally leaving the jungle.
SC1_B317_STYLE_1974_132|||The rougher voice celebrates the accomplishment with the admiral.
SC1_B317_STYLE_1974_168|||The older voice exclaims twice at making it out.
SC1_B317_STYLE_1974_202|||The formal voice congratulates the captain and confirms they made it through.
SC1_B317_STYLE_2252_0|||The lookout tentatively reports reaching the ruins.
SC1_B317_STYLE_2252_28|||The casual crew member identifies the ruins in a brief exclamation.
SC1_B317_STYLE_2252_50|Admiral, those are the ruins!|those are the ruins!|Keep the crew member's direct address when she points out the ruins.
SC1_B317_STYLE_2252_70|||The rougher voice quickly tells the admiral they found the ruins.
SC1_B317_STYLE_2252_92|||The older speaker tentatively confirms the party has reached the ruins.
SC1_B317_STYLE_2252_120|||The youthful voice calls out as soon as the ruins are visible.
SC1_B317_STYLE_2252_142|||The formal voice confirms the party finally reached the ruins.
""",
}
review = checked_text(previous.review, {"len(records) == 97": "len(records) == 127"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::fog-and-cave-exchanges", "exec"), scope)
if __name__ == "__main__":
    scope["main"]()
