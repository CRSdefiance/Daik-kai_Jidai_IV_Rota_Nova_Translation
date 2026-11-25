"""Review Cristina's dance, Samwell's introduction and the missing ship."""

from scripts import pair_hodram_B161_B170_20261122 as paired
from scripts import review_hodram_B159_B160_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B161_B163_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    161: "Hodram and Cristina have had a few drinks. Cristina hears a favorite tune and gets up to dance. The patrons applaud, and Hodram tells her he sees why Mivor is taken with her.",
    162: "A young vendor, Samwell, asks to join the crew. His banter gets him nowhere with Hodram, and he briefly storms off. He comes back with something he cooked and reads Hodram's expression before the captain will admit it is delicious.",
    163: "The crew reports the ship missing. At the port a witness says he saw a lanky man board and set sail alone. The next branches check whether the ship has returned; the cause remains unidentified at this point.",
}
DECISIONS = {
    161: """
5|||Hodram says he has had more to drink than in a long time. The ordinary admission sets a relaxed tone before Cristina hears the tune.
9|||Cristina says she has had quite a bit too, then notices something. The trailing sound leaves room for her reaction to the music.
14|||Hodram gives the music a brief, appreciative comment. It allows Cristina to recognize the specific tune in the next turn.
18|||Cristina recognizes the tune and politely excuses herself. The pause lets her decision to get up happen in the scene.
21|||Hodram barely reacts as she rises. The questioning beat suits a person waiting to see what happens.
26|||The first patron marvels at Cristina, using the existing embedded caption. This turn starts the crowd response without identifying the patron.
29|||The second patron admires her looks and skill. Keep the praise in the separate patron's voice and caption.
34|||Hodram watches without speaking. The pause belongs between the crowd's separate comments and its collective cheer.
38|||The patrons shout Bravo with an exaggerated final call. Keep the collective role and the emphatic sound of the last word.
41|||The clapping reads as a separate sound effect. Preserve the lack of an assigned speaker.
45|I couldn't help myself. I love that song.|couldn't help myself.;love that song.|Cristina explains that the tune moved her to dance. The point is affection for the tune, and the complete sentences still sound spontaneous.
48|I'd figured you were all about sword fighting...|all about sword fighting...|Hodram voices his own assumption about Cristina. It leaves her able to ask whether she surprised him.
52|I surprised you, huh?|I surprised you, huh?|Cristina teases him about that assumption. The short tag stays with her question.
56|A little. You danced beautifully. No wonder Mivor's so taken with you.|You danced beautifully.;so taken with you.|Hodram admits he was surprised, praises her dancing, and mentions Mivor's evident affection. Leave their relationship unstated.
""",
    162: """
6|It's hot here...|It's hot here...|Hodram notices the heat before the vendor speaks. Keep his brief reaction before the interruption.
11|Come take a look! See anything you like? I've got nothing but the best!|See anything you like?;nothing but the best!|Samwell calls to prospective buyers and praises his wares. The fast pitch starts his outgoing performance.
14|||Samwell notices strangers and asks if they are travelers. The friendly surprise leads directly to his request.
17|||Samwell immediately asks to come along, tired of seeing elephants and eager to see other countries. His sudden enthusiasm keeps the specific joke.
20|||Hodram asks what Samwell can do. The direct reply puts practical qualifications before the request.
24|I can cook! And I'm good at it!|I'm good at it!|Samwell boasts about cooking. The cheerful follow-up carries his pride without making him claim professional training.
28|Any experience at sea?|experience at sea?|Hodram checks for experience aboard a ship. The compact question makes the next blunt answer funny.
32|||Samwell proudly says he has none. The single exclamation keeps the comic timing.
36|||Hodram hesitates and tells him that makes him hard to rely on. The judgment belongs to the captain.
40|||Samwell points out that everyone has a first time. The familiar idiom preserves his argument for being given a chance.
44|||Hodram warns him about back talk. Keep the short reprimand that Samwell immediately disputes.
48|||Samwell questions whether that really counts as back talk. The tag and trailing pause keep his cheekiness.
51|Anyway, I don't need a kid I'll have to look after.|have to look after.|Hodram dismisses him as a kid who would need looking after. Leave the label in Hodram's voice and keep the cause of Samwell's objection.
55|Pfft! It wasn't that long ago you were a kid yourself!|a kid yourself!|Samwell reminds Hodram that he wasn't always an adult. The jibe directly answers the way Hodram just described him.
59|||Hodram reacts to the retort with a short challenge. The pause makes it a response to Samwell's nerve.
63|Fine! I don't like you. Bye!|I don't like you.|Samwell declares he has had enough and says he dislikes Hodram. The childish farewell sets up the quick reversal.
66|...What a strange kid. Back to the ship, I guess.|What a strange kid.;Back to the ship,|Hodram calls him odd and decides to leave. The dry aside leaves Samwell offscreen long enough to return out of breath.
71|Hah, hah... W-wait! Please? I didn't mean it. I do like you!|I didn't mean it.;I do like you!|Samwell runs back, begs him to wait, and takes back what he just said. The panting and stammer are part of the abrupt change of mind.
75|||Hodram lets the apology hang without answering. Keep the silence before Samwell tries a different approach.
79|I cooked this... How about you try it before you decide?|before you decide?|Samwell offers his own cooking as evidence. The pause keeps his change from pleading to bargaining audible.
82|I can at least give it a taste...|give it a taste...|Hodram agrees only to taste it. The trailing words give the game time to show his reaction before he speaks again.
85|||Hodram gives a brief, impressed reaction. Keep the hint as Samwell studies his face.
89|Well? Is it still a no?|Is it still a no?|Samwell asks for Hodram's verdict and is prepared for another refusal. The question shows what is at stake in the tasting.
93|||Hodram remains silent. Samwell's decision to read his reaction depends on the pause.
97|||Samwell guesses that Hodram's face means yes and celebrates. The answer is his interpretation before the captain agrees.
100|||Hodram points out he has said nothing. The understated objection makes Samwell's victory speech funnier.
104|I'm Samwell! I'm pretty handy. I can do all sorts of things. Glad to meet you!|I'm pretty handy.;Glad to meet you!|Samwell gives his approved given name and boasts that he is good with his hands and versatile. His eager introduction keeps the encounter moving even without an explicit yes.
108|||Hodram's terse reaction shows that Samwell leaves him at a loss. It precedes the separate admission about the food.
112|||Hodram privately admits the food is delicious. Retain the inner thought so Samwell's conclusion still runs ahead of a spoken answer.
""",
    163: """
5|Admiral! It's terrible! The ship... the ship is gone!|the ship is gone!|The sailor repeats ship in alarm as he delivers the news. His urgency starts the whole exchange.
8|||Hodram repeats the missing ship report in disbelief. His hesitation allows the officers to propose their own reactions.
12|||Gerhard refuses to believe a ship can simply vanish. His controlled denial lets Charles object in his own terms.
24|That defies science! It's physically impossible!|That defies science!;It's physically impossible!|Charles says both scientific explanation and physical possibility fail him. Keep the emphatic repeat as his own character beat.
30|||The sailor insists the news is true and urges them to the port office immediately. Both the destination and urgency matter.
33|||Hodram's silent exclamation marks the cut to the port. Preserve the independent reaction.
37|Wh-what do we do?!|Wh-what do we do?!|The sailor's stammer shows his panic after they arrive. He is looking to the crew for a response.
41|||Gerhard sees that the ship is gone without a trace. Keep his switchover from disbelief to the sight at the port.
53|||Charles still has no scientific explanation and is openly baffled. The repetition suits his concern with how a ship could disappear.
59|||The dock worker calls for the admiral and tries to get his attention. His interruption sets up the eyewitness account.
63|||The dock worker says he saw a lanky man working at the ship by himself that morning. The trailing end lets him deliver what happened next separately.
67|||The witness says the man sailed away. The short emphatic line supplies the answer the crew was trying to explain.
71|||Gerhard demands to know why the witness stood by and let him go. The accusation sounds sharper now that there was a way to prevent it.
82|||Charles gives a mild, dry appraisal of the problem. Keep his understatement after Gerhard's outburst.
88|||The dock worker says he assumed the lone man was inspecting the ship and never expected him to sail. His explanation preserves the limits of what he knew.
92|He sailed all by himself... Whoever he is, he's got nerve.|all by himself...;he's got nerve.|Hodram calls the man's solo sailing bold and keeps him unidentified. The remark leads into the search, before the man returns.
95|||Gerhard proposes returning to town and asking around for the man. Preserve his respectful runtime address to Hodram and both steps in the search.
""",
}
review = checked_text(previous.review, {"len(records) == 130": "len(records) == 60"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::dance-cooking-and-the-missing-ship", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

