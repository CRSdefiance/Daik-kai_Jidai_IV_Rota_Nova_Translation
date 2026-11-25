"""Contextual editorial decisions for Rafael's SC0 blocks 85–100."""

from collections import Counter
from pathlib import Path

from scripts import register_rafael_gerhard_tutorial_20261121 as parent
from scripts.review_rafael_gerhard_tutorial_20261121 import GATES, TOKEN, logical
from scripts.review_rafael_spain_london_20261121 import plan_progressive


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_B85_B100_followup_20261121")
SOURCE, OUTPUT = ROOT / "paired_source_registered_parent.json", ROOT / "rafael_followup_review_v2.json"
PRIOR = Path("translations/rafael_B85_B100_contextual_final_review_v1.json")
NAMES = Path("translations/rafael_B85_B100_scoped_names_final_v1.json")
BLOCKS = ((85, 86, 87, 88, 90, 91, 92, 93, 95, 97, 100), (), (), ())
CONTEXTS = {
    85: "A sailor proposes another meeting with Gerhard. Rafael can defer or go alone to renew the invitation. Gerhard acknowledges his training and agrees to join.",
    86: "An explosion interrupts the Caribbean crew's plans. The shipwright takes them to Charles's workshop. Charles connects scientific curiosity to sailing and decides to join the fleet.",
    87: "In Zipangu, Kurushima and his men use a staged collision to pick a fight. Yukihisa intervenes, explains his restraint and asks to see the wider world with Rafael.",
    88: "Rafael and Claudio find the Silla Gold Crown first. Rafael can let Julian give it to Mihwa or announce that he wants to give it himself. Julian runs off in either case, with different motives.",
    90: "Janus daydreams about trading in the Mediterranean. Rafael promises to remember the region when he puts Janus in charge of a regional fleet.",
    91: "A sailor asks about miracles. A believer gets the Miracle Bullet Charm and a Luck increase. A refusal leads to Fernando's warning about bad luck and a Spirit increase.",
    92: "Emilio talks between bites of tomato. The trader rewards the praise with a seedling while Emilio keeps eating.",
    93: "A monkey snatches Emilio's banana and throws things at him. Rafael sees an opportunity for discovery in the seeds but finally distracts Emilio by offering him a local dish.",
    95: "The sight of a familiar place reminds Gerhard of his missing Katzbalger. Rafael suggests it might have found someone who appreciates it.",
    97: "Angelo asks about rogue ninja and the rumored armor. Yukihisa mistakes teasing for an insult. Rafael calms both men and the conversation returns to the possible location.",
    100: "Charles's fascination with amber bewilders a port worker. The worker still remembers a rumor about a place that gives off an amber glow on an island off the cape.",
}

