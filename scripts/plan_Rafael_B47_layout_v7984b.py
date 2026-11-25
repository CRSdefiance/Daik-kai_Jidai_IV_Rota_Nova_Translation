"""Automatic full-width B47 paragraphs with exact source00 preambles andunchanged body guard."""
import inspect
from dataclasses import replace
from pathlib import Path
from scripts import plan_Rafael_B46_layout_v7932 as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Rafael_B47_layout_v7984b')
MANUSCRIPT=Path('translations/rafael_B47_editorial_manuscript_v1.json')
LOGICAL=Path('work/analysis/Rafael_B47_logical_v7983/15_logical_paragraphs60_original_native_progressive_alignments.json')
CURRENT=Path('work/analysis/Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json')
bound=read(CURRENT)
BOUND_ZERO_SOURCE_BODIES=frozenset(bytes.fromhex(r['source_hex']) for r in bound['records'] if r['source_selector']==0)
assert len(BOUND_ZERO_SOURCE_BODIES)==5 and previous.previous.measured['ARM9_sha256']==bound['current_ARM9_sha256']
def get_profile(row):
    assert row['kind']=='progressive' and row['source_selector'] in [0,4,5,6]
    return replace(previous.previous.get_profile(row),leading_speaker_bytes=frozenset({0,4,5,6}))
ADAPTER=checked_text(previous.ADAPTER,{
    "row['source_selector'] in [0,5,6]":"row['source_selector'] in [0,4,5,6]",
    'Rafael-B46-RESEARCH-ONLY':'Rafael-B47-RESEARCH-ONLY',
    'No source/prose-preserving Rafael B46 plan:':'No source/prose-preserving Rafael B47 plan:',
})
PAIRS=previous.PAIRS|{
    ('eastern','half'),('trading','contract'),('skilled','navigators'),('other','waters'),
    ("pasha's",'forces'),("valdes's",'spanish'),('ottoman','forces'),('at','least'),
    ('get','around'),('get','to'),('to','work'),('toughen','ourselves'),('ourselves','up'),
}
ENV={**previous.ENV,'BOUND_ZERO_SOURCE_BODIES':BOUND_ZERO_SOURCE_BODIES,'get_profile':get_profile,'PAIRS':PAIRS}
exec(compile(ADAPTER,__file__+'::source-bound-automatic-B47-planner','exec'),ENV);plan=ENV['plan']
qa_adapter=checked_text(previous.qa_adapter,{'Rafael-B46-native-QA':'Rafael-B47-native-QA'})
qenv={**previous.base_qa.__globals__,'get_profile':get_profile}
exec(compile(qa_adapter,__file__+'::all-original-QA','exec'),qenv);base_qa=qenv['base_qa']
if __name__=='__main__':
    assert not ROOT.exists();doc,logical=map(read,[MANUSCRIPT,LOGICAL])
    assert logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and logical['total_bound_alignment_cases']==60
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
                base_QA=base_qa(planning,p),original_consumer_usable_text_width_px=216,original_consumer_bitmap_width_px=216,
                source00_actor_byte_owned_by_native_preamble_not_NUL_body_formatter=row['source_selector']==0)
            rows.append(p)
        except (ValueError,AssertionError) as exc:
            failures.append(dict(id=row['id'],error_type=type(exc).__name__,error=str(exc)))
    ROOT.mkdir(parents=True)
    save(ROOT/'15_automatic_plans_full_native_width_zero_preamble_separate_body.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),logical=str(LOGICAL),logical_sha256=sha(LOGICAL.read_bytes()),
        records=rows,failures=failures,source_owned_plan_adapter=ADAPTER,source_owned_QA_adapter=qa_adapter,
        source_owned_measured_profile=inspect.getsource(get_profile),source_word_boundary_pairs=sorted(PAIRS),
        original_body_encoder_NUL_rejection_preserved_without_exception=True,exact_five_clean00_records_only=True,
        source_current_packet=str(CURRENT),source_current_packet_sha256=sha(CURRENT.read_bytes()),
        progressive_viewport=[216,64],original_physical_rows_per_page=4,
        no_global_font_profile_guard_orweak_rule_change=True,no_manual_break_padding_alignment_orprose_abbreviation_authored=True,
        all_original_QA_issues_preserved_no_waivers=True,all15_formatting_gates_remain_false=True,
        native_fonts_stored_controls_actual_andrelease_pending=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,LOGICAL,CURRENT,Path(previous.__file__),Path(__file__)]},full_goal_complete=False))
    for r in rows:print(r['id'],r['lines'],'QA',[(i['code'],i['severity']) for i in r['base_QA']['issues']])
    print('FAILURES',failures)
    if failures:raise SystemExit(1)
