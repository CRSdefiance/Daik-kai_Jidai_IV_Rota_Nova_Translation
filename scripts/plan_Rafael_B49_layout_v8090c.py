"""Automatic full-width B49 wrapping; exact source00/02/09 states,no manual staging."""
import inspect
from dataclasses import replace
from pathlib import Path
from scripts import plan_Rafael_B48_layout_v8035d as previous
from scripts.plan_Rafael_B45_layout_v7881b import get_profile as base_profile
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Rafael_B49_layout_v8090c')
MANUSCRIPT=Path('translations/rafael_B49_editorial_manuscript_v1.json')
LOGICAL=Path('work/analysis/Rafael_B49_logical_v8089/61_logical_paragraphs244_original_native_alignments_no_FE.json')
CURRENT=Path('work/analysis/Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json')
bound=read(CURRENT)
BOUND_ZERO_SOURCE_BODIES=frozenset(bytes.fromhex(r['source_hex']) for r in bound['records'] if r['source_selector']==0)
assert sum(r['source_selector']==0 for r in bound['records'])==16 and len(BOUND_ZERO_SOURCE_BODIES)==15

def get_profile(row):
    assert row['kind']=='progressive' and row['source_selector'] in [0,2,4,5,6,8,9]
    p=base_profile(row)
    assert p.window_width_px==216 and p.default_ascii_width==6 and p.default_multibyte_width==12
    assert p.macro_ascii_lengths==dict(FI=6,FA=6,FO=10)
    return replace(p,leading_speaker_bytes=frozenset({0,2,4,5,6,8,9}))

