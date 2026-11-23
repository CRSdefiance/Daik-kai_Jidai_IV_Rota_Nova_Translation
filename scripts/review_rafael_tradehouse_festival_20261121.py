"""Review Rafael's trade house, Charlotte's festival and Maria's bargain."""

from inspect import getsource
from pathlib import Path

from scripts import register_rafael_pereira_village_20261121 as parent
from scripts import review_rafael_pereira_village_20261121 as prior
from scripts.review_company_name_dialogue_20261121 import TOKEN, logical
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_tradehouse_festival_20261121")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v3.json"
BLOCKS = ((65, 66, 67, 69, 70), (), (), ())
CONTEXTS = {
    65: "Rafael proposes a trade house, and Charlotte tests the plan against the village's labor, finances, goods and building materials.",
    66: "Rafael brings timber. Charlotte worries about the cost. He explains how his investment will pay off when the village has goods to sell.",
    67: "Rafael offers corn seeds, and Claudio finds an excuse for him to walk Charlotte home. They discover they are the same age. Charlotte thanks him with a flower and the crew privately wonders what happened.",
    69: "Charlotte invites Rafael to celebrate the village's new product. She thanks him for helping, while he draws courage for Portugal from the village's example. The source leaves the moment before she runs away unspoken. Back aboard, Arcadius and Claudio decide how to help.",
    70: "Xien recognizes Rafael and brings him to Maria. She offers the Bamboo Assembly Plan in exchange for defeating Kurushima. Xien and Maria explain the wako and describe why the faction is difficult to catch.",
}

