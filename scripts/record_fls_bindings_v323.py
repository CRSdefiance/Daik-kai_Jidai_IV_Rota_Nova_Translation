"""Record native allocation/binding coverage and retain final rendering gates."""

import json
import struct
from collections import Counter
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.research_fls_stream_v310 import SNAPSHOT
from scripts.research_fls_submission_v323 import ROM, ROOT
from scripts.verify_fls_bindings_v323 import POSE_PROOF, read


def main():
    path = ROOT / 'all_bindings_proof.json'
    proof, poses = read(path), read(POSE_PROOF)
    digest = sha(ROM.read_bytes())
    assert proof['candidate_sha256'] == digest
    assert proof['source_poses_sha256'] == sha(POSE_PROOF.read_bytes())
    ram = SNAPSHOT.read_bytes()
    assert proof['captured_global_state_sha256'] == sha(ram)
    historical = NdsImage.open(poses['candidate'])
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, source = current.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    for left, right in ((0xFD178, 0x10044C), (0x10AB8C, 0x10AF10), (0xDFA88, 0xDFD00)):
        assert arm[left:right] == source[left:right] == ram[left:right]
    cases = proof['cases']
    assert len(cases) == 260 and len({(r['path'], r['texture_index']) for r in cases}) == 260
    assert len({r['path'] for r in cases}) == 14
    observed = {}
    for file in poses['cases']:
        for state in file['frames']['states']:
            for pose in state['slots']:
                observed[file['path'], state['tick'], pose['slot']] = pose
    for case in cases:
        raw = current.read_file(case['path'])
        assert raw == historical.read_file(case['path'])
        table = struct.unpack_from('<I', raw, 4)[0]
        record = struct.unpack_from('<6I', raw, table + case['texture_index'] * 24)
        width, height, kind = record[0] >> 16, record[1] & 0xFFFF, record[0] & 0xFFFF
        parameter = case['actual_native_texture_parameter']
        assert (parameter >> 26) & 7 == (3, 4, 7)[kind]
        assert (parameter >> 20) & 7 == max(0, (width - 1).bit_length() - 3)
        assert (parameter >> 23) & 7 == max(0, (height - 1).bit_length() - 3)
        assert case['native_dimensions'] == [width, height]
        pose = observed[case['path'], case['observed_pose_tick'], case['slot']]
        assert pose['native_texture_index'] == case['texture_index']
        state = bytes.fromhex(pose['state_hex'])
        u, v = struct.unpack_from('<2H', state, 0x30)
        packed = lambda x, y: ((x * 16) & 0xFFFF) | (((y * 16) & 0xFFFF) << 16)
        expected_uv = [packed(u, v), packed(u, v + height),
                       packed(u + width, v + height), packed(u + width, v)]
        uv = [r['value'] for r in case['native_writes'] if r['address'] == 0x04000488]
        assert uv == expected_uv
        assert case['clean_and_current_bindings_and_native_commands_exact']
        assert case['all_native_loader_draw_return_register_and_stack_checks_pass']
    commands = sum(len(r['native_writes']) for r in cases)
    assert commands == 5200
    summary = {'candidate': str(ROM), 'candidate_sha256': digest,
               'documentation': 'docs/fls_bindings_v323.md',
               'native_proof': str(path), 'native_proof_sha256': sha(path.read_bytes()),
               'compressed_textures': 260, 'fresh_native_binding_fixtures_clean_and_current': 520,
               'files_with_observed_poses': 14, 'source_identical_native_commands_each_version': commands,
               'formats_by_native_parameter': dict(Counter((r['actual_native_texture_parameter'] >> 26) & 7 for r in cases)),
               'independent_metadata_format_storage_exponent_and_full_UV_bounds_checks': 260,
               'native_loader_allocators_matrix_and_draw_code_source_exact': True,
               'all_current_FLS_files_used_here_exact_to_pose_provenance_ROM': True,
               'captured_historical_globals_and_one_observed_pose_per_fresh_object_are_explicit_contracts': True,
               'no_final_projection_contextual_mask_upload_palette_bank_or_GPU_pixel_clearance': True,
               'queued_jobs_not_uploaded': True, 'raw_root_no_observed_pose_and_still_open': True,
               'all18_plaques_and_variants_still_incomplete': True,
               'low_resolution_Online_images_translation_exempt': True,
               'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'binding_summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        target = Path('translations') / name
        audit = read(target)
        assert audit['latest_candidate_sha256'] == digest
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        for entry in audit['plaque_style_v247']['ongoing_plaque_inventory']:
            assert not entry['fully_completed']
            for variant in entry.get('observed_variants', []):
                assert not variant['fully_completed']
        audit['FLS_native_bindings_v323'] = summary
        audit['current_goal_turn_classification'] = 'progress260-native-texture-material-bindings-and-complete-UV-bounds'
        target.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'bindings': 260, 'commands_each_version': commands,
                      'independent_UV_and_format_checks': 260, 'full_goal_complete': False}))


if __name__ == '__main__':
    main()