# An empty English field keeps the installed wording. The optional fourth field keeps a phrase together.
DECISIONS = """
85 5|Admiral FI, should we go see Admiral Adernkatz again?|go see;Admiral Adernkatz|The sailor tentatively suggests a second approach while retaining Rafael's address and substitution.
85 11|||Yes accepts the suggestion and fits the original short answer slot.
85 13|||No defers the visit through the original negative slot.
85 20|||Rafael accepts the crew's need for help and decides to make this visit alone.
85 25|||The knock is formal and Rafael gives both parts of his substituted name.
85 29|||Gerhard's small pause makes the recognition understated.
85 33|I've done what I could to learn. Please, will you help us?|Rafael's earnest request keeps his effort without the awkward invitation to lend strength.
85 37|...Well, I can see you've been training.|Gerhard acknowledges Rafael's preparation without overstating how far he has come.
85 40|I haven't had a peaceful night since you came. I couldn't get your words out of my head.|The initial visit and the words that kept Gerhard up carry his change of heart.
85 43|Then you'll...?|Rafael jumps hopefully to an unfinished question as Gerhard considers joining.
85 48|Very well. I'll come aboard your ship.|Gerhard's formal assent lands simply at the close of the second visit.
85 55|||The alternate branch postpones the matter without refusing Gerhard's help permanently.
86 5|A sailor's first stop in the Caribbean is for a glass of rum! Come on, off to the tavern.|a glass of rum!|Julio treats the drink as a sailor's tradition and ushers the crew along.
86 9|||Julio's stammer contrasts with his confidence about the tavern.
86 21|||Cesare's escalating list is still a good panicked comic reaction.
86 24|Oh, quit yelling already!|Claudio shouts over Cesare's escalating panic.
86 31|That gave me a scare!|Rafael reacts to the blast in the familiar voice he uses with the crew.
86 36|Oh, great. That fool with the bombs again...|The shipwright is exasperated because the noise is recurring.
86 48|||Cristina seizes on the word bombs and stammers in surprise.
86 55|||The shipwright mockingly repeats Charles's nickname instead of endorsing it.
86 58|Blast Wizard? What a lousy name.|Claudio is blunt about the nickname the shipwright just quoted.
86 61|What's he like?|Rafael asks about the person behind the local commotion.
86 66|Charles the Eccentric? I'd rather not get into it.|The shipwright recognizes whom Rafael means but would rather avoid the conversation.
86 70|||Rafael's puzzled reaction gives the shipwright space to explain despite his reluctance.
86 75|There's a fellow at the workshop outside town. Studies explosives and cannons. Every so often, the rest of us have to hear about it.|The shipwright locates Charles and complains sarcastically about hearing his work.
86 78|Julio, if he knows how to make bombs, he must know about cannons too, right?|Rafael asks Julio to confirm a tentative connection, leaving room for his qualification.
86 83|||Julio makes the necessary distinction and then concedes the skills are related.
86 95|By my calculations, he'd make a very substantial contribution to our ship's fighting power.|Cesare's pompous calculation is about their ship's combat strength.
86 102|So he might come in handy.|Claudio boils down Cesare's calculation in his usual plain language.
86 105|Oh! You're sailors? You mean you'd take him out of town?|The shipwright spots an opportunity to have Charles taken elsewhere.
86 117|Out of town, huh? I suppose the middle of the ocean qualifies...|Janus dryly points out that at sea certainly counts as elsewhere.
86 124|I guess it does.|Rafael agrees tentatively with Janus before the shipwright can hide his relief.
86 129|Oh, that's exactly what I've been waiting for! I mean, I'm sure he'll be a great help to you!|The shipwright blurts out his relief before changing the pitch to Charles's merits.
86 133|Is it just me, or is this getting weird?|Claudio catches the shipwright's eagerness without guessing his motives outright.
86 138|||The shipwright calls Charles by name and expects him to answer.
86 143|Oh, hello, sir. And thank you for the other day.|thank you|Charles is amicable and explicitly refers back to their earlier encounter.
86 147|Spare me the greeting. You've gone and done it again!|The shipwright brusquely cuts off Charles's greeting because another blast just happened.
86 150|Like I told you before, it's not a failure! I'm this close to getting it right. For one thing...|Charles insists the work is close to success and starts an argument the shipwright cuts off.
86 153|All right! I get it, I get it. I didn't come to complain.|The shipwright repeats himself to stop Charles from giving another explanation.
86 157|You've got visitors. Seems they want a word with you.|He finally introduces the crew and lets them state their business.
86 160|||Rafael's brief greeting fits the awkward first introduction.
86 165|||Charles's puzzled question fits a meeting arranged without warning.
86 168|Just hear them out! I'm sure it's good news for you, too. Absolutely sure!|His repetition lays on the sales pitch before he leaves them with Charles.
86 172|||The shipwright's quick goodbye completes his exit once the handoff is made.
86 176|Oh, wait! Siiir!|Charles calls out and draws out the polite address as the shipwright leaves.
86 180|Science must be a bit much for him. I suppose I can't blame him for not understanding.|Charles sincerely misses the point even as he imagines being generous.
86 184|You're the one I can't make sense of...|Claudio undercuts Charles's self-assurance under his breath.
86 187|||Charles hears a remark but cannot make it out.
86 199|N-no! N-nothing! (Clau! You can't help yourself, can you?)|Janus stammers aloud, then privately calls out his shipmate for speaking out of turn.
86 205|Uh, we heard someone here knew about bom... er, gunpowder and cannons...|Rafael catches himself about to repeat the shipwright's unflattering choice of word.
86 210|That's what I'm studying! Oh! Are you from the Academy?|Charles immediately recognizes his own subject and guesses at the visitors' affiliation.
86 213|||Charles's matter-of-fact appraisal and second guess are the inadvertent insult.
86 217|Hey! Who asked you to size us up? You can't just say whatever you like!|Claudio takes offense at being assessed so freely.
86 221|Uh, don't mind him. We came to ask you to join us.|Rafael tries to defuse Claudio's objection and gives the real reason for the visit.
86 225|We're sailors. We travel the world. We could really use your talents in our fleet.|We travel the world.|Rafael explains their work and makes the invitation about Charles's specific skills.
86 230|Ah, sailors. I see, I see... Tell me, are you interested in science?|Charles considers the unexpected invitation and pivots straight to his favorite subject.
86 234|||Rafael's echo marks the sudden change of subject.
86 239|Science is absolutely wonderful!|Charles's delight is emphatic and immediate.
86 243|||Rafael's filler lets Charles press on without falsely endorsing the lecture.
86 248|Science starts when you ask, 'What would happen if I did this?' Then you try it for yourself.|What would happen|Charles connects curiosity to hands-on experience in the same order as the example.
86 251|That's how we make progress. We keep running experiments!|The second line moves from a single experiment to progress through repetition.
86 262|||Janus's polite doubt makes a natural foil to Charles's confidence.
86 269|It's the same with sailing! Curiosity, courage, and the will to act open up the world...|Charles sees the three qualities in navigation and gathers momentum.
86 272|Just think how wonderful that is! Sailing is science!|The enthusiasm culminates in Charles's discovery of a reason to accept.
86 275|I'm not sure I follow, but does that mean you'll come with us?|Rafael steers the conversation back to his invitation.
86 280|||Charles accepts outright and celebrates it in terms of science.
86 283|||Claudio's aside echoes what he said when Charles misunderstood the shipwright.
87 5|So this is Zipangu. The culture here is one of a kind.|Rafael takes in the unfamiliar culture and uses the historical place name in the source.
87 10|What's with those haircuts? Do they have any sense of style?|Claudio's rude reaction sets up Julio's reminder about cultural differences.
87 21|Now, now. Every culture has its own idea of what's beautiful.|Julio asks Claudio to consider a local aesthetic instead of judging by his own.
87 25|||Claudio concedes without sounding wholly persuaded.
87 32|Well, well! Southern barbarians, are you?|Southern barbarians, are you?|Kurushima opens with the insulting historical label that marks the crew as outsiders.
87 35|||Kurushima couples the mock accusation with his own country's familiar epithet.
87 39|Uh-oh, FI... Looks like this guy's got his eye on us.|Looks like|Claudio recognizes that the stranger has singled them out.
87 42|||Rafael initially tries to avoid the quarrel.
87 55|||Julio reinforces Rafael's instinct to steer clear.
87 62|||The henchman's loudly reported pain starts the staged collision.
87 66|Look at that! You ran into my man on purpose! You've broken one of his bones. What a mess!|Kurushima asserts intent and an injury as his own claims in the shakedown.
87 70|||Rafael stammers before challenging their version of the collision.
87 75|Don't bother, FI! You can't reason with these guys.|Claudio tells Rafael the explanation is pointless with these particular men.
87 87|||Julio's dry comment answers his earlier warning after trouble finds them anyway.
87 93|Oh, you wanna fight? Boss, first they bump into us, now they're looking for a fight!|The henchman turns the accusation into a pretext for violence.
87 97|Heaven might let that slide, but I, Kurushima, won't have it! Get them!|Use the Japanese appeal to Heaven and keep Kurushima's theatrical declaration of his name.
87 101|You got it, boss!|The henchman answers a superior's order in his rough voice.
87 106|What do we do? There are a lot of them. Can we take them?|Rafael worries specifically that they're outnumbered.
87 111|Outnumbered or not, we've got to fight. Julio, get behind me!|Claudio commits to a fight and protects Julio. The familiar age address does not imply kinship.
87 115|||Yukihisa's courteous declaration cuts into the brawl.
87 119|||Rafael's baffled reaction leaves room for Yukihisa to take over.
87 129|||Yukihisa takes responsibility tersely without boasting.
87 133|What? A samurai taking the barbarians' side?!|The henchman repeats the same prejudice after a samurai intervenes.
87 137|||Yukihisa's formal answer asserts his own judgment of right and wrong.
87 141|||Kurushima lashes out and rallies the men against the newcomer.
87 145|On it, boss!|The second acknowledgment follows Kurushima's redirected order.
87 150|||The first cry is a brief reaction to the blow.
87 154|||The drawn-out defeat cry makes sense after the first yell.
87 158|||Kurushima's short threat marks his retreat without specifying retaliation.
87 162|||Yukihisa explains the use of the back of the blade and assures them no one was cut.
87 166|Th-that was incredible. I couldn't even see your sword move!|Rafael stammers in admiration as he describes the speed of the blade.
87 170|Y-yeah... You surprised me, too.|Claudio's stammer recalls that he was expecting to fight, while yielding to Yukihisa's skill.
87 182|The wonders of the East, indeed!|Julio marvels at what he has just seen, using a period-flavored expression of wonder.
87 189|You have seen a shameful side of my country. Please accept my apologies.|Yukihisa formally regrets what the visitors have witnessed.
87 192|||Rafael answers the apology with gratitude for the rescue.
87 197|Forgive me for asking, but do you sail all over the world?|Yukihisa politely tests his impression before asking to come along.
87 200|If I may, I would like to sail with you.|The request is formal and conditional on the captain's agreement.
87 203|I wish to see the world for myself.|Yukihisa explicitly gives his reason for wanting to go.
87 206|||Rafael welcomes him while making it clear the ship will not return to Japan soon.
87 210|I have no intention of returning to Japan. A man should see what he's made of out in the wider world.|returning to Japan.;what he's made of|Yukihisa names his homeland and expresses his own ideal as the reason he wants to test himself.
87 213|||Rafael accepts and introduces himself with both name substitutions.
87 217|||The introduction retains the established full spoken name rather than expanding the short nameplate.
88 8|||Rafael's trailing wonder allows Claudio to react before the crown is named.
88 13|Whoa... Look at that.|Claudio's unguarded awe sounds distinct from Rafael's next comment.
88 17|It's... just magnificent, isn't it?|Rafael's slow appraisal invites agreement before Claudio changes the subject.
88 22|Wait a second. If we found it first, where's that Julian fellow?|Claudio realizes their discovery means they somehow got ahead of Julian.
88 25|||Rafael speculates about passing him without inventing where it happened.
88 31|||Julian recognizes what Rafael is holding and has trouble finishing the sentence.
88 35|||Claudio recognizes the very person they were discussing.
88 39|You're Julian, right? Good to meet you. I'm FI.|Good to meet you.|Rafael introduces himself after overhearing Julian previously, with the name substitution intact.
88 44|||Julian is surprised to be recognized and checks whether they have met.
88 48|Not face to face. We were nearby when you were talking to Mihwa at the tavern in Hangzhou.|Claudio identifies the location and explains that it had been an overheard conversation.
88 52|We overheard you talking about the Silla Gold Crown. It sounded interesting, so we came here to look for it, too.|Rafael owns the decision to look for the crown and keeps the item-card name.
88 57|||Julian's short incredulous reaction gives way to a specific grievance.
88 61|That's awful... I was going to give it to her!|Julian mourns losing his planned gift to Mihwa, without blaming anyone beyond his outburst.
88 65|Now I'll look like a complete fool! How am I supposed to face Mihwa?|Julian fears embarrassment and repeats what is at stake for him personally.
88 68|Uh-oh, FI. What do we do now?|What do we do now?|Claudio hands the awkward decision to Rafael, whom the player controls.
88 73|||The short caption matches handing the crown to Julian so he can give the gift.
88 75|||The short caption keeps Rafael as the giver in the other original choice.
88 82|Uh, please don't get the wrong idea. We saw how much this meant to you. We thought we'd help from the sidelines...|Rafael offers an awkward face-saving explanation for why they found it.
88 87|||Julian's stammer moves from dismay to hopeful disbelief.
88 91|That's right. Here, go give it to Mihwa.|Rafael confirms the explanation and urges Julian to present his gift.
88 96|This is wonderful! We barely know each other and you'd do this for me? You're too kind. Now, if you'll excuse me!|Julian's surprised gratitude tumbles into a hasty departure.
88 100|Hey, wait... He's already gone. That guy can move!|Claudio tries to get a word in and marvels at Julian's speed.
88 103|It's all right. We got to see the crown. He needs it more than we do.|Rafael is satisfied with seeing the find and explains why he gave it away.
88 108|||Claudio's familiar teasing expresses affection through the complaint.
88 118|I'm sorry, but I want to give the Silla Gold Crown to Mihwa myself.|Rafael apologizes before being direct about which of them will give the crown.
88 123|What?! I have a rival! I can't just stand here. I have to think of something else, and fast!|Julian calls Rafael a rival himself and rushes off to find an alternative.
88 126|||Rafael tries to stop Julian without pretending his interpretation is correct.
88 131|He sure moves fast. Gone already.|Claudio notices the same sudden departure on the other branch.
88 135|||Rafael questions what he has done instead of dismissing Julian's reaction.
88 140|No, come on. He got here late. That's on him. Let's go.|Claudio comforts Rafael with the simple argument that Julian arrived too late.
90 5|Whew...|Janus sighs reflectively before Rafael asks what's on his mind.
90 9|What's on your mind, Janus?|Rafael asks after Janus rather than assuming something has gone wrong.
90 14|Oh, Admiral... There's nothing like a good ship, is there?|Janus greets his admiral and voices an unexpected fondness that prompts Rafael's reaction.
90 18|||Rafael's puzzled sound leaves room for Janus to explain his daydream.
90 23|If I ever had a fleet of my own, I'd want to trade in the Mediterranean.|Janus names his preferred trading region in a hypothetical about leading his own fleet.
90 27|Why the Mediterranean?|Rafael echoes the region and asks about Janus's reasoning.
90 32|No waters have more variety. All kinds of ships call at ports in different countries. It's exciting just thinking about it!|Janus pictures both the ships and the ports and gets more excited as he speaks.
90 35|All right. When I put you in charge of a regional fleet, I'll give you the Mediterranean.|Rafael makes a conditional assignment and keeps the established regional fleet term.
90 40|Really? I'd love that. No hurry, of course. Just don't forget, all right?|don't forget, all right?|Janus is delighted and politely leaves the timing to Rafael.
90 43|||Rafael's unceremonious promise answers Janus's request directly.
91 5|||The stranger singles out a captain without claiming to know Rafael's identity.
91 9|||Rafael's surprised question confirms the stranger picked him out.
91 14||believe in miracles?|The question stays direct and the belief phrase should be read together before the two answers appear.
91 19|||The positive reply echoes the question and keeps the affirmative branch.
91 21|||The negative reply echoes the positive caption and keeps the refusal branch.
91 28|Really? You don't meet many people who believe in miracles these days. You don't sound like a captain a crew can count on.|The stranger sounds surprised, then questions whether Rafael is someone his crew can rely on.
91 32|||Fernando jumps to the defense of his own admiral and speaks with his usual bluntness.
91 35|||The stranger provokes Fernando by asking if the criticism is wrong.
91 39|Why, you...!|Fernando's unfinished threat preserves the escalation before the stranger interrupts him.
91 43|Still, some people refuse to believe in miracles and end up shipwrecked! You're a lot better than that!|The man abruptly defends believers, showing how much the stakes of the question matter to him.
91 47|||Fernando's bafflement gives the man room to change his tone.
91 51|Sorry. I didn't mean to raise my voice. I wasn't trying to insult your captain.|The man apologizes specifically for shouting and clarifies his intent.
91 55|||Fernando still cannot figure out what the stranger wants.
91 59|Truth is, I've been looking for a captain who believes in miracles. I want you to have this.|The stranger gives the two parts of his motive while moving to the gift.
91 62|I've been asking every time a ship comes in. You're the hundredth.|Keep the repetition at arrivals and the exact count of the people he has stopped.
91 66|What is it?|Fernando's question invites the man to identify the object he is offering.
91 70||Miracle Bullet Charm.|The installed item name and the claim that it brings miracles should stay intact.
91 73|||Rafael treats the gift with care and checks that the man genuinely means to part with it.
91 77|I do. I want someone like you to have it. It was my lucky charm, but... I can't go to sea anymore.|The man gives the charm because he is no longer able to sail, with his hesitation intact.
91 80|...All right. I'll take it. Thank you.|Rafael hesitates, accepts the gift, and ends with sincere thanks.
91 88|||The first reward names Rafael by substitution and raises Luck by exactly one.
91 91|||Fernando receives the same one-point Luck increase under his own name.
91 98|We're asking for bad luck if we stick around this guy. Let's get out of here.|Let's get out of here.|On the refusal branch Fernando treats the stranger as an omen and urges Rafael to go.
91 101|Y-yeah.|Rafael's hesitant answer goes along with Fernando's sudden push to leave.
91 109|||The refusal reward keeps Rafael's substituted given name and the one-point Spirit increase.
91 112|||Fernando receives the same one-point Spirit increase on the refusal branch.
92 5|These tomatoes are good! Munch, munch.|Emilio starts eating straight away and the double chewing sound establishes the joke.
92 8|Yeah, they are.|Rafael casually agrees before Emilio keeps talking between bites.
92 13|At first I thought it was an apple. Munch, munch.|Emilio recalls mistaking the tomato for an apple without pausing his chewing.
92 16|You did?|Rafael questions the comparison with a short reply that leaves the rhythm intact.
92 21|It's so sweet! Munch, munch.|Emilio singles out the sweetness and carries on eating.
92 24|||Rafael privately notices how much Emilio is eating. The short aside keeps its timing.
92 29|Ha ha! You two really took to those tomatoes, didn't you?|The trader is amused by both visitors and their reaction to the local produce.
92 32|Well, if you like them that much, here. Take this.|The trader makes his gift a direct response to their enthusiasm.
92 35|||Emilio asks what the trader gave them before the object is identified.
92 39|||The trader gives the precise name of the gift, a tomato seedling.
92 43|Are you sure?|Rafael checks whether the trader really wants to give the plant away.
92 48|Of course. It's good to hear someone say such nice things about the tomatoes we sell.|The trader is proud of the produce he sells and explicitly ties his generosity to the compliment.
92 52|||Rafael's brief thanks lets Emilio have the comic closing beat.
92 57|Lucky us, Admiral! Munch, munch.|Emilio is pleased by the gift and still has a mouthful at the same time.
92 61|... (He's still eating.)|Rafael's private observation pays off the repeated chewing sound.
93 5|||The first voice-only monkey sound sets up Emilio's startled response.
93 9|||Emilio's two brief cries make it clear the noise caught him off guard.
93 13|||The repeated sound stays separate from Emilio's effort to drive the animal off.
93 17|Hey, you! Get out of here!|Emilio tries to shoo it away before his banana is taken.
93 21|||The third matching sound repeats the animal's interruption just before Emilio calls for his banana back.
93 25|Hey! Give that back!|Emilio's demand comes immediately after the theft.
93 29|||Rafael asks what happened and what Emilio is doing without yet knowing about the thief.
93 33|It took my banana! Something snatched it right while I was eating!|Emilio blurts out the loss and then clarifies what he meant by it.
93 37|||Rafael echoes the unspecified culprit, letting Emilio try to point it out.
93 42|That thing over there... It's gone! Hey, come baaack!|Emilio looks where it was, then stretches out his shout as he gives chase.
93 45|||Rafael checks the outcome of the chase without assuming Emilio caught it.
93 50|It's too quick for me! And it throws things at me. Rocks and seeds and stuff.|Emilio reports both why he could not catch it and what it throws at him.
93 54|Let's see... I've never seen some of these seeds before. This might be quite a discovery!|Rafael looks at the debris and sees possibilities that Emilio has no interest in.
93 60|Forget the seeds! Give me back my banana!|Emilio answers the discovery with the same priority he had before.
93 64|Give me back my banana! Give me back my banana!|Give me back my banana!|Preserve both full demands to land the comic repetition before Rafael intervenes.
93 68|...Emilio, want to try the local specialty?|Rafael changes the subject with a food offer to distract Emilio.
93 73|||Emilio perks up only enough to ask who is paying.
93 77|||Rafael agrees to pay in the same plain words Emilio just used.
93 86|||Emilio's delight shows the offer immediately displaces his anger.
95 5|||Gerhard suddenly recognizes the location and trails off.
95 8|||Rafael asks about Gerhard's reaction without guessing the reason.
95 13|It's nothing. This place just brought back a memory...|Gerhard describes a recollection that arose on returning here.
95 16|A memory?|Rafael picks up Gerhard's last word to encourage the rest of the story.
95 21|||Gerhard places the loss in a fight with pirates nearby.
95 24|||Rafael echoes the unexpected object before Gerhard describes it.
95 29|Yes. Just an old Katzbalger, but it handled better than you'd think to look at it. It was my favorite for years.|Gerhard contrasts the sword's appearance with its use and says how long it was his favorite.
95 32|So the search turned up nothing?|the search turned up nothing?|Rafael gives him time and asks whether the search turned up the sword.
95 36|No sign of it anywhere. A local fisherman probably picked it up and sold it for next to nothing.|Gerhard has no physical trace of the sword and offers a guess about a cheap sale.
95 39|You think so? If it was that good a sword, I bet someone's taking good care of it.|Rafael offers a more hopeful possibility without claiming to know what happened.
95 44|You rarely come across a sword like that. I'd feel a little better if I knew it was in the hands of someone who appreciated it...|Gerhard admits the comfort of Rafael's suggestion while leaving the sword's fate open.
97 5|Admiral, what's a rogue ninja?|Angelo directs the opening question at Rafael and uses the term explained in the next replies.
97 9|||Rafael's echo shows he needs the same explanation as Angelo.
97 14|Someone who used to be a ninja.|Yukihisa initially gives the short definition before Angelo asks the obvious follow-up.
97 18|Oh, a ninja! ...So what's a ninja?|Angelo sounds as if he understands before admitting he does not.
97 21|In Japan, there are clans that specialize in moving and working unseen.|Yukihisa gives the concrete meaning of covert activity in the context of their clans.
97 24|So, a Japanese spy. You ever meet one?|Angelo puts it in his own terms and asks about an encounter.
97 28|||Yukihisa says he has never met one and explains the rule about exposed identities.
97 32|||Angelo's Italian exclamation is his own startled reaction.
97 36|Leaving the clan means risking your life. Any ninja who gets away while the clan is hunting them must be exceptionally skilled.|Yukihisa connects the danger, the pursuit, and the skill needed to become a successful fugitive.
97 39|||Yukihisa asks why Angelo has brought up deserters after finishing the explanation.
97 43|Well, it's their outfit I heard about, actually.|Angelo clarifies that the rumor concerns what they wear.
97 47|It's all black. They call it Ninja Garb, but get this. It's armor!|Ninja Garb,|Keep the established item name and preserve the surprising reveal that it serves as armor.
97 51|||Yukihisa echoes the detail that surprises him.
97 55|I don't know the details. All I heard was that it's really light and tough.|Angelo separates his lack of detailed knowledge from the two qualities in the rumor.
97 58|Ah. I've never heard of such a thing.|Yukihisa admits the gap in his knowledge in his more formal voice.
97 61|I wonder if it's rare. Even Yukihisa's never heard of it, and he's from Japan.|Rafael wonders aloud whether the item is rare. He does not assert that every Japanese person should know it.
97 66|||Yukihisa takes the lack of knowledge personally and feels he owes them an apology.
97 70|||Angelo's immediate reassurance names Yukihisa and leaves room for his objection.
97 73|||Yukihisa's unfinished objection allows Angelo to take back responsibility for bringing it up.
97 77|I'm the one who brought it up, anyway. You're a funny one, Yukihisa.|You're a funny one, Yukihisa.|Angelo owns the question and uses casual teasing that Yukihisa can hear as an insult.
97 80|Funny? ...What do you mean by that? If you mean to insult me, I won't stand for it.|Yukihisa repeats the ambiguous word, asks for clarification, and warns Angelo about his interpretation.
97 84|Oh, yeah? What are you gonna do about it?|Angelo treats the warning as a challenge.
97 88|Hey, both of you, stop. This is nothing to fight about.|Rafael interrupts and lowers the stakes of their argument.
97 93|...I am sorry.|Yukihisa's quieter pause brings down the tension after Rafael steps in.
97 97|||Angelo also takes responsibility in his own short, casual voice.
97 100|Still... If that black armor really exists, it must be somewhere in Japan.|Yukihisa returns to the practical clue while leaving the rumor unconfirmed.
97 103|||Rafael gives a qualified agreement before Angelo suggests looking.
97 108|That's what I think, too. Let's look for it when we have some time.|Angelo agrees and suggests looking when they have a chance, without making it urgent.
100 5|||The worker spots the goods and asks directly whether the crew deals in amber.
100 9|We do. Looking at that glow makes me feel like I'm back in the ancient world.|Charles describes how the glow takes his imagination into the past.
100 13|Huh? What's that supposed to mean?|The worker's bewilderment lets Charles launch into the explanation he would give anyway.
100 17|Amber is sap from an ancient tree. It hardened and became a gemstone.|Charles explains where amber comes from in plain terms before his language becomes more fanciful.
100 21|See the bee in there? It's been asleep for thousands of years in its own little sepia world. Isn't that mysterious?|It's been asleep|Charles keeps the bee, the time scale, and his fanciful miniature world.
100 24|How come you know all that fancy stuff, kid?|The worker is put off by the learned words and addresses Charles familiarly without implying kinship.
100 27|Science! We use what we know to try to make a little sense of miracles beyond our understanding.|Charles explains the ambition and the limits of scientific knowledge in an enthusiastic voice.
100 30|I didn't get a word of that. Oh, wait. Speaking of amber, I just remembered something.|The worker shrugs off the lecture but has a useful rumor of his own.
100 34|||Charles's short question invites the worker to give the information he remembered.
100 38|There are a few islands off this cape. I hear there's a strange place on one of them that gives off an amber glow.|The worker gives the geographic lead and treats the site and glow as hearsay.
100 41|An amber glow? Could it be a vein of ore?|Charles offers a tentative explanation for the strange color.
100 45|Couldn't tell you what it is. It's only a rumor, anyway.|The worker plainly says he cannot identify the place or its glow.
100 49|I see. Thanks for the tip. Now you've piqued my scientific curiosity!|scientific curiosity|Charles thanks the worker for going out of his way and ends in his characteristic scientific voice.
"""


