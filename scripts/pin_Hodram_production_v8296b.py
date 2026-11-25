"""Pin the immutable Hodram production inputs after independent native/actual checks."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_three_blocks_profile_v1 import contract
from dk4tool.patch.hodram_three_blocks_editorial_v2 import CONFIG,CANONICAL
from scripts.Hodram_three_blocks_release_paths_v8290 import PARENT,ROM,DOC,MAP,SEAL,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_production_tools_v8296b')
CHECKS=[Path('work/analysis/Hodram_independent_evidence_v8293/native56_body6_name_masks_six_fixture_traces262_actual_holds_recomputed.json'),
    Path('work/analysis/Hodram_independent_comparison_v8294/all_command_scene_final_native_state_and532_later_RGB_pairs_recomputed.json'),
    Path('work/analysis/Hodram_independent_controls_v8295/28_dispatches24_controls40_relatives6_queries150_reused_ends325_loads650_modes_census_bound.json')]
if __name__=='__main__':
    config=Path(CONFIG);assert not ROOT.exists() and not config.exists();frozen=contract();mapping,seal=read(MAP),read(SEAL);image=NdsImage.open(PARENT)
    assert read(CHECKS[0])['result']['complete_body_holds']==262 and read(CHECKS[1])['result']['later_full_RGB_pairs_recomputed']==532 and read(CHECKS[2])['entries']['initial_parent_modes_bound']==650
    assert sha(PARENT.read_bytes())==mapping['source_ROM_sha256']==seal['parent_sha256'] and sha(ROM.read_bytes())==seal['research_ROM_sha256']
    deps={Path(p) for p in frozen['dependencies']}|{DOC,MAP,SEAL,Path(__file__),Path('scripts/Hodram_three_blocks_release_paths_v8290.py'),*map(Path,proofs().values()),*CHECKS}
    deps|={Path('dk4tool/patch')/f'hodram_three_blocks_{part}_v1.py' for part in ['editorial','rebuild','references','evidence','comparison','controls']}
    deps|={Path('dk4tool/dialogue')/f'hodram_three_blocks_{part}_v1.py' for part in ['profile','layout','plan']}
    deps|={Path('scripts')/name for name in ['prove_lil_shrines_temples_controls_v3168c.py','approve_lil_lessons_references_v1773.py','inventory_lil_after_crew_items_complete_v3152.py','lil_B207_name_style_v6354d.py','verify_personal_gameplay_v841.py','verify_ceremony_prayer_gameplay_v814.py']}
    deps|={Path('dk4tool/patch/hodram_three_blocks_editorial_v2.py'),Path('dk4tool/patch/hodram_three_blocks_controls_v2.py')}
    save(config,dict(format='dk4-Hodram-three-blocks-editorial-release-v1',manuscripts=[str(DOC)],proofs=proofs(),
        reference_map=str(MAP),reference_approval=str(SEAL),reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),
        parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),canonical_ROM=str(CANONICAL),canonical_ROM_sha256=sha(CANONICAL.read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        predecessor_file_hashes={p:sha(v) for _,p,v in image.iter_files()},predecessor_component_hashes={p:sha(v) for p,v in image.iter_components()},
        required_registered_Gerhard_dependency=frozen['explicit_registered_Gerhard_dependency'],
        archives=[dict(file_path='/data/SC1.DK4',source_sha256=mapping['source_archive_sha256'],target_sha256=mapping['target_archive_sha256'])],components=[],
        dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)},independent_actual_controls_comparison_checks={str(p):sha(p.read_bytes()) for p in CHECKS},
        atomic_positive_corruption_tests_registered_release_andcredit_pending=True,new_credit=0,full_goal_complete=False))
    ROOT.mkdir(parents=True);save(ROOT/'immutable_single_archive_atomic_configuration.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),dependency_count=len(deps),
        all_previous_native_actual_controls_andfullscope_preserved=True,no_ROM_registry_orledger_change=True,new_credit=0,full_goal_complete=False))
    print('Pinned Hodram production configuration:one SC1 archive/28records/full V8259 predecessor;atomic positives/challenges next.')
