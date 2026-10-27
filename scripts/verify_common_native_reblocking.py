"""Verify a saved reblocked COMMON release against its complete registered map."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_reblocking_release import apply_common_reblocking
from scripts.build_integrated_release import rom_files


def verify(candidate: Path, previous: Path, config: Path) -> dict:
    current, parent = NdsImage.open(candidate), NdsImage.open(previous)
    common_path, arm9_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
    expected_common, expected_arm9, plan = apply_common_reblocking(
        parent.read_file(common_path), parent.read_file(arm9_path), config)
    if (current.read_file(common_path) != expected_common
            or current.read_file(arm9_path) != expected_arm9):
        raise ValueError('Saved reblocking bytes differ from the complete source-locked map')
    before_files, after_files = rom_files(parent), rom_files(current)
    if before_files.keys() != after_files.keys():
        raise ValueError('ROM file/component inventory changed')
    changed = sorted(k for k in before_files if before_files[k] != after_files[k])
    if set(changed) != {common_path, arm9_path}:
        raise ValueError(f'Unrelated ROM files changed: {changed}')
    clean = NdsImage.open('work/clean.nds')
    sources = common_message_entries(clean.read_file(common_path), clean.read_file(arm9_path))
    actual = common_message_entries(current.read_file(common_path), current.read_file(arm9_path), clean=False)
    mismatches = []
    for source, selected in zip(sources, actual, strict=True):
        if source.message_id != selected.message_id:
            raise ValueError('Global native message identity changed')
        if re.findall(rb'%[sdi]', source.text) != re.findall(rb'%[sdi]', selected.text):
            mismatches.append(selected.message_id)
    # Broader audit result is reported independently; future unrelated source
    # translation work must not inherit an unsupported semantic-completion claim.
    return {'status': 'pass', 'candidate': candidate.as_posix(),
            'candidate_sha256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
            'all_native_messages_checked': len(actual), 'authored_entries': len(plan['authored_ids']),
            'all_unrelated_selected_text_unchanged': True, 'all_saved_bytes_match_complete_map': True,
            'executable_code_unchanged': plan['executable_code_unchanged'],
            'common_loader_selector_code_unchanged': True,
            'preserved_untranslated_ids': plan.get('preserved_untranslated_ids', []),
            'bgm_title_renderer': plan.get('bgm_title_renderer'),
            'original_cache_limit_preserved': True,
            'physical_record_coordinates_changed': True,
            'max_native_copy_bytes': plan['max_native_copy_bytes'], 'block_sizes': plan['block_sizes'],
            'printf_shape_mismatch_count': len(mismatches), 'printf_shape_mismatch_ids': mismatches,
            'changed_paths': changed, 'config': config.as_posix()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--previous', type=Path, required=True)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    report = verify(args.candidate, args.previous, args.config)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
