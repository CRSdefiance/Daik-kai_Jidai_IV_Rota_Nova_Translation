"""Contextual reread of the story exchanges tied to trade facilities."""
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import prepare_story_market_terms_20261119 as intake
from scripts import review_story_short_phrase_wraps_20261119 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, parent = intake.pairing.base, intake.pairing.native, intake.pairing.stage, intake.parent
ROOT = intake.ROOT
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v3.json"
paired = SimpleNamespace(base=base, native=native, stage=stage, parent=parent,
                         ROOT=ROOT, SOURCE=SOURCE, BLOCKS=intake.BLOCKS)

SCENES = {
    (0, 65): "Charlotte hands over the latest batch of goods. Rafael proposes a proper trading post. Charlotte asks about staffing, wages, goods to sell and scarce materials. He decides to bring the timber himself.",
    (0, 66): "Rafael returns with timber. Charlotte worries about the cost. Rafael calls it an investment and says he will be the first to buy their goods. Her gratitude turns to resolve.",
    (0, 137): "The Lisbon trade lesson moves from local buy and sell advice to cargo units and market share. Rafael can ask about shares or skip to trying Finish.",
    (0, 170): "Carlo bargains with Adil, notices his illness, and postpones their business. The next morning the innkeeper thanks him and Adil returns. Rafael recognizes Carlo's skill and concern for others. Carlo discloses his bereavement and the crew offers him a place with them.",
    (1, 296): "The explorers find their route blocked. The optional Charles branch proposes clearing it and ends with Hodram agreeing to shop for supplies at the Market.",
    (3, 130): "Carlo's bargaining skill catches Maria's attention. His concern for Adil delays trade until tomorrow. Maria recruits him after hearing what made him put health first. Her offer to face Venice together is personal to this route.",
}

