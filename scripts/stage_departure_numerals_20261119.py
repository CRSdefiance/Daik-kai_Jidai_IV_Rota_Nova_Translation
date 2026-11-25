"""Use the installed regular-digit adapter at the three departure number calls."""

from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile

from dk4tool.patch.inn_numerals_20261119 import BASE, HELPER, ITCM, NUMBER, assemble, cache_plan, target
from scripts import register_inn_numerals_20261119 as inn
from scripts import register_rafael_sail_controls_20261119 as parent
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime

base, native = parent.base, parent.native
STAGED = ROOT = Path('work/departure_numerals_20261119/staged_v1')
ROM, PROOF = ROOT / 'Departure_Numerals_STAGED.nds', ROOT / 'staged.json'
ARM, COMMON = native.ARM, '/COMMON/MESFILE.DK4'
SITES = {0x02060BEC: (85, 0x02060BF8), 0x0207A2E4: (86, 0x0207A330), 0x0207A2F4: (86, 0x0207A330)}
CALLER_SPANS = ((0x60BD0, 0x60BFC), (0x7A2DC, 0x7A334), (0xABF50, 0xABFC8))


def recompile(arm, clean, helper):
    assert all(arm[a:b] == clean[a:b] for a, b in CALLER_SPANS)
    itcm, = (s for s in MainCodeFile(arm, BASE).sections if s.ramAddress == ITCM)
    assert bytes(itcm.data[HELPER-ITCM:HELPER-ITCM + len(helper)]) == helper
    output, details = bytearray(arm), []
    for call, (message, display) in SITES.items():
        at, endpoint = call - BASE, display - BASE
        assert target(arm, at) == NUMBER and target(arm, endpoint) == 0x020546B8
        assert unpack_from('<I', arm, endpoint - 4)[0] == 0xe3a00000 | message
        code = assemble(f'bl {HELPER}', call)
        assert len(code) == 4
        output[at:at + 4] = code
        details.append(dict(message_ID=message, call=call, display=display, before=arm[at:at + 4].hex(), after=code.hex()))
    installed = bytes(output)
    assert all(target(installed, call - BASE) == HELPER for call in SITES)
    assert cache_plan(installed) == cache_plan(arm)
    return installed, details


def main():
    assert not ROOT.exists()
    previous = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == previous['registry_sha256']
    assert base.digest(parent.ROM) == previous['candidate_sha256']
    assert base.digest(native.CLEAN) == previous['clean_input_sha256']
    image = base.NdsImage.open(parent.ROM)
    source = base.NdsImage.open(native.CLEAN)
    arm = image.read_file(ARM)
    assert native.digest(arm) == previous['target_ARM9_sha256']
    installed_helper = inn.VERIFY / 'staged.json'
    helper = bytes.fromhex(base.load(installed_helper)['helper_hex'])
    installed, details = recompile(arm, source.read_file(ARM), helper)
    verify_runtime(installed, previous)
    image.replace_file(ARM, installed)
    target_rom = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(target_rom)
    base.save(PROOF, dict(predecessor_sha256=previous['candidate_sha256'], candidate_sha256=base.digest(ROM),
        clean_input_sha256=previous['clean_input_sha256'], target_ARM9_sha256=native.digest(installed),
        target_COMMON_sha256=previous['target_COMMON_sha256'], helper_hex=helper.hex(), original_calls=details,
        entire_parent_inverse=True, evidence={str(p): base.digest(p) for p in (parent.RELEASE, installed_helper, Path(__file__))}))
    print('Staged the three original departure digit calls. The whole ROM reverses to its registered parent.')


if __name__ == '__main__':
    main()
