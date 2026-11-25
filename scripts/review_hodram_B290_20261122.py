"""Review every crew alternative and choice in Hodram's forest encounter."""

from scripts import review_hodram_B281_B289_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = previous.base, previous.ROOT
OUTPUT = ROOT / "B290_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    290: "A crew voice stops an expedition without a map. In the woods they meet a bear and can fight, play dead or choose between trying to scare it and running. The difficulty, injury and time notices belong to different branches. The crew voices react according to their personality before the party finally sights the ruins.",
}

DECISIONS = {290: """
SC1_B290_STYLE_24_0|||The crew member warms the warning with an ordinary contraction and says the party will lose its way without a map.
SC1_B290_STYLE_24_40|Admiral, we'll lose our way without a map.|we'll lose our way;without a map.|This crew member gives a straightforward warning in a measured voice.
SC1_B290_STYLE_24_72|||This casual voice blurts out the prospect of getting lost. Keep the emphatic ending.
SC1_B290_STYLE_24_108|||The rougher voice says they'll get themselves lost. The reflexive phrasing distinguishes it.
SC1_B290_STYLE_24_148|||This voice urges bringing a map and explains the consequence in a firm cadence.
SC1_B290_STYLE_24_186|Admiral, we're gonna get lost without a map!|we're gonna get lost;without a map!|The youthful voice drags out its protest. A loose contraction keeps it distinct from the other warnings.
SC1_B290_STYLE_24_228|Without a map, Admiral, we'll surely lose our way.|Without a map,;surely lose our way.|The older formal voice stresses the certainty of losing their way.
SC1_B290_STYLE_328_0|||The speaker notices how thick the woods are and suggests caution in an ordinary voice.
SC1_B290_STYLE_328_40|The forest is dense. We should watch where we're going.|The forest is dense.;watch where we're going.|The measured crew member proposes care as they enter the dense forest.
SC1_B290_STYLE_328_78|||The speaker grumbles about the darkness and an uneasy feeling. The pause leaves that unease hanging.
SC1_B290_STYLE_328_110|These woods are thick. I hope we don't get lost.|These woods are thick.;I hope we don't get lost.|This crew member worries personally about losing the trail after seeing the density of the woods.
SC1_B290_STYLE_328_156|||The crew member's curt remark captures the ominous feeling of the forest. Preserve the restraint.
SC1_B290_STYLE_328_182|||The older voice urges caution and readiness without repeating someone else's description.
SC1_B290_STYLE_328_212|||The youthful crew member hopes to find something good. The optimism stands apart from the other reactions.
SC1_B290_STYLE_328_244|These woods are dense. Let's hope nothing comes out of them...|These woods are dense.;nothing comes out of them...|This measured warning turns the dense woods into a worry about what might emerge. Keep the hesitation.
62|||Hodram orders the party forward after weighing the crew's reactions. The short decision fits.
SC1_B290_STYLE_670_0|||The speaker stammers the address and warns of something behind the admiral. The same stored utterance serves three styles.
SC1_B290_STYLE_670_18|||The crew member urgently tells Hodram to hold still and leaves the warning unfinished.
SC1_B290_STYLE_670_56|A-Admiral, behind you...|A-Admiral, behind you...|The casual crew member stammers at the address and gives the same unfinished warning as the matching voice.
SC1_B290_STYLE_670_76|Eek... B-behind you...|B-behind you...|This crew member squeaks and struggles to get the warning out.
SC1_B290_STYLE_670_100|Ah! Behind you, Admiral...|Behind you, Admiral...|The older crew member notices the threat and calls out without the other styles' stammer.
SC1_B290_STYLE_670_120|||This youthful voice recoils and stumbles over the first word of the warning.
92|||Keep the nonverbal reaction and its original speaker state before the warning that follows.
96|||The abrupt alert conveys immediate danger without identifying the creature early.
SC1_B290_CHOICE_876_0|||The caption offers to fight and leads to Hodram's order to shoot.
SC1_B290_CHOICE_876_1|||The caption offers to play dead and matches the crew's subsequent wait.
SC1_B290_CHOICE_876_2|||The caption deliberately leaves the alternative open. The later menu supplies the two options.
118|||Hodram gives the short firing order after the choice to fight.
SC1_B290_STYLE_970_0|||The excited voices report the bear's retreat without mentioning it by name. Keep the shared utterance.
SC1_B290_STYLE_970_26|||The speaker explicitly identifies the bear that ran off.
SC1_B290_STYLE_970_48|||The crew member exclaims at seeing it flee. The present progressive follows what she's watching.
SC1_B290_STYLE_970_72|Oh! There goes the bear!|There goes the bear!|The older voice spots the bear retreating and exclaims as it goes.
SC1_B290_STYLE_970_98|||The youthful speaker celebrates the bear leaving immediately. The higher energy distinguishes the delivery.
148|||The result panel reports minor injuries among some sailors and leaves their exact number unknown.
SC1_B290_STYLE_1166_0|A-Admiral... That bear doesn't look like it's going anywhere.|That bear doesn't look;like it's going anywhere.|The stammered report says that after waiting, the bear still gives no sign of leaving.
SC1_B290_STYLE_1166_58|||The measured voice hesitates before stating plainly that the bear shows no sign of leaving.
SC1_B290_STYLE_1166_112|||The crew member gives up on the tactic and complains that the bear will not move.
SC1_B290_STYLE_1166_148|||The stammered address leads into the speaker's assessment that lying still is not working.
SC1_B290_STYLE_1166_198|A-Admiral... It's no use. That damn bear won't budge.|It's no use.;That damn bear won't budge.|The rough reply keeps the fearful stammer and the emphasis on the bear's refusal to leave.
SC1_B290_STYLE_1166_248|This won't do. That bear looks like it's here to stay.|This won't do.;it's here to stay.|The older voice judges the tactic a failure and sees no sign that the bear will go away.
SC1_B290_STYLE_1166_310|||The youthful address and Mr. Bear preserve the affectionate, nervous contrast to the rough voice.
SC1_B290_STYLE_1166_358|||The measured voice hesitates and states there is no sign the bear will move.
175|||The whispered order asks the party to endure the wait. Its restrained delivery fits playing dead.
179|||The silence lets the wait play out before the bear loses interest.
SC1_B290_STYLE_1632_0|||This shared relieved breath is followed by recognition that the bear has finally given up.
SC1_B290_STYLE_1632_28|||The speaker exhales and observes that the bear has finally given up.
SC1_B290_STYLE_1632_56|||The rough voice disparages the bear as it gives up. The relief is still audible.
SC1_B290_STYLE_1632_90|||The older speaker snores while the others wait. That sound sets up Hodram saying Emilio's name.
214|||Hodram questions whether Emilio has fallen asleep. Keep the approved name and small pause that follows.
218|||The breathing sound continues the sleeping response, separate from the earlier style-specific snore.
222|||Hodram realizes Emilio really fell asleep. The dry phrasing and unfinished cadence land the joke.
233|||The speakerless notice records exactly one day passing on the waiting branch.
SC1_B290_CHOICE_1876_0|||The caption offers to drive the bear off by frightening it.
SC1_B290_CHOICE_1876_1|||The caption offers immediate flight in plain idiomatic English.
SC1_B290_STYLE_1924_0|We tried to scare it off, but it won't run!|scare it off,;it won't run!|The crew member reports that the attempt failed. Keep the order of action and result.
SC1_B290_STYLE_1924_30|It won't run, even when we try to scare it off...|It won't run,;try to scare it off...|The measured voice is surprised the attempted intimidation did nothing.
SC1_B290_STYLE_1924_56|||The speaker first wonders what's wrong with the bear, then protests that the scare did not work.
SC1_B290_STYLE_1924_100|It's got some nerve! We can't scare it off!|It's got some nerve!;We can't scare it off!|This voice complains about the bear's nerve before saying the tactic is failing.
SC1_B290_STYLE_1924_136|||The rougher crew member begrudgingly calls the bear courageous and says it will not run.
SC1_B290_STYLE_1924_186|Good grief! No matter how we try to scare it, it won't run. What's the matter with it?|No matter how we try;it won't run.;What's the matter with it?|The older crew member sounds exasperated by the animal and asks why it will not flee.
SC1_B290_STYLE_1924_252|Huh? We tried to scare it off! Why won't it go away?|We tried to scare it off!;Why won't it go away?|The youthful voice wonders aloud why the attempt has not worked. The surprise belongs to this alternative.
SC1_B290_STYLE_1924_288|It won't run, even after all that... A bold creature indeed.|even after all that...;A bold creature indeed.|The formal speaker cannot believe the tactic failed and labels the bear bold.
278|||The crew member warns that the bear could eat people and that a wrong move would endanger the party. Keep the uncertainty.
SC1_B290_STYLE_2398_0|Admiral, look out! Damn... It got one of our people! We need to run before we're next!|Admiral, look out!;one of our people!;before we're next!|The crew member warns the admiral, reports an attack on a member of the party and urges flight.
SC1_B290_STYLE_2398_82|Look out! Oh no... It attacked someone! Let's get out of here before it comes for us!|It attacked someone!;get out of here;before it comes for us!|The speaker notices the attack, urges escape and warns of immediate danger to the rest of the group.
SC1_B290_STYLE_2398_168|Look out, Admiral! This is bad. It attacked one of us! Forget this. Run!|Look out, Admiral!;attacked one of us!;Forget this. Run!|The panicked crew member sees an attack and wants the party to give up and run.
SC1_B290_STYLE_2398_236|Admiral, look out! It's attacking one of our people! We'd better run!|Admiral, look out!;one of our people!;We'd better run!|The speaker sees a member of the party under attack and urgently recommends flight.
SC1_B290_STYLE_2398_314|||The rougher voice fears that several have been hurt and urges leaving. Keep the uncertain question.
SC1_B290_STYLE_2398_392|||The older crew member puts the warning first and tells the admiral they should flee.
SC1_B290_STYLE_2398_436|Watch out! Let's run! Please!|Let's run! Please!|The youthful warning and plea preserve the dragged-out alarm without distorting the spelling.
SC1_B290_STYLE_2398_470|||The measured voice judges the danger and recommends escape. The short clauses suit the urgency.
305|||The result panel reports a considerable increase in fatigue and apparent injuries. Preserve both outcomes.
313|||Hodram orders an immediate retreat. Keep the blunt shout separate from the crew warnings.
SC1_B290_STYLE_3040_0|We got away somehow...|We got away somehow...|The speaker is relieved to have escaped and sounds as though the result is still sinking in.
SC1_B290_STYLE_3040_32|||The breath precedes a measured acknowledgment that the party escaped.
SC1_B290_STYLE_3040_66|||The crew member pants and tentatively says they made it. Both beats are part of the relief.
SC1_B290_STYLE_3040_98|||The cautious speaker preserves uncertainty that the party is safe.
SC1_B290_STYLE_3040_120|||The shared response breathes out and checks that the bear has been left behind.
SC1_B290_STYLE_3040_142|Huff... Huff... I was so scared...|I was so scared...|The youthful crew member admits fear after the breathless escape.
SC1_B290_STYLE_3040_176|||The older crew member is out of breath and relieved that everyone appears to be safe.
SC1_B290_STYLE_3300_0|||The crew member announces the end of the forest and confirms that they reached the ruins.
SC1_B290_STYLE_3300_42|||This voice reports the group is through the woods and considers the ruins aloud.
SC1_B290_STYLE_3300_78|We're out of the forest at last... Oh! Admiral, these must be the ruins!|out of the forest at last...;these must be the ruins!|The speaker moves from relief to a sudden recognition of the ruins.
SC1_B290_STYLE_3300_142|||The crew member observes that they are out of the woods, then recognizes the location with a pause.
SC1_B290_STYLE_3300_186|Admiral, we made it out of the woods! Yeah, those are the ruins!|made it out of the woods!;those are the ruins!|The rougher voice exclaims that the party got through, then identifies the ruins.
SC1_B290_STYLE_3300_244|||The older crew member remarks on getting through and wonders if the structures ahead are the ruins.
SC1_B290_STYLE_3300_302|||The young crew member celebrates getting out and asks whether the strange stones are the ruins. The simple terms fit the voice.
SC1_B290_STYLE_3300_394|||The formal speaker reports their exit to the admiral and gives a slower, awed recognition of the ruins.
"""}

review = checked_text(previous.review, {"len(records) == 90": "len(records) == 88"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::forest-encounter", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
