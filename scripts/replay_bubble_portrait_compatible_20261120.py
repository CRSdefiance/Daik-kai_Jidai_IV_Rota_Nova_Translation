"""Run the proven earlier bubbles voyage with only the revised lookout record."""

from argparse import ArgumentParser
from hashlib import sha256
from types import FunctionType

from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import register_sea_event_dialogue_followup_20261118 as history
from scripts import replay_bubble_portrait_wraps_20261120 as earlier


stage, base = earlier.stage, earlier.base
ROOT = stage.ROOT / 'compatible_fixture'
ROM, PROOF = (ROOT / filename for filename in ('Bubble_Voyage_RESEARCH_ONLY.nds', 'compatible_fixture.json'))
LIVE = ROOT / 'focused'
BOUND_PANELS = (461, 463, 469, 470, 478)
SPANS = ((0x30F04, 0x30F20), (0x31EC0, 0x325CC), (0x53BD8, 0x54164), (0x118800, 0x118860))


def records(image):
    arm = image.read_file(stage.ARM)
    return stage.owned_entries(image.read_file(stage.COMMON), arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())


def prepare():
    assert not ROOT.exists()
    own, former = map(base.load, (stage.PROOF, history.RELEASE))
    assert base.digest(history.ROM) == former['candidate_sha256']
    assert base.digest(stage.ROM) == own['candidate_sha256']
    source, current = map(base.NdsImage.open, (history.ROM, stage.ROM))
    previous_arm, current_arm = (img.read_file(stage.ARM) for img in (source, current))
    assert all(previous_arm[lo:hi] == current_arm[lo:hi] for lo, hi in SPANS)
    assert source.read_file('/GRP/KANJI.FNT') == current.read_file('/GRP/KANJI.FNT')
    active, target = map(records, (source, current))
    before = source.read_file(stage.COMMON)
    assert active[461].text != target[461].text
    after, visible, allocation = stage.owned_deployment(before, previous_arm, active, {461: target[461].text})
    assert all(visible[k].text == target[k].text for k in BOUND_PANELS)
    source.replace_file(stage.COMMON, after)
    candidate = bytes(source.rom.save())
    source.replace_file(stage.COMMON, before)
    assert bytes(source.rom.save()) == history.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), earlier_working_ROM_sha256=former['candidate_sha256'],
        staged_current_ROM_sha256=own['candidate_sha256'], exact_visible_records={k: visible[k].text.hex() for k in BOUND_PANELS},
        inherited_instruction_and_table_spans=[{'start': lo, 'end': hi, 'sha256': sha256(previous_arm[lo:hi]).hexdigest()}
                                              for lo, hi in SPANS],
        complete_earlier_ROM_inverse=True, current_font_bytes_exact=True, allocation=allocation,
        earlier_release_sha256=base.digest(history.RELEASE), staged_proof_sha256=base.digest(stage.PROOF)))


old_setter = FunctionType(earlier.prior.set_condition.__code__, vars(earlier.prior) | {'ROM': ROM})
set_condition = FunctionType(earlier.set_condition.__code__, vars(earlier) | {'old_setter': old_setter})


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'play'))
    if parser.parse_args().action == 'prepare':
        prepare()
    else:
        earlier.run(LIVE, 'from scripts.replay_bubble_portrait_compatible_20261120 import set_condition', rom=ROM, proof=PROOF)
