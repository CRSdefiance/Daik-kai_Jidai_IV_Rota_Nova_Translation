"""Promote the verified cumulative V4204 checkpoint without changing ROM bytes."""
from __future__ import annotations

import gzip
import hashlib
import json
import shutil
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.xdelta import apply_xdelta

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'work/analysis/promotion_v4226'
PACKAGE = ROOT / 'releases/all_routes_unified_v4204'
PROFILE = 'all-routes-unified-v4204'
ROM_SHA = 'c4bf500bd4ab5a291259558188ce60d4560ffb85ab0c850714739c11c5de2670'
PATCH_SHA = '92b8cf46009deeb7623b66dfc4a0390e711ca0c7a2f5fe1ca44ca954277380af'
REGISTRY_SHA = 'a0f84d539dd41aed1d709aab34677bdfc228e17f974c2f76f69c31188488bc40'
MANIFEST_SHA = '0df708521594f4f6c1c7942dc10a29fc6ce5bcbffe2c2bd280b12e881f0fa83e'
CLEAN_SHA = 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
BASE_SHA = '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
LEDGER_SHA = 'de8a0a0488e82777cc7837bf459c728bc399389e366b7baa837ed99d688aacc7'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def encoded(value, crlf=False):
    text = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    return (text.replace('\n', '\r\n') if crlf else text).encode('utf-8')


def save(path, value):
    path.write_bytes(encoded(value))


