"""Recover the exact missing historical input from its retained clean-input patch."""
from pathlib import Path
import json
import os
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B180_historical_restore_v4764')
ROM=Path('out/all_routes_combined_v1909_candidate.nds')

if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists()
    packet=read('work/analysis/lil_B180_source_v4758/all11_clean_current_complete_context.json')
    assert Path(packet['historical_snapshot_ROM'])==ROM
    manifest=read(ROM.with_suffix('.manifest.json'))
    expected='fdc6757a13af0a04c4f2355ade3c66163a6382a0a7081efa03a457b1198dd1d1'
    assert manifest['candidate_sha256']==expected
    clean=Path('work/clean.nds');assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch=ROM.with_suffix('.xdelta');patch_hash=sha(patch.read_bytes())
    ROOT.mkdir(parents=True);stage=ROOT/'reconstructed_historical_input.nds'
    apply_xdelta(clean,patch,stage)
    assert sha(stage.read_bytes())==expected
    assert not ROM.exists();os.replace(stage,ROM)
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before)
    entry=dict(path=str(ROM.resolve()),reason='Exact V1909 recovered from retained clean-input patch for B180 bounded historical-snapshot native proofs. Preserve this historical input; no current gameplay or release claim. SHA256 '+expected)
    assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)
    values.append(entry);newline='\r\n' if b'\r\n' in before else '\n'
    after=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n',newline).encode('utf-8')
    assert pins.read_bytes()==before;pins.write_bytes(after)
    save(ROOT/'restoration_receipt.json',dict(ROM=str(ROM),ROM_sha256=expected,patch=str(patch),patch_sha256=patch_hash,
        exact_historical_manifest_hash_restored=True,preexisting_ROM_overwritten=False,all_existing_pins_preserved=True,
        pins_before_sha256=sha(before),pins_after_sha256=sha(after),no_review_or_gameplay_credit=True,
        stopped_dispatch4760_and_entry4762_preserved=True))
    print('Exact historical V1909 restored from its clean-input patch and pinned; no current release change.')
