"""Prepare a labeled copied system-save fixture using the original checksum."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_location_fixture_v519 import ARM_SHA
from scripts.probe_button_prompt_native import call, machine

ROM = Path('out/all_routes_combined_v518_candidate.nds')
DONOR = Path('E:/Rota Nova translations/Saves/maria-nagasaki-namahage-v514.dsv')
OUT = Path('work/analysis/gallery_v521')


def main():
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert sha(arm) == ARM_SHA
    assert arm[0xEEC50:0xEEC78] == clean[0xEEC50:0xEEC78]
    raw = DONOR.read_bytes()
    assert sha(raw) == 'fbae21aa2c5a695bde0eddfc10a3bbeb80d01478bd6a9ed743d824595dc3096e'
    assert raw[0x3C000:0x3C004] == b'DK4R'
    u = machine(arm)
    pointer = 0x023F0000

    def checksum(data):
        u.mem_write(pointer, bytes(data[0x3C000:0x3C800]))
        call(u, 0xEEC50, (pointer,))
        native = u.reg_read(UC_ARM_REG_R0)
        signed = sum(v if v < 128 else v - 256 for v in data[0x3C008:0x3C044]) & 0xFFFFFFFF
        assert native == signed
        return native

    assert checksum(raw) == struct.unpack_from('<I', raw, 0x3C004)[0]
    after = bytearray(raw)
    before_flags = struct.unpack_from('<H', raw, 0x3C03C)[0]
    struct.pack_into('<H', after, 0x3C03C, before_flags | 15)
    struct.pack_into('<I', after, 0x3C004, checksum(after))
    changes = [{'offset': i, 'before': a, 'after': b}
               for i, (a, b) in enumerate(zip(raw, after)) if a != b]
    allowed = set(range(0x3C004, 0x3C008)) | {0x3C03C, 0x3C03D}
    assert all(c['offset'] in allowed for c in changes)
    assert after[:0x3C000] == raw[:0x3C000]
    assert after[0x3C044:] == raw[0x3C044:]
    OUT.mkdir(parents=True, exist_ok=True)
    fixture = OUT / 'gallery-test-only.dsv'
    fixture.write_bytes(after)
    manifest = {'synthetic_gallery_fixture': True, 'earned_unlock_verified': False,
                'original_donor': str(DONOR), 'original_donor_sha256': sha(raw),
                'fixture_save': str(fixture), 'fixture_save_sha256': sha(after),
                'production_ROM': str(ROM), 'production_ROM_sha256': sha(ROM.read_bytes()),
                'native_checksum_entry': '0x020EEC50',
                'signed_byte_checksum_span': ['0x3C008', '0x3C044'],
                'system_flags_before': before_flags, 'system_flags_after': before_flags | 15,
                'changes': changes, 'all_six_route_save_slots_and_footer_unchanged': True,
                'only_system_low_four_bits_and_original_checksum_changed': True,
                'donor_save_unchanged': sha(DONOR.read_bytes()) == sha(raw)}
    (OUT / 'save_fixture_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Isolated Gallery save: original checksum validates; only system unlock bits and checksum differ; six route slots exact.')


if __name__ == '__main__':
    main()
