"""Replace the developed-port exit label within its original ARM9 slot."""

from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from scripts import register_barmaid_town_labels_20261115 as parent
from scripts import replay_refit_help_startup_20261115 as startup
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.verify_release_baseline import files


base = parent.base
CLEAN, ARM = parent.stage.CLEAN, parent.stage.ARM
ROOT = Path('work/developed_port_menu_20261115_v1')
ROM = ROOT / 'Developed_Port_Menu_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
OFFSET = 0x1446CC
POINTER = 0x14471C
ENTRY = 0x60444
SLOT = 16
JAPANESE = '出港所を出る'
ENGLISH = 'Back to Town'
RECORD = 'DEVELOPED_PORT_MENU_BACK_TO_TOWN'


def apply(source, current):
    start, end = OFFSET, OFFSET + SLOT
    original = JAPANESE.encode('cp932').ljust(SLOT, b'\0')
    target = ENGLISH.encode('ascii').ljust(SLOT, b'\0')
    assert len(ENGLISH) == len(JAPANESE) * 2 == 12
    assert source[start:end] == current[start:end] == original
    assert unpack_from('<I', source, POINTER) == unpack_from('<I', current, POINTER) == (0x02000000 + start,)
    assert source[ENTRY:0x604D0] == current[ENTRY:0x604D0]
    assert source[0xB65E4:0xB6650] == current[0xB65E4:0xB6650]
    field = unpack_from('<16I', current, 0x1446EC)
    assert field[12] == 0x02000000 + OFFSET
    return current[:start] + target + current[end:], dict(clean_hex=original.hex(), previous_hex=original.hex(),
        target_hex=target.hex(), offset=start, size=SLOT, pointer_field=POINTER, port_menu_entry=0x02000000 + ENTRY)


def stage():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    clean, target = map(base.NdsImage.open, (CLEAN, parent.ROM))
    before = files(target)
    arm, owned = apply(clean.read_file(ARM), before[ARM])
    verify_runtime(arm, release)
    target.replace_file(ARM, arm)
    after = files(target)
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {ARM}
    ROOT.mkdir()
    target.save(ROM)
    target.replace_file(ARM, before[ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    base.save(STORED, dict(candidate_sha256=base.digest(ROM), previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=sha256(arm).hexdigest(), changed_slot=owned, whole_parent_inverse=True))
    print('Staged one exact 16-byte ARM9 label slot with a complete parent inverse.')


def replay_startup():
    import sys

    FunctionType(startup.main.__code__, vars(startup) | dict(stage=sys.modules[__name__]))()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('stage', 'startup'))
    (stage if parser.parse_args().action == 'stage' else replay_startup)()
