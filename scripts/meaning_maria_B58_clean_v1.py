"""Seal the complete London rescue exchange's clean meanings before independent English."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')
CONTEXT=('Cristina returns briefly to her hometown London and encounters her unwanted suitor Mivor. '
    'She rejects marriage again. A drowning boy panics and pulls her under;Mivor overcomes his established '
    'fear of water to rescue them. Cristina initially doubts him,then the mother confirms his courage. '
    'Her awkward thanks reignites his exuberant courtship despite her protest;Maria privately finds them well matched. '
    'Keep Cristina independent,Mivor comically effusive and the rescue frightening. The boy and rescuers are not siblings. '
    'The FE boy voices are explicitly labeled unseen speech,not narrator oractor254. The comparison signs express fear versus Cristina.')
MEANINGS={
4:'Cristina enjoys being back in London and says the air of home is best;her tone is relieved and nostalgic.',
7:'Maria says this is Cristina\'s hometown,so she should take her time and rest.',
10:'Cristina thanks Maria and says she will stroll along the port,where she has loved walking since long ago.',
14:'Maria agrees and says the rest of them will go ahead to the inn.',
17:'Cristina finds that nothing has changed and savors how pleasant it feels.',
20:'Mivor gives an extended ecstatic cry,calls this reunion a miracle and love itself,and stretches Cristina\'s name. Preserve comic excess,not a claim of mutual love.',
24:'Cristina is startled and realizes she is in trouble on seeing her unwanted suitor.',
28:'Mivor is overwhelmed with relief and says he believed his love would reach her;he repeats I and trails off emotionally.',
32:'Cristina stammers for him to stop crying because everyone is watching;she is embarrassed by the public scene.',
35:'Cristina clarifies she has not come home permanently;the ship only happened to call at London andshe will soon leave on another journey.',
38:'Mivor responds with a bewildered short question sound.',
42:'Cristina spells out her point impatiently:she did not return for him. Preserve emphasis rather than copying Japanese syllable dots.',
45:'Cristina emphatically says she is not thinking of marrying him in the slightest.',
49:'Mivor protests in a plaintive drawn-out voice and asks what she dislikes about him.',
52:'Cristina says that is not the issue:she is not thinking about marriage yet. She gently butfirmly asks him to give up.',
56:'Mivor reluctantly says he understands andwill give up,then mourns that his love is over;his awkward politeness is comic.',
60:'Cristina sighs with relief,thinking she can finally stop being pursued.',
64:'Cristina reacts to a new disturbance with startled question/exclamation punctuation.',
68:'Mivor sighs,then notices something andreacts in surprise.',
72:'A woman cries out in alarm for her little boy.',
76:'Cristina asks what happened.',
81:'The woman says her boy has fallen into the sea andbegs someone to save him. The source explicitly establishes her maternal relationship.',
85:'Cristina tells the woman to wait andsays she will save the boy.',
89:'Cristina encourages the drowning boy to hang on andsays she is coming to save him now.',
93:'Mivor cries out Cristina\'s name in alarm.',
98:'Cristina reassures the boy that she has reached him andhe will be all right. Her self-reference as big sister is a familiar reassuring address,not kinship.',
101:'The boy cries out twice that he is scared. Preserve the source\'s explicit boy voice label in this FE speech.',
104:'Cristina repeats gently that everything is all right.',
108:'Cristina asks the boy not to cling around her neck;she is struggling to breathe. Big sister again refers to herself,not a real sibling.',
111:'The unseen boy repeats that he is scared,with his explicit FE voice label.',
114:'Cristina realizes that at this rate she too will drown together with the boy.',
117:'The unseen boy wails again that he is scared;retain the explicit boy voice label andpanic.',
120:'Cristina is losing her ability to stay afloat andgaspingly fears she will drown.',
124:'The woman screams for someone to help.',
130:'Mivor desperately asks whether anyone is there to help.',
134:'Mivor sees Cristina in danger,butthe sea/water terrifies him;his speech breaks off in conflict.',
137:'Mivor repeatedly thinks that the sea is frightening. The greater-than comparison shows fear of the sea currently outweighing Cristina in his internal struggle.',
140:'Mivor hesitates with repeated but,then gives a long forceful yell as he resolves to act.',
143:'The repeated fear-of-sea thought returns,butthe less-than comparison now shows Cristina outweighing his fear. Preserve the reversal as a matched comic pair.',
146:'Mivor repeats Cristina\'s name three times,building resolve andurgency.',
149:'Mivor gives another very loud stretched cry of Cristina\'s name.',
153:'Mivor announces his own name andthat he is going in,with a comically stretched heroic cry. Do not invent a military rank ornew ability.',
157:'Mivor calls to Cristina that he is coming to her now. The source has a leading staged break andan exaggerated polite speech ending;retain intention,not automatic blank first row.',
163:'Cristina coughs andcomes round,recognizes Mivor,andasks where she is andwhat happened to her.',
167:'Mivor ecstatically calls her his beloved Cristina andsays she has regained consciousness;the endearing address is his feeling,not narrator-confirmed romance.',
170:'Cristina recalls drowning,then urgently asks whether the boy is safe.',
174:'Mivor says the boy is safe andthat the woman thanked them/him;do not invent an additional rescuer.',
178:'Cristina infers someone rescued her,says she must thank that person,andasks where her lifesaver is.',
182:'Mivor hesitantly tries to explain that the lifesaver is right here.',
185:'Cristina gives a short surprised question.',
189:'Mivor awkwardly admits that he himself saved her.',
192:'Cristina is stunned because he is afraid of water;her unfinished line leaves the apparent contradiction hanging.',
196:'Mivor acknowledges that fear,then trails off describing what happened in his mind when he thought he had to save Cristina. Do not add a conscious swimming lesson orlasting cure.',
200:'Mivor says that somehow he ended up swimming andthat he cannot believe it himself.',
203:'Cristina asks whether he really did it andsays she cannot believe it.',
206:'Cristina says she must get to the inn;she is unsettled andchanges the subject.',
210:'Mivor asks whether she is all right.',
214:'Cristina says she is fine andcan go alone.',
218:'Mivor politely takes his leave.',
223:'The boy recognizes Cristina excitedly,using familiar big sister address without a sibling relationship.',
227:'Cristina asks the boy whether he is all right.',
231:'The boy says he is fine andthanks her,then asks where the older boy/man who saved him is. Big brother is familiar address,not family.',
235:'The woman sincerely thanks Cristina andasks where the man who was with her is.',
238:'Cristina asks whether Mivor truly jumped into the sea.',
242:'The woman confirms he jumped in while giving a strange shriek;preserve the slightly comic witness description.',
245:'The woman infers that he must love Cristina very much. Keep this as her inference rather than Cristina\'s own admission orconfirmed engagement.',
248:'Cristina quietly realizes Mivor was telling the truth.',
252:'The woman offers a token of thanks andasks Cristina to accept it;the spoken line does not identify the gift.',
257:'Cristina is caught off guard andthanks her.',
261:'The woman takes her leave with another sincere thank-you.',
264:'The boy says goodbye to Cristina with the same familiar older-girl address,not Sister as a family title.',
270:'Cristina has finished recounting the incident to Maria andsays that is what happened.',
274:'Maria is surprised Mivor did that andgives him impressed credit.',
277:'Cristina says she still cannot believe it.',
281:'Maria chuckles andsays that very man is coming over now.',
286:'Cristina notices andaddresses Mivor hesitantly.',
290:'Mivor responds by saying Cristina\'s name.',
294:'Cristina admits she did not properly thank him earlier,thanks him now,andawkwardly says he looked cool/was impressive. Preserve her hesitant compliment without inventing a romantic acceptance.',
298:'Mivor is hugely surprised by her compliment,with escalating repeated cries.',
302:'Mivor asks whether she truly thinks he looked cool andsays he is extremely happy;his excited polite endings are comic rather than a foreign accent.',
306:'Cristina warns that he is getting the wrong idea.',
310:'Mivor says he does not care about that andis simply overjoyed,then stretches her name again.',
314:'Cristina snaps that he is loud andannoying andurges the group to set sail soon to get away from him.',
318:'Mivor calls after her that he will always wait for her. This is his declaration,not a new mutual promise.',
321:'Maria privately comments that those two are rather well matched. Keep this as her amused observation,not a guaranteed relationship outcome.',
}

def main():
    out=ROOT/'B58_clean_meanings_v1.json';assert not out.exists()
    packet_path=ROOT/'clean_source_packet.json';packet=load(packet_path)
    groups=[g for g in packet['groups'] if g['block']==58];assert len(groups)==1
    rows=deepcopy(groups[0]['records']);assert len(rows)==len(MEANINGS)==85
    assert set(MEANINGS)=={int(r['id'].rsplit('R',1)[1]) for r in rows}
    block=bytes.fromhex(groups[0]['clean_block_hex'])
    for row in rows:
        index=int(row['id'].rsplit('R',1)[1]);raw=bytes.fromhex(row['source_hex']);at=row['source_reference']['offset']
        assert block[at:at+len(raw)]==raw and not row['covered']
        row.update(source_meaning=MEANINGS[index],whole_exchange_context=CONTEXT,source_selector=raw[0],
            source_complete_preamble_hex=block[at-5:at+1].hex(),
            source_meaning_reviewed_from_complete_clean_exchange=True,current_English_not_consulted=True,
            independent_draft_pending=True,contextual_comparison_pending=True,new_credit=0)
    save(out,dict(records=rows,source_objects=85,complete_exchanges=1,source_meanings_sealed_before_independent_drafts=True,
        no_current_story_English_read=True,all_five_gates_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [packet_path,Path(__file__)]}))
    print('Sealed85 clean meanings forcomplete London rescue exchange;no drafts,current comparison orgates credited.')
if __name__=='__main__':main()
