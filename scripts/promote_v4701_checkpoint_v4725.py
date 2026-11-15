"""Stage and audit the explicitly requested V4701 main promotion without rebasing."""
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

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.xdelta import apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'work/analysis/promotion_v4725'
PACKAGE = ROOT / 'releases/all_routes_unified_v4701'
ROM = ROOT / 'out/all_routes_combined_v4701_candidate.nds'
PROFILE = 'all-routes-unified-v4701'
ROM_SHA = 'dbfb4e413047e54e50dc771f48fe0e5457e40e60e0991111474185c41858052e'
PATCH_SHA = 'fb3cc03224d63bf8fff48fbc577d942483c36d9ed5c80e07de264e539dff33cf'
MANIFEST_SHA = '10a2cff0c6d258a8d7961961095041921bb900173d23a1ed62b15cbba0dbf26f'
REGISTRY_SHA = '66692127cfe0a51086ade2bafcc9082b08f92ace27b8d9029eb510bd52d02c63'
LEDGER_SHA = 'ae6933430a6690501680b7c96cef2cbb8bf1ecc3c8a335f143e30a9bb136af6c'
CLEAN_SHA = 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
BASE_SHA = '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
NEXT = (
    'Resume B179 from manuscript v2 and passing fourteen-paragraph layout V4723. '
    'Run the prepared V4724 native-font checks once; view both sheets separately and '
    'complete native approval, reversible relocation/stored checks, representative actual '
    'content coverage, registered cumulative integration, exact clean-input patch and startup '
    'gates before credit. Preserve thirteen progressive panels and one impersonal FE, '
    'Barkeep92/Patron96/Sailor152 versus separate catalog Retainer152, sixteen commands, '
    'A0008 raw00a0ffff01221da1 and end508; no C200 exists. Preserve all eight revisions '
    'and six individually justified retentions unless a concrete finding requires review. '
    'Investigate separate untranslated Sao Jorge alias ARM9 15E5D4, pointer122504, '
    'for its specific consumer/ownership/display use without assuming dead storage or actual '
    'display. Continue B180 and every remaining storyline, shared shop/town dialogue, '
    'random scene, Help and other player-facing prose. B179-B180 has25 physical speeches, '
    'not a project denominator. Preserve COMMON750-752, canonical Maria32 SC3B97, '
    'SourceItems/LocalProduct, five named-target leads, exact-record Proof consistency, '
    'Samwell full-catalog middle-field lead and B157 provenance amendment. Keep graphics/all18 '
    'plaques separate and retain the later older-record technical re-audit/queued0D gap. '
    'Preserve all ROMs, translations, drafts, executed producers, proofs and failures. '
    'The full editorial goal remains active.')
SUMMARY = (
    'V4725 promotes verified cumulative V4701 as the user-designated main build, with '
    'completed B177 and B178 following the entire V4595 stack. The registered manifest '
    'contains554 manuscript batches and114 accepted layers. A fresh clean-input patch '
    'reconstruction is byte exact;78 release/dialogue regressions pass in3.84s. Promotion '
    'changes no ROM bytes, construction baseline or accepted-layer status and adds no '
    'editorial credit, emulator run or user cold-boot claim. Coverage stays5898 completed '
    'contextual rereads,5901 source/prose reviews,3740 historical revisions/2158 retentions, '
    'route4299/4299 and zero pending credited route drafts. B179 manuscript v2 remains '
    'outside the ROM and uncredited:14 whole-exchange decisions,8 revisions/6 justified '
    'retentions, terms/current comparison complete and offline paragraph layout passing. '
    'Native planes, actual gameplay and release gates remain pending. Six Sailor lines '
    'were still Japanese in the predecessor; their technical cause is not established. '
    'Approved Sao Jorge/Wine bindings are recorded, along with separate untranslated '
    'city alias15E5D4/pointer122504 as an unresolved shared-text lead. All earlier packages, '
    'ROMs, translations, drafts, proofs, failures and complete ledger history are preserved. '
    'Graphics and the later older-record technical re-audit remain separate and open. '
    'The full editorial objective remains active.')
