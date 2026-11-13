"""Bind the original generic view getter, including cached-direct source views."""

import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/view_getters_v679')
ROM = Path('out/all_routes_combined_v678_candidate.nds')
PC = 0x020D4170


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    prior = read('work/analysis/wedding_dialogue_v678/final_verification.json')
    assert prior['two_source_faithful_dialogue_repairs_complete_tested_combined_ROM_and_exact_patch']
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, old = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    assert arm[0xD4170:0xD41A4] == old[0xD4170:0xD41A4]
    raw = CORE.read_bytes()
    assert sha(raw) == CORE_SHA
    base, table = tables(raw)
    word = struct.unpack_from('<I', arm, PC - 0x02000000)[0]
    index = ((word >> 16) & 0xFF0) | ((word >> 4) & 15)
    target = {'PC': PC, 'original_instruction': word, 'instruction_index': index,
              'handler_RVA': struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - base}
    assert index == 0x920
    save(ROOT / 'source_contract.json', {'core_sha256': CORE_SHA, 'interpreter_table': table, 'target': target,
        'original_getter_code_hex': arm[0xD4170:0xD41A4].hex(),
        'view_layout': {'owner': 12, 'cached_header': 16, 'type': 20, 'source_x': 28,
                        'source_y': 32, 'palette_halfword': 36, 'width': 40, 'height': 44},
        'type4_calls_owner_virtual_getter_other_types_return_cached_header': True,
        'source_assets': [{'path': p, 'bytes': len(rom.read_file(p)), 'sha256': sha(rom.read_file(p))}
            for p in ('/_pxl/__frame.pxl', '/_pxl/kakutei.pxl', '/_pxl/__marker.pxl')],
        'actual_entry_not_return_or_paint_completion': True})
    names = ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json', 'graphics_completion_requirements_v313.json')
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
            Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds'))},
        'all_original_audits_before': {n: read(Path('translations') / n) for n in names},
        'previous_goal_turn_classification': 'progress: V678 two dialogue repairs integrated,three cold boots and387-file final archive verified',
        'full_goal_complete': False})
    # The established ordinary editor schedule exercises views absent from getter-request traces.
    donor_report = Path('E:/Rota Nova translations/Generated/work/emulation_v193/keyboard_labels_v599/capture_report.json')
    report = read(donor_report)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded')
    inputs = ROOT / 'ordinary_editor_inputs.json'
    save(inputs, report['scripted_input_schedule'])
    save(ROOT / 'run_config.json', {'frames': report['frames'], 'inputs': str(inputs),
        'inputs_sha256': sha(inputs.read_bytes()), 'capture_frames': sorted({r['frame'] for r in report['frames_captured']}),
        'historical_schedule_report': str(donor_report), 'historical_schedule_report_sha256': sha(donor_report.read_bytes()),
        'new_capture_path_is_original_view_getter_not_earlier_two_pixel_primitives': True})
    print('V679 original cached/type4 view getter and ordinary editor schedule bound.', flush=True)


if __name__ == '__main__':
    main()
