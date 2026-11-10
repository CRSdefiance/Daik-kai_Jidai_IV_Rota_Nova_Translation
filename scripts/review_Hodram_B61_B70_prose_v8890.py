"""Complete whole-exchange prose decisions; reuse the first44 value-exact."""
import re
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B61_B70_prose_v8890')
DOC=Path('translations/hodram_B61_B70_editorial_manuscript_v1.json')
PARTIAL=Path('translations/hodram_B61_B70_editorial_manuscript_partial_v1.json')
CURRENT=Path('work/analysis/Hodram_B61_B70_current_v8885/current_effective.json')
GLOSS=Path('work/analysis/Hodram_B61_B70_clean_gloss_v8877/224_complete_clean_first_meanings_all_ten_exchanges_before_current_English.json')
VIEW=Path('work/analysis/Hodram_B61_B70_source_review_v8884/source_context_names_display_review_before_current_English.json')
PATHS=Path('work/analysis/Hodram_B61_B70_source_paths_v8883/all224_source_memberships_original_branch_cases.json')
NAMES=Path('translations/hodram_B61_B70_speaker_name_review_v1.json')
VERIFIED=Path('work/analysis/editorial_handoff_verification_v8889/verified_handoff.json')

# Independent per-record decisions after the clean-first complete-exchange pass.
# These are prose, never manually wrapped bytes or a fixed-allocation shortcut.
LINES={
63:{
5:("Make way for Nagarpur and his party! You there, Westerner, clear the road!", 'Lord invents nobility and Nagalpur disagrees with the reviewed name.', 'Keep the loud, rude announcement and Westerner address. Sama conveys deference to Nagarpur, not proof of a noble rank. Party means his entourage.'),
8:('Nagarpur?', 'Reconcile the spoken surname with the source-bound native name.', 'The captain simply repeats the unfamiliar name. Keep the recognition question without adding a title or pretending he already knows the man.'),
12:("What's this strange procession...?", 'The predecessor drops the explicitly strange quality of the crowd.', 'Gerhard reacts to the approaching entourage. Procession naturally conveys the large passing party without inventing a parade, official ceremony or army.'),
15:('Ho ho ho! Make way! Hm? You there. Did you want something from me?', 'Restore the conspicuous laugh, singled-out address and self-important question.', 'Nagarpur is pompous and patronizing. Ordinary English and laughter preserve that voice without a fabricated ethnic accent or an invented threat.'),
19:("What are you talking about? I'm not trying to block your way...", 'The source denies an intention to interfere, rather than proving the road is unobstructed.', 'The captain challenges the assumption and denies intending to obstruct him. Do not convert his defense into an objective statement about every crew member or the road.'),
22:("Hmm, I see! You want a tip, don't you? Here!", 'Restore the patronizing supposed realization and question.', 'Nagarpur assumes the captain wants money and offers a tip. No amount, acceptance, agreement or successful bribery follows from the offer.'),
34:("What the hell do you take us for?!", 'The predecessor substitutes a detached insult for the angry protest at his misconception.', 'Al Shin angrily rejects the implication that the group is seeking tips. The idiomatic outburst preserves the rude address without inventing a slur, kinship or specific accusation.'),
41:('How dare you mock Admiral {MACRO:FI}!', 'The angry defense of the explicitly named admiral already works.', 'The clean line itself supplies 提督, so Admiral is supported here. Preserve Gerhard\'s indignation and the given-name macro; do not generalize the rank to other speakers.'),
45:("Nagarpur, is it? What's the meaning of this?", 'Correct the surname and make the dismissive name check conversational.', 'The captain questions the insulting gesture, not its monetary amount. His cool disapproval remains distinct from his crew\'s heated reactions.'),
48:("Ho ho ho! Not enough for you? Shall I give you more? I've got plenty of money!", 'Restore the repeated offer and boast, which the predecessor compresses.', 'He doubles down on his mistaken tip assumption. Keep the patronizing abundance without inventing a sum, a completed payment or a bargain.'),
52:('Nagarpur... Now I remember! The Nagarpur Company, those notorious upstarts! They seem to run things around here.', 'The predecessor loses the named company and its apparent local control.', 'Gerhard recalls the company\'s reputation for ostentatious new wealth. Upstarts carries that contempt; seem preserves the qualification about regional power without inventing a government office or royal rank.'),
56:("...You seem to be doing very well for yourself.", 'Earn quite well sounds translated; the source is a dry observation about his earnings.', 'Natural spoken English preserves the captain\'s reserved assessment, not admiration, an audited income or proof of how he acquired it.'),
60:('Money, money, money! Money is everything!', 'The repeated money boast already works.', 'The repetition and sweeping claim carry Nagarpur\'s ostentation. These are his values, not an objective statement about the setting or a new mechanic.'),
63:('Money is everything...? How pathetic.', 'Money is all? Pitiful is unnecessarily telegraphic.', 'The captain repeats and condemns the claim. A short complete judgment keeps his dry contempt without adding a new insult about ancestry or a threat.'),
75:("I like money myself. But anyone who thinks it's everything is rotten to the core.", 'Restore Fernando\'s personal liking for money and the universal condemnation of that attitude.', 'His rough optional aside distinguishes enjoying money from making it everything. Anyone preserves the source\'s no-exceptions force without limiting the accusation to an invented group.'),
82:('Hm? Did you say something?', 'His suspicious question already works.', 'The hesitation in Hm and the question naturally answer the optional aside. Do not supply words he overheard or make the aside unconditional.'),
85:('Got a problem, Westerner?', 'The entourage member\'s rough challenge already works.', 'The dropped auxiliary is idiomatic in this hostile voice. Preserve Westerner and the challenge without adding nationality, rank or a specific threat.'),
89:("You're as ugly inside as you are outside... You make me sick. Let's go.", 'Restore the parallel appearance/character insult and explicit revulsion.', 'The source itself makes the harsh comparison. Preserve it without sanitizing it or adding weight, race, sexual insults or a literal illness. The captain decides to leave.'),
92:('Exactly.', 'Gerhard\'s brief agreement already works.', 'This assent follows the captain\'s condemnation and decision to leave. It adds neither a new allegation nor a separate instruction.'),
96:("Oh? You're picking a fight with me? You must have a death wish...", 'Restore the picking-a-fight question and the source idiom about recklessness.', 'Death wish is the ordinary figurative English taunt for 命知らず here. It is not a new death sentence, literal wish or confirmed plan to kill.'),
100:('No one can match my wealth!', 'The emphatic wealth boast already works.', 'Keep Nagarpur\'s sweeping claim as boastful dialogue. It does not prove that he is objectively the richest person or stronger in every respect.'),
111:('He thinks money solves everything.', 'The companion\'s contemptuous aside already works.', 'Charles identifies the belief behind the boast. It remains an optional crew observation, not narration endorsing money as a solution.'),
117:("He's completely deluded!", 'Arrogance does not fully express the source\'s extreme misconception.', 'Gerhard rejects the man\'s confidence in wealth. The forceful judgment stays about that belief without introducing a diagnosis or an additional deed.'),
121:('Let him talk. Wealth is useless in incompetent hands.', 'The captain\'s dismissal and wealth-versus-ability distinction already work.', 'The idiomatic concise statement preserves the point that money alone is insufficient. It does not invent a tactical victory, current financial weakness or an order to attack.'),
125:("Ho ho ho! Instead of spouting nonsense, why don't you think about how to become as rich as I am?", 'Restore the condescending rhetorical suggestion instead of a flat command to learn.', 'His reply dismisses their criticism and flaunts his riches again. Keep the question and laugh without adding an actual lesson, deal or offer of employment.'),
129:('Come along, then. Make way!', 'The English should distinguish moving his party along from ordering the road cleared.', 'The two imperatives carry his departure and continued presumption of priority. They establish no official right of way or new rank.'),
132:('Move aside!', 'The shouted follow-up already works.', 'The entourage reinforces the road-clearing order. No extra insult, force or action needs to be added.'),
137:("...I don't think he and I will ever see eye to eye.", 'No common ground with that man is an awkward fragment.', 'The idiom expresses the captain\'s strong expectation of incompatible attitudes. It does not invent a prior friendship, formal feud or declared war.'),
140:("What outrageous rudeness! Let's use our fleet to teach him how the world ought to work!", 'Restore the moralizing right-way claim and the proposed use of their fleet.', 'Gerhard urges retaliation in an indignant, formal voice. It remains his proposal, not the captain\'s order, an actual battle or a newly declared war.'),
},
64:{
11:('You truly are the king of the Indian Ocean, {MACRO:FA}. Please accept this.', 'Eastern ocean loses the explicitly named Indian Ocean.', 'The Trader respectfully acclaims the captain and offers an unnamed object. King is the source\'s sea-king praise, not a newly established royal office. Preserve the surname macro.'),
17:('{MACRO:FI}', 'The simple given-name call already works.', 'On the alternative Sera path, she addresses the captain before explaining the legend. Preserve the exact macro without adding a relationship or rank.'),
21:('Hm?', 'His short attentive response already works.', 'The captain invites her to continue. A longer line would supply emotional content the source leaves understated.'),
25:("...You're... the king from the legend.", 'The predecessor omits that the identification comes from a legend.', 'Simple learner speech expresses Sera\'s belief. Do not turn her identification into objective confirmation that a prophecy is fulfilled.'),
29:('What did you say?', 'The fuller question carries his surprised request to repeat it.', 'The captain is startled by the identification. He has not accepted the legend, and no object is named in this turn.'),
33:('This', 'Her single-word presentation of the object already works.', 'The deictic word is appropriate learner speech in a visible offer. Do not supply a map, Proof or other object name from opaque surrounding commands.'),
37:("You're giving this to me? ...What is this?!", 'Restore his question about giving it to him and the startled second reaction.', 'The source does not establish the object\'s identity here. Keep surprise and recipient clear without turning recognition into a named-item fact.'),
51:("This leaf...? What does this mean? Why are you giving it to me?", 'Restore the middle question rather than compressing three questions into two.', 'The later conditional segment explicitly calls it a leaf. Do not conflate this segment with every earlier gift branch or rename the leaf as a map or Proof.'),
55:('...A legend... from my country.', 'Our legend omits the explicit country reference.', 'The simple phrases locate the account in her country\'s tradition. They establish cultural context without claiming that all peoples share it or that it is objectively true.'),
59:('A legend?', 'Tale weakens the deliberate echo of her explanation.', 'The captain repeats her key word to prompt more. This is curiosity, not acceptance of the legendary claim.'),
63:('Silver hair... blue eyes... an iron ship. The king of the seas... finds the treasure... handed down in the kingdom.', 'Restore the kingdom\'s transmitted treasure rather than reducing it to our treasure.', 'Keep every feature of the legend in respectful short learner phrases. The kingdom is part of the tradition; no royal ancestry, personal ownership, treasure identity or completed discovery is invented.'),
66:("I'm the king from the legend? On an iron ship?", 'Restore his explicit echo of the legendary identity.', 'His paired incredulous questions react to her account. They do not establish that the actual ship is iron or that he accepts a kingly rank.'),
70:('(Nods.)', 'The written nod already works.', 'This nonverbal assent is present in the source. Keep it as a stage reaction without adding speech, romance or a new animation claim.'),
74:('…', 'His silent response already works.', 'The pause precedes his laugh and rejection of the story. Do not fill it with an invented conclusion.'),
78:('Ha ha ha! Nonsense. Just a fairy tale.', 'The laugh and dismissive skepticism already work.', 'His insensitive dismissal motivates Sera\'s hurt response. Do not soften the insult so far that her next line loses its cause.'),
81:('{MACRO:FI}. You mocked... my country\'s legend.', 'Restore the country reference and past act of mockery.', 'Sera identifies the cultural slight before making it personal. Her simple accusation does not need a phonetic accent or an invented romance.'),
84:('Mocked it? But how can I believe such a far-fetched story? Silver hair and blue eyes? Hah! It sounds made up.', 'The predecessor loses his echo, rhetorical disbelief and dismissive laugh.', 'The captain defensively calls the story implausible and contrived. These are his opinions, not narrator proof that Sera fabricated it or that the legend is false.'),
87:('{MACRO:FI}. You mocked me.', 'The quiet personal accusation already works.', 'The shift from her country\'s legend to herself carries the emotional escalation. Keep that directness without supplying a new grievance or relationship.'),
90:("Ah, no... That's not what I meant.", 'That wasn\'t meant is unnatural and hides his own intent.', 'His flustered denial responds to having hurt her. Do not turn it into a retraction of every skeptical belief or an explanation not yet given.'),
93:('…', 'Her silence after his denial already works.', 'The hurt pause leads him to apologize more clearly. It does not supply forgiveness or a new spoken accusation.'),
97:("I'm sorry. I really am. But you must have the wrong man. It isn't me.", 'Restore the repeated apology and personal mistaken-identity claim.', 'He apologizes while maintaining disbelief that he is the man in the legend. His insistence remains dialogue, not a resolved proof of the prophecy\'s identity.'),
101:('{MACRO:FI}... Find the treasure.', 'Restore the pause and natural definite article in her insistence.', 'She returns to the request/expectation that he seek the treasure. Keep the simple learner demand without promising success or identifying the treasure.'),
104:("Hm? Yes, I'll look for it. I will. ...Don't look so fierce.", 'Restore his repeated promise to look rather than merely acknowledging the treasure.', 'His reluctant reassurance and mild comic complaint answer her insistence. Looking is not a guarantee of finding it; no romantic interpretation is needed.'),
},
65:{
6:('○×！！', 'The deliberately opaque source speech already works exactly.', 'Keep every circle, cross and exclamation unchanged. This is an intentionally untranslated in-world language, not a software placeholder or a confession to decode.'),
10:('Sirwood!', 'Reconcile Shirud with the individually reviewed source-bound name.', 'Sera recognizes the man by his given name. Sirwood is one proper name, not the English title Sir, and supplies no kinship or office.'),
14:('？', 'The captain\'s puzzled reaction already works.', 'Keep the wordless question while he does not understand the exchange. Do not translate the unknown words on his behalf.'),
18:('○○×○×！！', 'The second opaque utterance already preserves the source exactly.', 'Retain the complete symbol sequence. Recognition does not authorize inventing the content of the speaker\'s words.'),
22:('×××○○×！！', 'Sera\'s opaque reply already preserves the source exactly.', 'Her fluent response in the other language remains opaque to the player here. Do not replace it with a guessed family reunion or romantic statement.'),
26:("What?! Don't tell me you know him!", 'Restore the captain\'s disbelief in the recognition question.', 'He asks whether they know one another. The question does not decide how they met, how closely they are related or what their symbol speech means.'),
30:("He's... from my country!", 'My people is an awkward response about the one recognized compatriot.', 'The recognition establishes a fellow person from her country. Do not turn 仲間 into a brother, father, spouse or a claim that he accompanied a particular escape.'),
34:('What?!', 'What! is unnatural punctuation for this startled question.', 'Keep the second burst of surprise without supplying a new fact, name or relationship.'),
38:('○×○×？', 'The opaque question already matches the source.', 'Preserve both the symbol order and the question punctuation. Its meaning remains deliberately unavailable.'),
42:('×○○○！', 'The brief opaque reply already matches the source.', 'Keep the unknown-language response as written. It is not an English yes/no answer that can safely be guessed.'),
46:('So there were other survivors after all... A reunion after all this time, then.', 'The predecessor compresses the surprise and sense of long-awaited recognition.', 'The captain infers a reunion from the recognition. Other survivors does not prove that everyone else died, that an entire nation vanished or that the people are relatives.'),
49:('I see... You can rest easy now.', 'You\'re safe turns reassurance into an objective safety guarantee.', 'The captain expresses relief at her finding a compatriot. He does not certify that all future danger has ended.'),
53:('{MACRO:FI}', 'The direct name call already works.', 'She turns back to the captain before announcing her decision. Preserve the exact name substitution without adding a term of endearment.'),
57:('Hm?', 'His attentive short reply already works.', 'The simple prompt lets her announce her plans. It conveys no objection or approval before she speaks.'),
61:("I'm... going back to my country.", 'Restore her explicit subject, return and country rather than a compressed Going home.', 'The learner sentence announces her intention. It does not promise an intact hometown or establish that she has already returned.'),
65:("...Yes. That's best.", 'The reserved acceptance already works.', 'The captain accepts her decision quietly. He does not command her to leave, guarantee safety or turn the choice into abandonment.'),
68:("{MACRO:FI}... You'll be king of the seas. I'm sure.", 'The predecessor omits her confident prediction of becoming sea king.', 'This is Sera\'s belief and encouragement. Preserve the future becoming without claiming that a prophecy or game condition is already fulfilled.'),
71:("My dream is to build the world's finest navy... I couldn't ask for better parting words.", 'Restore the world\'s-finest ambition and farewell significance of her words.', 'The captain receives her encouragement as a parting gift in words. Do not invent a physical reward, completed naval supremacy or romantic pledge.'),
74:("{MACRO:FI}... When you're... king of the seas...", 'Restore the full conditional phrase while preserving her difficulty continuing.', 'Her thought depends on his future becoming sea king. The pause carries hesitation, not a promise that it will happen or an invented confession.'),
77:('？', 'His puzzled pause already works.', 'The question reaction prompts her to continue the unfinished conditional. No new sentence is needed.'),
81:('When you are...', 'The short repetition can be natural learner speech with its subject restored.', 'She repeats the unfinished condition instead of advancing to a different thought. Leave the continuation unresolved until her next spoken line.'),
85:('What?', 'His short request to continue already works.', 'The direct prompt fits his reserved manner in this hesitant exchange. It does not imply anger at her language learning.'),
89:('...We can... meet again.', 'Meet again loses the potential reunion and its participants.', 'The preceding condition frames the possibility of meeting again. Can preserves possibility; do not turn it into a guaranteed appointment or romantic promise.'),
93:('Hope so.', 'The captain\'s understated wish already works.', 'The idiomatic short reply expresses hope rather than a promise. It fits his reserve and keeps the tentative emotional progression.'),
97:('…', 'Sera\'s quiet pause already works.', 'Keep her silence after his hopeful answer. Do not fill it with an invented commitment or explicit romance.'),
101:("Don't let your guard down around Westerners... That includes me.", 'Beware Westerners... me too is compressed and loses the warning about trust.', 'Preserve the explicit cultural reference and his self-inclusion. This is his caution about misplaced trust, not narrator proof that every Westerner is evil.'),
104:('…', 'Her silent response to the warning already works.', 'The pause leaves her reaction understated. Do not invent agreement, a vow or an accusation.'),
108:('{MACRO:FI}!', 'Her sharp name call already works.', 'Keep the sudden call and exact given-name substitution before the opaque utterance. It does not name a relationship.'),
112:('Hm?', 'His brief response already works.', 'The captain answers the call without anticipating words he will not understand.'),
116:('○○○×○！！', 'The final opaque utterance already matches every source symbol.', 'Its private meaning is deliberately withheld. Do not invent a translation or romantic confession because of the emotional farewell context.'),
120:('！？', 'The compatriot\'s wordless surprise already works.', 'Keep the source reaction without decoding the speech or explaining the speaker\'s motive.'),
124:('...What did you say?', 'Restore his hesitant request to repeat the unfamiliar words.', 'The captain explicitly does not understand. The translation must preserve that gap rather than reveal invented content to him or the player.'),
128:('Nothing... Thank you! Goodbye!', 'The denial, gratitude and emphatic farewell already work.', 'She does not explain the unknown-language words. Keep the abrupt grateful departure without adding their hidden meaning or a promise to return.'),
132:('All right... Goodbye.', 'Yes... goodbye sounds less natural as a reply to the farewell.', 'The short acknowledgment and pause preserve his reserved acceptance. Do not add a pet name, promise or dramatic confession.'),
144:('…', 'This conditional crew silence already works.', 'Keep Gerhard\'s pause on its mapped path. It is an alternative reaction, not an extra line every party member must speak.'),
150:('…', 'This alternative crew silence already works.', 'Keep Manuel\'s quiet reaction on the separate mapped branch. Do not concatenate it with every other crew pause.'),
157:('Are you sure?', 'The companion\'s question already works.', 'Gerhard checks the captain\'s acceptance of the departure. The question does not grant him ownership of Sera or make her choice a formal dismissal.'),
161:("She's a strong woman. I don't think we need to worry.", 'Restore a natural sentence and the source\'s qualified expectation.', 'Strong is resilience in this farewell context, not proof of physical strength. The captain expects her to cope; he does not guarantee her future safety.'),
170:('…', 'The final Gerhard pause already works.', 'Preserve the optional silent reaction after the reassurance without adding commentary or a new emotional conclusion.'),
176:('…', 'The alternative Charles pause already works.', 'Keep this source-bound alternative silence distinct from the other crew branch. It supplies no new spoken judgment or relationship.'),
},
}

