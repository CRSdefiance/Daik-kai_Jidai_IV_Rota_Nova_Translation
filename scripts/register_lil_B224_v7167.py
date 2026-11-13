"""Append one sealed scene after the complete registered V7118 stack."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B224_editorial_v3 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B224_registration_v7167');PROFILE='all-routes-unified-v7168'
VALIDATION=Path('work/analysis/lil_B224_atomic_v7166');PARENT=Path('out/all_routes_combined_v7118_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();r=read(VALIDATION/'atomic_validation_receipt.json');config=Path(r['config']);conf=read(config);cases=read(r['negative_cases'])
    assert r['positive_records']==15 and r['negative_count']==len(cases)==161 and all(c['rejected'] and c['archive_writes']==0 for c in cases) and r['all_negatives_reject_before_mutation'] and r['all15_actual_pages59_body59_headers_and_four_ellipsis_full_RGB_holds_bound'] and r['original_A000_C20025_ends_and_explicit_comparison_limits_bound']
    assert sha(config.read_bytes())==r['config_sha256'] and sha(PARENT.read_bytes())==r['parent_ROM_sha256'] and sha(Path(r['negative_cases']).read_bytes())==r['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7163/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(PARENT.with_suffix('.manifest.json'))['batches'])==616
    stage=b'''    lil_proof = profile_config.get('lil_B224_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B224_editorial_v3 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B224_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B224 must run once after the complete V7118 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B224_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert after.index(b"profile_config.get('lil_B223_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7118']);profile.update(status='experimental',lil_B224_editorial=owned.CONFIG,description='Complete V7118 plus15 clean-Japanese whole-exchange B224 decisions:10 revisions and5 justified retentions. Julian Lopes and Safia retain their distinct flirting,stone metaphor,reported Tasman-Sea Medusa Shield clue,covered-hair compliment,practical statue joke and restrained final emotional softening.18 commands,15 preambles,voices2/0,zero macros,A000,C200 andfour-byte normal end remain.960 stored/958 logical/tail2 inverts fully;1040 target/no tail.15 native pages,120 logical/compiled and60 stored alignments,nine zero-ink tails,20 name alignments,five row reasons,three exact wrap waivers,all base QA and62 policy rejects. All15 actual initialized English pages/59 body59 headers. Original CP932 ellipsis1a8163 retains its source lighter gray andfull RGB inallfour holds;other14 ASCII checks unchanged. No name assets or duplicate credits;Basra metadata isnot a surname. Full editorial/207-name/earlier-wrap scope stays active.',note='161 actual-changing production corruptions reject before every archive write. All27 observed results/UI/timing/RNG,durations,15 matched portrait/scene pairs,159 later sampled RGB frames andfive queried final components agree within recorded scope. Both following SC2 B120 ends11256;captain2 andPRNG3169181745 agree. Initialized B22 coverage isnot natural event224 activation,original location,earned progress,full effects,an exhaustive route orhardware. No whole-RAM/every-frame/future-sequence/broad-simulation orcomplete causal claim. MainV4701 andall earlier artifacts remain. Exact patch/current startup pending;no automatic promotion.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v7167.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7118',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscript=conf['manuscript'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=r['positive_proof'],negative_cases=r['negative_cases'],negative_count=161,all_negatives_reject_before_mutation=True,expected_manifest_batches=617,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered experimental V7118:617 expected batches/114 accepted. All earlier profiles andmainV4701 preserved.')
