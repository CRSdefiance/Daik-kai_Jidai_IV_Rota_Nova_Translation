"""Register corrected B49 after complete V8377,with exact prior builder/profile inverse andno promotion."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import hodram_B49_editorial_v2 as owned
from dk4tool.patch.hodram_outcomes_builder_guard_v4 import STAGE_V3
from dk4tool.patch.hodram_outcomes_builder_guard_v5 import BUILDER,STAGE_V5,STAGE_B49_V2,validate_builder_bytes
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.Hodram_B49_release_paths_v8450 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_registration_v8458')
PROFILE='all-routes-unified-v8459'
POSITIVE=Path('work/analysis/Hodram_B49_atomic_positive_v8456/atomic_positive.json')
NEGATIVE=Path('work/analysis/Hodram_B49_atomic_challenges_v8457/semantic_rejections.json')
BINDING=Path('work/analysis/Hodram_B49_predecessor_binding_v8454/semantic_binding.json')
GUARD=Path('work/analysis/Hodram_B49_builder_v8452/exact_builder_inverse_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();positive,negative,binding,guard=map(read,[POSITIVE,NEGATIVE,BINDING,GUARD]);conf=read(owned.CONFIG);owned.check_dependencies(conf)
    assert positive['one_complete_NDS_commit'] and positive['original_object_still_exact_after_commit'] and positive['canonical_source_path_withcomplete_V8377_memory'] and len(positive['report']['changed_records'])==16
    assert negative['negative_count']==len(negative['cases'])==14 and negative['all_changed_inputs_distinct_andexpected_semantic_guards_match'] and negative['all_protected_files_ROMs_registry_ledger_pins_andmodules_hash_exact']
    assert all(c['rejected'] and c['commit_calls']==0 and c['actual_changed_input'] and c['original_object_files_components_andserialized_bytes_unchanged'] for c in negative['cases'])
    assert binding['all515_prior_dependencies_preserved'] and binding['current_dependency_count']==524 and binding['new_builder_rejections']==16
    verified=read('work/analysis/editorial_handoff_verification_v8430/verified_handoff.json');assert verified['candidate_sha256']==conf['parent_ROM_sha256']==sha(PARENT.read_bytes()) and sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp=Path('translations/release_stack.json');raw=rp.read_bytes();registry=read(rp);before=BUILDER.read_bytes();digest=guard['full_original_source_inverse_sha256'];anchor='    # Lexically valid "% o"'
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==642 and before.count(STAGE_V3.encode())==1 and before.count(anchor.encode())==1 and STAGE_B49_V2.encode() not in before
    after=checked_text(before.decode('utf8'),{STAGE_V3:STAGE_V5,anchor:STAGE_B49_V2+anchor}).encode('utf8')
    assert sha(after)==guard['planned_builder_sha256'] and after==Path('work/analysis/Hodram_B49_builder_v8452/planned_builder.bin').read_bytes()
    assert after.replace(STAGE_B49_V2.encode(),b'',1).replace(STAGE_V5.encode(),STAGE_V3.encode(),1)==before and validate_builder_bytes(after,digest)['corrected_B49_stage_version']==2
    profile=deepcopy(registry['profiles']['all-routes-unified-v8377'])
    profile.update(status='experimental',hodram_outcomes_editorial='translations/hodram_outcomes_editorial_release_v5.json',hodram_B49_editorial=str(owned.CONFIG),
        description='Complete V8377 plus clean-Japanese whole-exchange Hodram SC1B49:14speeches/two typedchoices,seven revisions/nine justified retentions.',
        note='Natural-dialogue-v2 en-US;source-bound Lil/Hodram bargaining,New World hearsay,qualified denial,outgoing Heavenly Wristband notice anddistinct Ullr Bow item UI. Full216usable width/14single pages/complete characters/two source-qualified ellipsis forms/zero warnings orwaivers/seven infos. All36commands/14completepreambles/eightrelatives40cases/rawquery/two-choice22byte native menu/item148two layouts-hide waits/sevenopaque effects/fullterminal/tails preserved. Every clean/current block/archive/whole ROM inverse and324unowned blocks/allotherfiles/components exact. All325wholeloads650parentmodes326actions andshippedcallers bound. Actual69868frames/eight initialized whole/boundedtail/focusedFE runs:14unique speeches,bothchoices,200completeholds,12menubacking/24visiblelabel samples,four FEpalette/VRAM/RGBholds. All231laterRGBpairs recomputed;five visible differences,seven durationdifferences,boundary/final PRNG differences retained;rawcalendar uninterpreted. Not natural eventactivation,earned possession/trade eligibility,original location,fullroute/hardware/customname/everyframe/future-outcome/simulationequivalence. 838policyrejections/14atomicsemanticrejections/16changedbuilder checks;precedingV8377 byte-exact andallprior pins/50semanticcases/fouraliascases retained byexactsource equivalence. OnewholeNDScommit afterallgates. Fullfourstory/sharedtown-shop/random/Help/207names/earlierwrap goalactive;graphics/laterolder-recordtechnicalaudit separate. PreserveeveryROM/draft/failure/main4701;no promotion,separatepackage,pruning,commit orpush.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'planned_builder.bin').write_bytes(after);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and BUILDER.read_bytes()==before
    temporary=BUILDER.with_name('build_integrated_release_v8458.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,BUILDER)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    inverse=deepcopy(read(rp));inverse['profiles'].pop(PROFILE);assert inverse==registry and BUILDER.read_bytes()==after;owned.check_dependencies(conf)
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v8377',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=str(owned.CONFIG),release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts=conf['manuscripts'],registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(after),positive_proof=str(POSITIVE),positive_proof_sha256=sha(POSITIVE.read_bytes()),negative_proof=str(NEGATIVE),negative_proof_sha256=sha(NEGATIVE.read_bytes()),predecessor_binding=str(BINDING),predecessor_binding_sha256=sha(BINDING.read_bytes()),expected_manifest_batches=643,expected_accepted_layers=114,expected_registered_release_checks=18,expected_regressions=110,all_prior_profiles_andmainV4701_preserved=True,every_unowned_builder_byte_andprior_registry_value_inverts_exactly=True,cumulative_build_cleanpatch_ownstartup_andonceonlycredit_pending=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Registered experimental V8459 aftercompleteV8377;expected643batches/114accepted. Exactprior builder andallprofiles recover. No build,promotion orcredit yet.')
