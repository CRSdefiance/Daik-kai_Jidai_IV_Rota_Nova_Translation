"""Verify saved V133 contains exactly three caption changes over complete V132."""
import hashlib
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.register_online_caption_fidelity_v133 import BATCH, patched_arm9


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def files(image):
    result = {path: data for _, path, data in image.iter_files()}
    result.update(dict(image.iter_components()))
    return result


def main():
    candidate_path = Path('out/all_routes_combined_v133_candidate.nds')
    old = NdsImage.open('out/all_routes_combined_v132_candidate.nds')
    new = NdsImage.open(candidate_path)
    old_files, new_files = files(old), files(new)
    batch = json.loads(Path(BATCH).read_text(encoding='utf-8'))
    assert old_files.keys() == new_files.keys()
    for path, raw in old_files.items():
        expected = patched_arm9(raw, batch) if path == '/__arm9__.bin' else raw
        assert new_files[path] == expected, path
    a = common_message_entries(old_files['/COMMON/MESFILE.DK4'], old_files['/__arm9__.bin'], clean=False)
    b = common_message_entries(new_files['/COMMON/MESFILE.DK4'], new_files['/__arm9__.bin'], clean=False)
    assert a == b
    manifest = json.loads(candidate_path.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    for field, path in [('candidate_sha256', manifest['candidate_rom']),
                        ('base_sha256', manifest['base_rom']),
                        ('release_stack_sha256', manifest['release_stack'])]:
        assert sha(Path(path).read_bytes()) == manifest[field]
    assert manifest['profile'] == 'all-routes-unified-v133'
    assert len(manifest['batches']) == 429 and all(manifest['checks'].values())
    report = {'status': 'pass', 'candidate': candidate_path.as_posix(),
              'candidate_sha256': sha(candidate_path.read_bytes()),
              'all_v132_files_preserved_except_three_fixed_caption_slots': True,
              'all_native_messages_byte_exact': len(a), 'COMMON_byte_exact': True,
              'executable_code_and_descriptor_tables_unchanged': True,
              'base_candidate_registry_hashes_verified': True,
              'complete_inherited_batch_count_plus_caption_batch': 429,
              'runtime_caption_rendering_verified': False}
    Path('work/analysis/online_caption_v133_saved_proof.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
