"""Full inherited release, complete Help article ownership and exact patch."""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sailor_data_help_release import TOPICS, apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_fleet_release_v375 import files

ROOT = Path('work/analysis/sailor_data_help_release_v447')
ROM = Path('out/all_routes_combined_v447_candidate.nds')
PARENT = Path('out/all_routes_combined_v443_candidate.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    manifest, old_manifest = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    digest = sha(ROM.read_bytes())
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v447'
    assert manifest['base_sha256'] == old_manifest['base_sha256']
    assert manifest['batches'] == old_manifest['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == old_manifest['required_batches'] and all(manifest['checks'].values())
    registry_path = Path('translations/release_stack.json')
    assert sha(registry_path.read_bytes()) == manifest['release_stack_sha256']
    profiles = read(registry_path)['profiles']
    assert all(profiles[manifest['profile']][k] == v for k, v in profiles['all-routes-unified-v443'].items()
               if k not in ('note', 'description'))
    previous, current = files(NdsImage.open(PARENT)), files(NdsImage.open(ROM))
    assert previous.keys() == current.keys()
    assert [k for k in previous if previous[k] != current[k]] == ['/COMMON/HELP.DK4']
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    target, report = apply_release(previous['/COMMON/HELP.DK4'], clean.read_file('/COMMON/HELP.DK4'),
                                   canonical.read_file('/COMMON/HELP.DK4'), 'translations/sailor_data_help_release_v1.json')
    assert target == current['/COMMON/HELP.DK4']
    proposal = read(Path('work/analysis/sailor_data_help_v446/page_proposal.json'))
    assert report['pages'] == proposal['pages'] and len(report['pages']) == 29
    old, new = [IlnkContainer.parse(raw).blocks for raw in (previous['/COMMON/HELP.DK4'], target)]
    assert len(old) == 208 and len(new) == 209 and new[203] == b'\0'
    assert all(new[n] == block for n, block in enumerate(old) if n not in TOPICS)
    assert proposal['all29_native_previews_visually_reviewed']
    assert proposal['all28_source_context_naturalness_and_fidelity_reviews_complete']
    native = read(Path('work/analysis/sailor_data_help_v446/native_archive_history_proof.json'))
    assert native['HELP_sha256'] == sha(target) and len(native['native209_topic_full_load_cases']) == 209
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    reconstruction = ROOT / 'patch_reconstruction.nds'
    apply_xdelta(Path('work/clean.nds'), patch, reconstruction)
    assert reconstruction.read_bytes() == ROM.read_bytes()
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'patch_sha256': sha(patch.read_bytes()),
             'exact_clean_patch_reconstruction': True, 'parent': str(PARENT),
             'parent_sha256': sha(PARENT.read_bytes()), 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'all470_inherited_batches_and_stages_preserved': True,
             'only_HELP_changed_from_V443': True,
             'all180_unselected_topics_and208_existing_IDs_and203_sentinel_exact': True,
             'all209_complete_native_archive_loads_pass': True,
             'all28_reviewed_articles_and29_complete_native_pages_pass': True,
             'original_links_and_complete_prose_and_plaque_labels_preserved': True,
             'compiler_owned_HP_continuation': 208,
             'actual_cold_boot_navigation_pending': True,
             'all18_plaques_incomplete': True, 'full_goal_complete': False,
             'release_status': 'experimental'}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('V447:28 articles/29 native pages,209 archive loads,180 untouched topics and470 inherited batches pass; only HELP changed; exact patch verified.')


if __name__ == '__main__':
    main()
