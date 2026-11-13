"""Register B54-B60 after the entire verified V8778 prefix using the shared late hook."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import hodram_B54_B60_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v8 import BUILDER,validate_builder_bytes
from scripts.Hodram_B54_B60_release_paths_v8853 import PARENT,ROM,DOC
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_registration_v8864')
PROFILE='all-routes-unified-v8865'
CONFIG=Path('translations/hodram_B54_B60_editorial_release_v2.json')
BINDING=Path('work/analysis/Hodram_B54_B60_integration_binding_v8863/integration_binding.json')
SUPPORT=Path('work/analysis/Hodram_B52_builder_support_v8694b')

if __name__=='__main__':
    assert not ROOT.exists();binding=read(BINDING);conf=read(CONFIG);owned.check_dependencies(conf)
    assert binding['configuration_sha256']==sha(CONFIG.read_bytes()) and binding['lifecycle_reports_value_equal'] and binding['entire_verified_registered_V8778_prefix_preserved']
    assert (binding['genuine_wrong_memory_cases'],binding['semantic_zero_commit_cases'],binding['shared_zero_commit_cases'],binding['unchanged_builder_changed_input_cases_reused'])==(3,4,1,29)
    verified=read('work/analysis/Hodram_B54_B60_checkpoint_v8861/verified_handoff_v8862.json')
    assert verified['candidate_sha256']==conf['parent_ROM_sha256']==sha(PARENT.read_bytes())
    assert verified['ledger_sha256']==sha(Path('translations/editorial_review_current_v1.json').read_bytes())
    source=read(SUPPORT/'source_equivalence.json');before=BUILDER.read_bytes();after=before
    assert before==(SUPPORT/'builder.planned.py').read_bytes() and sha(before)==source['builder_planned_sha256']
    assert validate_builder_bytes(before,source['original_frozen_builder_digest'])['shared_late_editorial_hook_present']
    rp=Path('translations/release_stack.json');raw=rp.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==647
    adapter=Path('dk4tool/patch/hodram_b54_b60_extension_v1.py')
    spec=dict(id='hodram-b54-b60',module='dk4tool.patch.hodram_b54_b60_extension_v1',module_sha256=sha(adapter.read_bytes()),config=str(CONFIG),
         config_sha256=sha(CONFIG.read_bytes()),parent_ROM_sha256=sha(PARENT.read_bytes()),target_ROM_sha256=sha(ROM.read_bytes()))
    profile=deepcopy(registry['profiles']['all-routes-unified-v8778'])
    assert len(profile['late_editorial_extensions'])==2 and profile['late_editorial_extensions'][-1]['target_ROM_sha256']==sha(PARENT.read_bytes())
    old_extensions=deepcopy(profile['late_editorial_extensions'])
    profile.update(status='experimental',late_editorial_extensions=old_extensions+[spec],
        description='Complete V8778 plus clean-Japanese whole-exchange Hodram SC1B54-B60:82 reviewed speeches,46 revisions and36 justified retentions.',
        note=profile.get('note','')+' B54-B60: natural-dialogue-v2 en-US; all five per-record gates,exact source/current/final refs,full216px automatic wrapping,85 English pages including3 two-page speeches andone distinct FE panel. Preserve152 commands/82 sixbyte preambles/24 relatives/6 unforced queries/33 nonprose controls/7 full normal ends andseparate tails. All9 production groups/886 semantic rejections,2 atomic lifecycles,3 wrongmemory,4 precommit semantic andone shared late-target rejection pass.14 saved initialized whole-scene runs130014frames/676 complete holds/150 page occurrences observe63 unique speeches;B55 and18 B58 conditionals remain offline. Two actual FEpaint contexts/sixheld bitmaps/palettes/VRAM/RGB andabsentnameplate are bound.335 later RGBpairs,14 final snapshots and81 own-language prefixcallbacks are independently compared. Retain every timing,decodedlength,RNG,RGB,followingcommand andlongB60 persistent actor difference. Focused7001 equality is bounded andRNG/11laterRGBpairs still differ. No immediate-return mainRAM,causal diagnosis,natural activation,earned chronology,fullcatalogue/all207/customnames,future-equivalence,fullroute orhardware claim. Geronimo/Alonso sharedde/fullname lead remains open. Every earlier profile,accepted layer,builder byte,ROM andtranslation is preserved;full editorial objective active,graphics andlater older-record audit separate.')
    assert all(profile[k]==v for k,v in registry['profiles']['all-routes-unified-v8778'].items() if k not in ['status','late_editorial_extensions','description','note'])
    assert profile['late_editorial_extensions'][:-1]==registry['profiles']['all-routes-unified-v8778']['late_editorial_extensions']
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'planned_builder.bin').write_bytes(after);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and BUILDER.read_bytes()==before
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==registry and BUILDER.read_bytes()==after;owned.check_dependencies(conf)
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v8778',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=str(CONFIG),release_config_sha256=sha(CONFIG.read_bytes()),manuscripts=[str(DOC)],extension_spec=spec,
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(after),
        integration_binding=str(BINDING),integration_binding_sha256=sha(BINDING.read_bytes()),
        expected_manifest_batches=648,expected_accepted_layers=114,expected_registered_release_checks=18,expected_regressions=110,
        all_prior_profiles_andmainV4701_preserved=True,whole_original_builder_inverse_andevery_prior_registry_value_exact=True,
        cumulative_build_cleanpatch_ownstartup_andonceonlycredit_pending=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Registered experimentalV8865 aftercompleteV8778;648batches/114accepted expected. Prior B52/B31-B53 extensions andevery builder byte unchanged;whole registry inverse retained. No ROMbuild/promotion/credit yet.')
