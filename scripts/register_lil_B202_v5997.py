"""Append the approved B202 batch once after the complete registered V5947 stack."""
import ast,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B202_editorial_v4 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B202_registration_v5997')
PROFILE='all-routes-unified-v5998'
VALIDATION=Path('work/analysis/lil_B202_atomic_v5996d')
PARENT=Path('out/all_routes_combined_v5947_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    receipt=read(VALIDATION/'atomic_validation_receipt.json');config=Path(receipt['config']);conf=read(config)
    assert receipt['all_negatives_reject_before_mutation'] and receipt['positive_records']==19 and receipt['negative_count']==69
    assert sha(config.read_bytes())==receipt['config_sha256'] and receipt['parent_ROM_sha256']==sha(PARENT.read_bytes())
    assert sha(Path(receipt['positive_proof']).read_bytes())==receipt['positive_proof_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v5981/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256'] and sha(PARENT.read_bytes())==verified['candidate_sha256']
    registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=registry_path.read_bytes(),builder.read_bytes();registry=read(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    parent_manifest=read(PARENT.with_suffix('.manifest.json'));assert len(parent_manifest['batches'])==589
    normal=lambda p:str(p).replace('\\','/')
    assert normal(conf['manuscript']) not in [normal(p) for p in parent_manifest['batches']]
    stage=b'''    lil_proof = profile_config.get('lil_B202_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B202_editorial_v4 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B202_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B202 must run once after the complete V5947 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('lil_B202_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    profile=deepcopy(registry['profiles']['all-routes-unified-v5947'])
    profile.update(status='experimental',lil_B202_editorial=owned.CONFIG,
        description='Complete V5947 plus19 whole-exchange B202 book-handoff/pursuit/examination/advice reviews:six revisions/13 justified retentions. All26 commands/19 preambles/seven leaves,zero FE/macros/relative sites/choices and one ending remain.19 actual English panels/74 complete holds match source regions,original paths and results.Three speech durations,22 shifted pairs,five RNG witnesses and21 later prompt samples differ;queried final native groups/whole actor agree and PRNG differs. No broad simulation/natural activation/earned item-effect claim. Source-defined Sailor alias,Retainer catalogue,Charles middle-name consumer and spoken Glassmaking Guide title remain bound.207-name and following B43/source-item/Local Product leads stay open.',
        note='Native/source/reference/actual English scope and69 pre-mutation semantic negatives approved. Registered cumulative build,clean-input patch and current startup pending. Main V4701 preserved.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before)
    (ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before and not Path(owned.CONFIG).exists()
    save(owned.CONFIG,conf)
    temporary=builder.with_name('build_integrated_release_v5997.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with registry_path.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v5947',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts={conf['manuscript']:sha(Path(conf['manuscript']).read_bytes())},
        reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(registry_path.read_bytes()),
        builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=receipt['positive_proof'],negative_cases=receipt['negative_cases'],negative_count=receipt['negative_count'],
        all_negatives_reject_before_mutation=True,expected_manifest_batches=590,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered experimental V5998:complete V5947 plus B202 once,590 expected batches/114 accepted.69 atomic negatives pass;main V4701 unchanged.')
