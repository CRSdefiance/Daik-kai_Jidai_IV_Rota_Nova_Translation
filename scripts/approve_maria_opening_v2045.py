"""Approve all38 complete source/native/actual panels without completion credit yet."""
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_opening_approval_v2045')
OLD=Path('translations/maria_opening_contextual_editorial_manuscript_v1.json')
DOC=Path('translations/maria_opening_contextual_editorial_manuscript_v2.json')
MAP=Path('translations/maria_opening_editorial_relocation_map_v1.json')
PLAN=Path('work/analysis/maria_opening_relocation_v2040/complete_B33_CS0101_typed_relocation_research.json')
FONT=Path('work/analysis/maria_opening_fonts_v2037c/all38_progressive_native_macros_and_complete_font_planes.json')
CONTROL=Path('work/analysis/maria_opening_controls_v2039/six_source_bound_native_controls_and_catalog.json')
REF=Path('work/analysis/maria_opening_references_v2043/B33_CS0101_mapping_and_inherited_executable_entry_census.json')
ACTUAL=Path('work/analysis/maria_opening_actual_v2044/ordinary_current_revised_opening_and_full_actual_planes.json')
if __name__=='__main__':
    assert not ROOT.exists()and not DOC.exists()and not MAP.exists()
    doc,plan,font,control,refs,actual=map(read,(OLD,PLAN,FONT,CONTROL,REF,ACTUAL))
    assert len(doc['records'])==len(font['cases'])==38 and not font['failures']and font['native_macro_calls']==308
    assert font['manuscript_sha256']==plan['manuscript_sha256']==sha(OLD.read_bytes())
    assert all(not any(i['severity']in('error','warning')for i in c['qa']['issues'])for c in font['cases'])
    assert plan['all85_typed_commands_and38_final_native_planes_exact']and plan['exact_inverse_restores_current_block']
    assert plan['CS0101_header_and_all47_non_speech_commands_exact']and not plan['relative_skip_fixups']
    assert refs['all303_loads606_parent_modes_each_ROM']and refs['every_current_target_executable_unit_exact_prior_census']
    assert actual['research_ROM_sha256']==plan['research_ROM_sha256']and actual['all38_speeches85_commands_and_normal_Hangzhou_return']
    assert actual['complete_matching_speech_panels']==actual['complete_matching_speech_holds']==38 and not actual['unmatched_capture_planes_no_full_pixel_claim']
    assert actual['existing_isolated_system_unlock_save_not_earned_and_no_savestate_story_location_RNG_funds_outcome_fixture']
    assert control['ARM9_sha256']==plan['ARM9_sha256']and len(control['controls'])==6 and control['exact_0A_speech_preamble_is_Xien_not_leading_text_LF']
    image=NdsImage.open(plan['parent']);clean=NdsImage.open('work/clean.nds');source=IlnkContainer.parse(image.read_file('/data/SC3.DK4')).blocks[33]
    original=IlnkContainer.parse(clean.read_file('/data/SC3.DK4')).blocks[33];assert source[:4]==original[:4]==b'CS\1\1'
    dependencies={str(p):sha(p.read_bytes())for p in(OLD,PLAN,FONT,CONTROL,REF,ACTUAL,Path(__file__),Path(doc['source_packet']),
        Path('scripts/review_maria_opening_v2036.py'),Path('scripts/probe_maria_opening_fonts_v2037.py'),Path('scripts/probe_maria_opening_fonts_v2037c.py'),
        Path('scripts/prove_maria_opening_controls_v2039.py'),Path('scripts/research_maria_opening_v2040.py'),Path('scripts/verify_maria_opening_loader_v2041.py'),
        Path('scripts/run_maria_opening_context_v2035.py'),Path('scripts/run_maria_opening_revised_v2042.py'),
        Path('scripts/verify_maria_opening_references_v2043.py'),Path('scripts/audit_maria_opening_actual_v2044.py'),
        Path('dk4tool/dialogue/codec.py'),Path('dk4tool/dialogue/encoder.py'),Path('dk4tool/dialogue/layout.py'),Path('dk4tool/dialogue/profiles.py'),Path('dk4tool/dialogue/review.py'))}
    dependencies.update(actual['evidence'])
    for r in font['cases']:dependencies[r['preview']]=r['preview_sha256']
    for r in font['review_sheets']:dependencies[r['path']]=r['sha256']
    for r in control['controls']:dependencies[r['actual_current_capture']]=r['capture_sha256']
    for p in actual['representative_contact_sheets']+[control['review_sheet']]:dependencies[p]=sha(Path(p).read_bytes())
    for p,digest in dependencies.items():assert sha(Path(p).read_bytes())==digest,p
    ROOT.mkdir(parents=True);scope=ROOT/'source_bound_presentation_macro_and_visual_contract.json'
    save(scope,dict(ARM9_sha256=plan['ARM9_sha256'],source_block_sha256=sha(source),clean_block_sha256=sha(original),
        clean_current_complete_six_byte_preambles_and_CS0101_equal=True,progressive_speaker_bytes=[3,10,11,12,21,74],
        private_explicit_leading_speaker_bytes=[10,21,74],source0A_is_Xien_actor_not_text_LF=True,
        all_six_actual_portraits_complete_nameplates_and38_body_panels_viewed=True,
        native_selectors_and_isolated_copy_full_catalog_names_verified=True,
        macro_ascii_lengths={'FI':5,'FA':2,'FO':7},native_macro_outputs=font['actual_measured_FI_FA_FO'],
        all38_logical_wrapped_macros_four_alignments308_calls_and_all4MiB_ABI_guards_pass=True,
        all38_complete_native_independent_planes_and_final_parity_equal=True,
        all5_native_and7_actual_review_sheets_viewed_no_warnings_or_waivers=True,
        native_literal_guard_and_source_runtime_substitutions_preserved=True,
        CS0101_85_commands47_opaque_commands303_loads606_parent_modes_exact=True,
        actual_original_and_revised38_speeches85_commands_normal_Hangzhou_return=True,
        existing_system_unlock_save_not_earned_no_story_location_RNG_funds_outcome_or_savestate_fixture=True,
        following_palace_trader_tavern_bar_drink_context_unreviewed_no_editorial_credit=True,
        private_profile_only_global_Maria_profile_and_other_routes_unchanged=True,evidence=dependencies,
        not_full_route_or_hardware_proof=True,full_goal_complete=False))
    dependencies[str(scope)]=sha(scope.read_bytes());fonts={r['id']:r for r in font['cases']};targets={r['id']:r for r in plan['text_records']}
    for row in doc['records']:
        native=targets[row['id']];assert re.findall('FI|FA|FO',row['source_Japanese'])==re.findall(r'\{MACRO:(FI|FA|FO)\}',row['english'])
        row['english']=row['english'].removesuffix('{PAD}');row['review']['formatting']=True
        row['target_command_offset']=native['new_command_offset'];row['target_record_index']=native['new_record_index'];row['target_native_command_hex']=native['target_hex']
        row['native_display_proof']=deepcopy(fonts[row['id']]);row['actual_panel_proof']=next(r for r in actual['observed_speech_panels']if r['id']==row['id'])
    doc.update(encoder='dialogue-relocatable-v1',dialogue_profile='maria-story-shared-events-live',scoped_native_profile='maria-opening-editorial-native-v1',
        formatting_review_pending=False,draft_only_not_formatting_or_release_authorized=False,source_bound_runtime_profile_proof=str(scope),
        native_font_proof=str(FONT),actual_representative_proof=str(ACTUAL),supersedes=str(OLD),superseded_manuscript_sha256=sha(OLD.read_bytes()),
        remaining_gates=['Registered cumulative integration and exact clean-input patch.'],
        formatting_contract='Exact CS0101 B33/native runtime. Whole six-byte preambles own allselectors,includingXien0A. Privateprofile extends only10/21/74 andusesmeasured5/2/7 macros,balanced protected pair-safe automatic wrapping. All38 actualpanels complete;globalprofiles unchanged.',
        editorial_completion_not_granted_until_registered_integration=True)
    validate_natural_dialogue_batch(doc);save(DOC,doc);dependencies[str(DOC)]=sha(DOC.read_bytes())
    spec={k:deepcopy(plan[k])for k in('block','source_block_sha256','target_block_sha256','old_bytes','new_bytes','target_hex','text_records','mapped_native_commands','relative_skip_fixups')}
    spec['clean_block_sha256']=sha(original)
    mapping=dict(format='dk4-maria-opening-source-relocation-map-v1',file_path='/data/SC3.DK4',blocks=[spec],entry_point_offset=8,
        source_SC3_sha256=plan['source_SC3_sha256'],target_SC3_sha256=plan['target_SC3_sha256'],
        research_ROM=plan['research_ROM'],research_ROM_sha256=plan['research_ROM_sha256'],external_references_complete=True,preserve_record_parity=True,
        all_native_formatting_typed_reference_and_representative_actual_gates_pass=True,registered_integration_and_clean_patch_pending=True,
        source_bound_profile_contract=str(scope),source_bound_profile_contract_sha256=sha(scope.read_bytes()),approved_manuscript=str(DOC),evidence=dependencies)
    save(MAP,mapping)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        scope=str(scope),scope_sha256=sha(scope.read_bytes()),speeches=38,revisions=23,retentions=15,
        all_native_reference_and_practical_actual_gates_pass=True,no_warnings_or_waivers=True,registration_clean_patch_and_completion_ledger_pending=True,
        no_ROM_registry_baseline_or_promotion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(approved=38,revisions=23,retentions=15,actual_matching_panels=38,registered=False))
