"""Seal three complete recruitment exchanges,including both Janus choice branches,from clean Japanese."""
from copy import deepcopy
from pathlib import Path
from scripts.meaning_maria_B58_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

CONTEXT={
59:'Maria and Janus seek a skilled navigator in a shipping town. A shopkeeper hints at Adernkatz,the boy identifies Admiral Adernkatz,and they visit Gerhard. He is retired anddismisses his age;Maria respectfully insists he is not old andasks him to guide them. Their silent exchange turns into his amused acceptance. The earlier part of his life might have differed had he met her sooner;do not invent a specific lost war orfamily story.',
60:'Janus approaches Maria for work andproposes a1000-gold condition. Richard objects to his apparent impudence. The payment branch waits one day andreveals he repaired a ship andpaid his debts,testing whether Maria has the stature of an admiral he can trust with his life. He offers the ship andmisunderstands her request for his own name. The alternative refusal branch says she lacks that much money andhe will try elsewhere. The FE instruction explains retrieving/renaming the ship. Do not combine alternatives into one earned outcome.',
61:'A blast interrupts Maria andXien on reaching the far West from the East. A shipyard man complains about Charles\'s repeated science experiments. Maria is interested in science changing daily life;Xien infers his bomb knowledge could help gunnery. They recruit the excitable,self-important scientist after Xien praises Maria in an explicitly abridged account. Maria\'s polite elderly-gentleman introduction prompts Xien\'s comic protest. No blood relationship between Charles andthe shipyard man is established.',
}
MEANINGS={
59:{
4:'Maria observes that shipping is thriving in this town too andwonders whether a capable navigator can be found.',
7:'Janus agrees andoffers to ask around.',
10:'Janus politely stops someone andsays they are looking for a person knowledgeable about ships.',
13:'The shopkeeper recognizes them as sailors andbegins a hesitant reference to Mr. Adernkatz. His familiar respectful address does not establish nobility.',
17:'The shopkeeper withdraws the comment andgives an odd chuckle.',
20:'Janus finds the shopkeeper unsettling,tries to recall Adernkatz\'s name,anddecides to look for him.',
24:'Janus asks a boy whether he knows someone named Adernkatz.',
28:'The boy identifies Admiral Adernkatz andpoints them toward his mansion. Admiral is explicitly supported here.',
31:'Janus thanks the boy andtells Admiral FI that the man\'s house seems to be over there;preserve FI as a live name token.',
35:'Maria says they should go andsee.',
40:'Janus wonders if they have found the right place.',
44:'This FE record is the sound of knocking,not a spoken actor line.',
49:'Gerhard asks who is there.',
53:'Janus politely greets him andstarts introducing them as from FO,then trails off. Preserve the live faction token.',
56:'Maria introduces herself as FI FA andidentifies her companion as the navigator Janus Pasar. Preserve both live name tokens andapproved Janus spelling.',
60:'Gerhard shows interest at navigator andinvites them inside.',
63:'Gerhard asks the purpose of their visit.',
67:'Maria says she heard he was a skilled navigator andcame to speak with him;her line trails off.',
70:'Gerhard says that was long ago andthat he now lives ashore,as they can see.',
73:'Maria asks him to take to sea again.',
76:'Gerhard doubts that an old hand like himself could be useful. Preserve self-deprecation,not confirmed incapacity.',
80:'Maria says he is not old andrespectfully asks him to guide/instruct their group.',
83:'Gerhard pauses silently,considering her.',
87:'Maria holds the silence in response.',
91:'Gerhard gives a brief amused breath/chuckle.',
95:'Janus is puzzled by the silent exchange.',
99:'Gerhard says that if he had met someone like Maria sooner,the earlier part of his life might have been different. Preserve the counterfactual anduncertainty.',
103:'Maria asks whether that means he accepts.',
107:'Gerhard agrees andformally places his abilities as Gerhard Adernkatz at her disposal.',
},
60:{
4:'Janus acknowledges his approach is rather sudden/out of the blue.',
8:'Maria responds with a silent beat.',
13:'Janus hesitantly asks Maria to hire him.',
23:'Richard brusquely demands to know who Janus is;do not add a class-based insult.',
32:'Maria asks whether Janus has any particular skills.',
36:'Janus likes machinery andis good at handling ships andmaking repairs.',
39:'Maria asks his terms/conditions.',
43:'Janus makes his request:give him1000 gold. Preserve the exact amount.',
53:'Richard is outraged by his impudence andtells the admiral she need not concern herself with such a man.',
'SC3_B60_CHOICE_428_0':'Maria chooses to pay him;preserve affirmative payment rather than a generic yes.',
'SC3_B60_CHOICE_428_1':'Maria says she does not have that much money. This is a funds-based refusal,not contempt orbare unwillingness.',
73:'Janus thanks her andexclaims that he can now make the repair;the object is revealed later.',
76:'Janus adds an apology andasks them to delay departure for just one day.',
79:'Maria agrees.',
90:'Richard protests that the admiral must not allow this;he thinks Janus is taking advantage of their kindness.',
94:'Richard demands whether Janus realizes whom he is addressing. Preserve his presumptuous indignation without inventing a formal court rank.',
102:'Janus cheerfully says they will meet at the port tomorrow.',
113:'Richard calls after him angrily to stop.',
125:'Janus has been waiting for them andinvites them over to look at something.',
129:'Maria reacts with surprise.',
133:'Janus says yesterday\'s repair money let him finish repairing the ship andhe has just repaid his debts too. Preserve both uses/results,not a purchase price.',
137:'Janus apologizes for testing Maria;an admiral to whom he entrusts his life must have suitable capability/stature. Do not turn this into a specific financial test orclaim she proved generosity alone.',
140:'Janus feels safe entrusting himself to Maria andoffers the ship for her use if she wishes.',
143:'Maria asks the name,leaving its referent unstated until the following comic misunderstanding.',
147:'Janus assumes she means the ship andsays she may choose any name she likes.',
151:'Maria clarifies that she asked for his name.',
155:'Janus apologizes:he was so excited yesterday that he failed to introduce himself.',
159:'He introduces himself as Janus Pasar andoffers a polite greeting for their future work together.',
164:'The FE instruction tells the player to take the ship out of dock andgive it a chosen name with the Refit/改造 command. Match the validated menu label before final approval.',
170:'In the refusal branch,Janus accepts that it cannot be helped andsays he will ask elsewhere.',
173:'Maria responds to the refusal outcome with a separate silent beat.',
},
61:{
4:'Xien reflects that they have finally come so far,from the world\'s eastern edge to its western edge,andfinds it moving. Do not insert a city name absent from this dialogue.',
8:'Maria asks what the loud blast/roar is.',
12:'Xien thinks it sounds like a bomb. Preserve his tentative identification.',
15:'The shipyard man complains that Charles is at it again,preventing a peaceful nap;he wishes Charles would be quiet occasionally.',
19:'Maria asks whether this Charles caused the thing just called a bomb.',
23:'The man confirms Charles is a nuisance to the neighborhood,obsessed with something called science,andmakes the booming noises almost daily.',
27:'Maria asks Xien what science is.',
30:'Xien calls it a field of study popular in the West,said to be powerful enough to change how people live. Bombs are one example/application. Keep the reported nature of the claim.',
34:'Maria is especially interested in how it could change ways of life andwants to learn more.',
38:'Xien reasons that if Charles can make bombs,he may know gunnery,andproposes meeting him. This is inference,not an already-confirmed skill assessment.',
42:'Maria agrees he seems worth meeting.',
46:'The shipyard man asks whether they are serious/sane.',
50:'Maria asks him to guide them to Charles andoffers to reward his trouble.',
53:'The man says escorting her would be easy,butstill thinks she should not go. His young-lady address does not establish noble rank.',
58:'The man shouts to Charles that he knows he is in there.',
63:'Charles recognizes the older man andasks him to come later because he is extremely busy andalmost ready to prove his theory. Uncle is familiar address,not kinship.',
67:'The man asks Charles to be quiet sometimes because the constant blasts are intolerable.',
71:'Maria politely interrupts,identifies Charles,andmentions hearing of his extensive learning.',
75:'Charles boasts that people respectfully call him Dr. Charles. Preserve this self-reported title without inventing a medical profession oruniversity credential.',
79:'Maria praises that andsays she came because she believes in him,to invite him to put his knowledge to the test around the world.',
83:'Charles is excited by the worldly scope butwonders whether one individual could possibly make it happen.',
87:'Xien says it is understandable he thinks that if he does not know whom he is addressing.',
90:'Xien introduces FI as a fine admiral already leading FO despite her youth. Preserve both live tokens andthe explicitly supported command role.',
94:'Xien begins listing her achievements,the source explicitly skips the middle,andhe says they are too many to count. Keep the comic abridgment rather than inventing accomplishments.',
98:'Charles is impressed,asks her to put his scientific knowledge to use,andfeels it is like a dream.',
101:'Xien laughs at this entertaining scholar andsuggests returning to the ship to introduce him to everyone,calling FI by the live name token.',
105:'Before that,Maria formally reintroduces herself as Admiral FI andidentifies Xien as the elderly gentleman. Preserve the playful age reference rather than kinship.',
109:'Xien protests the elderly description andinsists he is still young.',
112:'Charles says this sounds fun andintroduces his full name as Charles Jean Rochefort,with a polite greeting. Final field spelling remains subject to the scoped name reconciliation.',
},
}

