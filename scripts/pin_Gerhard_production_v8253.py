"""Pin immutable inputs and the complete predecessor for the two-component atomic integration stage."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.gerhard_surname_profile_v1 import contract
from dk4tool.patch.gerhard_surname_evidence_v1 import MODEL
from scripts.Gerhard_surname_release_paths_v8238 import PARENT,ROM,APPROVED,MAP,SEAL,FLAGS,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_production_tools_v8253')
CONFIG=Path('translations/gerhard_surname_editorial_release_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not CONFIG.exists();frozen=contract();mapping=read(MAP);seal=read(SEAL);image=NdsImage.open(PARENT)
    assert sha(PARENT.read_bytes())==frozen['parent_ROM_sha256']==mapping['parent_ROM_sha256'] and sha(ROM.read_bytes())==seal['reference_ROM_sha256']
    deps={Path(p) for p in frozen['dependencies']}|{Path('translations/gerhard_surname_native_contract_v1.json'),APPROVED,MAP,SEAL,Path(MODEL),Path(__file__),Path('scripts/Gerhard_surname_release_paths_v8238.py'),*map(Path,proofs().values())}
    deps|={Path('dk4tool/patch')/n for n in ['gerhard_surname_editorial_v1.py','gerhard_surname_rebuild_v1.py','gerhard_surname_evidence_v1.py','gerhard_surname_comparison_v1.py','gerhard_surname_risk_v1.py']}
    deps|={Path('dk4tool/dialogue')/n for n in ['gerhard_surname_profile_v1.py','gerhard_surname_layout_v1.py','gerhard_surname_plan_v1.py']}
    deps|={Path('scripts')/n for n in ['square_shopkeeper_font_oracles_v7020.py','research_lil_B209_native_pages_v6461.py','verify_name_catalog_glyphs_v278.py','prove_lil_B208_name_planes_v6405.py','focus_Rafael_B50_picture_risk_v8160.py','verify_personal_gameplay_v841.py','verify_market_gameplay_v753.py','verify_shipyard_gameplay_v760.py','verify_tavern_gameplay_v767.py','verify_followup_gameplay_v778.py','verify_ceremony_prayer_gameplay_v814.py']}
    save(CONFIG,dict(format='dk4-Gerhard-five-body-one-name-editorial-release-v1',manuscripts=[str(APPROVED)],proofs=proofs(),required_map_flags=FLAGS,
        reference_map=str(MAP),reference_approval=str(SEAL),reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),
        canonical_ROM='out/raphael_natural_v2_accepted_base.nds',canonical_ROM_sha256=sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        predecessor_file_hashes={p:sha(v) for _,p,v in image.iter_files()},predecessor_component_hashes={p:sha(v) for p,v in image.iter_components()},
        archives=[dict(file_path='/data/SC2.DK4',source_sha256=mapping['source_SC2_sha256'],target_sha256=mapping['target_SC2_sha256'])],
        components=[dict(file_path='/__arm9__.bin',source_sha256=mapping['source_ARM9_sha256'],target_sha256=mapping['target_ARM9_sha256'])],
        dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)},new_credit=0,full_goal_complete=False))
    ROOT.mkdir(parents=True);save(ROOT/'pinned_atomic_configuration.json',dict(config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),
        full_predecessor_andtwo_owned_outputs_pinned=True,atomic_positive_corruption_suite_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    print('Pinned fullV8172 predecessor andtwo-output atomic config;noROM/registry change.')
