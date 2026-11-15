"""Verify cumulative registered B49 output andexact clean-input reconstruction;preserve every artifact."""
import json,os
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import hodram_B49_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.patch.hodram_outcomes_builder_guard_v4 import STAGE_V3
from dk4tool.patch.hodram_outcomes_builder_guard_v5 import STAGE_V5,STAGE_B49_V2,validate_builder_bytes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_release_v8460')
ROM=Path('out/all_routes_combined_v8459_candidate.nds')
OLD=Path('out/all_routes_combined_v8377_candidate.nds')
REG=Path('work/analysis/Hodram_B49_registration_v8458')
POSITIVE=Path('work/analysis/Hodram_B49_atomic_positive_v8456/atomic_positive.json')
if __name__=='__main__':
    assert not ROOT.exists();registration=read(REG/'registration_receipt.json');build=read('work/analysis/Hodram_B49_build_v8459/build_terminal.json');tests=read('work/analysis/Hodram_B49_regressions_v8459/terminal.json')
    assert build['terminal'] and build['returncode']==0 and tests['terminal'] and tests['returncode']==0 and '110 passed' in Path(tests['log']).read_text('utf8') and sha(Path(tests['log']).read_bytes())==tests['log_sha256']
    conf=read(owned.CONFIG);manifest=read(ROM.with_suffix('.manifest.json'));prior=read(OLD.with_suffix('.manifest.json'));registry=read('translations/release_stack.json')
    assert manifest['profile']==registration['profile']=='all-routes-unified-v8459' and manifest['candidate_sha256']==sha(ROM.read_bytes())==conf['reference_ROM_sha256']
    assert manifest['base_sha256']==conf['canonical_ROM_sha256'] and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())==registration['registry_after_sha256']
    assert len(manifest['batches'])==registration['expected_manifest_batches']==643 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    inverse=deepcopy(registry);profile=inverse['profiles'].pop(manifest['profile']);assert inverse==read(REG/'release_stack.before.json')
    oldprofile=deepcopy(registry['profiles']['all-routes-unified-v8377']);newprofile=deepcopy(profile)
    for item in [oldprofile,newprofile]:item.pop('description',None);item.pop('note',None)
    assert newprofile.pop('hodram_B49_editorial')==str(owned.CONFIG) and newprofile.pop('hodram_outcomes_editorial')=='translations/hodram_outcomes_editorial_release_v5.json' and oldprofile.pop('hodram_outcomes_editorial')=='translations/hodram_outcomes_editorial_release_v3.json' and newprofile==oldprofile
    norm=lambda value:str(value).replace('\\','/')
    assert [norm(p) for p in manifest['batches']]==[norm(p) for p in prior['batches']]+[norm(p) for p in conf['manuscripts']]
    before,after=NdsImage.open(OLD),NdsImage.open(ROM);changedfiles=[p for _,p,v in before.iter_files() if after.read_file(p)!=v];changedcomponents=[p for p,v in before.iter_components() if after.read_file(p)!=v]
    assert changedfiles==[owned.PATH] and not changedcomponents and ROM.read_bytes()==Path(conf['reference_ROM']).read_bytes()
    positive=read(POSITIVE);proof=positive['report'];assert positive['one_complete_NDS_commit'] and len(proof['changed_records'])==16 and len(proof['files'])==1
    record=manifest['relocations'][owned.PATH]['hodram_B49_editorial'];assert record['proof']==proof and record['release_config_sha256']==sha(Path(owned.CONFIG).read_bytes())
    assert {r['id'] for r in proof['changed_records']}<=set(manifest['changed_records'][owned.PATH])
    banks=[IlnkContainer.parse(i.read_file(owned.PATH)).blocks for i in [before,after]];assert len(banks[0])==len(banks[1])==325 and [i for i,(a,b) in enumerate(zip(*banks,strict=True)) if a!=b]==[49]
    arm=after.read_file('/__arm9__.bin');assert arm==before.read_file('/__arm9__.bin') and sha(arm)=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b' and len(MainCodeFile(arm,0x02000000).sections[3].data)-48==123264
    builder=Path('scripts/build_integrated_release.py').read_bytes();oldbuilder=(REG/'build_integrated_release.py.before').read_bytes();guard=read('work/analysis/Hodram_B49_builder_v8452/exact_builder_inverse_cases.json')
    assert builder.count(STAGE_V5.encode())==builder.count(STAGE_B49_V2.encode())==1 and builder.replace(STAGE_B49_V2.encode(),b'',1).replace(STAGE_V5.encode(),STAGE_V3.encode(),1)==oldbuilder
    assert validate_builder_bytes(builder,guard['full_original_source_inverse_sha256'])['corrected_B49_stage_version']==2
    assert builder.index(STAGE_V5.encode())+len(STAGE_V5.encode())==builder.index(STAGE_B49_V2.encode()) and builder.index(STAGE_B49_V2.encode())+len(STAGE_B49_V2.encode())==builder.index(b'    # Lexically valid "% o"')
    clean=Path(conf['clean_ROM']);clean_sha=sha(clean.read_bytes());assert clean_sha==conf['clean_ROM_sha256'];patch=ROM.with_suffix('.xdelta');reconstructed=ROOT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
    assert not patch.exists() and not reconstructed.exists();ROOT.mkdir(parents=True);make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,reconstructed);assert reconstructed.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_sha
    pins=Path('translations/rom_retention_pins.json');pinbefore=pins.read_bytes();values=json.loads(pinbefore);original=deepcopy(values)
    for path,reason in [(ROM,'Registered cumulative B49 aftercompleteV8377;643manifest/114accepted/18checks/110regressions;main4701 unchanged.'),(reconstructed,'Exact clean-input patch reconstruction ofregistered V8459;immutable byte-exact release evidence.')]:
        assert not any(Path(v['path']).resolve()==path.resolve() for v in values);values.append(dict(path=str(path.resolve()),reason=reason+' Preserve every ROM. SHA256 '+sha(path.read_bytes())))
    assert values[:-2]==original;encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');(ROOT/'pins.before.json').write_bytes(pinbefore)
    assert pins.read_bytes()==pinbefore
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'registered_release_verification.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),manifest=str(ROM.with_suffix('.manifest.json')),manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),profile=manifest['profile'],canonical_base=manifest['base_rom'],canonical_base_sha256=manifest['base_sha256'],manifest_batches=643,accepted_layers=114,release_checks=18,regressions=110,all643_manifest_batches_and114_accepted_layers_present=True,all18_registered_release_checks_pass=True,all110_release_dialogue_regressions_pass=True,all_prior_profiles_andmainV4701_preserved=True,file_changes=changedfiles,component_changes=changedcomponents,only_SC1_B49_change_324_otherblocks_andall_other_files_components_exact=True,whole_ROM_equals_pinned_approved_reference=True,atomic_positive_proof=str(POSITIVE),atomic_positive_proof_sha256=sha(POSITIVE.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(after.read_file('/COMMON/MESFILE.DK4')),story_hashes={f'SC{r}':sha(after.read_file(f'/data/SC{r}.DK4')) for r in range(4)},complete_ARM9_BSS_names_Blades_and123264_staged_payload_preserved=True,patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=clean_sha,exact_patch_reconstruction=str(reconstructed),whole_clean_input_ROM_reconstruction_byte_exact=True,pins_before_sha256=sha(pinbefore),pins_after_sha256=sha(encoded),all_prior_pins_preserved=True,verified_registration_receipt=str(REG/'registration_receipt.json'),verified_registration_receipt_sha256=sha((REG/'registration_receipt.json').read_bytes()),regressions_terminal_sha256=sha(Path('work/analysis/Hodram_B49_regressions_v8459/terminal.json').read_bytes()),actual_scope_limits=proof['actual_scope'],own_registered_ROM_startup_andledger_completion_pending=True,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(candidate_sha256=sha(ROM.read_bytes()),patch_sha256=sha(patch.read_bytes()),batches=643,accepted=114,checks=18,regressions=110,exact_clean_patch=True),flush=True)
