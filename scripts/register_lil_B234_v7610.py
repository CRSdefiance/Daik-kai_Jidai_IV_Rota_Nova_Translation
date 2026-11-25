"""Append B234 after the complete registered V7563 without changing promotion."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B234_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B234_registration_v7610');PROFILE='all-routes-unified-v7611'
VALIDATION=Path('work/analysis/lil_B234_atomic_v7609');PARENT=Path('out/all_routes_combined_v7563_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();r=read(VALIDATION/'atomic_validation_receipt.json');config=Path(r['config']);conf=read(config);cases=read(r['negative_cases'])
    assert r['positive_records']==18 and r['negative_count']==len(cases)==110 and all(c['rejected'] and c['archive_writes']==0 for c in cases) and r['all_negatives_reject_before_mutation'] and r['all18_actual18_pages71_body71_headers_bound'] and r['original_A00025_ends_and_explicit_comparison_limits_bound']
    assert sha(config.read_bytes())==r['config_sha256'] and sha(PARENT.read_bytes())==r['parent_ROM_sha256'] and sha(Path(r['negative_cases']).read_bytes())==r['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7607/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(PARENT.with_suffix('.manifest.json'))['batches'])==625
    stage=b'''    lil_proof = profile_config.get('lil_B234_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B234_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B234_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B234 must run once after the complete V7563 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B234_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert after.index(b"profile_config.get('lil_B233_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7563']);profile.update(status='experimental',lil_B234_editorial=owned.CONFIG,description='Complete V7563 plus18 clean-Japanese B234 whole-exchange decisions:14 revisions andfour individually justified retentions. Preserve familiar Carlo/Filippo banter,unspecified recovery,aboard-their-ship fact,the merchant great-grandfather,papal direct rule almost to Venice,donation kinds/quantities,ancestral trade anddecline,reported finds,prospective blessings andexplicit if-found discovery. Carlo Sinat andTrader remain scoped contextual name/role retentions;Filippo is a spoken alias only. European regional storage is independently bound at physical ARM9 offset1518924 anddeployed-payload-relative960. Item106 Gregory Crown is unchanged;no quoted title,biography,card/getter orfull mechanic approval. Source1468/logical1468/tail0 fully inverts;target1532/logical1532/tail0 preserves all20 commands18 complete preambles,selectors19/104,voices7/0,zero macros,A0001456->1520 andfour-byte end1464->1528. Eighteen original four-row pages pass144 logical/compiled72 stored alignments,seven zero-ink tails,eight row reasons andone exact R33 line1 article continuation. Five name planes20 alignments comprise8 fresh actor104 literal cases and12 exact Carlo reuse.',note='Eighteen policy positives83 rejections and110 focused actual-changing production challenges pass before the sole archive write. Both16001-frame initialized B22 runs cover18 speeches/pages71 body71 header holds and29 commands. Exact R5 three CP932 ellipses retain18 black18 light-gray pixels inthree source andthree English holds;other ASCII uses dark gray. Matched portraits,results andUI agree. Exits7174/7173,port7270,eighteen command rows andeight duration differences remain. All147 later sampled RGB frames,five queried components,actors,captains andfinal seeds agree within that scope only. No full-RAM,every-frame,future-sequence,broad simulation orcomplete causal claim. Event234/action235 hasno explicit prerequisites orexclusions;fixture doesnot prove natural activation,original location,earned progress,full effects,routes orhardware. Catalogue UI andbroader207-name review remain open. Keep SC0B246/SC1B237 clean-counterpart leads unreviewed without duplicate credit. Preserve all earlier artifacts,failed derivations/census-dependent fixture attempt andinitial/refined layouts. MainV4701 unchanged;exact patch andown-current startup pending. No separate unified test package orautomatic promotion.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v7610.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7563',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscript=conf['manuscript'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=r['positive_proof'],negative_cases=r['negative_cases'],negative_count=110,all_negatives_reject_before_mutation=True,expected_manifest_batches=626,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered experimental V7611:626 expected batches/114 accepted. All earlier profiles andmainV4701 preserved.')
