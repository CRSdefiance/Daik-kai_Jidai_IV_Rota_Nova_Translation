"""Verify saved placeholder repairs and all inherited V141 ROM components."""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_placeholder_release import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.register_grand_race_help_v134 import components
from scripts.verify_common_native_repack import verify


def main():
    previous_path = Path('out/all_routes_combined_v141_candidate.nds')
    path = Path('out/all_routes_combined_v142_candidate.nds')
    if sha(previous_path.read_bytes()) != 'c32db16159db6d6da0db3aaf2fa774c342cda2c3af8abdc3b77acca86a201310':
        raise ValueError('Complete V141 source ROM differs')
    previous, saved = [components(NdsImage.open(p)) for p in (previous_path, path)]
    common_path, arm9_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
    config = Path('translations/common_placeholder_release_v1.json')
    common, arm9, report = apply_release(previous[common_path], previous[arm9_path], config)
    if saved != {**previous, common_path: common, arm9_path: arm9}:
        raise ValueError('Saved V142 changes components outside reviewed placeholder repairs')
    proof_path = Path('work/analysis/common_placeholder_v142_release_proof.json')
    proof_path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    proof = verify(path, previous_path, proof_path)
    phrase = b'A message about the story, a letter, or faction relations.'
    if any(phrase in raw for raw in IlnkContainer.parse(common).blocks):
        raise ValueError('Generic story/letter/faction placeholder remains')
    manifest = json.loads(path.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    old_manifest = json.loads(previous_path.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    registry_path = Path('translations/release_stack.json')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    if (manifest['profile'] != 'all-routes-unified-v142'
            or manifest['candidate_sha256'] != sha(path.read_bytes())
            or manifest['base_sha256'] != registry['canonical_baseline']['sha256']
            or manifest['release_stack_sha256'] != sha(registry_path.read_bytes())
            or manifest['batches'] != old_manifest['batches']):
        raise ValueError('V142 registry, lineage or inherited batch order differs')
    stage = manifest['relocations'][common_path]['placeholder_repair']
    if stage['release_config_sha256'] != sha(config.read_bytes()) or stage['expected_arm9_sha256'] != sha(arm9):
        raise ValueError('Saved repair stage identity differs')
    proof.update({'arm9_sha256': sha(arm9), 'common_sha256': sha(common),
                  'batch_count': len(manifest['batches']), 'all_other_components_byte_exact': True,
                  'all_v141_routes_ui_graphics_captions_tooltips_blizzard_alerts_preserved': True,
                  'specific_generic_placeholder_phrase_remaining': 0,
                  'older_english_semantic_audit_complete': False, 'runtime_verified': False})
    Path('work/analysis/common_placeholder_v142_saved_rom_proof.json').write_text(
        json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(proof, indent=2))


if __name__ == '__main__':
    main()
