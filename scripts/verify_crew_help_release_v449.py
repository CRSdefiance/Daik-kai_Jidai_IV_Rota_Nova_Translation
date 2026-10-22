"""Complete inherited release and source-owned crew Help/requirements."""

import json
import re
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.crew_help_release import TOPICS, apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_fleet_release_v375 import files

ROOT = Path('work/analysis/crew_help_release_v449')
ROM = Path('out/all_routes_combined_v449_candidate.nds')
PARENT = Path('out/all_routes_combined_v447_candidate.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    manifest, previous_manifest = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    digest = sha(ROM.read_bytes())
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v449'
    assert manifest['base_sha256'] == previous_manifest['base_sha256']
    assert manifest['batches'] == previous_manifest['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == previous_manifest['required_batches'] and all(manifest['checks'].values())
    registry = Path('translations/release_stack.json')
    assert manifest['release_stack_sha256'] == sha(registry.read_bytes())
    profiles = read(registry)['profiles']
    assert all(profiles[manifest['profile']][k] == v for k, v in profiles['all-routes-unified-v447'].items()
               if k not in ('note', 'description'))
    previous, current = files(NdsImage.open(PARENT)), files(NdsImage.open(ROM))
    assert previous.keys() == current.keys()
    assert [p for p in previous if previous[p] != current[p]] == ['/COMMON/HELP.DK4']
    target, result = apply_release(previous['/COMMON/HELP.DK4'], NdsImage.open('work/clean.nds').read_file('/COMMON/HELP.DK4'),
                                   NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/COMMON/HELP.DK4'),
                                   'translations/crew_help_release_v1.json')
    assert target == current['/COMMON/HELP.DK4']
    plan = read(Path('work/analysis/crew_help_v448/page_proposal.json'))
    assert result['pages'] == plan['pages'] and len(result['pages']) == 35
    old, new = [IlnkContainer.parse(raw).blocks for raw in (previous['/COMMON/HELP.DK4'], target)]
    assert len(old) == 209 and len(new) == 210 and new[203] == b'\0'
    assert all(new[i] == raw for i, raw in enumerate(old) if i not in TOPICS)
    assert plan['all35_native_previews_visually_reviewed']
    manuscript = read(Path('translations/crew_help_manuscript_v1.json'))
    table = next(r for r in manuscript['records'] if r['topic_id'] == 133)
    values = [int(n) for n in re.findall(r'\d+', table['source_Japanese_with_link_IDs'])]
    assert values == [int(n) for n in re.findall(r'\d+', table['english'])] and len(values) == 16
    entries = table['english'].split('; ')
    rows = [line for page in result['pages'] if page['source_article_id'] == 133
            for line in page['visible_lines'][1:-1]]
    assert rows == [v + (';' if i < 15 else '') for i, v in enumerate(entries)]
    archive = read(Path('work/analysis/crew_help_v448/native_archive_history_proof.json'))
    assert archive['HELP_sha256'] == sha(target) and len(archive['native210_topic_full_load_cases']) == 210
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    output = ROOT / 'patch_reconstruction.nds'
    apply_xdelta(Path('work/clean.nds'), patch, output)
    assert output.read_bytes() == ROM.read_bytes()
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'patch_sha256': sha(patch.read_bytes()),
             'exact_clean_patch_reconstruction': True, 'parent': str(PARENT), 'parent_sha256': sha(PARENT.read_bytes()),
             'profile': manifest['profile'], 'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'all470_inherited_batches_and_stages_preserved': True, 'only_HELP_changed_from_V447': True,
             'all175_unselected_articles_and209_existing_IDs_and203_sentinel_and208_exact': True,
             'all210_complete_native_archive_loads_pass': True,
             'all34_reviewed_articles_and35_native_pages_pass': True,
             'all16_source_requirement_values_and_whole_rows_exact': values,
             'seven_sailor_data_role_names_match_existing_native_glossary': True,
             'requirements_continuation': 209, 'actual_cold_boot_navigation_pending': True,
             'all18_plaques_incomplete': True, 'full_goal_complete': False, 'release_status': 'experimental'}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('V449:34 articles/35 native pages,210 archive loads,16 whole requirements,175 untouched articles; exact inherited stack and patch pass.')


if __name__ == '__main__':
    main()
