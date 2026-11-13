"""Extend all18 plaque audit records while preserving completion false."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_plaque_audit_native_v300 import DIGEST, ROM, ROOT, read


def main():
    native, live = read(ROOT / 'native_proof.json'), read(ROOT / 'live_proof.json')
    assert native['candidate_sha256'] == live['candidate_sha256'] == DIGEST == sha(ROM.read_bytes())
    assert len(live['plaque_cases']) == 61 and len(live['hint_cases']) == 5
    assert sum(len(r['complete_skill_lines']) for r in live['all40_complete_skill_label_value_lines']) == 40
    assert len(native['condition_glyph_cases']) == 13 and len(native['all470_native_framebuffer_paper_cases']) == 470
    checkpoint = {'documentation': 'docs/plaque_audit_v300.md', 'candidate_unchanged': str(ROM),
                  'candidate_sha256': DIGEST, 'complete_live_plaque_instances': 61,
                  'complete_independent_native_plaque_font_masks': 61,
                  'actual_Sailor_Info_characters': ['Lil', 'Camille', 'Emilio', 'Fernando'],
                  'actual_crew_allocations': [16, 0, 16], 'complete_live_skill_label_value_lines': 40,
                  'complete_live_hint_surfaces': 5, 'complete_live_name_captions': 4,
                  'full_native_gender_cells_palette48': 4, 'current_native_selector_cases': 512,
                  'current_complete_condition_rasters': 13, 'current_skill_formatter_cases': 50,
                  'current_guarded_native_framebuffer_paper_cases': 470,
                  'all17_source_labels_and_style_review_retained': True,
                  'all_observed_PXL_paper_edges_and_letters_exact': True,
                  'ROM_fix_required_for_observed_cases': False,
                  'all18_entries_and_Armor_Weapon_variants_remain_incomplete': True,
                  'occupied_Armor_Weapon_actual_alternate_health_mood_and_other_route_contexts_pending': True,
                  'two_cold_boot_runs_no_savestate_or_RAM_injection': True,
                  'capture_frame_counts': [11200, 14400],
                  'native_proof': str(ROOT / 'native_proof.json'), 'native_proof_sha256': sha((ROOT / 'native_proof.json').read_bytes()),
                  'live_proof': str(ROOT / 'live_proof.json'), 'live_proof_sha256': sha((ROOT / 'live_proof.json').read_bytes()),
                  'preview': str(ROOT / 'current_plaque_review.png'), 'preview_visually_reviewed': True,
                  'Online_translation_exemption_preserved': True, 'full_goal_complete': False}
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        data = read(path)
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        group = data['plaque_style_v247']
        inventory = group['ongoing_plaque_inventory']
        assert len(inventory) == 18 and not group['full_plaque_audit_complete']
        for row in inventory:
            assert not row['fully_completed']
            row['latest_scoped_coverage_proof'] = str(ROOT / 'live_proof.json')
            row['latest_current_ROM_native_proof'] = str(ROOT / 'native_proof.json')
            row['latest_audit_checkpoint'] = 'V300'
            for variant in row.get('observed_variants', []):
                assert not variant['fully_completed']
                variant['latest_current_empty_slot_pixel_proof'] = str(ROOT / 'live_proof.json')
        data['plaque_audit_v300'] = checkpoint
        assert data['latest_candidate_sha256'] == DIGEST
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V300: continued plaque audit on current V299

Two fresh ordinary-input cold boots verify 61 complete plaque instances across
three crew allocations and four Sailor Info characters. Every paper/bevel pixel
and independent native letter is exact, plus 40 complete skill/value lines,
five hint placements, four full names and four source-bank gender cells. Current
native checks cover 512 selectors, all 13 condition rasters, 50 numeric formats
and 470 bounded framebuffer paper surfaces. No observed-case ROM fix is needed;
V299 remains latest. All 18 audit entries and Armor/Weapon variants remain open,
including occupied equipment and actual alternate condition/route contexts.
Online image exemption retained. See [V300 audit](plaque_audit_v300.md).

'''
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if '## V300:' not in text:
            title, rest = text.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print('V300 current native/live evidence recorded for all18 entries; none marked fully complete; V299 unchanged.')


if __name__ == '__main__':
    main()