EVIDENCE = {
    'registered_release_verification.json': 'work/analysis/lil_B178_release_v4702/registered_release_verification.json',
    'cold_boot_Lil_startup_town_verification.json': 'work/analysis/lil_B178_startup_v4704/cold_boot_Lil_startup_town_verification.json',
    'current_six_frame_visual_review.json': 'work/analysis/lil_B178_startup_v4704/current_six_frame_visual_review.json',
    'B177_completion_receipt.json': 'work/analysis/lil_B177_completion_v4659/completion_receipt.json',
    'B178_completion_receipt.json': 'work/analysis/lil_B178_completion_v4705/completion_receipt.json',
    'V4717_verified_handoff.json': 'work/analysis/editorial_handoff_verification_v4717/verified_handoff.json',
    'B177_final_review.json': 'translations/lil_B177_contextual_final_review_v1.json',
    'B178_final_review.json': 'translations/lil_B178_contextual_final_review_v1.json',
    'B178_actual_view.json': 'work/analysis/lil_B178_actual_review_v4695/all3_actual_sheets13_planes_fullscreens_return_and_final_state.json',
    'B179_pending_manuscript_v2.json': 'translations/lil_B179_editorial_manuscript_v2.json',
    'B179_context_checkpoint.json': 'work/analysis/lil_B179_context_checkpoint_v4716/checkpoint_receipt.json',
    'B179_terms.json': 'work/analysis/lil_B179_terms_v4718/Barkeep_Patron_Sailor_Sao_Jorge_Wine_and_prospective_fashion_reconciliation.json',
    'B179_current_comparison.json': 'work/analysis/lil_B179_comparison_v4719/all14_current_effective_comparison_packet.json',
    'B179_layout_QA.json': 'work/analysis/lil_B179_layout_v4723/all14_paragraph_layout_QA.json',
    'untranslated_Sao_Jorge_alias_reference_lead.json': 'work/analysis/lil_B179_terms_v4718/untranslated_Sao_Jorge_alias_reference_lead.json',
    'previous_unfinished_editorial_scope_inventory.json': 'work/analysis/lil_B178_completion_v4705/unfinished_editorial_scope_inventory.json',
}
NEW_KEYS = {'promoted_main_build_v4725', 'lil_B179_uncredited_draft_v4725', 'unfinished_editorial_scope_v4725'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def encoded(value, crlf=False):
    data = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return data.replace(b'\n', b'\r\n') if crlf else data


def save(path, value):
    Path(path).write_bytes(encoded(value))


def validate_values(old, new, oldreg, reg, oldpins, pins):
    assert not NEW_KEYS.intersection(old)
    assert set(new) == set(old) | NEW_KEYS
    assert {k:v for k,v in new.items() if k not in NEW_KEYS | {'latest_checkpoint'}} == {
        k:v for k,v in old.items() if k != 'latest_checkpoint'}
    assert new['goal_status'] == 'active' and not new['full_goal_complete']
    assert tuple(new[k] for k in ['records_editorially_completed', 'records_with_source_and_prose_pass',
        'records_revised_and_integrated', 'retained_wordings_editorially_completed']) == (5898,5901,3740,2158)
    fresh = new['contextual_story_natural_dialogue_pass_v1871']
    assert tuple(fresh[k] for k in ['fresh_pass_records_explicitly_reread', 'fresh_pass_records_integrated',
        'fresh_pass_records_pending_native_actual_release']) == (5898,5898,0)
    assert fresh['pending_contextual_families'] == []
    assert {k:v for k,v in oldreg.items() if k != 'latest_promoted_build'} == {
        k:v for k,v in reg.items() if k != 'latest_promoted_build'}
    assert reg['latest_promoted_build']['profile'] == PROFILE
    assert reg['profiles'][PROFILE]['status'] == 'experimental' and len(reg['accepted_layers']) == 114
    assert pins[:-1] == oldpins and Path(pins[-1]['path']).read_bytes() == ROM.read_bytes()
    assert new['lil_B179_uncredited_draft_v4725']['credit_added'] == 0
    assert new['unfinished_editorial_scope_v4725']['untranslated_Sao_Jorge_alias_lead']['id'] == 'ARM9-Sao-Jorge-alias-15E5D4-pointer122504'
    assert len(encode_ledger(new)) < 100*1024*1024


def stage():
    assert Path.cwd() == ROOT and not AUDIT.exists() and not PACKAGE.exists()
    for path,digest in [(ROM,ROM_SHA),(ROM.with_suffix('.xdelta'),PATCH_SHA),
        (ROM.with_suffix('.manifest.json'),MANIFEST_SHA),(ROOT/'translations/release_stack.json',REGISTRY_SHA),
        (ROOT/'translations/editorial_review_current_v1.json',LEDGER_SHA),
        (ROOT/'work/clean.nds',CLEAN_SHA),(ROOT/'out/raphael_natural_v2_accepted_base.nds',BASE_SHA)]:
        assert sha(path.read_bytes()) == digest, str(path)
    values = {name:read(ROOT/path) for name,path in EVIDENCE.items()}
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['profile'] == PROFILE and manifest['release_stack_sha256'] == REGISTRY_SHA
    assert len(manifest['batches']) == 554 and all(manifest['checks'].values())
    assert values['registered_release_verification.json']['whole_ROM_reconstruction_byte_exact']
    checked = values['V4717_verified_handoff.json']
    assert checked['ledger_sha256'] == LEDGER_SHA and checked['all_jobs_terminal'] and checked['full_goal_active']
    startup = values['cold_boot_Lil_startup_town_verification.json']
    assert startup['candidate_sha256'] == ROM_SHA and startup['paired_frame_count'] == 31
    assert startup['all_current_requested_and_final_framebuffers_equal_V4655']
    assert startup['all_five_postload_actor_model_and_captain_checks_equal']
    visual = values['current_six_frame_visual_review.json']
    assert visual['viewed'] and visual['no_new_display_finding'] and visual['candidate_sha256'] == ROM_SHA
    assert sha((ROOT/visual['sheet']).read_bytes()) == visual['sha256']
    for name in ['B177_completion_receipt.json','B178_completion_receipt.json']:
        assert values[name]['all_jobs_terminal']
        for path,digest in values[name]['evidence'].items():
            assert sha((ROOT/path).read_bytes()) == digest, path
    draft = values['B179_pending_manuscript_v2.json']
    assert len(draft['records']) == 14 and (draft['revised'],draft['retained']) == (8,6)
    assert draft['formatting_review_pending'] and draft['source_prose_or_completion_credit_added'] == 0
    assert values['B179_layout_QA.json']['failures'] == []
    for key,value in draft.items():
        if key.endswith('_sha256') and key[:-7] in draft and isinstance(draft[key[:-7]],str):
            dependency = ROOT/draft[key[:-7]]
            if dependency.is_file(): assert sha(dependency.read_bytes()) == value, str(dependency)
    oldbytes = (ROOT/'translations/editorial_review_current_v1.json').read_bytes()
    old = json.loads(oldbytes)
    regbytes = (ROOT/'translations/release_stack.json').read_bytes()
    oldreg = json.loads(regbytes)
    previous_packages = {}
    for path in (ROOT/'releases').glob('*/checksums.json'):
        for name,digest in read(path).items(): assert sha((path.parent/name).read_bytes()) == digest
        previous_packages[path.parent.name] = sha(path.read_bytes())
    assert 'all_routes_unified_v4595' in previous_packages
    before,after = [NdsImage.open(ROOT/f'out/all_routes_combined_v{v}_candidate.nds') for v in [4595,4701]]
    file_changes = [p for _,p,data in before.iter_files() if after.read_file(p) != data]
    component_changes = [p for p,data in before.iter_components() if after.read_file(p) != data]
    assert file_changes == ['/data/SC2.DK4'] and component_changes == []
    containers = [IlnkContainer.parse(image.read_file('/data/SC2.DK4')) for image in [before,after]]
    assert len(containers[0].blocks) == len(containers[1].blocks) == 336
    changed_blocks = [i for i,(a,b) in enumerate(zip(containers[0].blocks,containers[1].blocks)) if a.data != b.data]
    assert changed_blocks == [177,178], changed_blocks
    AUDIT.mkdir(parents=True)
    reconstruction = AUDIT/'promoted_patch_reconstruction_RESEARCH_ONLY.nds'
    apply_xdelta(ROOT/'work/clean.nds',ROM.with_suffix('.xdelta'),reconstruction)
    assert reconstruction.read_bytes() == ROM.read_bytes()
    verification = PACKAGE/'verification'
    verification.mkdir(parents=True)
    shutil.copyfile(ROM.with_suffix('.xdelta'),PACKAGE/'translation.xdelta')
    (PACKAGE/'build_manifest.json.gz').write_bytes(gzip.compress(ROM.with_suffix('.manifest.json').read_bytes(),mtime=0))
    (PACKAGE/'build_release_stack.json.gz').write_bytes(gzip.compress(regbytes,mtime=0))
    for name,source in EVIDENCE.items(): shutil.copyfile(ROOT/source,verification/name)
    shutil.copyfile(ROOT/visual['sheet'],verification/'current_Lil_startup_and_town_review.png')
    promotion = dict(format='dk4-promoted-checkpoint-v1',status='promoted',main_build=True,
        promoted_on=datetime.now().astimezone().date().isoformat(),checkpoint='V4725',
        user_request='lets promote our current build as our new main build and then commit/push to github',
        profile=PROFILE,rom=ROM.relative_to(ROOT).as_posix(),rom_sha256=ROM_SHA,
        release_directory=PACKAGE.relative_to(ROOT).as_posix(),git_tag='promoted-v4701',
        patch_sha256=PATCH_SHA,source_rom_sha256=CLEAN_SHA,build_manifest_sha256=MANIFEST_SHA,
        build_registry_sha256=REGISTRY_SHA,immutable_construction_baseline=deepcopy(oldreg['canonical_baseline']),
        previous_promoted_build='releases/all_routes_unified_v4595/promotion.json',
        promotion_scope='User-designated main checkpoint; immutable baseline and accepted-layer status unchanged.',
        known_open_scope=NEXT,complete_entries=5898,source_prose_reviewed_entries=5901,
        fresh_contextual_rereads=5898,pending_credited_route_entries=0,uncredited_B179_draft_entries=14,
        full_editorial_goal_complete=False,full_graphics_goal_complete=False,
        new_user_cold_boot_test_claimed=False,new_emulator_runs_at_promotion=0,construction_baseline_rebased=False)
    save(PACKAGE/'promotion.json',promotion)
    save(PACKAGE/'release_manifest.json',dict(game='Daikoukai Jidai IV / Rota Nova DS',patch_version='unified-v4701',
        status='promoted',main_build=True,profile=PROFILE,source_rom_sha256=CLEAN_SHA,
        modified_rom_sha256=ROM_SHA,patch_sha256=PATCH_SHA,full_editorial_goal_complete=False,
        full_graphics_goal_complete=False,promotion_record='promotion.json',notes=SUMMARY))
    save(verification/'promotion_reconstruction.json',dict(clean_input_sha256=CLEAN_SHA,patch_sha256=PATCH_SHA,
        candidate_sha256=ROM_SHA,reconstructed_sha256=sha(reconstruction.read_bytes()),whole_ROM_byte_exact=True,
        original_build_registry_sha256=REGISTRY_SHA,changed_internal_files_from_V4595=file_changes,
        changed_components_from_V4595=component_changes,changed_SC2_blocks_from_V4595=changed_blocks))
    save(verification/'promotion_test_results.json',dict(command='python -m pytest tests/test_integrated_release.py tests/test_dialogue_review.py tests/test_dialogue_balanced_wrap.py tests/test_dialogue_pair_phase.py tests/test_dialogue_relocation.py tests/test_lil_editorial_literal_guard.py -q',
        result='78 passed in 3.84s',exit_code=0,source='Observed promotion-turn exec result',new_emulator_runs=0))
    draft_status = dict(family='B179',records=14,revised=8,retained=6,credit_added=0,
        manuscript='translations/lil_B179_editorial_manuscript_v2.json',
        manuscript_sha256=sha((ROOT/'translations/lil_B179_editorial_manuscript_v2.json').read_bytes()),
        terms_and_complete_current_comparison_complete=True,offline_paragraph_layout_passed=True,
        native_planes_and_visual_approval_pending=True,actual_and_release_gates_pending=True,
        integrated_in_promoted_ROM=False,resume=NEXT,full_goal_complete=False)
    save(verification/'UNINTEGRATED_B179_status.json',draft_status)
    scope = deepcopy(values['previous_unfinished_editorial_scope_inventory.json'])
    scope['promotion_v4725_resume'] = NEXT
    scope['B179_uncredited_draft_v4725'] = draft_status
    scope['untranslated_Sao_Jorge_alias_lead'] = values['untranslated_Sao_Jorge_alias_reference_lead.json']
    save(verification/'unfinished_editorial_scope_inventory.json',scope)
    new = deepcopy(old)
    new.update(promoted_main_build_v4725=promotion,lil_B179_uncredited_draft_v4725=draft_status,
        unfinished_editorial_scope_v4725=scope,latest_checkpoint=SUMMARY)
    reg = deepcopy(oldreg)
    reg['latest_promoted_build'] = dict(status='promoted',main_build=True,profile=PROFILE,rom_sha256=ROM_SHA,
        record='translations/promoted_build.json',git_tag='promoted-v4701',construction_baseline_rebased=False)
    oldpins = read(ROOT/'translations/rom_retention_pins.json')
    pins = oldpins+[dict(path=str(reconstruction.resolve()),reason='V4725 main V4701 byte-exact clean-input patch reconstruction. Preserve every ROM. SHA-256 '+ROM_SHA)]
    validate_values(old,new,oldreg,reg,oldpins,pins)
    mutations = {'translations/release_stack.json':encoded(reg,True),
        'translations/promoted_build.json':encoded(promotion),'translations/editorial_review_current_v1.json':encode_ledger(new),
        'translations/rom_retention_pins.json':encoded(pins,True)}
    section = ('## V4725: V4701 promoted as main; B179 draft preserved\n\n'+SUMMARY+
        '\n\nMain: [Unified V4701](../releases/all_routes_unified_v4701/README.md). ROM SHA-256: `'+ROM_SHA+
        '`. Patch SHA-256: `'+PATCH_SHA+'`. Earlier sections retain historical checkpoint status.\n\nNext: '+NEXT+'\n\n')
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md','release_build.md']:
        path = 'docs/'+name
        first,rest = (ROOT/path).read_text(encoding='utf-8').split('\n',1)
        if name == 'editorial_handoff_current.md': first = '# Current editorial handoff - V4725'
        mutations[path] = (first+'\n\n'+section+rest).encode('utf-8')
    text = (ROOT/'README.md').read_text(encoding='utf-8')
    oldlink = '[Unified V4595](releases/all_routes_unified_v4595/README.md)'
    assert text.count(oldlink) == 2
    text = text.replace(oldlink,'[Unified V4701](releases/all_routes_unified_v4701/README.md)')
    text = text.replace('Earlier [V4541]','Earlier [V4595](releases/all_routes_unified_v4595/README.md), [V4541]',1)
    mutations['README.md'] = text.encode('utf-8')
    ignore = (ROOT/'.gitignore').read_text(encoding='utf-8')
    assert '!releases/all_routes_unified_v4701/*.xdelta' not in ignore
    mutations['.gitignore'] = (ignore+'!releases/all_routes_unified_v4701/*.xdelta\n').encode('utf-8')
    staged = AUDIT/'staged'
    staged.mkdir()
    plan = []
    for i,(relative,data) in enumerate(mutations.items()):
        target,planned = ROOT/relative,staged/f'{i}.planned'
        (AUDIT/f'{i}.before').write_bytes(target.read_bytes())
        planned.write_bytes(data)
        plan.append(dict(target=relative,before_sha256=sha(target.read_bytes()),planned=str(planned.relative_to(AUDIT)),planned_sha256=sha(data)))
    save(AUDIT/'mutation_plan.json',plan)
    save(AUDIT/'staging_receipt.json',dict(producer_sha256=sha(Path(__file__).read_bytes()),
        evidence={p:sha((ROOT/p).read_bytes()) for p in EVIDENCE.values()},previous_packages=previous_packages,
        mutations=len(plan),new_emulator_runs=0,ROMs_deleted=0))
    (PACKAGE/'README.md').write_text(
        '# Main promoted English build: V4701\n\nPromoted on '+promotion['promoted_on']+
        '. Earlier [V4595](../all_routes_unified_v4595/README.md) remains available.\n\n'
        'Apply [translation.xdelta](translation.xdelta) to a clean source ROM with SHA-256 `'+CLEAN_SHA+
        '`. Result SHA-256: `'+ROM_SHA+'`. Patch SHA-256: `'+PATCH_SHA+'`. No ROM is included.\n\n'
        '## Verification and coverage\n\nProfile `'+PROFILE+'` preserves554 manuscript batches and114 accepted layers. '
        'The immutable base is `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `'+BASE_SHA+'`. '
        'Only SC2 blocks177 and178 change from V4595; all334 other blocks and every other file/component, '
        'ARM9, COMMON, fonts, graphics and staged payload remain exact. A fresh clean-input reconstruction '
        'is byte exact and78 release/dialogue tests pass. B177 adds5 revisions/5 retentions; B178 adds2/11. '
        'B178 has104 native alignments,52 stored cases and98 atomic negatives. Existing paired Japanese/English '
        'content-fixture cold boots cover all13 B178 panels, source A000/C200/end and parent return. '
        'Fourteen command-timing differences and four following A-button-indicator RGB differences remain '
        'disclosed in the actual-view receipt; final RGB and scoped native state agree. Registered New Game/town '
        'cold boots provide31 whole-frame comparisons/five actor controls/six viewed screens. These targeted '
        'automated headless tests establish no natural event eligibility, earned fashion, full route, hardware '
        'or full-RAM/future-world equality. Final visual/completion receipts supersede earlier pending flags. '
        'Promotion adds no emulator run or user cold-boot claim.\n\n'
        '## Unfinished work\n\n'+SUMMARY+'\n\nNext: '+NEXT+'\n\n'
        '## Reproduction records\n\n`build_manifest.json.gz` and `build_release_stack.json.gz` retain exact '
        'build-time bytes. `verification/` contains scoped evidence, the unintegrated B179 status and open '
        'city-alias lead. `checksums.json` covers every other packaged file. The profile remains experimental; '
        'the user-designated main pointer is `translations/promoted_build.json`. See the '
        '[current handoff](../../docs/editorial_handoff_current.md).\n',encoding='utf-8',newline='\n')
    print('Staged V4725 promotion:12 metadata targets; fresh exact reconstruction; no credit or ROM changes.')


def validate_plan(applied=False):
    plan = read(AUDIT/'mutation_plan.json')
    assert len(plan) == len({r['target'] for r in plan}) == 12
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
            stream.write(data); stream.truncate(len(data)); stream.flush(); os.fsync(stream.fileno())
    verify()


def verify():
    plan = validate_plan(True)
    receipt = read(AUDIT/'staging_receipt.json')
    assert sha(Path(__file__).read_bytes()) == receipt['producer_sha256']
    promotion = read(ROOT/'translations/promoted_build.json')
    ledger = read(ROOT/'translations/editorial_review_current_v1.json')
    assert promotion == read(PACKAGE/'promotion.json') == ledger['promoted_main_build_v4725']
    assert (ROOT/'translations/editorial_review_current_v1.json').read_bytes() == encode_ledger(ledger)
    assert sha(ROM.read_bytes()) == ROM_SHA and ROM.read_bytes() == (AUDIT/'promoted_patch_reconstruction_RESEARCH_ONLY.nds').read_bytes()
    assert (PACKAGE/'translation.xdelta').read_bytes() == ROM.with_suffix('.xdelta').read_bytes()
    assert sha((ROOT/'work/clean.nds').read_bytes()) == CLEAN_SHA
    assert sha((ROOT/'out/raphael_natural_v2_accepted_base.nds').read_bytes()) == BASE_SHA
    assert gzip.decompress((PACKAGE/'build_manifest.json.gz').read_bytes()) == ROM.with_suffix('.manifest.json').read_bytes()
    index = next(i for i,r in enumerate(plan) if r['target'] == 'translations/release_stack.json')
    assert gzip.decompress((PACKAGE/'build_release_stack.json.gz').read_bytes()) == (AUDIT/f'{index}.before').read_bytes()
    for name,source in EVIDENCE.items():
        assert (PACKAGE/'verification'/name).read_bytes() == (ROOT/source).read_bytes()
        assert sha((ROOT/source).read_bytes()) == receipt['evidence'][source]
    for name,digest in receipt['previous_packages'].items():
        path = ROOT/'releases'/name/'checksums.json'
        assert sha(path.read_bytes()) == digest
        for relative,h in read(path).items(): assert sha((path.parent/relative).read_bytes()) == h
    audit = dict(checkpoint='V4725',profile=PROFILE,main_build=True,rom_sha256=ROM_SHA,patch_sha256=PATCH_SHA,
        manifest_batches=554,accepted_layers=114,whole_clean_input_patch_reconstruction_byte_exact=True,
        all_prior_ledger_root_records_nested_history_and_coverage_preserved=True,only_registry_main_pointer_changed=True,
        canonical_baseline_unchanged=True,completed_contextual_reviews=5898,source_prose_reviews=5901,
        pending_credited_route_reviews=0,uncredited_B179_draft_entries=14,B179_in_promoted_ROM=False,
        untranslated_Sao_Jorge_alias_lead_preserved=True,
        ledger_sha256=sha((ROOT/'translations/editorial_review_current_v1.json').read_bytes()),
        previous_release_checksums_verified=list(receipt['previous_packages']),targeted_tests_passed=78,
        new_emulator_runs_at_promotion=0,ROMs_deleted=0,full_goal_active=True,full_goal_complete=False,
        updated_files={r['target']:r['planned_sha256'] for r in plan},producer_sha256=sha(Path(__file__).read_bytes()))
    save(AUDIT/'promotion_receipt.json',audit)
    save(PACKAGE/'verification/promotion_final_audit.json',audit)
    checksums = {p.relative_to(PACKAGE).as_posix():sha(p.read_bytes()) for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'}
    save(PACKAGE/'checksums.json',checksums)
    assert all(sha((PACKAGE/p).read_bytes()) == h for p,h in checksums.items())
    print('Promoted V4701: exact patch, all previous packages/history preserved, B179 uncredited, full goal active.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode',choices=['stage','apply','verify'])
    {'stage':stage,'apply':apply,'verify':verify}[parser.parse_args().mode]()
