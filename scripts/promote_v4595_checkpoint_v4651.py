"""Stage, validate, apply and audit the user-requested V4595 main checkpoint."""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil

from dk4tool.patch.xdelta import apply_xdelta
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.lil_B177_reference_checkpoint_text_v4641 import NEXT

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'work/analysis/promotion_v4651'
PACKAGE = ROOT / 'releases/all_routes_unified_v4595'
ROM = ROOT / 'out/all_routes_combined_v4595_candidate.nds'
PROFILE = 'all-routes-unified-v4595'
ROM_SHA = '8119f693e683ffd6ee94ed5288c5477b1dc686a5ee1e32f4ccf7ef1e7ca1501f'
PATCH_SHA = '15397f540ee6ad7143823bbb05a015965b733ce63b2ae74ae153465531a9d17c'
MANIFEST_SHA = '1434db9b2592b8ec7ced0a9874c948a11a66043067ece2cce3ff1760fcb27c45'
REGISTRY_SHA = '0357c6d195d0973e9e6ec640f055bc52b09765b29fb017c63d1365098085a3a2'
CLEAN_SHA = 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
BASE_SHA = '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
SUMMARY = (
    'V4651 promotes verified V4595 as the user-designated main cumulative build, including '
    'completed B176 (five revisions/five individually justified retentions). All552 manuscript '
    'batches and114 accepted layers remain present. A fresh clean-input patch reconstruction '
    'is byte exact;78 release/dialogue regression tests pass. Coverage remains5885 fresh '
    'contextual rereads:5875 integrated/completed and ten pending;source/prose5888, historical '
    'completed decisions3733 revised/2142 retained,route reviewed/completed4286/4276. '
    'B177 manuscript v6 and its sealed native/reference/actual evidence are preserved outside '
    'the promoted ROM, pending atomic compiler,registered cumulative integration,exact patch '
    'and current startup checks. Promotion adds no editorial credit or emulator run. '
    'Earlier main V4541 and every earlier package,ROM,translation,draft,executed producer,proof '
    'and failure remain preserved. Immutable construction inputs and accepted-layer status '
    'stay unchanged. The full editorial goal remains active across every storyline,shared '
    'shop/town dialogue,random scene,Help and remaining player-facing prose. B178-B180 has38 '
    'physical speeches,not a project denominator. Preserve COMMON750-752,canonical Maria32 '
    'SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency, '
    'Samwell full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 '
    'plaques remain separate;retain the later older-record technical re-audit/queued0D gap.')
