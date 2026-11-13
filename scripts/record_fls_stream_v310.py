"""Credit complete native FLS parsing without claiming textures or gameplay."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.research_fls_stream_v310 import ROM, ROOT


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    stream = read(ROOT / 'proof.json')
    descriptors = read(ROOT / 'cached_descriptor_callers.json')
    digest = sha(ROM.read_bytes())
    assert stream['candidate_sha256'] == descriptors['candidate_sha256'] == digest
    assert len(stream['cases']) == 15 and sum(r['texture_record_count'] for r in stream['cases']) == 261
    assert all(r['native_constructor_and_full_stream_parser_return_pass'] for r in stream['cases'])
    assert all(r['constructor_parser_saved_register_stack_return_and_outer_guards_pass'] for r in stream['cases'])
    assert len(descriptors['native_direct_argument_cases']) == 21 and len(descriptors['resource_families']) == 9
    assert len(descriptors['virtual_method_literal_still_requires_context']) == 1
    checkpoint = {'candidate_unchanged': str(ROM), 'candidate_sha256': digest,
                  'documentation': 'docs/fls_stream_and_descriptors_v310.md',
                  'complete_native_FLS_stream_parse_cases': 15,
                  'texture_table_records_loaded_in_exact_native_metadata_prefixes': 261,
                  'native_FINF_canvas_all15': [256, 192],
                  'root_FLS_native_stream_parse_supported': True,
                  'root_FLS_actual_trigger_texture_decode_projection_and_crop_proved': False,
                  'native_cached_descriptor_argument_cases': 21, 'unique_PXL_descriptor_paths': 9,
                  'virtual_cached_descriptor_method_unclassified': 1,
                  'all11_legacy_native_layout_gates_and_all18_plaques_remain_open': True,
                  'low_resolution_Online_images_translation_exempt': True,
                  'stream_proof': str(ROOT / 'proof.json'), 'stream_proof_sha256': sha((ROOT / 'proof.json').read_bytes()),
                  'descriptor_proof': str(ROOT / 'cached_descriptor_callers.json'),
                  'descriptor_proof_sha256': sha((ROOT / 'cached_descriptor_callers.json').read_bytes()),
                  'ROM_modified': False, 'full_goal_complete': False,
                  'next_original_native_path': 'Texture payload reads/decompression and movie texture/view composition; virtual descriptor context.'}
    for filename in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / filename
        data = read(path)
        assert data['latest_candidate_sha256'] == digest
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        group = data['plaque_style_v247']
        assert len(group['ongoing_plaque_inventory']) == 18 and not group['full_plaque_audit_complete']
        assert all(not row['fully_completed'] for row in group['ongoing_plaque_inventory'])
        data['FLS_stream_and_cached_descriptors_v310'] = checkpoint
        data['current_goal_turn_classification'] = 'progress-complete15-native-FLS-parsers-and21-captured-descriptor-arguments'
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V310: full native FLS stream parsing and cached descriptors

All15 actual FLS files execute the original stream constructor/parser through
native return, using genuine captured global state and SDK filesystem bridges.
All declared metadata prefixes and261 texture-table records are loaded exactly;
native table/command/FINF pointers,256x192 canvases, registers and outer guards
pass. Root m02_03 is accepted by this generic reader, but its actual trigger,
texture decode, projection and crop remain unproved. All21 direct cached-graphics
arguments resolve through actual captured descriptors to nine PXL paths; one
virtual method remains to map. No globally-unused legacy claim is made. No ROM
change: V309 remains current. All11 legacy layout gates and18 plaques stay open;
Online images exempt. See [V310 evidence](fls_stream_and_descriptors_v310.md).

'''
    for filename in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / filename
        content = path.read_text(encoding='utf-8')
        if '## V310:' not in content:
            title, rest = content.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print('V310 records15 complete native parsers and21 descriptor arguments; V309 current; full goal and all18 plaques remain open.')


if __name__ == '__main__':
    main()
