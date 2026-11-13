"""Automatic full-width B48 plans; exact00/4B/71 source state andfour distinct FE consumers."""
import inspect
from dataclasses import replace
from pathlib import Path
from scripts import plan_Rafael_B47_layout_v7984e as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Rafael_B48_layout_v8035c')
MANUSCRIPT=Path('translations/rafael_B48_editorial_manuscript_v2.json')
LOGICAL=Path('work/analysis/Rafael_B48_logical_v8032/91_logical_paragraphs364_original_native_alignments4_FE.json')
CURRENT=Path('work/analysis/Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json')
bound=read(CURRENT)
BOUND_ZERO_SOURCE_BODIES=frozenset(bytes.fromhex(r['source_hex']) for r in bound['records'] if r['source_selector']==0)
assert sum(r['source_selector']==0 for r in bound['records'])==28 and len(BOUND_ZERO_SOURCE_BODIES)==27 and previous.previous.previous.measured['ARM9_sha256']==bound['current_ARM9_sha256']
ELLIPSIS_ID='DK4_MES_B48_R0171'
ELLIPSIS_SOURCE='058163'
def display(text):
    # Display is a width-accounting string only. The real CP932 glyph remains untouched.
    return previous.previous.previous.previous.display(text).replace('…','..')
def get_profile(row):
    assert row['source_selector'] in [0,4,5,6,7,8,13,75,113,254]
    p=previous.previous.previous.get_profile(row)
    assert p.window_width_px==216 and p.default_ascii_width==6 and p.default_multibyte_width==12
    return replace(p,leading_speaker_bytes=frozenset({254} if row['kind']=='system-FE' else {0,4,5,6,7,8,13,75,113}))
ADAPTER=checked_text(previous.ADAPTER,{
    "row['source_selector'] in [0,4,5,6]":"row['source_selector'] in [0,4,5,6,7,8,13,75,113]",
    'all(32<=ord(c)<127 for c in body)':
        "all(32<=ord(c)<127 or c=='…' and row['id']==ELLIPSIS_ID and body=='…' and row['source_hex']==ELLIPSIS_SOURCE for c in body)",
    'Rafael-B47-RESEARCH-ONLY':'Rafael-B48-RESEARCH-ONLY',
    'No source/prose-preserving Rafael B47 plan:':'No source/prose-preserving Rafael B48 plan:',
})
ADAPTER=checked_text(ADAPTER,{
    'return (0,0,0,0,0),()':'return (0,0,0,0,0,0),()',
    'cost[0]+tiny,cost[1]+int(not final and (line+1)%4==0 and not terminal),cost[2]+1,cost[3]+weak,cost[4]+':
        'cost[0]+tiny,cost[1]+int(not final and length<18),cost[2]+int(not final and (line+1)%4==0 and not terminal),cost[3]+1,cost[4]+weak,cost[5]+',
})
PAIRS=previous.PAIRS|{
    ('proof','of'),('of','conquest'),('seven','sages'),('faraway','country'),
    ('item','information'),('deck','screen'),('each','sea'),('good','work'),
    ('young','man'),('arcadius','eudoxios'),('hans','letzel'),('southern','africa'),
    ('for','years'),('find','out'),('i','suppose'),('aboard','will'),
}
ENV={**previous.ENV,'BOUND_ZERO_SOURCE_BODIES':BOUND_ZERO_SOURCE_BODIES,'get_profile':get_profile,
    'PAIRS':PAIRS,'display':display,'ELLIPSIS_ID':ELLIPSIS_ID,'ELLIPSIS_SOURCE':ELLIPSIS_SOURCE}
exec(compile(ADAPTER,__file__+'::source-bound-automatic-B48-planner','exec'),ENV);plan=ENV['plan']
qa_adapter=checked_text(previous.qa_adapter,{'Rafael-B47-native-QA':'Rafael-B48-native-QA'})
qenv={**previous.base_qa.__globals__,'get_profile':get_profile}
exec(compile(qa_adapter,__file__+'::all-original-QA','exec'),qenv);base_qa=qenv['base_qa']
if __name__=='__main__':
    assert not ROOT.exists();doc,logical=map(read,[MANUSCRIPT,LOGICAL])
    assert logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and logical['total_bound_alignment_cases']==364
    rows=[];failures=[]
    for row in doc['records']:
        try:
            assert not row['review']['formatting'];planning=dict(row);body=row['english']
            assert not any(t in body for t in ['{LB','{ALIGN','{PAD','\n','\r'])
            assert body.count('{MACRO:FI}')==int(row['source_record_index']==370)
            planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body
            p=plan(planning);assert ' '.join(p['lines'])==body
            encoded=bytes.fromhex(p['encoded_hex']);assert encoded[0]==row['source_selector'] and b'\0' not in encoded[1:]
            assert row['kind']!='system-FE' or p['expected_native_pages']==1
            p.update(file_path=doc['file_path'],block=row['block'],source_record_index=row['source_record_index'],
                source_selector=row['source_selector'],kind=row['kind'],logical_English=body,planning_record=planning,
                base_QA=base_qa(planning,p),original_consumer_usable_text_width_px=216,
                original_consumer_bitmap_width_px=228 if row['kind']=='system-FE' else 216,
                source00_actor_byte_owned_by_native_preamble_not_NUL_body_formatter=row['source_selector']==0)
            rows.append(p)
        except (ValueError,AssertionError) as exc:failures.append(dict(id=row['id'],error_type=type(exc).__name__,error=str(exc)))
    ROOT.mkdir(parents=True)
    save(ROOT/'91_automatic_plans_full_native_width_source_preambles4_FE.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),logical=str(LOGICAL),logical_sha256=sha(LOGICAL.read_bytes()),
        records=rows,failures=failures,source_owned_plan_adapter=ADAPTER,source_owned_QA_adapter=qa_adapter,
        source_owned_measured_profile=inspect.getsource(get_profile),source_owned_width_accounting=inspect.getsource(display),
        source_word_boundary_pairs=sorted(PAIRS),original_body_encoder_NUL_rejection_preserved_without_exception=True,
        exact28_clean00_records_only=True,printable4B71_only_exact_source_actor_preambles=True,
        source_current_packet=str(CURRENT),source_current_packet_sha256=sha(CURRENT.read_bytes()),
        progressive_viewport=[216,64],original_physical_rows_per_page=4,
        FE_usable_width216_original_bitmap228_logical48_physical64_unchanged=True,
        exact_source_ellipsis_retained12px_accounting_native_glyph_validation_pending=True,
        no_global_font_profile_guard_orweak_rule_change=True,no_manual_break_padding_alignment_orprose_abbreviation_authored=True,
        all_original_QA_issues_preserved_without_removal=True,ordinary_boundary_warning_review_pending=True,
        orphan_then_short_internal_rows_then_sentence_page_boundaries_rows_soft_weak_preferences_final_balance=True,
        all91_formatting_gates_remain_false=True,native_fonts_names_stored_controls_actual_andrelease_pending=True,
        new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [MANUSCRIPT,LOGICAL,CURRENT,Path(previous.__file__),Path(__file__)]},full_goal_complete=False))
    for r in rows:
        issues=[i for i in r['base_QA']['issues'] if i['severity'] in ['warning','error']]
        if issues or r['expected_native_pages']>1:print(r['id'],r['lines'],'pages',r['expected_native_pages'],'QA',issues)
    print('PLANS',len(rows),'PAGES',sum(r['expected_native_pages'] for r in rows),'FAILURES',failures)
    if failures:raise SystemExit(1)
