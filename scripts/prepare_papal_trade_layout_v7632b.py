"""Prepare a record-scoped existing native-guard policy after fresh literal proofs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/papal_trade_layout_tools_v7632b')
PROOF=Path('work/analysis/papal_trade_logical_inputs_v7633/all36_new_logical_bodies144_fresh_native_literal_IF_alignment_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(PROOF);assert d['fresh_native_alignment_cases']==144 and d['original_captains']==[0,1]
    for g in d['groups']:assert sha(Path(g['manuscript']).read_bytes())==g['manuscript_sha256']
    row=derive('scripts/plan_papal_trade_layout_v7632.py','scripts/plan_papal_trade_layout_v7632b.py',{
        'papal_trade_layout_v7632':'papal_trade_layout_v7632b',
        '''"name='B234-source-bound-layout-RESEARCH-ONLY'":"name='papal-trade-route-bound-layout-RESEARCH-ONLY:'+row['id']",''':''' "name='B234-source-bound-layout-RESEARCH-ONLY'":"name='papal-trade-route-bound-layout-RESEARCH-ONLY:'+row['id'],literal_prefix_policy='native-guard-v255'",''',
        "name='papal-trade-source-native-QA-research:'+row['id'],max_lines=":"name='papal-trade-source-native-QA-research:'+row['id'],literal_prefix_policy='native-guard-v255',max_lines=",
        "assert not ROOT.exists();groups=[]":"assert not ROOT.exists();literal=read('"+str(PROOF).replace('\\','/')+"');assert literal['fresh_native_alignment_cases']==144 and literal['original_captains']==[0,1];assert all(sha(Path(g['manuscript']).read_bytes())==g['manuscript_sha256'] for g in literal['groups']);groups=[]",
        "all_base_QA_diagnostics_preserved_no_waivers=True":"all_base_QA_diagnostics_preserved_no_waivers=True,fresh_logical_literal_proof='"+str(PROOF).replace('\\','/')+"',fresh_logical_literal_proof_sha256=sha(Path('"+str(PROOF).replace('\\','/')+"').read_bytes()),native_guard_policy_scoped_to_exact36_proved_paragraphs=True",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_route_aware_guarded_planner.json',dict(tool=row,logical_literal_proof=str(PROOF),logical_literal_proof_sha256=sha(PROOF.read_bytes()),all_native_numeric_constants_andold_default_guard_preserved=True,prior_failed_planner_preserved_not_rejection_credit=True,new_credit=0,full_goal_complete=False))
    print('Source-locked successor prepared; only exact36 freshly proved logical bodies use existing native-guard-v255 policy.')
