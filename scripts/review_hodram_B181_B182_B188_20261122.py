"""Review the tomato, bread and tea forecast conversations."""

from scripts import pair_hodram_B181_B200_20261122 as paired
from scripts import review_hodram_B176_B180_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B181_B182_B188_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    181: "The owner is excited about tomatoes and compares their rich color to the passions of her youth. The cook is skeptical but agrees to sell the new dishes. The notice separately forecasts interest in tomatoes in Genoa.",
    182: "Three people share their enthusiasm for home-baked bread. Two encourage the third to try baking and offer to teach her. They decide to buy ingredients. The final notice names the trade good wheat and the city of Amsterdam.",
    188: "Two people enjoy tea and decide who will buy more tomorrow. The shared household language stays in their speech. Their local captions are Woman and Man. The game notice gives a separate tea forecast for Sofala.",
}
DECISIONS = {
    181: """
6|||The owner repeats tomatoes and declares them the future. Her theatrical prediction follows the same comic pattern as the banana forecast.
9|||The cook doubts her prediction because the food is so red. His concern gives her a reason to defend the color itself.
12|That red is the best part! It's the color of passion. Ah, it takes me back to the days when I was young and madly in love.|the best part!;color of passion.;madly in love.|The owner is excited by the red and associates it with the intensity of young love. Her enthusiasm contrasts with the cook's dry reaction.
16|||The cook acknowledges the reminiscence with a dry phrase. The pause preserves his muted response to her enthusiasm.
20|Get some tomato dishes on the menu right away!|tomato dishes;right away!|The owner orders the cook to prepare tomato dishes and offer them for sale immediately. The menu is a natural way to express that purpose in this setting.
23|||The cook simply acknowledges the instruction. It leads straight to the owner's reminder to capitalize on the trend.
27|||The owner says they must not miss the coming tomato craze. The idea that it will be a craze belongs to her prediction.
30|||The cook answers with the same resigned repetition heard in the banana exchange. It keeps his side of the dynamic consistent.
34|||The owner wishes him luck and laughs. The short closing leaves her excitement distinct from the game forecast.
37|||The forecast identifies tomatoes and Genoa and stays tentative. Preserve the commodity and the distinct city.
""",
    182: """
7|||The first woman says that baking your own bread makes the best bread. The established home-baked phrasing sounds like ordinary conversation.
10|||The second says her husband was delighted with hers. The relationship comes directly from her speech, without a change to the role caption.
13|Does bread really taste that much better when you bake it yourself?|taste that much better;you bake it yourself?|The third woman specifically asks whether baking the bread yourself makes it taste better. Restore the comparison that prompts the next answers.
17|Oh, it's the best. Right?|Oh, it's the best.|The first woman insists on the taste and checks her companion's agreement. The quick question hands the next turn over naturally.
21|Oh, yes. The bakery on the corner doesn't come close.|The bakery on the corner;doesn't come close.|The second agrees and compares home baking with the specific neighborhood bakery. Keep the colloquial confidence.
24|||The third considers baking some herself. The tentative thought makes sense after the two women praise the results.
28|||The first encourages her to try it. The existing short answer keeps the other woman's offer separate.
32|||The second offers to show her how to bake it. Her helpful offer answers the hesitation about trying.
36|Would you? I'd love that!|I'd love that!|The third is pleased that someone will teach her. Her warm reply makes it clear what she is accepting.
40|Then let's go get the ingredients right now.|go get the ingredients;right now.|The first proposes getting the ingredients straight away. The eager suggestion takes them from talking about bread to buying supplies.
43|||The second asks what they need. The brief prompt leaves the final response to name the commodity.
47|||Wheat is the ingredient named in the clean source and the trade good in the notice. The existing short answer sets up that linkage.
51|||The notice forecasts a rise in interest in wheat in Amsterdam. Keep that commodity separate from the bread made with it.
""",
    188: """
6|Mmm. This is as good as it gets.|as good as it gets.|The woman expresses how delicious the tea is. Her relaxed praise opens the exchange without adding a brand or flavor.
10|||The man agrees and names tea. The ordinary praise establishes the drink before they discuss its growing popularity.
14|||The woman wonders how something so good took so long to catch on. The existing question is natural and prompts his judgment.
18|||The man agrees and jokes that people have no taste. The dry judgment belongs to him.
22|||The woman realizes they are almost out of tea and asks him to buy more the next day. The polite request and shared household wording match the clean source and the reported example.
26|Sure, I'll pick some up.|I'll pick some up.|The man agrees to do the shopping she just asked about. His brief answer repeats the action without making her ask again.
30|Tea tastes so good. It puts me at ease.|puts me at ease.|The woman returns to praising the taste and says tea makes her feel calm. The ordinary phrasing suits the quiet exchange.
33|||The man jokes that they cannot live without tea. The plural keeps the closing line about both people.
36|||The independent notice forecasts that tea may catch on in Sofala. The city and uncertainty stay explicit.
""",
}
review = checked_text(previous.review, {"len(records) == 108": "len(records) == 32"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::tomatoes-bread-and-tea", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