LINES.update({
66:{
6:("I haven't seen you around before. You'd better leave before you get caught up in Kuhn and Pereira's feud.", 'Restore the observation and recommendation rather than declaring the listener new and ordering departure.', 'The Port Worker gives a rough local warning. Preserve both reviewed surnames without inventing a faction, prior visit, age or official authority.'),
26:("Whoever wins, it's nothing to celebrate... Right?", 'People here gain nothing overstates a specific population; lad adds an age implication.', 'The familiar address invites Camille\'s agreement in natural English. No brotherhood, age or new friendship needs to be asserted.'),
31:('Y-yes.', 'The hesitant polite assent already works.', 'Camille answers the worker before the captain recognizes him. Preserve his stammer without an invented explanation for his presence.'),
35:('You...?!', 'The captain\'s startled recognition already works.', 'His unfinished reaction does not yet supply a name or new relationship. Let the following exchange establish recognition.'),
39:('Huh? ...Oh!', 'What? Ah! is a stiff response to sudden recognition.', 'Camille first wonders who addressed him, then recognizes the captain. Keep the two reactions without inventing a motive or fear.'),
45:("You're... Camille, aren't you?!", 'The registered effective name check already works.', 'Retain approved Camille and the startled confirmation question. The current catalogue substitution is part of the real predecessor and must not be discarded.'),
49:('{MACRO:FI}... right?', 'His hesitant reciprocal recognition already works.', 'The given-name macro and question preserve uncertainty and the source\'s polite manner. Do not add a rank or pretend the question is about his legal name.'),
52:("Why are you here? Where's Lil?", 'The two clear questions already work.', 'The captain asks about Camille\'s presence and Lil\'s whereabouts. No romance, kinship, breakup or dismissal follows from those questions.'),
56:("Well... we're traveling separately for now.", 'The evasive temporary separation already works.', 'For now preserves the temporary wording. Do not explain the cause, make it a romantic breakup, or claim that he has permanently left her company.'),
59:('Hm?', 'The captain\'s puzzled response already works.', 'Keep his uncertainty rather than supplying knowledge of the dispute or deciding that Camille is lying.'),
63:('W-well, then...', 'Restore his flustered hesitation as he breaks off.', 'The incomplete conversational exit preserves evasiveness. It is not proof of a new destination, betrayal or refusal of an explicit request.'),
68:('？', 'The captain\'s question reaction already works.', 'His confusion remains wordless. Do not fill it with a theory about Camille and Lil.'),
72:('It seems he has his reasons...', 'There is more to this turns the source\'s impression into a flat assertion.', 'Gerhard senses an unexplained reason. Preserve the qualification without naming that reason or inventing a relationship dispute.'),
},
67:{
5:("You're {MACRO:FA}, correct? Someone would like to meet you. Would you come with me?", 'The predecessor is stiff and loses the courteous invitation to accompany the speaker.', 'Xien politely checks the surname and invites the captain to meet an unnamed person. Courtesy does not establish a lord, employer, rank or family relationship.'),
8:('Me?', 'The captain\'s surprised confirmation already works.', 'The short question naturally answers the invitation. It supplies no acceptance, suspicion or explanation of who wants to see him.'),
12:("Don't worry. It won't take long.", 'Relax is too casual for the source\'s courteous reassurance.', 'The speaker reassures him about time. It is dialogue, not an audited duration, guarantee of safety or official order.'),
15:('？', 'The question reaction already works.', 'Keep the captain\'s uncertainty as the invitation proceeds. Do not invent a spoken acceptance or new scene detail.'),
25:('…', 'The captain\'s silence on arrival already works.', 'This pause precedes Maria\'s welcome. It does not establish a hidden thought, location or completed agreement.'),
29:('Welcome.', 'Maria\'s restrained welcome already works.', 'The short greeting suits her controlled introduction. Do not add a title, venue or prior acquaintance.'),
33:('...Who are you?', 'Your name? narrows the source\'s broader question about identity.', 'The captain asks who she is, allowing her pointed enemy answer to follow naturally. Preserve his wary pause without inventing a rank.'),
36:('Someone who may become your enemy.', 'The oblique conditional identity answer already works.', 'Maria withholds her name and defines a possible relationship. May become is not a declaration of present hostility toward every Westerner.'),
39:('My enemy?', 'His incredulous echo already works.', 'Keep the brief challenge so her following condition explains it. No additional threat or allegiance is needed.'),
43:("If you're another Westerner planning to exploit Asia, then yes.", 'The predecessor is stilted; the conditional accusation should sound spoken.', 'Exploit preserves 喰い物 and its moral force. The enemy condition is exploiting Asia, not Western birth alone; do not erase the cultural and colonial context.'),
47:('……', 'His extended silence already works.', 'The pause before his declared purpose preserves the source pacing. Do not turn it into an admission of her accusation.'),
51:("We have one goal: to bring our country's navy up to world-class standards.", 'Restore the explicit sole purpose and raising the existing navy\'s standard.', 'This is the captain\'s stated aim, not proof of current supremacy. World-class preserves 世界一流 here; do not automatically replace it with the different world\'s-finest claim in the farewell.'),
55:('A noble excuse. You pushed others aside all the way here.', 'Maria\'s sarcastic criticism already works.', 'The first phrase is plainly sarcastic after his earnest claim. Keep it as her accusation, not narrator confirmation of every harm or a new allegation of conquest.'),
59:('Think what you will.', 'His curt refusal to argue about her opinion already works.', 'The formal, reserved phrasing suits the captain. He does not retract his goal or agree that the excuse is false.'),
63:("But whenever I look at the fleet we've built, I can't deny the grand ambitions it stirs in me.", 'Restore his first-person admission, the built fleet and the recurring impulse.', 'He candidly admits ambition without listing a new conquest plan or contradicting every part of his stated aim. Whenever preserves the recurrent source feeling.'),
66:("Sailors all over the world are locked in a fierce struggle for control of the seas. Those of us who make our lives at sea couldn't ask for a greater stage.", 'Restore the fierce competition and explicit perspective of people living at sea.', 'His elevated earnest rhetoric is intentional and sets up Maria\'s amused response. Preserve maritime hegemony without inventing a particular war, state or rank.'),
69:('…', 'Maria\'s pause before laughing already works.', 'Keep the beat between the captain\'s grand statement and her amusement. It is not assent to a joint plan.'),
73:('Pfft! How can you say that with a straight face?', 'The idiom carries her amused disbelief more naturally than shamelessly.', 'She laughs at his unabashed earnestness. Straight face is an idiom for delivery, not a new literal animation or an accusation that he has confessed to lying.'),
77:('…', 'His silent response to the laughter already works.', 'The pause allows Maria to apologize and reassess him. Do not supply anger, embarrassment or a romantic reaction as spoken fact.'),
81:("Heh... Sorry. You seem like someone I can trust. All right, then. I'll have you help me.", 'You may help sounds like a detached permission rather than her unilateral decision to obtain his help.', 'The light apology, qualified trust and assertive turn to cooperation preserve her confident voice. No new command rank or already accepted alliance is established.'),
84:("I'm not sure what you're talking about... But who are you in the first place?", 'Nothing you say makes sense overstates his confusion and loses the in-the-first-place challenge.', 'The captain has not yet agreed to cooperate. Keep his uncertainty and renewed identity question in the full exchange.'),
89:("Me? Ｉ'm Maria Huamei Li.", 'The effective introduction already uses the approved full name and works naturally.', 'Retain the complete approved name and simple introduction. The existing full-width I is preserved as an exact predecessor value pending native formatting; it does not license a new biography or global encoding rule.'),
98:("What?! You're with the Li family? What are you doing here?", 'Family gives a more neutral source-bound rendering of 一家 than the potentially loaded clan.', 'With the Li family identifies the source family/group connection without inventing a specific blood relationship, criminal organization or official post. This pair of lines remains conditional.'),
102:("Taking a look at the enemy, you might say. Keep it to yourself. Officially, I'm not here.", 'This meeting never happened replaces the source claim about her unacknowledged presence.', 'Restore reconnaissance of the enemy, secrecy and her officially absent status. Do not invent a disguise, employer, city or actual erasure of the meeting.'),
111:('{MACRO:FA}, do you know Kuhn and Pereira?', 'The polite familiarity question already works.', 'Keep the surname address and the two individually source-bound names. It introduces four alternative replies, not a sequence of contradictory answers.'),
126:('Yes.', 'The brief affirmative familiarity reply already works.', 'This is one structural alternative. Do not concatenate it with the following name questions or the negative reply.'),
132:('Kuhn?', 'The uncertain name echo already works.', 'Preserve the established fictional surname. Do not identify a historical person or append biography to explain this alternative reply.'),
147:('Pereira?', 'The alternative uncertain name echo already works.', 'Keep the source-bound surname and question. This is a different familiarity path, not the next answer after Kuhn.'),
153:('...No.', 'The hesitant negative familiarity reply already works.', 'Keep this alternative answer separate from the yes and name echoes. It adds no backstory about earlier meetings.'),
165:("They're prime examples of what I mean by enemies. Even now, they're locked in a standoff over control of the Spice Islands and their enormous profits.", 'Restore the prime-example wording, present standoff, sovereignty and large profits.', 'Maria identifies the kind of enemy she means and the commercial cause of rivalry. Do not reduce the conflict to simple desire for islands or invent a settled winner.'),
168:("They'll stop at nothing to serve their own interests. They bombard towns and seize them by force, then treat the spice-producing lands as their own private property.", 'Restore ruthless self-interest, forced occupation and private appropriation of production areas.', 'The preceding Spice Islands context supplies what is produced. Preserve these concrete abuses without adding deaths, a legal property deed or a new tax system.'),
172:("Kuhn's methods are especially appalling. He mercilessly arrests citizens who displease him in the slightest and crushes rebellions by force.", 'Resists is narrower than displeasing him even slightly; restore the lack of mercy.', 'The accusation covers arbitrary arrests and violent suppression. Do not invent executions, a death count or historical atrocities outside this fictional dialogue.'),
175:("...I see. I understand the sort of enemy you're talking about. So, what kind of help do you want?", 'Restore understanding the kind of enemy and a question about the requested cooperation.', 'The captain now understands her category of enemy but asks what cooperation means. He has not yet accepted a detailed plan or offered unspecified reinforcements.'),
179:("For a start, don't interfere with my plan.", 'Stay out of my plan suggests exclusion rather than not obstructing it.', 'Her assertive request is to avoid interfering. Preserve that word so the captain\'s next incredulous echo makes sense.'),
182:('Interfere?', 'Hindrance? is an unnatural isolated noun in this exchange.', 'Echo her preceding verb in natural English. His objection concerns being treated as an obstacle, not a newly discovered obstruction mechanic.'),
186:("I'll set them against each other to weaken them, then seize the opportunity to drive them both out of Asia at once.", 'Restore her active manipulation and exploitation of the opening, rather than passively waiting.', 'This is her prospective strategy. It does not say the two men are already weakened, expelled or under her control in actual gameplay.'),
190:('Will that work?', 'The skeptical question about the strategy already works.', 'The captain tests the feasibility of the plan before raising its moral cost. This does not promise success or assert failure.'),
194:("It'll take time, though.", 'With time is an overly compressed fragment.', 'The qualification admits delay; it does not guarantee eventual victory, set a date or remove the cost he raises next.'),
198:('That means turning a blind eye to their atrocities until then.', 'The predecessor loses the moral agency in overlooking the abuses.', 'The captain objects to tolerating the abuses while the plan unfolds. The idiom is moral criticism, not a claim that a particular person literally cannot see.'),
201:('…', 'Maria\'s silence at the objection already works.', 'Do not fill the pause with a confession, agreement or additional strategic explanation absent from the source.'),
205:('Care to hear my proposal?', 'Will you hear my proposal is stiff in ordinary dialogue.', 'The direct idiomatic offer suits his reserved voice and precedes his blunt alternative. It does not yet commit Maria to accept it.'),
209:('...What is it?', 'The complete question better expresses asking what the proposal is.', 'Maria invites the explanation. The pause preserves her guarded response without implying ignorance of every earlier point.'),
213:("No tricks. I'll drive them out. That's all.", 'Restore the captain\'s explicit I and natural finality.', 'He offers direct action as his proposal. I is his declared agency as captain, not a claim he will fight without his fleet or that the expulsion is already complete.'),
216:('You will?', 'The short skeptical echo already works.', 'Her emphasis questions his ability to do what he proposes. It is not acceptance or a request for a promise of personal sacrifice.'),
220:("Drop the act. That's what you wanted me to say, isn't it?", 'Restore the idiomatic accusation of acting and the rhetorical question.', 'He sees the attempted manipulation and challenges it. Keep the dry interplay without inventing a hidden romance or making her motive narrator-established fact.'),
223:('...Heh.', 'Her quiet amused acknowledgment already works.', 'The understated chuckle follows his recognition of the act. It does not add a spoken confession or romantic response.'),
227:("You win. Let's stop the games. I have my reasons, but it's true that I can't spare a fleet to send here right now.", 'Restore the concession, end to maneuvering and present inability to spare a fleet.', 'The reasons remain unspecified. Do not invent their cause, claim her fleet physically cannot travel here, or promise that reinforcements will arrive later.'),
230:("Still... I'm uneasy about leaving it all to you.", 'Leaving this to you seems risky is detached; the source states her own misgivings.', 'Keep the qualified concern about relying entirely on his group. It does not say she will abandon her plan or supply reinforcements.'),
234:("You don't hold back, do you?", 'Bold words loses the natural dry retort to her doubts.', 'The captain bristles at her frank assessment. This rhetorical question adds no threat, rank or pledge to prove himself by a specific action.'),
238:("Kuhn seized Portugal's holdings in this region just recently, and did it in no time at all. He's no ordinary opponent. He won't be easy to deal with.", 'Restore the recent transfer, regional scope, speed and warning that he is difficult to handle.', 'Maria cites the source\'s fictional strategic record. Do not import a historical identity, dates, a specific battle or additional colonial biography.'),
241:("Don't let impatience make you overreach. You'll invite a nasty counterattack. And keep in mind, my plan is going ahead unchanged.", 'Restore overextension, the warning\'s causal force and notice that her original plan continues.', 'This is her strategic prediction and declared intention, not narrator certainty about a future battle. No actual counterattack or completed plan is newly established.'),
244:('...Do as you wish.', 'The captain\'s gruff dismissal already works.', 'He leaves her to her own plan rather than making a new alliance promise or endorsing every part of it.'),
},
68:{
5:('{MACRO:FI}! Please help!', 'The urgent name call and plea already work.', 'Camille asks the captain for help. Preserve the given-name macro without adding an honorific rank or explaining the danger before his next lines.'),
8:('Camille? What happened?', 'The recognition and concerned question already work.', 'The captain recognizes the approved name and asks what is wrong. No new personal relationship is implied.'),
12:('Lil... Lil is in danger!', 'Restore the repeated name that carries his urgent distress.', 'The repetition is purposeful emotional delivery, not a padding artifact. Danger is prospective; this line does not say she is already captured or dead.'),
16:('What do you mean?', 'The predecessor repeats the previous question instead of asking for clarification.', 'The captain asks what kind of danger Camille means. It naturally prompts the explanation of Kuhn\'s deception.'),
20:("Kuhn's deceiving her! At this rate, she'll fall right into the trap he's set!", 'Restore ongoing deception and the explicit prospective condition.', 'The trap is set, but she has not necessarily fallen into it yet. Preserve the warning without making the trap\'s outcome or exact mechanism a completed fact.'),
24:("I don't quite understand... Never mind. Where is she?", 'The predecessor is clipped and drops his decision to act despite incomplete understanding.', 'The captain sets aside the explanation to ask the location. This is practical urgency, not a claim that he understands the entire scheme.'),
27:("Batavia! I'm sorry. I'll explain everything properly later!", 'Restore Camille\'s own apology and promise to explain, rather than an impersonal passive.', 'Keep the explicit Batavia location. The explanation is promised for later, not supplied or guaranteed to have occurred in this utterance.'),
30:('All right! Come with me!', 'Good is an odd response to danger; the source accepts action and tells him to come along.', 'The captain decisively takes Camille with him. No new destination beyond Batavia or formal appointment is added.'),
},
69:{
6:('Lil! Thank goodness we made it in time!', 'Restore the explicit relief at arriving in time.', 'Camille\'s relief follows the linked rescue scene. We refers to his arrival with the captain, not a new rescue party or an invented outcome beyond that context.'),
11:("Ｉ'm sorry! Ｉ'm so sorry, Camille... Ｉ... Ｉ believed that man and ignored you when you tried to stop me...", 'The effective apology already preserves her repetition, regret and ignored warning.', 'Retain the full emotional apology as one logical paragraph. The current full-width I values remain exact pending native formatting; no guessed confession or romance is added.'),
14:("Don't worry, Lil.", 'Camille\'s gentle reassurance already works.', 'His reply accepts her apology without adding an explicit new judgment, promise or relationship label.'),
19:("No. I almost doubted Maria. I'm so glad you came back.", 'Nearly became my enemy is a different relationship claim from almost doubting Maria.', 'Restore the narrowly averted doubt and warm welcome back. She does not say she actually betrayed Maria, made her an enemy or resumed a romantic relationship with Camille.'),
23:('Thank {MACRO:FI}.', 'The concise redirection of thanks already works.', 'Camille credits the captain rather than claiming sole responsibility. Preserve the exact given-name substitution.'),
26:("I only brought you here. Nothing more. I don't know the whole story, but it looks like things can go back to normal now.", 'Restore the captain\'s personal modesty and prospective return to the earlier situation.', 'Back to normal localizes 元の鞘 in this restored working relationship. Do not use a literal scabbard, imply marriage or romance, or claim he knows the whole dispute.'),
30:('Huh? Oh, um... Lil, could I come aboard your ship again...?', 'Restore the startled, hesitant lead-in and explicit ship.', 'The request is permission to return aboard. His hesitation does not by itself prove romantic embarrassment, a resignation or the reason for his earlier separation.'),
34:("Of course! Things were tough while you were gone! You'd better make up for the work you missed!", 'Restore the practical difficulty and work to make up without inventing an exact doubling.', 'Lil\'s warm, bossy teasing welcomes him back and demands work. Do not turn Life was awful into a romantic confession or twice as hard into a source-specified workload.'),
38:('Looks settled.', 'The captain\'s understated apparent-resolution comment already works.', 'Looks preserves the tentative assessment after her welcome. He does not claim knowledge of every circumstance or make the relationship romantic.'),
42:("{MACRO:FI}, you helped me when I couldn't even explain what was going on. Thank you so much.", 'Restore Camille as the one unable to explain, avoiding the ambiguous without any explanation.', 'His sincere thanks recognizes help despite the incomplete account. Preserve the macro and agency without inventing why he could not explain or promising a new reward.'),
45:("Don't mention it. You two get along now.", 'Enough sounds dismissive of sincere thanks; the source gently closes it.', 'The ordinary response to gratitude and brief good wish fit the captain\'s reserve. No marriage advice, parenthood, romance or new protective obligation is added.'),
},
70:{
6:("Admiral, Kuhn's hidden wealth has been found.", 'Make the hidden wealth explicit and use a natural current report.', 'The source explicitly addresses the captain as admiral here. The passive report does not invent who found the wealth, its exact amount or a specific search operation.'),
9:('Distribute it all among his victims.', 'The complete distribution order already works.', 'All preserves the whole amount and victims identifies people harmed by Kuhn. Do not add taxes, a personal reward or a nationality absent from the source.'),
12:('This was mixed in with it...', 'The report about the unnamed object already works.', 'Keep the object deictic and the hesitant ending. Surrounding opaque item commands do not authorize naming it in this line.'),
15:('This?', 'The captain\'s short puzzled question already works.', 'The question reacts to the object without identifying it or inventing recognition. Its concise delivery suits the reserved speaker.'),
}})