EVIDENCE = {
    'registered_release_verification.json': 'work/analysis/lil_B176_release_v4596/registered_release_verification.json',
    'cold_boot_Lil_startup_town_verification.json': 'work/analysis/lil_B176_startup_v4598/cold_boot_Lil_startup_town_verification.json',
    'current_six_frame_visual_review.json': 'work/analysis/lil_B176_startup_v4598/current_six_frame_visual_review.json',
    'B176_completion_receipt.json': 'work/analysis/lil_B176_completion_v4599/completion_receipt.json',
    'V4600_verified_handoff.json': 'work/analysis/editorial_handoff_verification_v4600/verified_handoff.json',
    'B176_final_review.json': 'translations/lil_B176_contextual_final_review_v1.json',
    'B177_pending_manuscript_v6.json': 'translations/lil_B177_editorial_manuscript_v6.json',
    'B177_reference_approval.json': 'work/analysis/lil_B177_reference_approval_v4640/approval_receipt.json',
    'B177_actual_view.json': 'work/analysis/lil_B177_actual_review_v4639/all2_actual_sheets10_planes_fullscreens_return_and_final_state.json',
    'B177_reference_checkpoint.json': 'work/analysis/lil_B177_reference_checkpoint_v4641/checkpoint_receipt.json',
    'unfinished_editorial_scope_inventory.json': 'work/analysis/lil_B177_reference_checkpoint_v4641/unfinished_editorial_scope_inventory.json',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def encoded(value, crlf=False):
    data = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return data.replace(b'\n', b'\r\n') if crlf else data


def save(path, value):
    Path(path).write_bytes(encoded(value))


def same_except(before, after, allowed):
    assert {k:v for k,v in before.items() if k not in allowed} == {k:v for k,v in after.items() if k not in allowed}


def validate_values(before, staged, oldregistry, registry, oldpins, pins):
    same_except(before, staged, {'latest_checkpoint', 'promoted_main_build_v4651'})
    assert 'promoted_main_build_v4651' not in before
    assert staged['goal_status'] == 'active' and not staged['full_goal_complete']
    assert tuple(staged[k] for k in ['records_editorially_completed', 'records_with_source_and_prose_pass',
        'records_revised_and_integrated', 'retained_wordings_editorially_completed']) == (5875,5888,3733,2142)
    fresh = staged['contextual_story_natural_dialogue_pass_v1871']
    assert tuple(fresh[k] for k in ['fresh_pass_records_explicitly_reread', 'fresh_pass_records_integrated',
        'fresh_pass_records_pending_native_actual_release']) == (5885,5875,10)
    assert len(fresh['pending_contextual_families']) == 1
    assert fresh['pending_contextual_families'][0]['manuscript'] == 'translations/lil_B177_editorial_manuscript_v6.json'
    same_except(oldregistry, registry, {'latest_promoted_build'})
    assert registry['latest_promoted_build']['profile'] == PROFILE
    assert registry['profiles'][PROFILE]['status'] == 'experimental' and len(registry['accepted_layers']) == 114
    assert pins[:-1] == oldpins
    assert Path(pins[-1]['path']).read_bytes() == ROM.read_bytes()
    assert len(encode_ledger(staged)) < 100*1024*1024


def stage():
    assert Path.cwd() == ROOT and not AUDIT.exists() and not PACKAGE.exists()
    for path, digest in [(ROM,ROM_SHA),(ROM.with_suffix('.xdelta'),PATCH_SHA),
        (ROM.with_suffix('.manifest.json'),MANIFEST_SHA),(ROOT/'translations/release_stack.json',REGISTRY_SHA),
        (ROOT/'work/clean.nds',CLEAN_SHA),(ROOT/'out/raphael_natural_v2_accepted_base.nds',BASE_SHA)]:
        assert sha(path.read_bytes()) == digest, str(path)
    values = {name:read(ROOT/path) for name,path in EVIDENCE.items()}
    checked = values['V4600_verified_handoff.json']
    assert checked['candidate_sha256'] == ROM_SHA and checked['regression_tests_passed'] == 78 and checked['all_jobs_terminal']
    assert values['registered_release_verification.json']['whole_ROM_reconstruction_byte_exact']
    startup = values['cold_boot_Lil_startup_town_verification.json']
    assert startup['paired_frame_count'] == 31 and startup['all_current_requested_and_final_framebuffers_equal_V4541']
    assert startup['all_five_postload_actor_model_and_captain_checks_equal']
    visual = values['current_six_frame_visual_review.json']
    assert visual['viewed'] and visual['no_new_display_finding'] and visual['candidate_sha256'] == ROM_SHA
    assert sha((ROOT/visual['sheet']).read_bytes()) == visual['sha256']
    for receipt in ['B176_completion_receipt.json','B177_reference_approval.json']:
        for path,digest in values[receipt]['evidence'].items():
            assert sha((ROOT/path).read_bytes()) == digest, path
    oldbytes = (ROOT/'translations/editorial_review_current_v1.json').read_bytes()
    assert sha(oldbytes) == values['B177_reference_checkpoint.json']['ledger_sha256']
    oldledger = json.loads(oldbytes)
    oldregistrybytes = (ROOT/'translations/release_stack.json').read_bytes()
    oldregistry = json.loads(oldregistrybytes)
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['profile'] == PROFILE and manifest['release_stack_sha256'] == REGISTRY_SHA
    assert len(manifest['batches']) == 552 and all(manifest['checks'].values())
    previous_packages = {}
    for p in (ROOT/'releases').glob('*/checksums.json'):
        for name,digest in read(p).items():
            assert sha((p.parent/name).read_bytes()) == digest, str(p.parent/name)
        previous_packages[p.parent.name] = sha(p.read_bytes())
    assert 'all_routes_unified_v4541' in previous_packages
    AUDIT.mkdir(parents=True)
    reconstruction = AUDIT/'promoted_patch_reconstruction_RESEARCH_ONLY.nds'
    apply_xdelta(ROOT/'work/clean.nds',ROM.with_suffix('.xdelta'),reconstruction)
    assert reconstruction.read_bytes() == ROM.read_bytes()
    verification = PACKAGE/'verification'
    verification.mkdir(parents=True)
    shutil.copyfile(ROM.with_suffix('.xdelta'),PACKAGE/'translation.xdelta')
    (PACKAGE/'build_manifest.json.gz').write_bytes(gzip.compress(ROM.with_suffix('.manifest.json').read_bytes(),mtime=0))
    (PACKAGE/'build_release_stack.json.gz').write_bytes(gzip.compress(oldregistrybytes,mtime=0))
    for name,source in EVIDENCE.items():
        shutil.copyfile(ROOT/source,verification/name)
    shutil.copyfile(ROOT/visual['sheet'],verification/'current_Lil_startup_and_town_review.png')
    promotion = {'format':'dk4-promoted-checkpoint-v1','status':'promoted','main_build':True,
        'promoted_on':datetime.now().astimezone().date().isoformat(),'checkpoint':'V4651',
        'user_request':'lets promote our current build as our new main build and then commit/push to github',
        'profile':PROFILE,'rom':ROM.relative_to(ROOT).as_posix(),'rom_sha256':ROM_SHA,
        'release_directory':PACKAGE.relative_to(ROOT).as_posix(),'git_tag':'promoted-v4595',
        'patch_sha256':PATCH_SHA,'source_rom_sha256':CLEAN_SHA,'build_manifest_sha256':MANIFEST_SHA,
        'build_registry_sha256':REGISTRY_SHA,'immutable_construction_baseline':deepcopy(oldregistry['canonical_baseline']),
        'previous_promoted_build':'releases/all_routes_unified_v4541/promotion.json',
        'promotion_scope':'User-designated main checkpoint; construction baseline and accepted-layer status preserved. Buildable profile retains experimental status.',
        'known_open_scope':NEXT,'complete_entries':5875,'source_prose_reviewed_entries':5888,
        'fresh_contextual_rereads':5885,'pending_credited_route_entries':10,'reviewed_incomplete_COMMON_entries':3,
        'B177_pending_integration_objects':10,'full_editorial_goal_complete':False,'full_graphics_goal_complete':False,
        'new_user_cold_boot_test_claimed':False,'new_emulator_runs_at_promotion':0,'construction_baseline_rebased':False}
    save(PACKAGE/'promotion.json',promotion)
    save(PACKAGE/'release_manifest.json',{'game':'Daikoukai Jidai IV / Rota Nova DS','patch_version':'unified-v4595',
        'status':'promoted','main_build':True,'profile':PROFILE,'source_rom_sha256':CLEAN_SHA,
        'modified_rom_sha256':ROM_SHA,'patch_sha256':PATCH_SHA,'full_editorial_goal_complete':False,
        'full_graphics_goal_complete':False,'promotion_record':'promotion.json','notes':SUMMARY})
    save(verification/'promotion_reconstruction.json',{'clean_input_sha256':CLEAN_SHA,'patch_sha256':PATCH_SHA,
        'candidate_sha256':ROM_SHA,'reconstructed_sha256':sha(reconstruction.read_bytes()),'whole_ROM_byte_exact':True,
        'original_build_registry_sha256':REGISTRY_SHA,'new_emulator_runs_at_promotion':0})
    save(verification/'promotion_test_results.json',{'command':'python -m pytest tests/test_integrated_release.py tests/test_dialogue_review.py tests/test_dialogue_balanced_wrap.py tests/test_dialogue_pair_phase.py tests/test_dialogue_relocation.py tests/test_lil_editorial_literal_guard.py -q',
        'result':'78 passed in 3.90s','exit_code':0,'source':'Observed promotion-turn exec output before staging','new_emulator_runs':0})
    draft = {'family':'B177','pending_reviewed_objects':10,'revised':5,'retained':5,
        'manuscript':'translations/lil_B177_editorial_manuscript_v6.json','native_reference_actual_approval_sealed':True,
        'new_B177_manuscript_integrated_in_promoted_ROM':False,'source_prose_or_completion_credit_added':0,
        'resume':NEXT,'full_goal_complete':False}
    save(verification/'UNINTEGRATED_B177_status.json',draft)
    ledger = deepcopy(oldledger)
    ledger['promoted_main_build_v4651'] = promotion
    ledger['latest_checkpoint'] = SUMMARY
    registry = deepcopy(oldregistry)
    registry['latest_promoted_build'] = {'status':'promoted','main_build':True,'profile':PROFILE,'rom_sha256':ROM_SHA,
        'record':'translations/promoted_build.json','git_tag':'promoted-v4595','construction_baseline_rebased':False}
    oldpins = read(ROOT/'translations/rom_retention_pins.json')
    pins = oldpins+[{'path':str(reconstruction.resolve()),'reason':'V4651 main V4595 byte-exact clean-input patch reconstruction. Preserve every ROM; no pruning. SHA-256 '+ROM_SHA}]
    validate_values(oldledger,ledger,oldregistry,registry,oldpins,pins)
    mutations = {'translations/release_stack.json':encoded(registry,True),
        'translations/promoted_build.json':encoded(promotion),'translations/editorial_review_current_v1.json':encode_ledger(ledger),
        'translations/rom_retention_pins.json':encoded(pins,True)}
    section = '## V4651: V4595 promoted as main; B177 integration pending\n\n'+SUMMARY+'\n\nMain build: [Unified V4595](../releases/all_routes_unified_v4595/README.md). ROM SHA-256: `'+ROM_SHA+'`. Patch SHA-256: `'+PATCH_SHA+'`. Earlier sections retain their original checkpoint status.\n\nNext: '+NEXT+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md','release_build.md']:
        path = 'docs/'+name
        first,rest = (ROOT/path).read_text(encoding='utf-8').split('\n',1)
        if name == 'editorial_handoff_current.md': first = '# Current editorial handoff - V4651'
        mutations[path] = (first+'\n\n'+section+rest).encode('utf-8')
    text = (ROOT/'README.md').read_text(encoding='utf-8')
    oldlink = '[Unified V4541](releases/all_routes_unified_v4541/README.md)'
    assert text.count(oldlink) == 2
    text = text.replace(oldlink,'[Unified V4595](releases/all_routes_unified_v4595/README.md)')
    text = text.replace('Earlier [V4496]','Earlier [V4541](releases/all_routes_unified_v4541/README.md), [V4496]',1)
    mutations['README.md'] = text.encode('utf-8')
    ignore = (ROOT/'.gitignore').read_text(encoding='utf-8')
    assert '!releases/all_routes_unified_v4595/*.xdelta' not in ignore
    mutations['.gitignore'] = (ignore+'!releases/all_routes_unified_v4595/*.xdelta\n').encode('utf-8')
    staged = AUDIT/'staged'
    staged.mkdir()
    plan = []
    for i,(relative,data) in enumerate(mutations.items()):
        target,planned = ROOT/relative,staged/f'{i}.planned'
        (AUDIT/f'{i}.before').write_bytes(target.read_bytes())
        planned.write_bytes(data)
        plan.append({'target':relative,'before_sha256':sha(target.read_bytes()),'planned':str(planned.relative_to(AUDIT)),
            'planned_sha256':sha(data)})
    save(AUDIT/'mutation_plan.json',plan)
    save(AUDIT/'staging_receipt.json',{'producer_sha256':sha(Path(__file__).read_bytes()),
        'evidence':{source:sha((ROOT/source).read_bytes()) for source in EVIDENCE.values()},
        'previous_packages':previous_packages,'mutations':len(plan),'new_emulator_runs':0,'ROMs_deleted':0})
    (PACKAGE/'README.md').write_text(
        '# Main promoted English build: V4595\n\nPromoted on '+promotion['promoted_on']+'. Earlier [V4541](../all_routes_unified_v4541/README.md) remains available.\n\n'
        'Apply [translation.xdelta](translation.xdelta) to a clean source ROM with SHA-256 `'+CLEAN_SHA+'`. Result SHA-256: `'+ROM_SHA+'`. Patch SHA-256: `'+PATCH_SHA+'`. No ROM is included.\n\n'
        '## Verification and coverage\n\nProfile `'+PROFILE+'` preserves all552 manuscript batches and114 accepted layers from the immutable baseline `out/raphael_natural_v2_accepted_base.nds` (SHA-256 `'+BASE_SHA+'`). Only SC2 B176 changes from V4541;all335 other blocks,every other file/component,ARM9,COMMON,fonts,graphics and123040 staged bytes remain exact. Fresh clean-input reconstruction is byte exact and78 release/dialogue tests pass.\n\n'
        'B176 has ten completed contextual decisions (five revisions/five retentions). Existing paired Japanese/English content-fixture cold boots cover all ten panels,nine progressive/one impersonal FE,source A000,C200,single end and normal town return. Eighty native alignments,40 stored cases and84 atomic negatives pass. Registered New Game/town cold boots provide31 whole-frame comparisons and five actor/captain checks. Final visual/completion receipts supersede earlier pending flags. These targeted automated headless emulator tests establish no natural event eligibility,earned fashion state,full-route completion,hardware or full-RAM/future-world equality. Promotion adds no new emulator run or user cold-boot claim.\n\n'
        '## Unfinished work\n\n'+SUMMARY+'\n\nB177 remains outside this ROM;its sealed actual/reference evidence records11 command-timing differences,14 following A-button-indicator animation differences and unequal PRNG seeds. See `verification/UNINTEGRATED_B177_status.json` and the preserved actual-view receipt.\n\nNext: '+NEXT+'\n\n'
        '## Reproduction records\n\n`build_manifest.json.gz` and `build_release_stack.json.gz` preserve exact build-time bytes. `verification/` contains scoped receipts and fresh reconstruction. `checksums.json` covers every other packaged file. The profile retains experimental status;the main designation is in `translations/promoted_build.json`. See the [current handoff](../../docs/editorial_handoff_current.md).\n',encoding='utf-8',newline='\n')
    print('Staged V4651 promotion;12 metadata files,byte-exact clean-input reconstruction,no editorial credit added.')


def validate_plan(applied=False):
    plan = read(AUDIT/'mutation_plan.json')
    assert len(plan) == 12 and len({r['target'] for r in plan}) == 12
    for i,row in enumerate(plan):
        target,planned = ROOT/row['target'],AUDIT/row['planned']
        assert target.resolve().is_relative_to(ROOT) and planned.resolve().is_relative_to(AUDIT.resolve())
        assert sha(target.read_bytes()) == row['planned_sha256' if applied else 'before_sha256']
        assert sha(planned.read_bytes()) == row['planned_sha256']
        assert sha((AUDIT/f'{i}.before').read_bytes()) == row['before_sha256']
    def load(relative,old=False):
        i = next(i for i,r in enumerate(plan) if r['target'] == relative)
        return read(AUDIT/f'{i}.before' if old else AUDIT/plan[i]['planned'])
    validate_values(load('translations/editorial_review_current_v1.json',True),load('translations/editorial_review_current_v1.json'),
        load('translations/release_stack.json',True),load('translations/release_stack.json'),
        load('translations/rom_retention_pins.json',True),load('translations/rom_retention_pins.json'))
    return plan


def apply():
    plan = validate_plan()
    assert sha(Path(__file__).read_bytes()) == read(AUDIT/'staging_receipt.json')['producer_sha256']
    for row in plan:
        data = (AUDIT/row['planned']).read_bytes()
        with (ROOT/row['target']).open('r+b') as stream:
            stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
    verify()


def verify():
    plan = validate_plan(True)
    receipt = read(AUDIT/'staging_receipt.json')
    assert sha(Path(__file__).read_bytes()) == receipt['producer_sha256']
    promotion = read(ROOT/'translations/promoted_build.json')
    ledger = read(ROOT/'translations/editorial_review_current_v1.json')
    assert promotion == read(PACKAGE/'promotion.json') == ledger['promoted_main_build_v4651']
    assert (ROOT/'translations/editorial_review_current_v1.json').read_bytes() == encode_ledger(ledger)
    assert sha(ROM.read_bytes()) == ROM_SHA
    assert ROM.read_bytes() == (AUDIT/'promoted_patch_reconstruction_RESEARCH_ONLY.nds').read_bytes()
    assert (PACKAGE/'translation.xdelta').read_bytes() == ROM.with_suffix('.xdelta').read_bytes()
    assert sha((ROOT/'work/clean.nds').read_bytes()) == CLEAN_SHA
    assert sha((ROOT/'out/raphael_natural_v2_accepted_base.nds').read_bytes()) == BASE_SHA
    assert gzip.decompress((PACKAGE/'build_manifest.json.gz').read_bytes()) == ROM.with_suffix('.manifest.json').read_bytes()
    old_registry_index = next(i for i,r in enumerate(plan) if r['target'] == 'translations/release_stack.json')
    assert gzip.decompress((PACKAGE/'build_release_stack.json.gz').read_bytes()) == (AUDIT/f'{old_registry_index}.before').read_bytes()
    for name,source in EVIDENCE.items():
        assert (PACKAGE/'verification'/name).read_bytes() == (ROOT/source).read_bytes()
        assert sha((ROOT/source).read_bytes()) == receipt['evidence'][source]
    for name,digest in receipt['previous_packages'].items():
        p = ROOT/'releases'/name/'checksums.json'
        assert sha(p.read_bytes()) == digest
        for path,h in read(p).items(): assert sha((p.parent/path).read_bytes()) == h
    audit = {'checkpoint':'V4651','profile':PROFILE,'main_build':True,'rom_sha256':ROM_SHA,'patch_sha256':PATCH_SHA,
        'manifest_batches':552,'accepted_layers':114,'whole_clean_input_patch_reconstruction_byte_exact':True,
        'all_prior_ledger_records_nested_history_and_coverage_preserved':True,'only_registry_main_pointer_changed':True,
        'canonical_baseline_unchanged':True,'completed_contextual_reviews':5875,'fresh_contextual_rereads':5885,
        'source_prose_reviews':5888,'pending_credited_route_reviews':10,'B177_in_promoted_ROM':False,
        'ledger_sha256':sha((ROOT/'translations/editorial_review_current_v1.json').read_bytes()),
        'previous_release_checksums_verified':list(receipt['previous_packages']),'targeted_tests_passed':78,
        'new_emulator_runs_at_promotion':0,'ROMs_deleted':0,'full_goal_active':True,'full_goal_complete':False,
        'updated_files':{r['target']:r['planned_sha256'] for r in plan},'producer_sha256':sha(Path(__file__).read_bytes())}
    save(AUDIT/'promotion_receipt.json',audit)
    save(PACKAGE/'verification/promotion_final_audit.json',audit)
    checksums = {p.relative_to(PACKAGE).as_posix():sha(p.read_bytes()) for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'}
    save(PACKAGE/'checksums.json',checksums)
    assert all(sha((PACKAGE/p).read_bytes()) == h for p,h in checksums.items())
    print('V4595 promoted and audited;all prior ledger history/packages preserved,B177 pending,78 tests passed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode',choices=['stage','apply','verify'])
    {'stage':stage,'apply':apply,'verify':verify}[parser.parse_args().mode]()
