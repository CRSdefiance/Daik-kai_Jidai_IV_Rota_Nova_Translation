"""Save new native consumer evidence without closing unresolved display gates."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.research_graphics_file_open_v301 import DIGEST, ROM, ROOT


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    proof, arguments = read(ROOT / 'proof.json'), read(ROOT / 'caller_argument_proof.json')
    assert sha(ROM.read_bytes()) == proof['candidate_sha256'] == arguments['candidate_sha256'] == DIGEST
    assert len(proof['constant_filename_cases']) == 20 and len(proof['caller_supplied_filename_cases']) == 5
    assert len(proof['generated_FLS_native_cases']) == 35
    assert len(arguments['captain_dependent_movie_argument_cases']) == 4
    checkpoint = {'documentation': 'docs/graphics_file_open_v301.md', 'candidate_unchanged': str(ROM),
                  'candidate_sha256': DIGEST, 'all_current_main_sections_and_declared_overlays_scanned': True,
                  'SDK_direct_open_callers': 25, 'constant_filename_callers': 20, 'supplied_filename_callers': 5,
                  'native_generated_FLS_valid_paths': 14, 'native_rejection_or_missing_cases': 21,
                  'FLS_direct_parent_callers': 6, 'actual_captured_captain_argument_cases': 4,
                  'captain_selected_FLS_indices': [29, 30, 31, 32],
                  'whole_file_reader_formats': [r['actual_format'] for r in arguments['whole_file_generated_formats']],
                  'literal_callers_and_generated_loader_bytes_exact_clean': True,
                  'SDK_existence_result_is_only_bridge': True,
                  'native_decoder_full_parent_playback_GPU_and_root_m02_03_consumer_pending': True,
                  'generic_computed_indirect_legacy_consumers_not_ruled_out': True,
                  'no_raw_comic_viewer_or_global_unused_archive_claim': True,
                  'all11_legacy_native_layout_composition_gates_remain_open': True,
                  'all18_plaques_and_variants_incomplete': True,
                  'low_resolution_Online_image_translation_exemption_preserved': True,
                  'native_proof': str(ROOT / 'proof.json'), 'native_proof_sha256': sha((ROOT / 'proof.json').read_bytes()),
                  'caller_proof': str(ROOT / 'caller_argument_proof.json'),
                  'caller_proof_sha256': sha((ROOT / 'caller_argument_proof.json').read_bytes()),
                  'next_action': 'Trace original FLS decoding/playback and cached-descriptor/stream readers; preserve legacy raw-display gates.',
                  'ROM_modified': False, 'full_goal_complete': False}
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        data = read(path)
        assert data['latest_candidate_sha256'] == DIGEST
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in data['plaque_style_v247']['ongoing_plaque_inventory'])
        data['graphics_file_open_v301'] = checkpoint
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V301: broader native graphics file-opening census

Current main sections/overlays have 25 SDK-open callers: 20 literal paths and
five supplied/generated names. The original FLS loader constructs all 14 /FLS
family names; 21 rejected/missing cases preserve native return/stack behavior.
Six direct FLS parent callers are identified. Actual captured captain data makes
the original getter/caller select M29 through M32. Whole-file reader formats are
evstill%03u.pxl and towngrp%02u.pxl. Decoder/playback/GPU, root m02_03 and indirect
legacy readers remain open; no raw-comic viewer or global unused-data claim.
No ROM change; V299 stays latest. All 18 plaques stay incomplete and Online
images exempt. See [V301 consumer evidence](graphics_file_open_v301.md).

'''
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if '## V301:' not in text:
            title, rest = text.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print('V301 native reader/caller evidence recorded; no ROM change; unresolved display gates retained.')


if __name__ == '__main__':
    main()
