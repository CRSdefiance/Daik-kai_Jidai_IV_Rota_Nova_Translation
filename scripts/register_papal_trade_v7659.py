"""Append the two sealed exchanges after all V7611 layers; preserve every prior profile."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import papal_trade_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_final_paths_v7655 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_registration_v7659')
PROFILE='all-routes-unified-v7660'
VALIDATION=Path('work/analysis/papal_trade_atomic_challenges_v7658/atomic_validation_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();r=read(VALIDATION);config=Path(r['config']);conf=read(config);cases=read(r['negative_cases'])
    assert r['positive_records']==36 and r['negative_count']==len(cases)==148 and all(c['rejected'] and c['commit_calls']==0 for c in cases) and r['all_negatives_reject_before_any_files_list_commit']
    assert r['all_dependency_digests_deliberately_bypassed'] and sha(config.read_bytes())==r['config_sha256'] and sha(PARENT.read_bytes())==r['parent_ROM_sha256'] and sha(Path(r['negative_cases']).read_bytes())==r['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7654/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(PARENT.with_suffix('.manifest.json'))['batches'])==626
    stage=b'''    papal_config = profile_config.get('papal_trade_editorial')
    if papal_config:
        from dk4tool.patch.papal_trade_editorial_v1 import apply_release as apply_papal_trade

        papal_report = apply_papal_trade(candidate, baseline, papal_config)
        for papal_file in papal_report['files']:
            papal_path = papal_file['file_path']
            grouped.setdefault(papal_path, [])
            changed_records.setdefault(papal_path, []).extend(row['id'] for row in papal_file['changed_records'])
            relocation_checks.setdefault(papal_path, {})['papal_trade_editorial'] = {
                'release_config': papal_config,
                'release_config_sha256': sha256(Path(papal_config).read_bytes()),
                'proof': papal_report}
        for papal_manuscript in papal_report['manuscripts']:
            more_batch = Path(papal_manuscript)
            if more_batch in release_batches:
                raise ValueError('Papal trade must run once after the complete V7611 stack')
            release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('papal_trade_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('lil_B234_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7611'])
    profile.update(status='experimental',papal_trade_editorial=owned.CONFIG,description='Complete V7611 plus36 clean-Japanese whole-exchange SC0B246 Rafael/SC1B237 Hodram decisions:26 revisions/10 justified retentions. Preserve Carlo/Filippo familiarity,unspecified tentative recovery,aboard-ship fact,great-grandfather,papal direct rule/donations/trade decline,reported occasional finds,prospective blessings andconditional discovery. Carlo Sinat/Trader remain scoped name retentions;Filippo is a spoken body address,European excluded from returned names,anditem106 remains unchanged. Both source1468/logical1468/tail0 blocks invert exactly;target1508/logical1506/tail2 preserves20 commands18 complete preambles,A0001456->1494/end1464->1502 perroute. One final files-list commit follows both complete reconstructions.',note='All36 paragraphs retain one original216x64/four-row page.288 fresh logical/compiled alignments,144 stored alignments(64 fresh/80 exact reuse),16 zero-ink parity tails,two exactR33 article continuations and16 row infos preserve all base QA. Policy36 positives174 changed-input rejects andproduction36-record positive148 changed-input rejects pass before commit.668 native loads1336 entry modes andshipped caller census bind both resized archives. Four16001-frame disclosed original-route initialized fixtures cover all18 speeches perroute/language:63 Rafael and70 Hodram complete body/name holds each,zero sampled partial holds,normal returns andall36 source/English scene/portrait/header pairs. All72 panes17 sheets viewed. Exits8095/8094 inboth routes;all19 command-difference rows/seven durations each remain. LaterRGB differs3/133 Rafael,53/133 Hodram;Hodram models/persistent objects/actors andRNG differ. Preserve every measured limit;no fullRAM,everyframe,future,broad simulation orcausal equivalence claim. Fixtures do not prove natural optional activation,original location,earned progress,full effects,routes orhardware. Keep all207 names/earlier prose/wrap review open,all prior artifacts andfailures,graphics separate andlater technical re-audit. MainV4701 unchanged;no separate test package,promotion,pruning,commit orpush.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v7659.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7611',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=r['positive_proof'],negative_cases=r['negative_cases'],negative_count=148,all_negatives_reject_before_commit=True,expected_manifest_batches=628,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimental V7660:628 expected batches/114 accepted;all prior profiles andmainV4701 unchanged.')
