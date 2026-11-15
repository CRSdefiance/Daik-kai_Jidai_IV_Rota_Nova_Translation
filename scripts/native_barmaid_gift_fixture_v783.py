"""Explicit frozen gift-fixture replay for the unchanged V783 inventory methods."""

from pathlib import Path
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_barmaid_gift_fixture_v780_v3 as original

SUPPORTED = ('d2d2670bfbbb8ce1c3433b0c1a6220f385ef8beba5678bea9e9d4bb612b57abb',
             'daa9686528955df3e88258c5c3fc1b63adb551b08669f2a33584e3bd9d674c02')


def transfer(arm, raw, items):
    if sha(arm) not in SUPPORTED or items != [143]:
        raise ValueError('Only pinned V780/V783 and Seoul gift143 are declared')
    reference = NdsImage.open('out/all_routes_combined_v780_candidate.nds').read_file('/__arm9__.bin')
    assert arm[0x49D00:0x4A800] == reference[0x49D00:0x4A800]
    replay = FunctionType(original.transfer.__code__, {**original.__dict__, 'SUPPORTED_ARM_SHA': SUPPORTED})
    result, proof = replay(arm, raw, items)
    proof['explicit_frozen_fixture_replay'] = str(Path(original.__file__))
    proof['frozen_fixture_sha256'] = sha(Path(original.__file__).read_bytes())
    proof['original_inventory_executable_span_exact_to_V780'] = True
    return result, proof
