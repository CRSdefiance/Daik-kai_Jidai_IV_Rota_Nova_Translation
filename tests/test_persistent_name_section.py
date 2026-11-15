import json
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.rom.nds import NdsImage
from scripts.probe_persistent_name_section import prepare


def test_reserved_section_and_preserved_native_regions():
    saved, placement, shop = prepare()
    source = NdsImage.open('out/all_routes_combined_v147_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    before, current, original = [MainCodeFile(raw, 0x02000000) for raw in (source, saved, clean)]
    assert len(current.sections) == 4
    assert (current.sections[3].ramAddress, placement['heap_low']) == (0x02387A20, 0x02388000)
    assert len(current.sections[3].data) == 1504
    assert bytes(current.sections[1].data) == bytes(before.sections[1].data)
    assert bytes(current.sections[2].data) == bytes(original.sections[2].data)
    restored = bytearray(current.sections[0].data)
    spans = [(0x15D088, 0x15D0A0), (0xE45DC, 0xE45E0),
             (current.codeSettingsOffs, current.codeSettingsOffs + 8)]
    spans += [(move['field'], move['field'] + 4) for move in placement['moves']]
    spans += [(ref['field'], ref['field'] + 4) for ref in shop['references']]
    for begin, end in spans:
        restored[begin:end] = before.sections[0].data[begin:end]
    assert restored == before.sections[0].data
    assert saved[current.codeSettingsOffs + 12:current.codeSettingsOffs + 20] == source[current.codeSettingsOffs + 12:current.codeSettingsOffs + 20]


def test_all_complete_pointer_owners():
    saved, placement, _ = prepare()
    import struct
    payload = bytes(MainCodeFile(saved, 0x02000000).sections[3].data)
    for move in placement['moves']:
        pointer = struct.unpack_from('<I', saved, move['field'])[0]
        delta = pointer - placement['base']
        assert delta % 4 == 0
        assert payload[delta:].split(b'\0', 1)[0].decode('cp932') == move['text']
    assert len(placement['moves']) == 239


def test_native_persistence_evidence():
    proof = json.loads(Path('work/analysis/persistent_name_section_proof.json').read_text(encoding='utf-8'))
    assert proof['same_machine_sdk_arena_initialization_preserves_names']
    assert proof['scratch_preserves_complete_pool']
    assert proof['scratch_write_count'] == 173