CONTEXTS={
63:'Nagarpur and his entourage demand passage. He patronizingly assumes the captain wants a tip; the captain and conditional crew replies reject the insult and his worship of wealth. His company\'s new wealth and apparent regional influence emerge before the argument over money versus ability. The captain leaves; Gerhard proposes a lesson by fleet power. Preserve pomp, rude cultural address, moral contempt and the source appearance insult without invented titles, bribe amounts, a completed payment or an actual declaration of war.',
64:'Alternative gift paths acclaim the captain as sea king or have Sera identify him with her country\'s legend. A separately conditional later leaf explanation describes silver hair, blue eyes, an iron ship and the kingdom\'s inherited treasure. His skeptical laughter hurts her culturally and personally; he apologizes but rejects the identification, then agrees to search. Preserve separate paths, her learner voice and his awkward comic defensiveness without a proven prophecy, romance or named item invention.',
65:'Sirwood and Sera recognize one another and exchange deliberately opaque symbol speech. The captain discovers her compatriot has survived; she announces her return to her country, encourages his naval dream and hopes to meet again. His warning includes himself. She says something still opaque, then thanks him and leaves. Conditional crew pauses and a question lead to his qualified confidence in her resilience. Preserve the unknown words, respectful learner speech and understated feeling without invented kinship, decoded confession or promised reunion.',
66:'A Port Worker warns a stranger about Kuhn and Pereira. The later doubly conditional exchange lets Hodram and Camille recognize one another from the clean prior Lil encounter. Camille evades questions about his temporary separation from Lil and breaks off; Gerhard senses an unexplained reason. Do not convert familiar address into brotherhood or age, or invent the cause and nature of the separation.',
67:'A courteous invitation leads to Maria\'s conditional challenge over Western exploitation of Asia. Hodram states his naval purpose and candid ambitions; she laughs, apologizes and seeks his help. Her full introduction and secrecy exchange are conditional, as are four alternative familiarity replies. She details Kuhn/Pereira\'s rivalry and abuses and proposes weakening them against one another; he rejects tolerating the abuses and offers direct action. She concedes her present fleet constraint while doubting his group and warning that Kuhn is formidable. Both keep their plans. Preserve the political, moral and strategic interplay without invented ranks, historical biography, promised reinforcements or completed future outcomes.',
68:'Camille urgently requests help because Lil is being deceived and risks falling into Kuhn\'s trap. The captain asks for enough information to act, learns Batavia and takes him along despite an incomplete explanation. Preserve urgency, prospective danger, named location and the promised later explanation without inventing captivity or a completed trap.',
69:'After the explicitly linked false-flag fleet rescue, Camille is relieved to arrive in time. Lil apologizes for ignoring his warning and nearly doubting Maria; he redirects thanks to Hodram. The captain modestly sees a return to normal; Camille asks to rejoin the ship and Lil warmly scolds him about missed work. Camille thanks the captain, who closes with goodwill. Preserve relief, working companionship and neutral reconciliation without invented marriage, romance, betrayal or a doubled workload.',
70:'Kuhn\'s hidden wealth is reported, and the captain orders all of it distributed among the people harmed by him. A mixed-in unnamed object prompts a question. Preserve the all/victims scope and leave the object unidentified rather than importing a label from opaque commands.'
}

