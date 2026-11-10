"""Register the validated six outcomes after the complete V8300 stack, preserving all prior profiles."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import hodram_outcomes_editorial_v3 as owned
from dk4tool.patch.hodram_outcomes_builder_guard_v2 import STAGE,LEGACY_STAGE,validate_builder_bytes
from dk4tool.dialogue.hodram_outcomes_profile_v3 import contract
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.Hodram_outcomes_release_paths_v8347 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcomes_registration_v8376')
PROFILE='all-routes-unified-v8377'
POSITIVE=Path('work/analysis/Hodram_outcome_atomic_positive_v8374b/one_whole_NDS_commit_exact_reference_andunchanged_precommit_input.json')
NEGATIVE=Path('work/analysis/Hodram_outcomes_atomic_challenges_v8356b/actual_changing_semantic_precommit_rejections.json')
BINDING=Path('work/analysis/Hodram_fixture_binding_v8375b/semantic_binding.json')
if __name__=='__main__':
    assert not ROOT.exists();positive,negative,binding=map(read,[POSITIVE,NEGATIVE,BINDING]);conf=read(owned.CONFIG);frozen=contract()
    assert positive['single_complete_NDS_commit'] and positive['original_object_still_exact_after_commit'] and len(positive['report']['changed_records'])==6
    assert negative['negative_count']==len(negative['cases'])==50 and negative['all_expected_semantic_guards_match'] and negative['all_protected_files_hash_exact']
    assert all(c['rejected'] and c['commit_calls']==0 and c['actual_input_changes_asserted'] and c['dependency_digest_gate_deliberately_bypassed'] for c in negative['cases'])
    assert binding['prior_semantic_cases']==50 and len(binding['derivations'])==7 and binding['new_lifecycle_negative_count']==3 and binding['new_builder_guard_negative_count']==11 and positive['canonical_source_path_with_exact_current_parent_memory']
    owned.check_dependencies(conf);assert sha(PARENT.read_bytes())==conf['parent_ROM_sha256'] and positive['planned_output_sha256']==conf['reference_ROM_sha256']
    verified=read('work/analysis/editorial_handoff_verification_v8371/verified_handoff.json');assert verified['candidate_sha256']==conf['parent_ROM_sha256'] and sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==641
    anchor='    # Lexically valid "% o"';text=before.decode('utf8');assert text.count(anchor)==1 and text.count(LEGACY_STAGE)==1 and STAGE not in text
    digest=frozen['dependencies'][str(builder.resolve())];assert validate_builder_bytes(before,digest)['owned_stage_version']=='preserved-v2'
    frozen_builder=before.replace(LEGACY_STAGE.encode(),b'',1);assert sha(frozen_builder)==digest
    after=checked_text(text,{LEGACY_STAGE:STAGE}).encode('utf8')
    assert after.replace(STAGE.encode(),b'',1)==frozen_builder and validate_builder_bytes(after,digest)['owned_stage_version']=='current-v3'

    profile=deepcopy(registry['profiles']['all-routes-unified-v8300'])
    profile.update(status='experimental',hodram_outcomes_editorial=owned.CONFIG,
        description='Complete V8300 plus clean-Japanese whole-exchange Hodram SC1 B47/B48 outcomes:6records,3revisions and3justified retentions.',
        note='Natural-dialogue-v2:preserve Lil voice,qualified Ullr Bow discovery,best-in-world expectation andAmsterdam wait direction;no invented unfairness/rank/relationship/award. Six one-page complete native bodies,originalFE/null actor/oneFI,full usable width,zero warnings/waivers,six source line-count infos. Exact15commands/six preambles/two full ends/tails/seven opaque effects andboth clean/fullparent inverses. All325wholeloads650modes/caller census. Four whole-script initialized source/revised fixtures40004frames plus8002focusedFE frames cover12complete pages/100body-name orFE-absentheader holds. OriginalFE typed context/view/palette/bankDVRAM/physicalRGB fullybound;temporary stackcontext isnot persistentview. B48 source4495/English4494 returns;allscriptboundaryPRNGpairs equal,but13of93laterRGBpairs andfinalPRNGdiffer. Five checked components/actors/captain1 match;no naturalactivation/eligibility/fullroute/hardware/everyframe/future-outcome/simulationequivalence. Frozen357policy rejections;50semanticprecommitrejections retained through exact sourceequivalence;newbuilder11negativeguard cases,3changed-memory lifecycle rejections andfresh canonical-source/current-memory whole-object positive;one tested fixtureinverse correction. All417frozen dependencyentries preserved through exactownedbuilderstage/fullsourceinverse;all492priorproductiondependencies retained;failedV8362 profile andalllogs preserved. Fullstory/sharedtown-shop/random/Help/207names/earlierwrap goalactive;graphics/latertechnicalaudit separate. B49clean14speech/twochoiceglosses remainuncredited/currentEnglishunread. No separatepackage,promotion,pruning,commit orpush;main4701unchanged.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(STAGE.encode());(ROOT/'builder.previous_stage.bin').write_bytes(LEGACY_STAGE.encode());(ROOT/'builder.frozen_original.bin').write_bytes(frozen_builder);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    temporary=builder.with_name('build_integrated_release_v8376.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(STAGE.encode(),LEGACY_STAGE.encode(),1)==before and builder.read_bytes().replace(STAGE.encode(),b'',1)==frozen_builder
    assert contract()==frozen;owned.check_dependencies(conf)
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v8300',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=str(POSITIVE),positive_proof_sha256=sha(POSITIVE.read_bytes()),negative_cases=str(NEGATIVE),negative_cases_sha256=sha(NEGATIVE.read_bytes()),negative_count=50,semantic_source_binding=str(BINDING),semantic_source_binding_sha256=sha(BINDING.read_bytes()),prior_semantic_cases_reused_not_claimed_as_rerun=True,new_builder_negative_cases=11,new_canonical_lifecycle_negative_cases=3,all_prior_profiles_accepted_layers_andmain_preserved=True,expected_manifest_batches=642,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],exact_owned_builder_stage_andwhole_frozen_source_inverse=True,producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimental V8377 aftercompleteV8300:642expectedmanifest/114accepted;exactbuilderinverse;mainunchanged.Completioncredit pendingverifiedrelease.')
