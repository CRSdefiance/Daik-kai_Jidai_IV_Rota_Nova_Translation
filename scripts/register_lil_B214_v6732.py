"""Append the sealed seventeen-object exchange after the complete registered V6686 stack."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B214_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B214_registration_v6732');PROFILE='all-routes-unified-v6733';VALIDATION=Path('work/analysis/lil_B214_atomic_v6731');PARENT=Path('out/all_routes_combined_v6686_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();r=read(VALIDATION/'atomic_validation_receipt.json');config=Path(r['config']);conf=read(config);cases=read(r['negative_cases'])
    assert r['positive_records']==17 and r['negative_count']==len(cases)>=90 and all(c['rejected'] and c['archive_writes']==0 for c in cases) and r['all_negatives_reject_before_mutation'] and r['nine_actual_objects29_body29_names_eight_offline_objects_and_scope_bound'] and r['both_opposite_predicate_alignment_changes_original_owned_scratch_and_normal_residual_bound']
    assert sha(config.read_bytes())==r['config_sha256'] and sha(PARENT.read_bytes())==r['parent_ROM_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v6713/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp);assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(PARENT.with_suffix('.manifest.json'))['batches'])==605
    stage=b'''    lil_proof = profile_config.get('lil_B214_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B214_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B214_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B214 must run once after the complete V6686 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B214_editorial')" not in before;after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert after.index(b"profile_config.get('lil_B213_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v6686']);profile.update(status='experimental',lil_B214_editorial=owned.CONFIG,description='Complete V6686 plus seventeen Lil B214 whole-exchange decisions: twelve revisions and five justified retentions. Preserve the Rome-road letter, reported Judas-sword clue, religious context, practical recommendation, optional Manuel aside/reply and distinct automatic crew voices. Correct this signature from Janus Pasha to the existing native Janus Pasar; five other consumers stay queued. All27 commands, ten preambles, seven automatic bodies/eight aliased slots, eight relatives, both original predicates, 4500/4621 staging, A000, normal residual end and full1316-byte inverse. Target1304 stored/1302 logical/tail2; seventeen native pages,136 logical/compiled and68 stored alignments,44 name alignments. Actual eight speeches/one style body,nine pages/29 body29 name holds; eight other objects explicitly offline. Eleven rowcount reasons,six scoped boundaries,80 policy rejections. No new name assets or duplicate credit. Full editorial/207-name/earlier-wrap objective remains active; graphics and later technical re-audit remain separate.',note=f"{r['negative_count']} independent semantic rejections precede every write. Source/English observed results,UI,timing,RNG,durations,nine semantic scenes,later samples andfive queried final components agree within recorded scope. No natural event214/prerequisite87 earned-progress/full-effect/route/hardware or broad simulation claim. MainV4701 andall earlier artifacts preserved. Patch/current startup pending;no automatic promotion.")
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode();ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v6732.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v6686',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscript=conf['manuscript'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=r['positive_proof'],negative_cases=r['negative_cases'],negative_count=r['negative_count'],all_negatives_reject_before_mutation=True,expected_manifest_batches=606,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Registered experimental V6733:606 expected batches/114 accepted. All earlier profiles and mainV4701 preserved.')
