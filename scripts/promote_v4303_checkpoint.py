"""Stage user-authorized V4303 main designation; preserve construction inputs."""
from __future__ import annotations

import gzip
import hashlib
import json
import shutil
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.xdelta import apply_xdelta

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'work/analysis/promotion_v4331'
PACKAGE = ROOT / 'releases/all_routes_unified_v4303'
PROFILE = 'all-routes-unified-v4303'
ROM_SHA = '6e861308863c5e655aea9927364b2ad3e3bd6200e5cbe52c5bb7d789f4069abe'
PATCH_SHA = '426885bf8defaa6a1a402e85505087ab3caa6aa32374730b90fbaafbaea5abd2'
REGISTRY_SHA = 'cb1afa76cf50763388c9e90632b47a55177f95aacb6bc4690b797a3880898731'
MANIFEST_SHA = 'e2591fdccd0ad5219bdb2a0544f662e95ca8de4742e72e91192454820f958cb6'
LEDGER_SHA = '443c0cad7672600785854e19c1bda1f7843803decf11701212909ab4972777ed'
CLEAN_SHA = 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
BASE_SHA = '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
RESUME = ('Complete B171 relocation and stored/native references, then paired Japanese/English content fixtures preserving all45 commands, original4500/4621/61FF/6325 transitions, C200 and both ends. Observe portraits, dream/morning presentation, first-end reachability and normal return. Then atomic compiler negatives, registered cumulative integration, exact clean-input patch and fresh startup checks. Existing clean glosses, names/voices/source controls/terms and native approval V4328 remain complete. Continue B172-B180 and every wider editorial family.')
SCOPE = ('The full contextual editorial goal stays active across every remaining storyline, shared shop/town exchange, random scene, Help and other player-facing prose. B171 has37 pending reviews outside this ROM; B172-B180 has161 physical speech leads, not a full-project denominator. Preserve COMMON750-752, canonical Maria32 SC3B97, SourceItems/LocalProduct, five named-target leads, exact-record Proof consistency, Samwell full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques remain separate. Retain the later older-record technical re-audit/queued0D gap.')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def encoded(value, crlf=False):
    text = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    return (text.replace('\n', '\r\n') if crlf else text).encode('utf-8')


def save(path, value):
    path.write_bytes(encoded(value))


