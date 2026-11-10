"""Reuse calibrated formatting with this batch's exact actor0/style source bindings."""
import struct
from pathlib import Path
from types import FunctionType

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import plan_editorial_scene_prose_v12 as previous


def qualify_source(doc):
    assert doc['file_path'] == '/data/SC1.DK4'
    clean_path = Path('work/clean.nds')
    assert sha(clean_path.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    blocks = IlnkContainer.parse(NdsImage.open(clean_path).read_file(doc['file_path'])).blocks
    zeros, bindings, style_ids = set(), [], set()
    zero_ids = set()
    for row in doc['records']:
        if row['kind'] == 'typed-choice-label':
            continue
        reference = row['source_reference']
        block = blocks[row['block']]
        raw = bytes.fromhex(row['source_hex'])
        assert block[reference['offset']:reference['offset'] + len(raw)] == raw
        if row.get('native_object_kind') == '4100-style-alternative':
            at = reference['command_offset']
            header = bytes.fromhex(row['source_header_hex'])
            assert row['block'] == 133 and at == 10
            assert len(header) == 20 and header[:2] == b'\0A'
            assert block[at:at + 20] == header and header[18:20] == b'\0\xd6'
            offsets = struct.unpack_from('<8H', header, 2)
            assert all(at + 20 + offsets[i] == reference['offset'] for i in row['source_style_indices'])
            assert block[reference['offset'] + len(raw)] == 0 and b'\0' not in raw
            style_ids.add(row['id'])
            bindings.append(dict(id=row['id'], source_reference=reference, source_header_hex=header.hex(),
                                 source_body_hex=raw.hex(), formatter_only_virtual_source_hex=(b'\xd6' + raw).hex(),
                                 prefix_not_stored_in_alternative=True))
        elif row['source_selector'] == 0:
            header = bytes.fromhex(row['source_complete_preamble_hex'])
            assert row['block'] == 143 and header.hex() == '0040ffff0000'
            assert block[reference['header_offset']:reference['header_offset'] + 6] == header
            assert raw[0] == 0 and b'\0' not in raw[1:] and block[reference['offset'] + len(raw)] == 0
            zeros.add(raw)
            zero_ids.add(row['id'])
            bindings.append(dict(id=row['id'], source_reference=reference,
                                 complete_source_preamble_hex=header.hex(), source_body_with_real_selector_hex=raw.hex(),
                                 original_Rafael_identity_proof='work/analysis/Hodram_B131_B150_clean_20261102/native_identity_reuse_checkpoint.json',
                                 actual_B143_gameplay_pending=True))
    assert zero_ids == {'DK4_MES_B143_R0079', 'DK4_MES_B143_R0087'}
    assert style_ids == {f'SC1_B133_STYLE_10_{i}' for i in range(8)}
    assert len(zeros) == 2 and len(bindings) == 10
    return zeros, bindings


main = FunctionType(previous.main.__code__,
                    {**previous.main.__globals__, 'qualify_source': qualify_source, '__file__': __file__},
                    argdefs=previous.main.__defaults__)

if __name__ == '__main__':
    main()
