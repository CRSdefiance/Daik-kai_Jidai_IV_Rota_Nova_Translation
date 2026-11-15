"""Append one validated name-data layer after the complete cumulative V6220 stack."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import shady_man_label_release_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shady_man_label_registration_v6269');PROFILE='all-routes-unified-v6270'
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();receipt=read('work/analysis/shady_man_label_atomic_v6267/atomic_validation_receipt.json')
    assert receipt['positive_records']==1 and receipt['negative_count']==57 and receipt['all_negatives_reject_before_mutation']
    conf=read(receipt['config']);assert sha(Path(receipt['config']).read_bytes())==receipt['config_sha256'] and sha(Path(receipt['positive_proof']).read_bytes())==receipt['positive_proof_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    prior=read('work/analysis/editorial_handoff_verification_v6256/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['ledger_sha256']
    parent=Path(prior['candidate']);assert sha(parent.read_bytes())==prior['candidate_sha256']==receipt['parent_ROM_sha256']
    regpath,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');registry=read(regpath);raw=regpath.read_bytes();before=builder.read_bytes()
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(parent.with_suffix('.manifest.json'))['batches'])==594
    stage=b'''    label_config = profile_config.get('shady_man_label')
    if label_config:
        from dk4tool.patch.shady_man_label_release_v1 import apply_release as apply_shady_man

        label_report = apply_shady_man(candidate, baseline, label_config)
        grouped.setdefault('/__arm9__.bin', [])
        changed_records.setdefault('/__arm9__.bin', []).extend(row['id'] for row in label_report['changed_records'])
        relocation_checks.setdefault('/__arm9__.bin', {})['shady_man_label'] = {
            'release_config': label_config,
            'release_config_sha256': sha256(Path(label_config).read_bytes()),
            'proof': label_report}
        more_batch = Path(label_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('Shady Man must run once after the complete V6220 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('shady_man_label')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    profile=deepcopy(registry['profiles']['all-routes-unified-v6220']);profile.update(status='experimental',shady_man_label=owned.CONFIG,description='Complete V6220 plus source-context actor173 label Shady Man. Eight complete clean seller exchanges/195 speeches support the localization. All621 field and414 name getters per version,eight voices,96 macro alignments,complete native font plane and10 changed actual headers pass.',note='One owned primary ASCII prefix only;all other names,story prose,code,pointers,fonts,graphics and123264 staged bytes extent preserved. Representative Japanese B206 purchase fixture shows small timing/RNG differences,recorded without broad equivalence claims. Catalogue UI/natural event activation not claimed. Full207-name and wider editorial goal open;mainV4701 preserved;no duplicate credit.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert regpath.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf)
    with builder.open('r+b') as stream:stream.write(after);stream.truncate();stream.flush();os.fsync(stream.fileno())
    with regpath.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(regpath));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v6220',parent_ROM=str(parent),parent_ROM_sha256=sha(parent.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(regpath.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),manuscript=conf['manuscript'],manuscript_sha256=sha(Path(conf['manuscript']).read_bytes()),expected_manifest_batches=595,accepted_layers=114,negative_count=57,all_negatives_reject_before_mutation=True,all_prior_profiles_and_V4701_promotion_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered experimental V6270:completeV6220 plus one Shady Man label;595batches/114accepted. Allpreviousprofiles/mainV4701 unchanged.')
