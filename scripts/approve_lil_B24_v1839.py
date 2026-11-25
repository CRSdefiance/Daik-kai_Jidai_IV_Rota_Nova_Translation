"""Approve exact B24 references after all13 actual panels and normal return."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_approval_v1839')
MAP=Path('translations/lil_trade_routes_editorial_relocation_map_v1.json')
DOC=Path('translations/lil_trade_routes_officers_editorial_manuscript_v4.json')
PRIOR=Path('translations/lil_trade_routes_officers_editorial_manuscript_v3.json')
ACTUAL=Path('work/analysis/lil_B24_actual_v1838/complete_B24_scene_and_two_coordinate_fixture_audit.json')
CENSUS=Path('work/analysis/lil_B24_reference_census_v1835/complete_shipped_entry_and17_mapped_command_census.json')
RELOC=Path('work/analysis/lil_B24_relocation_v1828/parity_and17_native_command_research.json')

if __name__=='__main__':
    assert not ROOT.exists()and not MAP.exists()and not DOC.exists()
    actual,census,reloc,doc=map(read,(ACTUAL,CENSUS,RELOC,PRIOR))
    assert actual['all13_speeches26_actual_complete_native_independent_holds']
    assert actual['all_readonly_callbacks_zero_errors_mismatches_host_restored']
    assert census['all17_native_commands_reexecuted_clean_current_and_research']
    assert actual['candidate_sha256']==census['research_ROM_sha256']
    assert actual['terminal_frame']==47650 and len(actual['all17_original_command_pairs'])==17
    assert {r['id']for r in actual['speeches']}=={r['id']for r in doc['records']}
    ROOT.mkdir(parents=True)
    visual={'both_actual_sheets_all13_panels_and_normal_Amsterdam_return_actually_viewed':True,
        'all13_portraits_nameplates_complete_text_first_last_letters_and_left_row_origins_reviewed':True,
        'all13_actual_individual_activations_no_equivalence_substitutions':True,
        'native_17_commands_and26_complete_actual_holds_pass':True,
        'two_disclosed_each16_byte_coordinate_fixtures_not_earned_travel':True,
        'no_full_route_or_hardware_claim':True,'full_goal_complete':False,
        'evidence':{str(ACTUAL):sha(ACTUAL.read_bytes()),**{p:sha(Path(p).read_bytes())for p in actual['review_sheets']}}}
    visual_path=ROOT/'actual_visual_review.json';save(visual_path,visual)
    mapping={'format':'dk4-lil-trade-routes-source-relocation-map-v1','file_path':'/data/SC2.DK4','block':24,
        'source_block_sha256':reloc['old_block_sha256'],'target_block_sha256':reloc['target_block_sha256'],
        'required_runtime_ARM9_sha256':reloc['ARM9_sha256'],'entry_point_offset':8,
        'external_references_complete':True,'preserve_record_parity':True,'parity_mismatch_policy':'append-single-space',
        'source_logical_end':reloc['old_logical_end'],'target_logical_end':reloc['new_logical_end'],
        'records':reloc['texts'],'commands':reloc['all17_commands'],
        'native_call_census':census['original_interpreter_entry_census'],
        'only_SC2_block_index_entry_no_interior_target_and_no_relative_operands':True,
        'all17_original_commands_all13_actual_speeches_and_normal_return_verified':True,
        'inverse_reconstruction_every_original_logical_byte_exact':True,
        'evidence':{str(p):sha(p.read_bytes())for p in (ACTUAL,CENSUS,RELOC,visual_path)},
        'scope':'Exact shipped B24,original runtime andsource-bound loaders. Native structural walk bridges opaque effects;actual13 confirms this one complete scene. Not all routes or hardware.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(MAP,mapping)
    successor=deepcopy(doc);successor.update(encoder='dialogue-relocatable-v1',status='all13-source-native-actual-reviewed;registered-integration-pending',
        required_runtime_ARM9_sha256=reloc['ARM9_sha256'],source_relocation_map=str(MAP),
        source_relocation_map_sha256=sha(MAP.read_bytes()),predecessor_manuscript=str(PRIOR),
        predecessor_manuscript_sha256=sha(PRIOR.read_bytes()),actual_visual_review=str(visual_path))
    fonts={r['id']:r for r in read(doc['native_font_proof'])['cases']}
    for row in successor['records']:
        row['english']=row['english'].removesuffix('{PAD}')
        row['compiled_hex']=fonts[row['id']]['encoded_hex']
        assert all(row['review'].values())
    validate_natural_dialogue_batch(successor);save(DOC,successor)
    save(ROOT/'approval_receipt.json',{'reference_map':str(MAP),'reference_map_sha256':sha(MAP.read_bytes()),
        'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),'registered_release_pending':True,
        'all13_individual_actual_speeches_and17_command_returns':True,'full_goal_complete':False})
    print({'approved_B24_reference_map':True,'reviewed_individual_actual_lines':13,'registered_integration_pending':True},flush=True)
