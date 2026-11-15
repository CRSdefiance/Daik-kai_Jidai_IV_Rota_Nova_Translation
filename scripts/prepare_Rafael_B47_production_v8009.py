"""Pin complete V7964 predecessor and all B47 approved reconstruction dependencies."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Rafael_B47_release_paths_v8006 import PARENT,ROM,APPROVED,MAP,SEAL,FLAGS,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_production_tools_v8009')
CONFIG=Path('translations/rafael_B47_editorial_release_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not CONFIG.exists()
    image=NdsImage.open(PARENT);mapping=read(MAP);seal=read(SEAL)
    assert sha(PARENT.read_bytes())==mapping['source_ROM_sha256']==seal['parent_sha256']
    assert sha(ROM.read_bytes())==seal['research_ROM_sha256'] and sha(APPROVED.read_bytes())==seal['manuscript_sha256']
    deps={APPROVED,MAP,SEAL,Path(__file__),Path('scripts/Rafael_B47_release_paths_v8006.py'),Path('scripts/seal_Rafael_B47_references_v8006.py'),
        Path('dk4tool/patch/rafael_B47_editorial_v1.py'),Path('dk4tool/patch/rafael_B47_reconstruction_v1.py'),
        *[Path('dk4tool/dialogue')/n for n in ['rafael_B47_profile_v1.py','rafael_B47_layout_v1.py','rafael_B47_plan_v1.py']],
        *map(Path,proofs().values())}
    for key in ['native_font_proof','actual_proof','source_font_proof']:
        for path,digest in read(proofs()[key]).get('evidence',{}).items():
            assert sha(Path(path).read_bytes())==digest;deps.add(Path(path))
    save(CONFIG,dict(format='dk4-Rafael15-B47-editorial-release-v1',manuscripts=[str(APPROVED)],proofs=proofs(),required_map_flags=FLAGS,
        reference_map=str(MAP),reference_approval=str(SEAL),reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),
        canonical_ROM='out/raphael_natural_v2_accepted_base.nds',canonical_ROM_sha256=sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        predecessor_file_hashes={p:sha(v) for _,p,v in image.iter_files()},predecessor_component_hashes={p:sha(v) for p,v in image.iter_components()},
        archives=[dict(file_path='/data/SC0.DK4',source_sha256=mapping['source_archive_sha256'],target_sha256=mapping['target_archive_sha256'])],
        dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)},new_credit=0,full_goal_complete=False))
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_atomic_config.json',dict(config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),
        complete_predecessor_andone_manifest_reference_exact=True,meaningful_atomic_challenges_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    print('B47 atomic config pinned to V7964;15 speech manifest. No ROM/registry/credit change;atomic tests pending.')
