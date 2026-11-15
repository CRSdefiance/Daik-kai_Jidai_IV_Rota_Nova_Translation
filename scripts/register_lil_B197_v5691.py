"""Append B197 once after the complete registered V5637 stack; preserve promotion."""
import ast,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B197_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B197_registration_v5691')
PROFILE='all-routes-unified-v5692'
VALIDATION=Path('work/analysis/lil_B197_atomic_v5690')
PARENT=Path('out/all_routes_combined_v5637_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    receipt=read(VALIDATION/'atomic_validation_receipt.json');config=Path(receipt['config']);conf=read(config)
    assert receipt['all_negatives_reject_before_mutation'] and receipt['positive_records']==24 and receipt['negative_count']>=80
    assert sha(config.read_bytes())==receipt['config_sha256'] and receipt['parent_ROM_sha256']==sha(PARENT.read_bytes())
    assert sha(Path(receipt['positive_proof']).read_bytes())==receipt['positive_proof_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v5675/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256'] and sha(PARENT.read_bytes())==verified['candidate_sha256']
    registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=registry_path.read_bytes(),builder.read_bytes();registry=read(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    parent_manifest=read(PARENT.with_suffix('.manifest.json'));assert len(parent_manifest['batches'])==581
    normal=lambda p:str(p).replace('\\','/')
    assert all(normal(conf[k]) not in [normal(p) for p in parent_manifest['batches']] for k in ['manuscript','choices'])
    stage=b'''    lil_proof = profile_config.get('lil_B197_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B197_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B197_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        for key in ['manuscript', 'choices']:
            more_batch = Path(lil_proof_report[key])
            if more_batch in release_batches:
                raise ValueError('B197 companions must run once after the complete V5637 stack')
            release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('lil_B197_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    profile=deepcopy(registry['profiles']['all-routes-unified-v5637'])
    profile.update(status='experimental',lil_B197_editorial=owned.CONFIG,
        description='Complete V5637 plus24 contextual B197 objects:16 revisions/eight justified retentions. Preserve Ian/Alluring Woman voices,Indian classic/celestial maiden/sage,8500 gold,purchase then romantic rebuff,delegated personal apology/gift,and common Ian Charm notice. One2200 proposal/refusal/delegation menu,six relative sites,39 commands,11 exact leaves and one common end remain.21 distinct speech panels/35 observations/128 native holds/all three visible options and normal returns are captured. Retain59 timing/82 later RGB and explicit RNG/state differences without broad simulation equivalence,natural activation,earned affordability,full-route or hardware claims.',
        note='Source/native/reference/representative and atomic positive/negative checks approved;registered build,clean patch and current startup pending.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before)
    (ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before and not Path(owned.CONFIG).exists()
    save(owned.CONFIG,conf)
    temporary=builder.with_name('build_integrated_release_v5691.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with registry_path.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v5637',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts={conf[k]:sha(Path(conf[k]).read_bytes()) for k in ['manuscript','choices']},
        reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(registry_path.read_bytes()),
        builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=receipt['positive_proof'],negative_cases=receipt['negative_cases'],negative_count=receipt['negative_count'],
        all_negatives_reject_before_mutation=True,expected_manifest_batches=len(parent_manifest['batches'])+len([conf[k] for k in ['manuscript','choices']]),accepted_layers=114,
        promoted_profile_unchanged='all-routes-unified-v4701',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(registered=PROFILE,positive_records=24,negative_cases=receipt['negative_count'],expected_batches=len(parent_manifest['batches'])+2,accepted=114,promotion_unchanged=True))