# Empty English keeps the wording. Named phrases ask the formatter to keep a beat together.
DECISIONS = """
65 5|...Here you go. This is the latest batch.|the latest batch.|Charlotte identifies the goods for this delivery in her everyday voice.
65 9|||Rafael thanks Charlotte and changes the subject by addressing her.
65 13|||Charlotte's quick question encourages him to go on.
65 17|If you're going to keep trading here, I think you ought to build a proper trade house.|keep trading here,;a proper trade house.|Use the established facility term and keep Rafael's suggestion tentative.
65 22|A trade house?||Charlotte repeats the proposed facility's name before he explains it.
65 26|You could handle more kinds of goods and have a place set up for buying and selling.|more kinds of goods;buying and selling.|Rafael explains both the wider selection and the dedicated place to trade.
65 30||go out of their way;to trade here.|Keep Rafael's concrete prediction that ships would make a detour.
65 35|But who's going to run the trade house? Everyone in the village already has their hands full.|run the trade house?;Everyone in the village;has their hands full.|Charlotte's objection is about staffing and the villagers' existing work.
65 39|You could hire people. A trade house would bring ships here, and people looking for work would come, too.|You could hire people.;A trade house;looking for work|Rafael expects the trade house to attract ships and workers. Keep that as his forecast.
65 43|||Charlotte follows up on hiring with a practical question about wages.
65 46|Ask merchants to invest in the trade house. Once you've got money to get started, the profits can keep it going.|merchants to invest;the trade house.;money to get started,;the profits can keep it going.|Retain commercial investment as the initial funding and trading profits as ongoing support.
65 51|Would that really work? We don't make anything special enough for merchants to go out of their way to buy.|Would that really work?;go out of their way|Charlotte questions whether any local specialty can justify the merchants' effort.
65 54|If investment helps the village grow, you can make more local goods and even come up with new ones!|helps the village grow,;make more local goods;come up with new ones!|Preserve both greater production and the possibility of new specialties.
65 58|||Charlotte still doubts that any merchant would put money in.
65 61|Of course! I'll invest!||Rafael answers enthusiastically by offering his own investment.
65 66|||Charlotte pauses and remains unconvinced because of materials.
65 69|||Rafael asks what's in the way before offering a solution.
65 74|There's hardly any building stone or timber around here. We couldn't build a big trade house.|building stone;timber around here.;build a big trade house.|Keep both missing materials, the local limit and the proposed building.
65 78|Then we'll bring it in! I'll get the timber. Leave it to me. I'll be back!|I'll get the timber.;Leave it to me.;I'll be back!|Rafael offers to bring the timber himself and asks Charlotte to wait.
66 5|||Charlotte's surprised greeting is carried by the given-name substitution.
66 9|Hi, Charlotte! I brought the timber! Let's build that trade house!|I brought the timber!;build that trade house!|Rafael comes back with what he promised and uses the same facility term.
66 14||the village can't afford;all this timber.|Charlotte is impressed but immediately sees a cost the village cannot afford.
66 18|||Rafael's simple answer reassures her about payment.
66 23|||Charlotte's unfinished objection leaves Rafael room to explain.
66 27|It's part of my investment. Once you've got plenty of local goods to sell, I'll be first in line to buy them!|part of my investment.;plenty of local goods;first in line|Rafael treats the timber as investment and expects to buy the new products himself.
66 31|Thank you, FI! It may take a while, but I'll build a trade house we can all be proud of!|Thank you, FI!;take a while,;build a trade house;be proud of!|Charlotte thanks Rafael and acknowledges the time it will take.
66 35|||Rafael's brief, eager reply suits Charlotte's promise.
66 40|Well, things are about to get busy! I'd better get to work.|about to get busy!;get to work.|Charlotte shifts from gratitude to getting the work done.
67 5|...Here you go. This is the latest batch.|the latest batch.|Keep the delivery greeting consistent with the earlier exchange.
67 9|||Rafael begins with thanks and hesitates before offering the gift.
67 14|||Charlotte asks him to elaborate.
67 18|These are corn seeds. I thought corn might give the village something new to sell.|These are corn seeds.;I thought corn might;something new to sell.|Preserve the crop, the seeds and the tentative possibility of a new trade good.
67 23||you're always helping me...|Charlotte's gratitude trails off before Rafael interrupts modestly.
67 26|N-no, think nothing of it. More goods for the village to trade would help us, too...|think nothing of it.;help us, too...|Keep Rafael's stammer and his explanation that the new product would also benefit the crew.
67 31|||Charlotte thanks him and thinks immediately of the other villagers.
67 34|||Rafael is pleased, then notices how much she is carrying.
67 38|I'm fine. Working the fields keeps me strong.|Working the fields;keeps me strong.|Charlotte explains her strength from her ordinary farmwork.
67 41|||Rafael begins another objection just before Claudio steps in.
67 46|||Claudio's short directive and given-name address cut off Rafael's hesitation.
67 49|||Rafael is surprised that Claudio volunteered him.
67 54|||Charlotte resists putting him to trouble and tries to demonstrate that she can carry it.
67 57|||Claudio takes charge in his usual direct voice.
67 60||split it in half...;FI's half|Keep Claudio's audible plan to divide the load and put extra weight in Rafael's share.
67 64|||Claudio finishes the arrangement and tells Rafael to take the load.
67 67|||Rafael's shout reacts to the unexpectedly heavy share.
67 71||Heavy, isn't it?|Charlotte apologizes and checks how heavy it feels. Keep the question tag together.
67 74|||Rafael denies the weight immediately after protesting to Claudio.
67 78|I'll be back shortly. Clau, can you take care of the rest...|I'll be back shortly.;take care of the rest...|Rafael leaves with Charlotte and starts to ask Claudio to handle things.
67 82|||Claudio answers before the question is finished and hurries them along.
67 85|||Claudio can finally exhale after orchestrating their departure.
67 88|He never follows through, does he? Good thing FI has me looking out for him!|follows through, does he?;looking out for him!|Claudio thinks Rafael needs his intervention and jokes to himself without claiming they are a couple.
67 97|||Charlotte's brisk invitation and offer of tea ease the move indoors.
67 100|All right.||Rafael's quiet acceptance sounds natural as he takes in the house.
67 105|||Charlotte reads his reaction and apologizes before explaining the house.
67 109|Heh... Not much here, is there? It's barely a house. Just a roof and some walls.|Not much here, is there?;barely a house.;a roof and some walls.|Keep her sheepish humor and the material description of the sparse house.
67 113|||Rafael asks how long she has been there without passing judgment on the house.
67 118|I was eleven when we left Europe. That would be six years ago. Here you go.|eleven when we left Europe.;six years ago.;Here you go.|Preserve both age facts and Charlotte handing him the tea.
67 122|Thanks. Wait, if you were eleven six years ago...|if you were eleven;six years ago...|Rafael begins to do the math out loud while taking the tea.
67 126|You're seventeen? Charlotte, we're the same age?!|You're seventeen?;we're the same age?!|Keep the age and Rafael's genuine surprise at discovering they are peers.
67 131|||Rafael starts to say he thought she was older and immediately regrets it.
67 136||My skin is rough,;look at my hands...|Charlotte points to the effects of work on her skin and hands.
67 140|||Keep Charlotte's vulnerable comparison to other girls her age.
67 143|Not at all! You're so good at handling things, I just assumed you were older...|good at handling things,;assumed you were older...|Rafael explains that her capability made him think she was older.
67 148||you're so pretty.;like a girl...|Preserve Charlotte's compliment and comparison as her own words.
67 152|A-a girl?! Do I really look like I can't handle myself?|A-a girl?!;can't handle myself?|Rafael hears a suggestion that he is unreliable and reacts to his own reading.
67 156|No, that's not what I meant. I just meant the person beside you must...|that's not what I meant.;the person beside you|Charlotte backs away from his interpretation and leaves the next thought unfinished.
67 160|||Rafael notices that Charlotte broke off and prompts her with her name.
67 165|Oh, never mind... Oh no, it's getting dark already!|never mind...;getting dark already!|Charlotte changes the subject and reacts to the late hour.
67 169|||Rafael realizes that he needs to get back.
67 173|||The unfinished farewell gives Charlotte a chance to stop him.
67 178|||Charlotte calls him by name and asks him to wait.
67 181|||Rafael's wordless confusion makes space for the gift to appear.
67 186|||Charlotte returns and leaves the object for Rafael to identify.
67 190|||Rafael likes the flower before asking if she means it for him.
67 194|(Nods) To thank you for today. It's all I've got.|To thank you for today.;It's all I've got.|Keep the nod, the reason for the gift and Charlotte's modesty.
67 198|Thank you, Charlotte! I love it!|Thank you, Charlotte!;I love it!|Rafael's warm thanks show how much the flower means to him.
67 202|I hope the seeds you gave us have sprouted and grown by the next time you come.|the seeds you gave us;have sprouted and grown;the next time you come.|Charlotte is already thinking about the crop and his next visit.
67 206|I'm looking forward to it! See you, then.|looking forward to it!;See you, then.|Rafael accepts the idea of returning and says goodbye.
67 210|||Charlotte answers his farewell simply.
67 214|||Claudio asks Arcadius where Rafael is and keeps the given-name substitution.
67 218||just came back;watering his flower.|Arcadius says when Rafael returned and what he was doing.
67 221|||Claudio's drawn-out surprise fits the sound of the Japanese question.
67 225|Yes. He asked for a vase. When I brought it, he just sat there smiling at the flower...|asked for a vase.;When I brought it,;smiling at the flower...|Keep the vase, Arcadius bringing it, and Rafael smiling at the flower.
67 229|||Arcadius wonders what good thing happened without claiming to know.
67 233|||Claudio begins to put it together without saying what he suspects.
67 237|||Arcadius hears Claudio's tone and asks for more.
67 241|||Claudio admits he knows a little without immediately telling the story.
67 245|That's unfair! Don't keep it to yourself. It's about the girl from before, isn't it?|Don't keep it to yourself.;about the girl from before,;isn't it?|Keep Arcadius's curiosity and guess, including the question tag.
67 249|||Claudio begins telling the story with a pleased laugh.
67 252|||The pause stands in for the actual retelling.
67 256||The village is coming along,;look forward to.|Keep Arcadius's pleasure in the village's growth and the affectionate speculation.
67 260|||Claudio's plain agreement closes the private exchange.
69 5|...Here you go. This is the latest batch.|the latest batch.|Keep the latest delivery in the same voice as the earlier visits.
69 9|||Rafael's brief thanks make room for the extra item.
69 14|||Charlotte hesitates and hands it over instead of explaining it first.
69 18|Is that...? At last! Congratulations!|At last!|Rafael recognizes the achievement with surprise and enthusiasm.
69 22|We haven't got much yet, but everyone's thrilled that we have something new to sell.|We haven't got much yet,;everyone's thrilled;something new to sell.|Charlotte distinguishes the small quantity from the big achievement for the village.
69 26|The village is finally coming to life. Everyone wants to celebrate there today.|finally coming to life.;celebrate there today.|Preserve the new bustle, timing and location of the celebration.
69 30|||Charlotte's invitation is direct and keeps Rafael's substituted given name.
69 33|Sure, I'll come!||Rafael replies eagerly in the same conversational register.
69 38|Really? I'm so glad!||Charlotte's open relief follows his acceptance.
69 41|I'll get back to the village first and wait for you there.|back to the village first;wait for you there.|Keep Charlotte going ahead and waiting at the village.
69 48|Wow, this looks like a festival!|looks like a festival!|Rafael's reaction expresses how festive the celebration looks.
69 52|||Charlotte calls Rafael by name over the picture. Keep the FE control and given-name substitution.
69 56|||Rafael's surprised recognition fits his reaction to her changed appearance.
69 62|||Charlotte welcomes him and sees he has stopped short. Keep the speakerless picture dialogue.
69 65||You just look different;than usual...|Rafael stammers and tries to say what surprised him without judging her clothes.
69 69|||Charlotte tentatively asks how the outfit looks on her. Keep the picture dialogue consumer.
69 73|||Rafael's quick denial answers her insecurity directly.
69 78||like this before.;It's a little embarrassing...|Keep the first-time outfit, tentative reassurance and embarrassment. Reflow the last sentence as a unit.
69 82|It looks great on you!||Rafael gives a direct compliment that answers her concern about how it looks.
69 87|Hee hee, thanks. Come this way. There's plenty to eat!|Come this way.;There's plenty to eat!|Keep Charlotte's laugh and invitation as she moves the festival visit along.
69 91|Sure!||Rafael accepts the invitation in a spoken reply.
69 100|||Charlotte offers the food directly.
69 104|||Rafael thanks her and reacts after trying it.
69 108|I'm glad you like it!||Charlotte's reply is relief at his reaction to the food.
69 112|Oh, that's right! Look over there.|Look over there.|Charlotte remembers something she wanted to show him.
69 115|||Rafael follows Charlotte's direction with a brief question.
69 120|||She points out the crop without naming it again.
69 124|||Rafael recognizes where the village is cultivating it.
69 128|That's right. Next year we'll have an even bigger harvest!|Next year;an even bigger harvest!|Keep Charlotte's expectation of more crops next year.
69 131|Then the village will be better off, too!|will be better off, too!|Rafael connects the larger harvest to the village's prosperity.
69 135|||Charlotte's short agreement follows that prospect.
69 139|||The pause turns the conversation from optimism to personal thanks.
69 143||thank you so much.;smiling again,;all thanks to you.|Keep the given-name address, Charlotte's gratitude and the villagers smiling again.
69 146|||Rafael redirects the credit to Charlotte's hard work.
69 150|That's not true!||Charlotte rejects Rafael's attempt to downplay his contribution.
69 154|Besides, seeing what you've all done here makes me want to try harder, too.|what you've all done here;want to try harder, too.|Rafael explains how the whole village inspires him.
69 158|||Charlotte's wordless prompt leads into Rafael's explanation of why.
69 162|Spain annexed Portugal, my homeland...|Spain annexed Portugal,|Preserve annexation as an event that has happened in this scene and keep Rafael's personal tie.
69 166|Seeing how you've built up your village makes me want us to win Portugal back for ourselves...|built up your village;win Portugal back;for ourselves...|Tie the crew's determination to the villagers' own effort and Rafael's wish to reclaim his country.
69 171|That's the courage you give me!|the courage you give me!|Rafael completes the thought by saying where he finds his courage.
69 176|...I was close to giving up, too. I used to think about running away from the village all the time.|close to giving up, too.;running away from the village;all the time.|Charlotte admits how often she thought about leaving despite staying.
69 180|||Rafael points out that she did stay. Keep his attention on her own decision.
69 184|Because you gave me hope.|you gave me hope.|Charlotte answers his point by crediting Rafael with her renewed hope.
69 188|You found that hope on your own.|found that hope on your own.|Rafael returns the credit to Charlotte herself.
69 193|||Charlotte begins another response and leaves the thought unfinished.
69 197|||Rafael's quiet repetition of her name leaves the moment unresolved.
69 202|||The silence is an intentional beat in the unspoken exchange.
69 207|||Charlotte's silent reaction precedes Rafael's unanswered question.
69 211|||Rafael reacts with uncertainty without specifying what happened.
69 216|||Keep Charlotte's stammered apology. The words leave the cause unspecified.
69 220|||Rafael's surprised punctuation carries the reaction as the source does.
69 225|||Rafael calls after Charlotte as she leaves.
69 230|||The quieter repetition of her name leads into the return aboard.
69 239|Hey, you're back already? That was fast. ...FI?|you're back already?;That was fast.|Claudio greets him casually before realizing something is wrong.
69 243|||Claudio asks what happened after seeing Rafael's expression.
69 247|He looked pretty down.|looked pretty down.|Arcadius describes what he saw in everyday speech without presuming the cause.
69 251||Did something happen...?;go check on him.|Claudio wants to find out what is wrong by checking on Rafael.
69 254|Wait, Clau. Let's give him some space for now...|Let's give him some space;for now...|Arcadius asks Claudio to leave Rafael alone for the time being.
69 257|||Arcadius offers the village as the alternative place to go.
69 260|The village?||Claudio repeats the destination, surprised by the suggestion.
69 264|||Arcadius suggests they might help Rafael by going.
69 268|Good idea! I'll get to the bottom of this...|get to the bottom of this...|Claudio immediately proposes finding out what happened in his eager voice.
69 271|||Arcadius gently points out that Claudio's questioning would backfire and offers to speak.
69 274||doesn't leave anything;for me to do!|Claudio's objection is that he would have no role.
69 277|Just come with me, Clau. Showing up will tell FI how much you care better than anything you could say.|Just come with me, Clau.;will tell FI;how much you care|Arcadius trusts that Claudio's presence will communicate his concern.
69 281|Tch... No fun in that, but all right. It's for FI, after all.|but all right.;It's for FI,;after all.|Claudio grumbles but agrees because he's worried about Rafael.
70 5|So this is what it looks like at the far eastern edge of the world...|the far eastern edge;of the world...|Rafael reacts to the landscape rather than leaving his thought as a fragment.
70 18|It's so different from the Arab lands and India. Look at these buildings. What a fascinating place.|the Arab lands and India.;Look at these buildings.;a fascinating place.|Keep the broader Arab region, India, the striking buildings and Arcadius's interest.
70 25|Amazing, isn't it? Now this feels like an adventure. ...Hey, what's that?|Amazing, isn't it?;feels like an adventure.;Hey, what's that?|Claudio enjoys the adventure before noticing the newcomer.
70 29|||Xien identifies the company and its leader politely. Keep the established company and surname substitution order.
70 32||That old fellow;an Eastern commander!|Keep Claudio's unguarded impression, which prompts Arcadius to shush him. He is guessing at an appearance.
70 43|Shh! You can't just say that to someone!|can't just say that|Arcadius calls out Claudio's rude opening to a stranger.
70 50|||Rafael confirms his identity with the original given-name and surname substitutions.
70 55|||Xien goes straight to the Proof without expanding the mystery he has just raised.
70 59|||Rafael's single outburst fits his surprise that Xien knows what he is seeking.
70 72|||Arcadius reacts silently before Rafael answers.
70 79|Ah... Yes, we are. Does that mean you know something about it?|Yes, we are.;Does that mean;know something about it?|Rafael confirms the search and tentatively asks whether Xien knows more.
70 83|||Xien invites discussion without giving the information away yet.
70 87|All right. Let's hear what you have to say.|Let's hear what you have to say.|Rafael agrees to listen before Xien introduces Maria.
70 92|||Xien introduces Rafael to Admiral Maria by surname, preserving both native identities.
70 97|||Rafael's unspoken surprise creates room for Claudio's reaction.
70 102|||Claudio blurts out that he finds Maria beautiful in the same unguarded voice he used on seeing Xien.
70 114|||Janus's restrained reaction contrasts with Claudio's outburst.
70 121|I'm Maria Li. Xien is my right-hand man. Time is short, so I'll get to the point.|I'm Maria Li.;my right-hand man.;Time is short,;get to the point.|Maria names herself and Xien's role, then briskly states why she is being direct.
70 125|||Rafael hesitates before he manages to answer her.
70 129|Hey, FI! You can stare later!|You can stare later!|Claudio teases Rafael for looking instead of listening.
70 132|||Rafael stammers a defensive answer.
70 137|||Claudio makes his embarrassment worse with a teasing laugh.
70 140|||Maria waits just long enough before asking to speak.
70 143|||Rafael gives way and apologizes after the interruption.
70 148||the key to deciphering;that map...|Maria reveals she already has the key used to read the map.
70 152|||Rafael's incomplete question conveys surprise at Maria having it.
70 157|Yes. But I have no use for it. There's an official ban on overseas voyages here, after all.|I have no use for it.;an official ban;on overseas voyages here,|Maria explains the official maritime ban as her reason for not needing the key.
70 161|I see. But we really do need it.|we really do need it.|Rafael acknowledges the explanation and insists on his own need.
70 166|So it seems. I might let you have it if you'll do something for me.|I might let you have it;do something for me.|Maria offers to consider the exchange if Rafael agrees to a request.
70 170|Really? What would it take?|What would it take?|Rafael asks directly what would make her part with it.
70 174|One condition. Wipe out Kurushima's pirates. They're wako.|Wipe out Kurushima's pirates.;They're wako.|Maria names the sole condition and uses the established group term that Claudio asks about.
70 178|||Claudio asks what the new term means before anyone assumes he knows.
70 181|Gangs of pirates. They spend their days plundering, mostly here in East Asian waters.|Gangs of pirates.;their days plundering,;East Asian waters.|Xien defines the wako by activity and primary waters without attributing a single nationality.
70 185|Are they really that dangerous?|really that dangerous?|Rafael asks how threatening the pirates are before Xien explains the real problem.
70 190|I'd call them a nuisance. The trouble is catching them.|call them a nuisance.;The trouble is catching them.|Xien corrects Rafael's impression and sets up Maria's account of why they escape.
70 193|They hit coastal villages in nimble ships. When we go after them, they get away before we can catch them.|coastal villages;in nimble ships.;go after them,;before we can catch them.|Preserve their targets, maneuverability and ability to evade pursuit.
70 204|||Janus draws the practical conclusion that the crew may need faster ships.
70 211|Small ships aren't all they have. They've improved their equipment lately. Seems they've got all kinds of ships now.|Small ships aren't all they have.;improved their equipment;all kinds of ships now.|Keep Xien's corrective warning, recent improvements and uncertainty about the range of ships.
70 214|Once I've confirmed the Kurushima faction is gone, I'll give you the Bamboo Assembly Plan.|Kurushima faction is gone,;the Bamboo Assembly Plan.|Maria waits for confirmation before giving Rafael the correctly named item.
70 218|||Rafael echoes the item type as a surprised question.
70 223||the Proof of Conquest;in East Asia.;Not a bad deal, is it?|Keep Maria's stated necessity and casual pressure in the final question.
70 227|All right. We'll give it a try.|We'll give it a try.|Rafael accepts the arrangement while promising an attempt.
"""


source = checked_text(getsource(prior.main), {
    'context=CONTEXTS[block] if block in CONTEXTS else village_context(number)': 'context=CONTEXTS[block]',
    '            if changed:\n                assert selector != 254': '            if changed and selector != 254:',
    'assert len(records) == 197 and not earlier and not decisions': 'assert len(records) == 200 and not earlier and not decisions',
})
scope = vars(prior) | globals()
exec(compile(source, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
