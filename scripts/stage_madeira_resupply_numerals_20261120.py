"""Apply the registered ASCII-digit helper to the ordinary resupply price."""

from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile

from dk4tool.patch.inn_numerals_20261119 import BASE, END, HELPER, ITCM, NUMBER, assemble, cache_plan, target
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import stage_swimmer_leak_square_dialogue_20261120 as batch


ROOT = Path('work/madeira_resupply_numerals_20261120_v1')
PRICE_ONLY = Path('work/madeira_resupply_price_only_20261120_v1')
ROM, PROOF = ROOT / 'candidate.nds', ROOT / 'staging.json'
CALL = 0x020607D0
MESSAGE, WRAPPER = 49, 0x02053F9C
HELPER_PROOF = Path('releases/all_routes_editorial_20261119_inn_numerals_candidate_v2/verification/staged.json')


def patch(arm, clean):
    at = CALL - BASE
    assert arm[0x60784:0x60890] == clean[0x60784:0x60890], 'Original resupply branches changed'
    assert arm[NUMBER - BASE:0xABFC8] == clean[NUMBER - BASE:0xABFC8]
    assert target(arm, at) == NUMBER and target(arm, 0x607E0) == WRAPPER
    assert unpack_from('<4I', arm, 0x607C4) == (0xE3540000, 0x0A000006, 0xE1A00004, unpack_from('<I', arm, at)[0])
    assert unpack_from('<3I', arm, 0x607D4) == (0xE1A02000, 0xE59D000C, 0xE3A01000 | MESSAGE)
    itcm, = [s for s in MainCodeFile(arm, BASE).sections if s.ramAddress == ITCM]
    receipt = batch.load(HELPER_PROOF)
    helper = bytes.fromhex(receipt['helper_hex'])
    assert bytes(itcm.data[HELPER - ITCM:END - ITCM]) == helper
    instruction = assemble(f'bl {HELPER}', CALL)
    assert len(instruction) == 4
    patched = arm[:at] + instruction + arm[at+4:]
    assert target(patched, at) == HELPER and cache_plan(arm) == cache_plan(patched)
    return patched, dict(address=CALL, original_target=NUMBER, registered_digit_helper=HELPER,
                         before=arm[at:at+4].hex(), after=instruction.hex(), price_message=MESSAGE,
                         portrait_choice=WRAPPER, positive_price_branch=0x020607CC)


def main(price_only=False):
    stage = batch.load(batch.ROOT / 'staging.json')
    predecessor = batch.load(batch.PARENT)
    assert batch.digest(batch.ROM.read_bytes()) == stage['candidate_sha256']
    assert stage['parent_sha256'] == predecessor['candidate_sha256']
    assert batch.digest(batch.CLEAN.read_bytes()) == stage['clean_input_sha256']
    input_rom = Path(predecessor['candidate']) if price_only else batch.ROM
    input_sha = predecessor['candidate_sha256'] if price_only else stage['candidate_sha256']
    assert batch.digest(input_rom.read_bytes()) == input_sha
    current, clean = map(batch.NdsImage.open, (input_rom, batch.CLEAN))
    arm = current.read_file(batch.ARM)
    assert batch.digest(arm) == stage['target_ARM9_sha256'] == predecessor['target_ARM9_sha256']
    installed, binding = patch(arm, clean.read_file(batch.ARM))
    original = batch.files(current)
    current.replace_file(batch.ARM, installed)
    changed = batch.files(current)
    assert original.keys() == changed.keys() and {name for name in original if original[name] != changed[name]} == {batch.ARM}
    data = bytes(current.rom.save())
    current.replace_file(batch.ARM, arm)
    assert bytes(current.rom.save()) == input_rom.read_bytes()
    folder = PRICE_ONLY if price_only else ROOT
    folder.mkdir()
    rom = folder / ROM.name
    rom.write_bytes(data)
    delta, rebuilt = folder / 'translation.xdelta', folder / 'clean_rebuilt.nds'
    make_xdelta(batch.CLEAN, rom, delta)
    apply_xdelta(batch.CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == data
    batch.write(folder / PROOF.name, dict(candidate_sha256=batch.digest(data), staged_parent_sha256=stage['candidate_sha256'],
        immediate_parent_sha256=input_sha, price_only=price_only,
        registered_parent_sha256=stage['parent_sha256'], clean_input_sha256=stage['clean_input_sha256'],
        target_ARM9_sha256=batch.digest(installed), target_COMMON_sha256=batch.digest(original[batch.COMMON]),
        whole_staged_parent_inverse=True, clean_input_patch_sha256=batch.digest(delta.read_bytes()),
        helper_proof_sha256=batch.digest(HELPER_PROOF.read_bytes()), original_call=binding))
    print('Patched the original resupply price call and rebuilt the candidate from clean input.')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--price-only', action='store_true')
    main(parser.parse_args().price_only)