SPEAKERS={1:'Hodram',2:'Lil',3:'Maria',9:'Camille',10:'Xien Yan',16:'Gerhard',17:'Al Shin',18:'Charles',20:'Fernando',23:'Manuel',24:'Sera',38:'Nagarpur',78:'Sirwood',105:'Trader',116:'Port Worker',154:'Sailor'}

def normalized_previous(text):
    return re.sub(r'\b(FI|FA|FO)\b',lambda m:'{MACRO:'+m[1]+'}',text)

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists()
    current,gloss,view,paths,names,partial,verified=map(read,[CURRENT,GLOSS,VIEW,PATHS,NAMES,PARTIAL,VERIFIED])
    ledgerpath=Path('translations/editorial_review_current_v1.json');before=ledgerpath.read_bytes();ledger=read(ledgerpath)
    assert sha(before)==verified['ledger_sha256'] and verified['pass'] and ledger['records_editorially_completed']==7319
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert current['all224_source_units_uncredited_in_current_ledger'] and current['source_first_glosses_andcomplete_native_page_view_precede_current_English']
    assert view['all23_source_sheets224_complete_native_pages_directly_viewed_before_current_English'] and len(names['records'])==16
    completed={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']}
    assert not completed&{historical_key(r) for r in current['records']}
    assert len(partial['records'])==44 and partial['revised']==32 and partial['retained']==12
    assert set(LINES)==set(range(63,71)) and sum(map(len,LINES.values()))==180
    earlier={r['id']:r for r in partial['records']};pathgroups={g['block']:g for g in paths['groups']}
    rows=[];macros=dict(FI=0,FA=0,FO=0);symbol_rows=[]
    for original in current['records']:
        if original['id'] in earlier:
            row=deepcopy(earlier[original['id']]);assert row['block'] in [61,62]
        else:
            row=deepcopy(original);text,finding,note=LINES[row['block']][row['source_record_index']]
            assert text==text.strip() and not any(v in text for v in ['\n','\r','{LB','{ALIGN','{PAD','  ','%']);text.encode('cp932')
            old=normalized_previous(row['effective_predecessor_paragraph']);decision='retention' if text==old else 'revision'
            group=pathgroups[row['block']];member=next(r for r in group['utterance_membership'] if r['id']==row['id']);neighbors=[]
            for model in group['binary_models']:
                ids=model['source_speech_IDs']
                if row['id'] not in ids:continue
                at=ids.index(row['id']);pair=dict(previous=ids[at-1] if at else None,following=ids[at+1] if at+1<len(ids) else None)
                found=next((p for p in neighbors if all(p[k]==v for k,v in pair.items())),None)
                if found:found['structural_models'].append(model['model'])
                else:neighbors.append(dict(**pair,structural_models=[model['model']]))
            assert neighbors and row['source_meaning_gloss'] and row['whole_exchange_fidelity_note']
            row.update(english=text,logical_English=text,speaker=SPEAKERS[row['source_selector']],source_meaning=row['source_meaning_gloss'],
                context=CONTEXTS[row['block']],localization_note=note,finding=finding,decision=decision,retention_reason=note if decision=='retention' else None,
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                exact_structural_neighbor_pairs=neighbors,structural_membership=member,whole_clean_exchange_andcadence_emotional_progression_reviewed=True,
                structural_neighbors_not_actual_eligibility_orcontinuous_chronology=True,
                prior_raw_storage_preserved=row['current_raw_storage_English'],prior_effective_paragraph_preserved=row['effective_predecessor_paragraph'],
                prior_macro_normalized_comparison=old,planned_English_markup='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+text,
                source_only_not_localized_dialogue_orreview_credit=False,
                no_authored_linebreak_alignment_padding_orallocation_driven_shortening=True,
                formatting_native_stored_actual_policy_atomic_registered_integration_andcompletion_credit_pending=True,
                no_source_prose_counter_orcompletion_credit=True)
        for macro in macros:
            n=bytes.fromhex(row['source_hex'])[1:].count(macro.encode());assert row['english'].count('{MACRO:'+macro+'}')==n;macros[macro]+=n
        if any(c in row['source_Japanese'] for c in ['○','×']):
            assert row['block']==65 and row['english']==row['source_Japanese']==row['effective_predecessor_paragraph'] and row['decision']=='retention';symbol_rows.append(row['id'])
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        rows.append(row)
    assert len(rows)==len({r['id'] for r in rows})==224 and macros==dict(FI=15,FA=3,FO=0) and len(symbol_rows)==6
    assert [r for r in rows if r['block'] in [61,62]]==partial['records']
    revisions=sum(r['decision']=='revision' for r in rows);retentions=len(rows)-revisions
    evidence={str(p):sha(p.read_bytes()) for p in [PARTIAL,CURRENT,GLOSS,VIEW,PATHS,NAMES,VERIFIED,Path(__file__)]}
    save(DOC,dict(format='dk4-whole-exchange-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=current['current_ARM9_sha256'],
        current_COMMON_sha256=current['current_COMMON_sha256'],current_archive_sha256=current['current_archive_sha256'],file_path='/data/SC1.DK4',
        blocks=list(range(61,71)),records=rows,total_editorial_objects=224,physical_speech_objects=224,typed_choice_objects=0,typed_choice_records=[],
        revised=revisions,retained=retentions,source_macro_counts=macros,source_FE_panels=0,source_relative_sites=60,source_query_sites=15,source_commands=392,
        first44_all_record_values_reused_exactly=True,prior_partial_manuscript=str(PARTIAL),prior_partial_manuscript_sha256=sha(PARTIAL.read_bytes()),
        six_deliberately_opaque_B65_utterances_retained_exactly=symbol_rows,
        all224_individual_source_context_localization_naturalness_gates_true_formatting_false=True,
        no_native_English_wrapping_stored_actual_orrelease_approval=True,whole_exchange_andalternate_branch_context_reviewed=True,
        all224_clean_first_meanings_names_native_source_andlinked_context_precede_English_comparison=True,
        names_packet=str(NAMES),names_packet_sha256=sha(NAMES.read_bytes()),source_context=str(GLOSS),source_context_sha256=sha(GLOSS.read_bytes()),
        current_packet=str(CURRENT),current_packet_sha256=sha(CURRENT.read_bytes()),source_native_view=str(VIEW),source_native_view_sha256=sha(VIEW.read_bytes()),
        ordinary_wrapping_owned_by_formatter=True,all_prior_full_scope_leads_names_graphics_andlater_technical_reaudit_preserved=True,
        no_new_ROM_registered_integration_orcompletion_credit=True,new_credit=0,full_goal_complete=False,evidence=evidence))
    ROOT.mkdir(parents=True)
    save(ROOT/'224_contextual_decisions_formatting_still_pending.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        records=[{k:r[k] for k in ['id','source_reference','source_hex','source_Japanese','current_reference','current_hex','prior_effective_paragraph_preserved','english','decision','finding','localization_note','retention_reason','exact_structural_neighbor_pairs','review']} for r in rows],
        revised=revisions,retained=retentions,first44_value_exact=True,new_individual_decisions=180,
        all_English_formatting_storage_actual_production_atomic_andrelease_gates_pending=True,
        new_credit=0,new_emulator_runs=0,no_ROM_registry_orledger_change=True,full_goal_complete=False,evidence=evidence))
    assert ledgerpath.read_bytes()==before
    print(f'224 whole-exchange decisions: {revisions} revisions/{retentions} justified retentions; first44 exact,180new. FI15/FA3/FO0; sixopaque utterances exact. All formatting/storage/actual/release gates pending;zero credit.')
