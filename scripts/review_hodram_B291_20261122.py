"""Review Hodram's jungle map warnings and cave encounter, including every crew voice."""

from scripts import review_hodram_B290_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = previous.base, previous.ROOT
OUTPUT = ROOT / "B291_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    291: "Without a map, the crew warns Hodram about entering the jungle. Inside, they find a deep cave and a tiger. On the attack branch, gunfire risks hitting allies and Hodram orders close combat. On the retreat branch they escape without pursuit. The scene ends when the group sees light at the exit.",
}

DECISIONS = {291: """
SC1_B291_STYLE_24_0|||The crew member warns that entering this jungle without a direction is dangerous. The direct caution suits the voice.
SC1_B291_STYLE_24_46|Admiral, it isn't safe to go wandering through a jungle like this.|it isn't safe;through a jungle like this.|The measured warning keeps the purposeless wandering and the danger of this particular jungle.
SC1_B291_STYLE_24_98|Admiral, it's way too dangerous to go wandering in there with no idea where we're going!|it's way too dangerous;with no idea;where we're going!|The casual voice protests strongly about entering without knowing where to go.
SC1_B291_STYLE_24_156|||This speaker explicitly says they will get lost in this jungle without a map. Preserve the contrast with the broader safety warnings.
SC1_B291_STYLE_24_216|Admiral, you'd have to be crazy to go blundering into this jungle.|you'd have to be crazy;into this jungle.|This rough crew member calls blind wandering reckless in a direct, colloquial voice.
SC1_B291_STYLE_24_270|Admiral, it's dangerous to go wandering through a jungle like this.|it's dangerous;through a jungle like this.|This older crew member warns against wandering without a clear route. The matter-of-fact delivery fits him.
SC1_B291_STYLE_24_322|||The youthful voice openly refuses to enter without a map. Keep the distinct informal contraction.
SC1_B291_STYLE_24_384|Admiral, a jungle like this is no place to wander without a plan.|a jungle like this;no place to wander;without a plan.|The measured crew member cautions that they need to know where they are going before entering.
37|There's something eerie about this jungle...|something eerie;about this jungle...|Hodram observes how unsettling the jungle feels. The pause leaves room for the officer's apprehension.
41|||The officer agrees and hopes nothing happens. The restrained phrasing suits the unease.
45|||Hodram recognizes the cave in a slow, quiet beat before considering their options.
49|It looks quite deep... But it's our only way forward.|It looks quite deep...;our only way forward.|The officer judges the cave deep and says it is their only route.
60|||The speaker is confident the cave will serve as a shortcut to the destination. That optimism follows the officer's caution.
66|||Hodram gives a quiet acknowledgment before the warning about the footing.
70|||The officer cautions the player by the exact given-name token and identifies slippery moss as the risk.
73|||Hodram acknowledges the caution without interrupting the scene progression.
77|||The anonymous low growl alerts the party before anyone sees the animal. Preserve the isolated panel and sound.
SC1_B291_STYLE_824_0|||The crew member breaks the silence and voices a bad feeling. Keep the hesitant opening.
SC1_B291_STYLE_824_32|||The measured speaker notes something in the cave and says it does not bode well.
SC1_B291_STYLE_824_62|||The crew member hesitates in the middle of the discovery. The pause conveys uncertainty before the sense of dread.
SC1_B291_STYLE_824_92|There's something in here, isn't there? I've got a bad feeling...|isn't there?;I've got a bad feeling...|The crew member checks that the others noticed it too, then voices unease. Keep the question tag readable.
SC1_B291_STYLE_824_126|||The rough crew member is certain something is present yet has a bad feeling about it.
SC1_B291_STYLE_824_166|||The older voice notices something with them in the cave and is uneasy. The initial pause suits the moment.
SC1_B291_STYLE_824_198|||The youthful voice repeats the hesitation, asks for reassurance, and voices a bad feeling.
100|||The crew member stammers as the animal appears. Keep the exclamation and surprise.
SC1_B291_CHOICE_1114_0|||The first choice orders an attack and leads to Hodram's firing order.
SC1_B291_CHOICE_1114_1|||The second choice orders flight and leads to the observation that the tiger is not pursuing them.
115|||Hodram gives a quick, isolated order to shoot after the attack choice.
119|Rawr!!|Rawr!!|The tiger barks out a sharper roar after the shot, distinct from its first low growl.
123|||The crew member cries out immediately after the tiger's roar. Keep the sound distinct.
127|||Hodram curses and reacts to the tiger's speed. The short assessment fits the action.
SC1_B291_STYLE_1246_0|||The speaker stops the firing and emphasizes the high risk of hitting allies in the cramped space.
SC1_B291_STYLE_1246_72|||The measured speaker voices the same risk and trails off in alarm. The unfinished warning has its own cadence.
SC1_B291_STYLE_1246_136|||The casual crew member tells them to stop and says they might hit each other in the confined space.
SC1_B291_STYLE_1246_200|||This urgent voice orders an end to the shooting and says how easily the shooter could hit one of the party.
SC1_B291_STYLE_1246_274|||The rougher voice bluntly predicts hitting allies if they fire in a space this tight.
SC1_B291_STYLE_1246_332|||The older crew member says they cannot fire in the cave without risking their own people.
SC1_B291_STYLE_1246_400|Admiral! It's so cramped in here, we might hit the others!|It's so cramped in here,;we might hit the others!|The youthful voice calls urgently to the admiral. The exclamation carries the drawn-out call without distorting the name of the rank.
SC1_B291_STYLE_1246_462|We can't! In a space this tight, we're far too likely to hit one of our own!|In a space this tight,;far too likely;one of our own!|The formal speaker refuses the order and emphasizes the high likelihood of hitting an ally in cramped quarters.
152|Hmm... We'll only get more people hurt. Close combat!|get more people hurt.;Close combat!|Hodram recognizes that firing would cause further injuries and changes the order to hand-to-hand fighting.
SC1_B291_STYLE_1890_0|||The crew member is breathless and observes that they managed to bring the animal down.
SC1_B291_STYLE_1890_32|We managed to bring it down.|bring it down.|The measured voice acknowledges the effort and result without the audible panting of other alternatives.
SC1_B291_STYLE_1890_52|||The crew member pants and doubts whether they have really defeated the tiger. Keep the tentative end.
SC1_B291_STYLE_1890_86|||The panted breaths precede this crew member's more cautious assessment that they have won.
SC1_B291_STYLE_1890_120|||The rough crew member pauses briefly and announces success in plain language.
SC1_B291_STYLE_1890_134|||The older crew member gasps for breath and exclaims that they finally managed to defeat it.
SC1_B291_STYLE_1890_166|We finally got it! That tiger was tough!|We finally got it!;That tiger was tough!|The youthful crew member celebrates the result and comments on how strong the tiger was.
SC1_B291_STYLE_1890_208|||The formal speaker pants and voices relief at having managed to defeat it.
186|||The panel reports apparent injuries to quite a few sailors and does not invent a number.
SC1_B291_STYLE_2194_0|I guess it wasn't hungry. It's not following us.|I guess it wasn't hungry.;It's not following us.|The crew member infers the tiger was not hungry from the lack of pursuit.
SC1_B291_STYLE_2194_44|It seems it wasn't hungry. It isn't pursuing us.|It seems it wasn't hungry.;It isn't pursuing us.|This speaker gives a composed assessment of the lack of hunger and notes that they are not being pursued.
SC1_B291_STYLE_2194_92|||The casual crew member guesses the tiger was not hungry after all and says it is not chasing them.
SC1_B291_STYLE_2194_158|||This voice expresses personal relief at the lack of pursuit after inferring the animal was not hungry.
SC1_B291_STYLE_2194_226|Ain't chasing us, so I guess it wasn't hungry... We got lucky.|it wasn't hungry...;We got lucky.|The rough crew member directly links the lack of pursuit to lack of hunger and expresses relief.
SC1_B291_STYLE_2194_300|It's not coming after us. I suppose the tiger wasn't hungry.|It's not coming after us.;the tiger wasn't hungry.|The older crew member recognizes they are no longer in danger and draws the original inference.
SC1_B291_STYLE_2194_364|||The youthful voice names the tiger and brightens when it does not chase them.
SC1_B291_STYLE_2194_418|It seems it wasn't hungry. It isn't pursuing us.|It seems it wasn't hungry.;It isn't pursuing us.|Repeat the matching measured source wording for this stored alternative.
211|||The crew member lets out a relieved breath and says they are safe.
221|||Hodram notices a light ahead, with a pause as it catches his attention.
225|||The officer recognizes that the light marks a way out. The brief conclusion ends the cave scene.
"""}

review = checked_text(previous.review, {"len(records) == 88": "len(records) == 60"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::cave-encounter", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
