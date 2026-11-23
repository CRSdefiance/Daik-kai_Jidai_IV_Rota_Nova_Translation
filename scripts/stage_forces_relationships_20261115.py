"""Localize three source-bound relationship formats in the Forces chart."""

from argparse import ArgumentParser
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from struct import unpack_from
import sys
from types import FunctionType

from scripts import register_market_info_trends_20261115 as parent
from scripts import replay_refit_help_startup_20261115 as startup
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.verify_release_baseline import files


base = parent.base
CLEAN, ARM = parent.stage.CLEAN, parent.stage.ARM
ROOT = Path('work/forces_relationships_staged_20261115_v1')
ROM = ROOT / 'Forces_Relationships_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
BASE = 0x02000000


@dataclass(frozen=True)
class Label:
    kind: str
    offset: int
    size: int
    pointer: int
    japanese: str
    english: str
    meaning: str
    reason: str

    @property
    def id(self):
        return f'FORCES_{self.kind.upper()}_FORMAT'


LABELS = (
    Label('allied', 0x14C244, 16, 0x8D810, '%sと同盟です', 'Allied with %s',
          'The selected faction is in an alliance with the named faction.',
          'Use Allied, the established relationship label, and keep the same company name.'),
    Label('war', 0x14C254, 24, 0x8D814, '%sと交戦中の勢力です', 'At war with %s',
          'The selected faction is currently at war with the named faction.',
          'At war with states the existing hostilities without predicting action or adding agency.'),
    Label('subordinate', 0x14C26C, 16, 0x8D818, '%sの傘下です', 'Subject to %s',
          'The selected faction is subordinate to the named faction.',
          'Subject to makes the direction of subordination clear and fits the original slot.'),
)


def apply(source, current):
    assert source[0x8D2F8:0x8D400] == current[0x8D2F8:0x8D400]
    assert source[0x3C858:0x3C8F4] == current[0x3C858:0x3C8F4]
    target = bytearray(current)
    ownership = []
    for row in LABELS:
        start, end = row.offset, row.offset + row.size
        original, english = row.japanese.encode('cp932'), row.english.encode('ascii')
        assert len(english) < row.size and len(original) < row.size
        assert original.count(b'%s') == english.count(b'%s') == 1
        assert original.count(b'%') == english.count(b'%') == 1
        before, after = original.ljust(row.size, b'\0'), english.ljust(row.size, b'\0')
        assert current[start:end] == source[start:end] == before
        assert unpack_from('<I', source, row.pointer) == unpack_from('<I', current, row.pointer) == (BASE + start,)
        target[start:end] = after
        ownership.append(dict(id=row.id, offset=start, size=row.size, pointer_field=row.pointer,
            clean_hex=before.hex(), previous_hex=before.hex(), target_hex=after.hex(), substitutions=['%s']))
    return bytes(target), ownership


def stage():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    clean, image = map(base.NdsImage.open, (CLEAN, parent.ROM))
    before = files(image)
    arm, ownership = apply(clean.read_file(ARM), before[ARM])
    verify_runtime(arm, release)
    image.replace_file(ARM, arm)
    after = files(image)
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {ARM}
    ROOT.mkdir()
    image.save(ROM)
    image.replace_file(ARM, before[ARM])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    base.save(STORED, dict(candidate_sha256=base.digest(ROM), previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=sha256(arm).hexdigest(), changed_slots=ownership, whole_parent_inverse=True))
    print('Staged three source-bound format slots. Complete parent inverse passed.')


def replay_startup():
    FunctionType(startup.main.__code__, vars(startup) | dict(stage=sys.modules[__name__]))()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('stage', 'startup'))
    (stage if parser.parse_args().action == 'stage' else replay_startup)()
