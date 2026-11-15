"""Complete inherited release and source-owned linked navigation Help."""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.navigation_help_release_v2 import TOPICS, apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_fleet_release_v375 import files

ROOT = Path('work/analysis/navigation_help_release_v461')
ROM = Path('out/all_routes_combined_v461_candidate.nds')
PARENT = Path('out/all_routes_combined_v457_candidate.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    manifest, previous_manifest = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    digest = sha(ROM.read_bytes())
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v461'
    assert manifest['base_sha256'] == previous_manifest['base_sha256']
    assert manifest['batches'] == previous_manifest['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == previous_manifest['required_batches'] and all(manifest['checks'].values())
    registry = Path('translations/release_stack.json')
    assert manifest['release_stack_sha256'] == sha(registry.read_bytes())
    profiles = read(registry)['profiles']
    assert all(profiles[manifest['profile']][k] == v for k, v in profiles['all-routes-unified-v457'].items()
               if k not in ('note', 'description'))
    previous, current = files(NdsImage.open(PARENT)), files(NdsImage.open(ROM))
    assert previous.keys() == current.keys()
    assert [p for p in previous if previous[p] != current[p]] == ['/COMMON/HELP.DK4']
    target, result = apply_release(previous['/COMMON/HELP.DK4'], NdsImage.open('work/clean.nds').read_file('/COMMON/HELP.DK4'),
                                   NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/COMMON/HELP.DK4'),
                                   'translations/navigation_help_release_v2.json')
    assert target == current['/COMMON/HELP.DK4']
    plan = read(Path('work/analysis/navigation_help_v460/page_proposal.json'))
    assert result['pages'] == plan['pages'] and len(result['pages']) == 4
    old, new = [IlnkContainer.parse(raw).blocks for raw in (previous['/COMMON/HELP.DK4'], target)]
    assert len(old) == len(new) == 211 and new[203] == b'\0'
    assert all(new[i] == raw for i, raw in enumerate(old) if i not in TOPICS)
    assert plan['all4_native_previews_visually_reviewed']
    manuscript = read(Path('translations/navigation_help_manuscript_v2.json'))
    movement = next(r for r in manuscript['records'] if r['topic_id'] == 83)
    assert movement['original_link_IDs'] == [101, 125]
    automatic = next(r for r in manuscript['records'] if r['topic_id'] == 76)
    assert automatic['original_link_IDs'] == [120, 123, 104, 150]
    archive = read(Path('work/analysis/navigation_help_v460/native_archive_history_proof.json'))
    assert archive['HELP_sha256'] == sha(target) and len(archive['native211_topic_full_load_cases']) == 211
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    output = ROOT / 'patch_reconstruction.nds'
    apply_xdelta(Path('work/clean.nds'), patch, output)
    assert output.read_bytes() == ROM.read_bytes()
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'patch_sha256': sha(patch.read_bytes()),
             'exact_clean_patch_reconstruction': True, 'parent': str(PARENT), 'parent_sha256': sha(PARENT.read_bytes()),
             'profile': manifest['profile'], 'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'all470_inherited_batches_and_stages_preserved': True, 'only_HELP_changed_from_V457': True,
             'all207_unselected_articles_and211_IDs_and203_sentinel_and208_209_210_exact': True,
             'all211_complete_native_archive_loads_pass': True,
             'all4_reviewed_articles_and4_native_pages_pass': True,
             'manual_touch_and_sail_role_links_and_auto_route_share_rules_complete': True,
             'actual_cold_boot_navigation_pending': True,
             'all18_plaques_incomplete': True, 'full_goal_complete': False, 'release_status': 'experimental'}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('V461:4 complete linked navigation pages,211 archive loads,207 untouched articles;exact full stack and patch pass.')


if __name__ == '__main__':
    main()
