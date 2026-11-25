"""Register B51 cumulatively after complete V8543 with exact prior builder/registry inverse."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import hodram_B51_editorial_v1 as owned
from dk4tool.patch.hodram_outcomes_builder_guard_v7 import BUILDER,STAGE_V6,STAGE_B49_V3,STAGE_B50,STAGE_V7,STAGE_B49_V4,STAGE_B50_V2,STAGE_B51,validate_builder_bytes
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.Hodram_B51_release_paths_v8595 import PARENT,CONFIG
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B51_registration_v8608')
PROFILE='all-routes-unified-v8609'
BINDING=Path('work/analysis/Hodram_B51_atomic_binding_v8606/semantic_binding.json')
GUARD=Path('work/analysis/Hodram_B51_builder_validation_v8596/exact_builder_inverse_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();binding,guard=map(read,[BINDING,GUARD]);conf=read(CONFIG);owned.check_dependencies(conf)
    assert binding['both_input_lifecycles_one_complete_commit_exact_reference'] and binding['all17_actually_changed_semantic_precommit_cases_rejected_without_mutation'] and binding['all3_genuine_wrong_memory_inputs_rejected_withall_guards_active'] and binding['lifecycle_reports_value_equal']
    assert binding['configuration_sha256']==sha(CONFIG.read_bytes()) and binding['atomic_module_sha256']==sha(Path(owned.__file__).read_bytes())
    verified=read('work/analysis/editorial_handoff_verification_v8601/verified_handoff.json');assert verified['candidate_sha256']==conf['parent_ROM_sha256']==sha(PARENT.read_bytes())
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp=Path('translations/release_stack.json');raw=rp.read_bytes();registry=read(rp);before=BUILDER.read_bytes();digest=guard['full_original_source_inverse_sha256']
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==644 and sha(before)==guard['current_builder_sha256']
    after=checked_text(before.decode('utf-8'),{STAGE_V6:STAGE_V7,STAGE_B49_V3:STAGE_B49_V4,STAGE_B50:STAGE_B50_V2+STAGE_B51}).encode('utf-8')
    assert sha(after)==guard['planned_builder_sha256'] and after==Path('work/analysis/Hodram_B51_builder_validation_v8596/planned_builder.bin').read_bytes()
    inverse=after.replace(STAGE_B51.encode(),b'',1).replace(STAGE_V7.encode(),STAGE_V6.encode(),1).replace(STAGE_B49_V4.encode(),STAGE_B49_V3.encode(),1).replace(STAGE_B50_V2.encode(),STAGE_B50.encode(),1)
    assert inverse==before and validate_builder_bytes(after,digest)['B51_additive_stage_present']
    profile=deepcopy(registry['profiles']['all-routes-unified-v8543'])
    profile.update(status='experimental',hodram_outcomes_editorial='translations/hodram_outcomes_editorial_release_v7.json',hodram_B49_editorial='translations/hodram_B49_editorial_release_v5.json',hodram_B50_editorial='translations/hodram_B50_editorial_release_v2.json',hodram_B51_editorial=str(CONFIG),
        description='Complete V8543 plus clean-Japanese whole-exchange Hodram SC1B51: five speeches, four revisions and one justified retention.',
        note='Natural-dialogue-v2 en-US. Restore gruff southern Mediterranean warning, complete Hodram clarification, unnamed bad-news description and well-meant self-preservation advice; preserve conditional Charles echo and unresolved private Gerhard suspicion. No invented identity, rulership, rank, gender, kinship, crime or supernatural fact. Scoped Hodram/Joakim, Gerhard Adernkatz, Charles/Jean and Port Worker names retained; no all207-name credit. All20commands/5fullpreambles/8relatives/2queries/4opaquecontrols/fullend/tails and325loads/650modes/326actions/shippedcallers bound. Original216px width/five English singlepages/complete characters/two line-count infos/zero warnings orwaivers. Two initialized actual entry fixtures20002frames/eight pageoccurrences/56completeholds show four speeches perlanguage; CharlesR32 remains offline-tested and unvisited. Normalends4736/4734 carry[0,0];two shortduration differences,13timing/length rows differ;no sampled boundaryPRNG/UIrequest differences,finalseeds differ,3of89laterRGBpairs differ. Five sampled components/wholeactors/captain1 match;rawcalendar uninterpreted. No naturalactivation,original location,earned inventory,customnames,fullroute,hardware,everyframe causality,futurePRNGoutcomes orbroadsimulation claim. Frozenpolicy322 rejections,17atomicsemanticfailures,3genuinewrongmemory failures,25changedbuilder rejections;two atomiclifecycle reports equal/onewholeNDScommit each. Compatible predecessors reproduce entireV8543 exactly retaining535/675/756prior dependencies. Fullfourstory/earlierdialogue/sharedtown-shop/random/Help/remainingprose/207names/retrospectivewrap goalactive. Graphics/laterolder-recordtechnicalaudit separate;preserveallROMs/drafts/failures/main4701. No promotion,separatepackage,pruning,commit orpush.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'planned_builder.bin').write_bytes(after);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and BUILDER.read_bytes()==before
    temporary=BUILDER.with_name('build_integrated_release_v8608.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,BUILDER)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and BUILDER.read_bytes()==after;owned.check_dependencies(conf)
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v8543',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=str(CONFIG),release_config_sha256=sha(CONFIG.read_bytes()),manuscripts=conf['manuscripts'],registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(after),atomic_binding=str(BINDING),atomic_binding_sha256=sha(BINDING.read_bytes()),guard_validation=str(GUARD),guard_validation_sha256=sha(GUARD.read_bytes()),expected_manifest_batches=645,expected_accepted_layers=114,expected_registered_release_checks=18,expected_regressions=110,all_prior_profiles_andmainV4701_preserved=True,every_unowned_builder_byte_andprior_registry_value_inverts_exactly=True,cumulative_build_cleanpatch_ownstartup_andonceonlycredit_pending=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Registered experimental V8609 aftercompleteV8543;expected645batches/114accepted.Exactprior builder/allprofiles recover.No build,promotion orcredit yet.')
