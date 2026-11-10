"""Finish the already validated fixture receipt after redundant old runner-generation failed."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_English_fixture_v5939b')
if __name__=='__main__':
    out=ROOT/'pin_and_runner_receipt.json';assert not out.exists()
    fp=ROOT/'complete_B201_English_B22_fixture.json';doc=read(fp);f=doc['fixtures'][0];rom=Path(f['research_ROM'])
    assert sha(rom.read_bytes())==f['research_ROM_sha256'] and sha(Path(doc['parent']).read_bytes())==doc['parent_sha256']
    parent,target=NdsImage.open(doc['parent']),NdsImage.open(rom)
    assert [p for _,p,v in parent.iter_files() if target.read_file(p)!=v]==['/data/SC2.DK4'] and all(target.read_file(p)==v for p,v in parent.iter_components())
    a,b=[IlnkContainer.parse(x.read_file('/data/SC2.DK4')).blocks for x in [parent,target]]
    assert [i for i,(x,y) in enumerate(zip(a,b,strict=True)) if x!=y]==[22] and b[22].hex()==f['fixture_block_hex']
    assert len(f['all53_stored_fixture_commands'])==53 and len(f['original_text_records'])==24
    pins=Path('translations/rom_retention_pins.json');before=(ROOT/'pins.before.json').read_bytes();old=json.loads(before);now=read(pins)
    assert now[:-1]==old and Path(now[-1]['path']).resolve()==rom.resolve() and f['research_ROM_sha256'] in now[-1]['reason']
    runners=[Path('scripts/run_lil_B201_English_buy_v5940b.py'),Path('scripts/run_lil_B201_English_decline_v5941b.py')]
    assert all(p.exists() and 'English_fixture_v5939b' in p.read_text() for p in runners)
    save(out,dict(new_ROM=str(rom),new_ROM_sha256=f['research_ROM_sha256'],all_prior_pins_preserved=True,
        before_sha256=sha(before),after_sha256=sha(pins.read_bytes()),ROMs_deleted=0,
        prepared_runners={str(p):sha(p.read_bytes()) for p in runners},
        preserved_failed_producer='scripts/research_lil_B201_English_fixture_v5939b.py',
        failure_was_redundant_legacy_runner_generation_after_correct_ROM_manifest_and_pin=True,
        validated_existing_ROM_reused_no_rebuild_or_duplicate_pin=True,
        complete_image_and53_commands24_speeches_verified=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Existing English fixture and pin validated;two already prepared source-owned runners bound. No ROM rebuilt or old artifact changed.')
