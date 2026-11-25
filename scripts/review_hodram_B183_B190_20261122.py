"""Review seven complete tavern, shop and street forecasts."""

from scripts import review_hodram_B181_B182_B188_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B183_B190_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    183: "A sailor teases a patron about his drink and talks him into trying wine. The patron is immediately converted. The forecast concerns wine in Sao Jorge.",
    184: "Two acquaintances notice somebody's scent and want to find out what it is before it becomes fashionable. The notice forecasts demand for Fragrances in Lisbon.",
    185: "Three acquaintances admire a ruby necklace and sigh at the idea of receiving such a gift. The notice forecasts demand for Rubies in Athens.",
    186: "Two acquaintances discuss a princess's engagement and decide to find out what gemstone she will wear before it becomes popular in London.",
    187: "Three collectors argue over paintings and each buys a different piece. A sailor asks what happened. The shopkeeper explains the fad and makes a private joke about the buyers' taste.",
    189: "A cold snap makes a woman want a fur coat. Her companion says the weather has driven up the price of furs, and the notice predicts demand in Stockholm.",
    190: "The owner tells a skeptical cook to make the dish sweeter. She predicts a fashion for sweets, which the game reports as a possibility in Alexandria.",
}
DECISIONS = {
    183: """
6|||The sailor asks why the patron is still drinking the same stuff. The familiar challenge starts their rivalry over taste.
9|||The patron asks what is wrong with his choice. Keep the sharp short answer before the sailor clarifies.
13|Nothing wrong with it. But everybody's drinking wine now. Wine!|everybody's drinking wine now.|The sailor says the drink is fine but touts wine as the current fashion. Keep the emphatic repetition as his sales pitch.
16|||The patron echoes wine and asks what it tastes like. His short questions show he is listening despite his first objection.
20|||The sailor immediately praises it as the best. His unqualified answer prompts the patron to check.
24|||The patron asks if it is really that good. The quick echo makes the sailor's next claim sound extravagant.
28|||The sailor says wine is all anyone needs. Keep his confident rhetorical question before the patron orders.
31|||The patron decides to try and asks the barkeep for one glass. The direct order supplies the payoff to his hesitation.
35|||The barkeep acknowledges the order. The ordinary tavern reply gives the patron the next beat.
39|||The repeated gulping represents the patron drinking. Keep the sound in his turn so the sailor can ask for a verdict.
43|||The sailor asks for a verdict in one word. The timing lets the patron's enthusiasm answer it.
47|||The patron praises the taste and calls for another. His immediate second order is the conversion the sailor wanted.
50|||The sailor places an order for himself. The terse turn shows he has talked himself back into a drink too.
54|||The forecast preserves wine, Sao Jorge and the tentative result apart from the men's enthusiasm.
""",
    184: """
5|||The first speaker asks about a lovely scent somebody wore. The existing wording leaves the person's gender open.
9|||The second realized the same thing and checks whether the first noticed. Keep the quick recognition.
13|I wonder what that scent was.|what that scent was.|The first speaker wonders what the scent was. The complete thought sets up the second speaker's prediction.
17|I couldn't say, but I bet it'll catch on.|it'll catch on.|The second speaker cannot identify it, yet expects others to want it. Preserve her uncertainty about the scent and confidence about fashion.
20|||The first speaker wants to obtain it before other people do. The deliberately urgent tone contrasts with the small mystery.
24|I'm sure you're right.|you're right.|The second agrees with her friend's urgency. The reply fits their courteous register.
28|Why don't we just come out and ask next time we see them?|come out and ask;next time we see them?|The first proposes asking directly at the next meeting. Keep the person's gender open and the slight hesitation about asking.
31|A splendid idea. Let's do that.|A splendid idea.;Let's do that.|The second agrees in a polite but conversational register. The assent closes the plan before the parting greetings.
34|||The first politely takes leave. Preserve the friendly prospect of a future meeting without naming a time.
38|||The second returns the farewell. Keep the separate acknowledgment.
73|||The notice predicts interest in the registered trade good Fragrances in Lisbon. Leave the forecast tentative.
""",
    185: """
6|||The first speaker asks whether the others saw the vivid red ruby. The existing question identifies the object before anyone mentions the necklace.
9|||The second confirms she saw it and calls it magnificent. The formal praise fits the company's enthusiasm.
13|||The third asks what they are discussing. Keep the invitation to identify the jewelry.
17|||The first identifies the necklace that the unnamed lady wore. Retain the reference to the same woman without giving her a title.
20|Oh, that one. What a big, beautiful stone!|big, beautiful stone!|The third recognizes the necklace and comments on the stone's size and beauty. Both qualities motivate the wish that follows.
23|||The second would love to receive such a gift once in her life. The wish keeps the source's courteous address and sense of longing.
27|Wouldn't that be lovely? (Sighs)|Wouldn't that be lovely?|The first agrees with the wish and sighs. The quick question keeps her reaction distinct before the other two follow suit.
31|||The second sighs in her own turn. Keep her response separate for the scene's timing.
35|||The third sighs last. The repeat completes the joke before the notice.
39|||The notice makes a tentative forecast for Rubies in Athens. The example necklace stays separate from the trade good.
""",
    186: """
5|||The first speaker reports that the princess is getting engaged. Keep the source title and the excited opening.
8|||The second has heard that it is the duke's son and asks for confirmation. The tag preserves that this is gossip.
11|They say her engagement ring cost enough to buy a mountain.|her engagement ring;to buy a mountain.|The quoted price is deliberately extravagant hearsay. Keep the mountain comparison and the engagement ring.
14|That's a duke for you... I wonder when we'll see the princess wearing it.|a duke for you...;the princess wearing it.|The second recognizes the extravagant price as fitting a duke and wonders when she will see the princess in the jewelry.
17|It won't be long. Once she's seen wearing it, more ladies will want a gem like that.|seen wearing it,;a gem like that.|The first expects to see the princess wear it soon and predicts demand for that kind of gemstone. Keep the fashionable object distinct from the engagement ring itself.
21|||The second realizes the opportunity will pass as soon as it comes into fashion. Her questions express urgency and ignorance of the gem's identity.
25|I haven't heard. We'd better go ask!|go ask!|The first does not know the answer and proposes finding out at once. Her hurry ends the gossip.
62|||The notice forecasts Gemstones in London and leaves the result tentative.
""",
    187: """
6|||The sailor reacts to the dispute he has just noticed. The questioning sound keeps him an observer.
10|||The first collector declares that a piece is wonderful. The short praise sets off the disagreement.
14|||The second questions the first collector's judgment. His hesitation gives the other man time to make a stronger claim.
18|||The first expects the artist to be remembered by later generations. Keep the prediction as his own judgment.
21|||The second offers a noncommittal acknowledgment. He has yet to point out the piece he prefers.
25|||The first recommends buying the artist's work while they can. His confidence motivates the disagreement.
28|I'd say this one's better!|this one's better!|The second points to his own preference. His voiced opinion answers the recommendation without making it an objective fact.
32|||The first concedes the other work is decent but sticks with his original artist. Preserve that competition.
35|What are you two talking about? The one over there is clearly the best.|talking about?;clearly the best.|The third cuts in and points to a different work. He comes across as certain that both others are wrong.
39|||The first collector commits to buying the painting he backed. Keep his persistence through the interruption.
42|||The second orders a piece by the painter he prefers. Keep his choice distinct from the first man's.
45|||The third buys his favorite. The short order lets the three buyers leave after making individual choices.
49|||The shopkeeper thanks the customers. The polite formula comes before the door slam and his private complaint.
53|||The speakerless door slam separates the sale from the shopkeeper's aside. Keep the effect as its own panel.
57|||The shopkeeper is relieved that they are gone and complains that they argue in his store every time. The existing line makes his frustration clear.
61|What was all that about?|What was all that about?|The sailor asks the shopkeeper to explain the quarrel. The plain question fits his position as a bystander.
65|||The shopkeeper calls it a rich man's pastime. The phrase belongs to his lightly mocking view.
69|||The sailor repeats the phrase in surprise. It gives the shopkeeper the turn to explain the fad.
73|||The shopkeeper explains that collecting paintings is fashionable. Keep the practice concrete instead of replacing it with a vague reference to taste.
76|Huh. A fancy hobby.|A fancy hobby.|The sailor calls it a refined pastime. The plain-spoken reaction gives the shopkeeper room for a sharper opinion.
80|Well, precious few of them have an eye for art.|have an eye for art.|The shopkeeper quietly undermines the pretensions of the buyers. His joke is about their judgment.
83|||The sailor laughs and comments on how blunt the shopkeeper is. The tag keeps their friendly complicity.
87|Whoops. Just between us, please.|Just between us, please.|The shopkeeper catches himself and asks the sailor to keep the comment private. His sudden discretion follows the laugh.
91|||The sailor promises to keep it quiet. The short agreement closes the shop exchange.
95|||The game forecasts the trade good Artwork in Basra. Earlier discussion stays specifically about paintings.
""",
    189: """
6|||The woman says the cold is penetrating. The existing phrasing sets the conditions for her request.
10|||The man agrees that it has not been so cold in some time. Keep his report grounded in how the weather feels to him.
13|||The woman wants a fur coat and says she feels she might freeze. The exaggeration explains why she wants it promptly.
16|||The man reports that furs are selling well and becoming more expensive. Keep both effects and the hearsay.
19|||The woman acknowledges that she heard the same thing and shivers. The brief interjection keeps her discomfort present.
22|||The man hopes it warms up soon. His wish is practical given what he just said about prices.
26|Me too. But as long as it's this cold, I want a fur coat.|as long as it's this cold,;a fur coat.|The woman agrees about the weather and returns to wanting a fur coat while it stays cold. Preserve her practical insistence.
29|||The notice forecasts Furs in Stockholm. It leaves the trend tentative even though the speakers have heard about increased sales.
""",
    190: """
5|||The owner tastes something and decides the missing element is sweetness. Her quick realization starts the exchange.
9|||The cook repeats what she wants. The short question sets up her explanation of what customers expect.
13|||The owner describes the dish as too mild and exaggerates the sound of sweet. Keep the repeated emphasis as part of her theatrical manner.
16|||The cook asks whether she really thinks so. His short reply suits the skeptical voice already heard in the other food forecasts.
20|Of course it does. I said so!|Of course it does.;I said so!|The owner insists on her judgment as the reason to change the dish. The short sentences keep her impatience.
23|||The cook asks what he should do to increase the sweetness. The practical question gives her an opportunity to hand the responsibility back.
26|That's your job to figure out.|your job to figure out.|The owner says figuring it out is the cook's work. Her direct dismissal answers his practical question.
29|||The cook responds with his usual resigned repetition after a pause. Keep the change from practical discussion to reluctant assent.
33|||The owner again predicts that sweets will catch on. Keep the certainty as her opinion.
36|||The cook repeats his resigned assent. The repetition is a comic contrast with her renewed enthusiasm.
40|Sweet, remember? Good luck! Oh-ho-ho-ho!|Sweet, remember?;Good luck!|The owner repeats the one thing she cares about and sends him back to work with a laugh. The short encouragement follows her order.
63|||The notice forecasts Sweets in Alexandria. Keep the actual game announcement separate from the owner's certainty.
""",
}
review = checked_text(previous.review, {"len(records) == 32": "len(records) == 88"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::wine-fragrances-and-town-forecasts", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

