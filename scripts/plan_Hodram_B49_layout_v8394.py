"""Private full-width automatic mixed-consumer B49 plans; two exact source-bound ellipsis cases only."""
import inspect
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Hodram_B47_B48_v8323 as previous
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_layout_v8394')
DOC=Path('translations/hodram_B49_editorial_manuscript_v1.json')
LOGICAL=Path('work/analysis/Hodram_B49_logical_v8389/logical_prose_and_choice_table.json')
MEASUREMENT=previous.MEASUREMENT
document=read(DOC)
ELLIPSIS_BINDINGS={r['id']:dict(source_hex=r['source_hex'],logical_English=r['english']) for r in document['records'] if '…' in r['english']}
assert set(ELLIPSIS_BINDINGS)=={'DK4_MES_B49_R0015','DK4_MES_B49_R0067'}
assert all(r['source_selector']==1 and r['source_Japanese'].startswith('…') and bytes.fromhex(r['source_hex'])[1:3]=='…'.encode('cp932') and r['english'].startswith('…') and r['english'].count('…')==1 for r in document['records'] if r['id'] in ELLIPSIS_BINDINGS)

def source_bound_ellipsis(row,body):
    return body.startswith('…') and body.count('…')==1 and ELLIPSIS_BINDINGS.get(row['id'])==dict(source_hex=row['source_hex'],logical_English=body)

ORDINARY_BINDINGS={r['id']:dict(source_hex=r['source_hex'],logical_English=r['english'],pairs=[('new','world')]) for r in document['records'] if r['id']=='DK4_MES_B49_R0033'}
assert len(ORDINARY_BINDINGS)==1

def ordinary_boundaries(row,body):
    if row['id'] not in ORDINARY_BINDINGS:return frozenset()
    binding=ORDINARY_BINDINGS[row['id']]
    if row['source_hex']!=binding['source_hex'] or body!=binding['logical_English']:
        raise ValueError('Exact source-qualified B49 directions paragraph required for ordinary word boundary')
    return set(binding['pairs'])

def get_profile(row):
    assert (row['kind']=='progressive' and row['source_selector'] in [1,2]) or (row['kind']=='system-FE' and row['source_selector']==254)
    p=get_dialogue_profile('hodram-story-live');assert p.window_width_px==216 and p.max_lines==4 and p.default_ascii_width==6 and p.default_multibyte_width==12
    assert p.macro_ascii_lengths==dict(FI=6,FA=9,FO=15) and p.guard_linebreaks and p.pair_phase_safe_breaks
    return replace(p,leading_speaker_bytes=frozenset({row['source_selector']}))

def display(text):return text.replace('{MACRO:FI}','Hodram').replace('{MACRO:FA}','Bergstrom').replace('{MACRO:FO}','Bergstrom Fleet')

