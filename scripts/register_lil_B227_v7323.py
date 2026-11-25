"""Append B227 after the complete registered V7277 without changing promotion."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B227_editorial_v3 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B227_registration_v7323');PROFILE='all-routes-unified-v7324'
VALIDATION=Path('work/analysis/lil_B227_atomic_v7322');PARENT=Path('out/all_routes_combined_v7277_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();r=read(VALIDATION/'atomic_validation_receipt.json');config=Path(r['config']);conf=read(config);cases=read(r['negative_cases'])
    assert r['positive_records']==9 and r['negative_count']==len(cases)==196 and all(c['rejected'] and c['archive_writes']==0 for c in cases) and r['all_negatives_reject_before_mutation'] and r['all9_actual9_pages35_body35_headers_bound'] and r['three_original_A00025_ends_both_tails_and_explicit_comparison_limits_bound']
    assert sha(config.read_bytes())==r['config_sha256'] and sha(PARENT.read_bytes())==r['parent_ROM_sha256'] and sha(Path(r['negative_cases']).read_bytes())==r['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7319/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(PARENT.with_suffix('.manifest.json'))['batches'])==619
    stage=b'''    lil_proof = profile_config.get('lil_B227_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B227_editorial_v3 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B227_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B227 must run once after the complete V7277 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B227_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert after.index(b"profile_config.get('lil_B226_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7277']);profile.update(status='experimental',lil_B227_editorial=owned.CONFIG,description='Complete V7277 plus nine clean-Japanese B227 whole-exchange decisions: seven revisions and two justified retentions. Preserve Yifa practice cries, Lil recognition, courage and hesitant-advance injury explanation, reported cloth martial-arts uniform rumor, personal conditional wish, gender-neutral remembered teacher quotation and renewed practice. Lil Argot and Yifa Sol are contextually retained without assets or duplicate credit; full207 names remain open. All13 commands/nine preambles, selectors2/25, voices3/3, zero macros, three A000 controls and four-byte normal end remain. Source668/logical666/tail2 fully inverts; target708/logical706/tail2. Nine complete native pages,72 logical/compiled36 stored24 name alignments,five zero-ink tails,two row reasons and one exact R15 phrasal-verb warning classification preserve all base QA. Nine positives/50 policy rejections and all35 actual body/header holds pass.',note='196 actual-changing production corruptions must reject before mutation. All22 observed commands/results/UI and nine matched scene/portrait pairs pass. Preserve11 command-comparison rows,four duration changes,120 of183 later sampled RGB differences,models/persistent/calendar differences,captains2/2,seeds2971698614/2367937388,andfollowing B120 ends9816/9813. Initialized B22 is not natural227 activation,original location,earned progress,full effects,routes orhardware. No whole-RAM/every-frame/future/broad-simulation orcomplete causal claim. Actual report copied226 disclaimer metadata is preserved; production independently binds explicit227 fixture/run-plan flags. Full editorial/name/earlier-wrap objective active. All artifacts andmainV4701 preserved; exact patch/current startup pending; no automatic promotion.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v7323.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7277',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscript=conf['manuscript'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=r['positive_proof'],negative_cases=r['negative_cases'],negative_count=196,all_negatives_reject_before_mutation=True,expected_manifest_batches=620,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered experimental V7324:620 expected batches/114 accepted. All earlier profiles andmainV4701 preserved.')
