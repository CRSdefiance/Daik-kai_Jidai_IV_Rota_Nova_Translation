"""Automatic source-bound216px text; preserve original00 preambles and distinct FE bitmap."""
import inspect
from dataclasses import replace
from pathlib import Path
from scripts import plan_Rafael_B45_layout_v7881b as previous
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_layout_v7932')
MANUSCRIPT=Path('translations/rafael_B46_editorial_manuscript_v1.json')
LOGICAL=Path('work/analysis/Rafael_B46_logical_v7931/24_logical_paragraphs96_original_native_alignments12_FE.json')
CURRENT=Path('work/analysis/Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json')
bound=read(CURRENT)
BOUND_ZERO_SOURCE_BODIES=frozenset(bytes.fromhex(r['source_hex']) for r in bound['records'] if r['source_selector']==0)
assert len(BOUND_ZERO_SOURCE_BODIES)==4 and previous.measured['ARM9_sha256']==bound['current_ARM9_sha256']
def get_profile(row):
    assert row['source_selector'] in [0,5,6,254]
    return replace(previous.get_profile(row),leading_speaker_bytes=frozenset({254} if row['kind']=='system-FE' else {0,5,6}))
ADAPTER=checked_text(previous.ADAPTER,{
    "row['source_selector'] in [0,6]":"row['source_selector'] in [0,5,6]",
    'Rafael-B45-RESEARCH-ONLY':'Rafael-B46-RESEARCH-ONLY',
    'No source/prose-preserving Rafael B45 plan:':'No source/prose-preserving Rafael B46 plan:',
})
PAIRS=previous.ENV['PAIRS']|{
    ('magnifying','glass'),('gray','frame'),('inspect','mode'),('battle','mode'),('search','mode'),
    ('press','a'),('press','y'),('press','l'),('press','r'),('r','or'),('or','y'),
    ("don't",'let'),('your','guard'),('guard','down'),('for','sure'),('all','sorts'),('sorts','of'),('at','sea'),('got','it')}
ENV={**previous.ENV,'BOUND_ZERO_SOURCE_BODIES':BOUND_ZERO_SOURCE_BODIES,'get_profile':get_profile,'PAIRS':PAIRS}
exec(compile(ADAPTER,__file__+'::source-bound-automatic-B46-planner','exec'),ENV);plan=ENV['plan']
qa_adapter=checked_text(inspect.getsource(previous.base_qa),{'Rafael-B45-native-QA':'Rafael-B46-native-QA'})
qenv={**previous.base_qa.__globals__,'get_profile':get_profile}
exec(compile(qa_adapter,__file__+'::all-original-QA','exec'),qenv);base_qa=qenv['base_qa']
if __name__=='__main__':
    assert not ROOT.exists();doc,logical=map(read,[MANUSCRIPT,LOGICAL])
    assert logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and logical['total_bound_alignment_cases']==96
    rows=[];failures=[]
    for row in doc['records']:
        try:
            assert not row['review']['formatting'];planning=dict(row);body=row['english']
            assert all(token not in body for token in ['{','}','FI','FA','FO'])
            planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body
            p=plan(planning);assert ' '.join(p['lines'])==body
            encoded=bytes.fromhex(p['encoded_hex']);assert encoded[0]==row['source_selector'] and b'\0' not in encoded[1:]
            p.update(file_path=doc['file_path'],block=row['block'],source_record_index=row['source_record_index'],
                source_selector=row['source_selector'],kind=row['kind'],logical_English=body,planning_record=planning,
                base_QA=base_qa(planning,p),original_consumer_usable_text_width_px=216,
                original_consumer_bitmap_width_px=228 if row['kind']=='system-FE' else 216,
                source00_actor_byte_owned_by_native_preamble_not_NUL_body_formatter=row['source_selector']==0)
            rows.append(p)
        except (ValueError,AssertionError) as exc:failures.append(dict(id=row['id'],error_type=type(exc).__name__,error=str(exc)))
    ROOT.mkdir(parents=True);save(ROOT/'24_automatic_plans_full_native_width_zero_preamble_separate_body.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),logical=str(LOGICAL),logical_sha256=sha(LOGICAL.read_bytes()),
        records=rows,failures=failures,source_owned_plan_adapter=ADAPTER,source_owned_QA_adapter=qa_adapter,
        source_owned_measured_profile=inspect.getsource(get_profile),source_word_boundary_pairs=sorted(PAIRS),
        original_body_encoder_NUL_rejection_preserved_without_exception=True,exact_four_clean00_records_only=True,
        source_current_packet=str(CURRENT),source_current_packet_sha256=sha(CURRENT.read_bytes()),
        progressive_viewport=[216,64],FE_logical_viewport=[228,48],FE_physical_viewport=[228,64],
        measured_FE_usable_text216_inside_original228_bitmap=True,
        same_runtime_boundary_measurement=str(previous.MEASUREMENT),same_runtime_boundary_measurement_sha256=sha(previous.MEASUREMENT.read_bytes()),
        no_global_font_profile_guard_orweak_rule_change=True,no_manual_break_padding_alignment_orprose_abbreviation_authored=True,
        all_original_QA_issues_preserved_no_waivers=True,all26_formatting_gates_remain_false=True,
        typed_two_choice_geometry_backing_highlights_andnative_fonts_pending=True,
        native_fonts_stored_controls_actual_andrelease_pending=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,LOGICAL,CURRENT,previous.MEASUREMENT,Path(previous.__file__),Path(__file__)]},full_goal_complete=False))
    for r in rows:print(r['id'],r['lines'],'QA',[(i['code'],i['severity']) for i in r['base_QA']['issues']])
    print('FAILURES',failures)
    if failures:raise SystemExit(1)
