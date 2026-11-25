"""Matched raw16 source/opacity controls in a compatible live cache widget."""

import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as checks
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.prepare_standalone_tiles_v702 import BORROWED, PRE_FRAMES, contents
from scripts.probe_button_prompt_native import machine
from scripts.run_room_gender_v694 import ROM
from scripts.run_small_controls_v701 import BASE, ORIGINAL_POSITION, POSITION, TARGETS
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/raw_caption_v703')
FRAME, BOX = 6, (40, 96, 112, 128)
TILES = [[0, 0, 48, 28], [48, 0, 24, 28], [0, 28, 48, 4], [48, 28, 24, 4]]
CASES = {}
for case in ('source', 'opaque_CONTROL', 'baseline'):
    baseline = case == 'baseline'
    CASES[case] = {'group': 'source' if baseline else case, 'baseline': baseline,
        'legacy_source': '/GRP/SLACKIMG.DK4:block19:frame6:box40,96,112,128',
        'path': '/_pxl/__marker.pxl' if baseline else BORROWED,
        'owner': 0x02313F74 if baseline else 0x023139C0,
        'rect': [232, 96, 16, 16] if baseline else TILES[0], 'bank': 48 if baseline else 0,
        'tiles': TILES, 'sample_frames': [6080, 6180, 6280, 6380],
        'restore_frame': 6401, 'exit_frame': 6501, 'final_frame': 6800,
        'capture_frames': [*PRE_FRAMES, 6080, 6180, 6280, 6380, 6480, 6600, 6800]}


def caption(image):
    block = IlnkContainer.parse(image.read_file('/GRP/SLACKIMG.DK4')).blocks[19]
    assert len(block) == 21 * 320 * 240 * 2
    frame = block[FRAME * 153600:(FRAME + 1) * 153600]
    assert not any(w & 0x8000 for (w,) in struct.iter_unpack('<H', frame))
    marks = b''.join(frame[(y * 320 + 175) * 2:(y * 320 + 229) * 2] for y in range(96, 136))
    assert sha(marks) == '3b0111f01e8f7a0857a723f28138d130e29caad046aa5d15f7367831ac1d6943'
    assert BOX[2] <= 175  # The opacity control cannot include the preserved marks.
    x0, y0, x1, y1 = BOX
    crop = b''.join(frame[(y * 320 + x0) * 2:(y * 320 + x1) * 2] for y in range(y0, y1))
    assert len(crop) == 72 * 32 * 2
    return crop, {'archive_sha256': sha(image.read_file('/GRP/SLACKIMG.DK4')),
        'block19_sha256': sha(block), 'frame6_sha256': sha(frame), 'caption_crop_sha256': sha(crop),
        'original_brown_marks_bytes': len(marks), 'original_brown_marks_sha256': sha(marks)}


def main():
    ROOT.mkdir()
    parent = NdsImage.open(ROM)
    pixels, source = caption(parent)
    header = struct.pack('<5I', 16, 72, 32, 20, 20)
    before, research = contents(parent), {}
    for case in ('source', 'opaque_CONTROL'):
        payload = pixels if case == 'source' else struct.pack('<2304H', *(w | 0x8000 for (w,) in struct.iter_unpack('<H', pixels)))
        image = NdsImage.open(ROM)
        image.replace_file(BORROWED, header + payload)
        path = ROOT / 'research_roms' / (case + '_RAW16_CAPTION_NOT_PLAYABLE_RELEASE.nds')
        image.save(path)
        reloaded = NdsImage.open(path)
        after = contents(reloaded)
        assert set(after) == set(before) and [p for p in before if before[p] != after[p]] == [BORROWED]
        assert after[BORROWED] == header + payload and reloaded.path_map() == parent.path_map()
        assert all(bytes(getattr(reloaded.rom, f)) == bytes(getattr(parent.rom, f))
                   for f in ('arm9OverlayTable', 'arm7OverlayTable', 'iconBanner'))
        research[case] = {'path': str(path), 'sha256': sha(path.read_bytes()),
            'borrowed_file_sha256': sha(header + payload), 'borrowed_file_bytes': len(header + payload),
            'explicit_source_header_not_original_comic_descriptor': [16, 72, 32, 20, 20],
            'source_payload_high_bits_preserved': case == 'source',
            'only_opacity_control_sets_bit15_low15_RGB_exact': case == 'opaque_CONTROL',
            'only_borrowed_slot_file_changes_no_production_archive_or_mark_change': True}
    core = CORE.read_bytes()
    assert sha(core) == CORE_SHA
    native_base, table = tables(core)
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in (ROM, 'work/clean.nds')]
    targets = []
    for pc, name in TARGETS:
        words = [bytes(machine(a).mem_read(pc, 4)) for a in arms]
        assert words[0] == words[1]
        value = int.from_bytes(words[0], 'little')
        index = ((value >> 16) & 0xFF0) | ((value >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': value, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', core, table['file_offset'] + index * 8)[0] - native_base})
    for address, xy in ((POSITION, (192, 64)), (ORIGINAL_POSITION, (84, 76))):
        assert all(struct.unpack_from('<2I', a, address - BASE) == xy for a in arms)
    save(ROOT / 'source_contract.json', {'targets': targets, 'interpreter_table': table,
        'cases': CASES, 'research_ROMs': research, 'source': source,
        'compatible_generic_raw16_widget_not_rejected_fixed_indexed8_event_canvas': True,
        'original_comic_parent_descriptor_geometry_or_opacity_policy_NOT_proven': True})
    old = checks.ROOT
    checks.ROOT = ROOT
    try:
        checks.main()
    finally:
        checks.ROOT = old
    inputs = [r for r in read('work/analysis/equipment_cursor_v663/inputs.json') if r['start'] <= 5901]
    for case in CASES:
        save(ROOT / (case + '_inputs.json'), [*inputs, {'start': 6501, 'duration': 8, 'buttons': ['B']}])
    donor = read('work/analysis/equipment_cursor_v663/preflight.json')
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('work/clean.nds'),
        Path('out/raphael_natural_v2_accepted_base.nds'))
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in paths}, 'research_ROMs': research,
        'source': source, 'donor': donor['donor'], 'donor_sha256': donor['donor_sha256'],
        'producer_sha256': sha(Path('scripts/run_raw_caption_v703.py').read_bytes()),
        'preparer_sha256': sha(Path(__file__).read_bytes()),
        'fixture_methods_sha256': sha(Path('scripts/run_gender_exception_v697.py').read_bytes()),
        'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'case_input_hashes': {c: sha((ROOT / (c + '_inputs.json')).read_bytes()) for c in CASES},
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V702 complete copyright/ship source coverage and version-bound native lower states',
        'full_goal_complete': False})
    print('V703 matched raw16 caption source/opacity controls and original baseline pinned; no production changes.', flush=True)


if __name__ == '__main__':
    main()