# Source index, gloss, decision, and optional replacement.
NOTES = {
    (0, 65): """5|Charlotte hands over this batch.|The brief pause fits the handover and the goods are already in view.|
9|Rafael thanks Charlotte and starts a new subject.|The trailing address lets her invite him to continue.|
13|Charlotte asks what he wants to say.|The short reply fits friends speaking without ceremony.|
17|Rafael proposes a proper place to conduct trade.|Use trading post for the village building he proposes.|If you're going to trade here, I think you ought to build a proper trading post.
22|Charlotte repeats the unfamiliar proposal.|Keep the questioning echo and match the building he just proposed.|A trading post?
26|Rafael wants more goods handled at a dedicated place to buy and sell.|The existing reply explains the post immediately.|
30|Ships would go out of their way to trade there.|Give Rafael enthusiasm and make the detour a deliberate choice.|Then ships would go out of their way to trade here.
35|Charlotte doubts they can staff the post since villagers are already busy.|Let her ask the practical question and follow it with the village's constraint.|But who's going to run the trading post? Everyone in the village already has their hands full.
39|Rafael suggests hiring people the post would attract.|Keep the ships and the prospect of work as two reasons people would come.|You could hire people. A trading post would bring ships here, and people looking for work would come, too.
43|Charlotte asks how they would pay the workers.|The wages question follows the hiring suggestion directly.|
46|Merchants could invest at the post, and profits could keep it running after that.|Keep the financing sequence and remove the repeated trade wording.|You could ask merchants to invest in the post. Once you had the money to get started, the profits from trading could keep it going.
51|Charlotte fears their specialties would not draw merchants to trade at the post.|Restore the merchants' reason to stop and do business.|Would that really work? What do we make here that's worth a merchant stopping to buy?
54|Investment and growth allow more local goods and new specialties.|The optimistic progression and exclamation lead into Charlotte's doubt.|
58|Charlotte doubts anyone would invest.|The direct question invites Rafael to volunteer.|
61|Rafael says he will invest himself.|Make the financial commitment explicit in his spontaneous answer.|Of course! I'll invest.
66|Charlotte still thinks they cannot do it.|Give her an intact hesitant sentence before Rafael asks why.|No... I still don't think we can.
69|Rafael asks why.|The immediate question fits his surprise.|
74|Charlotte says there's almost no building stone or timber to build a large post.|Keep both materials and match the building name without shortening her objection.|There's hardly any building stone or timber around here. We couldn't build a big trading post.
78|Rafael will bring in the timber and tells her to wait without worry.|His brisk solution and reassurance close the exchange naturally.|""",
    (0, 66): """5|Charlotte exclaims Rafael's name.|Keep the live name and startled hesitation.|
9|Rafael greets Charlotte, says he has brought the timber and proposes building.|Carry over the name of the building and keep the energy of his arrival.|Hi, Charlotte! I've brought the timber! Let's build that trading post!
14|Charlotte is amazed but says the village cannot pay for so much timber.|Use a contraction and let her surprise give way to concern.|That's amazing! But the village can't afford all this timber.
18|Rafael does not need payment.|The informal reassurance answers the cost objection.|
23|Charlotte starts to protest.|Keep the unfinished protest and its emotional timing.|
27|Rafael calls this an investment and wants to be first to buy their local goods.|The cheerful promise explains the investment without adding conditions.|
31|Charlotte thanks him and promises to work hard even if it takes time.|Let her sound grateful and determined. Keep the live address and established building.|Thank you, FI! It may take a while, but I'll do my best to make it a trading post we can be proud of!
35|Rafael looks forward to it.|The short excited reply keeps his voice distinct.|
40|Charlotte anticipates being busy and resolves to get to work.|Her final resolve should sound like something she says aloud.|We'll have our hands full now! I'd better get to work.""",
    (0, 137): """6|Buying low and selling high is the basis of trade.|Keep the familiar maxim that opens the tutorial.|
9|Travel between the Mediterranean and Africa offers quick profits.|The existing line keeps both regions and the travel prerequisite.|
13|A long voyage is unlikely right away, so try trading nearby.|Keep the advice friendly and make the nearby activity clear.|Try trading close to home first. It's a bit early to head that far.
16|Compare local prices for a chance at larger profits.|The practical instruction follows the advice to start close.|
19|Buy Lisbon saffron or almonds and sell them around Ceuta.|Keep both goods and the playable example destination.|
22|Few ships and cargo holds limit early transactions.|Use conversational advice and keep the limit per transaction.|You won't have many ships or cargo holds at first, so you can only trade so much at a time.
26|One trade unit fills one hold, so holds determine purchase capacity.|The two sentences keep the unit definition and its consequence clear.|
30|Greater market share allows more trade at once.|The existing explanation introduces the tutorial's optional question.|
35|Choice to ask about share.|Keep the same term as the lesson and the concise caption.|
37|Choice to indicate understanding.|The short natural caption correctly skips the question.|
44|Rafael asks how to increase market share.|The plain beginner question follows the choice.|
48|If unclaimed share remains, investment at either facility can earn some.|Use the matching Palace and Market labels and keep the prerequisite. Protect the location phrase.|If there's any unclaimed market share, you can earn some by investing at the Palace or the Market.
52|Defer worrying about share until the player has earned money and has more ships.|The existing encouragement returns the player to the immediate task.|
60|Finish completes the deal when the player is ready.|Keep the exact button label and prompt the player to try it.|
""".rstrip(),
    (1, 296): """5|Hodram reacts to the obstacle.|The unfinished reaction leaves Gerhard room to identify it.|
9|Gerhard suspects a rockfall and says they cannot pass.|Keep the tentative diagnosis and direct warning.|
12|Hodram reluctantly proposes going back.|The terse decision fits the blocked path.|
33|Charles pauses before speaking.|Keep the silence that prompts Gerhard's question.|
37|Gerhard asks what's wrong and says they are leaving.|The direct address keeps Charles's name and the intended retreat.|
40|Charles proposes blasting the obstruction.|The abrupt exclamation sets up the others' surprise.|
44|Gerhard is astonished and repeats the proposal.|Punctuation and short echo fit the abrupt interruption.|
47|Charles confirms he means the rocks blocking the path.|The energetic reply clarifies his proposal.|
50|Hodram says clearing hard rock would need a large amount of gunpowder.|The skeptical question and reason are both present.|
54|Gerhard doubts they can obtain that much at once.|The existing line preserves the quantity as relative, without adding specifics.|
57|Charles says they can make it themselves.|The calm confidence contrasts with their objections in the exchange.|
60|Hodram asks whether Charles can make it.|The short question advances the exchange.|
63|Charles reminds the admiral of his research and promises to help if they bring the requested goods.|The response keeps the reminder, form of address and condition.|
67|Gerhard thinks the town sells the goods.|Keep his uncertainty and the town reference.|
70|Charles says to buy it at the Market and bring it here.|Use the facility caption and preserve the requested return.|Yes. Buy it at the Market and bring it here.
73|Hodram agrees to buy the goods.|The compact agreement closes the decision.|
""".rstrip(),
}
NOTES[(0, 170)] = """5|Carlo orders his usual amount of cinnamon.|Keep the familiar order that shows he knows this seller.|
9|Rafael thinks a customer is ahead of him.|The quick private aside fits his arrival.|
14|Adil agrees and names the total.|His easy reply sets up Carlo's challenge.|
18|Carlo asks whether the price went up.|The conversational fragment makes his feigned surprise clear.|
22|Adil denies it and says the price is unchanged.|The defensive denial suits the start of the negotiation.|
25|Carlo laughs and calls out Adil because he knows the cost.|The laugh softens the jab and the question does the bargaining work.|
28|Adil protests briefly.|The short objection interrupts the price challenge.|
32|The harvest and local demand should let Adil offer a better price.|The existing line keeps both reasons and Carlo's courteous pressure.|
36|Carlo can always buy from another shop.|Keep the casual threat and its deliberately obvious follow-up.|
40|Adil hesitates, concedes, and admits he cannot beat Carlo.|His stammer and defeat are audible in the current version.|
44|Carlo notices something and asks whether Adil has a fever.|The shift from price to concern is clear even before Adil understands.|
47|Adil suspects Carlo is finding another fault with his business.|Keep the pointed comeback, which refers back to his price defense.|
50|Carlo means the fever and advises early rest.|The plain concern and advice mark the change in tone.|
53|Adil dismisses him, then actually feels a chill.|The pause and sudden reversal both work.|
56|Carlo postpones his purchase and tells Adil to close for the day.|Keep the order and the promise to return tomorrow.|
59|Adil agrees and asks the other customers to return tomorrow.|The apologetic request keeps the same timing for the group.|
65|Carlo apologizes and asks whether they came to trade.|The relaxed question opens a new exchange with the travelers.|
68|Rafael asks how Carlo spotted the owner's illness.|His curiosity sounds natural and gives Carlo room to explain.|
72|Adil looked unwell.|His plain observation fits the short answer and later disclosure.|
84|An optional companion claims Carlo is almost as observant as he is.|Keep the comparison and the dry boast.|
90|Rafael privately questions that boast.|The parenthetical reaction fits his mild skepticism.|
95|Carlo often spots when people are unwell where others would miss it.|Avoid repeating notice while keeping Carlo's modest, personal explanation.|Most people wouldn't catch it. I tend to pick up on it when someone isn't feeling well.
99|Rafael takes in the answer.|The small acknowledgment leaves the disclosure for later.|
104|Carlo asks Rafael to come along to the Market tomorrow morning and offers to make up for today.|Use the actual facility name and the same warm, tentative offer in both routes.|Would you come with me to the Market tomorrow morning? I think I can make up for the delay.
107|Rafael thanks Carlo and agrees to come.|The simple answer finishes the arrangements.|
112|The innkeeper thanks Carlo the following day.|Keep the familiar call and gratitude.|
116|Carlo asks after Adil.|His first concern remains Adil rather than the transaction.|
120|Adil is in bed at home as a precaution.|The existing response answers both where he is and why he stayed there.|
123|Carlo hopes Adil gets well soon.|Keep the sincere short wish.|
127|Adil ignores the innkeeper's advice, and Carlo's intervention helped yesterday.|The unfinished thought conveys worry and supports the next gratitude.|
131|The innkeeper notices the digression and wants to thank Carlo for saving him.|The lively self-interruption fits the voice and preserves the compliment.|
135|Carlo redirects the thanks to the travelers who waited overnight.|The existing courtesy recognizes their inconvenience.|
139|The innkeeper apologizes for the delay and humbly offers a gift.|Keep the hesitation and open question when she hands it over.|
145|Carlo thanks the innkeeper and lets the travelers trade first.|The existing courtesy keeps the thanks and the reason to give them priority.|
149|Adil appears and apologizes to Carlo.|His cheerful call makes the surprise work.|
152|The innkeeper reacts to Adil's unexpected arrival.|Keep the abrupt address and its exasperation.|
156|Carlo tells Adil he should be in bed.|Both the name and concern come through immediately.|
159|Adil insists he's well and will not miss a good trading day.|His bluster follows the surprise without weakening his enthusiasm.|
163|The innkeeper calls Adil impossible.|The exasperated response fits his stubbornness.|
167|Carlo is reassured by the energy but advises him to take it easy today.|The qualified reassurance and practical warning already work.|
171|Carlo plans to come back later and asks Adil to serve the travelers.|The current phrasing keeps the loose timing and immediate request.|
174|Carlo tells the travelers to treasure family and health and says goodbye.|The natural advice foreshadows what he tells the crew later.|
177|Rafael pauses.|The silence lets him consider asking Carlo to join.|
183|Rafael starts to speak tentatively.|Keep the hesitant interjection before Carlo prompts him.|
188|Carlo prompts Rafael to continue.|The brief acknowledgment suits the hesitant address.|
192|Rafael asks Carlo to come aboard.|The gentle invitation leaves room for Carlo's surprise.|
197|Carlo asks what prompted the sudden invitation.|The current line expresses surprise naturally.|
201|Rafael admires Carlo's ability and character.|The concrete reference to looking after people connects to the preceding scene.|
206|Clau compliments Carlo's bargaining the day before.|Keep the specific example and casual crew voice.|
209|Carlo has been a merchant a long time.|His matter-of-fact reply carries the humility.|
213|Rafael is impressed that Carlo knows prices.|Keep the straightforward question and his eagerness to learn.|
217|Clau suspected Carlo was a professional.|The casual confirmation fits his earlier compliment.|
221|The companion is impressed.|Keep the brief approving interjection.|
225|Carlo falls silent.|The pause motivates the question about family.|
229|Clau asks whether Carlo dislikes sailing or faces family opposition.|The casual address and questions keep his tone without inventing kinship.|
232|Carlo no longer has family because they died a year ago.|His hesitation and the time marker both matter.|
235|Rafael pauses in response.|Keep the silence before Carlo continues.|
241|Carlo's daughter caught an illness that was going around while he was wrapped up in work and neglected her care.|Restore that the illness was going around and let Carlo take responsibility in his own words.|My daughter caught an illness that was going around. I was so wrapped up in work... I didn't take proper care of her.
244|Care came too late, his wife caught it too, and he lost both.|The current line leaves the illness unnamed and keeps the change from explanation to grief.|
248|Rafael addresses Carlo with sympathy.|Use the approved name for the plain, hesitant acknowledgment.|
253|The work Carlo neglected his family for felt empty. Now he values people's health more.|The existing phrasing makes his change in priorities clear.|
256|Rafael realizes why Carlo worried about Adil.|The indirect reference fits Rafael's dawning understanding.|
261|Rafael asks whether Carlo will go home.|The hesitant question gives Carlo space to answer.|
266|Carlo has too many happy memories in Venice to live alone there.|Keep the specific city and the emotional difficulty of being alone.|
270|Rafael is silent for a moment.|Keep the pause before he renews his invitation.|
275|Rafael asks again for Carlo to come, saying he needs him.|His directness gives this route a different emotional turn from Maria's.|
280|Carlo hesitates.|Keep the reflective hesitation rather than adding agreement.|
284|Rafael tells Clau he could learn from Carlo.|The line explains Rafael's personal reason for asking.|
289|Clau tentatively agrees.|The low-key response fits after Rafael speaks earnestly.|
293|Carlo pauses again.|The silence holds until the companion offers a different way to think about it.|
297|A crew member asks if they can become Carlo's new family.|Keep the original captain address and offer of companionship.|
301|Rafael endorses that suggestion and asks what Carlo thinks.|His enthusiasm and invitation to decide both come through.|
305|Carlo thanks them and is surprised at the offer.|Keep the vulnerable pause and gratitude.|
308|Clau calls it settled and also expects Carlo's professional skill.|The light touch restores the original humor after the confession.|
312|Carlo gives his full name and greets the crew.|Keep the approved name and the natural greeting on joining.|"""

