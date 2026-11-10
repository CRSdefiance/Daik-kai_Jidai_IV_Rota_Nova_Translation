"""Automatic full-width Lil plans; surname-only prose revisit, all original QA retained."""
import inspect
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Rafael_B49_layout_v8090c as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Gerhard_layout_v8205')
MANUSCRIPT=Path('translations/gerhard_surname_consistency_manuscript_v1.json')
LOGICAL=Path('work/analysis/Gerhard_logical_v8204/5_logical_paragraphs20_original_native_alignments.json')

def get_profile(row):
    assert row['kind']=='progressive' and row['source_selector'] in [1,9,16]
    p=get_dialogue_profile('lil-story-deep-route-live')
    assert p.window_width_px==216 and p.default_ascii_width==6 and p.default_multibyte_width==12 and p.max_lines==4
    assert p.macro_ascii_lengths==dict(FI=3,FA=5,FO=9) and p.macro_widths==dict(FI=18,FA=30,FO=54,I=12)
    assert p.guard_linebreaks and p.pair_phase_safe_breaks
    return replace(p,leading_speaker_bytes=frozenset({1,9,16}))

def display(text):
    return text.replace('{MACRO:FI}','Lil').replace('{MACRO:FA}','Argot').replace('{MACRO:FO}','Argot Co.')

ADAPTER=checked_text(previous.ADAPTER,{
    "row['source_selector'] in [0,2,4,5,6,8,9]":"row['source_selector'] in [1,9,16]",
    'Rafael-B49-RESEARCH-ONLY':'Gerhard-surname-Lil-RESEARCH-ONLY',
    'No source/prose-preserving Rafael B49 plan:':'No source/prose-preserving Gerhard surname plan:',
    "profile.macro_ascii_lengths=={'FI':6,'FA':6,'FO':10} and profile.macro_widths['FA']==36":"profile.macro_ascii_lengths=={'FI':3,'FA':5,'FO':9} and profile.macro_widths['FA']==30",
})
PAIRS=previous.PAIRS|{('gerhard','adernkatz'),('admiral','adernkatz'),("it's",'been'),('thank','you'),('keep','teaching')}
COHERENT_PAIRS=previous.COHERENT_PAIRS|{('gerhard','adernkatz'),('admiral','adernkatz'),("it's",'been'),('thank','you'),('keep','teaching')}
ENV={**previous.ENV,'get_profile':get_profile,'display':display,'PAIRS':PAIRS,'COHERENT_PAIRS':COHERENT_PAIRS,'BOUND_ZERO_SOURCE_BODIES':frozenset()}
exec(compile(ADAPTER,__file__+'::Lil-exact-three-source-selectors','exec'),ENV);plan=ENV['plan']
qa_adapter=checked_text(previous.qa_adapter,{'Rafael-B49-native-QA':'Gerhard-surname-Lil-native-QA'})
qenv={**previous.base_qa.__globals__,'get_profile':get_profile}
exec(compile(qa_adapter,__file__+'::unchanged-original-QA','exec'),qenv);base_qa=qenv['base_qa']

if __name__=='__main__':
    assert not ROOT.exists();doc,logical=map(read,[MANUSCRIPT,LOGICAL])
    assert logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and logical['total_bound_alignment_cases']==20
    rows=[];failures=[]
    for row in doc['records']:
        try:
            assert not row['review']['formatting'];planning=dict(row);body=row['english']
            assert not any(t in body for t in ['{LB','{ALIGN','{PAD','\n','\r'])
            assert body.count('{MACRO:FI}')==int(row['block']==74 and row['source_record_index']==185)
            planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body
            p=plan(planning);assert ' '.join(p['lines'])==body
            encoded=bytes.fromhex(p['encoded_hex']);assert encoded[0]==row['source_selector'] and b'\0' not in encoded[1:]
            p.update(file_path=row['file_path'],block=row['block'],source_record_index=row['source_record_index'],source_selector=row['source_selector'],kind=row['kind'],
                logical_English=body,planning_record=planning,base_QA=base_qa(planning,p),original_consumer_usable_text_width_px=216,original_consumer_bitmap_width_px=216)
            rows.append(p)
        except (ValueError,AssertionError) as exc:failures.append(dict(id=row['id'],error_type=type(exc).__name__,error=str(exc)))
    ROOT.mkdir(parents=True)
    save(ROOT/'5_automatic_Lil_plans_full_native_width.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),logical=str(LOGICAL),logical_sha256=sha(LOGICAL.read_bytes()),
        records=rows,failures=failures,source_owned_plan_adapter=ADAPTER,source_owned_QA_adapter=qa_adapter,
        source_owned_measured_profile=inspect.getsource(get_profile),source_owned_measured_display=inspect.getsource(display),
        source_word_boundary_pairs=sorted(PAIRS),source_coherent_phrase_pairs=sorted(COHERENT_PAIRS),
        original_body_encoder_NUL_rejection_preserved_without_exception=True,progressive_viewport=[216,64],original_physical_rows_per_page=4,
        measured_default_macro_lengths=dict(FI=3,FA=5,FO=9),source_macro_totals=dict(FI=1,FA=0,FO=0),
        source_selectors_exactly_01_09_10_no_FE_or00_exception=True,no_global_font_profile_guard_orweak_rule_change=True,
        no_manual_break_padding_alignment_orprose_abbreviation_authored=True,all_original_QA_issues_preserved_without_removal=True,
        ordinary_boundary_warning_review_pending=True,all5_formatting_gates_remain_false=True,
        native_fonts_names_stored_controls_actual_andregistered_release_pending=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,LOGICAL,Path(previous.__file__),Path(__file__)]},full_goal_complete=False))
    for r in rows:print(r['id'],r['lines'],'pages',r['expected_native_pages'],'QA',r['base_QA']['issues'])
    print('PLANS',len(rows),'FAILURES',failures)
    if failures:raise SystemExit(1)
