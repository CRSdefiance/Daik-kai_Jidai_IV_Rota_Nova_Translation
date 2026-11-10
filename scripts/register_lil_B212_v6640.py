"""Append the approved B212 exchange after the complete V6584 registered stack."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B212_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B212_registration_v6640');PROFILE='all-routes-unified-v6641';VALIDATION=Path('work/analysis/lil_B212_atomic_v6639');PARENT=Path('out/all_routes_combined_v6584_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();receipt=read(VALIDATION/'atomic_validation_receipt.json');config=Path(receipt['config']);conf=read(config);assert receipt['positive_records']==14 and receipt['negative_count']==86 and receipt['all_negatives_reject_before_mutation'] and receipt['seven_actual_speeches_five_labels_two_offline_alternatives_bound'];assert sha(config.read_bytes())==receipt['config_sha256'] and sha(PARENT.read_bytes())==receipt['parent_ROM_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v6617/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256'];rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp);assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(PARENT.with_suffix('.manifest.json'))['batches'])==603
    stage=b'''    lil_proof = profile_config.get('lil_B212_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B212_editorial_v2 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B212_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B212 must run once after the complete V6584 stack')
        release_batches.append(more_batch)

''';anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B212_editorial')" not in before;after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert after.index(b"profile_config.get('lil_B211_editorial')")<after.index(stage)<after.index(anchor);profile=deepcopy(registry['profiles']['all-routes-unified-v6584']);profile.update(status='experimental',lil_B212_editorial=owned.CONFIG,description='Complete V6584 plus14 Lil B212 whole-exchange decisions:11 revisions/3 justified retentions. Nine Guildmaster speeches/five typed choices preserve Romance of the Three Kingdoms,full Zhao Yun/Guan Yu/Zhuge Liang identities,the source Changban Bridge rescue,qualified spear rumor,failed search andtentative hope. No invented Uncle kinship,rank,named peninsula/spear or guaranteed find. All26commands/10relative spans/2A000/3exact ends,complete884-byte inverse,target980bytes. Nine original single pages,72logical/compiled+36stored alignments,20menu planes andactual7speeches/5labels;two alternatives offline. FullGuildmaster retention,noasset/duplicatecredit. Actual256x36backing/allthreegeneralhighlights andnormal residual1 versus flagged state1/value0 verified;6533unownedbackingdifferences,timing/RGB/following-scene limits retained. Full editorial and207-name/role/alias scope active;graphics/later older-record re-audit separate.',note='86 independent semantic release rejections and65 layout-policy rejections pass. Preserved failed v1 proof-schema guard andsource-lockedv2 correction. Representative conditional coverage follows user instruction; clean-input patch/current startup pending. MainV4701 unchanged.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode();ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated);assert rp.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v6640.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before;save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v6584',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscript=conf['manuscript'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=receipt['positive_proof'],negative_cases=receipt['negative_cases'],negative_count=86,all_negatives_reject_before_mutation=True,expected_manifest_batches=604,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Registered experimental V6641:604 expected batches/114 accepted;all earlier profiles/mainV4701 preserved.')
