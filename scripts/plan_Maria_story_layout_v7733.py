"""Plan full-width guarded paragraphs with measured Maria macros; no formatting approval."""
import inspect
from types import FunctionType
from pathlib import Path
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.patch.grand_race_menu_release import sha
from scripts.plan_lil_B234_layout_v7586d import plan as old_plan,PAIRS
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_layout_v7733')
MANUSCRIPT=Path('translations/maria_B34_B108_B35_editorial_manuscript_v1.json')
LOGICAL=Path('work/analysis/maria_story_logical_v7732/67_logical_paragraphs268_original_native_macro_literal_alignments.json')
SELECTORS=frozenset({1,3,9,10,26,74,116,155})
PROFILE='maria-story-shared-events-live'
def display(text):
    return text.replace('{MACRO:FI}','Maria').replace('{MACRO:FA}','Li').replace('{MACRO:FO}','Li Clan').replace('…','XX')
def get_profile():
    original=old_plan.__globals__['get_dialogue_profile'](PROFILE)
    return old_plan.__globals__['replace'](original,macro_widths={'FI':30,'FA':12,'FO':42,'I':12},macro_ascii_lengths={'FI':5,'FA':2,'FO':7})
ADAPTER=checked_text(inspect.getsource(old_plan),{
    "row['source_selector'] in [19,104]":"row['source_selector'] in SELECTORS",
    "c=='…' and row['id']=='DK4_MES_B234_R0005' and body=='………' and bytes.fromhex(row['source_hex'])==bytes.fromhex('68816381638163')":"c=='…' and bytes.fromhex('8163') in bytes.fromhex(row['source_hex'])[1:]",
    "row['id']=='DK4_MES_B234_R0033'":"False",
    "{'DK4_MES_B234_R0016':{('draw','customers')}}.get(row['id'],set())":"set()",
    "get_dialogue_profile('lil-opening-editorial-native-v1')":"get_profile()",
    "name='B234-source-bound-layout-RESEARCH-ONLY'":"name='Maria-34-108-35-RESEARCH-ONLY:'+row['id'],literal_prefix_policy='native-guard-v255'",
    "leading_speaker_bytes=frozenset([19,104])":"leading_speaker_bytes=SELECTORS",
    "assert profile.macro_ascii_lengths['FA']==5 and profile.macro_widths['FA']==30":"assert profile.macro_ascii_lengths=={'FI':5,'FA':2,'FO':7} and profile.macro_widths['FA']==12",
    "No source/prose-preserving B234 plan:":"No source/prose-preserving Maria story plan:",
    "all_words_punctuation_and_zero_macros_unchanged":"all_words_punctuation_and_source_macros_unchanged",
})
ENV={**old_plan.__globals__,'SELECTORS':SELECTORS,'PROFILE':PROFILE,'display':display,'get_profile':get_profile,
    'PAIRS':PAIRS|{('north','sea'),('east','asia'),('southeast','asia'),('argot','company'),('swedish','navy'),('local','people'),
        ('sense','of'),('of','justice'),('running','away'),('caught','up'),('weighing','on'),('my','conscience'),('find','me'),
        ('came','to'),('to','light'),('both','sides'),('can','turn'),('turn','to'),('looking','into'),('around','batavia')}}
exec(compile(ADAPTER,__file__+'::source-locked-measured-Maria-planner','exec'),ENV)
plan=ENV['plan']
def base_qa(row,p):
    profile=ENV['replace'](get_profile(),name='Maria-34-108-35-native-QA:'+row['id'],literal_prefix_policy='native-guard-v255',
        max_lines=p['max_total_rows'],leading_speaker_bytes=SELECTORS)
    raw=bytes.fromhex(row['source_hex'])
    def encoded(source,text,prof):
        assert source==raw and text==row['english'] and prof==profile
        return RelocatableDialogueEncoding(p['formatted_markup'],bytes.fromhex(p['encoded_hex']),tuple(DialogueDiagnostic(**v) for v in p['diagnostics']))
    audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,'encode_relocatable_dialogue':encoded},argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
    return audit(raw,row['english'],profile)
if __name__=='__main__':
    assert not ROOT.exists();doc,logical=map(read,[MANUSCRIPT,LOGICAL])
    assert logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and logical['fresh_native_alignment_cases']==268
    rows=[];failures=[]
    for row in doc['records']:
        try:
            assert not row['review']['formatting'];planning=dict(row)
            body=row['english']
            for token in ['FI','FA','FO']:body=body.replace(token,'{MACRO:'+token+'}')
            planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body
            p=plan(planning);assert ' '.join(p['lines'])==body
            p.update(file_path=doc['file_path'],block=row['block'],source_record_index=row['source_record_index'],source_selector=row['source_selector'],
                logical_English=row['english'],planning_record=planning,base_QA=base_qa(planning,p))
            rows.append(p)
        except (ValueError,AssertionError) as exc:failures.append(dict(id=row['id'],error_type=type(exc).__name__,error=str(exc)))
    ROOT.mkdir(parents=True);save(ROOT/'67_automatic_full_width_plans_all_base_QA_preserved.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),logical=str(LOGICAL),logical_sha256=sha(LOGICAL.read_bytes()),
        records=rows,failures=failures,source_owned_plan_adapter=ADAPTER,source_owned_measured_macro_display=inspect.getsource(display),
        source_owned_measured_profile=inspect.getsource(get_profile),source_word_boundary_pairs=sorted(ENV['PAIRS']),
        physical_viewport=[216,64],physical_native_rows_per_page=4,source_macros_FI5_FA2_FO7=True,
        no_manual_break_padding_alignment_orprose_abbreviation_authored=True,full_width_pair_phase_andnative_linebreak_guards=True,
        all_original_QA_issues_preserved_no_waivers=True,no_global_profile_guard_font_orweak_boundary_change=True,
        maximum_two_native_pages_only_when_four_rows_cannot_hold_complete_prose=True,
        compiled_byte_native_font_bounds_pagination_controls_stored_actual_andrelease_checks_pending=True,
        all67_formatting_gates_remain_false=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,LOGICAL,Path(old_plan.__code__.co_filename),Path(__file__)]},full_goal_complete=False))
    print('PLANS',len(rows),'FAILURES',failures,'PAGES',sum(r['expected_native_pages'] for r in rows))
    print('QA',[(r['id'],r['base_QA']['issues']) for r in rows if r['base_QA']['issues']])
    if failures:raise SystemExit(1)
