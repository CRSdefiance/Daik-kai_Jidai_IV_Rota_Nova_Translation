"""Prepare the complete reviewed route/COMMON/HELP/name migration on V298."""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.message_actor_integrity import HEADER
from dk4tool.patch.reviewed_name_integration import transform
from dk4tool.rom.nds import NdsImage
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path('work/analysis/reviewed_name_release_v299')
PARENT = Path('out/all_routes_combined_v298_candidate.nds')
CONFIG = Path('translations/reviewed_name_integration_release_v1.json')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(PARENT.read_bytes()) == '0e57a87c72d711b3cab3ac29ea8c7bb51c1ab1fd3b30ac3551983d1ee31a5a5b'
    current, clean, canonical = [NdsImage.open(p) for p in (PARENT, 'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    paths = [f'/data/SC{i}.DK4' for i in range(4)] + ['/__arm9__.bin', '/COMMON/MESFILE.DK4', '/COMMON/HELP.DK4']
    files, clean_files, canonical_files = [{p: rom.read_file(p) for p in paths} for rom in (current, clean, canonical)]
    old_path = Path('out/all_routes_combined_v275_candidate.nds')
    assert sha(old_path.read_bytes()) == '94fa82c8edd99de4f21829bc94b1b98013929f98cc1378c73fe0768e1d1caddf'
    old = NdsImage.open(old_path)
    actor_positions = {}
    for path in paths[:4]:
        positions = []
        for block, (source, native) in enumerate(zip(IlnkContainer.parse(clean_files[path]).blocks,
                                                   IlnkContainer.parse(old.read_file(path)).blocks, strict=True)):
            parts, original_parts = native.split(b'\0'), source.split(b'\0')
            offsets, at = [], 0
            for raw in parts:
                offsets.append(at)
                at += len(raw) + 1
            original_at = 0
            for index, raw in enumerate(original_parts):
                if raw and source[max(0, original_at - 5):original_at] == HEADER:
                    positions.append([block, index, offsets[index], raw[0]])
                original_at += len(raw) + 1
        actor_positions[path] = positions
    assert sum(len(rows) for rows in actor_positions.values()) == 19254
    dependencies = {
        'preparation': ('translations/reviewed_name_packet_v299.json', read('work/analysis/reviewed_names_v297/preparation.json')),
        'COMMON_manuscript': ('translations/reviewed_name_common_v299.json', read('work/analysis/confirmed_names_v276/current_common_manuscript.json')),
        'HELP_proposal': ('translations/reviewed_name_help_pages_v299.json', read('work/analysis/help_display_v282/navigation_proposal.json')),
        'actor_positions': ('translations/original_actor_positions_v299.json', actor_positions),
    }
    for path, data in dependencies.values():
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    prep, common, help_proposal, actors = [data for _, data in dependencies.values()]
    # Preserve source review and actual paging/navigation dependencies as locks.
    for filename, digest in prep['source_review_dependencies'].items():
        assert sha(Path(filename).read_bytes()) == digest
    target, proof = transform(files, clean_files, canonical_files, prep, common, help_proposal, actors)
    assert target['/COMMON/MESFILE.DK4'] == Path('work/analysis/confirmed_names_v276/common_research_only.bin').read_bytes()
    initialized(target['/__arm9__.bin'])
    for path, raw in target.items():
        (ROOT / (Path(path).name + '.research_only')).write_bytes(raw)
    (ROOT / 'catalog_arm9_research_only.bin').write_bytes(target['/__arm9__.bin'])
    (ROOT / 'catalog_plan.json').write_text(json.dumps(proof['catalog'], indent=2) + '\n', encoding='utf-8')
    (ROOT / 'preparation.json').write_text(json.dumps(prep, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'transform_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    config = {'format': 'dk4-reviewed-name-integration-release-v1',
              **{k: path for k, (path, _) in dependencies.items()},
              'dependencies_sha256': {path: sha(Path(path).read_bytes()) for path, _ in dependencies.values()},
              'source_file_sha256': proof['source_file_sha256'], 'target_file_sha256': proof['target_file_sha256'],
              'clean_file_sha256': {p: sha(raw) for p, raw in clean_files.items()},
              'canonical_file_sha256': {p: sha(raw) for p, raw in canonical_files.items()},
              'status': 'research-complete-migration-native-current-tests-pending-not-yet-registered'}
    CONFIG.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    catalog = proof['catalog']
    print(f'444 route paragraphs, sixCOMMON messages, eightHELP pages, five names; {catalog["pool_payload_bytes"]} owned bytes; {catalog["remaining_before_stage"]} spare.', flush=True)


if __name__ == '__main__':
    main()
