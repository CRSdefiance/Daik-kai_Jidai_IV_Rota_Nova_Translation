"""Localize the original first-discovery banner and its separate power notice."""

from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile

from dk4tool.patch.inn_numerals_20261119 import BASE, END, HELPER, ITCM, NUMBER, assemble, cache_plan, target
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import register_swimmer_leak_square_dialogue_20261120 as parent
from scripts import stage_swimmer_leak_square_dialogue_20261120 as batch
from scripts.stage_madeira_resupply_numerals_20261120 import HELPER_PROOF


ROOT = Path('work/ruin_discovery_20261120/staged_v1')
ROM, PROOF = ROOT / 'candidate.nds', ROOT / 'staging.json'
SOURCE_TITLE = '遺跡発見'
SOURCE_SUFFIX = 'を発見しました'
TITLE, SUFFIX = b'Ruins Found', b' discovered'
STRINGS = {0x16ECF4: (12, SOURCE_TITLE, TITLE), 0x16ED00: (12, SOURCE_TITLE, TITLE),
           0x16ED0C: (16, SOURCE_SUFFIX, SUFFIX)}
POWER_CALL, POWER_NOTICE = 0x020610DC, 288


def patch(arm, clean):
    # The first copy is measured for centering. The second is painted.
    assert unpack_from('<4I', arm, 0x106570) == (0x0216ECF4, 0x0216ED00, 0x022A44EC, 0x0216ED0C)
    assert all(arm[low:high] == clean[low:high] for low, high in ((0x60DEC, 0x60E4C),
        (0x61054, 0x610FC), (0x61C58, 0x61CD0), (0x10628C, 0x106344), (0x106570, 0x1065FC)))
    assert target(arm, 0x610DC) == NUMBER and target(arm, 0x610E8) == 0x020546B8
    assert unpack_from('<I', arm, 0x610E4)[0] == (0xE3A00E12)
    itcm, = [section for section in MainCodeFile(arm, BASE).sections if section.ramAddress == ITCM]
    existing = bytes.fromhex(batch.load(HELPER_PROOF)['helper_hex'])
    assert bytes(itcm.data[HELPER-ITCM:END-ITCM]) == existing
    output, slots = bytearray(arm), []
    for at, (size, source, english) in STRINGS.items():
        source_bytes = (source.encode('cp932') + b'\0').ljust(size, b'\0')
        assert clean[at:at+size] == arm[at:at+size] == source_bytes
        assert len(english) < size
        replacement = (english + b'\0').ljust(size, b'\0')
        output[at:at+size] = replacement
        slots.append(dict(offset=at, size=size, Japanese=source, original=source_bytes.hex(), replacement=replacement.hex()))
    at = POWER_CALL - BASE
    instruction = assemble(f'bl {HELPER}', POWER_CALL)
    assert len(instruction) == 4
    output[at:at+4] = instruction
    result = bytes(output)
    assert target(result, at) == HELPER and cache_plan(result) == cache_plan(arm)
    return result, slots, dict(address=POWER_CALL, before=arm[at:at+4].hex(), after=instruction.hex(),
                               message_ID=POWER_NOTICE, original_target=NUMBER, helper=HELPER)


def main():
    assert not ROOT.exists()
    previous = batch.load(parent.RELEASE)
    assert parent.base.digest(parent.ROM) == previous['candidate_sha256']
    assert parent.base.digest(batch.CLEAN) == previous['clean_input_sha256']
    assert parent.base.digest(parent.base.REGISTRY) == previous['registry_sha256']
    image, clean = map(batch.NdsImage.open, (parent.ROM, batch.CLEAN))
    arm, source = image.read_file(batch.ARM), clean.read_file(batch.ARM)
    assert batch.digest(arm) == previous['target_ARM9_sha256']
    deployed, slots, call = patch(arm, source)
    old = batch.files(image)
    image.replace_file(batch.ARM, deployed)
    new = batch.files(image)
    assert old.keys() == new.keys() and {key for key in old if old[key] != new[key]} == {batch.ARM}
    candidate = bytes(image.rom.save())
    image.replace_file(batch.ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    delta, rebuilt = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
    make_xdelta(batch.CLEAN, ROM, delta)
    apply_xdelta(batch.CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == candidate
    batch.write(PROOF, dict(candidate_sha256=batch.digest(candidate), parent_sha256=previous['candidate_sha256'],
        target_ARM9_sha256=batch.digest(deployed), target_COMMON_sha256=previous['target_COMMON_sha256'],
        source_slots=slots, power_call=call, source_first_discovery_dispatch=0x02060DEC,
        original_notice_entry=0x02106194, original_painter=0x02106590, original_filename='Iseki/akebono.pxl',
        exact_parent_inverse=True, clean_input_patch_sha256=parent.base.digest(delta), distinct_runtime_substitutions_preserved=True))
    print('Staged the centered ruin discovery heading, name line, and power notice digit correction.')


if __name__ == '__main__':
    main()
