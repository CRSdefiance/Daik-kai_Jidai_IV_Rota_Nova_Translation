"""Automatic full-width B50 paragraphs; source00/02/09 and distinct FA/FI remain unchanged."""
import inspect
from dataclasses import replace
from pathlib import Path
from scripts import plan_Rafael_B49_layout_v8090c as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Rafael_B50_layout_v8140b')
MANUSCRIPT=Path('translations/rafael_B50_editorial_manuscript_v1.json')
LOGICAL=Path('work/analysis/Rafael_B50_logical_v8139/28_logical_paragraphs112_original_native_alignments_no_FE.json')
CURRENT=Path('work/analysis/Rafael_B50_current_v8136/all28_complete_source_current_refs_before_new_English_manuscript.json')
bound=read(CURRENT)
BOUND_ZERO_SOURCE_BODIES=frozenset(bytes.fromhex(r['source_hex']) for r in bound['records'] if r['source_selector']==0)
assert sum(r['source_selector']==0 for r in bound['records'])==10 and len(BOUND_ZERO_SOURCE_BODIES)==10
def get_profile(row):
    assert row['kind']=='progressive' and row['source_selector'] in [0,2,9]
    p=previous.get_profile(row);assert p.window_width_px==216 and p.default_ascii_width==6 and p.default_multibyte_width==12 and p.macro_ascii_lengths==dict(FI=6,FA=6,FO=10)
    return replace(p,leading_speaker_bytes=frozenset({0,2,9}))
ADAPTER=checked_text(previous.ADAPTER,{'B49':'B50','[0,2,4,5,6,8,9]':'[0,2,9]'})
PAIRS=previous.PAIRS|{('this','guy'),('never','mind'),('treasure','map'),('are','you'),('making','money'),('live','up'),('up','to'),('your','expectations'),('thank','you'),('take','care')}
COHERENT_PAIRS=previous.COHERENT_PAIRS|{('this','guy'),('never','mind'),('treasure','map'),('are','you'),('making','money'),('do','my'),('my','best'),('live','up'),('up','to'),('your','expectations'),('thank','you'),('take','care'),('as','ever'),('mr',previous.ENV['norm']('{MACRO:FA}'))}
COHERENT_PAIRS=COHERENT_PAIRS|{("it's",'been'),("you're",'as'),('come','on'),('no','idea'),("i'll",'do')}
ENV={**previous.ENV,'BOUND_ZERO_SOURCE_BODIES':BOUND_ZERO_SOURCE_BODIES,'get_profile':get_profile,'PAIRS':PAIRS,'COHERENT_PAIRS':COHERENT_PAIRS}
exec(compile(ADAPTER,__file__+'::exact-source-B50-automatic-plan','exec'),ENV);plan=ENV['plan']
qa_adapter=checked_text(previous.qa_adapter,{'Rafael-B49-native-QA':'Rafael-B50-native-QA'})
qenv={**previous.base_qa.__globals__,'get_profile':get_profile};exec(compile(qa_adapter,__file__+'::unchanged-original-QA','exec'),qenv);base_qa=qenv['base_qa']
if __name__=='__main__':
    assert not ROOT.exists();doc,logical=map(read,[MANUSCRIPT,LOGICAL]);assert logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and logical['total_bound_alignment_cases']==112
    rows=[];failures=[]
    for row in doc['records']:
        try:
            assert not row['review']['formatting'];planning=dict(row);body=row['english'];assert not any(t in body for t in ['{LB','{ALIGN','{PAD','\n','\r'])
            for token in ['FI','FA','FO']:assert body.count('{MACRO:'+token+'}')==bytes.fromhex(row['source_hex'])[1:].count(token.encode())
            planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body
            p=plan(planning);assert ' '.join(p['lines'])==body;encoded=bytes.fromhex(p['encoded_hex']);assert encoded[0]==row['source_selector'] and b'\0' not in encoded[1:]
            p.update(file_path=doc['file_path'],block=50,source_record_index=row['source_record_index'],source_selector=row['source_selector'],kind='progressive',logical_English=body,planning_record=planning,base_QA=base_qa(planning,p),
                original_consumer_usable_text_width_px=216,original_consumer_bitmap_width_px=216,source00_actor_byte_owned_by_native_preamble_not_NUL_body_formatter=row['source_selector']==0)
            rows.append(p)
        except (ValueError,AssertionError) as e:failures.append(dict(id=row['id'],error_type=type(e).__name__,error=str(e)))
    ROOT.mkdir(parents=True);save(ROOT/'28_automatic_plans_full_native_width_exact_source00_02_09_FA2_FI1.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),logical=str(LOGICAL),logical_sha256=sha(LOGICAL.read_bytes()),records=rows,failures=failures,
        source_owned_plan_adapter=ADAPTER,source_owned_QA_adapter=qa_adapter,source_owned_measured_profile=inspect.getsource(get_profile),source_word_boundary_pairs=sorted(PAIRS),source_coherent_phrase_pairs=sorted(COHERENT_PAIRS),
        original_body_encoder_NUL_rejection_preserved_without_exception=True,exact10_clean00_objects10_unique_bodies_only=True,source02_and09_actors_executable_preambles_not_prose=True,
        source_current_packet=str(CURRENT),source_current_packet_sha256=sha(CURRENT.read_bytes()),progressive_viewport=[216,64],original_physical_rows_per_page=4,
        source_macro_counts=dict(FI=1,FA=2,FO=0),no_FE_objects_orunreviewed_CP932_literal_exception=True,no_global_font_profile_guard_orweak_rule_change=True,
        no_manual_break_padding_alignment_orprose_abbreviation_authored=True,all_original_QA_issues_preserved_without_removal=True,ordinary_boundary_warning_review_pending=True,
        short_complete_sentences_not_penalized_asbroken_internal_rows=True,orphan_then_short_internal_rows_then_sentence_page_boundaries_rows_coherent_phrases_soft_weak_preferences_final_balance=True,
        all28_formatting_gates_remain_false=True,native_fonts_names_stored_controls_actual_andrelease_pending=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,LOGICAL,CURRENT,Path(previous.__file__),Path(__file__)]},full_goal_complete=False))
    for r in rows:
        issues=[i for i in r['base_QA']['issues'] if i['severity'] in ['warning','error']]
        if issues or r['expected_native_pages']>1:print(r['id'],r['lines'],'pages',r['expected_native_pages'],'QA',issues)
    print('PLANS',len(rows),'PAGES',sum(r['expected_native_pages'] for r in rows),'FAILURES',failures)
    if failures:raise SystemExit(1)
