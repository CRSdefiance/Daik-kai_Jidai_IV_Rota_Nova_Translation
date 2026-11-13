"""Record complete native compressed FLS decoding; retain raw/display gaps."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.research_fls_payload_v311 import ROOT
from scripts.research_fls_stream_v310 import ROM, SNAPSHOT


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    proof_path = ROOT / 'all_compressed_proof.json'
    proof, largest = read(proof_path), read(ROOT / 'largest_case.json')
    digest, ram = sha(ROM.read_bytes()), SNAPSHOT.read_bytes()
    capture = read('work/emulation_v193/sailing_conditions_v309/capture_report.json')
    assert proof['candidate_sha256'] == largest['candidate_sha256'] == capture['ROM_sha256'] == digest
    assert sha(ram) == capture['read_only_RAM_snapshot']['sha256']
    assert capture['cold_boot'] and not capture['savestate_loaded']
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    for start, end in ((0xFDED0, 0xFE138), (0xFE218, 0xFE79C), (0xFFB7C, 0x100050), (0xE2C20, 0xE2D4C)):
        assert arm[start:end] == ram[start:end]
    cases = proof['cases']
    assert len(cases) == 520 and len({(r['path'], r['texture']) for r in cases}) == 260
    assert len({r['path'] for r in cases}) == 14
    assert all(r['inspection'].get('pass') and r['inspection']['native_saved_register_stack_and_outer_guards_preserved'] for r in cases)
    assert largest['cases'][0]['inspection']['pass']
    assert largest['cases'][0]['inspection']['length'] == 131072
    assert len(largest['cases'][0]['inspection']['chunks']) == 4
    assert all(r['kind'] in ('palette', 'pixels') for r in cases)
    total = sum(r['inspection']['length'] for r in cases)
    checkpoint = {'candidate_unchanged': str(ROM), 'candidate_sha256': digest,
                  'documentation': 'docs/fls_payload_decode_v311.md',
                  'native_palette_cases': 260, 'native_pixel_cases': 260,
                  'actual_compressed_FLS_files': 14, 'complete_decoded_bytes_verified': total,
                  'all_native_register_stack_and_outer_guards_pass': True,
                  'largest_background_bytes_exact_after_four_overlapping_requests': 131072,
                  'original_heap_setup_and_SDK_EOF_short_reads_modeled': True,
                  'only_filesystem_SDK_operations_bridged': True,
                  'native_queue_parameters_and_inert_upload_destination_are_contracts': True,
                  'GPU_upload_palette_banks_projection_crops_and_gameplay_not_claimed': True,
                  'raw_root_not_cleared_by_compressed_queue_exploration': True,
                  'native_proof': str(proof_path), 'native_proof_sha256': sha(proof_path.read_bytes()),
                  'largest_case_proof': str(ROOT / 'largest_case.json'),
                  'raw_root_exploration': str(ROOT / 'exploration.json'),
                  'all11_legacy_native_layout_gates_and18_plaques_remain_open': True,
                  'low_resolution_Online_images_translation_exempt': True,
                  'ROM_modified': False, 'full_goal_complete': False}
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        data = read(path)
        assert data['latest_candidate_sha256'] == digest
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in data['plaque_style_v247']['ongoing_plaque_inventory'])
        data['FLS_payload_decode_v311'] = checkpoint
        data['current_goal_turn_classification'] = 'progress520-complete-native-compressed-FLS-palette-pixel-cases'
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V311: complete native compressed FLS palette/pixel decoding

All260 compressed textures across14 FLS files pass original queued palette and
pixel reads/decompression:520 complete byte comparisons with native registers,
stack and guards intact. The largest131,072-byte M22 background passes after
following four overlapping native requests through queue idle. SDK end-of-file
short reads and original movie heap setup are retained in the controlled harness.
Only filesystem operations are bridged; GPU upload/composition is uncredited.
The raw root does not pass this compressed queue exploration and remains open,
along with11 legacy layout gates and18 plaques. No ROM change; V309 current.
Online images exempt. See [V311 evidence](fls_payload_decode_v311.md).

'''
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        if '## V311:' not in content:
            title, rest = content.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print(json.dumps({'native_cases': 520, 'decoded_bytes_verified': total, 'current_candidate': 'V309', 'goal_complete': False}))


if __name__ == '__main__':
    main()