def main():
    assert Path.cwd() == ROOT and not AUDIT.exists() and not PACKAGE.exists()
    rom = ROOT / 'out/all_routes_combined_v4303_candidate.nds'
    patch, manifest = rom.with_suffix('.xdelta'), rom.with_suffix('.manifest.json')
    registry_path = ROOT / 'translations/release_stack.json'
    ledger_path = ROOT / 'translations/editorial_review_current_v1.json'
    clean, base = ROOT / 'work/clean.nds', ROOT / 'out/raphael_natural_v2_accepted_base.nds'
    for path, digest in [(rom, ROM_SHA), (patch, PATCH_SHA), (manifest, MANIFEST_SHA),
                         (registry_path, REGISTRY_SHA), (ledger_path, LEDGER_SHA), (clean, CLEAN_SHA), (base, BASE_SHA)]:
        assert sha(path.read_bytes()) == digest, str(path)
    build, registry, ledger = map(read, [manifest, registry_path, ledger_path])
    assert build['profile'] == PROFILE and build['release_stack_sha256'] == REGISTRY_SHA
    assert build['candidate_sha256'] == ROM_SHA and build['base_sha256'] == BASE_SHA
    assert len(build['batches']) == 546 and len(registry['accepted_layers']) == 114
    assert all(build['checks'].values()) and registry['canonical_baseline']['sha256'] == BASE_SHA
    assert registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4251'
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass'],
            ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (5725, 5765, 3635, 2090)
    evidence = {
        'registered_release_verification.json': 'work/analysis/lil_B170_release_v4304/registered_release_verification.json',
        'cold_boot_Lil_startup_town_verification.json': 'work/analysis/lil_B170_startup_v4306/cold_boot_Lil_startup_town_verification.json',
        'current_six_frame_visual_review.json': 'work/analysis/lil_B170_startup_v4306/current_six_frame_visual_review.json',
        'B170_completion_receipt.json': 'work/analysis/lil_B170_completion_v4307/completion_receipt.json',
        'B171_verified_handoff.json': 'work/analysis/editorial_handoff_verification_v4330/verified_handoff.json',
        'B171_native_approval.json': 'work/analysis/lil_B171_native_approval_v4328/approval_receipt.json',
        'B171_checkpoint_receipt.json': 'work/analysis/lil_B171_checkpoint_v4329/checkpoint_receipt.json',
        'unfinished_editorial_scope_inventory.json': 'work/analysis/lil_B171_checkpoint_v4329/unfinished_editorial_scope_inventory.json',
    }
    release, startup, visual, completion, verified, native, checkpoint, scope = [read(ROOT / p) for p in evidence.values()]
    assert release['candidate_sha256'] == startup['candidate_sha256'] == verified['candidate_sha256'] == ROM_SHA
    assert release['manifest_sha256'] == MANIFEST_SHA and release['patch_sha256'] == PATCH_SHA
    assert release['whole_ROM_reconstruction_byte_exact'] and verified['ledger_sha256'] == LEDGER_SHA
    assert (verified['fresh_reread'], verified['integrated'], verified['pending']) == (5762, 5725, 37)
    assert startup['paired_frame_count'] == 31 and startup['all_current_requested_and_final_framebuffers_equal_V4251']
    assert startup['all_five_postload_actor_model_and_captain_checks_equal']
    assert visual['viewed'] and visual['no_new_display_finding']
    assert sha((ROOT / visual['sheet']).read_bytes()) == visual['sha256']
    for receipt in [completion, checkpoint]:
        for path, digest in receipt['evidence'].items():
            assert sha((ROOT / path).read_bytes()) == digest, path
    manuscript = ROOT / 'translations/lil_B171_editorial_manuscript_v4.json'
    assert len(read(manuscript)['records']) == 37
    assert (native['revised'], native['retained'], native['progressive_planes']) == (24, 13, 37)
    AUDIT.mkdir(parents=True)
    reconstruction = AUDIT / 'promoted_patch_reconstruction_RESEARCH_ONLY.nds'
    apply_xdelta(clean, patch, reconstruction)
    assert reconstruction.read_bytes() == rom.read_bytes()
    PACKAGE.mkdir(parents=True)
    verification = PACKAGE / 'verification'
    verification.mkdir()
    shutil.copyfile(patch, PACKAGE / 'translation.xdelta')
    (PACKAGE / 'build_manifest.json.gz').write_bytes(gzip.compress(manifest.read_bytes(), mtime=0))
    (PACKAGE / 'build_release_stack.json.gz').write_bytes(gzip.compress(registry_path.read_bytes(), mtime=0))
    (AUDIT / 'ledger.before.json.gz').write_bytes(gzip.compress(ledger_path.read_bytes(), mtime=0))
    (AUDIT / 'registry.before.json').write_bytes(registry_path.read_bytes())
    evidence_hashes = {}
    for name, source in evidence.items():
        shutil.copyfile(ROOT / source, verification / name)
        evidence_hashes[source] = sha((ROOT / source).read_bytes())
    shutil.copyfile(ROOT / visual['sheet'], verification / 'current_Lil_startup_and_town_review.png')
    pending = {
        'objects': 37, 'proposed_revisions': 24, 'justified_retentions': 13,
        'status': 'contextual/native approved; relocation, stored references, representative gameplay and registered integration pending',
        'manuscript': manuscript.relative_to(ROOT).as_posix(), 'manuscript_sha256': sha(manuscript.read_bytes()),
        'integrated_in_promoted_ROM': False, 'new_editorial_ledger_credit_added': 0,
        'B171_actual_gameplay_coverage': False, 'new_gameplay_runs_at_promotion': 0,
        'resume': RESUME, 'full_goal_complete': False,
    }
    save(verification / 'UNINTEGRATED_B171_status.json', pending)
    promotion = {
        'format': 'dk4-promoted-checkpoint-v1', 'status': 'promoted', 'main_build': True,
        'promoted_on': '2026-10-26', 'checkpoint': 'V4331',
        'user_request': 'lets promote our current build as our new main build and then commit/push to github',
        'profile': PROFILE, 'rom': rom.relative_to(ROOT).as_posix(), 'rom_sha256': ROM_SHA,
        'release_directory': PACKAGE.relative_to(ROOT).as_posix(), 'git_tag': 'promoted-v4303',
        'patch_sha256': PATCH_SHA, 'source_rom_sha256': CLEAN_SHA,
        'build_manifest_sha256': MANIFEST_SHA, 'build_registry_sha256': REGISTRY_SHA,
        'immutable_construction_baseline': deepcopy(registry['canonical_baseline']),
        'previous_promoted_build': 'releases/all_routes_unified_v4251/promotion.json',
        'promotion_scope': 'User-designated main cumulative checkpoint; immutable construction baseline, accepted-layer status and frozen source/hash contracts remain unchanged. Buildable profile retains experimental status; this record designates the main build.',
        'known_open_scope': SCOPE, 'complete_entries': 5725, 'source_prose_reviewed_entries': 5765,
        'fresh_contextual_rereads': 5762, 'pending_B171_entries': 37,
        'reviewed_incomplete_COMMON_entries': 3,
        'full_editorial_goal_complete': False, 'full_graphics_goal_complete': False,
        'new_user_cold_boot_test_claimed': False, 'new_emulator_runs_at_promotion': 0,
        'construction_baseline_rebased': False,
    }
    save(PACKAGE / 'promotion.json', promotion)
    save(PACKAGE / 'release_manifest.json', {
        'game': 'Daikoukai Jidai IV / Rota Nova DS', 'patch_version': 'unified-v4303',
        'status': 'promoted', 'main_build': True, 'profile': PROFILE,
        'source_rom_sha256': CLEAN_SHA, 'modified_rom_sha256': ROM_SHA, 'patch_sha256': PATCH_SHA,
        'full_graphics_goal_complete': False, 'full_editorial_goal_complete': False,
        'promotion_record': 'promotion.json', 'notes': SCOPE,
    })
    save(verification / 'promotion_reconstruction.json', {
        'clean_input_sha256': CLEAN_SHA, 'patch_sha256': PATCH_SHA, 'candidate_sha256': ROM_SHA,
        'reconstructed_sha256': sha(reconstruction.read_bytes()), 'whole_ROM_byte_exact': True,
        'new_emulator_runs_at_promotion': 0, 'original_build_registry_sha256': REGISTRY_SHA,
        'producer': 'scripts/promote_v4303_checkpoint.py', 'producer_sha256': sha(Path(__file__).read_bytes()),
    })
    save(verification / 'promotion_test_results.json', {
        'command': 'python -m pytest tests/test_integrated_release.py tests/test_dialogue_review.py tests/test_dialogue_balanced_wrap.py tests/test_dialogue_pair_phase.py tests/test_dialogue_relocation.py tests/test_lil_editorial_literal_guard.py -q',
        'result': '78 passed in 3.86s', 'exit_code': 0, 'new_emulator_runs': 0,
    })
    registry['latest_promoted_build'] = {
        'status': 'promoted', 'main_build': True, 'profile': PROFILE, 'rom_sha256': ROM_SHA,
        'record': 'translations/promoted_build.json', 'git_tag': 'promoted-v4303',
        'construction_baseline_rebased': False,
    }
    summary = ("V4331 promotes verified V4303 as the new main cumulative build at the user's request. All546 manuscript batches and114 accepted layers are preserved, including completed B170. Fresh clean-input patch reconstruction is byte exact;78 integrated-release/dialogue regression tests pass. Coverage stays5762 fresh rereads,5725 completed,37 pending,5765 source/prose,3635 historically revised/2090 retained and4126 integrated route objects. B171's24 revisions/13 justified retentions remain pending outside the promoted ROM. Promotion adds no editorial credit, emulator run or user cold-boot claim. Preserve V4251 and every earlier package, ROM, translation, draft and executed producer/proof/failure. The immutable construction baseline and accepted-layer status are unchanged. " + SCOPE)
    ledger['promoted_main_build_v4331'] = promotion
    ledger['lil_B171_preintegration_review_v4331'] = pending
    ledger['latest_checkpoint'] = summary
    section = ('## V4331: V4303 promoted as main; B171 reviews preserved\n\n' + summary +
               '\n\nMain build: [Unified V4303](../releases/all_routes_unified_v4303/README.md). ROM SHA-256: `' + ROM_SHA +
               '`. Patch SHA-256: `' + PATCH_SHA + '`. Earlier sections retain their original checkpoint status.\n\nNext: ' + RESUME + '\n\n')
    mutations = {
        'translations/release_stack.json': encoded(registry, crlf=True),
        'translations/promoted_build.json': encoded(promotion, crlf=True),
        'translations/editorial_review_current_v1.json': encoded(ledger, crlf=True),
    }
    for name in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md', 'release_build.md']:
        path = 'docs/' + name
        first, rest = (ROOT / path).read_text(encoding='utf-8').split('\n', 1)
        if name == 'editorial_handoff_current.md':
            first = '# Current editorial handoff - V4331'
        mutations[path] = (first + '\n\n' + section + rest).encode('utf-8')
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    assert readme.count('[Unified V4251](releases/all_routes_unified_v4251/README.md)') == 2
    readme = readme.replace('[Unified V4251](releases/all_routes_unified_v4251/README.md)', '[Unified V4303](releases/all_routes_unified_v4303/README.md)')
    readme = readme.replace('Earlier [V4204]', 'Earlier [V4251](releases/all_routes_unified_v4251/README.md), [V4204]')
    mutations['README.md'] = readme.encode('utf-8')
    ignore = (ROOT / '.gitignore').read_text(encoding='utf-8')
    assert '!releases/all_routes_unified_v4303/*.xdelta' not in ignore
    mutations['.gitignore'] = (ignore + '!releases/all_routes_unified_v4303/*.xdelta\n').encode('utf-8')
    pins = read(ROOT / 'translations/rom_retention_pins.json')
    pins.append({'path': str(reconstruction.resolve()), 'reason': 'V4331 promoted V4303 exact clean-input patch reconstruction. Preserve all generated ROMs; no pruning. SHA-256 ' + ROM_SHA})
    mutations['translations/rom_retention_pins.json'] = encoded(pins, crlf=True)
    staged = AUDIT / 'staged'
    staged.mkdir()
    plan = []
    for index, (relative, data) in enumerate(mutations.items()):
        target = ROOT / relative
        before = target.read_bytes()
        (AUDIT / (str(index) + '.before')).write_bytes(before)
        planned = staged / (str(index) + '.planned')
        planned.write_bytes(data)
        plan.append({'target': str(target), 'before_sha256': sha(before), 'planned': str(planned), 'planned_sha256': sha(data)})
    save(AUDIT / 'mutation_plan.json', plan)
    (PACKAGE / 'README.md').write_text(
        '# Main promoted English build: V4303\n\nPromoted on 2026-10-26 at the user\'s request. Tag: `promoted-v4303`.\n\n'
        'This cumulative build contains 546 manuscript batches and 114 accepted layers, including completed Lil B170. Earlier releases and every local ROM and translation remain preserved.\n\n'
        '## Apply the patch\n\nSupply your unmodified Japanese ROM with SHA-256 `' + CLEAN_SHA + '`:\n\n'
        '```powershell\npython -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v4303/translation.xdelta --out out/all_routes_combined_v4303_candidate.nds\n```\n\n'
        'Expected ROM SHA-256: `' + ROM_SHA + '`.\n\nPatch SHA-256: `' + PATCH_SHA + '`.\n\n'
        'The complete clean-input patch was freshly reconstructed byte for byte at promotion. ROMs, saves and raw RAM captures remain local. Retained ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v4303_candidate.nds`.\n\n'
        '## Verification and coverage\n\nRegistered profile: `all-routes-unified-v4303`. Against V4251 only SC2 B170 changes. All335 other SC2 blocks and every other file/component, ARM9, COMMON, fonts, graphics and123040 staged bytes remain exact. All33 complete native planes,264 logical/compiled and132 stored alignment cases pass.\n\n'
        'Existing paired20001-frame Japanese/English content-fixture cold boots cover all33 B170 speeches, original presentations, pause, effects and normal town return. The first end is observed; the second has offline decoder coverage. Later SeaView outcomes differ consistently with documented scheduler entropy; focused repeats and persistent-state comparisons are retained without an equal-world claim. Two registered opening/town cold boots pass31 whole-frame comparisons andfive actor/captain checks. Viewed startup and completion receipts supersede historical pending flags. The inherited town battery is test data. These targeted automated headless emulator tests do not establish natural event eligibility, earned flags, full-route completion or hardware verification. Promotion adds no new emulator run or user cold-boot claim.\n\n'
        'At promotion,78 integrated-release/dialogue regression tests passed.\n\n'
        '## Unfinished work\n\nThe ledger retains5762 fresh contextual rereads:5725 completed and37 pending, with5765 source/prose reviews. B171 has37 contextual/native-approved speeches:24 revisions and13 justified retentions. **Those revisions are outside this ROM.** Relocation, stored references, representative gameplay and registered integration remain pending. See `verification/UNINTEGRATED_B171_status.json` for exact resume scope.\n\n'
        + SCOPE + '\n\nSee the [current handoff](../../docs/editorial_handoff_current.md).\n\n'
        '## Reproduction records\n\n`build_manifest.json.gz` and `build_release_stack.json.gz` preserve exact original build-time bytes; decompressed hashes appear in `promotion.json`. The current registry changes only its promotion pointer. `checksums.json` covers every other packaged file. `verification/` contains scoped receipts, fresh reconstruction and final audit.\n\n'
        'Immutable construction baseline: `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `' + BASE_SHA + '`. Frozen builders, canonical inputs and accepted-layer status are preserved. Buildable profiles retain experimental status; `translations/promoted_build.json` designates the main build.\n',
        encoding='utf-8', newline='\n')
    save(AUDIT / 'staging_receipt.json', {'profile': PROFILE, 'ROM_sha256': ROM_SHA, 'evidence': evidence_hashes,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'mutations': len(plan), 'new_emulator_runs': 0, 'ROMs_deleted': 0})
    print(json.dumps({'staged': len(plan), 'profile': PROFILE, 'whole_patch_reconstruction_byte_exact': True, 'B171_pending': 37}))


if __name__ == '__main__':
    main()
