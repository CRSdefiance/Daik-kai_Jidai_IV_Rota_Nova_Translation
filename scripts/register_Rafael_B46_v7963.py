"""Register all26 B46 decisions after the complete V7911 stack, retaining both manifests."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import rafael_B46_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Rafael_B46_release_paths_v7958 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_registration_v7963')
PROFILE='all-routes-unified-v7964'
VALIDATION=Path('work/analysis/Rafael_B46_atomic_challenges_v7962/atomic_validation_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and Path(owned.CONFIG).exists()
    result=read(VALIDATION);config=Path(result['config']);conf=read(config);cases=read(result['negative_cases'])
    assert result['positive_records']==26 and result['negative_count']==len(cases)==187
    assert result['all_negatives_reject_before_any_files_list_commit'] and result['config_dependency_digests_deliberately_bypassed']
    assert all(c['rejected'] and c['commit_calls']==0 for c in cases)
    assert sha(config.read_bytes())==result['config_sha256'] and sha(PARENT.read_bytes())==conf['parent_ROM_sha256']
    assert sha(Path(result['positive_proof']).read_bytes())==result['positive_proof_sha256']
    assert sha(Path(result['negative_cases']).read_bytes())==result['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7955/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==633
    stage=b"""    rafael_B46_editorial_config = profile_config.get('rafael_B46_editorial')
    if rafael_B46_editorial_config:
        from dk4tool.patch.rafael_B46_editorial_v2 import apply_release as apply_rafael_B46_editorial

        rafael_B46_editorial_report = apply_rafael_B46_editorial(candidate, baseline, rafael_B46_editorial_config)
        for rafael_B46_editorial_file in rafael_B46_editorial_report['files']:
            rafael_B46_editorial_path = rafael_B46_editorial_file['file_path']
            grouped.setdefault(rafael_B46_editorial_path, [])
            changed_records.setdefault(rafael_B46_editorial_path, []).extend(row['id'] for row in rafael_B46_editorial_file['changed_records'])
            relocation_checks.setdefault(rafael_B46_editorial_path, {})['rafael_B46_editorial'] = {
                'release_config': rafael_B46_editorial_config,
                'release_config_sha256': sha256(Path(rafael_B46_editorial_config).read_bytes()),
                'proof': rafael_B46_editorial_report}
        for rafael_B46_editorial_manuscript in rafael_B46_editorial_report['manuscripts']:
            more_batch = Path(rafael_B46_editorial_manuscript)
            if more_batch in release_batches:
                raise ValueError('Rafael B46 must run once after the complete V7911 stack')
            release_batches.append(more_batch)

"""
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('rafael_B46_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('rafael_B45_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7911'])
    profile.update(status='experimental',rafael_B46_editorial=owned.CONFIG,
        description="Complete V7911 plus Rafael B46:24 speeches andtwo choices;seven source-grounded revisions andnineteen contextual retentions.",
        note="Fresh clean Japanese/B38 prerequisite andwhole conditional exchange before current comparison. Rafael Castor,Claudio Manaus,Julio Erneco retained from scoped source getters. Hayreddin component retention;full207 name review remains open. Accepting plays22speeches including12FE panels;declining plays7;both share unfinished private thought. Exact Y/L/R/A instructions,opposite mode orders,icons,city/fleet targets,land inside search frame,no invented kinship/rank/ambition/guaranteed discovery. Automatic full216px usable body width;FE228bitmap distinct;24full pages/96alignments,44fresh stored52reused,14original row-count infos/no waivers;native66px two-choice captions without padding. All37commands/five A000/6300/61FF/four relative spans,complete preambles/source00/zero macros andfull end/inverses preserved.343loads/686parent modes. Four disclosed original-entry fixtures,64004frames,58speech occurrences/214holds;all24unique speech/all37command union each language,original menu[2,0]/[2,1],normal[0,0]/[0,1].Source accept4930 highlight-off retained;no phase equality claim. Preserve27/12comparison rows,6/2duration differences;English+1LCGstep at B46 exits,later-159/-316,41/113 and96/173RGB differences;models,persistent objects,actors differ,accept calendar differs. No future-state/full simulation/complete causal equivalence.24policy positives/two labels/300rejections;whole-ROM atomic positive/187 independent precommit rejections. Two manifest batches include26objects exactly once. Fullgoal active;allfour stories/earlier prose,shared shops/towns/random/Help,retrospective wraps/names open;graphics/later older-record re-audit separate. MainV4701 unchanged;no separate unified package,promotion,pruning,commit orpush.")
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage)
    save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    temporary=builder.with_name('build_integrated_release_v7963.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7911',
        parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        positive_proof=result['positive_proof'],negative_cases=result['negative_cases'],negative_count=187,
        all_negatives_reject_before_commit=True,expected_manifest_batches=635,accepted_layers=114,
        promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],
        producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimental V7964:635 expected batches/114 accepted;two new manifests for26objects. Main/prior profiles preserved;no credit orpromotion.')
