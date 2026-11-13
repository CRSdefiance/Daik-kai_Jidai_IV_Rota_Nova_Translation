"""Register the complete28-object B50 stage after verified V8122, without promotion."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import rafael_B50_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Rafael_B50_release_paths_v8164 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_registration_v8171')
PROFILE='all-routes-unified-v8172'
VALIDATION=Path('work/analysis/Rafael_B50_atomic_challenges_v8170/atomic_validation_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and Path(owned.CONFIG).exists()
    result=read(VALIDATION);config=Path(result['config']);conf=read(config);cases=read(result['negative_cases'])
    assert result['positive_records']==28 and result['negative_count']==len(cases)==479
    assert result['all_negatives_reject_before_any_files_list_commit'] and result['config_dependency_digests_deliberately_bypassed']
    assert result['trusted_frozen_contract_read_once_revalidated_after_all_cases'] and result['all_semantic_guards_andcommit_traps_active']
    assert all(c['rejected'] and c['commit_calls']==0 for c in cases)
    assert sha(config.read_bytes())==result['config_sha256'] and sha(PARENT.read_bytes())==conf['parent_ROM_sha256']
    assert sha(Path(result['positive_proof']).read_bytes())==result['positive_proof_sha256']
    assert sha(Path(result['negative_cases']).read_bytes())==result['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v8166/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==638
    stage=b"""    rafael_B50_editorial_config = profile_config.get('rafael_B50_editorial')
    if rafael_B50_editorial_config:
        from dk4tool.patch.rafael_B50_editorial_v1 import apply_release as apply_rafael_B50_editorial

        rafael_B50_editorial_report = apply_rafael_B50_editorial(candidate, baseline, rafael_B50_editorial_config)
        for rafael_B50_editorial_file in rafael_B50_editorial_report['files']:
            rafael_B50_editorial_path = rafael_B50_editorial_file['file_path']
            grouped.setdefault(rafael_B50_editorial_path, [])
            changed_records.setdefault(rafael_B50_editorial_path, []).extend(row['id'] for row in rafael_B50_editorial_file['changed_records'])
            relocation_checks.setdefault(rafael_B50_editorial_path, {})['rafael_B50_editorial'] = {
                'release_config': rafael_B50_editorial_config,
                'release_config_sha256': sha256(Path(rafael_B50_editorial_config).read_bytes()),
                'proof': rafael_B50_editorial_report}
        for rafael_B50_editorial_manuscript in rafael_B50_editorial_report['manuscripts']:
            more_batch = Path(rafael_B50_editorial_manuscript)
            if more_batch in release_batches:
                raise ValueError('Rafael B50 must run once after the complete V8122 stack')
            release_batches.append(more_batch)

"""
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('rafael_B50_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('rafael_B49_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v8122'])
    profile.update(status='experimental',rafael_B50_editorial=owned.CONFIG,description='Complete V8122 plus Rafael B50:28 speeches,13 contextual revisions and15 justified retentions.',note='Complete V8122 plus B50:28 complete clean-first contextual decisions,13revisions/15justified retentions. Three source identities;complete13-speech LilB131dye/map callback andfive openingtitle references precede currentEnglish. Keep awkward acknowledgment,dye/decipheringkey,future nonuse,long-time-no-see,personal lifechange,polite surname/given address,besteffort andfinal unknown-celebration joke. No newCommander rank,relationship,marriage,pregnancy,retirement,occupation orowned parchment inferred. ApprovedRafael/Camille preserved. All37commands/nine nontextcontrols/zero relative-predicate-querysites/FA2FI1/fullend/inverses remain;onlyB50 changes. All28singlepages216px/fourrows,source00/02/09/ten00objects,20fresh92reused native and60fresh52reused stored alignments/15tails. All18infos/two exactwarningsR61the/North,R114to/live retained;no narrowedglobalwidth orweakened guards. 343native loads/cachepaths/686parentmodes/shippedcallercensus,28policypositives/511expectedguardrejections and479independentprecommit proofcorruptiontests. Paired initialized fullscene32002frames/all28speeches/pages/37commands plus10originalinitializers/184completebody-nameholds/allthreeactualheaders;14actualsheets viewed. RedDye card appearance/hide,4821/A000/4720/4681 originalbodies/60-240-0-88durations/normalreturn pass. No opacitybridge orstate forcing. Exits10822/10824,35comparisonrows/11durationdifferences;firstphaseoffset350duration237/241steps57/58,exitLCG+2/final-10,seeds3888306843/2225786845. Seventeenof87lateRGBsamples differ,finalstate/tasks/calendar equal,models/persistentobjects/actor differ. Focused same-input repeat32002moreframes:allobserverrows/framebuffers/finalRAM reproducible. Sevenearly/postreturn/tutorial/departure sampledcomponents/wholeactors equal through15550;underway16000twofleet/oneship/105actor/twotownbytes differ. Rawcalendar185/[0,3,41]uninterpreted;noeveryframecausaltrace,futurestate orbroad simulationequivalence claim. SourceJapanese ontranslatedUI/names,initializedLisbonfixture notnatural event50activation/originallocation/earnedprogress/fullroute/hardware. Allfourstories/earlierdialogue/sharedshop-town/random/Help/remainingprose/207names/retrospectivewraps remainactive. Graphics/all18plaques andlaterolder-recordtechnicalre-audit separate;preserveallROMs/translations/proofs/failures. MainV4701 unchanged;no separateunifiedtestpackage,promotion,pruning,commit orpush.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage)
    save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    temporary=builder.with_name('build_integrated_release_v8171.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v8122',
        parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        positive_proof=result['positive_proof'],negative_cases=result['negative_cases'],negative_count=479,
        all_negatives_reject_before_commit=True,expected_manifest_batches=639,accepted_layers=114,
        promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],
        producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimental V8172:639 expected batches/114 accepted;one new28-object manifest. Main/prior profiles preserved;no credit orpromotion.')
