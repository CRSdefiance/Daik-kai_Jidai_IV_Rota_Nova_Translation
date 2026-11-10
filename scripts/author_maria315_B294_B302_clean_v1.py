"""Clean source meanings followed by independent English for nine complete exchanges."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/Maria_B286_B302_clean_20261110')
CONTEXTS={
294:"Actor206 shares a customer's story about a highly respected, virtuous monk from this town who crossed to the northern continent to preach and vanished after discovering a village far north in the New World. She hopes he is loved where he went and asks Maria to inquire if she travels north. Preserve the customer's hearsay, northern village, religious mission and uncertainty about his fate. Do not invent a named order, priestly rank, age, precise coast or confirmed harm before B302's reveal.",
295:"A troubled guildmaster asks FA for help. An unidentified ship has been sinking fleets passing nearby; nobody who saw the attacker survived to report its identity. Patrol and punitive fleets have failed to locate it. A rumor calls it a ghost ship; Maria is skeptical while the frustrated guildmaster feels driven to consider the rumor. He asks her to identify it, and would be even more grateful if she defeated it. Maria agrees. Preserve uncertainty in this request, the investigation-versus-defeat distinction and his apology for an eerie job. FA's familiar sister-like honorific is not kinship or a new noble rank; keep the original FA substitution.",
296:"After the ghost ship's defeat the guildmaster pays65000 coins and Havana share rises slightly. He introduces a villager/guide who asks Maria to find a ruin said to have been built by his ancestors to honor warriors. Tradition says only the greatest warrior, combining strength with a righteous heart and wisdom, can find it. He was convinced by her ghost-ship feat but admits asking any strong-looking person because the task is uncertain and nobody has succeeded. Maria dryly teases his permission to fail; he flusters and clarifies, and she agrees to try. He advances5000 coins, nonrefundable even on failure, then requests the map to the ancient city ruins and promises to accompany her, waiting at this town's gate. Keep the gentle humor, all amounts and uncertainty, not a guaranteed full reward or invented civilization/temple identity.",
297:"At Guam Maria tells actor135 the wait is over and they can return home. The other speaker says the source's Chinese thanks phrase twice in the exchange; Maria initially asks what was said, then recognizes that an unspoken presented object is a thank-you gift and accepts it. She wishes them well and advises care on their next sea journey. Keep the unfamiliar utterance as Xie xie to preserve Maria's initial noncomprehension; do not invent the gift's identity, a spoken offer, gender, kinship or nationality from one phrase. Actor135's clean role metadata is ritual leader with Southeast Asia metadata, which is not a license to add biography.",
298:"A New World guardian realizes seekers of the Proof have found him and vows to withhold it even at the cost of his life. He mistrusts people from across the sea who take everything; Maria recognizes that he sees her as another Western conqueror and refuses coercion. Xien warns that other conquerors may seize it, undoing their work and endangering the people. The guardian hears a threat; Maria denies that intention, while Xien insists Escante's removal does not mean Spain will abandon the New World. Two conditional Maria lines describe either destroying Escante's forces or bringing them under her authority and preventing abuses. The guardian then recognizes the female admiral from the East through a friend's account and chooses trust, hoping for true peace. Preserve this ethical tension and the voluntary resolution, not a sanitized misunderstanding, invented treaty, European identity for Maria or merged mutually exclusive military outcomes. The friend's name and the Proof's exact regional item title are not supplied here.",
299:"An Asian villager notices unfamiliar features and asks Maria's origin. She says China. He marvels that she traveled so far and guesses her party has a sextant, a tool rumored to reveal one's position on a featureless sea. He asks them to bring it in exchange for something good, keeping the reward a surprise until delivery. Preserve the source's sextant even if it is historically anachronistic; do not rewrite the game to fit external history or invent what the reward is.",
300:"The villager welcomes the brought sextant and offers the unnamed exchange item. The system confirms handing over the sextant. Preserve the barter and removal, without adding a separate gift identity or acquisition panel not present among these lines.",
301:"The same villager archetype asks whether this is the object the party seeks, reflects on the long wait and says the awaited day has finally come. He chooses to trust the party and offers it. This short branch's exact item and personal backstory remain unspecified. Preserve the solemn transition rather than inventing the number of years or a named guardian rank from the archetype.",
302:"A villager recognizes the monk Maria asks about. The monk devoted himself to an ailing village; his medicine quickly eased the illness and prevented the village's annihilation. Maria wonders about medical knowledge, but the villager recalls alchemy and neutralizing mineral poison in drinking water. He shows the monk's book. Two clean source lines use actor2, Lil, including recognition of the book Charles mentioned; keep those source controls rather than silently changing them to Maria. Charles excitedly explains that rumored new experimental material brought him to the New World, that he traced the need for the alchemy book and is certain it clues a precious metal, but still needs its use. Maria postpones his rambling and asks the monk's whereabouts. The mood turns to grief: he fell ill from the same water, hid it and gave all his medicine to villagers, then died; the villager calls him God's messenger. He asks the party to take the book and continue the research by seeking its unseen ore somewhere in the world. Maria agrees. Keep the scientific details at the source's specificity, no invented lead, gold, contagion mechanism or order. Keep the source's religious praise, self-sacrifice and final loss without treating a rendering proof as medical or historical fact.",
}
TEXT=r'''DK4_MES_B294_R0004|The named host warmly welcomes Maria.|Oh, welcome!
DK4_MES_B294_R0008|She asks whether Maria has visited a village far north in the New World.|Say, have you ever been to that village far to the north in the New World?
DK4_MES_B294_R0012|A customer said a respected monk from this town crossed to the northern continent to preach long ago.|A customer told me that a highly respected monk from this town crossed to the northern continent long ago to spread his faith.
DK4_MES_B294_R0016|He disappeared after discovering that village; she wonders if something happened.|They say he disappeared after finding that village. I wonder what happened to him.
DK4_MES_B294_R0020|Maria does not know.|Who knows?
DK4_MES_B294_R0024|The monk was apparently virtuous; she hopes the people he went to preach to cherish him.|He was supposed to be a very virtuous man. I hope the people he went to preach to are fond of him.
DK4_MES_B294_R0027|She asks Maria to inquire about him if she travels north.|If you ever go north, ask around about him, will you?
DK4_MES_B295_R0004|The guildmaster familiarly addresses FA and says only she can be asked for this help, without implying kinship.|FA, you're the only person I can ask to do this.
DK4_MES_B295_R0008|Maria asks what is wrong because he looks unusually grave.|What's wrong? You look so serious.
DK4_MES_B295_R0011|An unidentified ship has recently been sinking fleets passing nearby one after another; the following rumor consistently refers to one ghost ship.|Lately, an unidentified ship has been sinking fleets passing nearby, one after another.
DK4_MES_B295_R0015|Maria asks whether pirates are responsible.|Pirates?
DK4_MES_B295_R0019|The identity is a mystery; nobody who saw the enemy survived to report it.|That's the mystery. No one's seen the enemy and lived to tell us about it.
DK4_MES_B295_R0022|Patrol and punitive fleets have failed to find the enemy, which appears and vanishes unpredictably.|We've sent patrols and fleets to hunt it down, but we haven't found it once. It appears and vanishes without a trace.
DK4_MES_B295_R0026|Maria judges whoever is behind the attacks highly skilled.|Whoever it is, they're very skilled.
DK4_MES_B295_R0030|The guildmaster introduces a strange rumor.|But there's a strange rumor going around.
DK4_MES_B295_R0034|Maria asks what rumor.|What kind of rumor?
DK4_MES_B295_R0038|Rumor suggests the attacker is a ghost ship.|That it might be a ghost ship.
DK4_MES_B295_R0041|Maria skeptically asks if he believes it.|...You don't really believe that, do you?
DK4_MES_B295_R0045|Its elusiveness makes the unwilling guildmaster feel he must consider the rumor; he has a request.|When we can't find a single trace of it... I don't want to believe it, but what else can I think? ...That's where you come in.
DK4_MES_B295_R0048|He asks Maria to investigate what the enemy really is.|I want you to find out what it really is.
DK4_MES_B295_R0052|Maria asks whether investigation alone is enough.|You only want me to investigate?
DK4_MES_B295_R0056|He would naturally be even more grateful if she defeated it.|Of course, I'd be even more grateful if you got rid of it.
DK4_MES_B295_R0059|Maria agrees.|...All right.
DK4_MES_B295_R0063|He apologizes for the eerie job and entrusts it to her.|Sorry to give you such a creepy job. I'm counting on you.
DK4_MES_B296_R0004|The guildmaster is impressed she defeated the ghost ship and gives thanks through payment.|You actually defeated the ghost ship... I'm impressed. Please take this as a token of our thanks.
DK4_MES_B296_R0009|System awards65000 coins.|Received 65,000 coins.
DK4_MES_B296_R0031|System reports a small share increase in Havana.|Your market share in Havana increased slightly!
DK4_MES_B296_R0044|He judges her capable and wants to introduce someone.|I think you can handle this. There's someone I'd like you to meet.
DK4_MES_B296_R0047|Maria gives a questioning reaction.|Hm?
DK4_MES_B296_R0051|The newcomer greets her hesitantly.|...Hello.
DK4_MES_B296_R0055|Maria asks who the newcomer is.|Who are you?
DK4_MES_B296_R0059|The newcomer trusts her ability and urgently wants help locating ruins.|I have a request for someone of your ability. There are some ruins I desperately want you to find.
DK4_MES_B296_R0063|Maria questions the mention of ruins.|Ruins...?
DK4_MES_B296_R0067|The ruins are said to be a site built by the speaker's ancestors to honor warriors.|They are said to be the remains of a place our ancestors built to honor warriors.
DK4_MES_B296_R0070|Tradition says only someone qualified as the greatest warrior can find the site.|Tradition says only one worthy of being called the greatest warrior can find them...
DK4_MES_B296_R0074|Maria listens in silence.|...
DK4_MES_B296_R0078|The recent ghost-ship defeat convinced him she qualifies.|Your recent victory over the ghost ship convinced me.
DK4_MES_B296_R0082|The greatest warrior combines strength with a righteous heart and wisdom.|The greatest warrior is not merely strong. They must have a righteous heart and wisdom as well.
DK4_MES_B296_R0086|Maria appreciates the praise but questions whether she can help find ruins.|...I'm flattered, but can I really help you find these ruins?
DK4_MES_B296_R0090|He admits the undertaking is uncertain even to his people.|To be honest, it's all rather vague to us, too.
DK4_MES_B296_R0093|They ask any strong-looking person they find for help.|We've been asking anyone who looks strong to help us, just as I'm asking you now.
DK4_MES_B296_R0097|He knows this sounds rude; nobody has succeeded, so she need not worry about failure.|I realize that sounds terribly rude. But no one has ever succeeded, so you needn't worry if you fail.
DK4_MES_B296_R0100|Maria teases the unusual permission to fail and the resulting anticlimax.|A job where it's all right to fail? That's a first. ...What a letdown.
DK4_MES_B296_R0104|He flusters at his wording, clarifies that he does want success but she should not be discouraged if unsuccessful.|Oh, that came out all wrong! Of course I want you to find them! I only meant you needn't be discouraged if you can't...
DK4_MES_B296_R0107|Maria laughs, says she was joking and promises her best effort.|Heh, I'm teasing. I'll do what I can.
DK4_MES_B296_R0110|He is relieved by her acceptance.|O-oh, you will!
DK4_MES_B296_R0114|He offers part of the payment in advance, with no repayment if the search fails.|I'll pay part of your fee in advance. Of course, you won't have to return it even if you can't find the ruins.
DK4_MES_B296_R0117|System awards5000 coins.|Received 5,000 coins.
DK4_MES_B296_R0123|They first need the map to ancient city ruins; he asks to be told when she gets it and will join the search.|First, we'll need a map to the ruins. Let me know when you have the Map to the Ancient City Ruins. I'll join you in the search.
DK4_MES_B296_R0126|He will wait at this town's gate.|I'll be waiting at this town's gate.
DK4_MES_B297_R0004|At Guam Maria says the wait is over and the other person can go home.|This is Guam... Sorry to keep you waiting. You can go home now.
DK4_MES_B297_R0007|The source gives an unfamiliar Chinese thanks utterance; Maria's next reply shows she does not initially understand.|Xie xie.
DK4_MES_B297_R0011|Maria asks what was said.|Hm? What was that?
DK4_MES_B297_R0015|Maria recognizes an unspoken presented object as a thank-you gift and accepts.|For me? Oh, it's a thank-you gift. ...Thank you. I'd be happy to accept it.
DK4_MES_B297_R0019|The other speaker repeats the Chinese thanks phrase twice.|Xie xie. Xie xie.
DK4_MES_B297_R0023|Maria wishes them well and urges care on the next sea journey.|Take care. Be careful the next time you go to sea.
DK4_MES_B298_R0004|The guardian is alarmed at finally being found.|Ah! You've finally found me!
DK4_MES_B298_R0008|Maria asks what is wrong.|What's wrong?
DK4_MES_B298_R0012|The guardian asks whether they are collecting the Proofs.|...Y-you're collecting the Proofs, aren't you?
DK4_MES_B298_R0015|Maria confirms it.|Yes.
DK4_MES_B298_R0019|The guardian vows not to hand it over even at the cost of his life.|I knew it! I'll die before I let you have it!
DK4_MES_B298_R0022|Maria asks him to calm down and says she does not intend to seize it.|Please, calm down. I have no intention of taking it by force.
DK4_MES_B298_R0025|He refuses to be deceived; people from the other continent make such claims and take everything.|I won't be fooled! That's what those people from across the sea say, and then they take everything!
DK4_MES_B298_R0029|Maria realizes he sees her as no different from the Western conquerors.|...He thinks I'm no different from the Western conquerors.
DK4_MES_B298_R0033|The guardian falls silent.|...
DK4_MES_B298_R0037|Maria decides to abandon the attempt.|All right. Let's give up on it.
DK4_MES_B298_R0041|Xien protests FI abandoning the New World's Proof.|FI! You're going to give up on the New World's Proof?
DK4_MES_B298_R0045|Maria refuses to coerce the guardian.|We can't force them to give it to us.
DK4_MES_B298_R0049|Other conquerors might seize it if they learn of it, undoing the party's efforts.|If other conquerors hear of it, they may come and take it by force. What becomes of all our efforts if it falls into their hands?
DK4_MES_B298_R0052|Maria considers this in silence.|...
DK4_MES_B298_R0056|Xien adds that the people here would also be harmed.|And if that happens, these people won't escape unharmed.
DK4_MES_B298_R0059|The guardian takes this as a threat and challenges them.|What?! Are you threatening us?!
DK4_MES_B298_R0062|Maria denies her own intention to threaten but hesitates; this does not clear Xien's warning of its coercive implication.|I don't mean to threaten you. But...
DK4_MES_B298_R0065|Xien insists on the facts: Escante's threat is gone, but Spain is unlikely to abandon the New World.|But the facts remain. Escante's threat is gone, yet I doubt Spain will simply give up on the New World.
DK4_MES_B298_R0068|The guardian reacts to the mention of Escante and asks what happened.|What? What happened to Escante?
DK4_MES_B298_R0078|Conditional Maria line says their party destroyed Escante's forces.|We destroyed Escante's forces.
DK4_MES_B298_R0084|Alternative Maria line says Escante's forces submitted to her party and she will prevent abuses here.|Escante's forces have submitted to us... We won't let them terrorize the New World anymore.
DK4_MES_B298_R0091|The guardian realizes Maria may be the female admiral from the East.|What?! Then you're the woman admiral from the East...?
DK4_MES_B298_R0094|Xien marvels that her reputation reached even this place.|So word of you has reached even here.
DK4_MES_B298_R0097|A friend who entrusted the object to him told him about Maria.|No, the friend who entrusted this to me told me about you...
DK4_MES_B298_R0100|He chooses to trust her and hopes she brings true peace here.|I'll trust you. I pray you'll bring true peace to this land.
DK4_MES_B298_R0107|Maria thanks him and promises her utmost.|Thank you. I'll do everything I can.
DK4_MES_B299_R0004|The villager notices unfamiliar features and asks their origin.|I haven't seen faces like yours before. Where are you from?
DK4_MES_B299_R0007|Maria answers China.|China.
DK4_MES_B299_R0011|He is amazed they came so far from China.|Oh, from China? Really? To think you could come so far...
DK4_MES_B299_R0015|He guesses they have the useful instrument called a sextant.|Ah, I see! You must have one of those handy things called a sextant, don't you?
DK4_MES_B299_R0019|Maria is surprised.|What?
DK4_MES_B299_R0023|Rumor says it reveals position even on a sea with no landmarks.|I've heard about them. They tell you where you are, even out at sea with no landmarks. Or so they say.
DK4_MES_B299_R0027|He requests their sextant in exchange for something good.|Well? Would you give us that sextant? I'll give you something good in return.
DK4_MES_B299_R0030|Maria asks about the promised item.|Something good?
DK4_MES_B299_R0034|He keeps the reward a surprise until they bring the sextant.|You'll have to bring it here to find out.
DK4_MES_B300_R0005|He welcomes the brought item and offers the unnamed exchange object.|Oh, you've brought it? Here, take this in exchange.
DK4_MES_B300_R0013|System confirms giving away the sextant.|Handed over the Sextant.
DK4_MES_B301_R0005|The villager asks if this is the object they sought.|This is what you've been looking for, isn't it?
DK4_MES_B301_R0009|The long-awaited day has finally come.|It's been so long... At last, the day has come.
DK4_MES_B301_R0012|He decides to trust the party and offers the object.|I'll put my trust in you. Please, take it.
DK4_MES_B302_R0004|The villager is surprised the party knows of the monk.|Oh! You know about that monk!
DK4_MES_B302_R0008|Maria asks whether he knows the monk.|Do you know him?
DK4_MES_B302_R0012|The monk devotedly nursed the sick villagers, preventing the whole village's destruction.|He couldn't bear to see us so sick. He devoted himself to caring for us. Thanks to him, our village wasn't wiped out.
DK4_MES_B302_R0015|His medicine quickly eased the illness, which the villager calls miraculous.|As soon as we took the medicine he made, the sickness eased. It was a miracle.
DK4_MES_B302_R0019|Maria wonders whether he had medical knowledge, without asserting formal training.|Did he know something about medicine?
DK4_MES_B302_R0023|The monk called it alchemy and said it neutralized mineral poison in their drinking water.|No, he called it alchemy. Something about neutralizing the mineral poison mixed into our drinking water...
DK4_MES_B302_R0027|He identifies the monk as the author of the shown book.|Here, he's the one who wrote this book.
DK4_MES_B302_R0038|Clean actor2 reacts with surprised recognition; do not silently change the source speaker.|Wait! Could this be...?!
DK4_MES_B302_R0057|Clean actor2 recognizes the book Charles mentioned and celebrates finding it.|This is the book Charles told me about! I finally found it!
DK4_MES_B302_R0064|Charles is astonished to encounter the alchemy book here.|The Book of Alchemy?! I-I never thought I'd find it here!
DK4_MES_B302_R0068|Maria asks what has happened to Charles.|Charles, what's wrong?!
DK4_MES_B302_R0072|Charles came as far as the New World after hearing rumors of newly discovered experimental material.|I came all the way to the New World because I heard rumors of a newly discovered material for my experiments!
DK4_MES_B302_R0075|He learned that the alchemy book is needed to obtain that material.|I learned that I would need this Book of Alchemy to obtain it, but...
DK4_MES_B302_R0079|He is certain it offers a clue to a precious metal and now needs to know how to use it, then mutters.|There's no doubt it's a clue to some precious metal! Now, if I can just work out how to use it... Hmm, yes...
DK4_MES_B302_R0082|Maria postpones hearing the rest of his rambling.|...I'll hear the rest later.
DK4_MES_B302_R0089|Maria returns to asking the monk's current whereabouts.|So, where is the monk now?
DK4_MES_B302_R0093|The villager falls silent before the sad revelation.|...
DK4_MES_B302_R0097|A crew role reacts questioningly to the silence.|Hm?
DK4_MES_B302_R0101|The monk became sick like the villagers after drinking the village water.|He drank the water here and fell ill, just as we had...
DK4_MES_B302_R0104|He hid his own illness and gave all the medicine he made to the villagers.|But he hid it from us and gave every bit of the medicine he made to the villagers!
DK4_MES_B302_R0108|He eventually died; the grieving villager calls him truly God's messenger.|And in the end... he died! He truly was a messenger of God...
DK4_MES_B302_R0111|The captain responds to the loss in silence.|...
DK4_MES_B302_R0115|The villager asks whether he may entrust the book to them.|...May I entrust this book to you?
DK4_MES_B302_R0118|The captain questions the word entrust.|Entrust it to us?
DK4_MES_B302_R0122|The book contains the secret of an ore no one has seen before.|It holds the secret of an ore no one has ever seen before.
DK4_MES_B302_R0125|He believes the ore must occur somewhere in the world.|There must be deposits of this ore somewhere in the world.
DK4_MES_B302_R0128|They seek someone to carry on the monk's research and ask the party to find the ore.|We are looking for someone to carry on his research. Will you search for that ore?
DK4_MES_B302_R0132|Maria agrees to try.|...All right. Let's try.'''

def main():
    output=ROOT/'authored_B294_B302_v1.json';assert not output.exists()
    rows=[r.split('|',2) for r in TEXT.splitlines()];packet=load(ROOT/'clean_source_packet.json')
    expected=[r['id'] for g in packet['groups'] if g['block'] in CONTEXTS for r in g['records']]
    assert [r[0] for r in rows]==expected and len(rows)==124
    save(output,dict(contexts={str(k):v for k,v in CONTEXTS.items()},records=rows,current_English_not_consulted=True,
        source_gloss_precedes_independent_draft_in_each_entry=True,source='Complete clean Japanese exchanges only; item terms and native role/voice consumers remain provisional.',new_credit=0))
    print('Authored124 clean meanings andindependent drafts in nine complete groups;current story English unread.')

if __name__=='__main__':main()
