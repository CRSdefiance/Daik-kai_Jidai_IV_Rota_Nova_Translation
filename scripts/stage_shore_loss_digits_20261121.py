"""Use regular-width digits for the original shared Search sailor-loss notice."""

from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile
from dk4tool.patch import inn_numerals_20261119 as number
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import register_shore_phrase_wraps_20261121 as parent
from scripts.stage_madeira_resupply_numerals_20261120 import HELPER_PROOF


base, batch = parent.base, parent.batch
ARM, COMMON, CLEAN = parent.stage.ARM, parent.stage.COMMON, parent.stage.CLEAN
CONTEXTS, CHECKPOINTS = parent.stage.CONTEXTS, parent.stage.CHECKPOINTS
LEAD = CHECKPOINTS / 'shore_sailor_loss_digits_20261121_v1.json'
BASE = number.BASE
ROOT = Path('work/shore_loss_digits_20261121')
ROM, PROOF = ROOT / 'Shore_Loss_Digits_STAGED.nds', ROOT / 'staged.json'
PATCH, REBUILT = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
CALL, EFFECT, MODAL, MESSAGE = 0x02079710, 0x020796A4, 0x020546B8, 312
CALLERS = (0x02079250, 0x020793D8, 0x0207946C, 0x02079578, 0x02079674)
SPANS = ((0x791E4, 0x7972C), (0xABF50, 0xABFD0))


def patch(arm, clean):
    assert all(arm[a:b] == clean[a:b] for a, b in SPANS)
    assert all(number.target(arm, pc - BASE) == EFFECT for pc in CALLERS)
    assert number.target(arm, 0x79708) == 0x020AAF38
    assert number.target(arm, 0x7971C) == MODAL
    assert unpack_from('<2I', arm, 0x79714) == (0xE1A01000, 0xE3A00F4E)
    assert number.target(arm, CALL - BASE) == number.NUMBER
    itcm, = (s for s in MainCodeFile(arm, BASE).sections if s.ramAddress == number.ITCM)
    helper = bytes(itcm.data[number.HELPER - number.ITCM:number.END - number.ITCM])
    assert helper.hex() == base.load(HELPER_PROOF)['helper_hex']
    at = CALL - BASE
    instruction = number.assemble(f'bl {number.HELPER}', CALL)
    assert len(instruction) == 4
    patched = arm[:at] + instruction + arm[at + 4:]
    assert number.target(patched, at) == number.HELPER
    assert patched[:at] + arm[at:at + 4] + patched[at + 4:] == arm
    assert number.cache_plan(patched) == number.cache_plan(arm)
    return patched, dict(address=CALL, previous_hex=arm[at:at + 4].hex(), revised_hex=instruction.hex(),
                         original_target=number.NUMBER, current_target=number.HELPER,
                         original_effect=EFFECT, effect_callers=list(CALLERS), original_modal=MODAL, message_ID=MESSAGE,
                         exact_source_spans=[[a + BASE, b + BASE] for a, b in SPANS])


def main():
    assert not ROOT.exists()
    release, lead = map(base.load, (parent.RELEASE, LEAD))
    assert base.digest(parent.ROM) == lead['candidate_sha256'] == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256'] and base.digest(base.REGISTRY) == release['registry_sha256']
    image, clean = map(base.NdsImage.open, (parent.ROM, CLEAN))
    arm = image.read_file(ARM)
    assert batch.digest(arm) == release['target_ARM9_sha256']
    corrected, binding = patch(arm, clean.read_file(ARM))
    before = batch.files(image)
    image.replace_file(ARM, corrected)
    after = batch.files(image)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {ARM}
    target = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(target)
    make_xdelta(CLEAN, ROM, PATCH)
    apply_xdelta(CLEAN, PATCH, REBUILT)
    assert REBUILT.read_bytes() == target
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), parent_sha256=release['candidate_sha256'],
                         clean_input_sha256=release['clean_input_sha256'], target_ARM9_sha256=batch.digest(corrected),
                         target_COMMON_sha256=release['target_COMMON_sha256'], call=binding, complete_parent_inverse=True,
                         patch_sha256=base.digest(PATCH), exact_clean_patch_reconstruction=True,
                         source_evidence={str(p): base.digest(p) for p in (LEAD, HELPER_PROOF)}))
    print('Staged the one-call Search count glyph correction.', flush=True)


if __name__ == '__main__':
    main()

