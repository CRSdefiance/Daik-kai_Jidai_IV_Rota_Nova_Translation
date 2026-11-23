"""Review the complete trade forecasts from Malacca through Veracruz."""

from scripts import review_hodram_B183_B190_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B191_B199_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    191: "A man with a cough hears about a popular remedy said to contain almonds. Both speakers decide to look for it. The game forecasts interest in Almonds in Malacca.",
    192: "A collector admires a work of art and asks his attendant what it is. Once he learns the name giyaman, he orders the attendant to acquire more. The notice forecasts Glass in Osaka.",
    193: "Two art collectors complain that fashion has made good ceramics harder to find. Another pair overhears and sees a chance to sell them more worthless pieces. The notice forecasts Ceramics in Hamburg.",
    194: "Two people discuss a rumor that an ordinary shop remedy cured an unexplained illness. One is doubtful until he hears its reputation, then both decide to buy some. The notice forecasts Medicine in Havana.",
    195: "A shopkeeper doubts that a particular dye will sell out. An assistant is confident, presses him to buy sooner and finally gets permission. The notice forecasts Dyes in Calicut.",
    196: "One man admits that he has never tried tobacco. The other teases him and offers a chance to try it. The notice forecasts Tobacco in Istanbul.",
    197: "Two diners enjoy an unusually flavorful meal. Their friend names the chili peppers, reassures them about the price and offers to show them how to cook with them.",
    198: "Two men discuss sake and decide to have a drink. Julio overhears and jumps to the conclusion that sake must be the legendary drink. The notice forecasts Sake in Hangzhou.",
    199: "Two diners smell a tavern's cheese specialty, order it despite their doubts and decide to tell everybody after tasting it. The game forecasts Cheese in Veracruz.",
}
DECISIONS = {
    191: """
6|||The man says he has been coughing badly lately. Keep the audible cough as part of his opening.
10|||The other speaker asks if he is all right. The short concerned question lets the man answer for himself.
14|Yeah, I'm all right. It's just been bothering me. Cough, cough...|It's just been bothering me.|The man says he is managing despite his discomfort. Keep the cough and the broad complaint without supplying a new symptom.
17|||The other speaker recalls seeing many people coughing lately. That observation leads to speculation.
20|||The man wonders whether an illness is going around. Leave it as his question.
24|||The other speaker says he heard about a possible remedy. The line keeps the claim secondhand.
27|||The man reacts with hope and asks the name of the remedy. The cough interrupts his eagerness.
30|||The speaker remembers almonds as an ingredient despite forgetting the name. The uncertainty stays explicit.
33|||The man repeats almonds in surprise. This prompts the other speaker to explain why that detail stuck.
37|||The speaker says he had the same reaction to almonds in medicine. His own surprise explains his memory of that ingredient.
41|||The man asks whether the remedy works and coughs. Keep the question open.
45|They say it works like a charm. It's selling like crazy.|They say;selling like crazy.|The speaker repeats a report about effectiveness and popularity. Both claims belong to the conversation in the game.
48|||The man says he will look for some. The decision follows what he was told.
52|||The other speaker offers to look too. The brief offer follows his friend's decision naturally.
56|||The man thanks him and coughs again. The sound closes the exchange in his voice.
60|||The notice forecasts interest in Almonds in Malacca. It makes no additional claim about the remedy.
""",
    192: """
6|||The collector declares the item a work of art. His exclamation starts the inquiry.
10|||The attendant agrees respectfully. Keep the deferential turn distinct from the collector's praise.
14|Something this fine must have come from a well-known craftsman.|Something this fine;well-known craftsman.|The collector assumes the workmanship must be by a renowned maker. His conclusion stays a guess.
18|||The attendant concurs without naming a maker. The measured answer leaves the question open.
22|||The collector is surprised to learn the object is fashionable. He then asks what to call it.
26|||He asks for its name. Keep the direct question before the attendant introduces the term.
30|Giyaman, my lord. It's glass.|Giyaman, my lord.;It's glass.|The attendant gives the Japanese loanword and immediately identifies the material in English. Preserve his deferential address.
34|||The collector tries the unfamiliar term aloud. The short response keeps giyaman consistent.
38|||He decides to add the piece to his collection and orders the attendant to bring more from the town. Keep the extravagant scope of the order.
41|||The attendant accepts promptly. The short formal answer confirms compliance before the notice.
45|||The notice uses the registered commodity name Glass and the city Osaka. Its forecast stays tentative.
""",
    193: """
6|||The first collector says he finally acquired the piece recently. His indirect reference prompts the other collector to name it.
9|||The second identifies ceramics as the subject. The brief question comes before the quality judgment.
13|||The first confirms the purchase and says it lived up to his expectations. His satisfaction sets up the request to see it.
16|||The other collector is pleased and asks to see it. Keep his courtesy among peers.
19|||The buyer welcomes the visit and asks his acquaintance to come to his home. The invitation responds directly to the request.
22|||The visitor says widespread collecting makes a good piece harder to find. Keep the link between the fashion and scarcity.
26|||The owner blames buyers who follow the fashion and fail to understand value. It remains his judgment before the eavesdroppers contradict it.
30|||The other collector calls the trend a nuisance. The short complaint closes their part of the exchange.
34|||The buyer agrees. The separate assent leaves a clear break before another pair speaks.
38|||The first eavesdropper asks his companion to look at the men. The instruction shifts the viewpoint.
42|||The companion checks which pair he means. His curiosity lets the first man explain.
46|I sold them some worthless ceramics the other day. You wouldn't believe what they paid!|some worthless ceramics;what they paid!|The seller boasts that these very buyers paid an absurd price for worthless ceramics. His first-person claim reveals the joke about their judgment.
49|Now those are customers worth keeping! I'm short on cash. Want to go talk to them?|customers worth keeping!;go talk to them?|The companion recognizes the opportunity and suggests speaking to them because he is short on money. His register contrasts with the polite collectors.
53|||The seller thinks the suggestion is a good one. The quick assent gives his companion room to lead.
57|||The companion treats the plan as decided and says to go. The short turn moves them toward the buyers.
61|||The seller calls politely to get a buyer's attention. The switch in register is part of the joke.
65|||The notice forecasts Ceramics in Hamburg. Keep the commodity distinct from the men's appraisal of any individual piece.
""",
    194: """
24|||The first speaker asks whether the other has heard the news. The setup precedes naming the subject.
28|||The second asks what news. His short question gives the first speaker the next turn.
32|||The first identifies the owner of the mansion. The source supplies no personal name or formal title.
36|||The second asks whether the news concerns the man's mysterious illness. The question locates their shared knowledge.
40|||The first confirms the subject. Keep it separate from his new information about the outcome.
44|||The second says everybody knows the earlier story. His impatience invites the first speaker to explain what is new.
48|||The first asks whether he has heard what happened afterward. This prepares the claim about the remedy.
52|||The second repeats the question in surprise. The brief echo leaves the next turn to the person with the rumor.
56|They say an ordinary remedy from a shop cleared it up just like that.|an ordinary remedy;just like that.|The first speaker repeats a rumor that ordinary shop medicine quickly cured the owner's unexplained illness. The claim remains attributed.
59|Something from a shop cured an illness nobody could explain?|Something from a shop;cured an illness|The second speaker doubts that a shop remedy could cure such an illness. The question keeps the rumor under scrutiny.
63|||The first speaker agrees and calls it amazing. The short tag invites a reaction.
67|||The other speaker still asks whether it is true. Keep the uncertainty before the first speaker describes the rumor's reputation.
71|Supposedly. It's even got a reputation as a cure-all.|reputation as a cure-all.|The first speaker only says the story seems true and reports the medicine's reputation. Cure-all is what people say in the exchange.
74|||The other speaker is impressed enough to want some. His interest follows the reported reputation.
77|||The first suggests going to buy some. The simple question lets his companion agree.
81|||The second agrees to leave at once. Keep the brisk closing before the forecast.
85|||The notice forecasts interest in Medicine in Havana. It does not certify the rumored effects.
""",
    195: """
53|||The first speaker says only that dye will produce the color. The certainty is about the color rather than the forecast.
56|||The assistant agrees and says competitors may buy up the supply. The turn establishes the reason to act now.
60|||The first speaker hesitates. The single pause leaves the assistant room to press the point.
64|||The assistant warns that waiting until the dye is gone will be too late. The short question and consequence suit the disagreement.
68|We don't have to rush. It can't sell out that fast, can it?|sell out that fast, can it?|The first speaker doubts supplies will disappear right away. The tag leaves room for the assistant to contradict him.
72|||The assistant is confident the popular dye will sell out. The short answer suits the speaker's impatience.
76|||The first speaker doubts the forecast. The recurring short question gets a quick answer.
80|||The assistant confirms the prediction again. The separate emphatic assent keeps the exchange moving.
84|||The first speaker relents and leaves the purchase to the assistant. Keep the responsibility clear.
88|||The assistant tells the first speaker not to sulk and predicts a reliable profit from securing the color. The close working relationship stays implicit.
92|||The first speaker repeats the same doubts after giving permission. Keep the recurring question before the assistant's last insistence.
96|||The assistant reiterates the claim with some exasperation. The voice closes the joke.
100|||The notice forecasts Dyes in Calicut. The commodity and tentative forecast stay intact.
""",
    196: """
6|||The first man asks whether the other has ever smoked tobacco. Keep the question plain.
10|||The other understands the reason for the question and asks whether the first has tried it. The surprise prepares the admission.
13|||The first says he has not had the opportunity. The plain answer leaves the second man room to tease him.
16|||The second claims that tobacco is so fashionable that his companion might be the only one in town who has not tried it. Preserve it as his exaggeration.
20|||The first man hesitates and says he would like to try it. The existing stammer matches his discomfort.
23|||The second offers to let him try some and asks him to follow. Keep the action within the scene.
26|||The first agrees with a stammer. The short final reaction retains his uncertainty.
30|||The game forecasts Tobacco in Istanbul. The notice reports possible demand.
""",
    197: """
6|||The first guest praises the meal and says she has never had anything like it. The enthusiastic response starts the conversation.
10|||The second agrees and comments on the kick in the food. The phrase naturally describes the sensation before the spice is named.
14|||The first asks how the cook gets such good flavor. The plain question invites her to reveal the secret.
17|||The cook laughs softly and offers to show the secret. The short turn leaves the first guest briefly puzzled.
21|||The first guest reacts with curiosity. The separate beat prepares the identification of the spice.
25|Chili peppers. They're a kind of spice, or so I'm told. They go beautifully with the food we have around here.|a kind of spice,;the food we have|The cook names chili peppers, qualifies the category and explains how well they go with local ingredients. Keep the distinctly local observation.
29|||The first guest assumes the peppers might be expensive. Her polite question follows the praise.
33|||The cook says they are not particularly expensive. The brief reassurance gives the guest room to consider using them.
37|||The first guest is relieved and considers using them for dinner. Keep the tentative plan.
40|||The second guest also wants to try cooking with them. Her wish prompts the lesson.
44|Would you like me to show you how to use them right now?|show you how;right now?|Their friend offers to teach them immediately. Restoring what she will show them makes the offer self-contained in the conversation.
47|||The first guest is delighted by the offer. The short question preserves her surprise before the thanks.
51|||The second thanks their friend in a polite register. Keep her separate response.
55|Of course. We're friends.|We're friends.|The cook says friendship is reason enough to share her knowledge. This relationship is explicit in the source.
59|||The notice forecasts Chili Peppers in Seoul. It leaves the trend tentative after the enthusiastic meal.
""",
    198: """
6|||The first man says he tried sake recently. The established commodity name starts the exchange.
10|||The other says he tried it too. His quick answer leads to the shared verdict.
14|||The first says he liked it and checks the other man's opinion. The short tag suits the friendly tone.
18|||The other says he heard it is made from rice. The source presents that detail as something he was told.
22|||The first expresses surprise that a drink can be made from rice. Keep his reaction in the exchange.
26|||Talking about sake makes the other speaker want a drink. The plain invitation asks whether they should go now.
30|||The first man agrees quickly. His enthusiasm lets the other man suggest leaving straightaway.
34|||The second says to get going once the decision is made. The existing farewell moves them out of the exchange.
46|W-what?! That has to be the legendary drink! Did you hear that, Admiral FI?!|the legendary drink!;Admiral FI?!|Julio is startled and jumps to the conclusion that he has heard about the legendary drink. Preserve his stammer and the original controlled address.
49|||Julio says he cannot stand around and rushes to buy sake. The urgency follows his own conclusion.
56|||The notice forecasts Sake in Hangzhou. It does not identify the drink as the legendary one.
""",
    199: """
6|||The first diner notices a good smell and asks whether his companion smells it too. The tag opens the shared reaction.
9|||The second sniffs and agrees. Keep the physical sound and brief answer.
13|||The first asks the tavern worker about the smell. Barkeep conveys the role without turning the familiar address into a personal relationship.
17|That's our specialty! Plenty of cheese in it. Tastes great!|Plenty of cheese in it.;Tastes great!|The barkeep identifies the dish as the tavern's specialty, names the plentiful cheese and praises the flavor. The original does not name a specific recipe.
20|||The second diner doubts whether it is really good. The brief question lets the barkeep defend it.
24|Of course it is! Do you even have to ask?|Do you even have to ask?|The barkeep treats the question as needlessly obvious. His proud reply precedes them ordering a plate.
28|||The first diner orders one for the pair. The short request preserves the shared order.
32|||The barkeep acknowledges the order and says the wait will be brief. His promise leads to the fast delivery.
35|||The barkeep presents the dish. Keep it as its own turn after the promise to fetch it.
39|||The first diner is surprised by how quickly it arrived. The short comment gives the barkeep room to encourage them to taste it.
43|Trust me. Just take a bite.|Just take a bite.|The barkeep asks them to take his word for it long enough to taste the dish. The plain idiom fits his confident delivery.
46|||The first diner agrees to try it. The short assent sets up the two separate eating sounds.
50|||The first diner makes an audible chewing sound. Keep this turn distinct from the second diner's.
54|||The other diner also chews. The repeated sound gives them both time to taste before the verdict.
58|Whoa, that's good!|Whoa, that's good!|The first diner exclaims that the dish is delicious. The interjection carries the drawn-out Japanese surprise.
62|This is fantastic!|This is fantastic!|The other diner agrees emphatically. The short turn adds his own enthusiasm after the first reaction.
65|||The barkeep is pleased to be proven right. His brief reply echoes his earlier confidence.
69|||The first diner wants to tell everyone. His colloquial excitement gives the second diner room to predict a hit.
73|||The second praises the dish directly to the barkeep and predicts it will become popular. Keep that as his own prediction.
77|||The game forecasts Cheese in Veracruz. The notice names the commodity and the town after the exchange.
""",
}
review = checked_text(previous.review, {"len(records) == 88": "len(records) == 128"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::trade-forecast-exchanges", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