NOTES[(3, 130)] = """4|Carlo orders his usual quantity of cinnamon.|Keep the routine order that shows they have traded before.|
8|Maria notices another customer is ahead of her.|The concise private observation fits her arrival.|
12|Adil agrees and gives the price.|The informal start sets up Carlo's objection.|
16|Carlo asks whether the price has gone up.|The short question makes the feigned surprise audible.|
20|Adil insists the price is the same as ever.|His defensive answer leads directly into Carlo's response.|
23|Carlo laughs, chides Adil, and points out he knows his costs.|Let the jab sound familiar between two experienced traders.|Ha ha! Come on, Adil. You think I don't know what you paid for it?
26|Adil starts to object.|The brief protest lets Carlo follow up immediately.|
30|Carlo cites the crop and local demand to ask for a better price.|Keep his bargaining case and the tentative way he puts it.|With this year's harvest and the demand around here, I think you could do a little better.
34|Carlo points out he can use another supplier.|The dry legal exaggeration sounds like a trader pressing his advantage.|
38|Adil falters and concedes Carlo has beaten him.|The repetition and admission already carry his reluctant defeat.|
42|Carlo asks whether Adil has a fever.|The direct question lets his concern replace the bargaining.|
45|Adil thinks Carlo is still criticizing his business.|Keep the defensiveness from the pricing exchange.|
48|Carlo is talking about the fever and recommends early rest.|His plain change of subject and advice already read naturally.|
51|Adil dismisses the concern before admitting he has chills.|The reversal and reaction make a natural interruption.|
54|Carlo postpones his purchase and tells Adil to close for today.|Use his merchant's register and keep the same actions in both routes.|See? I'll do my buying tomorrow. Close up for today.
57|Adil agrees and asks the other customers to come back tomorrow.|Keep the apology and timing while making the request conversational.|Hmm... I'll do as you say. Sorry, folks. Could you come back tomorrow, too?
63|Carlo apologizes and asks whether they came to trade.|The existing line makes the transition to Maria natural.|
66|Maria asks how Carlo knew Adil was ill.|The brief question can rely on the immediately preceding exchange.|
70|Carlo could tell from Adil's color.|Use a natural observation that supports Maria's later doubt.|He looked pale, that's all.
82|The companion claims Carlo is almost as observant as he is.|Preserve the boast as a backhanded compliment rather than an exact equality.|Well, well. You're almost as sharp-eyed as I am.
88|Maria doubts Adil looked especially ill.|The private uncertainty preserves her reaction distinct from Rafael's.|
92|Carlo says the signs would escape most people but he notices illness.|Give the same unassuming explanation in both routes.|Most people wouldn't catch it. I tend to pick up on it when someone isn't feeling well.
96|Maria quietly takes in Carlo's answer.|The parenthetical response is separate from the later request to join.|
100|Carlo invites Maria to the Market tomorrow morning and wants to make up for the delay.|Match the facility caption and Carlo's identical Japanese offer to Rafael.|Would you come with me to the Market tomorrow morning? I think I can make up for the delay.
103|Maria agrees to go.|The cordial response ends the first day's exchange.|
107|The innkeeper thanks Carlo for yesterday.|The warm greeting brings us back the following morning.|
111|Carlo asks how Adil is doing.|His first concern is Adil, as in the other route.|
115|Adil is in bed at home for safety.|The brief reassurance gives the necessary information.|
118|Carlo hopes for Adil's recovery.|The sincere wish suits the next speaker's gratitude.|
122|Adil does not heed the innkeeper, who credits Carlo for stepping in yesterday.|The incomplete thought works as an expression of worry.|
126|The innkeeper cuts herself short and says she wants to thank Carlo for saving his life.|The first-person aside and thanks fit her talkative voice.|
130|Carlo directs her thanks to the travelers who waited overnight to trade.|The established line preserves both the courtesy and inconvenience.|
134|The innkeeper apologizes and tentatively offers a small gift.|Restore the question so she sounds tentative about asking them to accept.|Oh dear, we held you up. I'm sorry. It's nothing much, but... would you take this?
140|Carlo thanks the innkeeper and lets the travelers trade first because they are in a hurry.|The existing address and gesture of priority both work.|
144|Adil arrives and apologizes to Carlo for yesterday.|The upbeat greeting is a clear reversal of the expected bed rest.|
147|The innkeeper reacts to Adil's sudden arrival.|The sharp one-word address suits her surprise.|
151|Carlo says Adil ought to be in bed.|The short admonishment follows his earlier advice.|
154|Adil insists he's well and refuses to stay in bed on a good trading day.|Keep the stubborn confidence and the business motive.|
158|The innkeeper is exasperated with Adil.|The concise line sounds like a response to someone she knows well.|
162|Carlo is reassured but warns Adil against overexertion today.|The chuckle and friendly warning coexist naturally.|
166|Carlo says he may come tomorrow and asks Adil to help the travelers first.|Keep the possible next-day visit and who should be served now.|I'll stop by again, maybe tomorrow. For now, take care of these travelers, will you?
169|Carlo advises the travelers to value family and health, then takes his leave.|The advice foreshadows his later disclosure, and the farewell is conversational.|
172|Maria pauses before calling out.|The silent beat allows the farewell to settle.|
177|Maria tells Carlo to wait.|Her hesitation suits the change of subject.|
181|Carlo asks what she wants.|The short acknowledgment gives her the floor.|
185|Maria checks Carlo's name and asks if he will use his trading skill aboard her ship.|Keep the full recruitment request and the tentative opening.|
189|Carlo is surprised by the sudden suggestion.|The existing line keeps his polite disbelief.|
193|Maria says she has thought about it since yesterday.|Her firm explanation makes her initiative clear.|
196|Carlo is a merchant rather than a sailor.|The compact contrast sets up Maria's case for his usefulness.|
199|Maria argues that his market knowledge is valuable to her fleet.|The existing question and explanation fit her persuasive voice.|
203|Carlo goes quiet.|Keep the pause that prompts Maria's questions.|
207|Maria asks if Carlo dislikes sailing alone or being away from family.|Turn the source's second possibility into a complete, gentle question.|Do you dislike the thought of sailing alone? Or would you rather stay with your family?
210|Carlo says his family died a year ago.|The short sentences keep the grief and time frame.|
213|Maria pauses.|Keep the silence before he explains.|
218|His daughter caught an illness that was going around while he was consumed with work and neglected her care.|The existing panel preserves the epidemic context, hesitation and guilt.|
221|Care came too late and his wife also caught it. Both died.|The current panel keeps his self-blame and both losses without naming a disease.|
225|Maria reacts with sympathy.|The quiet response fits before he continues.|
229|The job he neglected his family to get felt empty, and now health comes first.|Untangle the opening clause and let Carlo explain what changed.|I'd put my work ahead of my family, and after that it all felt empty. Ever since, I've cared more about people's health than business.
232|Maria sees why Carlo worried about Adil.|Keep the connection in her own voice and address the preceding disclosure.|
236|Maria asks whether he has thought of returning home.|The softened question suits the moment.|
240|Venice holds too many happy memories for Carlo to live there alone.|Keep the reason and let the second sentence sound spoken without a fragment.|Venice? I have too many happy memories there. I couldn't live there alone.
244|Maria takes a moment to consider what he said.|The pause leads into her offer.|
248|Maria offers to accompany Carlo to Venice so he need not return alone.|Preserve the explicit offer about Venice, which is specific to her route.|
252|Carlo is puzzled.|Keep the punctuation-only reaction.|
256|Maria says a crew can be like family and suggests a new one.|The existing simile and warm suggestion keep the relationship as an offer.|
260|Carlo asks whether they would become his new family.|The broken opening fits his surprise and vulnerability.|
264|Maria says they would if he wants them to.|The gentle condition leaves him the choice.|
268|Carlo thanks them and accepts the offer to sail.|His brief assent follows the invitation naturally.|
271|Carlo gives his full name and greets the crew.|The approved spelling and glad greeting suit the ending.|"""