def key(row):return int(row['id'].rsplit('R',1)[1]) if row['kind']=='ordinary-speech' else row['id']
def main():
    out=ROOT/'B59_B61_clean_meanings_v1.json';assert not out.exists()
    path=ROOT/'clean_source_packet.json';packet=load(path);rows=[]
    for group in packet['groups']:
        if group['block'] not in MEANINGS:continue
        meanings=MEANINGS[group['block']];assert len(meanings)==len(group['records']) and set(meanings)=={key(r) for r in group['records']}
        block=bytes.fromhex(group['clean_block_hex'])
        for source in group['records']:
            row=deepcopy(source);raw=bytes.fromhex(row['source_hex']);at=row['source_reference']['offset']
            assert block[at:at+len(raw)]==raw and not row['covered']
            row.update(source_meaning=meanings[key(row)],whole_exchange_context=CONTEXT[row['block']],
                source_meaning_reviewed_from_complete_clean_exchange=True,current_English_not_consulted=True,
                independent_draft_pending=True,contextual_comparison_pending=True,new_credit=0)
            if row['kind']=='ordinary-speech':row.update(source_selector=raw[0],source_complete_preamble_hex=block[at-5:at+1].hex())
            rows.append(row)
    assert len(rows)==89
    save(out,dict(records=rows,source_objects=89,complete_exchanges=3,source_meanings_sealed_before_independent_drafts=True,
        no_current_story_English_read=True,all_five_gates_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [path,Path(__file__)]}))
    print('Sealed89 meanings forthree full recruitment exchanges andboth Janus payment choices;no drafts orgates credited.')
if __name__=='__main__':main()
