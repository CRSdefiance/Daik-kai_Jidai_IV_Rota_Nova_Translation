"""Append B228 after the complete registered V7324 without changing promotion."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B228_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B228_registration_v7370');PROFILE='all-routes-unified-v7371'
VALIDATION=Path('work/analysis/lil_B228_atomic_v7369');PARENT=Path('out/all_routes_combined_v7324_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();r=read(VALIDATION/'atomic_validation_receipt.json');config=Path(r['config']);conf=read(config);cases=read(r['negative_cases'])
    assert r['positive_records']==13 and r['negative_count']==len(cases)==212 and all(c['rejected'] and c['archive_writes']==0 for c in cases) and r['all_negatives_reject_before_mutation'] and r['all13_actual13_pages51_body51_headers_bound'] and r['original_A00025_ends_and_explicit_comparison_limits_bound']
    assert sha(config.read_bytes())==r['config_sha256'] and sha(PARENT.read_bytes())==r['parent_ROM_sha256'] and sha(Path(r['negative_cases']).read_bytes())==r['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7366/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(PARENT.with_suffix('.manifest.json'))['batches'])==620
    stage=b'''    lil_proof = profile_config.get('lil_B228_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B228_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B228_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B228 must run once after the complete V7324 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B228_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert after.index(b"profile_config.get('lil_B227_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7324']);profile.update(status='experimental',lil_B228_editorial=owned.CONFIG,description='Complete V7324 plus13 clean-Japanese whole-exchange B228 decisions: six revisions andseven justified retentions. Preserve the armadillo-hide shield hearsay,source-bound Armadillo Hide item50 name,vague Africa clue,familiar teasing,practical objection,Lil personal remembrance andluck-dependent reassurance. Lil Argot andSamwell Khan progressive headers are retained;Samwell ダ Khan catalog middle remains unapproved. Source760/logical758/tail2 fully inverts;target744/logical744/tail0. All15 commands/13 preambles,selectors2/22,voices3/2,zero macros,A000746->732 andfour-byte end754->740 remain. Thirteen native pages,104 logical/compiled52 stored32 name alignments,six zero-ink tails,five row reasons andzero warnings/waivers preserve all base QA.',note='Thirteen policy positives/62 rejections and212 actual-changing production corruptions pass before the sole archive write. All24 observed commands,13 scene/portrait pairs,51 body/header holds andnormal return5973 pass. Measured timing/results/UI/RNG,all167 later RGB samples,five final components andwhole actors agree,with explicit scope limits. Initialized B22 isnot natural228 activation,original location,earned progress,full effects,routes orhardware. No whole-RAM/every-frame/future/broad-simulation orcomplete causal claim. All207 names,other item50 route consumers,earlier wrapping andthe full editorial objective remain open. All artifacts andmainV4701 preserved;exact patch/current startup pending;no automatic promotion.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v7370.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7324',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscript=conf['manuscript'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=r['positive_proof'],negative_cases=r['negative_cases'],negative_count=212,all_negatives_reject_before_mutation=True,expected_manifest_batches=621,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered experimental V7371:621 expected batches/114 accepted. All earlier profiles andmainV4701 preserved.')
