"""Record full observed shared upload coverage, preserving final GPU limits."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.research_fls_shared_upload_v334 import ROM, ROOT


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    path = ROOT / 'all_shared_upload_proof.json'
    proof = read(path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    rows = proof['cases']
    assert len(rows) == 270 and len({(r['path'], r['tick']) for r in rows}) == 270
    assert len({(r['path'], c['texture']) for r in rows for c in r['current']['complete_shared_visible_texture_checks']}) == 260
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    a, b = current.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    for left, right in ((0xFE138, 0xFE208), (0xFFD14, 0x10044C), (0xE04E8, 0xE09C0), (0xE2034, 0xE231C)):
        assert a[left:right] == b[left:right]
    assert all(r['current_clean_bindings_and_material_commands_exact'] for r in rows)
    assert all(r[v]['all_native_queues_idle'] for r in rows for v in ('current', 'clean'))
    assert all(c['all_simultaneously_visible_rows_and_palette_bytes_exact']
               for r in rows for v in ('current', 'clean') for c in r[v]['complete_shared_visible_texture_checks'])
    summary = {'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
               'proof': str(path), 'proof_sha256': sha(path.read_bytes()),
               'observed_combinations': 270, 'current_clean_shared_pipeline_fixtures': 540,
               'distinct_compressed_texture_entries': 260,
               'current_checked_visible_and_palette_bytes': sum(c['visible_row_bytes_checked'] + c['palette_bytes_checked']
                                                            for r in rows for c in r['current']['complete_shared_visible_texture_checks']),
               'clean_checked_visible_and_palette_bytes': sum(c['visible_row_bytes_checked'] + c['palette_bytes_checked']
                                                          for r in rows for c in r['clean']['complete_shared_visible_texture_checks']),
               'all_concurrent_visible_rows_and_palettes_match_each_ROM_independent_decode': True,
               'original_bind_decode_upload_and_SDK_physical_address_selection_execute': True,
               'all_native_queues_drained': True,
               'copied_pose_captured_globals_immediate_DMA_LCDC_memory_are_contracts': True,
               'lifetime_recycling_GPU_aliases_clipping_blending_final_pixels_and_actual_playback_still_open': True,
               'raw_root_intended_loader_and_usage_still_open': True,
               'all18_plaques_and_variants_still_incomplete': True,
               'Online_low_resolution_images_exempt': True,
               'ROM_modified': False, 'full_goal_complete': False,
               'documentation': 'docs/fls_shared_upload_v334.md'}
    out = ROOT / 'summary.json'
    out.write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        target = Path('translations') / name
        audit = read(target)
        assert audit['latest_candidate_sha256'] == proof['candidate_sha256']
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in audit['plaque_style_v247']['ongoing_plaque_inventory'])
        audit['FLS_shared_native_upload_v334'] = summary
        audit['current_goal_turn_classification'] = 'progress270-observed-shared-native-bind-decode-upload-pipelines'
        target.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
