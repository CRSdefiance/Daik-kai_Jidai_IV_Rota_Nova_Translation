"""Plan complete SC0/SC1 paragraphs using each route's guarded native profile."""
import inspect
from pathlib import Path
from types import FunctionType
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.patch.grand_race_menu_release import sha
from scripts.plan_lil_B234_layout_v7586d import plan as previous_plan, PAIRS
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.draft_papal_trade_prose_v7631 import MANUSCRIPTS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/papal_trade_layout_v7632b')
ROUTE_PROFILE={0:'raphael-story-live',1:'hodram-story-live'}
ADAPTER=checked_text(inspect.getsource(previous_plan),{
    "row['id']=='DK4_MES_B234_R0005'":"row['source_record_index']==5",
    "row['id']=='DK4_MES_B234_R0033'":"row['source_record_index']==33",
    "{'DK4_MES_B234_R0016':{('draw','customers')}}.get(row['id'],set())":"({('draw','customers')} if row['source_record_index']==16 else set())",
    "get_dialogue_profile('lil-opening-editorial-native-v1')":"get_dialogue_profile(ROUTE_PROFILE[row['route']])",
     "name='B234-source-bound-layout-RESEARCH-ONLY'":"name='papal-trade-route-bound-layout-RESEARCH-ONLY:'+row['id'],literal_prefix_policy='native-guard-v255'",
    "assert profile.macro_ascii_lengths['FA']==5 and profile.macro_widths['FA']==30":"assert not any(v in row['english'] for v in ['{MACRO:','\\n','\\r']) and profile.pair_phase_safe_breaks and profile.guard_linebreaks",
})
ENV={**previous_plan.__globals__,'ROUTE_PROFILE':ROUTE_PROFILE,'PAIRS':PAIRS|{('divine','aid'),('no','joke'),('fell','away'),('papal','authority')}}
exec(compile(ADAPTER,__file__+'::route-aware-source-owned-planner','exec'),ENV)
plan=ENV['plan']

def base_qa(row,p):
    profile=ENV['replace'](ENV['get_dialogue_profile'](ROUTE_PROFILE[row['route']]),name='papal-trade-source-native-QA-research:'+row['id'],literal_prefix_policy='native-guard-v255',max_lines=p['max_total_rows'],leading_speaker_bytes=frozenset([19,104]))
    raw=bytes.fromhex(row['source_hex'])
    def encoded(source,text,prof):
        assert source==raw and text==row['english'] and prof==profile
        return RelocatableDialogueEncoding(p['formatted_markup'],bytes.fromhex(p['encoded_hex']),tuple(DialogueDiagnostic(**d) for d in p['diagnostics']))
    audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,'encode_relocatable_dialogue':encoded},argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
    return audit(raw,row['english'],profile)

if __name__=='__main__':
    assert not ROOT.exists();literal=read('work/analysis/papal_trade_logical_inputs_v7633/all36_new_logical_bodies144_fresh_native_literal_IF_alignment_cases.json');assert literal['fresh_native_alignment_cases']==144 and literal['original_captains']==[0,1];assert all(sha(Path(g['manuscript']).read_bytes())==g['manuscript_sha256'] for g in literal['groups']);groups=[]
    for route,path in MANUSCRIPTS.items():
        doc=read(path);rows=[]
        assert len(doc['records'])==18 and all(r['route']==route and not r['review']['formatting'] for r in doc['records'])
        for r in doc['records']:
            p=plan(r);p.update(file_path=doc['file_path'],route=route,route_identity=doc['route_identity'],source_record_index=r['source_record_index'],route_aware_base_profile=ROUTE_PROFILE[route],base_QA=base_qa(r,p))
            assert ' '.join(p['lines'])==r['english'].split('}',1)[1]
            rows.append(p)
        groups.append(dict(route=route,route_identity=doc['route_identity'],manuscript=str(path),manuscript_sha256=sha(path.read_bytes()),records=rows))
    for a,b in zip(groups[0]['records'],groups[1]['records'],strict=True):
        assert a['English']==b['English'] and a['encoded_hex']==b['encoded_hex'] and a['lines']==b['lines']
    ROOT.mkdir(parents=True)
    save(ROOT/'two_routes36_automatic_full_width_plans_all_base_QA_preserved.json',dict(groups=groups,source_owned_route_aware_planner=ADAPTER,previous_frozen_planner=str(Path(previous_plan.__code__.co_filename)),previous_frozen_planner_sha256=sha(Path(previous_plan.__code__.co_filename).read_bytes()),physical_viewport=[216,64],physical_rows_per_page=4,all_logical_prose_words_andpunctuation_preserved=True,all_source_andEnglish_zero_FI_FA_FO=True,no_manual_breaks_padding_oralignment_authored=True,all36_formatting_gates_remain_false=True,all_base_QA_diagnostics_preserved_no_waivers=True,fresh_logical_literal_proof='work/analysis/papal_trade_logical_inputs_v7633/all36_new_logical_bodies144_fresh_native_literal_IF_alignment_cases.json',fresh_logical_literal_proof_sha256=sha(Path('work/analysis/papal_trade_logical_inputs_v7633/all36_new_logical_bodies144_fresh_native_literal_IF_alignment_cases.json').read_bytes()),native_guard_policy_scoped_to_exact36_proved_paragraphs=True,complete_native_glyphs_bounds_pages_stored_actual_andrelease_pending=True,no_global_font_weak_ending_macro_orliteral_I_rule_change=True,evidence={str(p):sha(p.read_bytes()) for p in [*MANUSCRIPTS.values(),Path(__file__)]},new_credit=0,full_goal_complete=False))
    for g in groups:
        print(g['route_identity'])
        for r in g['records']: print(r['source_record_index'],r['lines'],r['line_lengths'],'QA',r['base_QA']['issues'])
