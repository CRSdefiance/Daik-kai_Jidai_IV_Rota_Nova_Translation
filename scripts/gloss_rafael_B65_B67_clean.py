"""Read village investment,construction andflower exchanges as complete source conversations."""
from pathlib import Path
from scripts.source_only_gloss_v1 import seal

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
MEANINGS={
65: '''
5|Charlotte hands over this visit's batch of goods.
9|Rafael thanks her andasks to raise another subject.
13|Charlotte asks what it is.
17|Rafael says that,if they are to trade,he thinks they should construct a proper trading post.
22|Charlotte repeats the unfamiliar proposal,a trading post.
26|Rafael explains that it would handle more kinds of goods andspecialize in buying andselling.
30|He says ships would then make a detour to visit specifically for trade.
35|Charlotte objects that a proper trading post would need workers andthe villagers already have their hands full with their current work.
39|Rafael suggests hiring people:the trading post would attract ships andpeople seeking work in the town.
43|Charlotte asks how they could pay those workers' wages.
46|Rafael proposes soliciting commercial investment from merchants at the trading post;after the initial funds arrive,trading profits could sustain it.
51|Charlotte questions whether it would work,because the village lacks specialties valuable enough to bring merchants to a trading post.
54|Rafael says investment would develop the village,allowing it to produce more specialty goods andeven new ones.
58|Charlotte wonders whether anyone would invest.
61|Rafael enthusiastically volunteers to invest himself.
66|After a pause,Charlotte says it still cannot be done.
69|Rafael asks why.
74|Charlotte explains that the area has almost no building stone ortimber,so they cannot construct a large trading post.
78|Rafael says they can transport the materials in;he will supply timber andasks her to wait without worrying.
''',
66: '''
5|Charlotte excitedly addresses FI as he arrives.
9|Rafael greets her,says he has obtained timber andproposes using it to build the trading post.
14|Charlotte is impressed butexplains that the village cannot afford to buy so much timber.
18|Rafael says he does not need payment.
23|Charlotte objects in surprise at accepting the gift.
27|Rafael frames it as part of his investment:when the village has plentiful specialty goods,he will be first in line to buy them.
31|Charlotte thanks FI andpromises to work hard toward a fine trading post,though it will take time.
35|Rafael says he will look forward to it.
40|Charlotte eagerly says there will be much to do andshe must work hard.
''',
67: '''
5|Charlotte hands over the current batch of goods.
9|Rafael thanks her andhesitantly says he has something to give her.
14|Charlotte asks what it is.
18|Rafael gives her corn seeds,thinking corn could become a new trade good for the village.
23|Charlotte is overwhelmed because FI is always doing kind things for her;her thought trails off.
26|Rafael awkwardly says she need not make much of it,as more specialty goods would benefit his people too.
31|Charlotte accepts his explanation andthanks him,saying everyone will be happy.
34|Rafael is glad butnotices that her many packages look difficult to carry.
38|Charlotte says she is fine,because regular farmwork has made her strong.
41|Rafael still hesitates with concern.
46|Claudio tells FI to walk her home.
49|Rafael is surprised by the suggestion.
54|Charlotte says she could not impose andinsists she really is fine,demonstrating with the load.
57|Claudio dismisses the objection andasks to take the packages for a moment.
60|Claudio splits the packages in half anddeliberately makes FI's portion a little heavier.
64|Claudio announces that the division is done andhands over the resulting load.
67|Rafael protests to Clau as the load is thrust upon him.
71|Charlotte apologizes andasks whether it is heavy.
74|Rafael quickly insists that it is not heavy at all.
78|Rafael says he will go for a little while andbegins asking Clau to handle the remaining business.
82|Claudio tells him to leave it to him andhurries the pair on their way.
85|Once they leave,Claudio pauses andsighs with a sense of effort andsatisfaction.
88|Claudio grumbles that Rafael fails to follow through at the crucial moment andneeds him looking out for him;preserve the fond matchmaking implication without inventing a declared relationship.
97|Charlotte welcomes Rafael inside andoffers to make tea.
100|Rafael agrees.
105|Charlotte notices his reaction andapologizes,assuming he is surprised.
109|She ruefully laughs that there is practically nothing in the house:beyond a roof andwalls,it barely deserves the name.
113|Rafael asks how long Charlotte has lived there.
118|She says she left Europe at eleven,about six years ago,andhands him his tea;preserve both the age andelapsed time.
122|Rafael thanks her andbegins calculating from eleven plus six years.
126|Rafael realizes she is seventeen andthe same age as he is;these ages are explicitly stated,not inferred from portraits.
131|He admits he had assumed she was older,then catches himself.
136|Charlotte asks whether that surprises him andpoints to her rough skin andwork-worn hands.
140|She says she hardly seems like other girls her own age.
143|Rafael denies that her appearance caused his assumption;he thought her older because she is so capable andself-possessed.
148|Charlotte says FI is very beautiful,almost like a girl.
152|Rafael is startled by the girl comparison andwonders whether he seems so unreliable;the misunderstanding is his own.
156|Charlotte says she did not mean that;she starts an unfinished thought about the person who must surely stand beside him.
160|Rafael asks what she means by calling her name.
165|Charlotte dismisses the unfinished thought andabruptly notices that the sun is setting.
169|Rafael agrees that it is getting late andsays he must return quickly.
173|Rafael starts saying goodbye.
178|Charlotte calls FI back andasks him to wait a moment.
181|Rafael waits in mild puzzlement.
186|She apologizes for keeping him waiting andoffers something.
190|Rafael admires the pretty flower andasks whether it is for him.
194|Charlotte nods andsays it is thanks for today,adding that it is all she has to give.
198|Rafael thanks her andsays it makes him very happy.
202|Charlotte hopes that by his next visit,the seeds he gave her will have grown well.
206|Rafael says he looks forward to it andsays goodbye.
210|Charlotte returns his goodbye.
214|Claudio asks Arcadius whether he has seen FI.
218|Arcadius tells Clau that FI returned a little earlier andwas watering a flower.
221|Claudio slowly echoes flower,clearly intrigued.
225|Arcadius explains that Rafael wanted a vase,andwhen Arcadius brought one,he was gazing at the flower with a broad smile.
229|Arcadius wonders whether something good happened.
233|Claudio knowingly starts drawing a conclusion,leaving it unfinished.
237|Arcadius notices that Clau knows something.
241|Claudio awkwardly admits he knows a little.
245|Arcadius calls it unfair to keep the amusement to himself,asks him to tell,andguesses it concerns the girl they met earlier.
249|Claudio chuckles andbegins explaining.
252|A pause stands in for the intervening account;do not invent a newly spoken story.
256|Arcadius understands andlaughs that,besides the village's development,they now have something else to look forward to;preserve the affectionate romantic speculation as speculation,not a declared couple.
260|Claudio enthusiastically agrees.
'''}
CONTEXT={
65:'Complete proposal after a trade:trading-post staffing,wages,merchant investment,profits,specialty development andthe shortage of stone/timber. Rafael offers concrete investment rather than making an unsupported charity promise. The predicted commercial benefits remain his proposal,not already-realized outcomes.',
66:'Complete timber delivery/construction promise. Charlotte cannot pay;Rafael calls the timber an investment andexpects to be a future customer. Building a fine trading post takes time;do not translate the promise as completed construction.',
67:'Complete corn-seed/carrying visit,tea andflower gift,thenClaudio/Arcadius gossip. Keep corn as the specific crop,eleven plus six years/seventeen as explicit facts,andthe same-age reveal. Claudio arranges the walk andheavier load;Charlotte is self-conscious andleaves her ideal-partner thought unfinished. Affection andcompanions romantic speculation are intentional,butno established romantic relationship is stated. Public Arcadius speaker identity remains unchanged;do not globally infer everyone knows the private Eirene identity.'}

if __name__=='__main__':
    seal(ROOT/'clean_source_packet.json',ROOT/'B65_B67_92_clean_meanings_v1.json',MEANINGS,CONTEXT,__file__)
