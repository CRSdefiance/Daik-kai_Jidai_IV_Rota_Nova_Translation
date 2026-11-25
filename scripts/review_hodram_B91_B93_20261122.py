"""Review the miracle charm and Emilio's two food-centered town exchanges."""

from types import SimpleNamespace

from scripts import pair_hodram_opening_20261122 as pairing
from scripts import review_hodram_B81_B84_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base = previous.base
ROOT = pairing.ROOT.with_name("hodram_B91_B110_followup_20261122")
paired = SimpleNamespace(PACKET=ROOT / "paired_source_registered_candidate.json",
                         CARRY=ROOT / "prior_contextual_decisions.json")
OUTPUT = ROOT / "B91_B93_contextual_v2.json"
GLYPHS = set()
CONTEXTS = {
    91: "A sailor stops Hodram as the hundredth person he has questioned. What seems like an insult turns into an apology and an offer of the Miracle Bullet Charm. The other answer leads to Fernando's impatience and a distinct stat notice.",
    92: "Emilio keeps eating tomatoes while Hodram gives shorter and shorter answers. A trader takes the praise seriously and gives them a seedling. Emilio is still chewing at the end.",
    93: "An unseen animal keeps interrupting Emilio and steals his banana. Emilio pursues it while Hodram notices the unfamiliar seeds. The promise of a meal on Hodram ends the argument.",
}
DECISIONS = {
    91: """
5|||The sailor calls to the person he thinks is captain. The casual form of address suits a stranger calling across the port.
9|||Hodram checks whether he is being addressed. The short reaction leaves the stranger room to explain.
13|||The sailor confirms he means Hodram and asks about belief in miracles. The last question directly frames the two choices.
SC1_B91_CHOICE_112_0|||I do is a natural affirmative answer to the sailor's question. Keep the original first slot.
SC1_B91_CHOICE_112_1|||I don't is the natural negative answer and leads to the distinct second branch. Keep the original second slot.
27|Really? You don't meet many people who believe in miracles these days. You don't sound too steady for a captain.|believe in miracles;too steady for a captain.|The sailor is surprised that a captain believes in miracles and suggests that this makes him seem unreliable. The needling remains his opinion.
31|||Fernando tells him to watch his mouth and identifies Hodram as their admiral. The sharper interruption fits his indignation.
34|||The sailor scoffs and asks if Fernando thinks he is wrong. The short reply keeps the exchange tense.
38|||Fernando begins an angry retort and does not get beyond a single word.
42|Some people don't believe in miracles and still get shipwrecked! You're better off than that!|believe in miracles;still get shipwrecked!;better off than that!|The sailor loudly points out that people who doubt miracles can still be shipwrecked and says Hodram is better off than that.
46|||Fernando's surprised sound gives the sailor room to explain the apparent reversal.
50|Sorry. I got carried away and yelled. I didn't mean to insult your captain.|got carried away and yelled.;insult your captain.|The sailor apologizes for raising his voice and clarifies that he did not mean to speak ill of Hodram.
54|||Fernando marvels at the man's odd behavior. His pause leaves the apology in place.
58|||The sailor explains that he was seeking a captain who believes in miracles. His existing line sets up the gift.
61|||The sailor says he asks whenever a ship comes in and they are his hundredth encounter. Keep the exact number.
65|||Fernando simply asks what the sailor is offering before it is identified.
72|You're giving me something this valuable?|something this valuable?|Hodram is surprised the sailor would part with such a valuable possession. The question retains his uncertainty.
75||someone like you;my lucky charm,;in no shape to sail anymore.|The sailor genuinely wants Hodram to have the charm and explains that he can no longer sail. Keep his wording and the charm's description together through the wrap.
78|I see. In that case, I'll take it. Thank you.|In that case,;Thank you.|Hodram accepts gratefully after hearing why its owner wants to hand it over.
84|||The speakerless notice increases the substituted captain's Luck by one. Keep the name token, the stat, and the exact amount.
87|||The alternate notice increases Fernando's Luck by one. Keep this separate from the captain's version.
94|Stick around an oddball like that and you'll have bad luck. Let's get moving.|you'll have bad luck.;Let's get moving.|Fernando dismisses the stranger as bad luck and wants them to leave at once. His superstition plays against the branch's rejection.
97|||Hodram agrees to move on. The short reply fits Fernando's impatience.
103|||The speakerless notice increases the substituted captain's Spirit by one. Keep the original stat distinct from Luck.
106|||The other notice increases Fernando's Spirit by one. Its speakerless presentation and amount remain the same.
""",
    92: """
5|||Emilio calls the tomatoes delicious and keeps chewing. Retain the sound that sets up the later repetition.
8|||Hodram briefly agrees with Emilio's assessment. The same reply will become less patient.
12|||Emilio says he initially took the tomato for an apple. The statement preserves his own first impression and the next chewing sound.
15|||Hodram agrees again after a pause. The repeated answer is part of the timing.
19|||Emilio again praises the sweetness and taste and keeps eating. The repeated sound is intentional.
22|... (How much is he going to eat before he's had enough?)|had enough?)|Hodram privately wonders how much Emilio will eat before being satisfied. The parentheses keep it separate from his spoken agreement.
26|||The trader laughs and notices their enthusiasm for tomatoes. The existing line fits the interruption.
29|If you like them that much, take this.|If you like them that much,;take this.|The trader decides to give them an object because of their enthusiasm. Emilio asks what it is and the trader identifies it in the next turns.
32|||Emilio asks what the item is. His question lets the trader name the seedling.
36|||The trader identifies it as a tomato seedling. Keep the specific object.
40|You sure?|You sure?|Hodram asks if the trader is sure about giving it to them. He is responding to the gift rather than doubting what it is.
48|||Hodram thanks the trader and accepts the gift. The short reply sounds direct and polite.
52|We lucked out, Admiral. Munch, munch.|We lucked out, Admiral.|Emilio points out their good fortune and keeps chewing while addressing his admiral.
56|||Hodram wonders privately if Emilio is still eating. The short thought pays off the repeated sounds.
""",
    93: """
5|||The first speakerless animal call interrupts Emilio. Preserve the established English sound and the original caption type.
9|||Emilio reacts in surprise and asks what the interruption is. His words precede the audience seeing what happened.
13|||The second call repeats the same sound while the creature persists. Keep the same speakerless presentation.
17|||Emilio tells it to go away. The sharp wording suits his growing annoyance.
21|||The third call remains unchanged and directly precedes Emilio demanding the banana back.
25|||Emilio yells for it to give the banana back. Keep the item implicit until he explains it.
29|||Hodram asks what Emilio is doing before knowing why he is shouting.
33|It stole my banana! I was eating it and that thing snatched it!|It stole my banana!;that thing snatched it!|Emilio blurts out that something stole the banana as he ate. The second sentence makes the theft clear without making him calmer.
37|What do you mean, 'something'?|What do you mean, 'something'?|Hodram asks what creature Emilio is talking about. Quoting his vague description fits the response.
40|That thing right there... It's gone! Hey, get back here!|right there...;It's gone!;get back here!|Emilio starts pointing it out, realizes it got away, and yells after it.
43|||Hodram asks whether Emilio caught the culprit. The direct question brings them back together.
47|||Emilio says it is too fast and throws things, including stones and seeds. His list matters to Hodram's response.
51|Let me see... Hm. Some of these seeds are new to me. Could be a lucky find.|Some of these seeds;Could be a lucky find.|Hodram notices seeds he has never seen and thinks they may turn out to be a good find. Keep his conclusion tentative.
56|||Emilio dismisses the seeds and demands his banana. The contrast with Hodram's curiosity is the joke.
60|||Emilio repeats his demand twice. Keep the repetition as he stays fixated on the banana.
64|...How about we go try something this town's known for?|something this town's known for?|Hodram changes the subject by offering to try a local specialty. His brief pause suits the pivot.
67|||Emilio checks if Hodram is buying. His pause lets his priorities turn quickly.
71|||Hodram confirms it is his treat. The answer leaves space for Emilio's delight.
77|||Emilio cheers as soon as he has the promise of a meal. Keep the one simple reaction.
""",
}

review = checked_text(previous.review, {"len(records) == 76": "len(records) == 58"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
