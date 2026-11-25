"""Review the royal audience, pirate hunt, and ancestral ruins commission."""

from scripts import review_hodram_B265_B280_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = previous.base, previous.ROOT
OUTPUT = ROOT / "B281_B289_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    281: "Hodram remembers Hernan's whereabouts. The guildmaster repeats the order to deal with the pirate.",
    282: "At court, the king asks Hodram to protect the kingdom's merchants from Iscal Yasar, whose fleet has defeated the forces already sent against him.",
    283: "The king rewards Hodram and asks him to gather all seven Proofs of Conquest. Outside the audience, Hodram and his officer discuss how the Proofs could validate their claim to the strongest fleet.",
    284: "A messenger tells Hodram the king wants him back in Stockholm immediately. Hodram and his officer wonder why.",
    285: "Hodram remembers the king's assignment to defeat the Indian Ocean pirate Iscal.",
    286: "The guildmaster describes William's rise and asks Hodram to stop him. Hodram accepts and tells his officer how he plans to draw William out.",
    287: "The Havana guild pays Hodram for bringing in William and introduces a man seeking his ancestors' ruins. He calls Hodram a worthy candidate and then frankly explains that many others have also tried.",
    288: "The port worker checks the captain's surname and says the Havana guild was looking for him.",
    289: "Hodram recalls the hunt in the New World. Two guild reminders distinguish whether William has emerged from whether he has been captured.",
}
DECISIONS = {
    281: """
12|Hernan's prowling the Mediterranean. I'd better stop him.|prowling the Mediterranean.;I'd better stop him.|Hodram remembers where the pirate is and that he is to defeat him.
24|Get out there and deal with that bastard Hernan!|that bastard Hernan!|The guildmaster presses Hodram to take immediate action against Hernan. Keep his coarse address.
""",
    282: """
6|Admiral FA, His Majesty summons you.|His Majesty summons you.|The court attendant formally addresses Hodram by rank and the surname token and passes on the king's summons.
9|Ah, Admiral FA. I have a favor to ask of you.|I have a favor;to ask of you.|The king recognizes the admiral and turns to a particular personal request. Preserve the rank and surname token.
12|Thanks to your efforts, our ships can now sail beyond the Indian Ocean. And yet...|Thanks to your efforts,;beyond the Indian Ocean.;And yet...|The king credits Hodram with extending the reach of the country's shipping. His hesitation leads to the problem.
16|A powerful enemy has appeared in Arab waters. Our merchant fleets have suffered heavy losses. I want you to defeat him.|in Arab waters.;heavy losses.;defeat him.|The king describes the enemy's region and the losses inflicted on merchant fleets, then asks Hodram to stop him.
19|His name is Iscal Yasar, an Arab pirate. He's defeated fleet after fleet sent against him. You are our last hope. I am counting on you.|Iscal Yasar,;an Arab pirate.;sent against him.;You are our last hope.;I am counting on you.|The king names the pirate and stresses that previous expeditions were defeated. His closing appeal shows how deeply he is relying on Hodram.
""",
    283: """
6|||The court attendant formally welcomes the admiral back and uses the surname substitution.
9|FA! You've defeated our mighty foe. Well done!|our mighty foe.;Well done!|The king uses the surname alone and openly praises Hodram for defeating the formidable enemy.
12|Bring forth his reward!|Bring forth his reward!|The king orders the reward brought forward. The command leads directly to his offer.
16|This hardly repays what you've done for us, but I ask that you accept it.|repays what you've done for us,;that you accept it.|The king says the reward may fall short of Hodram's service and asks him to accept it. Keep the courteous royal register.
19|||The panel gives the exact reward of 250,000 gold coins and preserves the celebratory exclamation.
28|||The king changes the subject, calls Hodram by the surname token and asks how his existing mission is proceeding.
31|||The formal response acknowledges the question without supplying details the king has yet to ask for.
35|Hmm. Have you settled the most important question yet?|the most important question yet?|The king doubts that the central point has been settled and prompts Hodram to think about it.
39|What would make the fleet you're building the strongest in the world?|the fleet you're building;the strongest in the world?|The king asks what standard could establish the fleet Hodram seeks as the strongest.
42|||Hodram asks the king to explain what he means. The respectful address and brief question fit his confusion.
45|Anyone can claim the title. Surely it means something only when everyone agrees that you are the strongest.|Anyone can claim the title.;only when everyone agrees;you are the strongest.|The king distinguishes self-proclamation from broad recognition. Keep his rhetorical invitation to agree.
48|Everyone would have to agree...|Everyone would have to agree...|Hodram picks up the need for recognition and considers it before the king explains the Proofs.
52|Exactly. Have you heard what the great powers seek as proof of who is strongest?|Have you heard;the great powers seek;who is strongest?|The king confirms the point and asks about the symbols coveted by the great powers. He leaves their name for Hodram to supply.
56|||Hodram tentatively recognizes the established name Proofs of Conquest. The pause suits his question.
60|Ah. So you've heard of them.|you've heard of them.|The king acknowledges that Hodram already knows what he has in mind.
64|Yes, the very same Proofs of Conquest said to be scattered across the world.|Proofs of Conquest;across the world.|The king confirms he means those Proofs and presents their distribution as what people say.
68|||The king attributes the qualification rule to hearsay and gives one Proof to the person worthy to rule its sea region.
72|||The king says that gathering all seven would demonstrate the kingdom's power at home and abroad. The measured language suits him.
76|||The king calls on Hodram to achieve the feat and bring Sweden into the ranks of the great powers.
80|Yes, Your Majesty!|Yes, Your Majesty!|The formal acknowledgment answers a royal command, with new force compared with the earlier quiet reply.
85|The Proofs of Conquest... So now it's a royal order to hunt for treasures we barely understand.|The Proofs of Conquest...;a royal order;we barely understand.|Outside the audience, Hodram considers how little they know about the treasures the king has just ordered them to collect.
89|His Majesty seems convinced, but do these Proofs really mean as much as he says?|His Majesty seems convinced,;as much as he says?|The officer questions the significance of the Proofs after the king's assertion. His skepticism stays respectful.
93|I don't know. I doubt so many powerful people in different countries would be this desperate to find something worthless...|I don't know.;in different countries;something worthless...|Hodram weighs the desperate interest of powerful people across countries and trails off before qualifying his thought.
97|Then again, it wouldn't be the first time we all got caught up chasing a fantasy.|it wouldn't be the first time;chasing a fantasy.|Hodram knows a widely shared obsession can still be hollow. The caveat follows his first argument.
100|||The officer pauses to consider Hodram's conflicting explanations before hearing what the assignment demands.
104|Either way, getting those Proofs means defeating powerful rivals in every sea region. They're after the same thing we are.|getting those Proofs;powerful rivals;in every sea region.;the same thing we are.|Hodram returns to the practical challenge and makes clear that the regional rivals want the same Proofs.
107|Winning a battle here and there won't be enough. We'll have to be strong on every front.|here and there;won't be enough.;strong on every front.|Hodram explains that the challenge goes well beyond local victories and requires broad, high-level strength.
111|In that sense, the Proofs really would show that our fleet is the strongest.|In that sense,;our fleet is the strongest.|Hodram concludes that the effort would validate the claim regardless of the objects' precise nature.
115|I see. Then we should treat gathering all the Proofs as the mission itself.|gathering all the Proofs;the mission itself.|The officer checks whether collecting the complete set is now the mission. His conclusion leads to Hodram's confirmation.
119|||Hodram confirms the officer has understood. The brief reply closes the exchange.
""",
    284: """
6|Admiral, His Majesty wants to see you. Please return to Stockholm at once.|His Majesty wants to see you.;Stockholm at once.|The messenger gives the king's summons and requests an urgent return to the named city.
9|||Hodram echoes the royal title in surprise, letting the officer ask what the king wants.
13|||The officer wonders at the reason for the summons. The open question conveys uncertainty about what awaits them.
""",
    285: """
6|I'd better deal with Iscal, the pirate in the Indian Ocean.|deal with Iscal,;the Indian Ocean.|Hodram remembers the pirate and the Indian Ocean lead in a current self-reminder.
""",
    286: """
5|Mr. FA, I've been looking for you. There's a gang I need you to stop.|I've been looking for you.;I need you to stop.|The guildmaster uses the surname token and urgently asks for help with the people he is about to describe.
9|A job? Who's it against?|Who's it against?|Hodram recognizes an assignment and asks for the identity of the target.
12|||The guildmaster describes the group's low origins and says they engaged in piracy and smuggling while paying tribute to Maldonado.
16|||The guildmaster explains how the gang struck out while Maldonado was dealing with the named men in Mexico and England.
19|Their leader's a pirate named William. A nasty piece of work, that one.|a pirate named William.;A nasty piece of work,|The guildmaster names William and speaks of him with personal distaste before listing his actions.
23|||The guildmaster cites attacks on immigrant and merchant ships, the killing of prisoners and the destruction of raided villages.
27|||The guildmaster uses an unfavorable comparison to make Maldonado sound almost decent by comparison with William's group.
31|They keep out of sight. They don't operate like an established faction, and William himself hardly ever shows his face.|an established faction,;William himself;shows his face.|The guildmaster explains why they are hard to find. The group has no open presence and William seldom appears.
35|||The guildmaster reports that several hunters sent to track William came back in poor shape. Keep the outcome open rather than assuming any deaths.
39|||The plea tells Hodram that the guildmaster has run out of people to ask.
43|Sounds like he'll be hard to catch... All right. I'll take the job.|be hard to catch...;I'll take the job.|Hodram weighs how troublesome William will be to reach before accepting the assignment.
46|||The guildmaster reacts with surprised relief and checks that Hodram will really take the job.
50|||Hodram says he cannot leave William's conduct unchallenged. The simple statement grounds his choice.
54|||The guildmaster welcomes the decision, hands over the advance and expresses confidence.
59|||The result panel gives the exact 25,000-gold advance.
65|||The officer asks the immediate practical question of how they will find William.
68|||Hodram admits they have no leads. Forcing William's hand leads naturally to the officer's question.
71|||The officer asks what that tactic means. The hesitation suits the unfinished explanation.
75|We take out his pirates one by one. Sooner or later he'll lose patience and show himself.|his pirates one by one.;he'll lose patience;and show himself.|Hodram proposes defeating William's subordinates in succession until he loses patience and comes out.
79|||The officer dryly sums up what the plan amounts to. Keep the concise answer.
""",
    287: """
5|||William cries out twice in inarticulate fury. The distinct bursts set up recognition by voice.
9|That voice... William! So they finally caught you.|That voice... William!;finally caught you.|The guildmaster recognizes William by his cry and reacts with relief that he has been captured.
12|||Hodram looks forward to being free of the noisy prisoner. The brief reaction follows William's outburst.
16|||The guildmaster is impressed by Hodram's skill and emphasizes that the reward is generous.
20|||The reward notice gives exactly 180,000 gold coins and keeps the source's exclamation.
46|||The separate panel gives a slight increase in Havana market share.
57|||The guildmaster pivots to an introduction rather than springing another assignment on Hodram in his own voice.
61|...Hello.|...Hello.|The stranger gives a hesitant greeting, before explaining his purpose.
65|||Hodram's puzzled pause invites the stranger to explain. Keep the silent question as a short beat.
69|I have a favor to ask. You've shown what you can do, and I need someone to find a particular ruin for us.|I have a favor to ask.;what you can do,;a particular ruin for us.|The stranger trusts Hodram's demonstrated ability and wants a specific ancestral site found.
73|||Hodram repeats ruins in surprise, giving the stranger room to tell him about them.
77|They say our ancestors built the ruins to honor their warriors.|our ancestors built the ruins;to honor their warriors.|The stranger identifies the ancestors and the purpose attributed to the site. Preserve his own community's voice and the traditional account.
80|Legend has it that only someone worthy of the name 'strongest warrior' can find them...|Legend has it;strongest warrior;can find them...|The stranger gives the test of worthiness as a legend and leaves the implication for Hodram to work out.
84|You mean you think I'm the strongest warrior?|the strongest warrior?|Hodram asks whether the stranger means him. Repeat the phrase from the legend so the response connects.
88|||The stranger says the defeat of those pirates convinced him. The compliment refers directly to the completed hunt.
92|The strongest warrior needs more than strength. He must have wisdom and a sense of what's right.|The strongest warrior;more than strength.;a sense of what's right.|The stranger explains that strength, right judgment and wisdom together make the warrior worthy. Preserve the recurring phrase.
96|Hold on. You're giving me too much credit. I can't take on a request like that...|You're giving me too much credit.;a request like that...|Hodram feels overrated and starts to decline before the stranger puts the request in perspective.
100|Please, there's no need to worry. To be honest, it feels like a long shot to us, too.|there's no need to worry.;a long shot to us, too.|The stranger reassures him and candidly describes a hope as hard to grasp as clouds. Use an idiom that conveys the same doubt.
104|We ask anyone who looks strong enough. We've been doing it whoever comes along.|who looks strong enough.;whoever comes along.|The stranger reveals that they ask one promising person after another. His frankness undercuts the initial compliment.
108|Forgive me if that sounds rude. No one has managed it yet, so we won't get our hopes too high.|if that sounds rude.;No one has managed it yet,;get our hopes too high.|He acknowledges the bluntness and reassures Hodram that the many prior failures keep expectations low.
112|At least you're honest. That takes some of the pressure off.|At least you're honest.;the pressure off.|Hodram appreciates the man's candor and feels freer to consider accepting.
115|Please accept a small advance. Of course, you won't have to pay it back if you can't find the ruins.|a small advance.;pay it back;if you can't find the ruins.|The stranger promises an advance and explicitly waives repayment if the search fails.
119|||The notice gives the exact 5,000-gold advance.
125|First, you'll need a map. Come see me when you have the Ancient City Map. I'll join you in the search.|you'll need a map.;the Ancient City Map.;I'll join you in the search.|The stranger gives the exact item name and explains that Hodram must get it before they set out together.
128|I'll be waiting at the city gate.|at the city gate.|The stranger identifies the gate of the town where they are speaking as their next meeting place.
""",
    288: """
6|||The port worker checks the name using the exact surname token, then passes on the Havana guild's message.
""",
    289: """
12|I've got to defeat William, the pirate in the New World.|I've got to defeat William,;the New World.|Hodram reminds himself of the target and the region. The task remains to defeat William.
23|William still hasn't shown his face?|shown his face?|The guildmaster specifically asks whether the elusive pirate has emerged.
28|You still haven't caught William?|haven't caught William?|The guildmaster asks whether the captain has captured William. This reminder is distinct from the one about whether he has appeared.
""",
}

review = checked_text(previous.review, {"len(records) == 80": "len(records) == 90"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::royal-audience-and-william", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