PHRASES = {
    (0, 65, 17): ("trading post",),
    (0, 65, 22): ("trading post",),
    (0, 65, 30): ("go out of their way",),
    (0, 65, 35): ("trading post",),
    (0, 65, 39): ("trading post",),
    (0, 65, 74): ("trading post",),
    (0, 66, 9): ("trading post",),
    (0, 66, 31): ("trading post",),
    (0, 137, 22): ("cargo holds",),
    (0, 137, 48): ("market share", "the Palace or the Market"),
    (0, 170, 104): ("tomorrow morning",),
    (3, 130, 100): ("tomorrow morning",),
}

def main():
    packet = base.load(SOURCE)
    groups = {(g["route"], g["block"]): g for g in packet["groups"]}
    assert groups.keys() == NOTES.keys()
    exchanges, edits = {}, {}
    for (route, block), prose in NOTES.items():
        rows = [line.split("|") for line in prose.splitlines()]
        source_indices = [r["source_record_index"] for r in groups[route, block]["records"]]
        assert [int(n) for n, *_ in rows] == source_indices, (route, block, source_indices)
        exchanges[route, block] = 0, "\n".join(f"{meaning}|{reason}" for _, meaning, reason, _ in rows)
        edits.update({(route, block, int(n)): (english, PHRASES.get((route, block, int(n)), ()))
                      for n, _, _, english in rows if english})
    text = checked_text(getsource(workflow.main), {
        '        excerpts = LIL if (route, block) == (2, 26) else (EXCHANGES[route, block],)':
            '        excerpts = (exchanges[route, block],)',
        '            for raw, note in zip(raw_rows, notes, strict=True):':
            '            for raw, note in zip(raw_rows, notes, strict=True):\n                meaning, reason = note.split("|", 1)',
        'speaker=speaker, context=group["context"], source_meaning=note, localization_note=note,':
            'speaker=speaker, context=SCENES[route, block], source_meaning=meaning, localization_note=reason,',
    })
    scope = vars(workflow) | globals() | dict(exchanges=exchanges, EDITS=edits)
    exec(compile(text, __file__ + "::market_terms_editorial", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
