"""Reuse calibrated width, guard and page planning with exact source preambles."""
from pathlib import Path
from types import FunctionType, SimpleNamespace
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import plan_editorial_scene_prose_v12 as previous


def qualify_source(doc):
    assert doc['file_path'] == '/data/SC1.DK4'
    clean = Path('work/clean.nds')
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    blocks = IlnkContainer.parse(NdsImage.open(clean).read_file(doc['file_path'])).blocks
    bindings = []
    for row in doc['records']:
        if row['kind'] == 'typed-choice-label':
            continue
        ref = row['source_reference']
        raw = bytes.fromhex(row['source_hex'])
        header = bytes.fromhex(row['source_complete_preamble_hex'])
        block = blocks[row['block']]
        assert block[ref['offset']:ref['offset'] + len(raw) + 1] == raw + b'\0'
        assert block[ref['header_offset']:ref['header_offset'] + len(header)] == header
        assert len(header) == 6 and header[:2] == b'\0@' and header[-1] == row['source_selector'] == raw[0]
        assert row['source_selector'] != 0 and row.get('native_object_kind') != '4100-style-alternative'
        bindings.append(dict(id=row['id'], source_reference=ref, source_complete_preamble_hex=header.hex(),
            source_body_sha256=sha(raw), no_virtual_prefix_oractor0=True))
    assert len(bindings) == 433
    return set(), bindings


inherited = previous.main.__globals__['previous']
parameters = {**vars(inherited), 'PAIRS': inherited.PAIRS | {
    ('silla', 'gold'), ('gold', 'crown'), ('king', 'muryeong'), ('tomb', 'of'),
    ('jigger', 'spanker'), ('square', 'sails'), ('sail', 'handlers'), ('ahead', 'of'),
    ('senior', 'fellow'), ('fellow', 'student'), ('sao', 'jorge'), ('home-baked', 'bread'),
    ('collecting', 'paintings'), ('at', 'last'), ('of', 'course'), ('thank', 'goodness'),
    ('all', 'right'), ('a', 'little'), ('each', 'other'), ('my', 'master'), ('your', 'master')}}
main = FunctionType(previous.main.__code__, {**previous.main.__globals__, 'qualify_source': qualify_source,
    'previous': SimpleNamespace(**parameters), '__file__': __file__}, argdefs=previous.main.__defaults__)


if __name__ == '__main__':
    main()
