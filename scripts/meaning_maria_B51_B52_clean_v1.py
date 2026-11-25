"""Seal meanings for two whole clean exchanges before current-English comparison."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B51_B57_clean_20261109')
MEANINGS={
    51:{
        6:'Richard is shocked that his plan has become known this soon;his opening is hesitant/stammered.',
        9:'Xien says that is where Richard is naive and that he never trusted him from the outset.',
        13:'Hearing Richard would remain in Hangzhou gave Xien a bad feeling. He says sending a messenger home ahead of time was the right precaution;do not invent the messenger recipient or nationality.',
        16:'Richard gives a frustrated,wordless growl.',
        20:'Maria recognizes that Richard deliberately played a man who was incapable and all talk to make her lower her guard. She calls the stratagem clever.',
        23:'Richard says they were so close to all seas west of India becoming Clifford\'s domain. Preserve the unrealized almost and the geographic limit;the honorific expresses deference without proving a noble rank.',
        27:'Maria calls this foolish and asks whether Richard knows what ultimately happens to traitors. This is her hostile rhetorical warning,not a narrated outcome.',
        31:'Richard claims the world\'s seas were completely divided until just a hundred years ago and that Western Europeans linked them through their great voyages. Keep the colonial boast as his claim,not narrator-approved history.',
        35:'Richard asserts the resulting rights/interests naturally belong to them and stammers that the others have no right to take them away. Do not turn the asserted entitlement into narrator fact.',
        39:'Richard pauses with a single ellipsis;preserve the separate silent beat.',
        44:'Richard gives two violent cries/gasps of pain. The text does not identify an attacker,weapon ormedical mechanism.',
        48:'Xien reacts with startled question/exclamation punctuation.',
        52:'Maria reacts with shocked exclamation punctuation.',
        56:'Richard cries out Clifford\'s name with a stammer and deferential honorific. Preserve distress/deference without inventing Lord,Sir oranother rank.',
        61:'Maria falls silent with an extended ellipsis after Richard\'s cry.',
        65:'Xien also falls silent;retain this distinct responding beat.',
        69:'Maria wonders whether Richard seriously believed such a plan would succeed.',
        72:'Xien says failure did not seem to enter Richard\'s mind. Preserve seemed,not certain access to his thoughts.',
        75:'Maria disagrees:Clifford certainly knew the plan was reckless,but she suspects Richard also realized that. Preserve her inference about Richard.',
        78:'Xien asks in surprise whether Richard knew too.',
        82:'Maria thinks Richard knew yet blindly believed in Clifford. He seemed swept up in his own devotion/self-image,staking his life on it. This is her assessment,not proof of literal intoxication.',
        85:'Xien asks whether Clifford had been exploiting Richard,with that character/devotion,from the start.',
        88:'Maria pauses silently as the implication develops.',
        101:'Xien begins an emphatic then-that-means inference,leaving Maria to state the implication next.',
        105:'Maria concludes Richard acted knowing he was an expendable pawn. Now that she has turned back east,Clifford will make a new move. Keep the inference,expendability and eastward diversion.',
        109:'Xien gives a brief sound of realization and agrees with Maria.',
    },
    52:{
        11:'A casual town speaker greets FA neutrally,explains that a Ming official is looking for FA,and suggests returning to Hangzhou. Preserve the FA runtime surname,not a hardcoded name or invented courtesy title.',
        17:'The speaker gives an excited cry announcing that FA has returned,with respectful address in Japanese. Preserve acclaim and the FA substitution without inventing rank or kinship.',
    },
}
def main():
    out=ROOT/'B51_B52_clean_meanings_v1.json';assert not out.exists()
    packet_path=ROOT/'clean_source_packet.json';packet=load(packet_path);rows=[]
    for group in packet['groups']:
        block=group['block']
        if block not in MEANINGS:continue
        assert {int(r['id'].split('_R')[1]) for r in group['records']}==set(MEANINGS[block])
        for original in group['records']:
            index=int(original['id'].split('_R')[1]);row=dict(original)
            row.update(source_meaning=MEANINGS[block][index],source_meaning_reviewed_from_complete_clean_exchange=True,
                current_English_not_consulted=True,independent_draft_pending=True,contextual_comparison_pending=True,
                source_selector_hex=original['source_hex'][:2],new_credit=0)
            rows.append(row)
    assert len(rows)==28
    save(out,dict(records=rows,source_objects=28,complete_exchanges=[51,52],
        context_by_block={'51':'Richard\'s exposed plan and Western-entitlement defense;cries/shock andsilence lead into Maria\'s inference that his willing expendability diverted her east. No attacker,weapon ormedical cause is invented.',
            '52':'Related return-to-Hangzhou town messages. Conditional alternatives are preserved as source text;they are not claimed as one naturally earned consecutive exchange.'},
        source_only_not_current_English=True,clean_meanings_sealed_before_independent_draft_artifact=True,
        all_five_review_gates_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [packet_path,Path(__file__)]}))
    print('Sealed28 clean meanings forcomplete B51/B52 exchanges;no current English ornew credit.')
if __name__=='__main__':main()
