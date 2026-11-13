"""Append B233 after the complete registered V7514 without changing promotion."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B233_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B233_registration_v7562');PROFILE='all-routes-unified-v7563'
VALIDATION=Path('work/analysis/lil_B233_atomic_v7561');PARENT=Path('out/all_routes_combined_v7514_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();r=read(VALIDATION/'atomic_validation_receipt.json');config=Path(r['config']);conf=read(config);cases=read(r['negative_cases'])
    assert r['positive_records']==11 and r['negative_count']==len(cases)==240 and all(c['rejected'] and c['archive_writes']==0 for c in cases) and r['all_negatives_reject_before_mutation'] and r['all11_actual11_pages43_body43_headers_bound'] and r['original_A00025_ends_and_explicit_comparison_limits_bound']
    assert sha(config.read_bytes())==r['config_sha256'] and sha(PARENT.read_bytes())==r['parent_ROM_sha256'] and sha(Path(r['negative_cases']).read_bytes())==r['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7558/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(PARENT.with_suffix('.manifest.json'))['batches'])==624
    stage=b'''    lil_proof = profile_config.get('lil_B233_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B233_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B233_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B233 must run once after the complete V7514 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B233_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert after.index(b"profile_config.get('lil_B231_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7514']);profile.update(status='experimental',lil_B233_editorial=owned.CONFIG,description='Complete V7514 plus11 clean-Japanese B233 whole-exchange decisions:seven revisions andfour justified retentions. Preserve Manuel Almeida personal library-paper discovery,reported Phidias chisel andposthumous soul/talent beliefs,vague Balkan Peninsula clue nearGreece,Lil Argot ship-repair teasing,reported Roman kings/tools policy joke,ships-as-art defense andopportunity-conditioned request. Source233/action234 requires232. Both personal names andnull middles match original getters;catalogue UI remains unvisited. Source964/logical962/tail2 fully inverts;target956/logical954/tail2 preserves all13 commands11 preambles,selectors2/23,voices3/7,zero macros,A000950->942 andfour-byte end958->950. Eleven original four-row pages pass88 logical/compiled44 stored alignments,three zero-ink tails,three row reasons andzero QA errors,warnings orwaivers. Six name planes24 alignments areexact reused inputs,zero fresh name-font executions.',note='Eleven policy positives65 rejections and240 fresh actual-changing production corruptions pass before the sole archive write. Both16001-frame initialized B22 runs cover11 speeches/pages43 body43 header holds and22 commands. Matched portraits,results andUI agree. Source/English exits5495/5493,port5590,eight command rows,three durations,109of175 later RGB differences,calendar/PRNG/components/actors andB120 ends10293/10294 remain explicit. Source finalSeaView differs fromEnglish complete Sailor Dizzy starving dialogue. Exact source/current item97 fields support Phidias Chisel spelling;no item asset,card,getter,mechanic orother-consumer approval. Initialized B22 proves no natural activation,original location,earned232,full effects,routes orhardware. No full-RAM,every-frame,future,broad-simulation orcomplete causal claim. Preserve source-page historical B222 filename failure/successor andallinitial/refined wraps. Full editorial/name/earlier-wrap objective andallprevious artifacts remain;mainV4701 unchanged;patch andown-current startup pending;no separate test package orautomatic promotion.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v7562.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7514',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscript=conf['manuscript'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=r['positive_proof'],negative_cases=r['negative_cases'],negative_count=240,all_negatives_reject_before_mutation=True,expected_manifest_batches=625,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered experimental V7563:625 expected batches/114 accepted. All earlier profiles andmainV4701 preserved.')
