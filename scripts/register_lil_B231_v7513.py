"""Append B231 after the complete registered V7466 without changing promotion."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B231_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B231_registration_v7513');PROFILE='all-routes-unified-v7514'
VALIDATION=Path('work/analysis/lil_B231_atomic_v7512');PARENT=Path('out/all_routes_combined_v7466_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();r=read(VALIDATION/'atomic_validation_receipt.json');config=Path(r['config']);conf=read(config);cases=read(r['negative_cases'])
    assert r['positive_records']==16 and r['negative_count']==len(cases)==253 and all(c['rejected'] and c['archive_writes']==0 for c in cases) and r['all_negatives_reject_before_mutation'] and r['all16_actual16_pages63_body63_headers_bound'] and r['original_A00025_ends_and_explicit_comparison_limits_bound']
    assert sha(config.read_bytes())==r['config_sha256'] and sha(PARENT.read_bytes())==r['parent_ROM_sha256'] and sha(Path(r['negative_cases']).read_bytes())==r['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7509/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(PARENT.with_suffix('.manifest.json'))['batches'])==623
    stage=b'''    lil_proof = profile_config.get('lil_B231_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B231_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B231_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B231 must run once after the complete V7466 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B231_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert after.index(b"profile_config.get('lil_B230_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7466']);profile.update(status='experimental',lil_B231_editorial=owned.CONFIG,description='Complete V7466 plus16 clean-Japanese B231 whole-exchange decisions:ten revisions andsix contextual retentions. Preserve the ancient physician andoldest medical-book exposition,reported crew fatigue management,conditional excitement,tentative old heard sighting in the far reaches ofthe Mediterranean,inadequate clue,polite apology,warm reassurance andconditional travel conclusion. Lil Argot andCarlo Sinat retain their exact personal names andnull middle fields. No physician gender,nationality,biography,occupation forCarlo,city,cure,stats,ownership orfind guarantee is invented. Source724/logical722/tail2 inverts completely;target752/logical750/tail2 preserves all18 commands16 preambles,selectors2/19,voices3/7,A000710->738 andfour-byte end718->746. Sixteen original four-row pages pass128 logical/compiled64 stored alignments;6 fresh name planes24 alignments,eight zero-ink tails,four individual row reasons andone exact justified R35 article continuation preserve all base QA.',note='Sixteen policy positives75 rejections and253 fresh actual-changing production corruptions must pass before the single archive write. Source/English each16 pages63 body63 header samples and27 commands;all matched portraits,results andUI agree. Exits6694/6696,port6790,13 command rows,three duration differences,92of155 later RGB differences,calendar/PRNG/components/actors andfollowing B120 differences remain measured scope. Both final16001 samples show complete Sailor food-exhaustion dialogue while whole frames differ. Item99 legacy Herophilus Medicine title remains anunapproved medical-book title consumer lead;no assets,card,getter,mechanics,full catalogue UI orglobal207 name approval. Source231/action232 hasno explicit requires/excludes;initialized B22 isnot natural activation,original location,earned progress,full effects,routes orhardware. No whole-RAM,every-frame,future,broad-simulation orcomplete causal equivalence claim. Preserve source-audit copied-key failure/successor,R12 metadata correction,R9 neutral gloss andall layouts. Full editorial/name/earlier-wrap objective andall artifacts remain;mainV4701 unchanged;exact patch/current startup pending;no separate test package orautomatic promotion.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v7513.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7466',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscript=conf['manuscript'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=r['positive_proof'],negative_cases=r['negative_cases'],negative_count=253,all_negatives_reject_before_mutation=True,expected_manifest_batches=624,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered experimental V7514:624 expected batches/114 accepted. All earlier profiles andmainV4701 preserved.')
