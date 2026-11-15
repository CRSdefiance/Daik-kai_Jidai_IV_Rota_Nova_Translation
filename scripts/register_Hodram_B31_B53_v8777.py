"""Register B52 after the entire verified V8609 prefix using the shared late hook."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import hodram_B31_B53_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v8 import BUILDER,validate_builder_bytes
from scripts.Hodram_B31_B53_release_paths_v8767 import PARENT,ROM,DOC
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B31_B53_registration_v8777')
PROFILE='all-routes-unified-v8778'
CONFIG=Path('translations/hodram_B31_B53_editorial_release_v2.json')
BINDING=Path('work/analysis/Hodram_B31_B53_integration_binding_v8776/integration_binding.json')
SUPPORT=Path('work/analysis/Hodram_B52_builder_support_v8694b')

if __name__=='__main__':
    assert not ROOT.exists();binding=read(BINDING);conf=read(CONFIG);owned.check_dependencies(conf)
    assert binding['configuration_sha256']==sha(CONFIG.read_bytes()) and binding['lifecycle_reports_value_equal'] and binding['entire_verified_registered_V8704_prefix_preserved']
    assert (binding['genuine_wrong_memory_cases'],binding['semantic_zero_commit_cases'],binding['shared_zero_commit_cases'],binding['unchanged_builder_changed_input_cases_reused'])==(3,4,1,29)
    verified=read('work/analysis/editorial_handoff_verification_v8775/verified_handoff.json')
    assert verified['candidate_sha256']==conf['parent_ROM_sha256']==sha(PARENT.read_bytes())
    assert verified['ledger_sha256']==sha(Path('translations/editorial_review_current_v1.json').read_bytes())
    source=read(SUPPORT/'source_equivalence.json');before=BUILDER.read_bytes();after=before
    assert before==(SUPPORT/'builder.planned.py').read_bytes() and sha(before)==source['builder_planned_sha256']
    assert validate_builder_bytes(before,source['original_frozen_builder_digest'])['shared_late_editorial_hook_present']
    rp=Path('translations/release_stack.json');raw=rp.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==646
    adapter=Path('dk4tool/patch/hodram_b31_b53_extension_v2.py')
    spec=dict(id='hodram-b31-b53',module='dk4tool.patch.hodram_b31_b53_extension_v2',module_sha256=sha(adapter.read_bytes()),config=str(CONFIG),
         config_sha256=sha(CONFIG.read_bytes()),parent_ROM_sha256=sha(PARENT.read_bytes()),target_ROM_sha256=sha(ROM.read_bytes()))
    profile=deepcopy(registry['profiles']['all-routes-unified-v8704'])
    assert len(profile['late_editorial_extensions'])==1 and profile['late_editorial_extensions'][0]['target_ROM_sha256']==sha(PARENT.read_bytes())
    old_extensions=deepcopy(profile['late_editorial_extensions'])
    profile.update(status='experimental',late_editorial_extensions=old_extensions+[spec],
        description='Complete V8704 plus clean-Japanese contextual Hodram SC1 B31/B53: three revisions, preserving speaker agency and wanted-status meaning.',
        note=profile.get('note','')+' B31/B53: natural-dialogue-v2 en-US; all five individual gates, full216px automatic pages2/4/3rows, zero warnings orwaivers. Preserve all18 original commands/3preambles/4relatives/1rawquery/8opaquecontrols/2normalends. Source52->31->53 dependencies do not establish continuity, location, earned chronology, B52choice effects orunnamed-man identity. Retain scoped Barbarossa Hayreddin/Fazul components and Port Worker role without invented ranks, kinship orhistory. Four whole-block coldboots24004frames/76body-name holds/fourpages observe long B31 andB53warning;short B31 remains offline-only. Normal returns[0,1]/[0,0] preserve existing resultword independently ofr3mode1. Three decodedlength differences retained;duration/UI/boundaryRNG/followingcommands, five finalcomponents/actors/captain1/calendar/seed3325064553 and68laterRGBpairs match inbounded fixtures. No natural activation/fullcatalogue/all207/customnames/future simulation/fullroute/hardware claim. All364 production negatives, both atomiclifecycles,3wrongmemory,4representative semantic andlate shared target failure pass. Every prior profile, accepted layer, builder byte, ROM andtranslation preserved;full editorial objective active,graphics/laterolder-record audit separate.')
    assert all(profile[k]==v for k,v in registry['profiles']['all-routes-unified-v8704'].items() if k not in ['status','late_editorial_extensions','description','note'])
    assert profile['late_editorial_extensions'][:-1]==registry['profiles']['all-routes-unified-v8704']['late_editorial_extensions']
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'planned_builder.bin').write_bytes(after);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and BUILDER.read_bytes()==before
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==registry and BUILDER.read_bytes()==after;owned.check_dependencies(conf)
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v8704',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=str(CONFIG),release_config_sha256=sha(CONFIG.read_bytes()),manuscripts=[str(DOC)],extension_spec=spec,
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(after),
        integration_binding=str(BINDING),integration_binding_sha256=sha(BINDING.read_bytes()),
        expected_manifest_batches=647,expected_accepted_layers=114,expected_registered_release_checks=18,expected_regressions=110,
        all_prior_profiles_andmainV4701_preserved=True,whole_original_builder_inverse_andevery_prior_registry_value_exact=True,
        cumulative_build_cleanpatch_ownstartup_andonceonlycredit_pending=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Registered experimentalV8778 aftercompleteV8704;647batches/114accepted expected. Prior B52 extension andevery builder byte unchanged;whole registry inverse retained. No ROMbuild/promotion/credit yet.')
