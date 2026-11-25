"""Pin complete predecessor/runtime/source/native/actual dependencies for atomic B45 production."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Rafael_B45_release_paths_v7903 import PARENT,ROM,APPROVED,MAP,SEAL,FLAGS,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_production_tools_v7904')
CONFIG=Path('translations/rafael_B45_editorial_release_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not CONFIG.exists()
    image=NdsImage.open(PARENT);mapping=read(MAP);seal=read(SEAL)
    assert sha(PARENT.read_bytes())==mapping['source_ROM_sha256']==seal['parent_sha256']
    assert sha(ROM.read_bytes())==seal['research_ROM_sha256'] and sha(APPROVED.read_bytes())==seal['manuscript_sha256']
    deps={APPROVED,MAP,SEAL,Path(__file__),Path('scripts/Rafael_B45_release_paths_v7903.py'),
        Path('dk4tool/patch/rafael_B45_editorial_v1.py'),Path('dk4tool/patch/rafael_B45_reconstruction_v1.py'),
        Path('dk4tool/dialogue/rafael_B45_profile_v1.py'),Path('dk4tool/dialogue/rafael_B45_layout_v1.py'),Path('dk4tool/dialogue/rafael_B45_plan_v1.py'),
        Path('work/analysis/Rafael_B45_source_name_planes_v7894/12_complete_source_pages2_names8_literal_alignments_distinct_FE.json'),
        *map(Path,proofs().values())}
    for key in ['native_font_proof','actual_proof','native_stored_proof']:
        for path,digest in read(proofs()[key]).get('evidence',{}).items():
            assert sha(Path(path).read_bytes())==digest;deps.add(Path(path))
    save(CONFIG,dict(format='dk4-Rafael12-B45-editorial-release-v1',manuscripts=[str(APPROVED)],proofs=proofs(),required_map_flags=FLAGS,
        reference_map=str(MAP),reference_approval=str(SEAL),reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),
        canonical_ROM='out/raphael_natural_v2_accepted_base.nds',canonical_ROM_sha256=sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        predecessor_file_hashes={path:sha(value) for _,path,value in image.iter_files()},
        predecessor_component_hashes={path:sha(value) for path,value in image.iter_components()},
        archives=[dict(file_path='/data/SC0.DK4',source_sha256=mapping['source_archive_sha256'],target_sha256=mapping['target_archive_sha256'])],
        dependencies={str(path):sha(path.read_bytes()) for path in sorted(deps)},new_credit=0,full_goal_complete=False))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_config.json',dict(config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),
        predecessor_all_files_components_andreference_exact=True,source00_body_guard_five_relative_fixups_andall_actual_limits_pinned=True,
        meaningful_atomic_challenges_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    print('B45 atomic production config pinned tocomplete V7857 predecessor andapproved research reference. No ROM orregistry mutation;positive/negative atomic tests pending.')
