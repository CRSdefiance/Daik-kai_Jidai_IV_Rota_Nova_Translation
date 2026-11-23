"""Review the wolf encounter and the hostess's private route directions."""

from scripts import review_hodram_B304_B308_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = previous.base, previous.ROOT
OUTPUT = ROOT / "B309_B310_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    309: "The crew stops for a map before entering the woods. A wolf appears, and the party can drive it off, fight, or run. Injury, fatigue and separation have distinct notices. The crew reacts in alternative voices before the group finally reaches the destination.",
    310: "A hostess recognizes Hodram and guesses he wants to find the city gate. She explains the policy that normally bars her from telling him, then privately decides to help.",
}
DECISIONS = {
    309: """
SC1_B309_STYLE_24_0|||The crew member warns the admiral that they will get lost if they go without a map.
SC1_B309_STYLE_24_32|Admiral, without a map we'll lose our way.|without a map;we'll lose our way.|This measured voice gives the warning plainly and keeps the direct address.
SC1_B309_STYLE_24_62|Admiral, shouldn't we get a map first?|shouldn't we get a map first?|The casual speaker asks whether continuing without a map is a bad idea. A short question conveys the suggestion.
SC1_B309_STYLE_24_98|||The crew member warns that the party could lose its way, with the same uncertainty as the source.
SC1_B309_STYLE_24_130|||The rougher voice calls going without a map asking for trouble. The phrasing fits his warning.
SC1_B309_STYLE_24_158|||The older speaker observes the missing map and predicts that the party will get lost.
SC1_B309_STYLE_24_194|Admiral, we need a map before we go!|before we go!|The youthful voice says the party needs a map if they intend to continue.
SC1_B309_STYLE_24_224|||The formal voice emphasizes that they are sure to lose their way without a map.
SC1_B309_STYLE_322_0|Come on, let's get going.|let's get going.|These four slots share the invitation to set out and now use the same English as the matching source in the swamp.
SC1_B309_STYLE_322_20|||Both casual slots share the short, enthusiastic call to set out.
SC1_B309_STYLE_322_36|||The rough speaker signals departure with a plain two-word call.
SC1_B309_STYLE_322_50|||The older voice calmly suggests moving on.
SC1_B309_STYLE_422_0|||The crew member stammers on the admiral's title in sudden alarm.
SC1_B309_STYLE_422_28|Ah! A wolf!|A wolf!|The measured speaker reacts in surprise on spotting the wolf.
SC1_B309_STYLE_422_48|||The casual speaker stammers while warning the admiral that a wolf has appeared.
SC1_B309_STYLE_422_74|||This speaker screams before calling out the animal. The doubled urgency is in the source.
SC1_B309_STYLE_422_102|||The rougher voice cries out and immediately identifies the wolf.
SC1_B309_STYLE_422_132|||The older speaker stammers the address before calling the animal a wolf.
SC1_B309_STYLE_422_160|||The youthful voice lets out a long cry before recognizing the animal aloud.
SC1_B309_STYLE_422_186|||The formal voice stammers during the warning while identifying the wolf plainly.
89|||The sailor cries out in fright. The short sound fits the pause before Hodram speaks.
94|||Hodram tells the frightened sailor to calm down. The steady instruction fits his leadership.
98|||The sailor stammers while asking what Hodram intends to do.
SC1_B309_CHOICE_738_0|||Drive it off offers to scare the wolf away without leaving or choosing a fight.
SC1_B309_CHOICE_738_1|||Fight commits the party to the confrontation.
SC1_B309_CHOICE_738_2|||Run leaves the encounter in a hurry. Keep it distinct from driving the wolf away.
117|||Hodram says to leave the task to him and announces that he will drive off the wolf.
SC1_B309_STYLE_810_0|||Three style slots share the short warning to the admiral. It preserves the initial recognition and urgency.
SC1_B309_STYLE_810_22|||The casual speaker calls to the admiral and urgently warns him to look out.
SC1_B309_STYLE_810_50|||This speaker says watch out as a natural variation within the same danger beat.
SC1_B309_STYLE_810_76|||The rougher voice gives an immediate alert without addressing the admiral by title.
SC1_B309_STYLE_810_92|||The older voice notices the danger and urgently calls to the admiral.
SC1_B309_STYLE_810_118|||The youthful speaker calls to the admiral and gives the same urgent warning.
140|||Hodram blurts out the realization that he dropped his guard. The abrupt exclamation suits the injury.
SC1_B309_STYLE_1006_0|||Five slots share the immediate, concerned question about Hodram's condition.
SC1_B309_STYLE_1006_16|||The casual voice checks on Hodram without a formal address.
SC1_B309_STYLE_1006_28|||The older crew member asks if Hodram is all right. The urgency belongs to the punctuation.
SC1_B309_STYLE_1006_40|||The youthful crew member asks the same question with a gentler rise.
167|||Hodram dismisses the wound as a scratch and tells the crew not to worry.
174|||The result notice confirms that the named character was injured. Keep the given-name substitution and the speakerless panel.
178|Form up! We'll break through together!|Form up!;break through together!|Hodram orders the group to take formation and push through as one. The commands are urgent.
SC1_B309_STYLE_1214_0|||Six slots share a short warning to the party as they run into danger.
SC1_B309_STYLE_1214_12|Watch out!|Watch out!|The rough crew member gives a distinct brief shout before the injury.
SC1_B309_STYLE_1214_24|Look out, look out!|Look out, look out!|The youthful voice urgently warns of danger. Repeating the alarm conveys the drawn-out cry.
SC1_B309_STYLE_1278_0|||Five slots share the same involuntary sound after a hit.
SC1_B309_STYLE_1278_10|||The older speaker gives a short involuntary cry on being hit.
SC1_B309_STYLE_1278_26|||The speaker gives a prolonged scream distinct from the shorter cries around it.
SC1_B309_STYLE_1278_34|||The youthful speaker cries loudly when struck. Keep the drawn-out response.
226|||Hodram immediately asks whether the crew member is all right. The short question conveys urgency.
SC1_B309_STYLE_1368_0|||Three slots share a strained reply that the speaker is managing. Keep the original stammer.
SC1_B309_STYLE_1368_18|Ow! That hurts...|That hurts...|The crew member winces and complains about the pain. Complete the thought in the speaker's voice.
SC1_B309_STYLE_1368_36|||The crew member cries out in pain and trails away. The response sounds shaken.
SC1_B309_STYLE_1368_56|Ugh! Th-this is nothing.|Th-this is nothing.|The rougher voice stammers while trying to brush off the injury.
SC1_B309_STYLE_1368_96|||The older voice struggles through the assurance that he is all right.
SC1_B309_STYLE_1368_120|||The young crew member wails and bluntly says he is not okay.
249|||Hodram blames his lapse for the injury and sincerely apologizes. The existing pause lets him voice regret before the apology.
SC1_B309_STYLE_1590_0|It'll be all right if we treat it right away. The wolf's gone now, too.|treat it right away.;The wolf's gone now, too.|The crew member reassures the admiral that prompt treatment should help and says the wolf fled.
SC1_B309_STYLE_1590_50|||The measured voice reassures Hodram respectfully and notes that the wolf is gone. Keep the qualified promise of healing.
SC1_B309_STYLE_1590_122|||The casual speaker cheerfully says all they need to do is treat the injury quickly. The wolf has already gone.
SC1_B309_STYLE_1590_182|||The speaker stresses prompt care and expresses relief that the wolf will not cause further trouble.
SC1_B309_STYLE_1590_236|Don't worry about it! Treat a wound like that right away and it'll heal. The wolf's gone, too.|Don't worry about it!;right away and it'll heal.;The wolf's gone, too.|The rougher voice tells Hodram not to dwell on the injury and adds that the wolf has gone.
SC1_B309_STYLE_1590_306|Don't blame yourself. If we tend to the wound now, it won't turn serious. The wolf's gone. That's that.|Don't blame yourself.;it won't turn serious.;That's that.|The older crew member reassures Hodram, emphasizes treating the wound promptly and closes the incident after the wolf leaves.
SC1_B309_STYLE_1590_394|We'll patch it up right away. It'll be fine! The wolf ran off, too. What a relief!|patch it up right away.;It'll be fine!;What a relief!|The youthful voice expresses confidence and relief that the wolf fled.
SC1_B309_STYLE_1590_456|||The formal voice says an injury of this size should heal with prompt care and notes that the wolf already fled.
273|||Hodram acknowledges the practical reassurance with a brief reply.
280|Your sailors look tired.|Your sailors look tired.|The panel reports apparent fatigue. Match the same notice in the earlier expedition.
285|||Hodram thinks the wolf looks hungry and urgently orders an escape. Its condition stays his inference.
294|||The panel states fatigue and says some sailors appear to be missing. Keep the separate outcomes and uncertainty about the second.
SC1_B309_STYLE_2364_0|||The sound of three labored breaths leads into a shared, hopeful statement about having reached safety.
SC1_B309_STYLE_2364_54|||The casual crew member pants and asks if the group is safe now.
SC1_B309_STYLE_2364_110|Hah... Hah... Hah... We're safe now, aren't we?|We're safe now, aren't we?|This speaker catches her breath and seeks reassurance with the tag intact.
SC1_B309_STYLE_2364_164|||The rougher voice checks that they are safe where they have stopped.
SC1_B309_STYLE_2364_220|||The older voice breathes heavily and stammers while confirming they are probably safe.
SC1_B309_STYLE_2364_268|Hah... Hah... This far should be safe, right?|This far should be safe, right?|The young crew member pants and seeks reassurance that they ran far enough.
SC1_B309_STYLE_2364_306|||The formal voice catches its breath and says its position should be safe now.
SC1_B309_STYLE_2758_0|||Four slots share the observation that they are nearly through the forest. The prediction keeps the original uncertainty.
SC1_B309_STYLE_2758_32|Aren't we nearly out of the woods?|nearly out of the woods?|The casual crew member checks whether they are approaching the edge. The question keeps the thought together.
SC1_B309_STYLE_2758_62|||The rougher crew member guesses they will soon be out of this forest.
SC1_B309_STYLE_2758_92|We ought to be out of the forest soon.|out of the forest soon.|The older voice expects the forest to end soon, without guaranteeing it.
SC1_B309_STYLE_2758_122|||The young voice says the forest must end soon. The simple cadence fits its certainty.
SC1_B309_STYLE_2938_0|||Four slots share the announcement that the destination has come into view.
SC1_B309_STYLE_2938_26|||The casual lookout recognizes the destination and tells the admiral.
SC1_B309_STYLE_2938_42|||The crew member excitedly points out the destination as soon as she sees it.
SC1_B309_STYLE_2938_64|||The older voice calls out that the destination is now visible.
SC1_B309_STYLE_2938_86|||The youthful lookout announces that they have found it and addresses the admiral.
""",
    310: """
6|||The hostess welcomes Hodram using the original given-name token.
9|||She guesses that he wants directions to the city gate. The tag makes her sound conversational.
13|||She says the gate's location is not supposed to be shared with visitors from abroad. Her trailing voice sets up the exception.
16|With all the pressure from abroad, we hardly have a policy of isolation anymore. All right. I'll tell you, but keep it between us.|pressure from abroad,;a policy of isolation;keep it between us.|She attributes the weakening of her country's isolation policy to pressure from abroad and privately agrees to give the directions.
""",
}

review = checked_text(previous.review, {"len(records) == 67": "len(records) == 89"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::wolf-and-private-directions", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
