"""Observe the failing native prefix's first unmapped access without replacing it."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_MEM_INVALID, UcError, arm_const

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import replay_person_gender_v698 as replay
from scripts.trace_thumb_controls_v700 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    original_root, original_machine = replay.ROOT, replay.machine
    scratch = ROOT / 'native_IO_diagnostic'
    scratch.mkdir()
    preflight = original_root / 'preflight.json'
    (scratch / 'preflight.json').write_bytes(preflight.read_bytes())
    accesses = []

    def machine(arm):
        u = original_machine(arm)

        def missing(uc, access, address, size, value, unused):
            accesses.append({'PC': uc.reg_read(arm_const.UC_ARM_REG_PC), 'access': access,
                'address': address, 'size': size, 'value': value,
                'R0': uc.reg_read(arm_const.UC_ARM_REG_R0),
                'R1': uc.reg_read(arm_const.UC_ARM_REG_R1),
                'SP': uc.reg_read(arm_const.UC_ARM_REG_SP), 'LR': uc.reg_read(arm_const.UC_ARM_REG_LR)})
            return False  # Preserve the real failure; no mapped zero or invented I/O return.
        u.hook_add(UC_HOOK_MEM_INVALID, missing)
        return u
    replay.ROOT, replay.machine = scratch, machine
    try:
        replay.main()
    except UcError:
        pass
    else:
        raise AssertionError('Expected native failure was not reproduced')
    finally:
        replay.ROOT, replay.machine = original_root, original_machine
    failure = read(scratch / 'native_flag0_call1_failure.json')
    assert failure == read(original_root / 'native_flag0_call1_failure.json')
    assert len(accesses) == 1
    access = accesses[0]
    assert access['PC'] == 0x020E31E4 and access['address'] == access['R1'] == 0x04000204 and access['size'] == 2
    versions = []
    for path in (replay.ROM, Path('work/clean.nds')):
        arm = NdsImage.open(path).read_file('/__arm9__.bin')
        assert struct.unpack_from('<I', arm, 0xE31E4)[0] == 0xE1D100B0  # LDRH r0,[r1]
        assert struct.unpack_from('<I', arm, 0xE31F4)[0] == 0x04000204
        versions.append({'ROM': str(path), 'source_words_sha256': sha(arm[0xE31E0:0xE31F8])})
    save(ROOT / 'native_IO_diagnostic.json', {'unmapped_accesses': accesses, 'source_words': versions,
        'failure': failure, 'original_V698_failure_retained_unchanged': True,
        'first_failure_is_original_halfword_read_of_unmapped_DS_IO_04000204': True,
        'no_I_O_value_invented_no_read_bridge_no_hardware_access_or_state_substitution': True,
        'later_prefix_behavior_full_state_equivalence_and_V694_suffix_NOT_proven': True,
        'source_preflight_sha256': sha(preflight.read_bytes()),
        'replayer_sha256': sha(Path('scripts/replay_person_gender_v698.py').read_bytes()),
        'diagnostic_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V700 first V698 replay failure bound to original unmapped16-bit DS I/O read04000204; no fabricated value or equivalence claim.', flush=True)


if __name__ == '__main__':
    main()
