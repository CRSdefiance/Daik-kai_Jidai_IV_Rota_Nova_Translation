"""Bind original SDK filename requests and the known raw-reader entry/return."""

import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, SOURCE
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/file_requests_v681')
ROM = Path('out/all_routes_combined_v678_candidate.nds')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, source = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    for lo, hi in ((0xDED50, 0xDEDC4), (0x4704C, 0x470B4), (0x9ED3C, 0x9EE94)):
        assert arm[lo:hi] == source[lo:hi]
    raw = CORE.read_bytes()
    assert sha(raw) == CORE_SHA
    base, table = tables(raw)
    targets = []
    for pc, name in ((0x020DED50, 'SDK_open_entry'), (0x0204704C, 'raw_SLACK_entry'),
                     (0x0209EDEC, 'known_raw_SLACK_caller_return')):
        word = struct.unpack_from('<I', arm, pc - 0x02000000)[0]
        index = ((word >> 16) & 0xFF0) | ((word >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': word, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - base})
    mmu = SOURCE / 'MMU.cpp'
    assert 'DUP16(0x003FFFFF)' in mmu.read_text(encoding='utf-8')
    save(ROOT / 'source_contract.json', {'targets': targets, 'interpreter_table': table,
        'core_sha256': CORE_SHA, 'MMU_source': str(mmu), 'MMU_source_sha256': sha(mmu.read_bytes()),
        'DS_main_RAM_mirror_address_region': [0x02000000, 0x03000000], 'mask': 0x3FFFFF,
        'actual_filename_requests_not_open_return_or_every_SDK_interface': True})
    historical = read('work/analysis/gallery_caption_v523/save_fixture_manifest.json')
    fixture = dict(historical, production_ROM=str(ROM), production_ROM_sha256=sha(ROM.read_bytes()))
    assert sha(Path(fixture['fixture_save']).read_bytes()) == fixture['fixture_save_sha256']
    assert sha(Path(fixture['original_donor']).read_bytes()) == fixture['original_donor_sha256']
    save(ROOT / 'gallery_save_fixture_manifest.json', fixture)
    plan = read('work/analysis/gallery_v522/run_plan.json')
    ordinary = read('E:/Rota Nova translations/Generated/work/emulation_v193/wedding_dialogue_v678_ordinary/capture_report.json')
    inputs = ROOT / 'ordinary_inputs.json'
    save(inputs, ordinary['scripted_input_schedule'])
    save(ROOT / 'run_cases.json', {'gallery': {'frames': plan['final_frame'],
        'inputs': plan['input_schedule'], 'capture_frames': plan['capture_frames'],
        'save': fixture['fixture_save'], 'fixture_manifest': str(ROOT / 'gallery_save_fixture_manifest.json')},
        'ordinary': {'frames': 4000, 'inputs': str(inputs),
            'capture_frames': [1, 60, 180, 900, 1200, 1500, 1600, 1800, 2000, 2100, 2400, 2800, 3200, 3600, 3900, 4000]}})
    names = ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json', 'graphics_completion_requirements_v313.json')
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
            ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
            Path('out/raphael_natural_v2_accepted_base.nds'))},
        'all_original_audits_before': {n: read(Path('translations') / n) for n in names},
        'previous_goal_turn_classification': 'progress: V680 all21 original raw reads,42 scales,72 caption edges and68-file verified archive',
        'full_goal_complete': False})
    print('V681 original filename/raw entry/return targets and Event Scenes/ordinary schedules bound.', flush=True)


if __name__ == '__main__':
    main()
