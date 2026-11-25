"""Append B196 once after the complete registered V5580 stack; preserve promotion."""
import ast,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B196_editorial_v3 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B196_registration_v5636')
PROFILE='all-routes-unified-v5637'
VALIDATION=Path('work/analysis/lil_B196_atomic_v5635c')
PARENT=Path('out/all_routes_combined_v5580_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    receipt=read(VALIDATION/'atomic_validation_receipt.json');config=Path(receipt['config']);conf=read(config)
    assert receipt['all_negatives_reject_before_mutation'] and receipt['positive_records']==36 and receipt['negative_count']>=90
    assert sha(config.read_bytes())==receipt['config_sha256'] and receipt['parent_ROM_sha256']==sha(PARENT.read_bytes())
    assert sha(Path(receipt['positive_proof']).read_bytes())==receipt['positive_proof_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v5633/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256'] and sha(PARENT.read_bytes())==verified['candidate_sha256']
    registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=registry_path.read_bytes(),builder.read_bytes();registry=read(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    parent_manifest=read(PARENT.with_suffix('.manifest.json'));assert len(parent_manifest['batches'])==579
    normal=lambda p:str(p).replace('\\','/')
    assert all(normal(conf[k]) not in [normal(p) for p in parent_manifest['batches']] for k in ['manuscript','choices'])
    stage=b'''    lil_proof = profile_config.get('lil_B196_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B196_editorial_v3 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B196_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        for key in ['manuscript', 'choices']:
            more_batch = Path(lil_proof_report[key])
            if more_batch in release_batches:
                raise ValueError('B196 companions must run once after the complete V5580 stack')
            release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('lil_B196_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    profile=deepcopy(registry['profiles']['all-routes-unified-v5580'])
    profile.update(status='experimental',lil_B196_editorial=owned.CONFIG,
        description='Complete V5580 plus36 contextual B196 speech/menu reviews:15 revisions/21 individual retentions. Preserve six prices,gender-neutral seller,source actor voices,conditional asides,one FE FI Charm notice,six Buy/Pass menus,52 relative sites,37 exact leaves and seven endings. All1816 predecessor bytes restore exactly. Six targeted cold boots cover13 speech panels/13 menu cases/three endings;11 speeches remain native offline. Current native guards and exact R74 ordinary-wrap approval remain. No natural eligibility,earned affordability,full-route or hardware claim.',
        note='Source/native/reference/representative and atomic positive/negative checks approved;registered build,clean patch and current startup pending.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before)
    (ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before and not Path(owned.CONFIG).exists()
    save(owned.CONFIG,conf)
    temporary=builder.with_name('build_integrated_release_v5636.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with registry_path.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v5580',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts={conf[k]:sha(Path(conf[k]).read_bytes()) for k in ['manuscript','choices']},
        reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(registry_path.read_bytes()),
        builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=receipt['positive_proof'],negative_cases=receipt['negative_cases'],negative_count=receipt['negative_count'],
        all_negatives_reject_before_mutation=True,expected_manifest_batches=len(parent_manifest['batches'])+len([conf[k] for k in ['manuscript','choices']]),accepted_layers=114,
        promoted_profile_unchanged='all-routes-unified-v4701',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(registered=PROFILE,positive_records=36,negative_cases=receipt['negative_count'],expected_batches=len(parent_manifest['batches'])+2,accepted=114,promotion_unchanged=True))
