"""Review the boulder pursuit, branching forest route, and lookout voices."""

from scripts import pair_hodram_B311_B324_20261122 as paired
from scripts import review_hodram_B309_B310_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B311_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    311: "The party needs a map before entering a very dark forest. A rock comes from behind. The first menu chooses a path, and the second chooses which side of the brush to dive into after a dead end. The group can encounter a snake or see the rock roll down the left path. The lookout finally spots the destination.",
}
DECISIONS = {311: """
SC1_B311_STYLE_24_0|Admiral, we can't go any farther without a map.|we can't go any farther;without a map.|The crew member addresses the admiral politely and says the party needs a map to go farther.
SC1_B311_STYLE_24_40|||The measured voice calls proceeding without a map reckless. Keep the stronger warning.
SC1_B311_STYLE_24_82|Admiral, how'll we know where to go without a map?|know where to go;without a map?|The casual speaker worries about knowing which way to go. The question makes his uncertainty sound immediate.
SC1_B311_STYLE_24_132|Admiral, we won't know which way to go without a map.|which way to go;without a map.|The crew member describes how a missing map leaves the party without a route.
SC1_B311_STYLE_24_182|||The rougher crew member says they need a map before they can proceed. The short sentence fits his voice.
SC1_B311_STYLE_24_220|Without a map, Admiral, how will we know the way?|Without a map,;how will we know the way?|The older speaker warns that they cannot tell where to go. His cadence differs from the casual question.
SC1_B311_STYLE_24_270|Admiral, we won't know where to go if we don't have a map!|know where to go;if we don't have a map!|The youthful crew member worries that they will not know the way and says so directly.
SC1_B311_STYLE_24_324|||The formal voice explains that proceeding without a map is impossible. The firmer phrasing distinguishes it.
SC1_B311_STYLE_436_0|||The speaker remarks on how dark the forest is. Straightforward English suits the observation.
SC1_B311_STYLE_436_28|The trees are thick...|The trees are thick...|This speaker notices the dense growth and trails off.
SC1_B311_STYLE_436_46|It's awfully dark for the middle of the day.|awfully dark;middle of the day.|The casual voice contrasts how dark it feels with the fact that it is daytime.
SC1_B311_STYLE_436_74|||The crew member voices surprise at the darkness once they are in the forest.
SC1_B311_STYLE_436_98|||The rougher crew member comments on the darkness in a familiar cadence.
SC1_B311_STYLE_436_118|||The older voice observes that the trees are thick. Keep the separate focus on density.
SC1_B311_STYLE_436_140|||The youthful voice says it feels as dark as night. The plain simile belongs to this alternative.
SC1_B311_STYLE_436_172|||The formal speaker makes a short observation about the dense woods and trails off.
SC1_B311_STYLE_654_0|||Three slots share a quiet address to the admiral and a question about a sound.
SC1_B311_STYLE_654_28|||The casual speaker asks whether Hodram heard something. The shorter question fits his voice.
SC1_B311_STYLE_654_52|Admiral... Do you hear that?|Do you hear that?|The speaker notices a sound and seeks confirmation. The question keeps her tentative delivery.
SC1_B311_STYLE_654_78|||The rougher voice gets the admiral's attention and urges him to listen. The blunt imperative fits.
SC1_B311_STYLE_654_102|||The older speaker asks whether the admiral can hear the sound too.
SC1_B311_STYLE_654_126|||The youthful speaker says there is a sound and trails off without identifying it.
84|||Hodram gives a puzzled reaction before anyone identifies the danger.
SC1_B311_STYLE_838_0|Whoa! There's a rock coming at us from behind!|coming at us from behind!|The lookout warns that the rock is approaching from behind. The initial gasp marks sudden danger.
SC1_B311_STYLE_838_26|||Two slots warn about something behind the party without identifying it. Preserve their shared cry.
SC1_B311_STYLE_838_44|||The casual warning specifies that the rock is huge, unlike the less specific voices.
SC1_B311_STYLE_838_74|||The speaker screams and alerts the group to look behind them without naming the object.
SC1_B311_STYLE_838_96|||The rough lookout notices a rock behind them and exclaims. Keep the concise identification.
SC1_B311_STYLE_838_120|||The young crew member stammers out only the direction of the threat.
SC1_B311_STYLE_838_138|A rock's coming down behind us!|coming down behind us!|The formal speaker warns that a rock is coming down from behind. The utterance keeps the direction and motion.
113|||The sailor screams at the sudden rock. The sound cues Hodram's order.
117|||Hodram immediately orders everyone to run. The line works as an urgent group command.
SC1_B311_CHOICE_1086_0|||Go left sends the group down the left path.
SC1_B311_CHOICE_1086_1|||Go right sends the group down the right path.
SC1_B311_STYLE_1124_0|||Three slots share the urgent realization they have reached a dead end. Keep the shared line.
SC1_B311_STYLE_1124_20|||The casual voice blurts out its surprise and identifies the dead end.
SC1_B311_STYLE_1124_46|||The crew member protests in alarm as she recognizes there is no way through.
SC1_B311_STYLE_1124_70|||The rougher speaker calls out the dead end without a separate exclamation.
SC1_B311_STYLE_1124_88|||The older voice starts with alarm and then tells the group what blocks them.
SC1_B311_STYLE_1124_114|||The youthful voice announces the dead end in a drawn-out cry. The short content suits the hurry.
156|||Hodram urgently tells everyone to dive into the brush at the side of the path.
SC1_B311_CHOICE_1306_0|||Brush on the left identifies the left hiding place.
SC1_B311_CHOICE_1306_1|||Brush on the right identifies the distinct hiding place on the right.
172|||The silence precedes Hodram's call from the brush.
176|||Hodram urgently checks whether everyone is all right after diving for cover.
180|Yeah!|Yeah!|The sailor calls back in a tired but affirmative voice.
185|||The same quiet interval precedes the check on the other side of the path.
189|||Hodram makes the same head count whichever of these two hiding places they reach.
193|Yeah!|Yeah!|The sailor gives the same quick assurance on the other branch.
SC1_B311_STYLE_1460_0|||Seven slots share a quiet puzzled sound just before the next surprise.
SC1_B311_STYLE_1460_6|||This distinct voice reacts with a questioning Oh before the scream.
SC1_B311_STYLE_1500_0|||The group of styles shares the source's sustained cry of shock.
SC1_B311_STYLE_1500_18|Eeeeeek!!|Eeeeeek!!|This style has a distinct high scream. Preserve that difference before the snake is named.
239|||Hodram reacts to the scream by demanding to know what is wrong.
SC1_B311_STYLE_1578_0|||The lookout stammers as he identifies a snake. No size is specified in this alternative.
SC1_B311_STYLE_1578_14|||The measured speaker identifies a giant snake. Keep the size that distinguishes this line.
SC1_B311_STYLE_1578_28|||The casual voice stumbles over the word snake in alarm.
SC1_B311_STYLE_1578_46|||The crew member stammers while announcing there is a snake. The urgency fits the moment.
SC1_B311_STYLE_1578_68|S-snake!!|S-snake!!|The rough voice stammers out the animal's name. The original cry is complete without an added warning.
SC1_B311_STYLE_1578_80|||The older speaker also stammers as he calls out the snake.
SC1_B311_STYLE_1578_96|A-a snake!!|A-a snake!!|The youthful voice stammers and drags out the alarm. Let the doubled exclamation carry the volume.
SC1_B311_STYLE_1578_116|||The formal voice notes that now they have a snake to contend with, after the earlier rock.
270|||The sailor squeals and urgently tells the party to run.
274|||The lookout catches their breath after running. Keep both audible breaths.
278|||The sailor cries that he cannot take any more. The outburst follows both fright and exertion.
284|||The result notice reports apparent sailor fatigue. The wording matches the earlier identical notice.
290|||Hodram tells everyone there is little distance left and urges them to keep their nerve.
SC1_B311_STYLE_1918_0|||Two slots share the sudden observation that the rock rolled down the left path.
SC1_B311_STYLE_1918_34|||The measured speaker explicitly names the rock and the path it took. The direction must remain left.
SC1_B311_STYLE_1918_68|||The casual crew member celebrates their luck before saying the rock went left.
SC1_B311_STYLE_1918_104|||The crew member succinctly calls out where the rock went. Left stays explicit.
SC1_B311_STYLE_1918_130|||The rough voice says the rock rolled left in a plain, emphatic shout.
SC1_B311_STYLE_1918_156|||The older voice exclaims before saying the rock went down the left path.
SC1_B311_STYLE_1918_190|||The youthful speaker announces the rock's leftward path with relief audible in the exclamation.
323|||Hodram acknowledges the party has escaped. The short relief fits the turn.
327|||The sailor catches his breath and admits the scare in a familiar voice.
SC1_B311_STYLE_2220_0|||Five slots share the urgent call for the admiral to look at what they have spotted.
SC1_B311_STYLE_2220_24|||The measured lookout points out the destination with a short exclamation.
SC1_B311_STYLE_2220_50|||The older speaker gets the admiral's attention and points to the visible destination.
SC1_B311_STYLE_2220_74|||The youthful voice excitedly calls the admiral's attention to the find.
"""}
review = checked_text(previous.review, {"len(records) == 89": "len(records) == 80"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::boulder-and-brush-choices", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
