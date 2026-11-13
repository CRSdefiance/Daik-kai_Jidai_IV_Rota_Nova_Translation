"""Bind original RAM-stream modes and their actual Save/Load caller returns."""

import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/memory_streams_v682')
ROM = Path('out/all_routes_combined_v678_candidate.nds')
BUFFERS = {1: 0x02249C40, 2: 0x02233040}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    for lo, hi in ((0xD010C, 0xD05F0), (0x46474, 0x46544), (0x46684, 0x46708), (0xD7650, 0xD7700)):
        assert arm[lo:hi] == original[lo:hi]
    assert struct.unpack_from('<2I', arm, 0xD0514) == (BUFFERS[1], BUFFERS[2])
    raw = CORE.read_bytes()
    assert sha(raw) == CORE_SHA
    base, table = tables(raw)
    targets = []
    for pc, name in ((0x020D0398, 'stream_open'), (0x02046498, 'mode1_original_caller_return'),
        (0x020466BC, 'mode2_original_caller_return'), (0x020D0340, 'stream_close')):
        word = struct.unpack_from('<I', arm, pc - 0x02000000)[0]
        index = ((word >> 16) & 0xFF0) | ((word >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': word, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - base})
    save(ROOT / 'source_contract.json', {'targets': targets, 'interpreter_table': table, 'core_sha256': CORE_SHA,
        'mode_buffers': {str(k): v for k, v in BUFFERS.items()},
        'open_owner_register': 'r0', 'known_caller_return_owner_register': 'r4',
        'fields': {'size_highwater': 8, 'RAM_backing': 28, 'cursor': 32, 'SDK_slot': 36},
        'source_assembler': 'scripts/observe_file_requests_v681.py',
        'source_assembler_sha256': sha(Path('scripts/observe_file_requests_v681.py').read_bytes())})
    historical = read('E:/Rota Nova translations/Generated/work/emulation_v193/save_load_plaques_v612_current/capture_report.json')
    donor = historical['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    save(ROOT / 'run_config.json', {'frames': historical['frames'],
        'inputs': 'work/analysis/save_load_plaques_v612/complete_inputs.json',
        'inputs_sha256': sha(Path('work/analysis/save_load_plaques_v612/complete_inputs.json').read_bytes()),
        'donor': donor['source'], 'donor_sha256': donor['source_sha256'],
        'capture_frames': sorted({r['frame'] for r in historical['frames_captured']}),
        'ordinary_Save_Load_slot_previews_and_actual_load_no_live_fixture': True})
    assert rom.read_file('/_pxl/saveloadinfo.pxl') == NdsImage.open('out/all_routes_combined_v612_candidate.nds').read_file('/_pxl/saveloadinfo.pxl')
    names = ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json', 'graphics_completion_requirements_v313.json')
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
            ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
            Path('out/raphael_natural_v2_accepted_base.nds'))},
        'all_original_audits_before': {n: read(Path('translations') / n) for n in names},
        'previous_goal_turn_classification': 'progress: V681 actual SDK requests,complete raw returns,all164 current Gallery positions and616-file archive verified',
        'full_goal_complete': False})
    print('V682 two fixed RAM-stream buffers and original Save/Load source paths bound.', flush=True)


if __name__ == '__main__':
    main()
