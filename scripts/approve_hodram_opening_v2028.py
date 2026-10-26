"""Approve source-bound native rules and practical representative gameplay scope."""
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hodram_opening_approval_v2028')
OLD=Path('translations/hodram_opening_contextual_editorial_manuscript_v1.json')
DOC=Path('translations/hodram_opening_contextual_editorial_manuscript_v2.json')
MAP=Path('translations/hodram_opening_editorial_relocation_map_v1.json')
PLAN=Path('work/analysis/hodram_opening_relocation_v2023/complete_three_block_typed_relocation_research.json')
FONT=Path('work/analysis/hodram_opening_fonts_v2021/all67_progressive_native_macros_and_complete_font_planes.json')
FE=Path('work/analysis/hodram_opening_FE_v2022/all6_separate_FE_native_planes_and48_macro_calls.json')
REF=Path('work/analysis/hodram_opening_references_v2026/three_block_mapping_and_inherited_executable_entry_census.json')
ACTUAL=Path('work/analysis/hodram_opening_actual_v2027d/ordinary_current_revised_opening_and_full_actual_planes.json')
LIL=Path('work/analysis/lil_opening_scene_v1708/complete_B22_actual_scene_proof.json')
LIL_VIEW=Path('work/analysis/lil_opening_references_v1709/actual_visual_review.json')

