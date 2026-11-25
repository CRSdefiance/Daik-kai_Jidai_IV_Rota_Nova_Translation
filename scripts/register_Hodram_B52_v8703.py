"""Register B52 after the entire verified V8609 prefix using the shared late hook."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import hodram_B52_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v8 import BUILDER,validate_builder_bytes
from scripts.Hodram_B52_release_paths_v8693 import PARENT,ROM,DOC
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_registration_v8703')
PROFILE='all-routes-unified-v8704'
CONFIG=Path('translations/hodram_B52_editorial_release_v3.json')
BINDING=Path('work/analysis/Hodram_B52_integration_binding_v8699/integration_binding.json')
SUPPORT=Path('work/analysis/Hodram_B52_builder_support_v8694b')

if __name__=='__main__':
    assert not ROOT.exists();binding=read(BINDING);conf=read(CONFIG);owned.check_dependencies(conf)
    assert binding['configuration_sha256']==sha(CONFIG.read_bytes()) and binding['lifecycle_reports_value_equal'] and binding['whole_registered_V8609_prefix_reproduced_withall_guards']
    assert (binding['genuine_wrong_memory_cases'],binding['semantic_zero_commit_cases'],binding['shared_zero_commit_cases'],binding['builder_changed_input_cases'])==(3,16,6,29)
    verified=read('work/analysis/editorial_handoff_verification_v8687/verified_handoff.json')
    assert verified['candidate_sha256']==conf['parent_ROM_sha256']==sha(PARENT.read_bytes())
    assert verified['ledger_sha256']==sha(Path('translations/editorial_review_current_v1.json').read_bytes())
    source=read(SUPPORT/'source_equivalence.json');before=BUILDER.read_bytes();after=(SUPPORT/'builder.planned.py').read_bytes()
    assert before==(SUPPORT/'builder.before.py').read_bytes() and sha(after)==source['builder_planned_sha256']
    assert validate_builder_bytes(after,source['original_frozen_builder_digest'])['shared_late_editorial_hook_present']
    rp=Path('translations/release_stack.json');raw=rp.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==645
    adapter=Path('dk4tool/patch/hodram_b52_extension_v2.py')
    spec=dict(id='hodram-b52',module='dk4tool.patch.hodram_b52_extension_v2',module_sha256=sha(adapter.read_bytes()),config=str(CONFIG),
         config_sha256=sha(CONFIG.read_bytes()),parent_ROM_sha256=sha(PARENT.read_bytes()),target_ROM_sha256=sha(ROM.read_bytes()))
    profile=deepcopy(registry['profiles']['all-routes-unified-v8609'])
    assert not profile.get('late_editorial_extensions')
    profile.update(status='experimental',hodram_outcomes_editorial='translations/hodram_outcomes_editorial_release_v8.json',
        hodram_B49_editorial='translations/hodram_B49_editorial_release_v6.json',hodram_B50_editorial='translations/hodram_B50_editorial_release_v3.json',
        hodram_B51_editorial='translations/hodram_B51_editorial_release_v2.json',late_editorial_extensions=[spec],
        description='Complete V8609 plus clean-Japanese whole-exchange Hodram SC1B52: three speeches and two typed choices, two revisions and three justified retentions.',
        note='Natural-dialogue-v2 en-US. Preserve intention to oppose Hayreddin\'s outfit, gruff warning and dangerous-boldness idiom without invented kinship or rank. Scoped Port Worker and mentioned Hayreddin surname component retained; wider207-name review remains open. All14commands/3fullpreambles/4relatives/2choices/4opaquecontrols/normal-preserving andflagged-clearing ends retained;full216px automatic wrapping,one info,zero warnings/waivers. Six initialized cold boots50406frames/138complete body-name holds/12page occurrences show all3unique speeches andboth choices/end kinds. Twelve actual menu samples/24captions prove visibleglyphs/centering/highlights;nativebackingbounds remainoffline,no actualowner/RAM/VRAM/palette/backingbyteidentity orcancelavailability claim. Longwithdrawal differs incomponents/actors/calendar/PRNG/46of93laterRGBpairs;longopposition matchescomponents/actors butdiffersinPRNG/13of93RGBpairs. Focusedwithdrawal withunchangedinputprefix matches sampled finalcomponents/actors/seed/calendar/all13laterRGBpairs. Preserve boundarytiming/RNG andfollowingcommands;no causal,future simulation,naturalactivation/originallocation/earnedprogress/fullroute/hardware claim. Sourcecontrols8620 usedV8543;completecode/COMMON/font/EV1/actors equal andfreshownV8609 consumers revalidated,wholeRAMsnapshotsdiffer,no historicaloverlay. Frozen compiler/native policy andall independent readers pass340 changed-input checks. Both atomiclifecycles onecompleteNDScommit/exactreference,3wrongmemory/16semantic/6sharedhook failures leaveinputsunchanged. Sharedbuilder5positive/29negative cases retainentireoldbuilderinverse;compatibleprefix reproduceswholeV8609. Fullfourstory/earlierdialogue/sharedtown-shop/random/Help/remainingprose/207names/retrospectivewrap goalactive. Graphics/laterolder-recordtechnicalaudit separate. PreserveallROMs/drafts/failures/main4701;no promotion,separatepackage,pruning,commitorpush.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'planned_builder.bin').write_bytes(after);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and BUILDER.read_bytes()==before
    temporary=BUILDER.with_name('build_integrated_release_v8703.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,BUILDER)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==registry and BUILDER.read_bytes()==after;owned.check_dependencies(conf)
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v8609',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=str(CONFIG),release_config_sha256=sha(CONFIG.read_bytes()),manuscripts=[str(DOC)],extension_spec=spec,
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(after),
        integration_binding=str(BINDING),integration_binding_sha256=sha(BINDING.read_bytes()),
        expected_manifest_batches=646,expected_accepted_layers=114,expected_registered_release_checks=18,expected_regressions=110,
        all_prior_profiles_andmainV4701_preserved=True,whole_original_builder_inverse_andevery_prior_registry_value_exact=True,
        cumulative_build_cleanpatch_ownstartup_andonceonlycredit_pending=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Registered experimentalV8704 afterwholeV8609 through shared late hook;646batches/114accepted expected. Full oldbuilder/registry inverse retained. No ROMbuild/promotion/credit yet.')
