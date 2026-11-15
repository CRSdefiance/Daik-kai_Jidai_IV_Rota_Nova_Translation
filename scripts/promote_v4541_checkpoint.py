"""Stage, apply and independently audit the requested V4541 main promotion."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dk4tool.patch.xdelta import apply_xdelta
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'work/analysis/promotion_v4571'
PACKAGE = ROOT / 'releases/all_routes_unified_v4541'
ROM = ROOT / 'out/all_routes_combined_v4541_candidate.nds'
PROFILE = 'all-routes-unified-v4541'
ROM_SHA = 'a4f2023eb2dd1b84cc0c0879663ef5b57fd89e7fa832307aaf78d11411e1897d'
PATCH_SHA = '6cc5b2b8b9a9b75c3841e416106bbd5798a9b2f208c368762f83fdb33836c83b'
MANIFEST_SHA = '03cfbbc4fc6c46f9a593c96b92119eb588549e4bc6ba14f1858c497fbdf66e1c'
REGISTRY_SHA = '4ed4dcf764bd2492b5b96b2a87fc8cbdb0cd9cbb10e49f193276ea87b247ccfa'
LEDGER_SHA = '04fc333f8d4a8bd92540ccabd77e073ebf834c48eab7e98862429e4ddf2e83e6'
CLEAN_SHA = 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
BASE_SHA = '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
SCOPE = (
    'The full editorial goal remains active across every remaining storyline, shared shop/town '
    'dialogue, random scene, Help and other player-facing prose. B176-B180 contains58 physical '
    'speeches and zero typed-choice leads, not a project denominator. Preserve COMMON750-752, '
    'canonical Maria32 SC3B97, SourceItems/LocalProduct, five named-target leads, exact-record '
    'Proof consistency, Samwell full-catalogue middle-field lead and B157 provenance amendment. '
    'Graphics/all18 plaques remain separate; retain the later older-record technical re-audit '
    'and queued0D gap. Preserve every ROM, translation, draft, executed producer, proof and failure.')
RESUME = (
    'Resume B176 from all10 clean-first contextual decisions (five proposed revisions/five '
    'retentions), manuscript v2, layout V4569 and native-font proof V4570. The two V4570 sheets '
    'still require individual visual inspection; the prior combined image output was truncated. '
    'The shared planner already normalizes punctuation. V4568 narrowly permits the complete '
    'clause "with a flavor like this," and preserves the failed hypotheses; no prose or metrics '
    'were weakened. Then native approval, additive ledger credit, relocation/stored checks, '
    'representative gameplay and registered cumulative integration. B176 remains uncredited '
    'and outside this ROM. Continue B177-B180 and the entire wider objective.')
SUMMARY = (
    'V4571 promotes verified V4541 as the user-designated main cumulative build, including '
    'completed B175 (19 revisions/13 justified retentions). All551 manuscript batches and114 '
    'accepted layers are preserved. A fresh clean-input patch reconstruction is byte exact; '
    '78 release/dialogue regression tests pass. Coverage stays5865 completed contextual rereads, '
    '5868 source/prose reviews,3728 revised/2137 retained and4266 completed route objects, '
    'with zero pending credited route drafts. B176 has10 uncredited draft decisions and '
    'offline native checks; visual approval and integration remain pending. Promotion adds '
    'no editorial credit, emulator run or user cold-boot claim. Earlier main V4496 and every '
    'earlier package remain preserved. Immutable construction inputs and accepted-layer '
    'status are unchanged. ' + SCOPE)
EVIDENCE = {
    'registered_release_verification.json': 'work/analysis/lil_B175_release_v4542/registered_release_verification.json',
    'cold_boot_Lil_startup_town_verification.json': 'work/analysis/lil_B175_startup_v4544/cold_boot_Lil_startup_town_verification.json',
    'current_six_frame_visual_review.json': 'work/analysis/lil_B175_startup_v4544/current_six_frame_visual_review.json',
    'B175_completion_receipt.json': 'work/analysis/lil_B175_completion_v4545/completion_receipt.json',
    'V4546_verified_handoff.json': 'work/analysis/editorial_handoff_verification_v4546/verified_handoff.json',
    'unfinished_editorial_scope_inventory.json': 'work/analysis/lil_B175_completion_v4545/unfinished_editorial_scope_inventory.json',
    'B175_final_review.json': 'translations/lil_B175_contextual_final_review_v1.json',
    'B175_actual_scene_review.json': 'work/analysis/lil_B175_actual_review_v4535/all6_actual_sheets_32_planes_scoped_transitions_return_and_final_state.json',
    'B176_clean_context.json': 'work/analysis/lil_B176_clean_context_v4547/all10_complete_B176_exchange_and_fresh_glosses.json',
    'B176_contextual_decisions.json': 'work/analysis/lil_B176_author_v4558/all10_clean_first_contextual_decisions.json',
    'B176_draft_manuscript_v2.json': 'translations/lil_B176_editorial_manuscript_v2.json',
    'B176_layout_QA.json': 'work/analysis/lil_B176_layout_v4569/all10_paragraph_layout_QA.json',
    'B176_offline_native_fonts.json': 'work/analysis/lil_B176_fonts_v4570/all10_progressive_FE_native_planes_and80_alignment_cases.json',
    'B176_complete_clause_derivation.json': 'work/analysis/lil_B176_complete_clause_v4568/source_derivation.json',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def save(path, value):
    Path(path).write_bytes(encoded(value))


def stage():
    assert Path.cwd() == ROOT and not AUDIT.exists() and not PACKAGE.exists()
    for path, digest in [(ROM, ROM_SHA), (ROM.with_suffix('.xdelta'), PATCH_SHA),
                         (ROM.with_suffix('.manifest.json'), MANIFEST_SHA),
                         (ROOT/'translations/release_stack.json', REGISTRY_SHA),
                         (ROOT/'translations/editorial_review_current_v1.json', LEDGER_SHA),
                         (ROOT/'work/clean.nds', CLEAN_SHA),
                         (ROOT/'out/raphael_natural_v2_accepted_base.nds', BASE_SHA)]:
        assert sha(path.read_bytes()) == digest, str(path)
    values = {name: read(ROOT/path) for name, path in EVIDENCE.items()}
    verified = values['V4546_verified_handoff.json']
    assert (verified['fresh_reread'], verified['integrated'], verified['pending']) == (5865, 5865, 0)
    assert verified['ledger_sha256'] == LEDGER_SHA and verified['all_jobs_terminal']
    assert verified['candidate_sha256'] == ROM_SHA and verified['regression_tests_passed'] == 78
    assert values['registered_release_verification.json']['whole_ROM_reconstruction_byte_exact']
    startup = values['cold_boot_Lil_startup_town_verification.json']
    assert startup['paired_frame_count'] == 31 and startup['all_current_requested_and_final_framebuffers_equal_V4496']
    assert startup['all_five_postload_actor_model_and_captain_checks_equal']
    visual = values['current_six_frame_visual_review.json']
    assert visual['viewed'] and visual['no_new_display_finding'] and visual['candidate_sha256'] == ROM_SHA
    assert sha((ROOT/visual['sheet']).read_bytes()) == visual['sha256']
    for path, digest in values['B175_completion_receipt.json']['evidence'].items():
        assert sha((ROOT/path).read_bytes()) == digest, path
    assert not values['B176_layout_QA.json']['failures']
    assert values['B176_offline_native_fonts.json']['visual_review_pending']
    registry = read(ROOT/'translations/release_stack.json')
    ledger = read(ROOT/'translations/editorial_review_current_v1.json')
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['release_stack_sha256'] == REGISTRY_SHA and manifest['profile'] == PROFILE
    assert len(manifest['batches']) == 551 and all(manifest['checks'].values())
    assert len(registry['accepted_layers']) == 114 and registry['profiles'][PROFILE]['status'] == 'experimental'
    AUDIT.mkdir(parents=True)
    reconstruction = AUDIT/'promoted_patch_reconstruction_RESEARCH_ONLY.nds'
    apply_xdelta(ROOT/'work/clean.nds', ROM.with_suffix('.xdelta'), reconstruction)
    assert reconstruction.read_bytes() == ROM.read_bytes()
    PACKAGE.mkdir(parents=True)
    verification = PACKAGE/'verification'
    verification.mkdir()
    shutil.copyfile(ROM.with_suffix('.xdelta'), PACKAGE/'translation.xdelta')
    for name, source in [('build_manifest.json.gz', ROM.with_suffix('.manifest.json')),
                         ('build_release_stack.json.gz', ROOT/'translations/release_stack.json')]:
        (PACKAGE/name).write_bytes(gzip.compress(source.read_bytes(), mtime=0))
    (AUDIT/'ledger.before.json.gz').write_bytes(gzip.compress((ROOT/'translations/editorial_review_current_v1.json').read_bytes(), mtime=0))
    (AUDIT/'registry.before.json').write_bytes((ROOT/'translations/release_stack.json').read_bytes())
    for name, source in EVIDENCE.items():
        shutil.copyfile(ROOT/source, verification/name)
    shutil.copyfile(ROOT/visual['sheet'], verification/'current_Lil_startup_and_town_review.png')
    draft = {'family': 'B176', 'draft_objects': 10, 'revised': 5, 'retained': 5,
             'native_planes': 10, 'logical_compiled_alignments': 80,
             'source_consumer_negatives': 18, 'visual_review_pending': True,
             'new_B176_manuscript_integrated_in_promoted_ROM': False,
             'source_prose_or_completion_credit_added': 0, 'resume': RESUME,
             'full_goal_complete': False}
    save(verification/'UNINTEGRATED_B176_status.json', draft)
    promotion = {'format': 'dk4-promoted-checkpoint-v1', 'status': 'promoted', 'main_build': True,
                 'promoted_on': datetime.now(ZoneInfo('America/Indianapolis')).date().isoformat(),
                 'checkpoint': 'V4571', 'user_request': 'lets promote our current build as our new main build and then commit/push to github',
                 'profile': PROFILE, 'rom': ROM.relative_to(ROOT).as_posix(), 'rom_sha256': ROM_SHA,
                 'release_directory': PACKAGE.relative_to(ROOT).as_posix(), 'git_tag': 'promoted-v4541',
                 'patch_sha256': PATCH_SHA, 'source_rom_sha256': CLEAN_SHA,
                 'build_manifest_sha256': MANIFEST_SHA, 'build_registry_sha256': REGISTRY_SHA,
                 'immutable_construction_baseline': deepcopy(registry['canonical_baseline']),
                 'previous_promoted_build': 'releases/all_routes_unified_v4496/promotion.json',
                 'promotion_scope': 'User-designated main checkpoint; construction baseline and accepted-layer status preserved. Buildable profile retains experimental status.',
                 'known_open_scope': SCOPE, 'complete_entries': 5865, 'source_prose_reviewed_entries': 5868,
                 'fresh_contextual_rereads': 5865, 'pending_credited_route_entries': 0,
                 'reviewed_incomplete_COMMON_entries': 3, 'B176_uncredited_draft_objects': 10,
                 'full_editorial_goal_complete': False, 'full_graphics_goal_complete': False,
                 'new_user_cold_boot_test_claimed': False, 'new_emulator_runs_at_promotion': 0,
                 'construction_baseline_rebased': False}
    save(PACKAGE/'promotion.json', promotion)
    save(PACKAGE/'release_manifest.json', {'game': 'Daikoukai Jidai IV / Rota Nova DS',
         'patch_version': 'unified-v4541', 'status': 'promoted', 'main_build': True, 'profile': PROFILE,
         'source_rom_sha256': CLEAN_SHA, 'modified_rom_sha256': ROM_SHA, 'patch_sha256': PATCH_SHA,
         'full_editorial_goal_complete': False, 'full_graphics_goal_complete': False,
         'promotion_record': 'promotion.json', 'notes': SCOPE})
    save(verification/'promotion_reconstruction.json', {'clean_input_sha256': CLEAN_SHA,
         'patch_sha256': PATCH_SHA, 'candidate_sha256': ROM_SHA, 'reconstructed_sha256': sha(reconstruction.read_bytes()),
         'whole_ROM_byte_exact': True, 'new_emulator_runs_at_promotion': 0,
         'original_build_registry_sha256': REGISTRY_SHA, 'producer_sha256': sha(Path(__file__).read_bytes())})
    save(verification/'promotion_test_results.json', {'command': 'python -m pytest tests/test_integrated_release.py tests/test_dialogue_review.py tests/test_dialogue_balanced_wrap.py tests/test_dialogue_pair_phase.py tests/test_dialogue_relocation.py tests/test_lil_editorial_literal_guard.py -q',
         'result': '78 passed in 3.94s', 'exit_code': 0, 'source': 'Observed promotion-turn exec command output before staging', 'new_emulator_runs': 0})
    registry['latest_promoted_build'] = {'status': 'promoted', 'main_build': True, 'profile': PROFILE,
        'rom_sha256': ROM_SHA, 'record': 'translations/promoted_build.json', 'git_tag': 'promoted-v4541', 'construction_baseline_rebased': False}
    assert 'promoted_main_build_v4571' not in ledger and 'lil_B176_draft_status_v4571' not in ledger
    ledger['promoted_main_build_v4571'] = promotion
    ledger['lil_B176_draft_status_v4571'] = draft
    ledger['latest_checkpoint'] = SUMMARY
    mutations = {'translations/release_stack.json': encoded(registry),
                 'translations/promoted_build.json': encoded(promotion),
                 'translations/editorial_review_current_v1.json': encode_ledger(ledger)}
    section = ('## V4571: V4541 promoted as main; B176 draft preserved\n\n' + SUMMARY +
               '\n\nMain build: [Unified V4541](../releases/all_routes_unified_v4541/README.md). ROM SHA-256: `' + ROM_SHA +
               '`. Patch SHA-256: `' + PATCH_SHA + '`. Earlier sections retain their original checkpoint status.\n\nNext: ' + RESUME + '\n\n')
    for name in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md', 'release_build.md']:
        path = 'docs/' + name
        first, rest = (ROOT/path).read_text(encoding='utf-8').split('\n', 1)
        if name == 'editorial_handoff_current.md':
            first = '# Current editorial handoff - V4571'
        mutations[path] = (first + '\n\n' + section + rest).encode('utf-8')
    text = (ROOT/'README.md').read_text(encoding='utf-8')
    old_link = '[Unified V4496](releases/all_routes_unified_v4496/README.md)'
    assert text.count(old_link) == 2
    text = text.replace(old_link, '[Unified V4541](releases/all_routes_unified_v4541/README.md)')
    text = text.replace('Earlier [V4445]', 'Earlier [V4496](releases/all_routes_unified_v4496/README.md), [V4445]')
    text = text.replace('(2026-10-26). Full editorial', '(' + promotion['promoted_on'] + '). Full editorial', 1)
    mutations['README.md'] = text.encode('utf-8')
    ignore = (ROOT/'.gitignore').read_text(encoding='utf-8')
    assert '!releases/all_routes_unified_v4541/*.xdelta' not in ignore
    mutations['.gitignore'] = (ignore + '!releases/all_routes_unified_v4541/*.xdelta\n').encode('utf-8')
    pins = read(ROOT/'translations/rom_retention_pins.json')
    pins.append({'path': str(reconstruction.resolve()), 'reason': 'V4571 main V4541 clean-input patch reconstruction. Preserve every ROM; no pruning. SHA-256 ' + ROM_SHA})
    mutations['translations/rom_retention_pins.json'] = encoded(pins)
    (AUDIT/'staged').mkdir()
    plan = []
    for index, (relative, data) in enumerate(mutations.items()):
        target, planned = ROOT/relative, AUDIT/'staged'/f'{index}.planned'
        before = target.read_bytes()
        (AUDIT/f'{index}.before').write_bytes(before)
        planned.write_bytes(data)
        plan.append({'target': str(target), 'before_sha256': sha(before), 'planned': str(planned), 'planned_sha256': sha(data)})
    save(AUDIT/'mutation_plan.json', plan)
    (PACKAGE/'README.md').write_text(
        '# Main promoted English build: V4541\n\nPromoted on ' + promotion['promoted_on'] +
        ' at the user\'s request. Tag: `promoted-v4541`.\n\n'
        'This cumulative build contains551 manuscript batches and114 accepted layers, including completed Lil B175. Earlier packages, ROMs and translations remain preserved.\n\n'
        '## Apply the patch\n\nSupply an unmodified Japanese ROM with SHA-256 `' + CLEAN_SHA + '`:\n\n'
        '```powershell\npython -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v4541/translation.xdelta --out out/all_routes_combined_v4541_candidate.nds\n```\n\n'
        'Expected ROM SHA-256: `' + ROM_SHA + '`.\n\nPatch SHA-256: `' + PATCH_SHA + '`.\n\n'
        'The complete clean-input patch was freshly reconstructed byte for byte at promotion. ROMs, saves and raw RAM remain local.\n\n'
        '## Verification and coverage\n\nRegistered profile: `' + PROFILE + '`. Canonical construction baseline: `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `' + BASE_SHA + '`. Only SC2 B175 changes from V4496; all335 other blocks and every other file/component, ARM9, COMMON, fonts, graphics and123040 staged bytes remain exact.\n\n'
        'Existing paired Japanese/English content-fixture cold boots display all32 B175 speeches (23 progressive/nine FE), original resource/presentations, C200, first end and normal town return. Second end retains offline native coverage. All256 native alignment cases,128 stored cases and82 atomic negatives pass. Registered New Game/town cold boots pass31 whole-frame comparisons and five actor/captain checks. Viewed visual/completion receipts supersede pending flags in earlier receipts.\n\n'
        'The actual-scene receipt retains14 scoped nontext differences: two samples inside original presentation transitions starting/ending one frame apart, and twelve following sailing-cloud samples. Final map/text panel and five state components agree; PRNG and final whole RGB differ. These targeted automated headless tests do not establish natural event eligibility, earned flags, full-route completion, hardware behavior or future-world equality. Promotion adds no new emulator run or user cold-boot claim. All78 release/dialogue regression tests pass.\n\n'
        '## Unfinished work\n\nThe ledger retains5865 completed contextual rereads,5868 source/prose reviews,3728 revisions and2137 justified retentions, with zero pending credited route drafts. B176 has10 uncredited decisions (five proposed revisions/five retentions), ten offline native planes and80 alignments. Its two sheets still require visual inspection. B176 is outside this ROM; see `verification/UNINTEGRATED_B176_status.json`.\n\n' + SCOPE +
        '\n\nNext: ' + RESUME + '\n\nSee the [current handoff](../../docs/editorial_handoff_current.md).\n\n'
        '## Reproduction records\n\n`build_manifest.json.gz` and `build_release_stack.json.gz` preserve exact original build-time bytes. `checksums.json` covers every other packaged file. `verification/` contains scoped receipts, fresh reconstruction and final audit. Frozen builders, canonical inputs and accepted-layer status remain preserved. The profile retains experimental status; `translations/promoted_build.json` designates the main build.\n', encoding='utf-8', newline='\n')
    save(AUDIT/'staging_receipt.json', {'profile': PROFILE, 'evidence': {path: sha((ROOT/path).read_bytes()) for path in EVIDENCE.values()},
         'producer_sha256': sha(Path(__file__).read_bytes()), 'mutations': len(plan), 'new_emulator_runs': 0, 'ROMs_deleted': 0})
    print(json.dumps({'staged': len(plan), 'whole_patch_reconstruction_byte_exact': True, 'profile': PROFILE}))


def apply():
    plan = read(AUDIT/'mutation_plan.json')
    assert len(plan) == 12 and len({row['target'] for row in plan}) == 12
    for row in plan:
        target, planned = Path(row['target']), Path(row['planned'])
        assert target.is_relative_to(ROOT) and planned.is_relative_to(AUDIT)
        assert sha(target.read_bytes()) == row['before_sha256'], str(target)
        assert sha(planned.read_bytes()) == row['planned_sha256'], str(planned)
    for row in plan:
        target, data = Path(row['target']), Path(row['planned']).read_bytes()
        with target.open('r+b') as stream:
            stream.write(data)
            stream.truncate(len(data))
            stream.flush()
            os.fsync(stream.fileno())
        assert sha(target.read_bytes()) == row['planned_sha256']
    verify()


def verify():
    plan = read(AUDIT/'mutation_plan.json')
    for row in plan:
        assert Path(row['target']).read_bytes() == Path(row['planned']).read_bytes()
    before_registry = read(AUDIT/'registry.before.json')
    registry = read(ROOT/'translations/release_stack.json')
    assert sha((AUDIT/'registry.before.json').read_bytes()) == REGISTRY_SHA
    assert {k: v for k, v in before_registry.items() if k != 'latest_promoted_build'} == {k: v for k, v in registry.items() if k != 'latest_promoted_build'}
    assert registry['latest_promoted_build']['profile'] == PROFILE
    assert registry['profiles'][PROFILE]['status'] == 'experimental' and len(registry['accepted_layers']) == 114
    old_bytes = gzip.decompress((AUDIT/'ledger.before.json.gz').read_bytes())
    assert sha(old_bytes) == LEDGER_SHA
    before, ledger = json.loads(old_bytes), read(ROOT/'translations/editorial_review_current_v1.json')
    allowed = {'latest_checkpoint', 'promoted_main_build_v4571', 'lil_B176_draft_status_v4571'}
    assert not (allowed - {'latest_checkpoint'}) & set(before)
    assert {k: v for k, v in before.items() if k not in allowed} == {k: v for k, v in ledger.items() if k not in allowed}
    assert tuple(ledger[k] for k in ['records_editorially_completed', 'records_with_source_and_prose_pass', 'records_revised_and_integrated', 'retained_wordings_editorially_completed']) == (5865, 5868, 3728, 2137)
    ledger_path = ROOT/'translations/editorial_review_current_v1.json'
    assert ledger_path.read_bytes() == encode_ledger(ledger) and ledger_path.stat().st_size < 100*1024*1024
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    promotion = read(ROOT/'translations/promoted_build.json')
    assert promotion == read(PACKAGE/'promotion.json') == ledger['promoted_main_build_v4571']
    assert promotion['previous_promoted_build'] == 'releases/all_routes_unified_v4496/promotion.json'
    assert promotion['main_build'] and not promotion['construction_baseline_rebased']
    assert ledger['lil_B176_draft_status_v4571'] == read(PACKAGE/'verification/UNINTEGRATED_B176_status.json')
    assert gzip.decompress((PACKAGE/'build_manifest.json.gz').read_bytes()) == ROM.with_suffix('.manifest.json').read_bytes()
    assert gzip.decompress((PACKAGE/'build_release_stack.json.gz').read_bytes()) == (AUDIT/'registry.before.json').read_bytes()
    assert sha(ROM.read_bytes()) == ROM_SHA
    assert ROM.read_bytes() == (AUDIT/'promoted_patch_reconstruction_RESEARCH_ONLY.nds').read_bytes()
    assert (PACKAGE/'translation.xdelta').read_bytes() == ROM.with_suffix('.xdelta').read_bytes()
    assert sha((PACKAGE/'translation.xdelta').read_bytes()) == PATCH_SHA
    assert sha((ROOT/'work/clean.nds').read_bytes()) == CLEAN_SHA
    assert sha((ROOT/'out/raphael_natural_v2_accepted_base.nds').read_bytes()) == BASE_SHA
    receipt = read(AUDIT/'staging_receipt.json')
    assert receipt['producer_sha256'] == sha(Path(__file__).read_bytes())
    for name, source in EVIDENCE.items():
        assert (PACKAGE/'verification'/name).read_bytes() == (ROOT/source).read_bytes()
        assert sha((ROOT/source).read_bytes()) == receipt['evidence'][source]
    visual = read(PACKAGE/'verification/current_six_frame_visual_review.json')
    assert sha((PACKAGE/'verification/current_Lil_startup_and_town_review.png').read_bytes()) == visual['sha256']
    previous = []
    for checksums in sorted((ROOT/'releases').glob('*/checksums.json')):
        if checksums.parent == PACKAGE:
            continue
        for name, digest in read(checksums).items():
            assert sha((checksums.parent/name).read_bytes()) == digest, str(checksums.parent/name)
        previous.append(checksums.parent.name)
    assert 'all_routes_unified_v4496' in previous
    index = next(i for i, row in enumerate(plan) if Path(row['target']).name == 'rom_retention_pins.json')
    pins = read(ROOT/'translations/rom_retention_pins.json')
    assert pins[:-1] == read(AUDIT/f'{index}.before')
    assert Path(pins[-1]['path']).read_bytes() == ROM.read_bytes()
    assert 'Unified V4541' in (ROOT/'README.md').read_text(encoding='utf-8').splitlines()[0]
    assert (ROOT/'docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4571')
    audit = {'checkpoint': 'V4571', 'profile': PROFILE, 'main_build': True,
             'rom_sha256': ROM_SHA, 'patch_sha256': PATCH_SHA, 'manifest_batches': 551, 'accepted_layers': 114,
             'original_manifest_and_registry_byte_exact': True, 'only_registry_promotion_pointer_changed': True,
             'whole_clean_input_patch_reconstruction_byte_exact': True, 'canonical_baseline_unchanged': True,
             'all_prior_ledger_records_and_coverage_preserved': True, 'ledger_sha256': sha(ledger_path.read_bytes()),
             'completed_contextual_reviews': 5865, 'source_prose_reviews': 5868, 'pending_credited_route_reviews': 0,
             'B176_uncredited_draft_objects': 10, 'B176_visual_review_pending': True,
             'previous_release_checksums_verified': previous, 'targeted_tests_passed': 78,
             'new_emulator_runs_at_promotion': 0, 'ROMs_deleted': 0, 'every_prior_ROM_retention_pin_preserved': True,
             'full_goal_active': True, 'full_goal_complete': False,
             'updated_files': {str(Path(row['target']).relative_to(ROOT)): row['planned_sha256'] for row in plan},
             'producer_sha256': sha(Path(__file__).read_bytes())}
    save(AUDIT/'promotion_receipt.json', audit)
    save(PACKAGE/'verification/promotion_final_audit.json', audit)
    checksums = {p.relative_to(PACKAGE).as_posix(): sha(p.read_bytes()) for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'}
    save(PACKAGE/'checksums.json', checksums)
    assert all(sha((PACKAGE/name).read_bytes()) == digest for name, digest in checksums.items())
    print(json.dumps({'promoted_package_verified': True, 'profile': PROFILE, 'files': len(checksums), 'whole_ROM_byte_exact': True, 'all_prior_ledger_records_preserved': True}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['stage', 'apply', 'verify'])
    args = parser.parse_args()
    {'stage': stage, 'apply': apply, 'verify': verify}[args.mode]()