ADAPTER=checked_text(previous.ADAPTER,{
    "row['source_selector'] in [2]":"row['source_selector'] in [1,2]",
    'all(32<=ord(c)<127 for c in body)':"all(32<=ord(c)<127 or c=='…' and source_bound_ellipsis(row,body) for c in body)",
    'length=len(display(text))':"length=len(display(text).encode('cp932'))",
    'line_lengths=[len(display(v)) for v in lines]':"line_lengths=[len(display(v).encode('cp932')) for v in lines]",
    'ordinary=pair in set()':'ordinary=pair in ordinary_boundaries(row,body)',
    'Hodram B47/B48 plan:':'Hodram B49 plan:','Hodram-B47-B48-RESEARCH-ONLY:':'Hodram-B49-RESEARCH-ONLY:',
})
PAIRS=previous.PAIRS|{('proof','of'),('of','supremacy'),('heavenly','wristband'),('new','world'),("i'd",'trade'),('give','me'),('now','give'),('find','it'),('give','you')}
ENV={**previous.ENV,'get_profile':get_profile,'display':display,'PAIRS':PAIRS,'BOUND_ZERO_SOURCE_BODIES':frozenset(),'source_bound_ellipsis':source_bound_ellipsis,'ordinary_boundaries':ordinary_boundaries}
exec(compile(ADAPTER,__file__+'::source-bound-full-usable-width','exec'),ENV);plan=ENV['plan']
QA_ADAPTER=checked_text(inspect.getsource(previous.base_qa),{'Rafael-B45-native-QA:':'Hodram-B49-native-QA:'})
qa_env={**previous.base_qa.__globals__,'get_profile':get_profile};exec(compile(QA_ADAPTER,__file__+'::unchanged-base-QA','exec'),qa_env);base_qa=qa_env['base_qa']
if __name__=='__main__':
    assert not ROOT.exists();logical,measured=map(read,[LOGICAL,MEASUREMENT]);assert logical['manuscript_sha256']==sha(DOC.read_bytes()) and logical['fresh_native_alignment_cases']==56
    image=NdsImage.open(document['current_ROM']);assert sha(Path(document['current_ROM']).read_bytes())==document['current_ROM_sha256'];_,_,oracle=bind(image)
    assert oracle['whole12byte_name_inverse_to_previous_font_oracle_ARM9'] and measured['ARM9_sha256']==previous.previous.bound['current_ARM9_sha256'];rows=[];failures=[]
    for row in document['records']:
        try:
            assert not row['review']['formatting'];planning=dict(row);planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english'];p=plan(planning)
            assert ' '.join(p['lines'])==row['english'];raw=bytes.fromhex(p['encoded_hex']);assert raw[0]==row['source_selector'] and b'\0' not in raw[1:]
            p.update(file_path=row['file_path'],block=row['block'],source_record_index=row['source_record_index'],source_selector=row['source_selector'],kind=row['kind'],logical_English=row['english'],planning_record=planning,base_QA=base_qa(planning,p),original_consumer_usable_text_width_px=216,original_consumer_bitmap_width_px=228 if row['kind']=='system-FE' else 216);rows.append(p)
        except (ValueError,AssertionError) as error:failures.append(dict(id=row['id'],error_type=type(error).__name__,error=str(error)))
    ROOT.mkdir(parents=True);save(ROOT/'automatic_plans.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),logical=str(LOGICAL),logical_sha256=sha(LOGICAL.read_bytes()),records=rows,failures=failures,source_owned_planner=ADAPTER,source_owned_QA_adapter=QA_ADAPTER,source_owned_profile_function=inspect.getsource(get_profile),source_owned_display_function=inspect.getsource(display),source_owned_ellipsis_predicate=inspect.getsource(source_bound_ellipsis),source_bound_ellipsis_bindings=ELLIPSIS_BINDINGS,source_owned_ordinary_boundary_predicate=inspect.getsource(ordinary_boundaries),ordinary_boundary_bindings=ORDINARY_BINDINGS,prior_layout_preserved="work/analysis/Hodram_B49_layout_v8393/automatic_plans.json",read_only_comparison="work/analysis/Hodram_B49_wrap_compare_v8393b/read_only_wrap_comparison.json",all_QA_recomputed_for_changed_compiler_breaks_without_filtering=True,coherent_pairs=sorted(PAIRS),all_words_punctuation_andzero_source_macros_preserved_without_shortening=True,no_prose_manual_breaks_alignment_padding_font_viewport_orcore_guard_changes=True,automatic_compiler_breaks_not_authored_prose=True,original_FE_usable216_bitmap228_stride288_metrics6x12_physical16_distinction_preserved=True,earlier_boundary_measurement=str(MEASUREMENT),earlier_boundary_measurement_sha256=sha(MEASUREMENT.read_bytes()),target_font_oracle_inverse_binding=oracle,all_original_QA_errors_warnings_infos_preserved_without_waiver=True,logical_typed_choice_proposal=logical['typed_choice'],all16_formatting_gates_remain_false=True,native_complete_glyphs_bounds_pagination_stored_actual_choice_UI_policy_andregistered_integration_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,LOGICAL,MEASUREMENT,Path(previous.__file__),Path('scripts/Hodram_FE_font_oracles_v8315.py'),Path(__file__)]}))
    for row in rows:print(row['id'],row['expected_native_pages'],row['lines'],[(i['severity'],i['code']) for i in row['base_QA']['issues']])
    print('PLANS',len(rows),'FAILURES',failures);assert not failures and len(rows)==14
