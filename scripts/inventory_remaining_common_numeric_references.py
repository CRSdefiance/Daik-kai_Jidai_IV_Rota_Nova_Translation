"""Inventory numeric-ID leads without mistaking instruction bytes for consumers."""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

CLEAN = 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
IDS = set(range(3289, 3320)) | set(range(3393, 3607))


def reviewed_exclusions(arm9):
    """Require exact reviewed native uses before excluding coincidental IDs."""
    spans = (
        (0x4F940, 0x4F97C, 'f361cf9c7633460e2d9a0f761e8a75342d8a80dc0798dfdc2b27afb97a01d464'),
        (0x60DAC, 0x60DDC, 'f70479332215062a41a57a97006d32441bb2bb6fadbfbb9122d345b8c5702717'),
        (0x5A140, 0x5A174, '366ca605c6e54c8318e83b4204fea75c83ed87764b2bf903c7314c8b18827cbc'),
    )
    for lo, hi, digest in spans:
        if sha(arm9[lo:hi]) != digest:
            raise ValueError('Reviewed numeric-reference producer differs')
    expected = {0x13FF38: 0x02050D58, 0x1400C4: 0x02050D84,
                0x1446E4: 0x02060DCC, 0x5A16C: 3316}
    for offset, word in expected.items():
        if struct.unpack_from('<I', arm9, offset)[0] != word:
            raise ValueError('Reviewed numeric-reference owner differs')
    return {
        0x0213FF38: {'classification': 'low-half-of-function-pointer',
                     'full_word': expected[0x13FF38],
                     'reason': 'Constructor 0204F960 loads the table address from 0204F9D0 and stores it at object+10; this table word is the full pointer 02050D58, not message ID 3416.'},
        0x021400C4: {'classification': 'low-half-of-function-pointer',
                     'full_word': expected[0x1400C4],
                     'reason': 'Constructor 0204F958 loads the table address from 0204F9CC and stores it at object+1C4; this table word is the full pointer 02050D84, not message ID 3460.'},
        0x021446E4: {'classification': 'low-half-of-function-pointer',
                     'full_word': expected[0x1446E4],
                     'reason': 'Native constructors 02060DAC and 02060DCC install table 021446E4 at object+0; its first word is native function pointer 02060DCC, not message ID 3532.'},
        0x0205A16C: {'classification': 'stack-restoration-size',
                     'full_word': 3316,
                     'reason': '0205A144 and 0205A160 load this literal into ip, add it to sp and return; it is not passed to a COMMON accessor.'},
    }, [{'start': 0x02000000 + lo, 'end': 0x02000000 + hi,
         'sha256': digest} for lo, hi, digest in spans]


def main():
    path = Path('work/clean.nds')
    if sha(path.read_bytes()) != CLEAN:
        raise ValueError('Exact clean source required')
    image = NdsImage.open(path)
    arm9 = image.read_file('/__arm9__.bin')
    exclusions, reviewed_spans = reviewed_exclusions(arm9)
    altered = bytearray(arm9)
    altered[0x5A164] ^= 1
    try:
        reviewed_exclusions(altered)
    except ValueError:
        negative_rejected = True
    else:
        raise ValueError('Changed reviewed producer was incorrectly accepted')
    entries = common_message_entries(image.read_file('/COMMON/MESFILE.DK4'), arm9)
    sections = MainCodeFile(arm9, 0x02000000).sections
    components = [(f'arm9_section_{i}', s.ramAddress, bytes(s.data))
                  for i, s in enumerate(sections)]
    overlays = loadOverlayTable(image.rom.arm9OverlayTable,
                                lambda oid, fid: image.files[fid])
    components.extend((f'arm9_overlay_{i}', s.ramAddress, bytes(s.data))
                      for i, s in overlays.items())
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    rows = []
    for name, base, raw in components:
        # Include halfword tables; retain the alignment so accidental byte
        # coincidences can be separated from actual typed data later.
        for width, fmt in ((2, '<H'), (4, '<I')):
            for offset in range(0, len(raw) - width + 1, width):
                value = struct.unpack_from(fmt, raw, offset)[0]
                if value not in IDS:
                    continue
                address = base + offset
                lo, hi = max(0, offset - 24), min(len(raw), offset + 28)
                aligned_lo = lo & ~3
                context = [f'{ins.address:08X} {ins.mnemonic} {ins.op_str}'
                           for ins in cs.disasm(raw[aligned_lo:hi], base + aligned_lo)]
                references = []
                packed = struct.pack('<I', address)
                for other_name, other_base, other in components:
                    start = 0
                    while (found := other.find(packed, start)) >= 0:
                        references.append({'component': other_name,
                                           'runtime_address': other_base + found,
                                           'aligned': found % 4 == 0})
                        start = found + 1
                rows.append({'component': name, 'runtime_address': address,
                             'offset': offset, 'width': width, 'message_id': value,
                             'source': entries[value].text.decode('cp932'),
                             'context_hex': raw[lo:hi].hex(),
                             'arm_interpretation_not_code_proof': context,
                             'literal_address_references': references,
                             'classification': 'unreviewed-numeric-coincidence'})
                if name == 'arm9_section_0' and address in exclusions:
                    rows[-1].update(exclusions[address])
    report = {'status': 'numeric-leads-not-consumer-or-unused-proof',
              'source_rom_sha256': CLEAN,
              'components': [{'name': n, 'base': b, 'length': len(r),
                              'sha256': sha(r)} for n, b, r in components],
              'rows': rows,
              'reviewed_exclusion_spans': reviewed_spans,
              'changed_reviewed_producer_rejected': negative_rejected,
              'limitations': ['Computed IDs and base-plus-index producers may have no numeric match.',
                              'Instruction words and unrelated data may contain matching numbers.',
                              'Literal address matches do not establish dereference or reachability.',
                              'Halfword matches in a word are retained as separate leads.']}
    out = Path('work/analysis/remaining_common_numeric_references_clean.json')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'matches': len(rows), 'word_matches': sum(r['width'] == 4 for r in rows),
                      'address_referenced_matches': sum(bool(r['literal_address_references']) for r in rows)}))
    for row in rows:
        if row['width'] == 4 or row['literal_address_references']:
            print(row['component'], hex(row['runtime_address']), row['width'],
                  row['message_id'], len(row['literal_address_references']))


if __name__ == '__main__':
    main()
