"""Append one name-data layer after the complete cumulative V5872 stack."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import generic_speaker_labels_release_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/generic_speaker_labels_registration_v5890')
PROFILE='all-routes-unified-v5891'

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    receipt=read('work/analysis/generic_speaker_labels_atomic_v5889/atomic_validation_receipt.json')
    assert receipt['positive_records']==3 and receipt['negative_count']>=65 and receipt['all_negatives_reject_before_mutation']
    conf=read(receipt['config']);assert sha(Path(receipt['config']).read_bytes())==receipt['config_sha256']
    assert sha(Path(receipt['positive_proof']).read_bytes())==receipt['positive_proof_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    prior=read('work/analysis/editorial_handoff_verification_v5878/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['ledger_sha256']
    parent=Path(prior['candidate']);assert sha(parent.read_bytes())==prior['candidate_sha256']==receipt['parent_ROM_sha256']
    regpath,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    registry=read(regpath);raw=regpath.read_bytes();before=builder.read_bytes()
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(parent.with_suffix('.manifest.json'))['batches'])==586
    stage=b'''    label_config = profile_config.get('generic_speaker_labels')
    if label_config:
        from dk4tool.patch.generic_speaker_labels_release_v1 import apply_release as apply_labels

        label_report = apply_labels(candidate, baseline, label_config)
        grouped.setdefault('/__arm9__.bin', [])
        changed_records.setdefault('/__arm9__.bin', []).extend(row['id'] for row in label_report['changed_records'])
        relocation_checks.setdefault('/__arm9__.bin', {})['generic_speaker_labels'] = {
            'release_config': label_config,
            'release_config_sha256': sha256(Path(label_config).read_bytes()),
            'proof': label_report}
        more_batch = Path(label_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('Generic speaker labels must run once after the complete V5872 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('generic_speaker_labels')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    profile=deepcopy(registry['profiles']['all-routes-unified-v5872'])
    profile.update(status='experimental',generic_speaker_labels=owned.CONFIG,
        description='Complete V5872 plus three source-context speaker-label revisions:Man/Woman/Stranger. All621 source field getters,414 progressive/catalogue consumers,64 macro alignments,three native font planes and16 changed actual headers in two complete existing exchanges pass. No scene words,other names,code,pointers,allocations,graphics or fonts change.',
        note='Three source-owned primary string prefixes only;114 accepted layers and mainV4701 remain. Representative B22 fixtures are not natural event activation;catalogue UI not visited. Full207-name and wider editorial scope remain open;no duplicate dialogue credit.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before)
    (ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert regpath.read_bytes()==raw and builder.read_bytes()==before
    save(owned.CONFIG,conf)
    temporary=builder.with_name('build_integrated_release_v5890.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with regpath.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(regpath));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v5872',parent_ROM=str(parent),parent_ROM_sha256=sha(parent.read_bytes()),
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        registry_before_sha256=sha(raw),registry_after_sha256=sha(regpath.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        manuscript=conf['manuscript'],manuscript_sha256=sha(Path(conf['manuscript']).read_bytes()),expected_manifest_batches=587,accepted_layers=114,
        negative_count=receipt['negative_count'],all_negatives_reject_before_mutation=True,all_prior_profiles_and_V4701_promotion_preserved=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered experimental V5891:completeV5872 plus three labels once;587batches/114accepted;allpreviousprofiles/mainV4701 unchanged.')
