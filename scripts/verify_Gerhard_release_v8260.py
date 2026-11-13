"""Verify complete registered ancestry, both owned changes and exact reconstruction from the clean ROM."""
import json,os
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch import gerhard_surname_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_surname_release_v8260')
ROM=Path('out/all_routes_combined_v8259_candidate.nds')
OLD=Path('out/all_routes_combined_v8172_candidate.nds')
REG=Path('work/analysis/Gerhard_surname_registration_v8258')
POSITIVE=Path('work/analysis/Gerhard_atomic_positive_v8256/one_whole_NDS_commit_exact_reference_andunchanged_precommit_input.json')
if __name__=='__main__':
    assert not ROOT.exists();registration=read(REG/'registration_receipt.json');build=read('work/analysis/Gerhard_surname_build_v8259/build_terminal.json');tests=read('work/analysis/Gerhard_surname_regressions_v8259/terminal.json')
    assert build['terminal'] and build['returncode']==0 and tests['terminal'] and tests['returncode']==0
    assert sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf8')
    conf=read(owned.CONFIG);manifest=read(ROM.with_suffix('.manifest.json'));prior=read(OLD.with_suffix('.manifest.json'));registry=read('translations/release_stack.json')
    assert manifest['profile']==registration['profile']=='all-routes-unified-v8259' and manifest['candidate_sha256']==sha(ROM.read_bytes())==conf['reference_ROM_sha256']
    assert manifest['base_sha256']==conf['canonical_ROM_sha256'] and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())==registration['registry_after_sha256']
    assert len(manifest['batches'])==registration['expected_manifest_batches']==640 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    restored=deepcopy(registry);profile=restored['profiles'].pop(manifest['profile']);assert restored==read(REG/'release_stack.before.json')
    previous=deepcopy(registry['profiles']['all-routes-unified-v8172']);new=deepcopy(profile)
    for v in [previous,new]:v.pop('description',None);v.pop('note',None)
    assert new.pop('gerhard_surname_editorial')==owned.CONFIG and previous==new
    normal=lambda p:str(p).replace('\\','/')
    assert [normal(p) for p in manifest['batches']]==[normal(p) for p in prior['batches']]+[normal(p) for p in conf['manuscripts']]
    before,after=NdsImage.open(OLD),NdsImage.open(ROM)
    changedfiles=[p for _,p,v in before.iter_files() if after.read_file(p)!=v];changedcomponents=[p for p,v in before.iter_components() if after.read_file(p)!=v]
    assert changedfiles==[owned.PATH] and changedcomponents==[owned.ARM] and ROM.read_bytes()==Path(conf['reference_ROM']).read_bytes()
    positive=read(POSITIVE);proof=positive['report'];assert positive['single_complete_NDS_commit'] and len(proof['changed_records'])==6
    for path in [owned.PATH,owned.ARM]:
        record=manifest['relocations'][path]['gerhard_surname_editorial']
        assert record['proof']==proof and record['release_config_sha256']==sha(Path(owned.CONFIG).read_bytes())
        expected={r['id'] for r in proof['changed_records'] if r['file_path']==path}
        assert expected<=set(manifest['changed_records'][path])
    oldblocks,newblocks=[IlnkContainer.parse(i.read_file(owned.PATH)).blocks for i in [before,after]]
    assert len(oldblocks)==len(newblocks)==336 and [i for i,(a,b) in enumerate(zip(oldblocks,newblocks,strict=True)) if a!=b]==[27,74]
    arm=after.read_file(owned.ARM);nameproof=owned.validate_name_transition(before.read_file(owned.ARM),arm)
    assert len(MainCodeFile(arm,0x02000000).sections[3].data)-48==123264
    builder=Path('scripts/build_integrated_release.py').read_bytes();stage=(REG/'builder.stage.bin').read_bytes()
    assert builder.count(stage)==1 and builder.replace(stage,b'',1)==(REG/'build_integrated_release.py.before').read_bytes()
    assert builder.index(b"profile_config.get('rafael_B50_editorial')")<builder.index(stage)<builder.index(b'    # Lexically valid')
    clean=Path(conf['clean_ROM']);clean_sha=sha(clean.read_bytes());assert clean_sha==conf['clean_ROM_sha256']
    patch=ROM.with_suffix('.xdelta');reconstructed=ROOT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
    assert not patch.exists() and not reconstructed.exists();ROOT.mkdir(parents=True)
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,reconstructed)
    assert reconstructed.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_sha
    pins=Path('translations/rom_retention_pins.json');pinbefore=pins.read_bytes();values=json.loads(pinbefore);original=deepcopy(values)
    for path,reason in [(ROM,'Registered cumulative Gerhard surname correction aftercompleteV8172;640manifest/114accepted/18checks/110regressions;main4701 unchanged.'),
                        (reconstructed,'Exact clean-input patch reconstruction ofregistered V8259;immutable byte-exact release evidence.')]:
        assert not any(Path(v['path']).resolve()==path.resolve() for v in values)
        values.append(dict(path=str(path.resolve()),reason=reason+' Preserve every ROM. SHA256 '+sha(path.read_bytes())))
    assert values[:-2]==original;encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');(ROOT/'pins.before.json').write_bytes(pinbefore)
    assert pins.read_bytes()==pinbefore
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'registered_release_verification.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),manifest=str(ROM.with_suffix('.manifest.json')),manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),
        profile=manifest['profile'],canonical_base=manifest['base_rom'],canonical_base_sha256=manifest['base_sha256'],manifest_batches=640,accepted_layers=114,release_checks=18,regressions=110,
        all640_manifest_batches_and114_accepted_layers_present=True,all18_registered_release_checks_pass=True,all110_release_dialogue_regressions_pass=True,
        all_prior_profiles_andmainV4701_preserved=True,file_changes=changedfiles,component_changes=changedcomponents,only_SC2_B27_B74_five_bodies_andARM9_owned12_name_changed=True,
        name_transition=nameproof,protected_Blades8_andall_pointerfields_unowned_bytes_exact=True,atomic_positive_proof=str(POSITIVE),atomic_positive_proof_sha256=sha(POSITIVE.read_bytes()),
        whole_ROM_equals_pinned_approved_reference=True,ARM9_sha256=sha(arm),COMMON_sha256=sha(after.read_file('/COMMON/MESFILE.DK4')),story_hashes={f'SC{r}':sha(after.read_file(f'/data/SC{r}.DK4')) for r in range(4)},
        all_native_shapes_BSS_and123264_staged_bytes_preserved=True,patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=clean_sha,
        exact_patch_reconstruction=str(reconstructed),whole_clean_input_ROM_reconstruction_byte_exact=True,pins_before_sha256=sha(pinbefore),pins_after_sha256=sha(encoded),all_prior_pins_preserved=True,
        registration_receipt_sha256=sha((REG/'registration_receipt.json').read_bytes()),verified_registration_receipt=str(REG/'registration_receipt.json'),verified_registration_receipt_sha256=sha((REG/'registration_receipt.json').read_bytes()),
        regressions_terminal_sha256=sha(Path('work/analysis/Gerhard_surname_regressions_v8259/terminal.json').read_bytes()),
        actual_scope_limits=proof['actual_scope'],own_registered_ROM_startup_andledger_overlay_pending=True,completion_credit_added=0,zero_duplicate_editorial_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(candidate_sha256=sha(ROM.read_bytes()),patch_sha256=sha(patch.read_bytes()),batches=640,accepted=114,checks=18,regressions=110,exact_clean_patch=True),flush=True)