def main():
    assert Path.cwd() == ROOT and not AUDIT.exists() and not PACKAGE.exists()
    rom = ROOT / 'out/all_routes_combined_v4204_candidate.nds'
    patch, manifest = rom.with_suffix('.xdelta'), rom.with_suffix('.manifest.json')
    registry_path = ROOT / 'translations/release_stack.json'
    ledger_path = ROOT / 'translations/editorial_review_current_v1.json'
    clean = ROOT / 'work/clean.nds'
    base = ROOT / 'out/raphael_natural_v2_accepted_base.nds'
    for path, digest in [(rom, ROM_SHA), (patch, PATCH_SHA), (manifest, MANIFEST_SHA),
                         (registry_path, REGISTRY_SHA), (ledger_path, LEDGER_SHA),
                         (clean, CLEAN_SHA), (base, BASE_SHA)]:
        assert sha(path.read_bytes()) == digest, str(path)
    build, registry, ledger = map(read, [manifest, registry_path, ledger_path])
    assert build['profile'] == PROFILE and build['release_stack_sha256'] == REGISTRY_SHA
    assert len(build['batches']) == 544 and len(registry['accepted_layers']) == 114
    assert all(build['checks'].values()) and registry['canonical_baseline']['sha256'] == BASE_SHA
    assert registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4160'
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass'],
            ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (5656, 5659, 3595, 2061)
    evidence = {
        'registered_release_verification.json': 'work/analysis/lil_B168_release_v4205/registered_release_verification.json',
        'cold_boot_Lil_startup_town_verification.json': 'work/analysis/lil_B168_startup_v4207/cold_boot_Lil_startup_town_verification.json',
        'current_six_frame_visual_review.json': 'work/analysis/lil_B168_startup_v4207/current_six_frame_visual_review.json',
        'B168_completion_receipt.json': 'work/analysis/lil_B168_completion_v4208/completion_receipt.json',
        'B168_verified_handoff.json': 'work/analysis/editorial_handoff_verification_v4209/verified_handoff.json',
    }
    release, startup, visual, completion, verified = [read(ROOT / p) for p in evidence.values()]
    assert release['candidate_sha256'] == startup['candidate_sha256'] == verified['candidate_sha256'] == ROM_SHA
    assert release['manifest_sha256'] == MANIFEST_SHA and release['patch_sha256'] == PATCH_SHA
    assert release['whole_ROM_reconstruction_byte_exact'] and verified['ledger_sha256'] == LEDGER_SHA
    assert startup['paired_frame_count'] == 31 and startup['all_current_requested_and_final_framebuffers_equal_V4160']
    assert startup['all_five_postload_actor_model_and_captain_checks_equal']
    assert visual['viewed'] and visual['no_new_display_finding']
    assert sha((ROOT / visual['sheet']).read_bytes()) == visual['sha256']
    for path, digest in completion['evidence'].items():
        assert sha((ROOT / path).read_bytes()) == digest, path
    b169 = ROOT / 'translations/lil_B169_editorial_manuscript_v1.json'
    draft = read(b169)
    assert len(draft['records']) == 36
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
        'objects': 36, 'proposed_revisions': 19, 'justified_retentions': 17,
        'status': 'clean-first-contextual-draft; automatic-layout-failed; no-native-approval-or-integration',
        'manuscript': b169.relative_to(ROOT).as_posix(), 'manuscript_sha256': sha(b169.read_bytes()),
        'layout_findings': 'work/analysis/lil_B169_layout_v4224/all36_paragraph_layout_QA.json',
        'layout_findings_sha256': sha((ROOT / 'work/analysis/lil_B169_layout_v4224/all36_paragraph_layout_QA.json').read_bytes()),
        'resume': 'Resolve R32 split Mikhail Letzel, R41 weak ending those and R167 weak ending is without weakening guards or losing source meaning. Then full native/visual approval, ledger reconciliation, relocation, stored references, representative content and registered release/startup checks.',
        'editorial_ledger_credit_added': 0, 'integrated_in_promoted_ROM': False,
        'new_gameplay_runs': 0, 'full_goal_complete': False,
    }
    save(verification / 'UNINTEGRATED_B169_status.json', pending)
    (verification / 'UNINTEGRATED_B169_layout_QA.json.gz').write_bytes(gzip.compress((ROOT / pending['layout_findings']).read_bytes(), mtime=0))
    scope = ('Full contextual editorial review remains active across remaining storylines, shared shop/town dialogue, random scenes, Help and other player-facing prose. B169 has36 uncredited draft objects outside this ROM. Preserve COMMON750-752, canonical Maria32 SC3 B97, SourceItems/LocalProduct, five named-target leads, exact-record Proof consistency, Samwell full-catalogue middle-field lead, B157 provenance amendment, separate graphics/all18 plaques and the later older-record technical re-audit/queued0D gap.')
    promotion = {
        'format': 'dk4-promoted-checkpoint-v1', 'status': 'promoted', 'main_build': True,
        'promoted_on': '2026-10-26', 'checkpoint': 'V4226',
        'user_request': 'lets promote our current build as our new main build and then commit/push to github',
        'profile': PROFILE, 'rom': rom.relative_to(ROOT).as_posix(), 'rom_sha256': ROM_SHA,
        'release_directory': PACKAGE.relative_to(ROOT).as_posix(), 'git_tag': 'promoted-v4204',
        'patch_sha256': PATCH_SHA, 'source_rom_sha256': CLEAN_SHA,
        'build_manifest_sha256': MANIFEST_SHA, 'build_registry_sha256': REGISTRY_SHA,
        'immutable_construction_baseline': deepcopy(registry['canonical_baseline']),
        'previous_promoted_build': 'releases/all_routes_unified_v4160/promotion.json',
        'promotion_scope': 'User-designated main cumulative checkpoint. Preserve immutable construction baseline, accepted-layer status and frozen source/hash contracts. Registry buildable profile remains experimental; this record designates the main build.',
        'known_open_scope': scope, 'complete_entries': 5656, 'source_prose_reviewed_entries': 5659,
        'reviewed_incomplete_COMMON_entries': 3, 'unintegrated_uncredited_B169_objects': 36,
        'full_editorial_goal_complete': False, 'full_graphics_goal_complete': False,
        'new_user_cold_boot_test_claimed': False, 'new_emulator_runs_at_promotion': 0,
        'construction_baseline_rebased': False,
    }
    save(PACKAGE / 'promotion.json', promotion)
    save(PACKAGE / 'release_manifest.json', {
        'game': 'Daikoukai Jidai IV / Rota Nova DS', 'patch_version': 'unified-v4204',
        'status': 'promoted', 'main_build': True, 'profile': PROFILE,
        'source_rom_sha256': CLEAN_SHA, 'modified_rom_sha256': ROM_SHA, 'patch_sha256': PATCH_SHA,
        'full_graphics_goal_complete': False, 'full_editorial_goal_complete': False,
        'promotion_record': 'promotion.json', 'notes': scope,
    })
    save(verification / 'promotion_reconstruction.json', {
        'clean_input_sha256': CLEAN_SHA, 'patch_sha256': PATCH_SHA, 'candidate_sha256': ROM_SHA,
        'reconstructed_sha256': sha(reconstruction.read_bytes()), 'whole_ROM_byte_exact': True,
        'new_emulator_runs_at_promotion': 0, 'original_build_registry_sha256': REGISTRY_SHA,
        'producer': 'scripts/promote_v4204_checkpoint.py', 'producer_sha256': sha(Path(__file__).read_bytes()),
    })
    save(verification / 'promotion_test_results.json', {
        'command': 'python -m pytest tests/test_integrated_release.py tests/test_dialogue_review.py tests/test_dialogue_balanced_wrap.py tests/test_dialogue_pair_phase.py tests/test_dialogue_relocation.py tests/test_lil_editorial_literal_guard.py -q',
        'result': '78 passed in 4.72s', 'exit_code': 0, 'new_emulator_runs': 0,
    })
    registry['latest_promoted_build'] = {
        'status': 'promoted', 'main_build': True, 'profile': PROFILE, 'rom_sha256': ROM_SHA,
        'record': 'translations/promoted_build.json', 'git_tag': 'promoted-v4204',
        'construction_baseline_rebased': False,
    }
    summary = ('V4226 promotes verified V4204 as the new main cumulative build at the user\'s request. All544 manuscript batches and114 accepted layers are preserved, including completed B168. The packaged clean-input patch was freshly reconstructed byte for byte. Coverage remains5656 completed contextual rereads,5659 source/prose,3595 historically revised and2061 retained, with4057 integrated route objects and zero credited records pending. B169\'s36 separate draft objects (19 proposed revisions/17 justified retentions) remain uncredited and outside this ROM; automatic layout has three unresolved findings. Promotion adds no review credit, new emulator run or user cold-boot claim. Earlier V4160/V4046/V1492 builds and every ROM, translation, draft, executed producer/proof/failure remain preserved. Immutable construction inputs and accepted-layer status are unchanged. ' + scope)
    ledger['promoted_main_build_v4226'] = promotion
    ledger['lil_B169_preintegration_review_v4226'] = pending
    ledger['latest_checkpoint'] = summary
    section = ('## V4226: V4204 promoted as main; B169 draft preserved\n\n' + summary +
               '\n\nMain build: [Unified V4204](../releases/all_routes_unified_v4204/README.md). ROM SHA-256: `' + ROM_SHA +
               '`. Patch SHA-256: `' + PATCH_SHA + '`. Earlier sections describe their original checkpoints.\n\nNext: ' + pending['resume'] +
               ' Continue B170-B180 and every wider editorial family. Remaining B169-B180 has267 physical speeches, not a full-project denominator. Full goal active.\n\n')
    mutations = {
        'translations/release_stack.json': encoded(registry, crlf=True),
        'translations/promoted_build.json': encoded(promotion, crlf=True),
        'translations/editorial_review_current_v1.json': encoded(ledger, crlf=True),
    }
    for name in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md', 'release_build.md']:
        path = 'docs/' + name
        first, rest = (ROOT / path).read_text(encoding='utf-8').split('\n', 1)
        if name == 'editorial_handoff_current.md':
            first = '# Current editorial handoff - V4226'
        mutations[path] = (first + '\n\n' + section + rest).encode('utf-8')
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    readme = readme.replace('[Unified V4160](releases/all_routes_unified_v4160/README.md)', '[Unified V4204](releases/all_routes_unified_v4204/README.md)')
    readme = readme.replace('Earlier [V4046]', 'Earlier [V4160](releases/all_routes_unified_v4160/README.md), [V4046]')
    mutations['README.md'] = readme.encode('utf-8')
    ignore = (ROOT / '.gitignore').read_text(encoding='utf-8')
    assert '!releases/all_routes_unified_v4204/*.xdelta' not in ignore
    mutations['.gitignore'] = (ignore + '!releases/all_routes_unified_v4204/*.xdelta\n').encode('utf-8')
    pins = read(ROOT / 'translations/rom_retention_pins.json')
    pins.append({'path': str(reconstruction.resolve()), 'reason': 'V4226 promoted V4204 byte-exact clean-input patch reconstruction. Preserve all ROMs; no pruning. SHA-256 ' + ROM_SHA})
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
        '# Main promoted English build: V4204\n\nPromoted on 2026-10-26 at the user\'s request. Tag: `promoted-v4204`.\n\n'
        'This cumulative build contains544 manuscript batches and114 accepted layers, including the completed Lil B168 review. Earlier releases and all local ROMs/translations are preserved.\n\n'
        '## Apply the patch\n\nSupply your unmodified Japanese ROM with SHA-256 `' + CLEAN_SHA + '`:\n\n'
        '```powershell\npython -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v4204/translation.xdelta --out out/all_routes_combined_v4204_candidate.nds\n```\n\n'
        'Expected ROM SHA-256: `' + ROM_SHA + '`.\n\nPatch SHA-256: `' + PATCH_SHA + '`.\n\n'
        'The complete clean-input patch reconstruction was rerun byte for byte at promotion. ROMs, saves and raw RAM captures remain local. Retained ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v4204_candidate.nds`.\n\n'
        '## Verification and coverage\n\nRegistered profile: `all-routes-unified-v4204`. Against V4160 only SC2 B168 changes; all335 other SC2 blocks and every other file/component, ARM9, COMMON, fonts, graphics and123040-byte staged payload remain exact. All54 complete native speech/system planes,432 logical/compiled and216 stored alignment cases pass.\n\n'
        'Existing paired20001-frame Japanese/English cold boots cover51 selected B168 speeches, original effects and normal town return. Three conditional remarks have offline native coverage only. Two additional registered opening/town cold boots pass31 whole-frame comparisons and five actor/captain checks. Viewed startup and completion receipts supersede earlier pending flags in the historical release/startup receipts. The inherited town battery is test data. These targeted automated headless emulator tests do not establish natural event eligibility, full-route completion, hardware verification or the item-information X mechanic. Promotion adds no new emulator or user cold-boot claim.\n\n'
        'At promotion78 existing integrated-release, dialogue-review, wrapping, pair-phase, relocation and literal-guard tests passed.\n\n'
        '## Unfinished work\n\nThe ledger retains5656 completed contextual reviews (3595 historically revised/2061 retained) and5659 source/prose reviews. B169 has36 draft objects:19 proposed revisions and17 justified retentions. **Those revisions are outside this ROM and remain uncredited.** Its automatic layout has three findings; full native/visual approval and later integration checks remain pending. The packaged B169 status identifies exact resume references.\n\n'
        + scope + '\n\nSee the [current handoff](../../docs/editorial_handoff_current.md).\n\n'
        '## Reproduction records\n\n`build_manifest.json.gz` and `build_release_stack.json.gz` preserve exact original build-time bytes; decompressed hashes are in `promotion.json`. The current registry changes only its promotion pointer. `checksums.json` covers every other packaged file. `verification/` contains scoped receipts, fresh reconstruction and final audit.\n\n'
        'Immutable construction baseline: `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `' + BASE_SHA + '`. Frozen builders, canonical inputs and accepted-layer status are preserved. Registry buildable profiles retain experimental status; `translations/promoted_build.json` designates the main build.\n',
        encoding='utf-8', newline='\n')
    save(AUDIT / 'staging_receipt.json', {'profile': PROFILE, 'ROM_sha256': ROM_SHA, 'evidence': evidence_hashes, 'producer_sha256': sha(Path(__file__).read_bytes()), 'mutations': len(plan), 'new_emulator_runs': 0, 'ROMs_deleted': 0})
    print(json.dumps({'staged': len(plan), 'profile': PROFILE, 'whole_patch_reconstruction_byte_exact': True, 'B169_uncredited': 36}))


if __name__ == '__main__':
    main()
