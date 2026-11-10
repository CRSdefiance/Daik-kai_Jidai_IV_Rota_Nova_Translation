"""Pin complete six-record atomic inputs after independent native/actual/FE/controls positives."""
import sys
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_outcomes_profile_v1 import contract
from dk4tool.patch.hodram_outcomes_editorial_v1 import CONFIG,CANONICAL
from scripts.Hodram_outcomes_release_paths_v8347 import PARENT,ROM,DOC,MAP,SEAL,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcomes_production_v8354')
CHECKS=[
Path('work/analysis/Hodram_outcome_actual_evidence_v8349b/four_whole_fixtures_all_original_traces_and100_actual_body_name_FE_holds_recomputed.json'),
Path('work/analysis/Hodram_outcome_comparison_validation_v8350/all_commands_scenes_final_native_states186_RGBpairs_andB48_differences_recomputed.json'),
Path('work/analysis/Hodram_outcome_FE_evidence_v8351b/two_original_FE_snapshots_four_live_VRAM_palette_RGB_holds_recomputed.json'),
Path('work/analysis/Hodram_outcome_controls_validation_v8353/six_dispatches_two_EV1_entries100_endcases14_opaque_decodes325_loads650_modes_recomputed.json')]
if __name__=='__main__':
    config=Path(CONFIG);assert not ROOT.exists() and not config.exists();frozen=contract();mapping,seal=read(MAP),read(SEAL);image=NdsImage.open(PARENT)
    assert read(CHECKS[0])['result']['complete_actual_holds']==100 and read(CHECKS[1])['result']['later_full_RGB_pairs_recomputed']==186 and read(CHECKS[2])['result']['complete_actual_VRAM_bitmap_palette_RGB_holds_recomputed']==4 and read(CHECKS[3])['loaders']['initial_parent_modes_bound']==650
    assert sha(PARENT.read_bytes())==mapping['source_ROM_sha256']==seal['parent_sha256'] and sha(ROM.read_bytes())==seal['research_ROM_sha256']
    deps={Path(p).resolve() for p in frozen['dependencies']}|{p.resolve() for p in [DOC,MAP,SEAL,Path(__file__),*map(Path,proofs().values()),*CHECKS]}
    repo=Path.cwd().resolve()
    for module in list(sys.modules.values()):
        path=getattr(module,'__file__',None)
        if not path:continue
        path=Path(path).resolve()
        if path.is_relative_to(repo) and path.suffix=='.py' and path.is_file() and not path.is_relative_to((repo/'.deps').resolve()):deps.add(path)
    for path in deps:assert path.is_file()
    save(config,dict(format='dk4-Hodram-outcomes-editorial-release-v1',manuscripts=[str(DOC)],proofs=proofs(),reference_map=str(MAP),reference_approval=str(SEAL),reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),canonical_ROM=str(CANONICAL),canonical_ROM_sha256=sha(CANONICAL.read_bytes()),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),predecessor_file_hashes={p:sha(v) for _,p,v in image.iter_files()},predecessor_component_hashes={p:sha(v) for p,v in image.iter_components()},required_registered_Gerhard_dependency=frozen['explicit_registered_Gerhard_dependency'],archives=[dict(file_path='/data/SC1.DK4',source_sha256=mapping['source_archive_sha256'],target_sha256=mapping['target_archive_sha256'])],components=[],dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)},independent_native_actual_FE_controls_comparison_checks={str(p):sha(p.read_bytes()) for p in CHECKS},atomic_positive_corruption_tests_registered_release_andcredit_pending=True,new_credit=0,full_goal_complete=False))
    ROOT.mkdir(parents=True);save(ROOT/'immutable_six_record_atomic_configuration.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),dependency_count=len(deps),all_actual_scope_limits_andFE_temporary_context_VRAM_andB48_later_differences_preserved=True,no_ROM_registry_orledger_change=True,new_credit=0,full_goal_complete=False))
    print('Pinned six-record atomic configuration:',len(deps),'dependencies;all prior translations/ROMs preserved.No credit orregistration.')