def main():
    assert not OUTPUT.exists()
    packet, previous, release, names = map(base.load, (SOURCE, PRIOR, parent.RELEASE, NAMES))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    earlier = {(row["block"], row["source_reference"]["offset"]): row for row in previous["records"]}
    speakers = {row["actor_ID"]: row["english"] for row in names["records"]} | {None: "Rafael Castor", 254: "System panel"}
    decisions = {}
    for line in DECISIONS.strip().splitlines():
        fields = line.split("|")
        key = tuple(map(int, fields[0].split()))
        assert key not in decisions, key
        if len(fields) == 3:
            _, replacement, note = fields
            phrases = []
        else:
            _, replacement, phrase_text, note = fields
            phrases = phrase_text.split(";") if phrase_text else []
        decisions[key] = replacement, phrases, note
    records, plans, failures = [], {}, []
    for group in packet["groups"]:
        block, path = group["block"], group["file_path"]
        for entry in group["records"]:
            number, selector = entry["source_record_index"], entry["selector"]
            old = earlier.pop((block, entry["source_offset"]))
            assert entry["Japanese"] == old["source_Japanese"] and selector == old.get("source_selector")
            assert all(old["review"].values())
            replacement, phrases, note = decisions.pop((block, number))
            current = logical(entry["current_English"])
            english = replacement or current
            assert english.isascii() and logical(english) == english
            assert all(phrase in english for phrase in phrases)
            assert TOKEN.findall(entry["Japanese"]) == TOKEN.findall(current) == TOKEN.findall(english)
            prefix = "" if selector is None else f"{selector:02x}"
            refs = {side: dict(file_path=path, block=block, offset=entry[f"{side}_offset"],
                               command_offset=entry[f"{side}_command_offset"],
                               archive_sha256=group[f"{side}_archive_sha256"], block_sha256=group[f"{side}_block_sha256"],
                               exact_hex=prefix + entry[f"{side}_body_hex"])
                    for side in ("source", "current")}
            assert old["source_hex"] == refs["source"]["exact_hex"]
            kind = "typed-choice-label" if selector is None else "system-FE" if selector == 254 else "progressive"
            assert kind == old["kind"], (old["id"], kind, old["kind"])
            different = english != current
            row = dict(id=old["id"], file_path=path, route=0, block=block, source_record_index=number, kind=kind,
                       native_command_word=entry["native_command_word"], native_slots=entry["slots"], source_selector=selector,
                       source_reference=refs["source"], current_reference=refs["current"],
                       source_hex=refs["source"]["exact_hex"], current_hex=refs["current"]["exact_hex"],
                       Japanese=entry["Japanese"], previous_English=current, english=english, speaker=speakers[selector],
                       context=CONTEXTS[block], source_meaning=old["source_meaning"], localization_note=note,
                       protected_phrases=phrases, decision="revision" if different or phrases else "retention",
                       finding="wording" if different else "wrap" if phrases else "retention",
                       review=dict.fromkeys(GATES, True) | {"formatting": False})
            if row["decision"] == "revision" and kind == "progressive":
                jp, en = (bytes.fromhex(entry[f"{side}_body_hex"]) for side in ("source", "current"))
                try:
                    body, plan = plan_progressive(row, selector, en, jp)
                    if body.rstrip(b" ") == en.rstrip(b" "):
                        assert not different
                        row.update(decision="retention", finding="retention")
                    else:
                        plans[row["id"]] = plan
                except (ValueError, AssertionError) as error:
                    failures.append((block, number, english, phrases, str(error)))
            records.append(row)
    assert len(records) == 261 and not decisions and not earlier
    assert not failures, failures
    counts = dict(Counter(row["finding"] for row in records))
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), status="Contextual review complete. Native display and release verification pending.",
        previous_sha256=packet["candidate_sha256"], previous_registry_sha256=release["registry_sha256"],
        source_packet=str(SOURCE), source_packet_sha256=base.digest(SOURCE),
        earlier_contextual_reviews={str(PRIOR): base.digest(PRIOR)}, scoped_name_precedent={str(NAMES): base.digest(NAMES)},
        records=records, plans=plans, findings=counts, new_editorial_credit=0))
    print(f"Reviewed {len(records)} records across {len(BLOCKS[0])} complete exchanges. {counts}.")


if __name__ == "__main__":
    main()

