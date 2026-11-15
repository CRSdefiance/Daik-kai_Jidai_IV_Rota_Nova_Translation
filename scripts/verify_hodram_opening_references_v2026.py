"""Bind all three typed maps to unchanged executable entries and EV1."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_rafael_opening_references_v2006 import units
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hodram_opening_references_v2026')
PLAN=Path('work/analysis/hodram_opening_relocation_v2023/complete_three_block_typed_relocation_research.json')
LOAD=Path('work/analysis/hodram_opening_loader_v2024/whole_SC1_and_B42_B44_initial_entry_proof.json')
PRIOR=Path('work/analysis/lil_Hamburg_reference_census_v1963/all123_commands20_relative_sites_and_shipped_entry_census.json')

if __name__=='__main__':
    assert not ROOT.exists()
    plan,loader,prior=map(read,(PLAN,LOAD,PRIOR));image=NdsImage.open(plan['research_ROM']);parent=NdsImage.open(plan['parent'])
    for key in('research_ROM','parent'):assert sha(Path(plan[key]).read_bytes())==plan[key+'_sha256']
    assert loader['all325_whole_blocks_and650_modes_each_pass']and loader['original_EV1_actions_select_by_block_index_without_interior_byte_offset']
    assert loader['original_parent_both_modes_start_at_loaded_payload_plus8']
    for row in loader['versions']:
        for kind in('load','parent'):assert sha(Path(row[kind+'_proof']).read_bytes())==row[kind+'_sha256']
    old=prior['native_call_census']['current']
    assert [r['address']for r in old['branches']]==[0x02024070]and not old['literal_aliases']
    assert units(image)==units(parent)==old['units']
    assert image.read_file('/data/EV1.DK4')==parent.read_file('/data/EV1.DK4')
    a,b=[IlnkContainer.parse(im.read_file('/data/SC1.DK4')).blocks for im in(parent,image)]
    assert len(a)==len(b)==325 and[n for n,(x,y)in enumerate(zip(a,b,strict=True))if x!=y]==[42,43,44]
    assert plan['all171_typed_commands24_relative_sites360_native_cases']and plan['all73_final_parity_native_planes_exact']
    assert plan['all_three_current_blocks_restore_exactly']and plan['all322_other_blocks_other_files_and_components_exact']
    ROOT.mkdir(parents=True)
    save(ROOT/'three_block_mapping_and_inherited_executable_entry_census.json',dict(
        research_ROM=plan['research_ROM'],research_ROM_sha256=plan['research_ROM_sha256'],parent=plan['parent'],parent_sha256=plan['parent_sha256'],
        plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),loader=str(LOAD),loader_sha256=sha(LOAD.read_bytes()),
        inherited_executable_census=str(PRIOR),inherited_executable_census_sha256=sha(PRIOR.read_bytes()),
        every_current_and_target_executable_unit_exact_prior_census=True,all_unit_hashes=old['units'],
        only_original_02024070_interpreter_entry_no_literal_alias=True,EV1_original_block_index_loader_and_parent_plus8_verified=True,
        all325_original_loads_and650_parent_modes_each_ROM=True,all322_other_SC1_blocks_exact=True,
        all171_clean_current_target_commands24_relative_sites360_native_cases_bound=True,
        representative_revised_actual_transition_pending=True,not_gameplay_or_registered_release_completion=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(commands=171,relative_sites=24,native_cases=360,loader_blocks=325,parent_modes=650))
