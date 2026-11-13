"""Approve the source/native map after both ordinary choice transitions.

This does not register,build,promote or count an editorial completion.
"""
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/rafael_opening_approval_v2010')
OLD=Path('translations/rafael_opening_contextual_editorial_manuscript_v2.json')
DOC=Path('translations/rafael_opening_contextual_editorial_manuscript_v3.json')
OLD_CHOICES=Path('translations/rafael_opening_contextual_choices_editorial_draft_v1.json')
CHOICES=Path('translations/rafael_opening_contextual_choices_editorial_draft_v2.json')
MAP=Path('translations/rafael_opening_editorial_relocation_map_v1.json')
PLAN=Path('work/analysis/rafael_opening_relocation_v2001b/current_B44_typed_relocation_research.json')
FONT=Path('work/analysis/rafael_opening_fonts_v1998/all114_progressive_native_macros_and_complete_font_planes.json')
FE=Path('work/analysis/rafael_money_FE_v2005/unchanged_money_notice_native_modal_proof.json')
MENU=Path('work/analysis/rafael_opening_choices_v2004/typed_choice_VM_geometry_and_complete_native_pixels.json')
REFERENCES=Path('work/analysis/rafael_opening_references_v2006/complete_B44_mapping_and_inherited_executable_entry_census.json')
ACTUAL1=Path('work/analysis/rafael_independent_actual_v2007e/independent_preparation_and_normal_Lisbon_return.json')
ACTUAL0=Path('work/analysis/rafael_guided_actual_v2009/guided_preparation_repaired_outer_skip_and_Lisbon_return.json')

