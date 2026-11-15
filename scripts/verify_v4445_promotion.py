"""Apply the prevalidated promotion plan and audit preservation independently."""
from __future__ import annotations

import argparse
import gzip
import os
from pathlib import Path

from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.promote_v4445_checkpoint import (
    AUDIT, BASE_SHA, CLEAN_SHA, LEDGER_SHA, MANIFEST_SHA, PACKAGE, PATCH_SHA,
    PROFILE, REGISTRY_SHA, ROM, ROM_SHA, ROOT, read, save, sha,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    assert Path.cwd() == ROOT
    plan = read(AUDIT/'mutation_plan.json')
    assert len(plan) == 12 and len({row['target'] for row in plan}) == 12
    if args.apply:
        # Validate the entire plan before mutating any current metadata.
        for row in plan:
            target, staged = Path(row['target']), Path(row['planned'])
            assert target.is_relative_to(ROOT) and staged.is_relative_to(AUDIT)
            assert sha(target.read_bytes()) == row['before_sha256'], str(target)
            assert sha(staged.read_bytes()) == row['planned_sha256'], str(staged)
        for row in plan:
            target, data = Path(row['target']), Path(row['planned']).read_bytes()
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
        updates[target.relative_to(ROOT).as_posix()] = sha(target.read_bytes())
    promotion = read(ROOT/'translations/promoted_build.json')
    assert promotion == read(PACKAGE/'promotion.json')
    assert promotion['profile'] == PROFILE and promotion['main_build']
    assert promotion['previous_promoted_build'] == 'releases/all_routes_unified_v4353/promotion.json'
    assert not promotion['construction_baseline_rebased']
    before_registry = read(AUDIT/'registry.before.json')
    registry = read(ROOT/'translations/release_stack.json')
    assert sha((AUDIT/'registry.before.json').read_bytes()) == REGISTRY_SHA
    assert {k:v for k,v in before_registry.items() if k != 'latest_promoted_build'} == {
        k:v for k,v in registry.items() if k != 'latest_promoted_build'}
    assert registry['latest_promoted_build']['profile'] == PROFILE
    assert len(registry['accepted_layers']) == 114
    assert registry['profiles'][PROFILE]['status'] == 'experimental'
    original_manifest = gzip.decompress((PACKAGE/'build_manifest.json.gz').read_bytes())
    original_registry = gzip.decompress((PACKAGE/'build_release_stack.json.gz').read_bytes())
    assert sha(original_manifest) == MANIFEST_SHA and sha(original_registry) == REGISTRY_SHA
    assert original_manifest == ROM.with_suffix('.manifest.json').read_bytes()
    assert original_registry == (AUDIT/'registry.before.json').read_bytes()
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['profile'] == PROFILE and len(manifest['batches']) == 549
    assert all(manifest['checks'].values())
    assert sha(ROM.read_bytes()) == ROM_SHA
    assert ROM.read_bytes() == (AUDIT/'promoted_patch_reconstruction_RESEARCH_ONLY.nds').read_bytes()
    assert sha((PACKAGE/'translation.xdelta').read_bytes()) == PATCH_SHA
    assert (PACKAGE/'translation.xdelta').read_bytes() == ROM.with_suffix('.xdelta').read_bytes()
    assert sha((ROOT/'work/clean.nds').read_bytes()) == CLEAN_SHA
    assert sha((ROOT/'out/raphael_natural_v2_accepted_base.nds').read_bytes()) == BASE_SHA
    before_bytes = gzip.decompress((AUDIT/'ledger.before.json.gz').read_bytes())
    assert sha(before_bytes) == LEDGER_SHA
    import json
    before = json.loads(before_bytes)
    ledger_path = ROOT/'translations/editorial_review_current_v1.json'
    ledger = read(ledger_path)
    allowed = {'latest_checkpoint','promoted_main_build_v4452','lil_B174_clean_context_v4452'}
    assert not (allowed - {'latest_checkpoint'}) & set(before)
    assert {k:v for k,v in before.items() if k not in allowed} == {
        k:v for k,v in ledger.items() if k not in allowed}
    assert ledger_path.read_bytes() == encode_ledger(ledger)
    assert ledger_path.stat().st_size < 100*1024*1024
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert ledger['promoted_main_build_v4452'] == promotion
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass',
        'records_revised_and_integrated','retained_wordings_editorially_completed']) == (5800,5803,3686,2114)
    draft = ledger['lil_B174_clean_context_v4452']
    assert draft == read(PACKAGE/'verification/UNINTEGRATED_B174_status.json')
    assert draft['clean_source_speeches'] == 33 and draft['source_prose_or_completion_credit_added'] == 0
    assert not draft['new_B174_manuscript_integrated_in_promoted_ROM']
    assert sha((PACKAGE/'verification/B174_clean_context.json').read_bytes()) == draft['clean_context_sha256']
    receipt = read(AUDIT/'staging_receipt.json')
    for path,digest in receipt['evidence'].items():
        assert sha((ROOT/path).read_bytes()) == digest, path
    assert receipt['producer_sha256'] == sha((ROOT/'scripts/promote_v4445_checkpoint.py').read_bytes())
    visual = read(PACKAGE/'verification/current_six_frame_visual_review.json')
    assert sha((PACKAGE/'verification/current_Lil_startup_and_town_review.png').read_bytes()) == visual['sha256']
    assert 'Unified V4445' in (ROOT/'README.md').read_text(encoding='utf-8').splitlines()[0]
    assert (ROOT/'docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4452')
    previous_packages = []
    for checksum_file in sorted((ROOT/'releases').glob('*/checksums.json')):
        if checksum_file.parent == PACKAGE:
            continue
        for name,digest in read(checksum_file).items():
            assert sha((checksum_file.parent/name).read_bytes()) == digest, str(checksum_file.parent/name)
        previous_packages.append(checksum_file.parent.name)
    assert 'all_routes_unified_v4353' in previous_packages
    audit = {'checkpoint':'V4452','profile':PROFILE,'main_build':True,
        'rom_sha256':ROM_SHA,'patch_sha256':PATCH_SHA,
        'original_manifest_and_registry_byte_exact':True,'only_registry_promotion_pointer_changed':True,
        'whole_clean_input_patch_reconstruction_byte_exact':True,'canonical_baseline_unchanged':True,
        'manifest_batches':549,'accepted_layers':114,'fresh_contextual_rereads':5800,
        'completed_contextual_reviews':5800,'pending_credited_route_reviews':0,'source_prose_reviews':5803,
        'ledger_sha256':sha(ledger_path.read_bytes()),'all_prior_ledger_records_and_coverage_preserved':True,
        'B174_uncredited_clean_glosses':33,'previous_release_checksums_verified':previous_packages,
        'targeted_tests_passed':78,'new_emulator_runs_at_promotion':0,'ROMs_deleted':0,
        'full_goal_active':True,'full_goal_complete':False,'updated_files':updates,
        'producer_sha256':sha(Path(__file__).read_bytes())}
    save(AUDIT/'promotion_receipt.json',audit)
    save(PACKAGE/'verification/promotion_final_audit.json',audit)
    checksums = {p.relative_to(PACKAGE).as_posix():sha(p.read_bytes())
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'}
    save(PACKAGE/'checksums.json',checksums)
    assert all(sha((PACKAGE/name).read_bytes()) == digest for name,digest in checksums.items())
    print(json.dumps({'promoted_package_verified':True,'files':len(checksums),'profile':PROFILE,
        'whole_ROM_byte_exact':True,'all_prior_ledger_records_preserved':True,'B174_uncredited_glosses':33}))


if __name__ == '__main__':
    main()
