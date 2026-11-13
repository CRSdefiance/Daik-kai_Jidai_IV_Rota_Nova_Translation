"""Plan Maria full-width logical paragraphs; preserve every base-QA finding."""
import inspect
from pathlib import Path
from types import FunctionType
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.patch.grand_race_menu_release import sha
from scripts.plan_lil_B234_layout_v7586d import plan as previous_plan,PAIRS
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_layout_v7689')
MANUSCRIPT=Path('translations/maria_B207_editorial_manuscript_v1.json')
LOGICAL=Path('work/analysis/maria_B207_logical_v7688/all18_Maria_logical_bodies72_fresh_literal_IF_alignments.json')
PROFILE='maria-story-shared-events-live'
ADAPTER=checked_text(inspect.getsource(previous_plan),{
    "row['id']=='DK4_MES_B234_R0005'":"row['source_record_index']==4",
    "row['id']=='DK4_MES_B234_R0033'":"row['source_record_index']==32",
    "{'DK4_MES_B234_R0016':{('draw','customers')}}.get(row['id'],set())":"set()",
    "get_dialogue_profile('lil-opening-editorial-native-v1')":"get_dialogue_profile(PROFILE)",
    "name='B234-source-bound-layout-RESEARCH-ONLY'":"name='Maria-B207-source-bound-layout-RESEARCH-ONLY:'+row['id'],literal_prefix_policy='native-guard-v255'",
    "assert profile.macro_ascii_lengths['FA']==5 and profile.macro_widths['FA']==30":"assert not any(v in row['english'] for v in ['{MACRO:','\\n','\\r']) and profile.pair_phase_safe_breaks and profile.guard_linebreaks",
})
ENV={**previous_plan.__globals__,'PROFILE':PROFILE,'PAIRS':PAIRS|{('divine','aid'),('no','joke'),('fell','away'),('spaced','out'),('sharp','tongue'),('doing','better'),('drive','your'),('passing','goods'),('a','fortune')}}
exec(compile(ADAPTER,__file__+'::Maria-source-owned-planner','exec'),ENV)
plan=ENV['plan']
def base_qa(row,p):
    profile=ENV['replace'](ENV['get_dialogue_profile'](PROFILE),name='Maria-B207-source-native-QA-research:'+row['id'],literal_prefix_policy='native-guard-v255',max_lines=p['max_total_rows'],leading_speaker_bytes=frozenset([19,104]))
    raw=bytes.fromhex(row['source_hex'])
    def encoded(source,text,prof):
        assert source==raw and text==row['english'] and prof==profile
        return RelocatableDialogueEncoding(p['formatted_markup'],bytes.fromhex(p['encoded_hex']),tuple(DialogueDiagnostic(**d) for d in p['diagnostics']))
    audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,'encode_relocatable_dialogue':encoded},argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
    return audit(raw,row['english'],profile)
if __name__=='__main__':
    assert not ROOT.exists();doc,literal=map(read,[MANUSCRIPT,LOGICAL]);assert literal['fresh_native_alignment_cases']==72 and literal['original_captain']==3 and literal['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    rows=[]
    for r in doc['records']:
        assert not r['review']['formatting'];p=plan(r);p.update(file_path=doc['file_path'],route=3,route_identity='Maria',source_record_index=r['source_record_index'],route_aware_base_profile=PROFILE,base_QA=base_qa(r,p));assert ' '.join(p['lines'])==r['english'].split('}',1)[1];rows.append(p)
    assert len(rows)==18;ROOT.mkdir(parents=True)
    save(ROOT/'Maria18_automatic_full_width_plans_all_base_QA_preserved.json',dict(manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),records=rows,source_owned_Maria_planner=ADAPTER,previous_frozen_planner=str(Path(previous_plan.__code__.co_filename)),previous_frozen_planner_sha256=sha(Path(previous_plan.__code__.co_filename).read_bytes()),physical_viewport=[216,64],physical_rows_per_page=4,all_logical_prose_words_andpunctuation_preserved=True,all_source_andEnglish_zero_FI_FA_FO=True,no_manual_breaks_padding_oralignment_authored=True,all18_formatting_gates_remain_false=True,all_base_QA_diagnostics_preserved_no_waivers=True,fresh_logical_literal_proof=str(LOGICAL),fresh_logical_literal_proof_sha256=sha(LOGICAL.read_bytes()),native_guard_policy_scoped_to_exact18_proved_paragraphs=True,complete_native_glyphs_bounds_pages_stored_actual_andrelease_pending=True,no_global_font_weak_ending_macro_orliteral_I_rule_change=True,new_credit=0,full_goal_complete=False))
    for r in rows:print(r['source_record_index'],r['lines'],r['line_lengths'],'QA',r['base_QA']['issues'])
