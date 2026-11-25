"""Register the ten-label data layer after every V7011 dialogue compiler."""
import ast,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import square_shopkeeper_label_release_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/square_shopkeeper_registration_v7028')
PROFILE='all-routes-unified-v7029'
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    atomic=Path('work/analysis/square_shopkeeper_atomic_v7027/atomic_validation_receipt.json');receipt=read(atomic)
    cases=read(receipt['negative_cases']);test_source=Path('scripts/challenge_square_shopkeeper_atomic_v7027.py')
    count=next(len(n.value.elts) for n in ast.walk(ast.parse(test_source.read_text('utf8'))) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='tests' for t in n.targets))
    assert count>=60 and receipt['positive_records']==10 and receipt['negative_count']==len(cases)==count
    assert receipt['all_negatives_reject_before_mutation'] and all(c['rejected'] and c['archive_writes']==0 for c in cases)
    conf=read(receipt['config']);assert sha(Path(receipt['config']).read_bytes())==receipt['config_sha256']
    assert sha(Path(receipt['positive_proof']).read_bytes())==receipt['positive_proof_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    prior=read('work/analysis/editorial_handoff_verification_v7017/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['ledger_sha256']
    parent=Path(prior['candidate']);assert prior['profile']=='all-routes-unified-v7011' and sha(parent.read_bytes())==prior['candidate_sha256']==receipt['parent_ROM_sha256']
    regpath,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    registry=read(regpath);raw=regpath.read_bytes();before=builder.read_bytes()
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(parent.with_suffix('.manifest.json'))['batches'])==613
    template=Path('scripts/register_generic_speaker_labels_v5890.py')
    stage=next(n.value.value for n in ast.walk(ast.parse(template.read_text('utf8'))) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='stage' for t in n.targets))
    stage=stage.replace(b'generic_speaker_labels_release_v1',b'square_shopkeeper_label_release_v2').replace(b'generic_speaker_labels',b'square_shopkeeper_labels')
    stage=stage.replace(b'Generic speaker labels',b'Ten Shopkeeper labels').replace(b'V5872',b'V7011')
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('square_shopkeeper_labels')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('lil_B221_editorial')")<after.index(stage)<after.index(anchor)
    assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    profile=deepcopy(registry['profiles']['all-routes-unified-v7011']);profile.update(status='experimental',square_shopkeeper_labels=owned.CONFIG,
        description='Complete V7011 plus all ten clean広場の店主 labels localized as Shopkeeper.42 complete source contexts/34 unique blocks/216 role utterances support the occupational label. Only18 bytes in two owned prefixes change;all621 pointers,all other197 names,207 voices,code,fonts,cache wrapper and123264-byte extent remain. Both original name getters/three field getters,176 macro alignments,complete60px native label and nine actual changed headers across32 complete body pages pass. No story prose or duplicate name/dialogue credit.',
        note=f'{count} real-changing pre-mutation corruptions rejected. Static parent/target scene exits6937/6936 with18 timing/two RNG-word and98 RGB differences(82 outside the name strip);staged exits6693/6693 with no command differences and19 name-strip-only RGB differences. Keep all raw evidence and later-world limits,B189 retrospective wrapping and broader207-name/full editorial goal open. Main V4701 preserved;registered build/patch/current startup pending.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert regpath.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf)
    tmp=builder.with_name('build_integrated_release_v7028.tmp');assert not tmp.exists();tmp.write_bytes(after);os.replace(tmp,builder)
    with regpath.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    inverse=deepcopy(read(regpath));inverse['profiles'].pop(PROFILE);assert inverse==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile=prior['profile'],parent_ROM=str(parent),parent_ROM_sha256=prior['candidate_sha256'],
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(regpath.read_bytes()),
        builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),manuscript=conf['manuscript'],manuscript_sha256=sha(Path(conf['manuscript']).read_bytes()),
        atomic_receipt=str(atomic),atomic_receipt_sha256=sha(atomic.read_bytes()),negative_producer=str(test_source),negative_producer_sha256=sha(test_source.read_bytes()),
        negative_count=count,all_negatives_reject_before_mutation=True,expected_manifest_batches=614,accepted_layers=114,all_prior_profiles_and_V4701_promotion_preserved=True,
        source_stage_template=str(template),source_stage_template_sha256=sha(template.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(f'Registered experimental V7029:614 batches/114 accepted;ten labels follow all V7011 stages. All earlier profiles/main V4701 preserved.',flush=True)
