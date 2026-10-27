"""Isolated item/site collection flags, bounded by original Gallery dispatch."""

import argparse
import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROM = Path('out/all_routes_combined_v525_candidate.nds')
DONOR = Path('work/analysis/gallery_v521/gallery-test-only.dsv')
OUT = Path('work/analysis/collection_gallery_v526')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site-ids', type=int, nargs='+')
    parser.add_argument('--skip-items', action='store_true')
    parser.add_argument('--out', type=Path, default=OUT)
    args = parser.parse_args()
    sites = list(range(21)) if args.site_ids is None else args.site_ids
    assert len(set(sites)) == len(sites) and all(0 <= i < 21 for i in sites)
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x41EF4:0x41FC0] == clean[0x41EF4:0x41FC0]
    for offset, word in [(0x41F0C, 0xE35000C6), (0x41F34, 0xE5D33018),
                         (0x41F78, 0xE3500015), (0x41FA0, 0xE5D33034)]:
        assert struct.unpack_from('<I', arm, offset)[0] == word
    prior_manifest = json.loads(Path('work/analysis/gallery_v521/save_fixture_manifest.json').read_text())
    raw = DONOR.read_bytes()
    assert sha(raw) == prior_manifest['fixture_save_sha256']
    original = Path(prior_manifest['original_donor']).read_bytes()
    assert sha(original) == prior_manifest['original_donor_sha256']
    u = machine(arm)

    def checksum(data):
        u.mem_write(0x023F0000, bytes(data[0x3C000:0x3C800]))
        call(u, 0xEEC50, (0x023F0000,))
        value = u.reg_read(UC_ARM_REG_R0)
        assert value == sum(v if v < 128 else v - 256 for v in data[0x3C008:0x3C044]) & 0xFFFFFFFF
        return value

    assert checksum(raw) == struct.unpack_from('<I', raw, 0x3C004)[0]
    after = bytearray(raw)
    ranges = []
    for name, offset, bits in [('items', 0x3C01C, [] if args.skip_items else list(range(198))),
                               ('historic_sites', 0x3C038, sites)]:
        for bit in bits:
            after[offset + bit // 8] |= 1 << (bit % 8)
        ranges.append({'collection': name, 'save_byte_offset': offset, 'selected_bits': bits,
                       'valid_bit_count': 198 if name == 'items' else 21})
    struct.pack_into('<I', after, 0x3C004, checksum(after))
    changes = [{'offset': i, 'before': a, 'after': b}
               for i, (a, b) in enumerate(zip(raw, after)) if a != b]
    permitted = set(range(0x3C004, 0x3C008)) | set(range(0x3C01C, 0x3C035)) | set(range(0x3C038, 0x3C03B))
    assert all(c['offset'] in permitted for c in changes)
    assert after[:0x3C000] == raw[:0x3C000] and after[0x3C044:] == raw[0x3C044:]
    assert (after[0x3C034] & 0xC0) == (raw[0x3C034] & 0xC0)
    assert (after[0x3C03A] & 0xE0) == (raw[0x3C03A] & 0xE0)
    args.out.mkdir(parents=True, exist_ok=True)
    save = args.out / 'collection-gallery-test-only.dsv'
    save.write_bytes(after)
    manifest = {'synthetic_gallery_fixture': True, 'earned_unlock_verified': False,
                'synthetic_collection_history': True, 'natural_acquisition_or_discovery_verified': False,
                'original_donor': prior_manifest['original_donor'], 'original_donor_sha256': sha(original),
                'parent_fixture': str(DONOR), 'parent_fixture_sha256': sha(raw),
                'fixture_save': str(save), 'fixture_save_sha256': sha(after),
                'production_ROM': str(ROM), 'production_ROM_sha256': sha(ROM.read_bytes()),
                'original_Gallery_dispatch_range': ['0x02041EF4', '0x02041FC0'],
                'collection_ranges': ranges, 'changes': changes,
                'native_signed_byte_checksum_verified': True,
                'all_six_route_slots_footer_unrelated_system_bits_unchanged': True}
    (args.out / 'save_fixture_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Isolated collection fixture prepared: {0 if args.skip_items else 198} items/{len(sites)} sites; source dispatch, checksum and route slots preserved.')


if __name__ == '__main__':
    main()
