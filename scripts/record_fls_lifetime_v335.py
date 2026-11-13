"""Record native continuous allocator/job lifetimes; preserve actual GPU gates."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.research_fls_lifetime_v335 import ROM, ROOT
from scripts.research_fls_stream_v310 import SNAPSHOT


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    path = ROOT / 'all_lifetimes_proof.json'
    proof = read(path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    rows = proof['cases']
    assert len(rows) == 15 and len({r['path'] for r in rows}) == 15
    assert all(r['current_clean_native_allocation_lifetimes_exact'] for r in rows)
    for row in rows:
        for variant in ('current', 'clean'):
            result = row[variant]
            assert result['native_terminal_state'] == 3
            assert result['original_cleanup_leaves_no_tracked_live_keys_or_pending_jobs']
            assert result['all_live_native_allocation_intervals_nonoverlapping']
            assert result['all_update_service_cleanup_returns_saved_registers_stack_pass']
            for kind in ('texture', 'palette'):
                events = [e for e in result['allocation_free_events'] if e['kind'] == kind]
                assert sum(e['operation'] == 'allocate' for e in events) == sum(e['operation'] == 'free' for e in events)
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    a, b, ram = current.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin'), SNAPSHOT.read_bytes()
    for left, right in ((0xFD338, 0xFD4F8), (0xFDF00, 0xFE050), (0xFFA04, 0x10044C), (0x10AB8C, 0x10AF10)):
        assert a[left:right] == b[left:right] == ram[left:right]
    calls = sum(r['current']['continuous_native_update_calls'] for r in rows)
    alloc = sum(e['operation'] == 'allocate' for r in rows for e in r['current']['allocation_free_events'])
    reuse = sum(r['current']['freed_keys_reused_count'] for r in rows)
    summary = {'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
               'proof': str(path), 'proof_sha256': sha(path.read_bytes()),
               'complete_current_clean_continuous_lifetimes': 15,
               'native_update_calls_each_version': calls,
               'native_allocations_and_matched_frees_each_version': alloc,
               'previously_freed_keys_reallocated_each_version': reuse,
               'maximum_live_texture_allocations': max(r['current']['maximum_live_texture_allocations'] for r in rows),
               'all_native_key_lifetimes_match_source_without_overlap': True,
               'all_original_cleanup_no_tracked_keys_or_pending_jobs': True,
               'original_lifecycle_loader_allocator_and_cancel_code_source_exact': True,
               'captured_globals_no_geometry_VBlank_and_immediate_DMA_are_contracts': True,
               'continuous_GPU_data_fetch_timing_alias_clipping_blending_pixels_actual_playback_still_open': True,
               'raw_root_original_loader_usage_not_inferred': True,
               'all18_plaques_and_variants_still_incomplete': True,
               'Online_low_resolution_images_exempt': True,
               'ROM_modified': False, 'full_goal_complete': False,
               'documentation': 'docs/fls_lifetime_v335.md'}
    out = ROOT / 'summary.json'
    out.write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        target = Path('translations') / name
        audit = read(target)
        assert audit['latest_candidate_sha256'] == proof['candidate_sha256']
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in audit['plaque_style_v247']['ongoing_plaque_inventory'])
        audit['FLS_continuous_native_lifetimes_v335'] = summary
        audit['current_goal_turn_classification'] = 'progress15-continuous-original-resource-lifetimes-and-cleanup'
        target.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