ADAPTER=checked_text(previous.ADAPTER,{
    "((row['kind']=='progressive' and row['source_selector'] in [0,4,5,6,7,8,13,75,113]) or (row['kind']=='system-FE' and row['source_selector']==254))":"(row['kind']=='progressive' and row['source_selector'] in [0,2,4,5,6,8,9])",
    "all(32<=ord(c)<127 or c=='…' and row['id']==ELLIPSIS_ID and body=='…' and row['source_hex']==ELLIPSIS_SOURCE for c in body)":"all(32<=ord(c)<127 for c in body)",
    'Rafael-B48-RESEARCH-ONLY':'Rafael-B49-RESEARCH-ONLY','No source/prose-preserving Rafael B48 plan:':'No source/prose-preserving Rafael B49 plan:',
})
PAIRS=previous.PAIRS|{
    ('trade','house'),('north','sea'),('argot','company'),('hanseatic','league'),('martin','speyer'),
    ('portuguese','territory'),('new','world'),('far','east'),('for','now'),('i','bet'),('go','along'),("don't",'you'),
}
COHERENT_PAIRS={
    ('who','gave'),('navy','guy'),('fight','out'),('beyond','this'),('west','to'),('head','west'),('look','beyond'),('this','sea'),
    ('north','sea'),('new','world'),('far','east'),('argot','company'),
    ('martin','speyer'),('hanseatic','league'),('trade','house'),("don't",'you'),("aren't",'you'),
}
ADAPTER=checked_text(ADAPTER,{
    'return (0,0,0,0,0,0),()':'return (0,0,0,0,0,0,0),()',
    'cost[1]+int(not final and length<18)':'cost[1]+int(not final and length<18 and not terminal)',
    'cost[3]+1,cost[4]+weak,cost[5]+':'cost[3]+1,cost[4]+int(not final and pair in COHERENT_PAIRS),cost[5]+weak,cost[6]+',
})
ENV={**previous.ENV,'BOUND_ZERO_SOURCE_BODIES':BOUND_ZERO_SOURCE_BODIES,'get_profile':get_profile,'PAIRS':PAIRS,'COHERENT_PAIRS':COHERENT_PAIRS}
ENV.pop('ELLIPSIS_ID');ENV.pop('ELLIPSIS_SOURCE')
exec(compile(ADAPTER,__file__+'::exact-source-B49-automatic-plan','exec'),ENV);plan=ENV['plan']
qa_adapter=checked_text(previous.qa_adapter,{'Rafael-B48-native-QA':'Rafael-B49-native-QA'})
qenv={**previous.base_qa.__globals__,'get_profile':get_profile}
exec(compile(qa_adapter,__file__+'::unchanged-original-QA','exec'),qenv);base_qa=qenv['base_qa']
if __name__=='__main__':
    assert not ROOT.exists();doc,logical=map(read,[MANUSCRIPT,LOGICAL])
    assert logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and logical['total_bound_alignment_cases']==244
    rows=[];failures=[]
    for row in doc['records']:
        try:
            assert not row['review']['formatting'];planning=dict(row);body=row['english']
            assert not any(t in body for t in ['{LB','{ALIGN','{PAD','\n','\r'])
            assert body.count('{MACRO:FI}')==int(row['source_record_index'] in [311,388])
            planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body
            p=plan(planning);assert ' '.join(p['lines'])==body
            encoded=bytes.fromhex(p['encoded_hex']);assert encoded[0]==row['source_selector'] and b'\0' not in encoded[1:]
            p.update(file_path=doc['file_path'],block=row['block'],source_record_index=row['source_record_index'],
                source_selector=row['source_selector'],kind=row['kind'],logical_English=body,planning_record=planning,base_QA=base_qa(planning,p),
                original_consumer_usable_text_width_px=216,original_consumer_bitmap_width_px=216,
                source00_actor_byte_owned_by_native_preamble_not_NUL_body_formatter=row['source_selector']==0)
            rows.append(p)
        except (ValueError,AssertionError) as exc:failures.append(dict(id=row['id'],error_type=type(exc).__name__,error=str(exc)))
    ROOT.mkdir(parents=True)
    save(ROOT/'61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),logical=str(LOGICAL),logical_sha256=sha(LOGICAL.read_bytes()),
        records=rows,failures=failures,source_owned_plan_adapter=ADAPTER,source_owned_QA_adapter=qa_adapter,source_owned_measured_profile=inspect.getsource(get_profile),
        source_word_boundary_pairs=sorted(PAIRS),source_coherent_phrase_pairs=sorted(COHERENT_PAIRS),original_body_encoder_NUL_rejection_preserved_without_exception=True,
        exact16_clean00_objects15_unique_bodies_only=True,source02_and09_actors_executable_preambles_not_prose=True,
        source_current_packet=str(CURRENT),source_current_packet_sha256=sha(CURRENT.read_bytes()),progressive_viewport=[216,64],original_physical_rows_per_page=4,
        no_FE_objects_orunreviewed_CP932_literal_exception=True,no_global_font_profile_guard_orweak_rule_change=True,
        no_manual_break_padding_alignment_orprose_abbreviation_authored=True,all_original_QA_issues_preserved_without_removal=True,
        ordinary_boundary_warning_review_pending=True,short_complete_sentences_not_penalized_asbroken_internal_rows=True,orphan_then_short_internal_rows_then_sentence_page_boundaries_rows_coherent_phrases_soft_weak_preferences_final_balance=True,
        all61_formatting_gates_remain_false=True,native_fonts_names_stored_controls_actual_andrelease_pending=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,LOGICAL,CURRENT,Path(previous.__file__),Path(base_profile.__code__.co_filename),Path(__file__)]},full_goal_complete=False))
    for r in rows:
        issues=[i for i in r['base_QA']['issues'] if i['severity'] in ['warning','error']]
        if issues or r['expected_native_pages']>1:print(r['id'],r['lines'],'pages',r['expected_native_pages'],'QA',issues)
    print('PLANS',len(rows),'PAGES',sum(r['expected_native_pages'] for r in rows),'FAILURES',failures)
    if failures:raise SystemExit(1)
