"""Stage the displayed Market Info trend heading in its exact original slot."""

from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
from struct import unpack_from
import sys
from types import FunctionType

from scripts import register_developed_port_menu_20261115 as parent
from scripts import replay_refit_help_startup_20261115 as startup
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.verify_release_baseline import files


base = parent.base
CLEAN, ARM = parent.stage.CLEAN, parent.stage.ARM
ROOT = Path('work/market_info_trends_staged_20261115_v1')
ROM = ROOT / 'Market_Info_Trends_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
OFFSET, SLOT, POINTER, DRAW = 0x159F88, 8, 0xBEE7C, 0xBECC8
JAPANESE, ENGLISH, RECORD = '流行品', 'Trends', 'MARKET_INFO_TRENDS_HEADING'


def apply(source, current):
    start, end = OFFSET, OFFSET + SLOT
    before = JAPANESE.encode('cp932').ljust(SLOT, b'\0')
    after = ENGLISH.encode('ascii').ljust(SLOT, b'\0')
    assert source[start:end] == current[start:end] == before and len(after) == SLOT
    assert len(ENGLISH) == len(JAPANESE) * 2 == 6
    assert unpack_from('<I', source, POINTER) == unpack_from('<I', current, POINTER) == (0x02000000 + start,)
    assert source[0xBE884:0xBEE44] == current[0xBE884:0xBEE44]
    assert source[0xB30EC:0xB320C] == current[0xB30EC:0xB320C]
    assert current[0x143E98:0x143E9F] == ENGLISH.encode('ascii') + b'\0'
    return current[:start] + after + current[end:], dict(offset=start, size=SLOT, pointer_field=POINTER,
        source_draw=0x02000000 + DRAW, clean_hex=before.hex(), previous_hex=before.hex(), target_hex=after.hex())


def stage():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    clean, candidate = map(base.NdsImage.open, (CLEAN, parent.ROM))
    before = files(candidate)
    arm, field = apply(clean.read_file(ARM), before[ARM])
    verify_runtime(arm, release)
    candidate.replace_file(ARM, arm)
    after = files(candidate)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {ARM}
    ROOT.mkdir()
    candidate.save(ROM)
    candidate.replace_file(ARM, before[ARM])
    assert bytes(candidate.rom.save()) == parent.ROM.read_bytes()
    base.save(STORED, dict(candidate_sha256=base.digest(ROM), previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=sha256(arm).hexdigest(), changed_slot=field, whole_parent_inverse=True))
    print('Staged the eight-byte Market Info label slot and verified the complete parent inverse.')


def replay_startup():
    FunctionType(startup.main.__code__, vars(startup) | dict(stage=sys.modules[__name__]))()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('stage', 'startup'))
    (stage if parser.parse_args().action == 'stage' else replay_startup)()
