"""Exact standalone art in research-only cache slots; no production changes."""

import struct
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as checks
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.probe_button_prompt_native import machine
from scripts.run_room_gender_v694 import ROM
from scripts.run_small_controls_v701 import BASE, ORIGINAL_POSITION, POSITION, TARGETS
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/standalone_tiles_v702')
BORROWED = '/_pxl/kakutei.pxl'
SOURCES = {'copyright': ('/_pxl/copyright.pxl', 256, 16), 'ship': ('/_pxl/ship_eurL.pxl', 312, 246)}
PRE_FRAMES = (1, 60, 180, 1600, 2000, 2400, 2800, 3200, 3500, 3900, 4300, 4700, 5100, 5500, 5900)
CASES = {}
for group, (path, width, height) in SOURCES.items():
    tiles = [[x, y, min(48, width - x), min(28, height - y)]
             for y in range(0, height, 28) for x in range(0, width, 48)]
    samples = [6080 + i * 100 for i in range(len(tiles))]
    restore, exit_frame = samples[-1] + 21, samples[-1] + 121
    for baseline in (False, True):
        case = ('baseline_' if baseline else '') + group
        CASES[case] = {'group': group, 'baseline': baseline, 'legacy_source': path,
            'path': '/_pxl/__marker.pxl' if baseline else BORROWED,
            'owner': 0x02313F74 if baseline else 0x023139C0,
            'rect': [232, 96, 16, 16] if baseline else tiles[0], 'bank': 48 if baseline else 0,
            'tiles': tiles, 'sample_frames': samples, 'restore_frame': restore, 'exit_frame': exit_frame,
            'final_frame': exit_frame + 299,
            'capture_frames': [*PRE_FRAMES, *samples, restore + 79, exit_frame + 99, exit_frame + 299]}


def contents(image):
    return {p: data for _, p, data in image.iter_files()} | dict(image.iter_components())


def make_research(parent, group):
    path, width, height = SOURCES[group]
    source = parent.read_file(path)
    assert source == NdsImage.open('work/clean.nds').read_file(path)
    pxl = PxlImage.from_bytes(source)
    assert (pxl.bits_per_pixel, pxl.width, pxl.height) == (8, width, height)
    image = NdsImage.open(ROM)
    before = contents(image)
    image.replace_file(BORROWED, source)
    target = ROOT / 'research_roms' / (group + '_BORROWED_SLOT_NOT_PLAYABLE_RELEASE.nds')
    image.save(target)
    restored = NdsImage.open(target)
    after = contents(restored)
    assert set(after) == set(before)
    assert [p for p in before if before[p] != after[p]] == [BORROWED]
    assert restored.path_map() == parent.path_map()
    for field in ('arm9OverlayTable', 'arm7OverlayTable', 'iconBanner'):
        assert bytes(getattr(restored.rom, field)) == bytes(getattr(parent.rom, field))
    assert after[BORROWED] == source
    return {'path': str(target), 'sha256': sha(target.read_bytes()), 'group': group,
        'only_changed_file_or_code_component': BORROWED, 'source_path': path,
        'whole_source_PXL_sha256': sha(source), 'whole_source_PXL_bytes': len(source),
        'file_ids_all_other_file_data_ARM9_ARM7_overlays_banner_exact': True,
        'ROM_layout_FAT_offsets_may_rebuild_not_claimed_byte_identical': True,
        'research_slot_fixture_not_registered_release_or_original_filename_consumer': True}


def main():
    ROOT.mkdir()
    parent = NdsImage.open(ROM)
    research = {g: make_research(parent, g) for g in SOURCES}
    arm, clean = [NdsImage.open(p).read_file('/__arm9__.bin') for p in (ROM, 'work/clean.nds')]
    for address, xy in ((POSITION, (192, 64)), (ORIGINAL_POSITION, (84, 76))):
        assert all(struct.unpack_from('<2I', a, address - BASE) == xy for a in (arm, clean))
    core = CORE.read_bytes()
    assert sha(core) == CORE_SHA
    native_base, table = tables(core)
    targets = []
    for pc, name in TARGETS:
        words = [bytes(machine(a).mem_read(pc, 4)) for a in (arm, clean)]
        assert words[0] == words[1]
        value = int.from_bytes(words[0], 'little')
        index = ((value >> 16) & 0xFF0) | ((value >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': value, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', core, table['file_offset'] + index * 8)[0] - native_base})
    save(ROOT / 'source_contract.json', {'targets': targets, 'interpreter_table': table,
        'cases': CASES, 'research_ROMs': research,
        'native_tiled_widget_not_whole_image_normal_scene_or_original_consumer': True})
    previous = checks.ROOT
    checks.ROOT = ROOT
    try:
        checks.main()
    finally:
        checks.ROOT = previous
    source_inputs = [r for r in read('work/analysis/equipment_cursor_v663/inputs.json') if r['start'] <= 5901]
    for case, config in CASES.items():
        save(ROOT / (case + '_inputs.json'), [*source_inputs,
            {'start': config['exit_frame'], 'duration': 8, 'buttons': ['B']}])
    donor = read('work/analysis/equipment_cursor_v663/preflight.json')
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('work/clean.nds'),
        Path('out/raphael_natural_v2_accepted_base.nds'))
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
        'research_ROMs': research, 'donor': donor['donor'], 'donor_sha256': donor['donor_sha256'],
        'producer_sha256': sha(Path('scripts/run_standalone_tiles_v702.py').read_bytes()),
        'preparer_sha256': sha(Path(__file__).read_bytes()),
        'fixture_methods_sha256': sha(Path('scripts/run_gender_exception_v697.py').read_bytes()),
        'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'case_input_hashes': {c: sha((ROOT / (c + '_inputs.json')).read_bytes()) for c in CASES},
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V701 all six exact control widgets and complete restored screen comparisons',
        'full_goal_complete': False})
    print('V702 two exact source-file research slots,69 complete-cover tiles and two normal baseline schedules pinned.', flush=True)


if __name__ == '__main__':
    main()
