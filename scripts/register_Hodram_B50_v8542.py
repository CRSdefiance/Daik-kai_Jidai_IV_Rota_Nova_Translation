"""Register B50 cumulatively after complete V8475 with exact prior builder/registry inverse."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import hodram_B50_editorial_v1 as owned
from dk4tool.patch.hodram_outcomes_builder_guard_v6 import BUILDER,STAGE_V5,STAGE_B49_V2,STAGE_V6,STAGE_B49_V3,STAGE_B50,validate_builder_bytes
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.Hodram_B50_release_paths_v8537 import PARENT,CONFIG
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_registration_v8542')
PROFILE='all-routes-unified-v8543'
BINDING=Path('work/analysis/Hodram_B50_atomic_binding_v8541/semantic_binding.json')
GUARD=Path('work/analysis/Hodram_B50_builder_validation_v8535/exact_builder_inverse_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();binding,guard=map(read,[BINDING,GUARD]);conf=read(CONFIG);owned.check_dependencies(conf)
    assert binding['both_input_lifecycles_one_complete_commit_exact_reference'] and binding['all16_actually_changed_semantic_precommit_cases_rejected_without_mutation']
    assert binding['configuration_sha256']==sha(CONFIG.read_bytes()) and binding['atomic_module_sha256']==sha(Path(owned.__file__).read_bytes())
    verified=read('work/analysis/editorial_handoff_verification_v8533/verified_handoff.json');assert verified['candidate_sha256']==conf['parent_ROM_sha256']==sha(PARENT.read_bytes())
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp=Path('translations/release_stack.json');raw=rp.read_bytes();registry=read(rp);before=BUILDER.read_bytes();digest=guard['full_original_source_inverse_sha256']
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==643 and sha(before)==guard['current_builder_sha256']
    after=checked_text(before.decode('utf-8'),{STAGE_V5:STAGE_V6,STAGE_B49_V2:STAGE_B49_V3+STAGE_B50}).encode('utf-8')
    assert sha(after)==guard['planned_builder_sha256'] and after==Path('work/analysis/Hodram_B50_builder_validation_v8535/planned_builder.bin').read_bytes()
    inverse=after.replace(STAGE_B50.encode(),b'',1).replace(STAGE_V6.encode(),STAGE_V5.encode(),1).replace(STAGE_B49_V3.encode(),STAGE_B49_V2.encode(),1)
    assert inverse==before and validate_builder_bytes(after,digest)['B50_additive_stage_present']
    profile=deepcopy(registry['profiles']['all-routes-unified-v8475'])
    profile.update(status='experimental',hodram_outcomes_editorial='translations/hodram_outcomes_editorial_release_v6.json',hodram_B49_editorial='translations/hodram_B49_editorial_release_v4.json',hodram_B50_editorial=str(CONFIG),
        description='Complete V8475 plus clean-Japanese whole-exchange Hodram SC1B50:three speeches/system notices,two revisions andone justified retention.',
        note='Natural-dialogue-v2 en-US. Retain eager brought-it request;restore delighted confirmation,gift gesture,cheer/farewell andexplicit outgoing Heavenly Wristband handover. All12commands/3fullpreambles/zero relative-query-menu sites/6opaque effects/item148layout0 show-hide/fullend/tails preserved. Full216usablewidth/3singlepages/completecharacters/3infos/zero warnings orwaivers. Allsource/current/finalrefs,whole inverses and324unownedblocks/files/components exact. 325loads/650parentmodes/326actions/shippedcallers bound. Two initialized actual runs20002frames/sixpageoccurrences/50completeholds/twoFEpaints/six same-run VRAMpaletteRGBholds,including originalFE-before6302 absentheader/portrait anddistinct bow UI. Two one-frame speech-duration differences,no measured boundaryPRNG/UIrequest differences,final PRNGseeds differ,4of89laterRGBpairs differ;five checkedcomponents/actors match;rawcalendar uninterpreted. No natural activation,earned inventory,original location,fullroute,hardware,customnames,everyframe causality,future-random-outcome orbroadsimulation claim. 182policyrejections,16atomicsemanticfailures,16changedbuilder checks;bothatomic lifecycles pass. Compatible priorstages reproduce fullV8475 exactly withallprior dependencies retained. WholeNDScommit onlyafterallgates. Fullfourstory/sharedtown-shop/random/Help/207names/retrospectivewrap goalactive;graphics/laterolder-recordtechnicalaudit separate. PreserveeveryROM/draft/failure/main4701;no promotion,separatepackage,pruning,commit orpush.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'planned_builder.bin').write_bytes(after);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and BUILDER.read_bytes()==before
    temporary=BUILDER.with_name('build_integrated_release_v8542.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,BUILDER)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and BUILDER.read_bytes()==after;owned.check_dependencies(conf)
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v8475',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=str(CONFIG),release_config_sha256=sha(CONFIG.read_bytes()),manuscripts=conf['manuscripts'],registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(after),atomic_binding=str(BINDING),atomic_binding_sha256=sha(BINDING.read_bytes()),guard_validation=str(GUARD),guard_validation_sha256=sha(GUARD.read_bytes()),expected_manifest_batches=644,expected_accepted_layers=114,expected_registered_release_checks=18,expected_regressions=110,all_prior_profiles_andmainV4701_preserved=True,every_unowned_builder_byte_andprior_registry_value_inverts_exactly=True,cumulative_build_cleanpatch_ownstartup_andonceonlycredit_pending=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Registered experimental V8543 aftercompleteV8475;expected644batches/114accepted.Exactprior builder/allprofiles recover.No build,promotion orcredit yet.')
