"""Exact V1189 COMMON reader; retain the frozen V1166 opaque-prefix guard."""
from pathlib import Path
from dk4tool.patch.escape_direct_formatting import CONFIG
from dk4tool.patch.duel_editorial import current_entries as parent_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read


def current_entries(common,arm):
    config=read(CONFIG);assert sha(arm)==config['target_arm9_sha256']
    key=config['runtime_plan'];path=Path(key)
    assert sha(path.read_bytes())==config['dependencies'][key]
    restored=bytearray(arm)
    for row in read(path)['patches']:
        at=row['address']-0x02000000;data=bytes.fromhex(row['target_hex'])
        assert arm[at:at+len(data)]==data
        restored[at:at+len(data)]=bytes.fromhex(row['source_hex'])
    assert sha(restored)==config['source_arm9_sha256']
    return parent_entries(common,bytes(restored))
