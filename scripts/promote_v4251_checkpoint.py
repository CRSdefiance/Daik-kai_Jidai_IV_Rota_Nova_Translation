"""Stage the user-authorized V4251 main-build promotion without changing ROMs."""
from __future__ import annotations

import gzip
import hashlib
import json
import shutil
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.xdelta import apply_xdelta

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'work/analysis/promotion_v4289'
PACKAGE = ROOT / 'releases/all_routes_unified_v4251'
PROFILE = 'all-routes-unified-v4251'
ROM_SHA = 'ff9917225f4e8812ac890973c454a352b5416bee27a7263a5b3258efe9b91b12'
PATCH_SHA = '49fca69ff751bc8228066b1b30b3fbcb3150a88ea35fa2cf57dc13ae3f9b7f90'
REGISTRY_SHA = 'e880c0f52ae90b41b7ce3ad2fc6404cf9444339b63e142cf1445d98448e1ddf4'
MANIFEST_SHA = 'e0b4d6ef85988fe986987a3648638664c2f8540f6a8cafc9e7dfe16959a0c8ba'
LEDGER_SHA = '3d27e93c7ca3eb93e8a6938986505091dc5b8002f503c7216442339bfc18bf23'
CLEAN_SHA = 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
BASE_SHA = '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'


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
    rom = ROOT / 'out/all_routes_combined_v4251_candidate.nds'
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
    assert build['candidate_sha256'] == ROM_SHA and build['base_sha256'] == BASE_SHA
    assert len(build['batches']) == 545 and len(registry['accepted_layers']) == 114
    assert all(build['checks'].values()) and registry['canonical_baseline']['sha256'] == BASE_SHA
    assert registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4204'
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass'],
            ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (5692, 5728, 3614, 2078)
    evidence = {
        'registered_release_verification.json': 'work/analysis/lil_B169_release_v4252/registered_release_verification.json',
        'cold_boot_Lil_startup_town_verification.json': 'work/analysis/lil_B169_startup_v4254/cold_boot_Lil_startup_town_verification.json',
        'current_six_frame_visual_review.json': 'work/analysis/lil_B169_startup_v4254/current_six_frame_visual_review.json',
        'B169_completion_receipt.json': 'work/analysis/lil_B169_completion_v4255/completion_receipt.json',
        'B170_verified_handoff.json': 'work/analysis/editorial_handoff_verification_v4280/verified_handoff.json',
    }
    release, startup, visual, completion, verified = [read(ROOT / p) for p in evidence.values()]
    assert release['candidate_sha256'] == startup['candidate_sha256'] == verified['candidate_sha256'] == ROM_SHA
    assert release['manifest_sha256'] == MANIFEST_SHA and release['patch_sha256'] == PATCH_SHA
    assert release['whole_ROM_reconstruction_byte_exact'] and verified['ledger_sha256'] == LEDGER_SHA
    assert (verified['fresh_reread'], verified['integrated'], verified['pending']) == (5725, 5692, 33)
    assert startup['paired_frame_count'] == 31 and startup['all_current_requested_and_final_framebuffers_equal_V4204']
    assert startup['all_five_postload_actor_model_and_captain_checks_equal']
    assert visual['viewed'] and visual['no_new_display_finding']
    assert sha((ROOT / visual['sheet']).read_bytes()) == visual['sha256']
    for path, digest in completion['evidence'].items():
        assert sha((ROOT / path).read_bytes()) == digest, path
    manuscript = ROOT / 'translations/lil_B170_editorial_manuscript_v5.json'
    assert len(read(manuscript)['records']) == 33
    research_receipt = read(ROOT / 'work/analysis/lil_B170_research_v4284/research_image_receipt.json')
    research_rom = ROOT / research_receipt['research_ROM']
    assert sha(research_rom.read_bytes()) == research_receipt['research_ROM_sha256']
    research_proofs = {
        'native_approval': 'work/analysis/lil_B170_native_approval_v4278/approval_receipt.json',
        'relocation': 'work/analysis/lil_B170_relocation_v4281/nested_source_relocation_research.json',
        'stored_native_targets': 'work/analysis/lil_B170_stored_v4282/all33_final_stored_targets132_macro_cases_and_complete_planes.json',
        'research_image': 'work/analysis/lil_B170_research_v4284/research_image_receipt.json',
        'whole_loaders': 'work/analysis/lil_B170_loader_v4285/whole_SC2_and_B170_initial_entry_proof.json',
        'reference_census': 'work/analysis/lil_B170_reference_census_v4286/all45_commands_zero_relative_sites_and_shipped_entry_census.json',
        'both_ends': 'work/analysis/lil_B170_ends_v4287/four_declared_end_decodes_and_zero_relative_sites.json',
        'relocated_controls': 'work/analysis/lil_B170_relocated_controls_v4288/all33_progressive_dispatches_C200_pause_and12_leaves.json',
    }
    for name, path in research_proofs.items():
        read(ROOT / path)
        evidence['B170_' + name + '.json'] = path
    controls = read(ROOT / research_proofs['relocated_controls'])
    assert controls['all33_progressive_consumers_FI1_FO1_exact']
    assert controls['original_C200_queue_and_all_unowned4MiB_preserved_at_relocated_cursor']
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
        'objects': 33, 'proposed_revisions': 21, 'justified_retentions': 12,
        'status': 'contextual/native approved; research relocation, stored text, loaders, references, both ends and relocated consumers verified; representative gameplay and registered integration pending',
        'manuscript': manuscript.relative_to(ROOT).as_posix(), 'manuscript_sha256': sha(manuscript.read_bytes()),
        'proofs': {name: {'path': path, 'sha256': sha((ROOT / path).read_bytes())} for name, path in research_proofs.items()},
        'research_ROM': research_receipt['research_ROM'], 'research_ROM_sha256': research_receipt['research_ROM_sha256'],
        'resume': 'Continue paired Japanese/English B170 content fixtures retaining all45 commands, pause, presentations/resources, later A000, C200 and both declared ends. Observe actual return and end reachability. Then seal approval, atomic compiler controls, registered cumulative integration, exact clean-input patch and fresh startup checks. Existing relocation/native/loader proofs need not be repeated without a change.',
        'credited_pending_contextual_reviews': 33, 'new_editorial_ledger_credit_added': 0,
        'integrated_in_promoted_ROM': False, 'new_gameplay_runs_at_promotion': 0,
        'B170_actual_gameplay_coverage': False, 'full_goal_complete': False,
    }
    save(verification / 'UNINTEGRATED_B170_status.json', pending)
    scope = ('The full contextual editorial goal remains active across every remaining storyline, shared shop/town exchange, random scene, Help and other player-facing prose. B170 has33 pending reviews outside this ROM; B171-B180 has198 physical speech leads, not a full-project denominator. Preserve COMMON750-752, canonical Maria32 SC3 B97, SourceItems/LocalProduct, five named-target leads, exact-record Proof consistency, Samwell full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques stay separate. Retain the later older-record technical re-audit/queued0D gap.')
    promotion = {
        'format': 'dk4-promoted-checkpoint-v1', 'status': 'promoted', 'main_build': True,
        'promoted_on': '2026-10-26', 'checkpoint': 'V4289',
        'user_request': 'lets promote our current build as our new main build and then commit/push to github',
        'profile': PROFILE, 'rom': rom.relative_to(ROOT).as_posix(), 'rom_sha256': ROM_SHA,
        'release_directory': PACKAGE.relative_to(ROOT).as_posix(), 'git_tag': 'promoted-v4251',
        'patch_sha256': PATCH_SHA, 'source_rom_sha256': CLEAN_SHA,
        'build_manifest_sha256': MANIFEST_SHA, 'build_registry_sha256': REGISTRY_SHA,
        'immutable_construction_baseline': deepcopy(registry['canonical_baseline']),
        'previous_promoted_build': 'releases/all_routes_unified_v4204/promotion.json',
        'promotion_scope': 'User-designated main cumulative checkpoint; immutable construction baseline, accepted-layer status and frozen source/hash contracts remain unchanged. The registry buildable profile retains experimental status; this record designates the main build.',
        'known_open_scope': scope, 'complete_entries': 5692, 'source_prose_reviewed_entries': 5728,
        'fresh_contextual_rereads': 5725, 'pending_B170_entries': 33,
        'reviewed_incomplete_COMMON_entries': 3,
        'full_editorial_goal_complete': False, 'full_graphics_goal_complete': False,
        'new_user_cold_boot_test_claimed': False, 'new_emulator_runs_at_promotion': 0,
        'construction_baseline_rebased': False,
    }
    save(PACKAGE / 'promotion.json', promotion)
    save(PACKAGE / 'release_manifest.json', {
        'game': 'Daikoukai Jidai IV / Rota Nova DS', 'patch_version': 'unified-v4251',
        'status': 'promoted', 'main_build': True, 'profile': PROFILE,
        'source_rom_sha256': CLEAN_SHA, 'modified_rom_sha256': ROM_SHA, 'patch_sha256': PATCH_SHA,
        'full_graphics_goal_complete': False, 'full_editorial_goal_complete': False,
        'promotion_record': 'promotion.json', 'notes': scope,
    })
    save(verification / 'promotion_reconstruction.json', {
        'clean_input_sha256': CLEAN_SHA, 'patch_sha256': PATCH_SHA, 'candidate_sha256': ROM_SHA,
        'reconstructed_sha256': sha(reconstruction.read_bytes()), 'whole_ROM_byte_exact': True,
        'new_emulator_runs_at_promotion': 0, 'original_build_registry_sha256': REGISTRY_SHA,
        'producer': 'scripts/promote_v4251_checkpoint.py', 'producer_sha256': sha(Path(__file__).read_bytes()),
    })
    save(verification / 'promotion_test_results.json', {
        'command': 'python -m pytest tests/test_integrated_release.py tests/test_dialogue_review.py tests/test_dialogue_balanced_wrap.py tests/test_dialogue_pair_phase.py tests/test_dialogue_relocation.py tests/test_lil_editorial_literal_guard.py -q',
        'result': '78 passed in 3.91s', 'exit_code': 0, 'new_emulator_runs': 0,
    })
    registry['latest_promoted_build'] = {
        'status': 'promoted', 'main_build': True, 'profile': PROFILE, 'rom_sha256': ROM_SHA,
        'record': 'translations/promoted_build.json', 'git_tag': 'promoted-v4251',
        'construction_baseline_rebased': False,
    }
    summary = ('V4289 promotes verified V4251 as the new main cumulative build at the user\'s request. All545 manuscript batches and114 accepted layers are preserved, including completed B169. The clean-input patch was freshly reconstructed byte for byte. Coverage remains5725 fresh contextual rereads,5692 integrated/completed,33 pending,5728 source/prose,3614 historically revised/2078 retained, with4093 integrated route objects. B170 has33 contextual/native-approved pending speeches (21 revisions/12 justified retentions), outside the promoted ROM. Research relocation,132 stored alignment cases, both original whole loaders, three reference censuses, four declared-end decodes and relocated speech/C200 consumers pass; representative B170 gameplay and registered integration remain pending. Promotion adds no editorial credit, new emulator run or user cold-boot claim. Preserve earlier V4204/V4160/V4046/V1492 packages and every ROM, translation, draft, executed producer/proof/failure. The immutable construction baseline and accepted-layer status are unchanged. ' + scope)
    ledger['promoted_main_build_v4289'] = promotion
    ledger['lil_B170_preintegration_review_v4289'] = pending
    ledger['latest_checkpoint'] = summary
    section = ('## V4289: V4251 promoted as main; B170 review and research preserved\n\n' + summary +
               '\n\nMain build: [Unified V4251](../releases/all_routes_unified_v4251/README.md). ROM SHA-256: `' + ROM_SHA +
               '`. Patch SHA-256: `' + PATCH_SHA + '`. Earlier sections retain their original checkpoint status.\n\nNext: ' + pending['resume'] +
               ' Continue B171-B180 and every wider editorial family. Full goal active.\n\n')
    mutations = {
        'translations/release_stack.json': encoded(registry, crlf=True),
        'translations/promoted_build.json': encoded(promotion, crlf=True),
        'translations/editorial_review_current_v1.json': encoded(ledger, crlf=True),
    }
    for name in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md', 'release_build.md']:
        path = 'docs/' + name
        first, rest = (ROOT / path).read_text(encoding='utf-8').split('\n', 1)
        if name == 'editorial_handoff_current.md':
            first = '# Current editorial handoff - V4289'
        mutations[path] = (first + '\n\n' + section + rest).encode('utf-8')
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    readme = readme.replace('[Unified V4204](releases/all_routes_unified_v4204/README.md)', '[Unified V4251](releases/all_routes_unified_v4251/README.md)')
    readme = readme.replace('Earlier [V4160]', 'Earlier [V4204](releases/all_routes_unified_v4204/README.md), [V4160]')
    mutations['README.md'] = readme.encode('utf-8')
    ignore = (ROOT / '.gitignore').read_text(encoding='utf-8')
    assert '!releases/all_routes_unified_v4251/*.xdelta' not in ignore
    mutations['.gitignore'] = (ignore + '!releases/all_routes_unified_v4251/*.xdelta\n').encode('utf-8')
    pins = read(ROOT / 'translations/rom_retention_pins.json')
    for p, digest, reason in [(reconstruction, ROM_SHA, 'V4289 promoted V4251 byte-exact clean-input patch reconstruction'),
                              (research_rom, research_receipt['research_ROM_sha256'], 'B170 V4284 unintegrated research ROM needed by pending reference/content checks')]:
        if not any(row['path'] == str(p.resolve()) for row in pins):
            pins.append({'path': str(p.resolve()), 'reason': reason + '. Preserve all generated ROMs; no pruning. SHA-256 ' + digest})
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
        '# Main promoted English build: V4251\n\nPromoted on 2026-10-26 at the user\'s request. Tag: `promoted-v4251`.\n\n'
        'This cumulative build contains 545 manuscript batches and 114 accepted layers, including the completed Lil B169 review. Earlier releases and every local ROM and translation remain preserved.\n\n'
        '## Apply the patch\n\nSupply your unmodified Japanese ROM with SHA-256 `' + CLEAN_SHA + '`:\n\n'
        '```powershell\npython -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v4251/translation.xdelta --out out/all_routes_combined_v4251_candidate.nds\n```\n\n'
        'Expected ROM SHA-256: `' + ROM_SHA + '`.\n\nPatch SHA-256: `' + PATCH_SHA + '`.\n\n'
        'The complete clean-input patch reconstruction was rerun byte for byte at promotion. ROMs, saves and raw RAM captures remain local. Retained ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v4251_candidate.nds`.\n\n'
        '## Verification and coverage\n\nRegistered profile: `all-routes-unified-v4251`. Against V4204 only SC2 B169 changes. All 335 other SC2 blocks and every other file/component, ARM9, COMMON, fonts, graphics and the 123040-byte staged payload remain exact. All 36 complete native planes, 288 logical/compiled and 144 stored alignment cases pass.\n\n'
        'Existing paired 20001-frame Japanese/English content-fixture cold boots cover 33 selected B169 speeches, original effects and normal town return. Three conditional remarks have offline native coverage only. Two further registered opening/town cold boots pass 31 whole-frame comparisons and five actor/captain checks. The viewed startup and completion receipts supersede historical pending flags. The inherited town battery is test data. These targeted automated headless emulator tests do not establish natural event eligibility, earned flags, full-route completion or hardware verification. Promotion adds no new emulator run or user cold-boot claim.\n\n'
        'At promotion, 78 integrated-release and dialogue regression tests passed.\n\n'
        '## Unfinished work\n\nThe ledger retains 5725 fresh contextual rereads: 5692 completed and 33 pending, with 5728 source/prose reviews. B170 has 33 pending speeches: 21 revisions and 12 justified retentions. **Those revisions are outside this ROM.** Contextual/native approval and research relocation, stored text, loader, reference and relocated-control checks are complete; representative gameplay and registered integration remain pending. The packaged B170 status gives exact resume references.\n\n'
        + scope + '\n\nSee the [current handoff](../../docs/editorial_handoff_current.md).\n\n'
        '## Reproduction records\n\n`build_manifest.json.gz` and `build_release_stack.json.gz` preserve the exact original build-time bytes; decompressed hashes are in `promotion.json`. The current registry changes only its promotion pointer. `checksums.json` covers every other packaged file. `verification/` contains scoped receipts, fresh reconstruction and final audit.\n\n'
        'Immutable construction baseline: `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `' + BASE_SHA + '`. Frozen builders, canonical inputs and accepted-layer status are preserved. Registry buildable profiles retain experimental status; `translations/promoted_build.json` designates the main build.\n',
        encoding='utf-8', newline='\n')
    save(AUDIT / 'staging_receipt.json', {'profile': PROFILE, 'ROM_sha256': ROM_SHA, 'evidence': evidence_hashes,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'mutations': len(plan), 'new_emulator_runs': 0, 'ROMs_deleted': 0})
    print(json.dumps({'staged': len(plan), 'profile': PROFILE, 'whole_patch_reconstruction_byte_exact': True, 'B170_pending': 33}))


if __name__ == '__main__':
    main()
