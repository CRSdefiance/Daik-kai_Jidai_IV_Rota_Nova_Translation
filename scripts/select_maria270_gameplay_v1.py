"""Select representative source-ordered utterances for distinct FE/menu/page behaviors."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B37_B50_clean_20261109')

def main():
    out=ROOT/'representative270_selection_v1.json';assert not out.exists()
    rebuilt_path=ROOT/'stored270_reconstruction_v1/reconstruction.json';rebuilt=load(rebuilt_path)
    doc=load(rebuilt['manuscript']);bykey={(r['block'],r['source_record_index']):r for r in doc['records']}
    def speeches(block,indices):return [dict(speech=bykey[(block,i)]['id']) for i in indices]
    menu38=next(r for r in doc['records'] if r['block']==38 and r['kind']=='typed-choice-label')
    menu49=next(r for r in doc['records'] if r['block']==49 and r['kind']=='typed-choice-label')
    specs=[dict(name='maria270_indian_menu_FE',
        sequence=speeches(38,[5,8,12,16,19,22,25,29])+[dict(menu=dict(block=38,source_command_offset=menu38['source_command_offset']))]+
            speeches(38,[44,52])+speeches(40,[12,16,19])+speeches(46,[4,9,13,17,21,28,31,39,42,65,68]),
        purpose='Representative native two-choice labels/default A return, B40 two-page geography explanation, unseen FE voice switching to named Xien/Clifford/Maria and original host cleanup. Display sequence only; acceptance/refusal and political alternatives are not naturally activated.'),
        dict(name='maria270_rafael_pagination',
        sequence=speeches(48,[17,21,25,57,83,142,162,166,182,194,197,210,216,227,239,254,257,261]),
        purpose='Three B48 two-page cases, Rafael source0/nameplate, FI/FA substitutions, mixed-I corrections, sparse-line retention and conditional Mediterranean reports. Source-ordered fragments are display QA, not a single earned regional chronology.'),
        dict(name='maria270_caribbean_menu',
        sequence=speeches(49,[85,96,101,110,113,120,130,136,139,143,164,167,174])+
            [dict(menu=dict(block=49,source_command_offset=menu49['source_command_offset']))]+speeches(49,[188,192,195,198,201,209,213,217]),
        purpose='Both B49 two-page cases, two reclaimed single pages, complete rhetorical question tag, typed two-choice/default A return and following named-speaker transitions. Competing betrayal accounts and refusal dialogue remain disclosed alternatives, not simulated branch outcomes.')]
    selected={a['speech'] for s in specs for a in s['sequence'] if 'speech' in a}
    plans={r['id']:r for r in load(rebuilt['plan'])['records']}
    two={r['id'] for r in plans.values() if r['expected_native_pages']==2}
    assert len(two)==6 and two<=selected
    assert sum('menu' in a for s in specs for a in s['sequence'])==2
    assert 'DK4_MES_B46_R0004' in selected
    save(out,dict(fixtures=specs,selected_speech_ids=sorted(selected),all_six_two_page_cases_selected=sorted(two),
        unvisited_body_ids=sorted(set(plans)-selected),natural_activation=False,earned_chronology=False,
        expected_menu_observation='default selection0 andnormal A return;other selection/cancel/conditional outcomes offline-only',
        original_static_controls_copied_complete=True,actual_gameplay_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [rebuilt_path,Path(__file__)]}))
    print('Selected',len(selected),'distinct utterances/two menus/all six two-page cases andFE entrance;unvisited content explicit.')

if __name__=='__main__':main()
