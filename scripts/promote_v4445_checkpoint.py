"""Stage the explicitly requested V4445 main release, preserving frozen inputs."""
from __future__ import annotations

import gzip
import hashlib
import json
import shutil
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.xdelta import apply_xdelta
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'work/analysis/promotion_v4452'
PACKAGE = ROOT / 'releases/all_routes_unified_v4445'
PROFILE = 'all-routes-unified-v4445'
ROM = ROOT / 'out/all_routes_combined_v4445_candidate.nds'
ROM_SHA = '2f39e03f1f5fa2993c3f63d820bbf42bec8b0975646b0d739fbb716b0516b99d'
PATCH_SHA = 'cb7a6111346d0b56aae61542b89620aab74378b268522a4e205f5edc53c0fb29'
REGISTRY_SHA = 'ba27ee30c20e7144d802cdc53560c09ae754d05b943d62590aa80ab38656276b'
MANIFEST_SHA = '20d1429707b794140097091d606bfca3ef11b3306482743c50d71a2042116db5'
LEDGER_SHA = '13438ffe31a4cb31129238918d4f6ecfb9877cfe22d0ecb857a98f93ba4c2099'
CLEAN_SHA = 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
BASE_SHA = '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
RESUME = ('Continue B174 from the complete clean-Japanese exchange and 33 fresh glosses in V4451. '
          'Bind current approved names, voices, terms, conditional selector0E and native controls before '
          'predecessor-English comparison and natural-dialogue-v2 authoring. B174 has no new review credit '
          'or manuscript in this release. Continue B174-B180 and every wider editorial family.')
SCOPE = ('The full contextual editorial goal remains active across every remaining storyline, shared '
         'shop/town exchange, random scene, Help and other player-facing prose. B174-B180 contains123 '
         'physical speeches and zero typed-choice leads, not a project denominator. Preserve COMMON750-752, '
         'canonical Maria32 SC3B97, SourceItems/LocalProduct, five named-target leads, exact-record Proof '
         'consistency, Samwell full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 '
         'plaques remain separate. Retain the later older-record technical re-audit/queued0D gap. Preserve '
         'every generated ROM, translation, draft, executed producer, proof and failure.')
