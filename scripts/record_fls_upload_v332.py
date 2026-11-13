"""Record complete CPU-side upload evidence without claiming final GPU pixels."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.compression_probe import decompress_lz10
from scripts.research_fls_stream_v310 import SNAPSHOT
from scripts.research_fls_upload_v332 import ROM, ROOT


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    path = ROOT / 'all_upload_proof.json'
    proof = read(path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, source, ram = current.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin'), SNAPSHOT.read_bytes()
    for left, right in ((0xFE138, 0xFE208), (0xE04E8, 0xE09C0), (0xE2034, 0xE231C), (0xE25C4, 0xE266C)):
        assert arm[left:right] == source[left:right] == ram[left:right]
    new_code, old_code = MainCodeFile(arm, 0x02000000), MainCodeFile(source, 0x02000000)
    new_itcm = next(s for s in new_code.sections if s.ramAddress == 0x01FF8000)
    old_itcm = next(s for s in old_code.sections if s.ramAddress == 0x01FF8000)
    assert bytes(new_itcm.data[0x190C:0x195C]) == bytes(old_itcm.data[0x190C:0x195C])
    assert arm[0xE55D4:0xE5600] == source[0xE55D4:0xE5600] == ram[0xE55D4:0xE5600]
    cases = proof['cases']
    assert len(cases) == 520 and len({(r['path'], r['texture'], r['kind']) for r in cases}) == 520
    total = 0
    for row in cases:
        result = row['inspection']
        assert result['native_decode_and_upload_service_returned']
        assert result['complete_final_modeled_VRAM_bytes_match_independent_decode']
        assert result['all_modeled_VRAM_outside_DMA_ranges_preserved']
        raw = current.read_file(row['path'])
        table, count, payload = struct.unpack_from('<3I', raw, 4)
        assert row['texture'] < count
        record = struct.unpack_from('<6I', raw, table + row['texture'] * 24)
        width, height, kind = record[0] >> 16, record[1] & 0xFFFF, record[0] & 0xFFFF
        length = record[3] if row['kind'] == 'palette' else (1 << max(3, (width - 1).bit_length())) * (
            1 << max(3, (height - 1).bit_length())) * (4, 8, 16)[kind] // 8
        offset = record[2] if row['kind'] == 'palette' else record[4]
        expected = decompress_lz10(raw[payload + offset:])
        assert len(expected) == length == result['expected_payload_bytes']
        assert sha(expected) == result['expected_payload_sha256']
        total += length
    assert total == 9821984
    summary = {'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
               'native_proof': str(path), 'native_proof_sha256': sha(path.read_bytes()),
               'native_palette_pixel_decode_to_upload_cases': len(cases),
               'complete_final_independent_payload_bytes': total,
               'tested_SDK_bank_upload_interrupt_and_ITCM_DMA_routine_source_exact': True,
               'whole_ITCM_source_equality_not_claimed_established_arena_changes_outside_DMA_routine': True,
               'all_modeled_destination_bytes_and_unowned_VRAM_preservation_pass': True,
               'largest131072_byte_four_overlapping_chunks_verified': True,
               'logical_destination_zero_captured_bank_configuration_immediate_DMA_and_LCDC_memory_are_contracts': True,
               'hardware_cycles_IRQ_gpu_bank_alias_concurrency_screen_clipping_alpha_pixels_not_verified': True,
               'raw_root_intended_loader_usage_still_open': True,
               'all18_plaques_and_variants_still_incomplete': True,
               'low_resolution_Online_images_exempt': True,
               'ROM_modified': False, 'full_goal_complete': False,
               'documentation': 'docs/fls_upload_v332.md'}
    out = ROOT / 'summary.json'
    out.write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        target = Path('translations') / name
        audit = read(target)
        assert audit['latest_candidate_sha256'] == proof['candidate_sha256']
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in audit['plaque_style_v247']['ongoing_plaque_inventory'])
        audit['FLS_original_CPU_upload_v332'] = {**summary, 'summary': str(out)}
        audit['current_goal_turn_classification'] = 'progress520-native-decode-to-SDK-upload-cases-and9821984-final-bytes'
        target.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'cases': len(cases), 'final_payload_bytes': total, 'GPU_pixels_verified': False}))


if __name__ == '__main__':
    main()
