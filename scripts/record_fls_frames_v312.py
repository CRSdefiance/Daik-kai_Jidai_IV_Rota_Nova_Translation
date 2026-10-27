"""Record source-identical native timelines and pre-GPU quad preparation."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.research_fls_frames_v312 import ROOT
from scripts.research_fls_stream_v310 import ROM, SNAPSHOT


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    path = ROOT / 'all_files_proof.json'
    proof, ram = read(path), SNAPSHOT.read_bytes()
    digest = sha(ROM.read_bytes())
    capture = read('work/emulation_v193/sailing_conditions_v309/capture_report.json')
    assert proof['candidate_sha256'] == capture['ROM_sha256'] == digest
    assert sha(ram) == capture['read_only_RAM_snapshot']['sha256']
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    a, b = current.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    for start, end in ((0xFD4F8, 0xFDC60), (0xFEB28, 0xFEFCC), (0x100390, 0x1003CC), (0xDFA88, 0xDFD00)):
        assert a[start:end] == b[start:end] == ram[start:end]
    rows = proof['cases']
    assert len(rows) == 15
    assert all(r['clean_source_native_states_and_geometry_exact'] and r['frames']['error'] is None for r in rows)
    assert all(r['frames']['states'][-1]['return'] == 5 for r in rows)
    calls = sum(r['frames']['native_update_calls'] for r in rows)
    states = sum(len(r['frames']['states']) for r in rows)
    quads = sum(len(s['previous_buffer_geometry']) for r in rows for s in r['frames']['states'])
    assert calls == 45058 and states >= 4276 and quads >= 11035
    subtitle_cases = []
    wanted = {'/FLS/M20.fls': {27: 168}, '/FLS/M22.fls': {1: 176, 2: 176}, '/FLS/M24.fls': {3: 216, 4: 216}}
    for row in rows:
        mapping = {}
        for state in row['frames']['states']:
            for slot in state['slots']:
                value = slot['native_texture_index']
                assert slot['texture_input'] not in mapping or mapping[slot['texture_input']] == value
                mapping[slot['texture_input']] = value
        for texture, width in wanted.get(row['path'], {}).items():
            matched = []
            for state in row['frames']['states']:
                for draw in state['previous_buffer_geometry']:
                    if mapping[draw['texture_input']] == texture:
                        xy = draw['native_corners_fx12_before_clipping_or_GPU']
                        assert xy[1][0] - xy[0][0] == width * 4096
                        assert xy[2][1] - xy[0][1] == 32 * 4096
                        assert xy[0][1] == xy[1][1] and xy[0][0] == xy[2][0]
                        matched.append({'tick': state['tick'], 'corners_fx12': xy})
            assert matched
            subtitle_cases.append({'file': row['path'], 'texture': texture, 'native_width': width,
                                   'height': 32, 'prepared_quad_instances': len(matched), 'first': matched[0], 'last': matched[-1]})
    assert len(subtitle_cases) == 5
    root = next(r for r in rows if r['path'] == '/m02_03.fls')
    assert not any(s['slots'] or s['previous_buffer_geometry'] for s in root['frames']['states'])
    checkpoint = {'candidate_unchanged': str(ROM), 'candidate_sha256': digest,
                  'documentation': 'docs/fls_timeline_geometry_v312.md',
                  'complete_native_timelines_source_and_current': 15,
                  'native_update_calls_each_version': calls, 'distinct_native_state_snapshots_each_version': states,
                  'complete_prepared_native_quads_each_version': quads,
                  'source_controls_mapping_and_preclip_geometry_all_exact': True,
                  'global_camera_colour_alpha_canvas_and_depth_controls_included': True,
                  'five_subtitle_width_height_cases': subtitle_cases,
                  'root_timeline_native_calls': root['frames']['native_update_calls'],
                  'root_no_active_draw_slots_in_this_controlled_original_update_path': True,
                  'root_global_usage_or_all_other_readers_not_inferred': True,
                  'texture_binding_upload_palette_banks_clipping_and_GPU_not_claimed': True,
                  'all11_legacy_native_gates_and18_plaques_remain_open': True,
                  'low_resolution_Online_images_translation_exempt': True,
                  'native_proof': str(path), 'native_proof_sha256': sha(path.read_bytes()),
                  'ROM_modified': False, 'full_goal_complete': False}
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        target = Path('translations') / name
        data = read(target)
        assert data['latest_candidate_sha256'] == digest
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in data['plaque_style_v247']['ongoing_plaque_inventory'])
        data['FLS_timeline_geometry_v312'] = checkpoint
        data['current_goal_turn_classification'] = 'progress15-source-identical-native-timelines-and11035-prepared-quads'
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = f'''## V312: native FLS timelines and quad preparation

All15 FLS timelines reach their original end through native update. Current
and clean source inputs produce identical45,058 update calls,{states:,} distinct
state snapshots and{quads:,} prepared quads each, including global camera/colour/
alpha/depth controls. Original texture selection and
CPU affine math execute before clipping/GPU; all five opening subtitle widths
168/176/216 and32-row heights are retained. The raw root ends after876 calls
with no active drawable slots in this path; no global-unused claim is made.
Texture binding/upload, palette banks and final clipping remain separate gates.
No ROM change; V309 current. All11 legacy gates and18 plaques stay open; Online
images exempt. See [V312 evidence](fls_timeline_geometry_v312.md).

'''
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        target = Path('docs') / name
        content = target.read_text(encoding='utf-8')
        if '## V312:' not in content:
            title, rest = content.split('\n\n', 1)
            target.write_text(title + '\n\n' + section + rest, encoding='utf-8')
        else:
            start = content.index('## V312:')
            following = content.find('\n## ', start + 1)
            end = len(content) if following == -1 else following + 1
            target.write_text(content[:start] + section + content[end:], encoding='utf-8')
    print(json.dumps({'timelines': 15, 'native_calls_each': calls, 'prepared_quads_each': quads,
                      'subtitle_cases': subtitle_cases, 'ROM_unchanged': 'V309'}))


if __name__ == '__main__':
    main()
