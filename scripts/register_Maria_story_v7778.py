"""Register one sealed Maria67 layer after V7717, preserving every previous profile andmain."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import maria_story_editorial_v3 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Maria_story_final_paths_v7771 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_registration_v7778')
PROFILE='all-routes-unified-v7779'
VALIDATION=Path('work/analysis/maria_story_atomic_challenges_v7776/atomic_validation_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    result=read(VALIDATION);config=Path(result['config']);conf=read(config);cases=read(result['negative_cases'])
    assert result['positive_records']==67 and result['negative_count']==len(cases)==256
    assert result['all_negatives_reject_before_any_files_list_commit'] and result['all_dependency_digests_deliberately_bypassed']
    assert all(c['rejected'] and c['commit_calls']==0 for c in cases)
    assert sha(config.read_bytes())==result['config_sha256'] and sha(PARENT.read_bytes())==result['parent_ROM_sha256']
    assert sha(Path(result['negative_cases']).read_bytes())==result['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7774/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==629
    stage=b"""    maria_story_config = profile_config.get('maria_story_editorial')
    if maria_story_config:
        from dk4tool.patch.maria_story_editorial_v3 import apply_release as apply_maria_story

        maria_story_report = apply_maria_story(candidate, baseline, maria_story_config)
        for maria_story_file in maria_story_report['files']:
            maria_story_path = maria_story_file['file_path']
            grouped.setdefault(maria_story_path, [])
            changed_records.setdefault(maria_story_path, []).extend(row['id'] for row in maria_story_file['changed_records'])
            relocation_checks.setdefault(maria_story_path, {})['maria_story_editorial'] = {
                'release_config': maria_story_config,
                'release_config_sha256': sha256(Path(maria_story_config).read_bytes()),
                'proof': maria_story_report}
        for maria_story_manuscript in maria_story_report['manuscripts']:
            more_batch = Path(maria_story_manuscript)
            if more_batch in release_batches:
                raise ValueError('Maria67 must run once after the complete V7717 stack')
            release_batches.append(more_batch)

"""
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('maria_story_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('maria_B207_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7717'])
    profile.update(status='experimental',maria_story_editorial=owned.CONFIG,
        description='Complete V7717 plus67 whole-exchange clean-Japanese Maria SC3B34/B108/B35 decisions:48 revisions/19 justified retentions. Preserve political exploitation,East/Southeast Asia distinctions,injured informant,moral discomfort,false Argot trade allegation,reported justice/anger,conditional risks,andMaria personal safety promise. PreserveHodram/Bergstrom,approvedCamille,hisexplicitnonmembershipintheSwedishfleet,unspecifiedclosenesstoLil,temporaryseparatetravel,tentativeBataviawhereabouts,andunexplainedpresentreluctance. Noinventedromance,rank,kinship,commodity,locationorcompletedmechanic.',
        note='67 native singlepages/22 row-count infos/no warnings orwaivers;268 final logical/compiled/stored alignments,33 zero-ink paritytails,12 original substitutions withscopedFI5/FA2/FO7. All116commands/20relative sites/100targetcases,303whole loads606parentmodes,source/current/gloss/effective/native/stored/actual references andfullclean/predecessor inverse pass. Final paired initializedfixturescover65speeches eachlanguage/130completepages/528body+headerholds;twoJulianconditionals offlineonly. Fourunchangedactualgroupsreusedbyexacthash,twochangedEnglishgroupsfresh. All65upperRGBpairsandresults/UI match. Preserveallcommand/duration/RNG/actor/component/calendar/lateRGB differences andnormaltype0valuecarry/source-onlyR65rightcellfindings. Existingexactsystem-onlyunlockisdisclosed,earned=false;notnaturaloptionallocation/activation/fullroutes/fullmechanics/hardware.67positive/200policyrejections;oneatomicpositive/256actual-changingproductionrejectionswithdependencychecks bypassed,zero commits innegativecases. Full207names/shared155Sailor-Retainerwordingandbroaderconsumers remainopen;no nameassetchange. Fullgoal/previousfamilies/town-random/Help/prose/retrospectivewraps/graphicsseparation/latertechnicalauditpreserved.MainV4701unchanged;noseparatepackage,promotion,pruning,commitorpush.')
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
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7717',
        parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        positive_proof=result['positive_proof'],negative_cases=result['negative_cases'],negative_count=256,
        all_negatives_reject_before_commit=True,expected_manifest_batches=630,accepted_layers=114,
        promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],
        producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimentalV7779:630expectedbatches/114accepted;all prior profiles/mainV4701 preserved.No credit orpromotion.')
