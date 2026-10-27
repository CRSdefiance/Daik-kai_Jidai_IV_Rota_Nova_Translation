"""Verify the completed E-drive archive and unchanged original graphics scope."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_refit_help_v713 import ARCHIVE, KEY, RELEASE, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    provenance = read(ARCHIVE / 'provenance.json')
    for path, digest in provenance['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    for path, digest in provenance['external_E_drive_evidence'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    pre = read(RELEASE / 'preflight.json')
    scope = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    entries, plaque_counts, requirement_counts = [], [], []
    for name, original in scope.items():
        current = read(Path('translations') / name)
        requirements = current.get('historical_pending_items_retained')
        assert requirements == original['historical_pending_items_retained']
        plaques = current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory')
        assert plaques == original['ongoing_plaque_inventory']
        if plaques is not None:
            assert len(plaques) == 18 and all(r['fully_completed'] is False for r in plaques)
            plaque_counts.append(len(plaques))
        if requirements is not None:
            assert len(requirements) == 22
            requirement_counts.append(len(requirements))
        reduced, before = deepcopy(current), pre['all_original_audits_before'][name]
        entries.append(reduced.pop(KEY))
        reduced['current_goal_turn_classification'] = before['current_goal_turn_classification']
        reduced['latest_compiled_experimental_candidate_with_inherited_native_gap'] = before['latest_compiled_experimental_candidate_with_inherited_native_gap']
        assert reduced == before
    assert entries[0] == entries[1] == entries[2] and plaque_counts and requirement_counts
    heading = '## V712/V713: complete Refit help and actual native bitmap lifetime'
    previous = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V705 Yard selection and Refit findings/docs')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        content = (Path('docs') / name).read_text(encoding='utf-8')
        assert content.count(heading) == 1
        assert content.split(heading)[0].rstrip() == (previous / name).read_text(encoding='utf-8').rstrip()
    registry = read('translations/release_stack.json')
    assert registry['profiles']['all-routes-unified-v706']['status'] == 'revoked'
    assert registry['profiles']['all-routes-unified-v710']['status'] == 'revoked'
    assert registry['profiles']['all-routes-unified-v712']['status'] == 'experimental'
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == registry['canonical_baseline']['sha256']
    save(ROOT / 'archive_verification.json', {'archive': str(ARCHIVE),
        'archive_files_verified': len(provenance['files']),
        'external_E_drive_files_verified': len(provenance['external_E_drive_evidence']),
        'all18_plaque_objects_incomplete22_historical_objects_deep_exact': True,
        'all_other_audit_fields_exact_except_additive_entry_and_experimental_pointer': True,
        'all_four_documents_append_only_against_frozen_V705_archive': True,
        'V706_V710_revoked_V712_experimental_canonical_exact': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V713 archive verified:', len(provenance['files']), 'copied files,',
        len(provenance['external_E_drive_evidence']), 'external refs;18 plaques/22 scopes exact;4 docs append-only.', flush=True)


if __name__ == '__main__':
    main()
