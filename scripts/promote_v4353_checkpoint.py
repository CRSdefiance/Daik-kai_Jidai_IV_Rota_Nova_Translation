"""Stage the user-authorized V4353 main designation without rebasing inputs."""
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
AUDIT = ROOT / 'work/analysis/promotion_v4392'
PACKAGE = ROOT / 'releases/all_routes_unified_v4353'
PROFILE = 'all-routes-unified-v4353'
ROM_SHA = '964c2da7273773c2db63b53eaf1136981d212c4e6282aee303ad101cc508de4e'
PATCH_SHA = '96d1fd20e085519c65b75dfd88d57ced2b4a6b1d21503ed385173833dd83528b'
REGISTRY_SHA = '58cbf2328b1816089e44fb0b789220dd4e97fb60ead82a6946b56b48fa2013bd'
MANIFEST_SHA = 'c6a3741bb25685bc3f11fda5f384129a2592fc74b6ec00220e8b8c39dbc82bdf'
LEDGER_SHA = 'af09ac4600d252f7c0d757f89c6e3f55dd74cdc1fc75690b64cf8bb1be91cbc6'
CLEAN_SHA = 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
BASE_SHA = '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
RESUME = ('Audit the two terminal B172 Japanese/English content runs V4390 against all38 source commands plus nine original initialization commands. Do not restart them. Review all27 speeches, portraits/names, departure, C200 before later A000 raw00a0ffff010cc960,6240,single end and normal return. Existing contextual/native,relocation,stored,loader and control proofs remain complete. Seal representative references,then atomic compiler negatives,registered cumulative integration,exact patch and fresh startup checks. B172 remains outside the main ROM. Continue B173-B180 and every wider editorial family.')
SCOPE = ('The full contextual editorial goal remains active across every remaining storyline,shared shop/town exchange,random scene,Help and other player-facing prose. B172 has27 pending reviews;B173-B180 has134 physical speech leads,not a project denominator. Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques remain separate. Retain the later older-record technical re-audit/queued0D gap. Preserve every generated ROM,translation,draft,executed producer,proof and failure.')
SUMMARY = ("V4392 promotes verified V4353 as the new main cumulative build at the user's request. All547 manuscript batches and114 accepted layers are preserved,including completed B171. Fresh clean-input patch reconstruction is byte exact;78 integrated-release/dialogue regression tests pass. Coverage remains5789 fresh contextual rereads,5762 completed,27 pending,5792 source/prose,3659 historically revised/2103 retained and4163 completed route objects. B172's19 revisions/eight justified retentions remain outside this ROM. Promotion adds no editorial credit or emulator run and makes no new user cold-boot claim. Earlier main V4303 and every earlier package remain preserved. The immutable construction baseline and accepted-layer status remain unchanged. " + SCOPE)


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
    rom = ROOT / 'out/all_routes_combined_v4353_candidate.nds'
    patch, manifest = rom.with_suffix('.xdelta'), rom.with_suffix('.manifest.json')
    registry_path = ROOT / 'translations/release_stack.json'
    ledger_path = ROOT / 'translations/editorial_review_current_v1.json'
    for path, digest in [(rom, ROM_SHA), (patch, PATCH_SHA), (manifest, MANIFEST_SHA),
                         (registry_path, REGISTRY_SHA), (ledger_path, LEDGER_SHA),
                         (ROOT / 'work/clean.nds', CLEAN_SHA),
                         (ROOT / 'out/raphael_natural_v2_accepted_base.nds', BASE_SHA)]:
        assert sha(path.read_bytes()) == digest, str(path)
    build, registry, ledger = map(read, [manifest, registry_path, ledger_path])
    assert build['profile'] == PROFILE and build['release_stack_sha256'] == REGISTRY_SHA
    assert build['candidate_sha256'] == ROM_SHA and build['base_sha256'] == BASE_SHA
    assert len(build['batches']) == 547 and len(registry['accepted_layers']) == 114
    assert all(build['checks'].values()) and registry['canonical_baseline']['sha256'] == BASE_SHA
    assert registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4303'
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass',
        'records_revised_and_integrated','retained_wordings_editorially_completed']) == (5762,5792,3659,2103)
    evidence = {
        'registered_release_verification.json': 'work/analysis/lil_B171_release_v4354/registered_release_verification.json',
        'cold_boot_Lil_startup_town_verification.json': 'work/analysis/lil_B171_startup_v4356/cold_boot_Lil_startup_town_verification.json',
        'current_six_frame_visual_review.json': 'work/analysis/lil_B171_startup_v4356/current_six_frame_visual_review.json',
        'B171_completion_receipt.json': 'work/analysis/lil_B171_completion_v4357/completion_receipt.json',
        'B172_verified_handoff.json': 'work/analysis/editorial_handoff_verification_v4380/verified_handoff.json',
        'B172_native_approval.json': 'work/analysis/lil_B172_native_approval_v4378/approval_receipt.json',
        'B172_checkpoint_receipt.json': 'work/analysis/lil_B172_checkpoint_v4379/checkpoint_receipt.json',
        'unfinished_editorial_scope_inventory.json': 'work/analysis/lil_B172_checkpoint_v4379/unfinished_editorial_scope_inventory.json',
        'B172_Japanese_content_terminal.json': 'work/analysis/lil_B172_display_run_v4390_clean_Japanese/terminal.json',
        'B172_English_content_terminal.json': 'work/analysis/lil_B172_display_run_v4390_reviewed_English/terminal.json',
    }
    release,startup,visual,completion,verified,native,checkpoint,scope,jp,en = [read(ROOT/p) for p in evidence.values()]
    assert release['candidate_sha256'] == startup['candidate_sha256'] == verified['candidate_sha256'] == ROM_SHA
    assert release['manifest_sha256'] == MANIFEST_SHA and release['patch_sha256'] == PATCH_SHA
    assert release['whole_ROM_reconstruction_byte_exact'] and verified['ledger_sha256'] == LEDGER_SHA
    assert (verified['fresh_reread'],verified['integrated'],verified['pending']) == (5789,5762,27)
    assert startup['paired_frame_count'] == 31 and startup['all_current_requested_and_final_framebuffers_equal_V4303']
    assert startup['all_five_postload_actor_model_and_captain_checks_equal']
    assert visual['viewed'] and visual['no_new_display_finding']
    assert sha((ROOT/visual['sheet']).read_bytes()) == visual['sha256']
    for receipt in [completion,checkpoint]:
        for path,digest in receipt['evidence'].items():
            assert sha((ROOT/path).read_bytes()) == digest, path
    assert (native['revised'],native['retained'],native['progressive_planes']) == (19,8,27)
    assert jp['terminal'] and en['terminal']
    manuscript = ROOT/'translations/lil_B172_editorial_manuscript_v3.json'
    assert len(read(manuscript)['records']) == 27
    AUDIT.mkdir(parents=True)
    reconstruction = AUDIT/'promoted_patch_reconstruction_RESEARCH_ONLY.nds'
    apply_xdelta(ROOT/'work/clean.nds',patch,reconstruction)
    assert reconstruction.read_bytes() == rom.read_bytes()
    PACKAGE.mkdir(parents=True)
    verification = PACKAGE/'verification'
    verification.mkdir()
    shutil.copyfile(patch,PACKAGE/'translation.xdelta')
    for target,path in [('build_manifest.json.gz',manifest),('build_release_stack.json.gz',registry_path)]:
        (PACKAGE/target).write_bytes(gzip.compress(path.read_bytes(),mtime=0))
    (AUDIT/'ledger.before.json.gz').write_bytes(gzip.compress(ledger_path.read_bytes(),mtime=0))
    (AUDIT/'registry.before.json').write_bytes(registry_path.read_bytes())
    evidence_hashes = {}
    for name,source in evidence.items():
        shutil.copyfile(ROOT/source,verification/name)
        evidence_hashes[source] = sha((ROOT/source).read_bytes())
    shutil.copyfile(ROOT/visual['sheet'],verification/'current_Lil_startup_and_town_review.png')
    pending = {'objects':27,'proposed_revisions':19,'justified_retentions':8,
        'status':'contextual/native approved; relocation/stored/loaders/controls pass; paired content runs terminal, actual audit and reference approval pending; registered integration pending',
        'manuscript':manuscript.relative_to(ROOT).as_posix(),'manuscript_sha256':sha(manuscript.read_bytes()),
        'integrated_in_promoted_ROM':False,'new_editorial_ledger_credit_added':0,
        'B172_actual_gameplay_coverage_approved':False,'content_runs_terminal':True,
        'new_gameplay_runs_at_promotion':0,'resume':RESUME,'full_goal_complete':False}
    save(verification/'UNINTEGRATED_B172_status.json',pending)
    promotion = {'format':'dk4-promoted-checkpoint-v1','status':'promoted','main_build':True,
        'promoted_on':'2026-10-26','checkpoint':'V4392',
        'user_request':'lets promote our current build as our new main build and then commit/push to github',
        'profile':PROFILE,'rom':rom.relative_to(ROOT).as_posix(),'rom_sha256':ROM_SHA,
        'release_directory':PACKAGE.relative_to(ROOT).as_posix(),'git_tag':'promoted-v4353',
        'patch_sha256':PATCH_SHA,'source_rom_sha256':CLEAN_SHA,'build_manifest_sha256':MANIFEST_SHA,
        'build_registry_sha256':REGISTRY_SHA,'immutable_construction_baseline':deepcopy(registry['canonical_baseline']),
        'previous_promoted_build':'releases/all_routes_unified_v4303/promotion.json',
        'promotion_scope':'User-designated main cumulative checkpoint; immutable construction baseline, accepted-layer status and frozen source/hash contracts remain unchanged. Buildable profile retains experimental status; this record designates the main build.',
        'known_open_scope':SCOPE,'complete_entries':5762,'source_prose_reviewed_entries':5792,
        'fresh_contextual_rereads':5789,'pending_B172_entries':27,'reviewed_incomplete_COMMON_entries':3,
        'full_editorial_goal_complete':False,'full_graphics_goal_complete':False,
        'new_user_cold_boot_test_claimed':False,'new_emulator_runs_at_promotion':0,'construction_baseline_rebased':False}
    save(PACKAGE/'promotion.json',promotion)
    save(PACKAGE/'release_manifest.json',{'game':'Daikoukai Jidai IV / Rota Nova DS','patch_version':'unified-v4353',
        'status':'promoted','main_build':True,'profile':PROFILE,'source_rom_sha256':CLEAN_SHA,
        'modified_rom_sha256':ROM_SHA,'patch_sha256':PATCH_SHA,'full_graphics_goal_complete':False,
        'full_editorial_goal_complete':False,'promotion_record':'promotion.json','notes':SCOPE})
    save(verification/'promotion_reconstruction.json',{'clean_input_sha256':CLEAN_SHA,'patch_sha256':PATCH_SHA,
        'candidate_sha256':ROM_SHA,'reconstructed_sha256':sha(reconstruction.read_bytes()),'whole_ROM_byte_exact':True,
        'new_emulator_runs_at_promotion':0,'original_build_registry_sha256':REGISTRY_SHA,
        'producer':'scripts/promote_v4353_checkpoint.py','producer_sha256':sha(Path(__file__).read_bytes())})
    save(verification/'promotion_test_results.json',{'command':'python -m pytest tests/test_integrated_release.py tests/test_dialogue_review.py tests/test_dialogue_balanced_wrap.py tests/test_dialogue_pair_phase.py tests/test_dialogue_relocation.py tests/test_lil_editorial_literal_guard.py -q',
        'result':'78 passed in 3.81s','exit_code':0,'new_emulator_runs':0})
    registry['latest_promoted_build'] = {'status':'promoted','main_build':True,'profile':PROFILE,'rom_sha256':ROM_SHA,
        'record':'translations/promoted_build.json','git_tag':'promoted-v4353','construction_baseline_rebased':False}
    ledger['promoted_main_build_v4392'] = promotion
    ledger['lil_B172_preintegration_review_v4392'] = pending
    ledger['latest_checkpoint'] = SUMMARY
    section = ('## V4392: V4353 promoted as main; B172 research preserved\n\n'+SUMMARY+
        '\n\nMain build: [Unified V4353](../releases/all_routes_unified_v4353/README.md). ROM SHA-256: `'+ROM_SHA+
        '`. Patch SHA-256: `'+PATCH_SHA+'`. Earlier sections retain their original checkpoint status.\n\nNext: '+RESUME+'\n\n')
    mutations = {'translations/release_stack.json':encoded(registry,True),
        'translations/promoted_build.json':encoded(promotion,True),
        'translations/editorial_review_current_v1.json':encode_ledger(ledger)}
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md','release_build.md']:
        path = 'docs/'+name
        first,rest = (ROOT/path).read_text(encoding='utf-8').split('\n',1)
        if name == 'editorial_handoff_current.md': first = '# Current editorial handoff - V4392'
        mutations[path] = (first+'\n\n'+section+rest).encode('utf-8')
    readme = (ROOT/'README.md').read_text(encoding='utf-8')
    assert readme.count('[Unified V4303](releases/all_routes_unified_v4303/README.md)') == 2
    readme = readme.replace('[Unified V4303](releases/all_routes_unified_v4303/README.md)','[Unified V4353](releases/all_routes_unified_v4353/README.md)')
    mutations['README.md'] = readme.replace('Earlier [V4251]','Earlier [V4303](releases/all_routes_unified_v4303/README.md), [V4251]').encode('utf-8')
    ignore = (ROOT/'.gitignore').read_text(encoding='utf-8')
    assert '!releases/all_routes_unified_v4353/*.xdelta' not in ignore
    mutations['.gitignore'] = (ignore+'!releases/all_routes_unified_v4353/*.xdelta\n').encode('utf-8')
    pins = read(ROOT/'translations/rom_retention_pins.json')
    pins.append({'path':str(reconstruction.resolve()),'reason':'V4392 promoted V4353 exact clean-input patch reconstruction. Preserve every ROM; no pruning. SHA-256 '+ROM_SHA})
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
        plan.append({'target':str(target),'before_sha256':sha(before),'planned':str(planned),'planned_sha256':sha(data)})
    save(AUDIT/'mutation_plan.json',plan)
    (PACKAGE/'README.md').write_text(
        '# Main promoted English build: V4353\n\nPromoted on 2026-10-26 at the user\'s request. Tag: `promoted-v4353`.\n\n'
        'This cumulative build contains547 manuscript batches and114 accepted layers,including completed Lil B171. Earlier packages and every ROM and translation remain preserved.\n\n'
        '## Apply the patch\n\nSupply your unmodified Japanese ROM with SHA-256 `'+CLEAN_SHA+'`:\n\n'
        '```powershell\npython -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v4353/translation.xdelta --out out/all_routes_combined_v4353_candidate.nds\n```\n\n'
        'Expected ROM SHA-256: `'+ROM_SHA+'`.\n\nPatch SHA-256: `'+PATCH_SHA+'`.\n\n'
        'The complete clean-input patch was freshly reconstructed byte for byte at promotion. ROMs,saves and raw RAM remain local. Retained ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v4353_candidate.nds`.\n\n'
        '## Verification and coverage\n\nRegistered profile: `all-routes-unified-v4353`. Against V4303 only SC2 B171 changes. All335 other SC2 blocks and every other file/component,ARM9,COMMON,fonts,graphics and123040 staged bytes remain exact.\n\n'
        'Existing paired Japanese/English content-fixture cold boots cover all37 B171 speeches and original presentation/effect commands,first-end reachability and normal town return. The second end has offline decoder coverage. Later SeaView differences and focused repeat/state evidence remain documented without an equal-world claim. Registered New Game/town cold boots pass31 whole-frame comparisons andfive actor/captain checks. Viewed startup and completion receipts supersede historical pending flags. These targeted automated headless tests do not establish natural event eligibility,earned flags,full-route completion or hardware verification. Promotion adds no new emulator run or user cold-boot claim. All78 integrated-release/dialogue regression tests pass.\n\n'
        '## Unfinished work\n\nThe ledger retains5789 fresh contextual rereads:5762 completed and27 pending,with5792 source/prose reviews. B172 has19 revisions/eight justified retentions. **Those revisions are outside this ROM.** Its paired content runs are terminal;actual audit,reference approval and registered integration remain pending. See `verification/UNINTEGRATED_B172_status.json`.\n\n'+SCOPE+
        '\n\nSee the [current handoff](../../docs/editorial_handoff_current.md).\n\n'
        '## Reproduction records\n\n`build_manifest.json.gz` and `build_release_stack.json.gz` preserve exact original build-time bytes. `checksums.json` covers every other packaged file. `verification/` contains scoped receipts,fresh reconstruction and final audit. Immutable construction baseline: `out/raphael_natural_v2_accepted_base.nds`,SHA-256 `'+BASE_SHA+'`. Frozen builders,canonical inputs and accepted-layer status remain preserved. The profile retains experimental status;`translations/promoted_build.json` designates the main build.\n',encoding='utf-8',newline='\n')
    save(AUDIT/'staging_receipt.json',{'profile':PROFILE,'ROM_sha256':ROM_SHA,'evidence':evidence_hashes,
        'producer_sha256':sha(Path(__file__).read_bytes()),'mutations':len(plan),'new_emulator_runs':0,'ROMs_deleted':0})
    print(json.dumps({'staged':len(plan),'profile':PROFILE,'whole_patch_reconstruction_byte_exact':True,'B172_pending':27}))


if __name__ == '__main__':
    main()
