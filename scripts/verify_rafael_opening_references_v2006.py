"""Bind complete B44 mapping to unchanged shipped interpreter entries and EV0.

Reuse the existing full executable census only after comparing every unit hash.
This is distinct from the later older-record technical re-audit.
"""
from pathlib import Path
from ndspy.code import MainCodeFile,loadOverlayTable
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/rafael_opening_references_v2006')
PLAN=Path('work/analysis/rafael_opening_relocation_v2001b/current_B44_typed_relocation_research.json')
LOAD=Path('work/analysis/rafael_opening_loader_v2002/whole_SC0_and_B44_initial_entry_proof.json')
PRIOR=Path('work/analysis/lil_Hamburg_reference_census_v1963/all123_commands20_relative_sites_and_shipped_entry_census.json')

def units(image):
    arm=image.read_file('/__arm9__.bin')
    result=[('section'+str(n),s.ramAddress,bytes(s.data))for n,s in enumerate(MainCodeFile(arm,0x02000000).sections)]
    result += [('overlay'+str(n),s.ramAddress,bytes(s.data))for n,s in loadOverlayTable(image.rom.arm9OverlayTable,lambda _,f:image.rom.files[f]).items()]
    return [dict(name=n,base=b,bytes=len(d),sha256=sha(d))for n,b,d in result]

if __name__=='__main__':
    assert not ROOT.exists()
    plan,loader,prior=map(read,(PLAN,LOAD,PRIOR));image=NdsImage.open(plan['research_ROM']);parent=NdsImage.open(plan['parent'])
    assert sha(Path(plan['research_ROM']).read_bytes())==plan['research_ROM_sha256']
    assert sha(Path(plan['parent']).read_bytes())==plan['parent_sha256']
    assert loader['all343_whole_blocks_and686_modes_each_pass']and loader['original_EV0_actions_select_by_block_index_without_interior_byte_offset']
    assert loader['original_parent_both_modes_start_at_loaded_payload_plus8']
    for row in loader['versions']:
        for kind in ('load','parent'):assert sha(Path(row[kind+'_proof']).read_bytes())==row[kind+'_sha256']
    old=prior['native_call_census']['current']
    assert [r['address']for r in old['branches']]==[0x02024070]and not old['literal_aliases']
    assert units(image)==units(parent)==old['units']
    assert image.read_file('/data/EV0.DK4')==parent.read_file('/data/EV0.DK4')
    old_blocks,new_blocks=[IlnkContainer.parse(im.read_file('/data/SC0.DK4')).blocks for im in(parent,image)]
    assert len(old_blocks)==len(new_blocks)==343
    assert [n for n,(a,b)in enumerate(zip(old_blocks,new_blocks,strict=True))if a!=b]==[44]
    assert plan['all182_typed_command_words_preambles_extents_and_ancestors_verified']
    assert plan['all4_relative_sites60_native_cases_pass']and plan['explicit_two_inherited_stale_spans_repaired']
    assert plan['exact_inverse_restores_actual_current_source_including_old_stale_span']
    assert plan['typed_choice_object_and_both_original_labels_unchanged']
    ROOT.mkdir(parents=True)
    save(ROOT/'complete_B44_mapping_and_inherited_executable_entry_census.json',dict(
        research_ROM=plan['research_ROM'],research_ROM_sha256=plan['research_ROM_sha256'],parent=plan['parent'],parent_sha256=plan['parent_sha256'],
        plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),loader=str(LOAD),loader_sha256=sha(LOAD.read_bytes()),
        inherited_executable_census=str(PRIOR),inherited_executable_census_sha256=sha(PRIOR.read_bytes()),
        every_current_and_target_executable_unit_exact_prior_census=True,all_unit_hashes=old['units'],
        only_original_02024070_interpreter_entry_no_literal_alias=True,EV0_unchanged_original_block_index_loader_and_parent_plus8_verified=True,
        all343_original_loads_and686_parent_modes_each_ROM=True,all342_other_SC0_blocks_exact=True,
        all182_clean_current_target_typed_commands_and4_relative_sites_bound=True,
        two_actual_current_stale_spans_explicitly_classified_and_repaired_from_clean_targets=True,
        actual_revised_choice_paths_and_final_reference_approval_pending=True,
        not_a_gameplay_or_registered_release_completion=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(typed_commands=182,relative_sites=4,external_executable_units_exact_prior=True,loader_blocks=343,parent_modes=686,actual_pending=True))
