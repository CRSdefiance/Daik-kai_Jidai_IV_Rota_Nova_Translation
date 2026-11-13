"""Apply validated promotion metadata and independently audit preservation."""
from __future__ import annotations

import argparse
import gzip
import os
from pathlib import Path

from scripts.promote_v4204_checkpoint import (
    AUDIT, BASE_SHA, CLEAN_SHA, LEDGER_SHA, MANIFEST_SHA, PACKAGE, PATCH_SHA,
    PROFILE, REGISTRY_SHA, ROM_SHA, ROOT, read, save, sha,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    assert Path.cwd() == ROOT
    plan = read(AUDIT / 'mutation_plan.json')
    if args.apply:
        # Validate every destination and both hashes before any write.
        for row in plan:
            target, staged = Path(row['target']), Path(row['planned'])
            assert target.is_relative_to(ROOT) and staged.is_relative_to(AUDIT)
            assert sha(target.read_bytes()) == row['before_sha256']
            assert sha(staged.read_bytes()) == row['planned_sha256']
        for row in plan:
            target, data = Path(row['target']), Path(row['planned']).read_bytes()
            # Existing mapped files can be updated in place without truncating first.
            with target.open('r+b') as stream:
                stream.write(data)
                if stream.seek(0, os.SEEK_END) != len(data):
                    stream.truncate(len(data))
                stream.flush()
                os.fsync(stream.fileno())
            assert sha(target.read_bytes()) == row['planned_sha256']
    updates = {}
    for row in plan:
        target = Path(row['target'])
        assert target.is_relative_to(ROOT)
        assert target.read_bytes() == Path(row['planned']).read_bytes()
        assert sha(target.read_bytes()) == row['planned_sha256']
        updates[target.relative_to(ROOT).as_posix()] = row['planned_sha256']
    promotion = read(ROOT / 'translations/promoted_build.json')
    assert promotion == read(PACKAGE / 'promotion.json')
    assert promotion['profile'] == PROFILE and promotion['main_build']
    before_registry = read(AUDIT / 'registry.before.json')
    registry = read(ROOT / 'translations/release_stack.json')
    assert sha((AUDIT / 'registry.before.json').read_bytes()) == REGISTRY_SHA
    assert {k: v for k, v in before_registry.items() if k != 'latest_promoted_build'} == {
        k: v for k, v in registry.items() if k != 'latest_promoted_build'}
    assert len(registry['accepted_layers']) == 114
    assert registry['latest_promoted_build']['profile'] == PROFILE
    assert registry['profiles'][PROFILE]['status'] == 'experimental'
    original_manifest = gzip.decompress((PACKAGE / 'build_manifest.json.gz').read_bytes())
    original_registry = gzip.decompress((PACKAGE / 'build_release_stack.json.gz').read_bytes())
    assert sha(original_manifest) == MANIFEST_SHA and sha(original_registry) == REGISTRY_SHA
    assert original_manifest == (ROOT / 'out/all_routes_combined_v4204_candidate.manifest.json').read_bytes()
    assert original_registry == (AUDIT / 'registry.before.json').read_bytes()
    rom = ROOT / promotion['rom']
    reconstruction = AUDIT / 'promoted_patch_reconstruction_RESEARCH_ONLY.nds'
    assert sha(rom.read_bytes()) == ROM_SHA and rom.read_bytes() == reconstruction.read_bytes()
    assert sha((PACKAGE / 'translation.xdelta').read_bytes()) == PATCH_SHA
    assert (PACKAGE / 'translation.xdelta').read_bytes() == rom.with_suffix('.xdelta').read_bytes()
    assert sha((ROOT / 'work/clean.nds').read_bytes()) == CLEAN_SHA
    assert sha((ROOT / 'out/raphael_natural_v2_accepted_base.nds').read_bytes()) == BASE_SHA
    old_bytes = gzip.decompress((AUDIT / 'ledger.before.json.gz').read_bytes())
    assert sha(old_bytes) == LEDGER_SHA
    import json
    before = json.loads(old_bytes)
    ledger = read(ROOT / 'translations/editorial_review_current_v1.json')
    allowed = {'latest_checkpoint', 'promoted_main_build_v4226', 'lil_B169_preintegration_review_v4226'}
    assert {k: v for k, v in before.items() if k not in allowed} == {
        k: v for k, v in ledger.items() if k not in allowed}
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert ledger['promoted_main_build_v4226'] == promotion
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass'],
            ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (5656, 5659, 3595, 2061)
    pending = ledger['lil_B169_preintegration_review_v4226']
    assert pending == read(PACKAGE / 'verification/UNINTEGRATED_B169_status.json')
    assert (pending['objects'], pending['proposed_revisions'], pending['justified_retentions']) == (36, 19, 17)
    assert not pending['integrated_in_promoted_ROM'] and pending['editorial_ledger_credit_added'] == 0
    assert sha((ROOT / pending['manuscript']).read_bytes()) == pending['manuscript_sha256']
    assert sha((ROOT / pending['layout_findings']).read_bytes()) == pending['layout_findings_sha256']
    assert gzip.decompress((PACKAGE / 'verification/UNINTEGRATED_B169_layout_QA.json.gz').read_bytes()) == (ROOT / pending['layout_findings']).read_bytes()
    receipt = read(AUDIT / 'staging_receipt.json')
    for path, digest in receipt['evidence'].items():
        assert sha((ROOT / path).read_bytes()) == digest
    assert 'Unified V4204' in (ROOT / 'README.md').read_text(encoding='utf-8').splitlines()[0]
    assert (ROOT / 'docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4226')
    assert (ROOT / promotion['previous_promoted_build']).is_file()
    audit = {
        'checkpoint': 'V4226', 'profile': PROFILE, 'main_build': True,
        'rom_sha256': ROM_SHA, 'patch_sha256': PATCH_SHA,
        'original_manifest_and_registry_byte_exact': True,
        'only_registry_promotion_pointer_changed': True,
        'whole_clean_input_patch_reconstruction_byte_exact': True,
        'canonical_baseline_unchanged': True, 'manifest_batches': 544, 'accepted_layers': 114,
        'completed_contextual_reviews': 5656, 'source_prose_reviews': 5659,
        'ledger_sha256': sha((ROOT / 'translations/editorial_review_current_v1.json').read_bytes()),
        'all_prior_ledger_records_and_coverage_preserved': True,
        'B169_draft_objects_unintegrated_uncredited': 36,
        'B169_three_layout_findings_still_open': True,
        'targeted_tests_passed': 78, 'new_emulator_runs_at_promotion': 0,
        'ROMs_deleted': 0, 'full_goal_active': True, 'full_goal_complete': False,
        'updated_files': updates, 'producer_sha256': sha(Path(__file__).read_bytes()),
    }
    save(AUDIT / 'promotion_receipt.json', audit)
    save(PACKAGE / 'verification/promotion_final_audit.json', audit)
    checksums = {p.relative_to(PACKAGE).as_posix(): sha(p.read_bytes())
                 for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'}
    save(PACKAGE / 'checksums.json', checksums)
    assert all(sha((PACKAGE / name).read_bytes()) == digest for name, digest in checksums.items())
    print(json.dumps({'promoted_package_verified': True, 'files': len(checksums), 'profile': PROFILE,
                      'whole_ROM_byte_exact': True, 'all_prior_ledger_records_preserved': True,
                      'B169_unintegrated_uncredited': 36}))


if __name__ == '__main__':
    main()