if __name__=='__main__':
    assert not ROOT.exists()and not DOC.exists()and not MAP.exists()
    doc,plan,font,fe,refs,actual,lil,lilview=map(read,(OLD,PLAN,FONT,FE,REF,ACTUAL,LIL,LIL_VIEW))
    assert len(doc['records'])==73 and len(font['cases'])==67 and not font['failures']and font['native_macro_calls']==540
    assert len(fe['cases'])==6 and not fe['failures']and fe['exact_original_null_actor_macro_calls']==48
    assert font['manuscript_sha256']==fe['manuscript_sha256']==sha(OLD.read_bytes())
    assert plan['all171_typed_commands24_relative_sites360_native_cases']and plan['all73_final_parity_native_planes_exact']
    assert plan['all_three_current_blocks_restore_exactly']and plan['all322_other_blocks_other_files_and_components_exact']
    assert refs['all171_clean_current_target_commands24_relative_sites360_native_cases_bound']and refs['all325_original_loads_and650_parent_modes_each_ROM']
    assert refs['every_current_and_target_executable_unit_exact_prior_census']
    assert actual['research_ROM_sha256']==plan['research_ROM_sha256']and actual['all37_opening_speeches93_commands_and_town_return']
    assert actual['complete_matching_speech_panels']==actual['complete_matching_speech_holds']==37
    assert not actual['unmatched_capture_planes_no_full_pixel_claim']and actual['actual_Hodram_Gerhard_Charles_Manuel_and_FE_complete_native_planes_match']
    assert actual['no_save_savestate_location_RNG_funds_crew_outcome_or_event_fixture']
    assert lil['ARM9_sha256']==plan['ARM9_sha256']and lilview['source_actual_proof_sha256']==sha(LIL.read_bytes())
    assert lilview['source_speakers_native_nameplates_full_letters_left_origins_and_pagination_acceptable']
    parent,target,clean=map(NdsImage.open,(plan['parent'],plan['research_ROM'],'work/clean.nds'))
    original=IlnkContainer.parse(clean.read_file('/data/SC1.DK4')).blocks
    source=IlnkContainer.parse(parent.read_file('/data/SC1.DK4')).blocks
    dependencies={str(p):sha(p.read_bytes())for p in(OLD,PLAN,FONT,FE,REF,ACTUAL,LIL,LIL_VIEW,Path(__file__),
        Path('scripts/probe_hodram_opening_fonts_v2021.py'),Path('scripts/probe_hodram_opening_FE_v2022.py'),
        Path('scripts/research_hodram_opening_v2023.py'),Path('scripts/verify_hodram_opening_loader_v2024.py'),
        Path('scripts/run_hodram_opening_revised_v2025.py'),Path('scripts/run_hodram_opening_context_v2018.py'),
        Path('scripts/verify_hodram_opening_references_v2026.py'),Path('scripts/audit_hodram_opening_actual_v2027.py'),
        Path('scripts/audit_hodram_opening_actual_v2027d.py'),Path(doc['source_packet']),
        Path('dk4tool/dialogue/codec.py'),Path('dk4tool/dialogue/encoder.py'),Path('dk4tool/dialogue/layout.py'),
        Path('dk4tool/dialogue/profiles.py'),Path('dk4tool/dialogue/review.py'))}
    dependencies.update(actual['evidence'])
    for case in font['cases']+fe['cases']:dependencies[case['preview']]=case['preview_sha256']
    for sheet in font['review_sheets']:dependencies[sheet['path']]=sheet['sha256']
    for p in actual['representative_contact_sheets']+[str(Path(FE).parent/'six_FE_review_sheet.png')]:dependencies[p]=sha(Path(p).read_bytes())
    for p,digest in dependencies.items():assert sha(Path(p).read_bytes())==digest,p
    ROOT.mkdir(parents=True);scope=ROOT/'source_bound_presentation_macro_and_visual_contract.json'
    save(scope,dict(ARM9_sha256=plan['ARM9_sha256'],source_blocks_sha256={str(b):sha(source[b])for b in(42,43,44)},
        clean_and_current_complete_speech_preambles_equal=True,progressive_speaker_bytes=[1,2,9,16,18,23],
        high_progressive_speaker_bytes=[16,18,23],FE_owned_by_separate_original_mode1_consumer=True,
        actual_Hodram_Gerhard_Charles_Manuel_portraits_full_nameplates_and37_complete_panels_viewed=True,
        exact_runtime_Lil_Camille_source02_09_live_controls_inherited=True,
        native_selector_same_on_current_route1_all_six_actors_and_isolated_catalog_names_verified=True,
        macro_ascii_lengths={'FI':6,'FA':9,'FO':15},native_macro_outputs=font['actual_measured_FI_FA_FO'],
        all67_progressive_planes540_macro_calls_and_six_FE_planes48_null_actor_calls_pass=True,
        all73_final_parity_native_planes_exact=True,native_literal_guard_F_I_and_source_substitutions_preserved=True,
        all9_progressive_and1_FE_preview_sheets_and7_actual_sheets_viewed=True,
        ordinary_revised_opening_normal_Stockholm_return_and_current_departure_context_verified=True,
        B43_B44_source_prose_and_native_reference_complete_but_not_gameplay_visits=True,
        B135_B127_observed_context_unreviewed_no_editorial_credit=True,
        one_B43_R0068_weak_wrap_heuristic_justified_no_hard_gate_waived=True,
        source_bound_private_profiles_only_global_profiles_unchanged=True,evidence=dependencies,
        not_full_route_or_hardware_proof=True,full_goal_complete=False))
    dependencies[str(scope)]=sha(scope.read_bytes())
    fonts={r['id']:r for r in font['cases']};papers={r['id']:r for r in fe['cases']}
    targets={r['id']:r for b in plan['blocks']for r in b['text_records']}
    for row in doc['records']:
        t=targets[row['id']];assert re.findall('FI|FA|FO',row['source_Japanese'])==re.findall(r'\{MACRO:(FI|FA|FO)\}',row['english'])
        row['english']=row['english'].removesuffix('{PAD}');row['review']['formatting']=True
        row['target_command_offset']=t['new_command_offset'];row['target_record_index']=t['new_record_index'];row['target_native_command_hex']=t['target_hex']
        row['native_display_proof']=deepcopy(papers[row['id']]if t['separate_FE_modal']else fonts[row['id']])
        row['actual_gameplay_coverage']='complete-native-matching-revised-opening-panel'if row['block']==42 else'offline-native-complete-no-actual-scene-visit-claimed'
        if row['block']==42:row['actual_panel_proof']=next(r for r in actual['observed_speech_panels']if r['id']==row['id'])
        if row['id']=='DK4_MES_B43_R0068':
            row['qa_waivers']=['weak-line-ending']
            row['qa_waiver_reason']='The first row ends with a and the next continues contract within one complete three-row paragraph. The wartime rival-contract condition remains explicit. The complete native plane was viewed, all glyphs and page consumption pass. This narrow wrap preference is accepted; no bounds,control,macro,parity or capacity gate is waived. No actual B43 visit is claimed.'
    doc.update(encoder='dialogue-relocatable-v1',dialogue_profile='hodram-story-live',scoped_native_profile='hodram-opening-editorial-native-v1',
        formatting_review_pending=False,draft_only_not_formatting_or_release_authorized=False,
        source_bound_runtime_profile_proof=str(scope),native_font_proof=str(FONT),native_FE_proof=str(FE),actual_representative_proof=str(ACTUAL),
        supersedes=str(OLD),superseded_manuscript_sha256=sha(OLD.read_bytes()),remaining_gates=['Registered cumulative integration and exact clean-input patch.'],
        formatting_contract='Exact three blocks/native runtime. Whole six-byte preambles,private progressive selector16/18/23,measured6/9/15 macros,balanced automatic protected pair-safe wrapping. FE retains its separate mode1 consumer and verified full228x48 plane. No authored wrapping or allocation-driven shortening.',
        editorial_completion_not_granted_until_registered_integration=True)
    validate_natural_dialogue_batch(doc);save(DOC,doc);dependencies[str(DOC)]=sha(DOC.read_bytes())
    mapping=deepcopy(plan)
    for b in mapping['blocks']:b['clean_block_sha256']=sha(original[b['block']])
    mapping.update(format='dk4-hodram-opening-source-relocation-map-v1',file_path='/data/SC1.DK4',entry_point_offset=8,
        source_SC1_sha256=plan['source_SC1_sha256'],external_references_complete=True,preserve_record_parity=True,
        all_native_formatting_typed_reference_and_representative_actual_gates_pass=True,
        loader_external_entry_actual_revised_and_registered_release_pending=False,registered_integration_and_clean_patch_pending=True,
        source_bound_profile_contract=str(scope),source_bound_profile_contract_sha256=sha(scope.read_bytes()),approved_manuscript=str(DOC),
        B43_B44_offline_only_no_actual_visit_claim=True,evidence=dependencies)
    save(MAP,mapping)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        scope=str(scope),scope_sha256=sha(scope.read_bytes()),speeches=73,revisions=38,retentions=35,
        full_native_source_reference_and_practical_representative_actual_gates_pass=True,
        B43_B44_actual_visits_not_required_or_claimed=True,registration_clean_patch_and_completion_ledger_pending=True,
        no_ROM_registry_baseline_or_promotion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(approved=73,revisions=38,retentions=35,actual_matching_panels=37,registered=False))
