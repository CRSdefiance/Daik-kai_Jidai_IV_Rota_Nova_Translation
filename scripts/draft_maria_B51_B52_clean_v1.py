"""Seal independent logical prose after the clean meanings, before current English."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

DRAFTS={
    51:{
        6:"I-impossible... You found out about my plan already?!",
        9:"That's where you went wrong. I never trusted you to begin with.",
        13:"When I heard you were staying in Hangzhou, I had a bad feeling. I was right to send a messenger home ahead of time.",
        16:"Grr...",
        20:"So you played the man who was all talk and no action, just to make me lower my guard. Clever.",
        23:"Just a little more, and every sea west of India would have belonged to Clifford!",
        27:"How foolish... You know what happens to traitors, don't you?",
        31:"Until just a hundred years ago, the world's seas were completely cut off from one another. We Europeans linked them through our great voyages.",
        35:"Of course those rights belong to us! Y-you have no right to take them away!",
        39:"...",44:"Aagh! Guh...!!",48:"!?",52:"!!",56:"C-Clifford...!!",61:"...",65:"...",
        69:"Did Richard really think a plan like that could work?",
        72:"Failure never seemed to cross his mind.",
        75:"I don't think so. Clifford certainly knew how reckless it was, but I suspect Richard did, too.",
        78:"Richard, too?",
        82:"Yes. He knew, but he believed blindly in Clifford anyway. He seemed swept up in his own devotion... enough to stake his life on it.",
        85:"So Clifford was using him from the start...?",
        88:"...",101:"...Then that means...!",
        105:"Richard acted knowing he was an expendable pawn... Now that I've turned back east, Clifford will make his next move!",
        109:"Ah! You're right!",
    },
    52:{11:"Hey, {MACRO:FA}. A Ming official's looking for you. You should head back to Hangzhou.",
        17:"Ah! {MACRO:FA} is back!"},
}

def main():
    out=ROOT/'B51_B52_independent_drafts_v1.json';assert not out.exists()
    meaning_path=ROOT/'B51_B52_clean_meanings_v1.json';meanings=load(meaning_path)
    assert meanings['source_only_not_current_English'] and meanings['source_objects']==28
    rows=[]
    for original in meanings['records']:
        row=dict(original);index=int(row['id'].split('_R')[1]);block=row['block']
        actor=int(row['source_selector_hex'],16)
        speaker={3:'Maria',10:'Xien',74:'Richard'}.get(actor,f'source actor {actor}')
        row.update(english=DRAFTS[block][index],speaker=speaker,
            context=meanings['context_by_block'][str(block)],
            independent_draft_pending=False,independent_clean_first_draft=True,
            current_English_not_consulted=True,current_comparison_pending=True,
            localization_note=('Preserve the whole exchange and individual reaction beats. '
                'Natural logical prose; no invented rank, kinship, attacker or outcome. '
                'Colonial entitlement and motives remain the speakers\' claims/inferences.' if block==51 else
                'Casual greeting or excited acclaim; keep the runtime surname and conditional alternatives without inventing a title.'),
            review={gate:False for gate in ['source','context','localization','naturalness','formatting']},
            natural_dialogue_policy='natural-dialogue-v2',target_locale='en-US',new_credit=0)
        assert '\n' not in row['english'] and '{LB' not in row['english']
        assert row['source_hex'].startswith(row['source_selector_hex'])
        rows.append(row)
    assert len(rows)==sum(map(len,DRAFTS.values()))==28
    save(out,dict(records=rows,source_objects=28,complete_exchanges=[51,52],
        complete_exchange_clean_meanings_precede_independent_drafts=True,
        current_English_not_consulted=True,all_five_review_gates_pending=True,
        new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [meaning_path,ROOT/'clean_source_packet.json',Path(__file__)]}))
    print('Sealed28 independent logical drafts after clean meanings; current comparison and all gates pending.')
if __name__=='__main__':main()