if __name__=='__main__':
    assert not ROOT.exists()and not DOC.exists()and not CHOICES.exists()and not MAP.exists()
    doc,menu,plan,font,fe,choice,refs,actual1,actual0=map(read,(OLD,OLD_CHOICES,PLAN,FONT,FE,MENU,REFERENCES,ACTUAL1,ACTUAL0))
    assert len(doc['records'])==115 and len(menu['records'])==2
    assert len(font['cases'])==114 and font['native_macro_calls']==916 and not font['failures']
    assert all(p['manuscript_sha256']==sha(OLD.read_bytes())for p in(font,fe))
    assert choice['manuscript_sha256']==sha(OLD_CHOICES.read_bytes())
    assert actual0['research_ROM_sha256']==actual1['research_ROM_sha256']==plan['research_ROM_sha256']
    assert actual0['actual_repaired_outer0100_length72_and_cleanup6742']
    assert actual1['actual_choice1_result_2_1_and_repaired0300_jump_to6674']
    assert actual0['both_guided_instructions_four_holds_complete_native_actual_ink']
    assert actual1['revised_R0479_two_holds_complete_native_actual_pixels']
    assert actual1['unchanged_FE_money_notice_actual_complete_native_mode1_ink']
    assert actual0['union_complete_matching_panel_samples']==107 and actual0['union_complete_matching_panel_holds']==111
    assert actual0['both_actual_branches_union115_source_speeches']
    assert actual0['normal_Lisbon_town_ID']==actual1['normal_Lisbon_town_ID']==11
    assert refs['all182_clean_current_target_typed_commands_and4_relative_sites_bound']
    assert refs['all343_original_loads_and686_parent_modes_each_ROM']
    assert refs['every_current_and_target_executable_unit_exact_prior_census']
    assert plan['all114_final_parity_native_planes_exact']and plan['exact_inverse_restores_actual_current_source_including_old_stale_span']
    assert choice['three_native_selection_cancel_cases_pass']and len(choice['four_complete_native_style_label_planes'])==4
    assert fe['one_page_full_target_and_terminal_pointer_exact']and fe['complete_native_independent_plane_and_all_glyphs_bounds']
    dependencies={str(p):sha(p.read_bytes())for p in(OLD,OLD_CHOICES,PLAN,FONT,FE,MENU,REFERENCES,ACTUAL1,ACTUAL0,Path(__file__),
        Path('scripts/native_storyline_walk_v1995.py'),Path('scripts/census_native_storylines_v1995.py'),
        Path('scripts/preflight_rafael_opening_v1996.py'),Path('scripts/probe_rafael_opening_fonts_v1998.py'),
        Path('scripts/research_rafael_opening_v2001.py'),Path('scripts/research_rafael_opening_v2001b.py'),
        Path('scripts/verify_rafael_opening_loader_v2002.py'),Path('scripts/prove_rafael_opening_choices_v2004.py'),
        Path('scripts/probe_rafael_money_FE_v2005.py'),Path('scripts/verify_rafael_opening_references_v2006.py'),
        Path('scripts/audit_rafael_independent_v2007e.py'),Path('scripts/audit_rafael_guided_v2009.py'),
        Path('dk4tool/dialogue/codec.py'),Path('dk4tool/dialogue/encoder.py'),Path('dk4tool/dialogue/layout.py'),
        Path('dk4tool/dialogue/profiles.py'),Path('dk4tool/dialogue/review.py'))}
    for p in(font['source_report'],font['snapshot']['path'],actual1['capture_report'],actual1['observer_report'],actual0['capture_report'],actual0['observer_report']):
        dependencies[p]=sha(Path(p).read_bytes())
    for r in font['cases']:
        dependencies[r['preview']]=r['preview_sha256']
    for r in font['review_sheets']:dependencies[r['path']]=r['sha256']
    for p in actual1['representative_contact_sheets']+[fe['preview'],choice['preview']]:dependencies[p]=sha(Path(p).read_bytes())
    for r in actual1['observed_speech_panels']:
        for hold in r['holds']:dependencies[hold['capture']]=hold['capture_sha256']
    for r in actual0['focused_guided_holds']:
        for hold in r['holds']:dependencies[hold['capture']['path']]=hold['capture']['sha256']
    for p,digest in dependencies.items():assert sha(Path(p).read_bytes())==digest,p
    parent,target,clean=map(NdsImage.open,(plan['parent'],plan['research_ROM'],'work/clean.nds'))
    source_block=IlnkContainer.parse(parent.read_file('/data/SC0.DK4')).blocks[44]
    clean_block=IlnkContainer.parse(clean.read_file('/data/SC0.DK4')).blocks[44]
    target_block=IlnkContainer.parse(target.read_file('/data/SC0.DK4')).blocks[44]
    assert sha(source_block)==plan['source_block_sha256']and sha(target_block)==plan['target_block_sha256']
    ROOT.mkdir(parents=True)
    scope=ROOT/'source_bound_presentation_macro_and_visual_contract.json'
    save(scope,dict(ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),source_block_sha256=sha(source_block),clean_block_sha256=sha(clean_block),
        target_block_sha256=sha(target_block),clean_and_current_complete_speech_preambles_equal=True,
        progressive_speaker_bytes=[0,4,5,6],default_actor_selectors=[0,4,5,6],
        actual_Rafael_Janus_Claudio_Julio_portraits_and_complete_nameplates_viewed=True,
        native_default_macro_outputs={'FI':'Rafael','FA':'Castor','FO':'Castor Co.'},macro_ascii_lengths={'FI':6,'FA':6,'FO':10},
        all114_logical_and_wrapped_macro_inputs_four_alignments_all4MiB_ABI_guards_pass=True,
        native_literal_guard_F_and_I_preserves_real_macros_and_forbids_IC_I_control_suffix_collisions=True,
        native_font_planes114_and_all15_review_sheets_viewed=True,
        all114_final_parity_native_planes_equal_reviewed_planes=True,
        source00_actor_byte_owned_by_whole_native_preamble_not_NUL_text_formatter=True,
        FE_original_separate_mode1_228x48_paper_actual_money_notice_verified=True,
        two_original_choice_labels_four_native_styles_and_actual_complete_ink_holds_verified=True,
        both_ordinary_controller_choices_repaired_skips_and_normal_Lisbon_returns_verified=True,
        complete_actual_panel_samples107_holds111_separate_from115_executed_speech_union=True,
        no_fresh_per_panel_actual_pixel_claim_for_other8_early_speeches=True,
        global_profiles_unchanged_private_B44_profile_only=True,not_full_route_or_hardware_proof=True,
        evidence=dependencies,full_goal_complete=False))
    dependencies[str(scope)]=sha(scope.read_bytes())
    by_ID={r['id']:r for r in font['cases']};targets={r['id']:r for r in plan['text_records']}
    doc=deepcopy(doc)
    for row in doc['records']:
        ident=row['id'];native=targets[ident]
        assert re.findall('FI|FA|FO',row['source_Japanese'])==re.findall(r'\{MACRO:(FI|FA|FO)\}',row['english'])
        row['english']=row['english'].removesuffix('{PAD}');row['review']['formatting']=True
        row['target_native_command_hex']=native['target_hex'];row['target_command_offset']=native['new_command_offset']
        row['target_record_index']=native['new_record_index']
        if row['source_presentation_prefix_hex']=='fe':
            row['native_display_proof']=dict(separate_FE_modal_proof=str(FE),actual_money_notice_proof=str(ACTUAL1),target_unchanged_exact=True)
        else:
            case=by_ID[ident];row['native_display_proof']=case
            for issue in case['qa']['issues']:
                if issue['severity']!='warning':continue
                assert ident=='DK4_MES_B44_R0327'and issue['code']=='weak-line-ending'
                row['qa_waivers']=['weak-line-ending']
                row['qa_waiver_reason']='The second row ends with the and the third continues fleet in one complete four-row paragraph. All three explicit roles and all macros stay in source order. Exact native and actual pixels at31920 show the whole paragraph with no clipped,missing or orphaned glyph. This narrow prose-wrap heuristic is accepted; no control,parity,bounds or capacity gate is waived.'
    doc.update(encoder='dialogue-relocatable-v1',dialogue_profile='raphael-story-live',
        scoped_native_profile='rafael-opening-editorial-native-v1',source_bound_runtime_profile_proof=str(scope),
        formatting_review_pending=False,draft_only_not_registered_or_formatting_approved=False,
        native_font_proof=str(FONT),native_FE_proof=str(FE),actual_choice1_proof=str(ACTUAL1),actual_choice0_proof=str(ACTUAL0),
        required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),
        formatting_contract='Whole native speech command owns speaker00. The source-bound private Rafael formatter uses measured6/6/10 substitutions,the inherited native literal guard,balanced automatic wrapping,protected breaks and pair phase. FE is preserved as exact original separate-modal bytes. Default global profile remains unchanged.',
        supersedes=str(OLD),superseded_manuscript_sha256=sha(OLD.read_bytes()),
        no_new_gameplay_display_or_editorial_completion_credit=False,editorial_completion_not_granted_until_registered_integration=True))
    validate_natural_dialogue_batch(doc);save(DOC,doc)
    menu=deepcopy(menu)
    for row in menu['records']:row['review']['formatting']=True
    menu.update(formatting_review_pending=False,draft_only_not_registered_or_formatting_approved=False,
        native_choice_proof=str(MENU),actual_complete_choice_labels_proof=str(ACTUAL1),
        supersedes=str(OLD_CHOICES),superseded_manuscript_sha256=sha(OLD_CHOICES.read_bytes()))
    validate_natural_dialogue_batch(menu);save(CHOICES,menu)
    dependencies[str(DOC)]=sha(DOC.read_bytes());dependencies[str(CHOICES)]=sha(CHOICES.read_bytes())
    mapping={**deepcopy(plan),'format':'dk4-rafael-opening-source-relocation-map-v1','block':44,'entry_point_offset':8,
        'external_references_complete':True,'preserve_record_parity':True,'source_bound_profile_contract':str(scope),
        'source_bound_profile_contract_sha256':sha(scope.read_bytes()),'clean_block_sha256':sha(clean_block),
        'approved_manuscript':str(DOC),'approved_choices':str(CHOICES),
        'all_native_formatting_typed_reference_and_both_actual_choice_gates_pass':True,
        'external_entry_loader_and_actual_scene_proofs_pending':False,'FE_and_choices_final_display_proofs_pending':False,
        'registered_integration_and_clean_patch_pending':True,'evidence':dependencies}
    save(MAP,mapping)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choices=str(CHOICES),choices_sha256=sha(CHOICES.read_bytes()),
        map=str(MAP),map_sha256=sha(MAP.read_bytes()),scope=str(scope),scope_sha256=sha(scope.read_bytes()),
        speeches115_choices2_revisions33_retentions84=True,all_native_reference_and_both_actual_transition_checks_pass=True,
        source00_controls_and_two_inherited_skip_repairs_explicit=True,one_source_bound_R0327_wrap_warning_narrowly_justified=True,
        production_compiler_registration_clean_patch_and_completion_ledger_still_pending=True,
        no_ROM_patch_registry_baseline_or_promotion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(approved_speeches=115,choices=2,revisions=33,retentions=84,registered=False,completed=False))
