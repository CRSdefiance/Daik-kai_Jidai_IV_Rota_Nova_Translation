"""Review all six offers and refusals in the shady merchant's bargain."""

from scripts import review_hodram_B191_B199_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B200_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    200: "A shady merchant asks 200,000 coins for an item, then drops the price after repeated refusals. The crew whispers advice between offers. Each Buy branch ends the negotiation. Passing on the 30,000-coin offer sends the merchant away. The first, most expensive purchase has a separate Charm notice.",
}
DECISIONS = {
    200: """
5|You look like you've got money. Hee hee hee hee hee!|you've got money.|The merchant sizes up the customer's wealth and laughs. Keep the unsettling laugh that recurs when he names prices.
8|||Hodram remains silent after the merchant approaches. The pause gives the man space to pitch his item.
12|I've got something good for you. How about 200,000 coins? Hee hee hee hee hee!|How about 200,000 coins?|The merchant offers an unspecified item for 200,000 coins. The sales pitch keeps the amount, anonymity of the item and laugh.
24|Hold on. You're not trying to gouge us, are you?|gouge us, are you?|Fernando challenges the inflated price. The tag keeps it a suspicious question before the player chooses.
SC1_B200_CHOICE_218_0|||Buy accepts the 200,000-coin offer. The short caption matches the rest of the negotiation.
SC1_B200_CHOICE_218_1|||Pass declines the opening offer. It leaves room for the counteroffer that follows.
42|You're a big spender! This'll come in handy, though.|a big spender!;come in handy, though.|The merchant praises the buyer's spending and promises the item will be useful. The playful praise suits the expensive outcome.
45|||The independent panel names FI and raises Charm by exactly one as a consequence of the opening-price purchase. Keep the controlled name and stat label.
62|||The merchant responds to refusal by halving the price to 100,000 coins. His laugh still belongs to the same sales pitch.
74|(Admiral, he cut the price in half right away. He must've marked it way up. You could get him down at least twice more.)|cut the price in half;at least twice more.)|Carlo infers a large markup from the immediate drop and advises holding out for at least two more reductions. Keep the advice private and the numerical point explicit.
SC1_B200_CHOICE_582_0|||Buy accepts the 100,000-coin offer. The caption remains consistent and keeps the correct branch.
SC1_B200_CHOICE_582_1|||Pass declines the 100,000-coin offer without ending the bargain. The next price is still available.
92|Hee hee hee! You're sharp. This'll come in handy.|You're sharp.;come in handy.|The merchant approves of the deal and promises that the item will be useful. Keep his laughter in the purchase response.
107|||The next offer is 70,000 coins. Keep the smaller price and the merchant's laugh.
118|||Fernando says he would haggle once more. The aside gives advice without making the decision for the player.
SC1_B200_CHOICE_832_0|||Buy accepts the 70,000-coin offer. Keep the same affirmative command and branch.
SC1_B200_CHOICE_832_1|||Pass declines the 70,000-coin offer and leads to another price.
136|||The merchant hands over the item and says it will be useful. The repeated laugh keeps him recognizable even when his price falls.
152|||The merchant accuses the customer of being greedier than he expected and offers 50,000 coins. The judgment belongs to his bargaining voice.
170|||Julio quietly says he would hold out once more. Preserve the option to bargain further.
178|||Yifa privately encourages more bargaining. Her excited language differs from Julio's advice in the alternate turn.
SC1_B200_CHOICE_1156_0|||Buy accepts the 50,000-coin offer. The wording keeps the menu consistent.
SC1_B200_CHOICE_1156_1|||Pass turns down the 50,000-coin offer but still permits a counteroffer.
197|You're a pretty good bargainer. Here you go.|a pretty good bargainer.;Here you go.|The merchant concedes the player's skill and hands over the item. The more casual wording keeps him in the same voice.
212|||The merchant offers 40,000 coins after a long pause. The short laugh has less confidence than the opening one.
223|(This seems like the time to buy.)|the time to buy.)|Carlo suggests taking the current price. The tentative aside contrasts with his earlier encouragement to haggle further.
SC1_B200_CHOICE_1370_0|||Buy accepts the 40,000-coin offer. Preserve the same short instruction.
SC1_B200_CHOICE_1370_1|||Pass keeps the bargain open through the next offer. It retains its specific refusal branch.
242|I was starting to think you wouldn't buy it. Here you go.|you wouldn't buy it.;Here you go.|The merchant thought the customer might never buy and hands over the item. His relief marks how long the negotiation has lasted.
257|||The merchant has stopped laughing and pleads for the sale at 30,000 coins. The short wording carries the changed leverage.
268|||Julio doubts the seller will lower the price any further. Keep it as whispered advice before the final choice.
SC1_B200_CHOICE_1588_0|||Buy accepts the last offer of 30,000 coins. The same caption remains clear in this final menu.
SC1_B200_CHOICE_1588_1|||Pass rejects the last offer. This time the merchant ends the bargain.
287|||The merchant complains that he practically gave the item away and tells the buyer to look after it. The tag carries his grudging farewell.
302|Hmph! You don't know a good deal when you see one!|a good deal when you see one!|The merchant blames the customer for failing to see the value. The sales idiom fits his frustration at a final refusal.
306|Forget it. I'll sell it to somebody else!|sell it to somebody else!|The merchant ends the negotiation and says he will sell to another person. The brisk dismissal confirms there is no lower offer.
""",
}
review = checked_text(previous.review, {"len(records) == 128": "len(records) == 36"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::six-bargaining-offers", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

