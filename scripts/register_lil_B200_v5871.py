"""Append the approved B200 batch once after the complete registered V5816 stack."""
import ast,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B200_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B200_registration_v5871')
PROFILE='all-routes-unified-v5872'
VALIDATION=Path('work/analysis/lil_B200_atomic_v5869')
PARENT=Path('out/all_routes_combined_v5816_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    receipt=read(VALIDATION/'atomic_validation_receipt.json');config=Path(receipt['config']);conf=read(config)
    assert receipt['all_negatives_reject_before_mutation'] and receipt['positive_records']==19 and receipt['negative_count']==110
    assert sha(config.read_bytes())==receipt['config_sha256'] and receipt['parent_ROM_sha256']==sha(PARENT.read_bytes())
    assert sha(Path(receipt['positive_proof']).read_bytes())==receipt['positive_proof_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v5867/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256'] and sha(PARENT.read_bytes())==verified['candidate_sha256']
    registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=registry_path.read_bytes(),builder.read_bytes();registry=read(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    parent_manifest=read(PARENT.with_suffix('.manifest.json'));assert len(parent_manifest['batches'])==585
    normal=lambda p:str(p).replace('\\','/')
    assert normal(conf['manuscript']) not in [normal(p) for p in parent_manifest['batches']]
    stage=b'''    lil_proof = profile_config.get('lil_B200_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B200_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B200_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B200 must run once after the complete V5816 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('lil_B200_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    profile=deepcopy(registry['profiles']['all-routes-unified-v5816'])
    profile.update(status='experimental',lil_B200_editorial=owned.CONFIG,
        description='Complete V5816 plus19 whole-exchange B200 collapse/inn-recovery/rescue/thanks reviews:13 revisions/six justified retentions. All31 commands/19 preambles/12 leaves/two distinct FE/zero macros and one ending remain. All19 actual panels/73 holds match native text/source regions.172 of182 nontext samples match;ten subsequent sailing-cloud and six prompt differences remain explicit,as do eight speech-duration changes,19 shifted pairs and unequal PRNG. Queried final native components agree;no natural activation,full-route or broad simulation claim. Stranger name target remains separate.',
        note='Source/native/reference/English-content and110 semantic pre-mutation negatives approved. Registered build,clean-input patch and current startup pending. Main V4701 preserved.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before)
    (ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before and not Path(owned.CONFIG).exists()
    save(owned.CONFIG,conf)
    temporary=builder.with_name('build_integrated_release_v5871.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with registry_path.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v5816',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts={conf['manuscript']:sha(Path(conf['manuscript']).read_bytes())},
        reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(registry_path.read_bytes()),
        builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=receipt['positive_proof'],negative_cases=receipt['negative_cases'],negative_count=receipt['negative_count'],
        all_negatives_reject_before_mutation=True,expected_manifest_batches=586,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered experimental V5872:complete V5816 plus B200 once,586 expected batches/114 accepted.110 atomic negatives pass;main V4701 unchanged.')
