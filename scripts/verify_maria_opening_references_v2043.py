"""Bind the CS0101 map to unchanged executable entries,EV3 and all route loads."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_rafael_opening_references_v2006 import units
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_opening_references_v2043')
PLAN=Path('work/analysis/maria_opening_relocation_v2040/complete_B33_CS0101_typed_relocation_research.json')
LOAD=Path('work/analysis/maria_opening_loader_v2041/whole_SC3_and_B33_initial_entry_proof.json')
PRIOR=Path('work/analysis/lil_Hamburg_reference_census_v1963/all123_commands20_relative_sites_and_shipped_entry_census.json')
if __name__=='__main__':
    assert not ROOT.exists()
    plan,loader,prior=map(read,(PLAN,LOAD,PRIOR));image=NdsImage.open(plan['research_ROM']);parent=NdsImage.open(plan['parent'])
    for key in('research_ROM','parent'):assert sha(Path(plan[key]).read_bytes())==plan[key+'_sha256']
    assert loader['all303_whole_blocks_and606_modes_each_pass']and loader['original_EV3_actions_select_by_block_index_without_interior_byte_offset']
    assert loader['original_parent_both_modes_start_at_loaded_payload_plus8']
    for row in loader['versions']:
        for kind in('load','parent'):assert sha(Path(row[kind+'_proof']).read_bytes())==row[kind+'_sha256']
    old=prior['native_call_census']['current'];assert[r['address']for r in old['branches']]==[0x02024070]and not old['literal_aliases']
    assert units(image)==units(parent)==old['units']and image.read_file('/data/EV3.DK4')==parent.read_file('/data/EV3.DK4')
    a,b=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks for im in(parent,image)]
    assert len(a)==len(b)==303 and[n for n,(x,y)in enumerate(zip(a,b,strict=True))if x!=y]==[33]
    assert a[33][:4]==b[33][:4]==b'CS\1\1'
    assert plan['all85_typed_commands_and38_final_native_planes_exact']and plan['exact_inverse_restores_current_block']
    assert plan['CS0101_header_and_all47_non_speech_commands_exact']and not plan['relative_skip_fixups']
    ROOT.mkdir(parents=True)
    save(ROOT/'B33_CS0101_mapping_and_inherited_executable_entry_census.json',dict(
        research_ROM=plan['research_ROM'],research_ROM_sha256=plan['research_ROM_sha256'],parent=plan['parent'],parent_sha256=plan['parent_sha256'],
        plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),loader=str(LOAD),loader_sha256=sha(LOAD.read_bytes()),
        inherited_executable_census=str(PRIOR),inherited_executable_census_sha256=sha(PRIOR.read_bytes()),
        every_current_target_executable_unit_exact_prior_census=True,all_unit_hashes=old['units'],only_original_02024070_entry_no_literal_alias=True,
        EV3_original_block_index_loader_parent_plus8_and_CS0101_preserved=True,all303_loads606_parent_modes_each_ROM=True,
        all302_other_SC3_blocks_exact_including_unclassified_B109=True,all85_commands38_complete_native_planes_bound=True,
        all47_non_speech_commands_exact_no_relative_sites_or_choices=True,representative_revised_actual_transition_pending=True,
        not_gameplay_or_registered_release_completion=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(commands=85,CS0101_preserved=True,loader_blocks=303,parent_modes=606,actual_pending=True))
