"""Clean Japanese meanings followed by independent whole-exchange American English drafts."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/Maria_B275_B285_clean_20261110')
CONTEXTS={
275:"Sakura reports a wounded stranger. He initially resents her talking but accepts Maria's help and ship's doctor. Once the danger passes, he confesses his role in a local arms-smuggling organization: assisting foreign sellers and carrying guns to wokou pirates. Hearing a priest preach in Nagasaki made him want to quit; his former organization pursues him. Maria rejects his fatalism and infers he knows a secret. He recalls an approaching Portuguese missionary delegation seeking an audience with the Ming emperor, but does not know its arrival details. A Macau tavern informant may know. He asks to accompany Maria for safety despite his wounds. Keep the sincere priest who moved him separate from the suspected impostors revealed later. Familiar address to Sakura is not kinship, and praise for Maria's skill is not a new rank. Wokou remains the historical pirate term without an invented uniform ethnicity. Actor102's permanent name/role label is not established by this confession.",
276:"At the Macau tavern, actor102 asks the proprietor to summon the informant. The informant asks who Maria is; actor102 calls her his new boss. Information costs1,000 coins. He says the fleet arrives tomorrow in Macau, and argues that a liar would choose a week away or Hangzhou so he could escape before exposure. Actor102 plans to approach the visitors and discover why the smuggling boss forbade him from meeting them. Preserve tomorrow versus a hypothetical week, Macau versus hypothetical Hangzhou, the price and Maria's agreement. Tavern address is not a father-child relationship; the new boss is Maria, not the informant.",
277:"The delegation arrives. The supposed priest says Amen; actor102 recognizes Jacob beside him as a senior member of the smuggling organization, previously met through work. Maria infers the missionaries are likely impostors planning a lucrative state arms/contraband deal, then military investment strong enough to destroy fleets sent against them. These are her deductions, not proof of every future action. Xien suggests the Ming government's defenses might benefit, but Maria argues inexperienced officials will overpay for obsolete weapons, waste taxes and encourage future drug/slave sales. She resolves to act if the military will not believe them, and follows the delegation to the governor's office. Preserve the political argument and her protective anger, not a blanket attack on actual missionaries or a new relationship to Jacob.",
278:"At the governor's office the impostor delegation claims to represent the Jesuits and number over100. Actor129, posing as a county magistrate, dramatically denounces them; Xien backs the accusation. Guards and Maria's crew intervene, while Jacob refuses capture and flees in the action. The fooled governor later wonders where the rescuing troops went and why Ming soldiers included Westerners and Japanese. The reveal identifies actor129 as a former actor and gifted local mimic, despite the native magistrate label used in the performance. He was not silently granted an actual government appointment. Maria explains answering their disguise with one of her own; Xien expects the organization to lie low. Actor102 now commits to working aboard and Maria accepts. Preserve more than100, the Jesuit claim, the emperor's title, the later audience, the governor's embarrassment, the identity reveal and conditional consequences without inventing arrest or execution outcomes.",
279:"Maria and the recovered former smuggling associate revisit Sakura. She was worried, is relieved to see him well, and hears their account. She notices the time because she intended to visit a temple. Maria politely avoids delaying her. Sakura suggests sightseeing in Kyoto, saying a map makes it easy and she can guide part of the way. Preserve a temple rather than a Shinto shrine, a sightseeing suggestion rather than an order, and partial guidance rather than a promise to accompany the entire trip.",
280:"Eight physical personality alternatives remind the admiral to visit the clan guarding the map to the quoted Proof, in a village far northeast of China. The clean earlier clue B94R60/R63/R67/R70 says the clan fled China to the far northeast near an icy sea; do not relocate the village to northeastern China. Preserve the individual curiosity, urgency, forgetfulness concern and degrees of formality. The exact item title and dynamic actor208 still require scoped native consumer binding; Proof is provisional, not a newly approved global UI name.",
}
TEXT=r'''DK4_MES_B275_R0005|Sakura calls FI in alarm; something serious has happened.|FI! Something terrible's happened!
DK4_MES_B275_R0008|Maria asks what happened.|What's wrong?
DK4_MES_B275_R0012|A wounded person just rushed in.|A wounded man came rushing in just now...
DK4_MES_B275_R0015|The wounded man tells Sakura not to talk about him, then cries in pain.|Hey, girl! Don't go blabbing about me! Ugh... Ow, ow, ow!
DK4_MES_B275_R0019|Sakura insists he keep still.|Stop that! You need to keep still!
DK4_MES_B275_R0023|Maria sees that the wounds are serious.|Those are nasty wounds.
DK4_MES_B275_R0027|He curses in pain and frustration.|Damn it!
DK4_MES_B275_R0031|Maria urges rest and will fetch the ship's doctor.|You'd better rest. Wait here. I'll bring our ship's doctor.
DK4_MES_B275_R0035|He is silent after her offer.|...
DK4_MES_B275_R0039|Sakura thinks the worst danger has passed.|It looks like he's through the worst of it.
DK4_MES_B275_R0043|He apologizes or expresses indebtedness softly.|I'm sorry...
DK4_MES_B275_R0047|Maria identifies blade wounds and invites his story.|Those wounds came from a blade. Would you care to tell me what happened?
DK4_MES_B275_R0050|He hesitates silently.|...
DK4_MES_B275_R0054|He belonged to the local smuggling organization.|I... used to be part of a smuggling ring around here.
DK4_MES_B275_R0057|Sakura reacts with surprise.|Oh, my!
DK4_MES_B275_R0061|Maria repeats the criminal occupation as a question.|Smugglers?
DK4_MES_B275_R0065|He helped foreign sellers covertly sell arms and armor without local lords' knowledge.|Yeah. I was helping foreigners sell weapons and armor behind the local lords' backs. That was the dirty business I was in.
DK4_MES_B275_R0068|Maria infers he acted as the organization's contact in Japan.|Then you were their contact in Japan, I take it?
DK4_MES_B275_R0071|He confirms and says he carried guns and other supplies to wokou pirates.|Heh. That's right. I was the one carrying guns and such to the wokou pirates.
DK4_MES_B275_R0075|Maria listens silently.|...
DK4_MES_B275_R0079|In Nagasaki he unexpectedly had occasion to hear a priest preach.|But when I was in Nagasaki, I ended up listening to a priest's sermon. Not my usual sort of thing.
DK4_MES_B275_R0083|At first he was partly mocking; listening made him disgusted with his trade.|At first I was just there for a laugh. But the more I listened, the more disgusted I got with the business.
DK4_MES_B275_R0087|He tried to leave, was wounded, and is pursued wherever he flees.|So I tried to quit, and look where that got me. No matter where I run, they keep coming after me.
DK4_MES_B275_R0091|He believes criminal involvement prevents an honest life until death.|Once you've dirtied your hands, you can never go straight. You're in it till you die.
DK4_MES_B275_R0094|Maria rejects that fatalism; honest employment must be possible, but she has a concern.|That's not true. There must be some way for you to make an honest living. But...
DK4_MES_B275_R0098|Maria infers their determination to kill him means he knows a secret.|There's only one reason they'd be so determined to kill you. You must know one of their secrets.
DK4_MES_B275_R0102|He doubts it, then considers an unexpected possibility.|A secret? Hmm... No, it couldn't be.
DK4_MES_B275_R0105|Maria asks whether something has occurred to him.|Did you think of something?
DK4_MES_B275_R0109|He doubts whether this information would be an important secret to them.|But... I don't know if they'd consider it such an important secret...
DK4_MES_B275_R0113|Maria encourages him to explain.|Tell me.
DK4_MES_B275_R0117|He overheard the smuggling boss speaking with a subordinate.|I overheard the boss talking to one of his men.
DK4_MES_B275_R0120|A Portuguese missionary group is coming and supposedly will meet the Ming emperor.|A group of missionaries is coming from Portugal. Something about an audience with the Ming emperor...
DK4_MES_B275_R0124|Maria asks when and which port they will arrive at.|...When? Which port are they coming to?
DK4_MES_B275_R0128|He does not know; the boss was secretive and repeatedly forbade an uncouth man like him from approaching the guests.|I dunno... The boss was tight-lipped about that. Kept telling me a lout like me had no business going near such distinguished guests.
DK4_MES_B275_R0131|He wonders whether the boss knew a priest's sermon could sway him.|Maybe he could tell I was a sucker for a priest's sermons.
DK4_MES_B275_R0134|Maria is concerned and asks who might know more.|...This troubles me. Do you know anyone who might have more information?
DK4_MES_B275_R0138|A Macau tavern informant might know something.|An informant at the tavern in Macau might know something.
DK4_MES_B275_R0141|Maria confirms Macau's tavern and plans to visit.|The tavern in Macau? I'll go there.
DK4_MES_B275_R0144|He asks to be taken along.|Hold on. Take me with you.
DK4_MES_B275_R0148|Sakura objects to sailing in his wounded state.|What are you saying? You can't board a ship in that condition!
DK4_MES_B275_R0151|He argues the ship is safer than town whatever his condition and flatters the capable female admiral.|No matter what shape I'm in, it's safer than staying in this town. Right, Admiral? With you in command, I'm in good hands.
DK4_MES_B275_R0155|Maria accepts his reasoning and permits him to come if he wishes.|You may be right. Come along if you like.
DK4_MES_B276_R0006|He asks the tavern proprietor whether the man is present; address is familiar, not filial.|Barkeep, is that fellow here?
DK4_MES_B276_R0010|The proprietor asks him to wait.|...Wait here.
DK4_MES_B276_R0014|The informant recognizes him and asks what he wants.|Oh, it's you. What's up?
DK4_MES_B276_R0017|Maria identifies the informant and asks about the Portuguese missionaries.|You're the informant? I'd like to know about the missionaries coming from Portugal.
DK4_MES_B276_R0020|The informant rudely asks who this woman is.|Huh? Who's this woman?
DK4_MES_B276_R0023|The former smuggling associate calls Maria his new boss.|My new boss.
DK4_MES_B276_R0027|The informant sells information and demands1,000 coins.|My information isn't free. Can you pay a thousand coins?
DK4_MES_B276_R0030|Maria accepts the price.|Very well.
DK4_MES_B276_R0035|The fleet will arrive tomorrow, here in Macau.|All right, here's what I know. The fleet arrives tomorrow, right here in Macau.
DK4_MES_B276_R0039|He challenges whether the informant is telling the truth.|You'd better be telling the truth.
DK4_MES_B276_R0043|A liar would choose a week away or Hangzhou, allowing time to flee before exposure.|If I wanted to fool you, I'd say next week, or Hangzhou. Something that'd give me time to run before you caught on.
DK4_MES_B276_R0047|He accepts the explanation and thanks him.|All right. Got it. Thanks.
DK4_MES_B276_R0051|He intends to approach the delegation and learn why the boss forbade contact.|Anyway, I'll try getting close to those visitors. I've got to find out why the boss didn't want me meeting them.
DK4_MES_B276_R0054|Maria agrees.|Yes.
DK4_MES_B277_R0005|He announces the group's arrival.|Here they come! That's them!
DK4_MES_B277_R0009|The supposed priest says Amen.|Amen...
DK4_MES_B277_R0013|Maria asks whether he recognizes them.|Do you recognize anyone?
DK4_MES_B277_R0017|He initially does not, then notices something.|No... Hm!?
DK4_MES_B277_R0020|He singles out a man.|That man!
DK4_MES_B277_R0024|Maria is puzzled.|?
DK4_MES_B277_R0028|He points out the large apparent bodyguard beside the missionary.|Look! The big fellow beside the missionary, the one who looks like a bodyguard!
DK4_MES_B277_R0031|Jacob is silent.|...
DK4_MES_B277_R0035|Maria asks whether he knows that man.|Do you know him?
DK4_MES_B277_R0039|He met Jacob through past work; Jacob is now a senior member of the ring.|Yeah! I met him on a job once. That's Jacob. He's one of the ring's top men now!
DK4_MES_B277_R0043|He reacts in shock.|What!?
DK4_MES_B277_R0047|He cannot understand why Jacob is with the delegation.|W-what's going on? What's he doing with them?
DK4_MES_B277_R0050|Maria suspects an alarming explanation.|It couldn't be...
DK4_MES_B277_R0054|He urgently asks Maria to explain if she understands.|Y-you've figured it out? I don't understand a thing! What's going on here!?
DK4_MES_B277_R0058|Maria urges calm and thinks the missionaries are probably impostors.|Calm down. Listen... I think those missionaries are impostors.
DK4_MES_B277_R0062|He exclaims in surprise.|W-what!?
DK4_MES_B277_R0066|Maria hushes him.|Shh!
DK4_MES_B277_R0070|He catches himself and quiets down.|(Whoops.)
DK4_MES_B277_R0074|She infers a plan to manipulate the Ming government into large arms and contraband purchases.|They're probably trying to talk the Ming government into buying huge quantities of weapons and contraband.
DK4_MES_B277_R0078|He thinks the deception would quickly be exposed in their home country.|B-but wouldn't word get back home right away?
DK4_MES_B277_R0081|Maria explains a state-level deal would earn immense sums and begins her inference about its use.|This is a deal with an entire nation. If it succeeds, they'll make a fortune. And with that money...
DK4_MES_B277_R0085|She thinks they intend to buy modern arms powerful enough to destroy suppression fleets at once.|I think they mean to buy the latest military equipment. Enough to wipe out any fleet sent to suppress their smuggling in an instant...
DK4_MES_B277_R0088|He gulps nervously.|(Gulp...)
DK4_MES_B277_R0092|Maria pauses in thought.|...
DK4_MES_B277_R0096|Maria takes responsibility for handling this.|Leave this to me.
DK4_MES_B277_R0101|Xien suggests reflection may reveal an opportunity.|FI, if we think this through, it may be an opportunity.
DK4_MES_B277_R0105|Maria asks him to explain.|What do you mean?
DK4_MES_B277_R0109|A large arms purchase might help the defense-neglecting Ming government resist the great powers.|The Ming government pays too little attention to defense. If it buys a large supply of arms, it might gain the strength to stand up to the great powers.
DK4_MES_B277_R0113|Maria calls that naive because the smugglers are highly experienced.|...That's naive. These are seasoned smugglers we're dealing with.
DK4_MES_B277_R0116|Inexperienced officials would pay exorbitant prices for obsolete guns.|Officials who know next to nothing about weapons will only get charged outrageous prices for obsolete guns.
DK4_MES_B277_R0119|Maria refuses to squander the people's taxes on nearly worthless arms.|We can't squander the people's tax money on weapons worth next to nothing.
DK4_MES_B277_R0123|Success would encourage another deal, likely drugs or slaves.|Once they get a taste of that, they'll be back. Next time... I expect they'll be selling drugs or slaves.
DK4_MES_B277_R0127|Ignoring this would let them have their way; Maria insists it must be stopped.|If we let this pass, we'll be playing right into their hands. We cannot allow it.
DK4_MES_B277_R0131|Xien grudgingly concedes she may be right.|Hmm... You may be right.
DK4_MES_B277_R0135|If appealing to the military will not be believed, they must act themselves.|If the military won't believe us, we'll have to do something ourselves...
DK4_MES_B277_R0139|The impostors went to the governor's office; Maria urges haste.|They're heading for the governor's office. We must hurry!
DK4_MES_B278_R0004|The spokesman claims a Jesuit delegation of more than100 has just arrived.|We have just arrived, over a hundred of us, sent by the Society of Jesus.
DK4_MES_B278_R0008|The governor thanks them and offers rest before a later audience.|Ah, you have done well to come. Rest at your leisure before your audience in the coming days.
DK4_MES_B278_R0013|The disguised magistrate loudly orders a halt.|Halt! Stop right there!
DK4_MES_B278_R0017|The false priest reacts to the interruption.|!?
DK4_MES_B278_R0021|The performer denounces filthy smugglers who would deceive them and the emperor.|Filthy smugglers! You dare deceive us, and even the Son of Heaven himself!
DK4_MES_B278_R0025|Jacob reacts in alarm.|!!
DK4_MES_B278_R0029|The governor is shocked.|W-what!?
DK4_MES_B278_R0033|The performer warns against believing local criminals.|Do not be deceived! These men are a gang of scoundrels who prey on the surrounding lands!
DK4_MES_B278_R0037|Jacob curses and demands to know what is happening.|Damn it! What's going on?
DK4_MES_B278_R0041|The governor asks whether it is true.|I-is this true!?
DK4_MES_B278_R0045|The false priest protests innocence and begins to assert authenticity.|These accusations are false! We are genuine...
DK4_MES_B278_R0048|Xien silences them and says someone who recognizes their faces informed on them.|Silence! Someone who knows your faces has informed on you!
DK4_MES_B278_R0052|They successfully entered Macau disguised as missionaries, but the sham is over.|You may have reached Macau disguised as missionaries, but this farce is over!
DK4_MES_B278_R0056|The performer declares excuses exhausted and orders everyone's arrest.|There is no talking your way out of this! Seize them all!
DK4_MES_B278_R0059|A guard answers the order forcefully.|Yes!
DK4_MES_B278_R0071|Jam cheers while joining the action.|Yahoo!
DK4_MES_B278_R0086|Yukihisa gives a martial shout.|Hyah!
DK4_MES_B278_R0093|The false priest cries in fear.|E-eek!
DK4_MES_B278_R0097|Jacob refuses to be caught here.|Tch! I'm not getting caught here!
DK4_MES_B278_R0101|The governor admits being completely fooled and nearly losing his head, then notices something while thanking them.|Hmm... I was completely taken in. I nearly lost my head! It is all thanks to you... Hm?
DK4_MES_B278_R0105|He asks where the force that exposed the smugglers went.|Where have the troops who exposed the smugglers gone?
DK4_MES_B278_R0108|The bystander says they already withdrew.|Hm? They've already left.
DK4_MES_B278_R0111|The governor is puzzled they left without greeting him.|Oh, I see. Well... Without a word to me? ...Hm?
DK4_MES_B278_R0131|He wonders since when Ming troops included Westerners and Japanese.|But... Since when have there been Westerners and Japanese in the Ming army?
DK4_MES_B278_R0143|The performer tentatively asks whether his performance was sufficient.|Um... Was that all right?
DK4_MES_B278_R0146|Maria is impressed by his convincing performance.|I'm impressed. You were very convincing.
DK4_MES_B278_R0157|Jam laughs at the villains' faces during the ruse.|Ha! That was priceless! You should've seen their faces!
DK4_MES_B278_R0171|Actor25 agrees that even the governor fully believed it.|Exactly! Even the governor of Macau completely fell for it!
DK4_MES_B278_R0178|Xien praises the former actor as the best mimic in town.|Just what I would expect from a former actor. The finest mimic in town!
DK4_MES_B278_R0181|The performer is uneasy at the audacity of impersonating a magistrate.|Impersonating a magistrate... I hardly dared.
DK4_MES_B278_R0185|Maria says they had to answer the enemy's disguise with one of their own.|We had no choice. If they came in disguise, we had to answer in kind.
DK4_MES_B278_R0189|Xien expects the smugglers to lie low for a while and asks the man what he will do.|That should keep the smugglers quiet for a while. ...Well, what will you do now?
DK4_MES_B278_R0193|The man has nowhere else to go and commits to working with them.|What else can I do? I've got nowhere else to go now. I'll stay and work for you.
DK4_MES_B278_R0197|Maria welcomes his decision.|All right. Welcome aboard.
DK4_MES_B279_R0005|Sakura greets FI and says she was worried.|FI! I've been worried about you.
DK4_MES_B279_R0008|Maria reassures her.|I'm all right.
DK4_MES_B279_R0012|The recovered man apologizes for the trouble he caused earlier.|Sorry for all the trouble I caused you back then.
DK4_MES_B279_R0016|Sakura is relieved that he recovered.|Oh, good! You're well again!
DK4_MES_B279_R0021|Maria finishes recounting what happened.|...And that's what happened.
DK4_MES_B279_R0025|Sakura reacts to the ordeal, then notices it is late.|Oh, my! You've been through so much! ...Oh! Is that the time already?
DK4_MES_B279_R0028|Maria asks whether Sakura was about to go out.|Were you just about to go out?
DK4_MES_B279_R0032|Sakura planned to visit a temple.|Yes. I was going to visit the temple.
DK4_MES_B279_R0035|Maria politely stops delaying her departure.|We shouldn't keep you, then. We'll be on our way.
DK4_MES_B279_R0038|Sakura suggests Kyoto sightseeing with a map and offers to guide them partway.|Why not visit Kyoto sometime? It's easy to reach with a map. I could show you part of the way.
DK4_MES_B279_R0042|Maria thanks her.|Thank you.
SC3_B280_STYLE_8_0|Polite encouragement to visit the map-guarding clan in a village far northeast of China.|Admiral, let's visit the clan guarding the map to the Proof. Their village was far northeast of China, wasn't it?
SC3_B280_STYLE_8_90|Measured urgency to meet the guardians as soon as possible, recalling the village.|Admiral, we should visit the clan guarding the map to the Proof as soon as possible. Their village is far northeast of China, I was told.
SC3_B280_STYLE_8_192|Youthful curiosity about the clan and suggestion to visit soon.|Admiral, I wonder what the clan guarding the map to the Proof is like. They live in a village far northeast of China, right? Why don't we go now?
SC3_B280_STYLE_8_300|Conversational reminder to visit before forgetting, with confirming question about location.|Admiral, let's visit the clan guarding the map to the Proof before we forget. They're in a village far northeast of China, aren't they?
SC3_B280_STYLE_8_404|Rough urging to meet the clan soon and confirming its location.|Admiral, let's hurry and meet that clan guarding the map to the Proof. They're in a village far northeast of China, right?
SC3_B280_STYLE_8_498|Elderly considered recommendation to visit the guardians' distant village soon.|Admiral, about that Proof... I think we should visit the clan guarding its map soon. Shall we head for that village far northeast of China?
SC3_B280_STYLE_8_614|Child curiosity about the guardians and wish to visit the far-northeastern village.|Admiral, aren't you curious about the people guarding the map to the Proof? Let's visit that village far northeast of China!
SC3_B280_STYLE_8_716|Formal interest in the Proof's map, proposing a visit and recalling location.|Admiral, I am curious about the map to the Proof. Shall we visit the village where its guardians live? It was... far northeast of China, wasn't it?'''

def main():
    output=ROOT/'authored_B275_B280_v1.json';assert not output.exists()
    rows=[r.split('|',2) for r in TEXT.splitlines()];packet=load(ROOT/'clean_source_packet.json')
    expected=[r['id'] for g in packet['groups'] if g['block'] in CONTEXTS for r in g['records']]
    assert [r[0] for r in rows]==expected and len(rows)==145
    save(output,dict(contexts={str(k):v for k,v in CONTEXTS.items()},records=rows,current_English_not_consulted=True,
        source_gloss_precedes_independent_draft_in_each_entry=True,source='Complete clean Japanese exchanges and clean B94 source clue only; terms and native consumers remain provisional.',new_credit=0))
    print('Authored145 clean meanings andindependent drafts in six complete groups;current story English unread.')

if __name__=='__main__':main()
