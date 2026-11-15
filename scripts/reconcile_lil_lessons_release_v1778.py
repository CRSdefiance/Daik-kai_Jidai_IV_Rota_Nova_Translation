"""Bind all targeted lesson paths, original controls and startup to V1775."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_lessons_release_v1774')
OUT=ROOT/'targeted_gameplay_and_startup_reconciliation.json'
MAP=Path('translations/lil_lessons_editorial_relocation_map_v1.json')
WIND=Path('work/analysis/lil_revised_wind_v1744/actual_revised_wind_branch_proof.json')
FULL=Path('work/analysis/lil_crew_scene_v1763_final/complete_B23_scene_and_fixture_audit.json')
DECLINE=Path('work/analysis/lil_crew_decline_v1767_decline/complete_B23_scene_and_fixture_audit.json')
DEFAULT=Path('work/analysis/lil_sailing_choice0_audit_v1772/complete_B120_choice0_scene_audit.json')

if __name__=='__main__':
    assert not OUT.exists()
    release=read(ROOT/'registered_release_verification.json');rom=Path(release['candidate']);digest=sha(rom.read_bytes())
    assert digest==release['candidate_sha256'] and release['complete_reconstruction_byte_exact']
    image=NdsImage.open(rom);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    mapping=read(MAP);assert mapping['external_references_complete'] and mapping['individual_actual_speech_count']==55
    all_ids={r['id']for b in mapping['blocks']for r in b['text_records']};actual={};paths=[]
    for path,block_number,expected_count,command_key,expected_commands in [
        (WIND,120,22,'all41_original_command_pairs_mapped_and_same_path_results',41),
        (FULL,23,30,'all_original_B23_command_pairs_and_mapped_branches_verified',46),
        (DECLINE,23,4,'all_original_B23_command_pairs_and_mapped_branches_verified',9),
        (DEFAULT,120,14,'all30_original_B120_command_pairs_and_mapped_branches_verified',30)]:
        proof=read(path);tested=Path(proof['research_ROM']);assert sha(tested.read_bytes())==proof['research_ROM_sha256']
        target=NdsImage.open(tested)
        assert target.read_file('/__arm9__.bin')==arm
        assert IlnkContainer.parse(target.read_file('/data/SC2.DK4')).blocks[block_number]==blocks[block_number]
        speeches=proof.get('speeches',proof.get('all22_executed_speeches44_holds_complete_native_independent_actual_pixels'))
        assert len(speeches)==expected_count and len(proof[command_key])==expected_commands
        assert proof[command_key][-1]['result_words'][0]==0
        for row in speeches:
            ident=row['id'];holds=row['two_complete_actual_holds']
            assert len(holds)==2 and ident in all_ids
            for hold in holds:assert sha(Path(hold['capture']).read_bytes())==hold['capture_sha256']
            actual.setdefault(ident,[]).append({'proof':str(path),'holds':holds,'same_target_block_and_runtime_verified':True})
        paths.append({'proof':str(path),'proof_sha256':sha(path.read_bytes()),'block':block_number,
            'individual_speeches':expected_count,'complete_holds':expected_count*2,'native_command_pairs':expected_commands,
            'tested_ROM':str(tested),'tested_ROM_sha256':proof['research_ROM_sha256'],
            'whole_ROM_identical_to_registered_candidate':tested.read_bytes()==rom.read_bytes(),
            'exact_target_block_and_entire_runtime_match_registered':True,
            'disclosed_fixture':'one16-byte coordinate-only Bruges fixture' if block_number==23 else 'none'})
    assert len(actual)==55 and all_ids-set(actual)=={r['id']for r in mapping['unvisited_conditional_records']}
    startup=read(ROOT/'ordinary_startup_verification.json')
    assert startup['candidate_sha256']==digest and startup['all8_complete_startup_title_NewGame_frames_exact']
    assert startup['no_battery_save_savestate_or_fixtures'] and len(startup['pairs'])==8
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    prior=read('work/analysis/lil_opening_terminal_v1713b/terminal_scene_and_registered_ROM_reconciliation.json')
    previous=NdsImage.open('out/all_routes_combined_v1711_candidate.nds')
    assert previous.read_file('/COMMON/MESFILE.DK4')==image.read_file('/COMMON/MESFILE.DK4')
    assert previous.read_file('/__arm9__.bin')==arm and prior['COMMON676_677_repaired_layout_preserved_without_new_shop_visit']
    save(OUT,{'candidate':str(rom),'candidate_sha256':digest,'targeted_paths':paths,
        'all_four_original_response_paths_normal_type0_returns_verified':True,
        'all70_speech_visits140_complete_holds_and126_native_command_pairs':True,
        'individual_actual_speech_IDs':sorted(actual),'actual_holds_by_ID':actual,
        'unvisited_conditional_records':mapping['unvisited_conditional_records'],
        'no_claim_of_individual_activation_for_five_native_equivalents':True,
        'all8_fixture_free_startup_controls_and_viewed_sheet_verified':True,
        'startup_review_sheet_actually_viewed':True,
        'both_new_B120_choice0_sheets_menu_and_terminal_actually_viewed':True,
        'prior_wind_and_both_B23_visual_reviews_retained':True,
        'COMMON676_677_repaired_layout_preserved_without_new_shop_visit':True,
        'research_current_ROM_entire_file_identical_to_registered':release['registered_ROM_whole_file_byte_exact_to_actual_scene_research_ROM'],
        'older_wind_test_inherits_exact_B120_block_and_runtime_not_entire_ROM_identity':True,
        'no_full_route_earned_travel_hardware_or_graphics_audit_completion_claim':True,
        'evidence':{str(p):sha(p.read_bytes())for p in [ROOT/'registered_release_verification.json',ROOT/'ordinary_startup_verification.json',MAP,WIND,FULL,DECLINE,DEFAULT]},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1775:four original lesson response paths,55 individual speeches/five explicit native equivalents,140 complete holds,startup8 and inherited shop formatting reconciled.',flush=True)
