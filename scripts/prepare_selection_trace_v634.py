"""Apply the existing bounded observer to V633 for new selection-menu research."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_blitter_trace_abi_v603 as abi
from scripts.prepare_blitter_trace_v603 import (
    CAPACITY,
    CONTROL,
    CORNER,
    END,
    ENTRY,
    FIELDS,
    RECORDS,
    STRIDE,
    TILE,
    TILE_ENTRY,
    build_body,
)
from scripts.probe_common_display_name_hook import branch_link
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/selection_contexts_v634')
SOURCE = Path('out/all_routes_combined_v633_candidate.nds')


def main():
    digest = sha(SOURCE.read_bytes())
    assert digest == 'eea7c88cd8c6082cf56a8779421018913f2ef9b40ca3cc77fe1d1b13b74ec05f'
    rom = NdsImage.open(SOURCE)
    arm = rom.read_file('/__arm9__.bin')
    code, before = MainCodeFile(arm, 0x02000000), MainCodeFile(arm, 0x02000000)
    assert len(code.sections) == 5
    assert all(not (s.ramAddress < END and ENTRY < s.ramAddress + len(s.data) + s.bssSize) for s in code.sections)
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda _id, fid: rom.rom.files[fid])[0]
    clean = NdsImage.open('work/clean.nds')
    original = loadOverlayTable(clean.rom.arm9OverlayTable, lambda _id, fid: clean.rom.files[fid])[0]
    assert overlay.ramAddress == 0x01FFA000 and len(overlay.data) == 6208
    assert overlay.data == original.data and overlay.flags == 0
    section = next(s for s in code.sections if s.ramAddress <= CORNER < s.ramAddress + len(s.data))
    at = CORNER - section.ramAddress
    assert section.data[at:at + 4] == bytes.fromhex('f0432de9')
    tile = bytearray(overlay.data)
    assert tile[TILE - overlay.ramAddress:TILE - overlay.ramAddress + 4] == bytes.fromhex('f04f2de9')
    body = build_body()
    payload = bytearray(END - ENTRY)
    payload[:len(body)] = body
    struct.pack_into('<I', payload, CONTROL - ENTRY + 20, 0x603B117)
    code.sections.append(MainCodeFile.Section(payload, ENTRY, 0))
    struct.pack_into('<I', section.data, at, branch_link(CORNER, ENTRY) & ~0x01000000)
    struct.pack_into('<I', tile, TILE - overlay.ramAddress, branch_link(TILE, TILE_ENTRY) & ~0x01000000)
    revised = bytes(code.save())
    restored = MainCodeFile(revised, 0x02000000)
    for i, old in enumerate(before.sections):
        new = bytearray(restored.sections[i].data)
        assert restored.sections[i].ramAddress == old.ramAddress and len(new) == len(old.data)
        if old.ramAddress == section.ramAddress:
            new[at:at + 4] = old.data[at:at + 4]
        if i == 0:
            settings = code.codeSettingsOffs
            new[settings:settings + 12] = old.data[settings:settings + 12]
        assert bytes(new) == bytes(old.data)
    rom.replace_file('/__arm9__.bin', revised)
    rom.rom.files[overlay.fileID] = bytes(tile)
    ROOT.mkdir(parents=True, exist_ok=True)
    target = ROOT / 'selection_trace_RESEARCH_ONLY.nds'
    rom.save(target)
    saved, source = NdsImage.open(target), NdsImage.open(SOURCE)
    files = {p: b for _, p, b in saved.iter_files()} | dict(saved.iter_components())
    old_files = {p: b for _, p, b in source.iter_files()} | dict(source.iter_components())
    assert files.keys() == old_files.keys()
    changed = sorted(p for p in files if files[p] != old_files[p])
    assert changed == ['/__arm9__.bin', '/__unnamed__/file_00000.bin']
    assert saved.rom.arm9OverlayTable == source.rom.arm9OverlayTable
    manifest = {'research_only': True, 'production_ROM': str(SOURCE), 'production_ROM_sha256': digest,
                'research_ROM': str(target), 'research_ROM_sha256': sha(target.read_bytes()),
                'changed_components': changed, 'new_autoload_section': [ENTRY, END],
                'helper_body_bytes': len(body), 'helper_body_sha256': sha(body),
                'observer_identical_to_V603': True, 'corner_hook': CORNER, 'tile_hook': TILE,
                'tile_entry': TILE_ENTRY, 'control': CONTROL, 'records': RECORDS,
                'capacity': CAPACITY, 'record_stride': STRIDE, 'fields': FIELDS,
                'original_resources_getters_crops_palettes_and_draw_inputs_preserved': True,
                'instrumentation_can_change_timing_no_guide_credit': True,
                'script_sha256': sha(Path(__file__).read_bytes()), 'production_changed': False,
                'full_goal_complete': False}
    save(ROOT / 'fixture_manifest.json', manifest)
    abi.ROOT = ROOT
    abi.main()
    print('V634 diagnostic-only observer prepared and ABI checked;production unchanged.')


if __name__ == '__main__':
    main()
