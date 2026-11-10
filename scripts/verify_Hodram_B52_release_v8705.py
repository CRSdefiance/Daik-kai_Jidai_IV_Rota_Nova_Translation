"""Verify registered B52 cumulative output, complete stack and exact clean-input patch."""
import json,os
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.patch.hodram_outcomes_builder_guard_v7 import STAGE_V7,STAGE_B49_V4,STAGE_B50_V2,STAGE_B51
from dk4tool.patch.hodram_outcomes_builder_guard_v8 import STAGE_V8,STAGE_B49_V5,STAGE_B50_V3,STAGE_B51_V2,BUILDER_STAGE,validate_builder_bytes
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_release_v8705')
ROM=Path('out/all_routes_combined_v8704_candidate.nds')
OLD=Path('out/all_routes_combined_v8609_candidate.nds')
CONFIG=Path('translations/hodram_B52_editorial_release_v3.json')
REG=Path('work/analysis/Hodram_B52_registration_v8703')
POSITIVE=Path('work/analysis/Hodram_B52_atomic_positive_v8690b/atomic_positive.json')
PATH='/data/SC1.DK4'

if __name__=='__main__':
    assert not ROOT.exists()
    registration=read(REG/'registration_receipt.json');build=read('work/analysis/Hodram_B52_build_v8704/build_terminal.json');tests=read('work/analysis/Hodram_B52_regressions_v8704/terminal.json')
    assert build['terminal'] and build['returncode']==0 and tests['terminal'] and tests['returncode']==0
    assert '110 passed' in Path(tests['log']).read_text(encoding='utf-8') and sha(Path(tests['log']).read_bytes())==tests['log_sha256']
    conf=read(CONFIG);manifest=read(ROM.with_suffix('.manifest.json'));prior=read(OLD.with_suffix('.manifest.json'));registry=read('translations/release_stack.json')
    assert manifest['profile']==registration['profile']=='all-routes-unified-v8704'
    assert manifest['candidate_sha256']==sha(ROM.read_bytes())==conf['reference_ROM_sha256']
    assert manifest['base_sha256']==conf['canonical_ROM_sha256'] and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())==registration['registry_after_sha256']
    assert len(manifest['batches'])==registration['expected_manifest_batches']==646 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    inverse=deepcopy(registry);profile=inverse['profiles'].pop(manifest['profile']);assert inverse==read(REG/'release_stack.before.json')
    oldprofile=deepcopy(registry['profiles']['all-routes-unified-v8609']);newprofile=deepcopy(profile)
    for p in [oldprofile,newprofile]:p.pop('description',None);p.pop('note',None)
    assert newprofile.pop('late_editorial_extensions')==[registration['extension_spec']]
    for key,old,new in [('hodram_outcomes_editorial','hodram_outcomes_editorial_release_v7','hodram_outcomes_editorial_release_v8'),
                        ('hodram_B49_editorial','hodram_B49_editorial_release_v5','hodram_B49_editorial_release_v6'),
                        ('hodram_B50_editorial','hodram_B50_editorial_release_v2','hodram_B50_editorial_release_v3'),
                        ('hodram_B51_editorial','hodram_B51_editorial_release_v1','hodram_B51_editorial_release_v2')]:
        assert Path(oldprofile.pop(key)).as_posix()=='translations/'+old+'.json' and Path(newprofile.pop(key)).as_posix()=='translations/'+new+'.json'
    assert oldprofile==newprofile
    norm=lambda value:str(value).replace('\\','/')
    assert [norm(p) for p in manifest['batches']]==[norm(p) for p in prior['batches']]+[norm(p) for p in conf['manuscripts']]
    before,after=NdsImage.open(OLD),NdsImage.open(ROM)
    changedfiles=[p for _,p,v in before.iter_files() if after.read_file(p)!=v];changedcomponents=[p for p,v in before.iter_components() if after.read_file(p)!=v]
    assert changedfiles==[PATH] and changedcomponents==[] and ROM.read_bytes()==Path(conf['reference_ROM']).read_bytes()
    positive=read(POSITIVE);proof=positive['cases'][1]['report']
    assert positive['positive_lifecycles']==2 and positive['one_complete_NDS_commit_percase'] and len(proof['changed_records'])==5
    record=deepcopy(manifest['relocations'][PATH]['late_editorial:hodram-b52'])
    for key,value in [('extension_id','hodram-b52'),('module',registration['extension_spec']['module']),('module_sha256',registration['extension_spec']['module_sha256']),
                      ('release_config',str(CONFIG)),('release_config_sha256',sha(CONFIG.read_bytes())),('parent_ROM_sha256',sha(OLD.read_bytes())),('target_ROM_sha256',sha(ROM.read_bytes()))]:
        assert record.pop(key)==value,key
    assert record==proof and {r['id'] for r in proof['changed_records']}<=set(manifest['changed_records'][PATH])
    banks=[IlnkContainer.parse(i.read_file(PATH)).blocks for i in [before,after]]
    assert len(banks[0])==len(banks[1])==325 and [i for i,(a,b) in enumerate(zip(*banks,strict=True)) if a!=b]==[52]
    arm=after.read_file('/__arm9__.bin')
    assert arm==before.read_file('/__arm9__.bin') and sha(arm)=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b' and len(MainCodeFile(arm,0x02000000).sections[3].data)-48==123264
    builder=Path('scripts/build_integrated_release.py').read_bytes();oldbuilder=(REG/'build_integrated_release.py.before').read_bytes()
    guard=read('work/analysis/Hodram_B52_builder_validation_v8695/exact_builder_inverse_cases.json')
    restored=builder.replace(BUILDER_STAGE.encode(),b'',1)
    for new,old in [(STAGE_V8,STAGE_V7),(STAGE_B49_V5,STAGE_B49_V4),(STAGE_B50_V3,STAGE_B50_V2),(STAGE_B51_V2,STAGE_B51)]:restored=restored.replace(new.encode(),old.encode(),1)
    assert restored==oldbuilder and validate_builder_bytes(builder,guard['original_frozen_builder_digest'])['shared_late_editorial_hook_present']
    clean=Path(conf['clean_ROM']);clean_sha=sha(clean.read_bytes());assert clean_sha==conf['clean_ROM_sha256']
    patch=ROM.with_suffix('.xdelta');reconstructed=ROOT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
    assert not patch.exists() and not reconstructed.exists();ROOT.mkdir(parents=True)
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,reconstructed)
    assert reconstructed.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_sha
    pins=Path('translations/rom_retention_pins.json');pinbefore=pins.read_bytes();values=json.loads(pinbefore);original=deepcopy(values)
    for path,reason in [(ROM,'Registered cumulative B52 after wholeV8609;646batches/114accepted/18checks/110regressions;main4701 unchanged.'),
                        (reconstructed,'Exact clean-input patch reconstruction ofregisteredV8704;immutable byte-exact release evidence.')]:
        assert not any(Path(v['path']).resolve()==path.resolve() for v in values)
        values.append(dict(path=str(path.resolve()),reason=reason+' Preserve every ROM. SHA256 '+sha(path.read_bytes())))
    assert values[:-2]==original;encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    (ROOT/'pins.before.json').write_bytes(pinbefore);assert pins.read_bytes()==pinbefore
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'registered_release_verification.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),manifest=str(ROM.with_suffix('.manifest.json')),
        manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),profile=manifest['profile'],canonical_base=manifest['base_rom'],canonical_base_sha256=manifest['base_sha256'],
        manifest_batches=646,accepted_layers=114,release_checks=18,regressions=110,
        all646_manifest_batches_and114_accepted_layers_present=True,all18_registered_release_checks_pass=True,all110_release_dialogue_regressions_pass=True,
        all_prior_profiles_andmainV4701_preserved=True,file_changes=changedfiles,component_changes=changedcomponents,
        only_SC1_B52_change_324_otherblocks_andall_other_files_components_exact=True,whole_ROM_equals_pinned_approved_reference=True,
        atomic_positive_proof=str(POSITIVE),atomic_positive_proof_sha256=sha(POSITIVE.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(after.read_file('/COMMON/MESFILE.DK4')),
        story_hashes={f'SC{r}':sha(after.read_file(f'/data/SC{r}.DK4')) for r in range(4)},
        complete_ARM9_BSS_names_Blades_and123264_staged_payload_preserved=True,patch=str(patch),patch_sha256=sha(patch.read_bytes()),
        clean_input_sha256=clean_sha,exact_patch_reconstruction=str(reconstructed),whole_clean_input_ROM_reconstruction_byte_exact=True,
        pins_before_sha256=sha(pinbefore),pins_after_sha256=sha(encoded),all_prior_pins_preserved=True,
        verified_registration_receipt=str(REG/'registration_receipt.json'),verified_registration_receipt_sha256=sha((REG/'registration_receipt.json').read_bytes()),
        regressions_terminal_sha256=sha(Path('work/analysis/Hodram_B52_regressions_v8704/terminal.json').read_bytes()),
        actual_scope_limits=proof['actual_scope'],shared_extension_report_value_equal_to_qualified_atomic_report=True,
        own_registered_ROM_startup_andledger_completion_pending=True,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(candidate_sha256=sha(ROM.read_bytes()),patch_sha256=sha(patch.read_bytes()),batches=646,accepted=114,checks=18,regressions=110,exact_clean_patch=True),flush=True)
