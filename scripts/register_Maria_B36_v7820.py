"""Register one sealed Maria B36 layer after V7779, preserving every previous profile andmain."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import maria_B36_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Maria_B36_final_paths_v7816b import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B36_registration_v7820')
PROFILE='all-routes-unified-v7821'
VALIDATION=Path('work/analysis/maria_B36_atomic_challenges_v7819/atomic_validation_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    result=read(VALIDATION);config=Path(result['config']);conf=read(config);cases=read(result['negative_cases'])
    assert result['positive_records']==16 and result['negative_count']==len(cases)==120
    assert result['all_negatives_reject_before_any_files_list_commit'] and result['all_dependency_digests_deliberately_bypassed']
    assert all(c['rejected'] and c['commit_calls']==0 for c in cases)
    assert sha(config.read_bytes())==result['config_sha256'] and sha(PARENT.read_bytes())==result['parent_ROM_sha256']
    assert sha(Path(result['negative_cases']).read_bytes())==result['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7817d/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==630
    stage=b"""    maria_B36_config = profile_config.get('maria_B36_editorial')
    if maria_B36_config:
        from dk4tool.patch.maria_B36_editorial_v1 import apply_release as apply_maria_B36

        maria_B36_report = apply_maria_B36(candidate, baseline, maria_B36_config)
        for maria_B36_file in maria_B36_report['files']:
            maria_B36_path = maria_B36_file['file_path']
            grouped.setdefault(maria_B36_path, [])
            changed_records.setdefault(maria_B36_path, []).extend(row['id'] for row in maria_B36_file['changed_records'])
            relocation_checks.setdefault(maria_B36_path, {})['maria_B36_editorial'] = {
                'release_config': maria_B36_config,
                'release_config_sha256': sha256(Path(maria_B36_config).read_bytes()),
                'proof': maria_B36_report}
        for maria_B36_manuscript in maria_B36_report['manuscripts']:
            more_batch = Path(maria_B36_manuscript)
            if more_batch in release_batches:
                raise ValueError('Maria B36 must run once after the complete V7779 stack')
            release_batches.append(more_batch)

"""
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('maria_B36_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('maria_story_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7779'])
    profile.update(status='experimental',maria_B36_editorial=owned.CONFIG,
        description="Complete V7779 plus16 clean-Japanese whole-exchange decisions for Maria's confrontation with Lil, SC3B36:9 revisions and7 individually justified retentions. Preserve differing beliefs about Kuhn, Southeast Asia's people, the underworld accusation, intended betrayal, fear, proof challenge, refusal and exasperation. Preserve original FO-before-FI order naturally; no invented rank, kinship, romance, attack, rescue, method, deadline, reconciliation or guaranteed mechanic.",
        note='All16 native single pages,64 logical/compiled/stored alignment cases,11 zero-ink parity tails,9 individual row-count infos andno warnings/waivers. Three actors2/3/10,six getters,FI2/FO1 andscopedFI5/FA2/FO7;Lil/Maria/Xien progressive headers areobserved,fullcatalogueUI/full207/shared151-159 semantics remainopen. All22 commands/six numeric leaves,6000/633D/623D/632A/A000/fourbyte end,fullclean/predecessor block andarchive inverse;302 otherSC3 blocks/allotherfiles/components exact. Original303native loads606parentmodes andcaller census bound. Paired16001-frame initialized source/English fixtures playall16 speeches/29commands each:32complete panes,132complete body+header holds,zero partials/unknowns/unplayed. Allsource andEnglish black/ASCII-gray/CP932-gray/name masks,16upperRGBpairs andresults/UI agree. Preserveexits8213/8216,18command/sixduration rows,108/131lateRGBdifferences,allrawRNG/component/calendar/actor/after-scene measurements andno broad equivalence claim. Existingexactsystem-onlyunlock isdisclosed,earned=false;initializedHangzhou return8300 isnot naturaloptional location/activation/fullmechanics/routes/hardware.16positive/81policyrejections;oneatomicpositive/120actual-changingproductionrejections withdependencychecks bypassed andno negative commits. Allprior drafts,producer failures,proofs,traces,ROMs,profiles,fullobjective,graphicsseparation andlatertechnicalaudit preserved.MainV4701unchanged;no separatepackage,promotion,pruning,commit orpush.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage)
    save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf)
    temporary=builder.with_name('build_integrated_release_v7778.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7779',
        parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        positive_proof=result['positive_proof'],negative_cases=result['negative_cases'],negative_count=120,
        all_negatives_reject_before_commit=True,expected_manifest_batches=631,accepted_layers=114,
        promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],
        producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimentalV7821:631expectedbatches/114accepted;all prior profiles/mainV4701 preserved.No credit orpromotion.')
