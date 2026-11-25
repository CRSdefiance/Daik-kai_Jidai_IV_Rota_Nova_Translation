"""Private automatic full-width Hodram layout; no prose shortening or global rule changes."""
import inspect
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Rafael_B49_layout_v8090c as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B137_B45_B46_layout_v8245')
MANUSCRIPT=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v2.json')
LOGICAL=Path('work/analysis/Hodram_B137_B45_B46_refinement_v8244/28_logical_paragraphs4_fresh108_exact_reused_alignments.json')
doc=read(MANUSCRIPT)
ELLIPSIS_SOURCES={r['id']:r['source_hex'] for r in doc['records'] if r['english']=='…'}
assert len(ELLIPSIS_SOURCES)==3 and all(r['source_Japanese']=='…' for r in doc['records'] if r['id'] in ELLIPSIS_SOURCES)

def get_profile(row):
    assert row['kind']=='progressive' and row['source_selector'] in [1,2,9,16,18,113]
    p=get_dialogue_profile('hodram-story-live')
    assert p.window_width_px==216 and p.default_ascii_width==6 and p.default_multibyte_width==12 and p.max_lines==4
    assert p.macro_ascii_lengths==dict(FI=6,FA=9,FO=15) and p.macro_widths==dict(FI=36,FA=54,FO=90,I=12)
    assert p.guard_linebreaks and p.pair_phase_safe_breaks
    return replace(p,leading_speaker_bytes=frozenset({1,2,9,16,18,113}))

def display(text):
    return text.replace('{MACRO:FI}','Hodram').replace('{MACRO:FA}','Bergstrom').replace('{MACRO:FO}','Bergstrom Fleet')

ADAPTER=checked_text(previous.ADAPTER,{
    "row['source_selector'] in [0,2,4,5,6,8,9]":"row['source_selector'] in [1,2,9,16,18,113]",
    'all(32<=ord(c)<127 for c in body)':"all(32<=ord(c)<127 or c=='…' and body=='…' and ELLIPSIS_SOURCES.get(row['id'])==row['source_hex'] for c in body)",
    'length=len(display(text))':'length=sum(1 if ord(c)<128 else 2 for c in display(text))',
    'line_lengths=[len(display(v)) for v in lines]':'line_lengths=[sum(1 if ord(c)<128 else 2 for c in display(v)) for v in lines]',
    'Rafael-B49-RESEARCH-ONLY':'Hodram-B137-B45-B46-RESEARCH-ONLY',
    'No source/prose-preserving Rafael B49 plan:':'No source/prose-preserving Hodram B137/B45/B46 plan:',
    "profile.macro_ascii_lengths=={'FI':6,'FA':6,'FO':10} and profile.macro_widths['FA']==36":"profile.macro_ascii_lengths=={'FI':6,'FA':9,'FO':15} and profile.macro_widths['FA']==54",
})
PHRASES={("the","Mediterranean".lower()),("the","towns"),("all","of"),("can't","seem"),("she's","right"),("what","does"),("does","she"),("she","mean"),('north','sea'),('sea','trade'),('trade','routes'),('argot','company'),('business','rival'),('treasure','map'),('map','key'),('of','all'),('all','people'),('no','holding'),('holding','back'),("wasn't",'it'),('no','wonder'),('so','sorry'),('so','much')}
PAIRS=previous.PAIRS|PHRASES
COHERENT_PAIRS=previous.COHERENT_PAIRS|PHRASES
ENV={**previous.ENV,'get_profile':get_profile,'display':display,'PAIRS':PAIRS,'COHERENT_PAIRS':COHERENT_PAIRS,'BOUND_ZERO_SOURCE_BODIES':frozenset(),'ELLIPSIS_SOURCES':ELLIPSIS_SOURCES}
exec(compile(ADAPTER,__file__+'::captain1-sourcebound-automatic-plan','exec'),ENV);plan=ENV['plan']
qa_adapter=checked_text(previous.qa_adapter,{'Rafael-B49-native-QA':'Hodram-B137-B45-B46-native-QA'})
qenv={**previous.base_qa.__globals__,'get_profile':get_profile}
exec(compile(qa_adapter,__file__+'::unchanged-original-QA','exec'),qenv);base_qa=qenv['base_qa']

if __name__=='__main__':
    assert not ROOT.exists();logical=read(LOGICAL)
    assert logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and logical['total_bound_alignment_cases']==112
    rows=[];failures=[]
    for row in doc['records']:
        try:
            assert not row['review']['formatting'];planning=dict(row);body=row['english']
            assert not any(t in body for t in ['{LB','{ALIGN','{PAD','\n','\r','{MACRO:'])
            planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body
            p=plan(planning);assert ' '.join(p['lines'])==body
            encoded=bytes.fromhex(p['encoded_hex']);assert encoded[0]==row['source_selector'] and b'\0' not in encoded[1:]
            p.update(file_path=row['file_path'],block=row['block'],source_record_index=row['source_record_index'],source_selector=row['source_selector'],kind=row['kind'],
                logical_English=body,planning_record=planning,base_QA=base_qa(planning,p),original_consumer_usable_text_width_px=216,original_consumer_bitmap_width_px=216)
            rows.append(p)
        except (ValueError,AssertionError) as exc:failures.append(dict(id=row['id'],error_type=type(exc).__name__,error=str(exc)))
    ROOT.mkdir(parents=True)
    save(ROOT/'28_automatic_Hodram_plans_full_native_width.json',dict(manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),logical=str(LOGICAL),logical_sha256=sha(LOGICAL.read_bytes()),
        records=rows,failures=failures,source_owned_plan_adapter=ADAPTER,source_owned_QA_adapter=qa_adapter,source_owned_measured_profile=inspect.getsource(get_profile),source_owned_measured_display=inspect.getsource(display),
        source_word_boundary_pairs=sorted(PAIRS),source_coherent_phrase_pairs=sorted(COHERENT_PAIRS),source_bound_three_ellipsis_records=ELLIPSIS_SOURCES,
        original_body_encoder_NUL_rejection_preserved_without_exception=True,progressive_viewport=[216,64],original_physical_rows_per_page=4,
        measured_default_macro_lengths=dict(FI=6,FA=9,FO=15),source_macro_totals=dict(FI=0,FA=0,FO=0),
        source_selectors_exactly_01_02_09_10_12_71_no_FE_or00_exception=True,no_global_font_profile_guard_orweak_rule_change=True,
        no_manual_break_padding_alignment_orprose_abbreviation_authored=True,all_original_QA_issues_preserved_without_removal=True,
        ordinary_boundary_warning_review_pending=True,all28_formatting_gates_remain_false=True,
        native_fonts_names_stored_controls_actual_andregistered_release_pending=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,LOGICAL,Path(previous.__file__),Path(__file__)]},full_goal_complete=False))
    for r in rows:print(r['id'],r['lines'],'pages',r['expected_native_pages'],'QA',r['base_QA']['issues'])
    print('PLANS',len(rows),'PAGES',sum(r['expected_native_pages'] for r in rows),'FAILURES',failures)
    if failures:raise SystemExit(1)
