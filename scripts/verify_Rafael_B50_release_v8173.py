"""Verify all ancestry,production equality andan exactly reconstructed clean-input patch."""
import json,os
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch import rafael_B50_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_release_v8173')
ROM=Path('out/all_routes_combined_v8172_candidate.nds')
OLD=Path('out/all_routes_combined_v8122_candidate.nds')
REG=Path('work/analysis/Rafael_B50_registration_v8171')
if __name__=='__main__':
    assert not ROOT.exists();registration=read(REG/'registration_receipt.json');assert registration['negative_count']==479 and registration['expected_manifest_batches']==639;terminal=read('work/analysis/Rafael_B50_build_v8172/build_terminal.json')
    regressions=read('work/analysis/Rafael_B50_regressions_v8172/terminal.json')
    assert terminal['terminal'] and terminal['returncode']==0 and regressions['terminal'] and regressions['returncode']==0
    assert sha(Path(regressions['log']).read_bytes())==regressions['log_sha256'] and '110 passed' in Path(regressions['log']).read_text('utf8')
    registry=read('translations/release_stack.json');manifest=read(ROM.with_suffix('.manifest.json'));prior=read(OLD.with_suffix('.manifest.json'));conf=read(owned.CONFIG)
    digest=sha(ROM.read_bytes())
    assert manifest['profile']=='all-routes-unified-v8172' and manifest['candidate_sha256']==digest
    assert manifest['base_sha256']==conf['canonical_ROM_sha256'] and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==639 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    restored=deepcopy(registry);profile=restored['profiles'].pop(manifest['profile']);assert restored==read(REG/'release_stack.before.json')
    previous=deepcopy(registry['profiles']['all-routes-unified-v8122']);new=deepcopy(profile)
    for value in [previous,new]:value.pop('description',None);value.pop('note',None)
    assert new.pop('rafael_B50_editorial')==owned.CONFIG and previous==new
    normal=lambda p:str(p).replace('\\','/')
    assert [normal(p) for p in manifest['batches']]==[normal(p) for p in prior['batches']]+[normal(p) for p in conf['manuscripts']]
    before,after,reference=[NdsImage.open(p) for p in [OLD,ROM,conf['reference_ROM']]]
    changes=[p for _,p,v in before.iter_files() if after.read_file(p)!=v];components=[p for p,v in before.iter_components() if after.read_file(p)!=v]
    assert changes==[owned.PATH] and components==[] and ROM.read_bytes()==Path(conf['reference_ROM']).read_bytes()
    positive=read('work/analysis/Rafael_B50_atomic_positive_v8169/positive_reconstruction.json')
    record=manifest['relocations']['/data/SC0.DK4']['rafael_B50_editorial']
    assert record['proof']==positive and record['release_config_sha256']==sha(Path(owned.CONFIG).read_bytes())
    ids={r['id'] for r in positive['changed_records']};assert len(ids)==28 and ids<=set(manifest['changed_records']['/data/SC0.DK4'])
    a,b=[IlnkContainer.parse(im.read_file('/data/SC0.DK4')).blocks for im in [before,after]]
    assert len(a)==len(b)==343 and [i for i,(x,y) in enumerate(zip(a,b,strict=True)) if x!=y]==[50]
    arm=after.read_file('/__arm9__.bin');assert sha(arm)==conf['predecessor_component_hashes']['/__arm9__.bin']
    assert len(MainCodeFile(arm,0x02000000).sections[3].data)-48==123264
    builder=Path('scripts/build_integrated_release.py').read_bytes();stage=(REG/'builder.stage.bin').read_bytes()
    assert builder.count(stage)==1 and builder.replace(stage,b'',1)==(REG/'build_integrated_release.py.before').read_bytes()
    assert builder.index(b"profile_config.get('rafael_B49_editorial')")<builder.index(stage)<builder.index(b'    # Lexically valid')
    clean=Path(conf['clean_ROM']);clean_sha=sha(clean.read_bytes());assert clean_sha==conf['clean_ROM_sha256']
    patch=ROM.with_suffix('.xdelta');reconstructed=ROOT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
    assert not patch.exists() and not reconstructed.exists();ROOT.mkdir(parents=True)
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,reconstructed)
    assert reconstructed.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_sha
    pins=Path('translations/rom_retention_pins.json');pin_before=pins.read_bytes();values=json.loads(pin_before);prior_values=list(values)
    for path,reason in [(ROM,'Registered cumulative Rafael B50 candidate;all639batches/18checks/110regressions andexact clean-input patch. No promotion orseparate test package.'),
        (reconstructed,'Exact clean-input xdelta reconstruction ofregistered Rafael B50 candidate;retain asimmutable byte-exact release evidence.')]:
        assert all(Path(p['path']).resolve()!=path.resolve() for p in values)
        values.append(dict(path=str(path.resolve()),reason=reason+' Preserve every ROM. SHA256 '+sha(path.read_bytes())))
    assert values[:-2]==prior_values
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');(ROOT/'pins.before.json').write_bytes(pin_before)
    assert pins.read_bytes()==pin_before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'registered_release_verification.json',dict(candidate=str(ROM),candidate_sha256=digest,
        manifest=str(ROM.with_suffix('.manifest.json')),manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),profile=manifest['profile'],
        canonical_base=manifest['base_rom'],canonical_base_sha256=manifest['base_sha256'],manifest_batches=639,accepted_layers=114,
        all639_manifest_batches_and114_accepted_layers_present=True,all18_registered_release_checks_pass=True,
        all110_release_dialogue_regressions_pass=True,all_prior_profiles_andmainV4701_preserved=True,
        file_changes=changes,component_changes=components,only_SC0_B50_change_all342others_exact=True,
        atomic_positive_proof='work/analysis/Rafael_B50_atomic_positive_v8169/positive_reconstruction.json',
        atomic_positive_proof_sha256=sha(Path('work/analysis/Rafael_B50_atomic_positive_v8169/positive_reconstruction.json').read_bytes()),
        whole_ROM_equals_pinned_approved_reference=True,ARM9_sha256=sha(arm),COMMON_sha256=sha(after.read_file('/COMMON/MESFILE.DK4')),
        story_hashes={f'SC{r}':sha(after.read_file(f'/data/SC{r}.DK4')) for r in range(4)},
        all_native_shapes_BSS_and123264_staged_bytes_preserved=True,patch=str(patch),patch_sha256=sha(patch.read_bytes()),
        clean_input_sha256=clean_sha,exact_patch_reconstruction=str(reconstructed),whole_clean_input_ROM_reconstruction_byte_exact=True,
        pins_before_sha256=sha(pin_before),pins_after_sha256=sha(encoded),all_prior_pins_preserved=True,
        registration_receipt_sha256=sha((REG/'registration_receipt.json').read_bytes()),verified_registration_receipt=str(REG/'registration_receipt.json'),verified_registration_receipt_sha256=sha((REG/'registration_receipt.json').read_bytes()),
        regressions_terminal_sha256=sha(Path('work/analysis/Rafael_B50_regressions_v8172/terminal.json').read_bytes()),
        own_ROM_startup_andcompletion_credit_pending=True,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(candidate_sha256=digest,patch_sha256=sha(patch.read_bytes()),batches=639,accepted=114,checks=18,regressions=110,exact_clean_patch=True),flush=True)