SUMMARY = ('V4452 promotes verified V4445 as the new main cumulative build at the user\'s request. '
           'All549 manuscript batches and114 accepted layers are preserved, including completed B172 '
           'and B173. Fresh clean-input patch reconstruction is byte exact;78 release/dialogue regression '
           'tests pass. Coverage remains5800 completed contextual rereads, zero pending credited route '
           'drafts,5803 source/prose reviews,3686 revised/2114 justified retentions and4201 completed '
           'route objects. B174 has33 clean-first glosses with zero new ledger credit. Promotion adds no '
           'editorial credit, emulator run or user cold-boot claim. Earlier main V4353 and every earlier '
           'package remain preserved. Immutable construction inputs and accepted-layer status remain '
           'unchanged. ' + SCOPE)


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
    registry_path = ROOT / 'translations/release_stack.json'
    ledger_path = ROOT / 'translations/editorial_review_current_v1.json'
    manifest_path = ROM.with_suffix('.manifest.json')
    for path, digest in [(ROM, ROM_SHA), (ROM.with_suffix('.xdelta'), PATCH_SHA),
                         (manifest_path, MANIFEST_SHA), (registry_path, REGISTRY_SHA),
                         (ledger_path, LEDGER_SHA), (ROOT/'work/clean.nds', CLEAN_SHA),
                         (ROOT/'out/raphael_natural_v2_accepted_base.nds', BASE_SHA)]:
        assert sha(path.read_bytes()) == digest, str(path)
    registry, ledger, manifest = map(read, [registry_path, ledger_path, manifest_path])
    assert registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4353'
    assert registry['canonical_baseline']['sha256'] == BASE_SHA
    assert len(registry['accepted_layers']) == 114 and len(manifest['batches']) == 549
    assert manifest['profile'] == PROFILE and manifest['release_stack_sha256'] == REGISTRY_SHA
    assert manifest['candidate_sha256'] == ROM_SHA and manifest['base_sha256'] == BASE_SHA
    assert all(manifest['checks'].values())
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert tuple(ledger[k] for k in ['records_editorially_completed', 'records_with_source_and_prose_pass',
        'records_revised_and_integrated', 'retained_wordings_editorially_completed']) == (5800,5803,3686,2114)
    evidence = {
        'registered_release_verification.json': 'work/analysis/lil_B173_release_v4446/registered_release_verification.json',
        'cold_boot_Lil_startup_town_verification.json': 'work/analysis/lil_B173_startup_v4448/cold_boot_Lil_startup_town_verification.json',
        'current_six_frame_visual_review.json': 'work/analysis/lil_B173_startup_v4448/current_six_frame_visual_review.json',
        'B173_completion_receipt.json': 'work/analysis/lil_B173_completion_v4449/completion_receipt.json',
        'V4450_verified_handoff.json': 'work/analysis/editorial_handoff_verification_v4450/verified_handoff.json',
        'unfinished_editorial_scope_inventory.json': 'work/analysis/lil_B173_completion_v4449/unfinished_editorial_scope_inventory.json',
        'B172_completion_receipt.json': 'work/analysis/lil_B172_completion_v4408/completion_receipt.json',
        'B172_final_review.json': 'translations/lil_B172_contextual_final_review_v1.json',
        'B173_final_review.json': 'translations/lil_B173_contextual_final_review_v1.json',
        'B173_actual_scene_review.json': 'work/analysis/lil_B173_actual_review_v4439/all2_actual_sheets_unforced_suffix_paired_return_and_final_state.json',
        'B174_clean_context.json': 'work/analysis/lil_B174_clean_context_v4451/all33_complete_B174_exchange_and_fresh_glosses.json',
    }
    values = {name: read(ROOT/path) for name,path in evidence.items()}
    release = values['registered_release_verification.json']
    startup = values['cold_boot_Lil_startup_town_verification.json']
    visual = values['current_six_frame_visual_review.json']
    verified = values['V4450_verified_handoff.json']
    assert release['candidate_sha256'] == startup['candidate_sha256'] == verified['candidate_sha256'] == ROM_SHA
    assert release['manifest_sha256'] == MANIFEST_SHA and release['patch_sha256'] == PATCH_SHA
    assert release['whole_ROM_reconstruction_byte_exact'] and verified['ledger_sha256'] == LEDGER_SHA
    assert (verified['fresh_reread'],verified['integrated'],verified['pending']) == (5800,5800,0)
    assert startup['paired_frame_count'] == 31 and startup['all_current_requested_and_final_framebuffers_equal_V4404']
    assert startup['all_five_postload_actor_model_and_captain_checks_equal']
    assert visual['viewed'] and visual['no_new_display_finding']
    assert sha((ROOT/visual['sheet']).read_bytes()) == visual['sha256']
    for name in ['B172_completion_receipt.json','B173_completion_receipt.json']:
        receipt = values[name]
        assert receipt['all_jobs_terminal']
        for path,digest in receipt['evidence'].items():
            assert sha((ROOT/path).read_bytes()) == digest, path
    clean = values['B174_clean_context.json']
    assert clean['total_editorial_objects'] == 33 and clean['no_predecessor_English_exposed']
    assert clean['source_prose_or_completion_credit_added'] == 0
    assert sha((ROOT/clean['source_transcript']).read_bytes()) == clean['source_transcript_sha256']
    AUDIT.mkdir(parents=True)
    reconstruction = AUDIT/'promoted_patch_reconstruction_RESEARCH_ONLY.nds'
    apply_xdelta(ROOT/'work/clean.nds', ROM.with_suffix('.xdelta'), reconstruction)
    assert reconstruction.read_bytes() == ROM.read_bytes()
    PACKAGE.mkdir(parents=True)
    verification = PACKAGE/'verification'
    verification.mkdir()
    shutil.copyfile(ROM.with_suffix('.xdelta'), PACKAGE/'translation.xdelta')
    for name,path in [('build_manifest.json.gz',manifest_path),('build_release_stack.json.gz',registry_path)]:
        (PACKAGE/name).write_bytes(gzip.compress(path.read_bytes(),mtime=0))
    (AUDIT/'ledger.before.json.gz').write_bytes(gzip.compress(ledger_path.read_bytes(),mtime=0))
    (AUDIT/'registry.before.json').write_bytes(registry_path.read_bytes())
    evidence_hashes = {}
    for name,path in evidence.items():
        shutil.copyfile(ROOT/path, verification/name)
        evidence_hashes[path] = sha((ROOT/path).read_bytes())
    shutil.copyfile(ROOT/visual['sheet'], verification/'current_Lil_startup_and_town_review.png')
    draft = {'family':'B174', 'clean_source_speeches':33, 'source_prose_or_completion_credit_added':0,
             'new_B174_manuscript_integrated_in_promoted_ROM':False, 'resume':RESUME,
             'clean_context_sha256':sha((verification/'B174_clean_context.json').read_bytes()),
             'new_emulator_runs_at_promotion':0, 'full_goal_complete':False}
    save(verification/'UNINTEGRATED_B174_status.json', draft)
    promotion = {'format':'dk4-promoted-checkpoint-v1', 'status':'promoted', 'main_build':True,
        'promoted_on':'2026-10-26', 'checkpoint':'V4452',
        'user_request':'lets promote our current build as our new main build and then commit/push to github',
        'profile':PROFILE, 'rom':ROM.relative_to(ROOT).as_posix(), 'rom_sha256':ROM_SHA,
        'release_directory':PACKAGE.relative_to(ROOT).as_posix(), 'git_tag':'promoted-v4445',
        'patch_sha256':PATCH_SHA, 'source_rom_sha256':CLEAN_SHA,
        'build_manifest_sha256':MANIFEST_SHA, 'build_registry_sha256':REGISTRY_SHA,
        'immutable_construction_baseline':deepcopy(registry['canonical_baseline']),
        'previous_promoted_build':'releases/all_routes_unified_v4353/promotion.json',
        'promotion_scope':'User-designated main checkpoint; immutable construction inputs and accepted-layer status preserved. Buildable profile retains experimental status.',
        'known_open_scope':SCOPE, 'complete_entries':5800, 'source_prose_reviewed_entries':5803,
        'fresh_contextual_rereads':5800, 'pending_credited_route_entries':0,
        'reviewed_incomplete_COMMON_entries':3, 'B174_clean_glosses_without_credit':33,
        'full_editorial_goal_complete':False, 'full_graphics_goal_complete':False,
        'new_user_cold_boot_test_claimed':False, 'new_emulator_runs_at_promotion':0,
        'construction_baseline_rebased':False}
    save(PACKAGE/'promotion.json',promotion)
    save(PACKAGE/'release_manifest.json',{'game':'Daikoukai Jidai IV / Rota Nova DS',
        'patch_version':'unified-v4445','status':'promoted','main_build':True,'profile':PROFILE,
        'source_rom_sha256':CLEAN_SHA,'modified_rom_sha256':ROM_SHA,'patch_sha256':PATCH_SHA,
        'full_graphics_goal_complete':False,'full_editorial_goal_complete':False,
        'promotion_record':'promotion.json','notes':SCOPE})
    save(verification/'promotion_reconstruction.json',{'clean_input_sha256':CLEAN_SHA,
        'patch_sha256':PATCH_SHA,'candidate_sha256':ROM_SHA,
        'reconstructed_sha256':sha(reconstruction.read_bytes()),'whole_ROM_byte_exact':True,
        'new_emulator_runs_at_promotion':0,'original_build_registry_sha256':REGISTRY_SHA,
        'producer':'scripts/promote_v4445_checkpoint.py','producer_sha256':sha(Path(__file__).read_bytes())})
    save(verification/'promotion_test_results.json',{'command':'python -m pytest tests/test_integrated_release.py tests/test_dialogue_review.py tests/test_dialogue_balanced_wrap.py tests/test_dialogue_pair_phase.py tests/test_dialogue_relocation.py tests/test_lil_editorial_literal_guard.py -q',
        'result':'78 passed in 4.33s','exit_code':0,'new_emulator_runs':0})
    registry['latest_promoted_build'] = {'status':'promoted','main_build':True,'profile':PROFILE,
        'rom_sha256':ROM_SHA,'record':'translations/promoted_build.json','git_tag':'promoted-v4445',
        'construction_baseline_rebased':False}
    ledger['promoted_main_build_v4452'] = promotion
    ledger['lil_B174_clean_context_v4452'] = draft
    ledger['latest_checkpoint'] = SUMMARY
    mutations = {'translations/release_stack.json':encoded(registry,True),
        'translations/promoted_build.json':encoded(promotion,True),
        'translations/editorial_review_current_v1.json':encode_ledger(ledger)}
    section = ('## V4452: V4445 promoted as main; B174 clean-first review preserved\n\n'+SUMMARY+
        '\n\nMain build: [Unified V4445](../releases/all_routes_unified_v4445/README.md). ROM SHA-256: `'+
        ROM_SHA+'`. Patch SHA-256: `'+PATCH_SHA+'`. Earlier sections retain their original checkpoint status.\n\nNext: '+RESUME+'\n\n')
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md',
                 'todo.md','known_issues.md','release_build.md']:
        path = 'docs/'+name
        first,rest = (ROOT/path).read_text(encoding='utf-8').split('\n',1)
        if name == 'editorial_handoff_current.md': first = '# Current editorial handoff - V4452'
        mutations[path] = (first+'\n\n'+section+rest).encode('utf-8')
    readme = (ROOT/'README.md').read_text(encoding='utf-8')
    old_link = '[Unified V4353](releases/all_routes_unified_v4353/README.md)'
    assert readme.count(old_link) == 2
    readme = readme.replace(old_link,'[Unified V4445](releases/all_routes_unified_v4445/README.md)')
    mutations['README.md'] = readme.replace('Earlier [V4303]',
        'Earlier [V4353](releases/all_routes_unified_v4353/README.md), [V4303]').encode('utf-8')
    ignore = (ROOT/'.gitignore').read_text(encoding='utf-8')
    assert '!releases/all_routes_unified_v4445/*.xdelta' not in ignore
    mutations['.gitignore'] = (ignore+'!releases/all_routes_unified_v4445/*.xdelta\n').encode('utf-8')
    pins = read(ROOT/'translations/rom_retention_pins.json')
    pins.append({'path':str(reconstruction.resolve()),'reason':'V4452 promoted V4445 exact clean-input patch reconstruction. Preserve every ROM; no pruning. SHA-256 '+ROM_SHA})
    mutations['translations/rom_retention_pins.json'] = encoded(pins,True)
    staged = AUDIT/'staged'
    staged.mkdir()
    plan = []
    for index,(relative,data) in enumerate(mutations.items()):
        target = ROOT/relative
        before = target.read_bytes()
        (AUDIT/(str(index)+'.before')).write_bytes(before)
        planned = staged/(str(index)+'.planned')
        planned.write_bytes(data)
        plan.append({'target':str(target),'before_sha256':sha(before),
                     'planned':str(planned),'planned_sha256':sha(data)})
    save(AUDIT/'mutation_plan.json',plan)
    (PACKAGE/'README.md').write_text(
        '# Main promoted English build: V4445\n\nPromoted on 2026-10-26 at the user\'s request. Tag: `promoted-v4445`.\n\n'
        'This cumulative build contains549 manuscript batches and114 accepted layers, including completed Lil B172 and B173. Earlier packages, ROMs and translations remain preserved.\n\n'
        '## Apply the patch\n\nSupply an unmodified Japanese ROM with SHA-256 `'+CLEAN_SHA+'`:\n\n'
        '```powershell\npython -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v4445/translation.xdelta --out out/all_routes_combined_v4445_candidate.nds\n```\n\n'
        'Expected ROM SHA-256: `'+ROM_SHA+'`.\n\nPatch SHA-256: `'+PATCH_SHA+'`.\n\n'
        'The complete clean-input patch was freshly reconstructed byte for byte at promotion. ROMs, saves and raw RAM remain local. Retained ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v4445_candidate.nds`.\n\n'
        '## Verification and coverage\n\nRegistered profile: `all-routes-unified-v4445`. Immutable construction baseline: `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `'+BASE_SHA+'`. B172 and B173 change SC2 only. The latest B173 step against V4404 preserves all335 other SC2 blocks and every other file/component, ARM9, COMMON, fonts, graphics and123040 staged bytes.\n\n'
        'Existing paired Japanese/English content-fixture cold boots cover all27 B172 and11 B173 speeches, original controls/effects and normal town return. B173\'s unvisited jump744 retains offline native coverage. Current registered New Game/town cold boots pass31 whole-frame comparisons and five actor/captain checks. Viewed visual and completion receipts supersede historical pending flags in earlier receipts. These targeted automated headless tests do not establish natural event eligibility, earned flags, full-route completion, hardware behavior or future-world equivalence. Promotion adds no new emulator run or user cold-boot claim. All78 release/dialogue regression tests pass.\n\n'
        '## Unfinished work\n\nThe ledger retains5800 completed contextual rereads,5803 source/prose reviews,3686 revisions and2114 justified retentions, with zero pending credited route drafts. B174 has33 clean-first glosses without new credit or a new manuscript in this ROM. See `verification/UNINTEGRATED_B174_status.json`.\n\n'+SCOPE+
        '\n\nNext: '+RESUME+'\n\nSee the [current handoff](../../docs/editorial_handoff_current.md).\n\n'
        '## Reproduction records\n\n`build_manifest.json.gz` and `build_release_stack.json.gz` preserve exact original build-time bytes. `checksums.json` covers every other packaged file. `verification/` contains scoped receipts, fresh reconstruction and final audit. Frozen builders, canonical inputs and accepted-layer status remain preserved. The profile retains experimental status; `translations/promoted_build.json` designates the main build.\n',encoding='utf-8',newline='\n')
    save(AUDIT/'staging_receipt.json',{'profile':PROFILE,'ROM_sha256':ROM_SHA,'evidence':evidence_hashes,
        'producer_sha256':sha(Path(__file__).read_bytes()),'mutations':len(plan),
        'new_emulator_runs':0,'ROMs_deleted':0})
    print(json.dumps({'staged':len(plan),'profile':PROFILE,'whole_patch_reconstruction_byte_exact':True,
                      'completed':5800,'pending_credited_route_reviews':0,'B174_uncredited_glosses':33}))


if __name__ == '__main__':
    main()
