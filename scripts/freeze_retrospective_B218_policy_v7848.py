"""Freeze the exact13 unchanged paragraphs andone scoped automatic boundary preference."""
from copy import deepcopy
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_policy_v7848')
DOC=Path('translations/lil_B218_retrospective_layout_manuscript_v1.json')
MAP=Path('work/analysis/retrospective_B218_relocation_v7839b/all13_bound_one_changed_wrap15_commands_complete_clean_predecessor_inverse.json')
PLAN=Path('work/analysis/retrospective_B218_predicate_plan_v7833/one_changed_automatic_plan12_exact_reuses_all13_unmodified_base_QA.json')
VIEW=Path('work/analysis/retrospective_B218_actual_view_v7847/26_actual_panes_eight_sheets_andall_measured_limits_viewed.json')
CONTRACT=Path('translations/lil_B218_retrospective_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/lil_B218_retrospective_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/lil_B218_retrospective_layout_v1.py')
PLANNER=Path('dk4tool/dialogue/lil_B218_retrospective_plan_v1.py')
PLANNER_SOURCE='''"""Exact B218 retrospective plan adapter;one paragraph receives a soft boundary preference."""
from types import FunctionType
from scripts import plan_lil_B218_layout_v6881c as inherited
def plan(row):
    if row['id']!='DK4_MES_B218_R0027':return inherited.plan(row)
    bound=FunctionType(inherited.plan.__code__,{**inherited.plan.__globals__,'PAIRS':inherited.PAIRS|{("that's","a")}},argdefs=inherited.plan.__defaults__)
    return bound(row)
'''
if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT,PROFILE,FORMATTER,PLANNER])
    doc,mapping,plan,view=map(read,[DOC,MAP,PLAN,VIEW])
    assert mapping['manuscript_sha256']==plan['manuscript_sha256']==sha(DOC.read_bytes())
    assert view['all_eight_sheets_directly_viewed'] and view['all13_previous_andproposed_body_pages_andLil_Ian_headers_viewed']
    oldcontract=read('translations/lil_B218_native_contract_v1.json');bindings={};row_infos=0
    for row in mapping['records']:
        ident=row['id'];before=oldcontract['record_bindings'][ident];p=next(p for p in plan['records'] if p['id']==ident)
        current=p['proposed'];assert current['encoded_hex']==row['compiled_hex']
        assert not any(i['severity'] in ['warning','error'] for i in p['base_QA']['issues'])
        b=deepcopy(before);b.update(source_reference=row['source_reference'],current_reference=row['current_reference'],
            compiler_source_hex=row['source_hex'],
            planning_record={k:row[k] for k in ['id','english','kind','source_hex','source_selector']},
            compiled_hex=current['encoded_hex'],lines=current['lines'])
        assert (bytes.fromhex(row['source_hex']).count(b'\n')!=len(current['lines'])-1)==bool(b['row_count_reason'])
        row_infos+=bool(b['row_count_reason'])
        if ident=='DK4_MES_B218_R0027':
            assert current['lines']==["(Ian's interested?","That's a surprise.)"]
            b['retrospective_layout_reason']="Keep the complete short That's a surprise predicate together after the complete private question;all words and punctuation remain."
        else:assert current['encoded_hex']==before['compiled_hex']
        bindings[ident]=b
    assert len(bindings)==13 and row_infos==9
    compile(PLANNER_SOURCE,str(PLANNER),'exec')
    deps=[DOC,MAP,PLAN,VIEW,
        Path('work/analysis/retrospective_B218_native_v7838/one_changed_wrap12_alignments_two_complete_current_native_planes.json'),
        Path('work/analysis/retrospective_B218_stored_controls_v7840/one_changed_stored_plane13_dispatches_A00025_ends_andtwo_sheets_viewed.json'),
        Path('work/analysis/retrospective_B218_actual_v7846/two_English_scenes_complete_masks_commands_andall_measured_late_limits.json'),
        Path('work/analysis/retrospective_B218_loader_v7842/whole_SC2_336_loads_cache_hits672_original_parent_modes.json'),
        Path('work/analysis/retrospective_B218_caller_census_v7843/all15_commands_original_entry_andbounded_shipped_callers.json'),
        Path('work/analysis/retrospective_B218_wrap_gloss_v7832/thirteen_fresh_clean_exchange_glosses_before_full_current_layout_review.json'),
        Path('scripts/plan_lil_B218_layout_v6881c.py'),Path('scripts/plan_lil_B214_layout_v6705b.py'),
        Path('dk4tool/patch/retrospective_SC2_reconstruction_v2.py'),Path(__file__),
        *[Path('dk4tool/dialogue')/n for n in ['profiles.py','codec.py','encoder.py','layout.py','qa.py','review.py']]]
    profile_source=Path('dk4tool/dialogue/lil_B218_profile_v1.py').read_text(encoding='utf-8')
    oldhash=sha(Path('translations/lil_B218_native_contract_v1.json').read_bytes())
    # Plan module has no generated dependency on its own contract, avoiding a hash cycle.
    PLANNER.write_text(PLANNER_SOURCE,encoding='utf-8');deps.append(PLANNER)
    save(CONTRACT,dict(format='B218-retrospective-current-native-source-contract-v1',
        source_block_hashes=[mapping['groups'][0]['clean_block_sha256'],mapping['groups'][0]['source_block_sha256']],
        physical_native_rows_per_page=4,physical_viewport=[216,64],complete_native_pages=13,
        record_bindings=bindings,choice_bindings={},dependencies={str(p):sha(p.read_bytes()) for p in deps},
        all_words_andsource_controls_retained_one_automatic_wrap_only=True,nine_individual_rowcount_reasons_preserved=True,
        all_base_QA_without_warning_removal_orwaivers=True,no_original_orinvented_macros=True,
        unchanged12_stored_plans_exact_new_changed_plane_andboth_actual_scenes_bound=True,
        policy_validation_atomic_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    profile=checked_text(profile_source,{
        'translations/lil_B218_native_contract_v1.json':str(CONTRACT).replace('\\','/'),
        oldhash:sha(CONTRACT.read_bytes()),
        'aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05':
        '2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a',
        'lil-B218-source-bound-v1:':'lil-B218-retrospective-source-bound-v1:',
        'AA5 runtime required':'current2b6 runtime required',
    })
    formatter=checked_text(Path('dk4tool/dialogue/lil_B218_layout_v1.py').read_text(encoding='utf-8'),{
        'dk4tool.dialogue.lil_B218_profile_v1':'dk4tool.dialogue.lil_B218_retrospective_profile_v1',
        'from scripts.plan_lil_B218_layout_v6881c import plan as frozen_plan':
        'from dk4tool.dialogue.lil_B218_retrospective_plan_v1 import plan as frozen_plan',
        'lil-B218-source-bound-v1:':'lil-B218-retrospective-source-bound-v1:',
    })
    PROFILE.write_text(profile,encoding='utf-8');FORMATTER.write_text(formatter,encoding='utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'prepared_frozen_policy.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),
        profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),
        planner=str(PLANNER),planner_sha256=sha(PLANNER.read_bytes()),thirteen_exact_paragraphs_one_scoped_boundary_change=True,
        original_numeric_geometry_profile_ownership_andQA_guards_preserved=True,
        negative_policy_checks_atomic_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    print('Frozen retrospective B218 policy:13unchanged paragraphs/one scoped wrap,9original row reasons,zero warning waivers. Positive/negative policy checks pending.')
