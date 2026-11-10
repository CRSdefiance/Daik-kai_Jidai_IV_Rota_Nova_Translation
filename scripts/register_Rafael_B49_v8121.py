"""Register the complete61-object B49 stage after verified V8066, without promotion."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import rafael_B49_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Rafael_B49_release_paths_v8114 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_registration_v8121')
PROFILE='all-routes-unified-v8122'
VALIDATION=Path('work/analysis/Rafael_B49_atomic_challenges_v8120/atomic_validation_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and Path(owned.CONFIG).exists()
    result=read(VALIDATION);config=Path(result['config']);conf=read(config);cases=read(result['negative_cases'])
    assert result['positive_records']==61 and result['negative_count']==len(cases)==413
    assert result['all_negatives_reject_before_any_files_list_commit'] and result['config_dependency_digests_deliberately_bypassed']
    assert result['trusted_frozen_contract_read_once_revalidated_after_all_cases'] and result['all_semantic_guards_andcommit_traps_active']
    assert all(c['rejected'] and c['commit_calls']==0 for c in cases)
    assert sha(config.read_bytes())==result['config_sha256'] and sha(PARENT.read_bytes())==conf['parent_ROM_sha256']
    assert sha(Path(result['positive_proof']).read_bytes())==result['positive_proof_sha256']
    assert sha(Path(result['negative_cases']).read_bytes())==result['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v8116/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==637
    stage=b"""    rafael_B49_editorial_config = profile_config.get('rafael_B49_editorial')
    if rafael_B49_editorial_config:
        from dk4tool.patch.rafael_B49_editorial_v1 import apply_release as apply_rafael_B49_editorial

        rafael_B49_editorial_report = apply_rafael_B49_editorial(candidate, baseline, rafael_B49_editorial_config)
        for rafael_B49_editorial_file in rafael_B49_editorial_report['files']:
            rafael_B49_editorial_path = rafael_B49_editorial_file['file_path']
            grouped.setdefault(rafael_B49_editorial_path, [])
            changed_records.setdefault(rafael_B49_editorial_path, []).extend(row['id'] for row in rafael_B49_editorial_file['changed_records'])
            relocation_checks.setdefault(rafael_B49_editorial_path, {})['rafael_B49_editorial'] = {
                'release_config': rafael_B49_editorial_config,
                'release_config_sha256': sha256(Path(rafael_B49_editorial_config).read_bytes()),
                'proof': rafael_B49_editorial_report}
        for rafael_B49_editorial_manuscript in rafael_B49_editorial_report['manuscripts']:
            more_batch = Path(rafael_B49_editorial_manuscript)
            if more_batch in release_batches:
                raise ValueError('Rafael B49 must run once after the complete V8066 stack')
            release_batches.append(more_batch)

"""
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('rafael_B49_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('rafael_B48_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v8066'])
    profile.update(status='experimental',rafael_B49_editorial=owned.CONFIG,
        description='Complete V8066 plus Rafael B49:61 speeches,31 contextual revisions and30 justified retentions.',
        note="Complete clean Japanese exchange,22-speech B39 prerequisite and27-speech B41 destination context precede current English. Seven source speakers andthree mentioned identity components;256 complete structural text paths,156250 result compositions. Preserve Lil's blunt bravado,Camille's restraint,Rafael's mild perceptiveness,conditional Janus/Claudio alternatives,prospective regional ambition,unfinished Hodram Ber... something joke,surname-only Clifford,Martin Speyer/Hanseatic League,temporary trade request,proposed pact rather than completed alliance,common-enemy optional exchange andqualified closing. All154commands/56relative sites/13raw predicates/one completion query/sevenA000/C281/fullend andcomplete inverses remain. Original00/02/09 andseven selectors,twoFI,noFE,all61singlepages216px/four rows. Final native20fresh224reused,stored124fresh120reused;22original infos/three exact warning scopes.343load/cache paths/686parent modes,61policy positives/1014guard rejections,one final file-list commit exact full-reference positive and413independent precommit semantic rejects. Paired disclosed B44initialized-entry fixtures48002frames,50actual speeches/50pages perlanguage,318complete body/name holds,22directly viewed sheets. Actual headers Rafael,Lil,Claudio,Camille;three native-only headers andeleven native-only conditional speeches remain explicit. C281's original effect executes at4016-4017,2bytes,[3,0],equal UIrequests/no internal RNGadvance;transition/Lil/Camille names/return verified. Normal exits16013/16016;retain111comparisonrows/18duration differences,exitEnglishLCG+3/final+2,seeds3456469704/204362374. Final sampled state/models/persistent/tasks/calendar/wholeactor equal;19of134later fullRGB differ. No natural Amsterdam event49 activation,fullroute,hardware,every-call causal orfuture-state equivalence claim. Full editorial goal/allfourstories/earlier dialogue/sharedshop/town/random/Help/wraps/all207names remain active;graphics andlater older-record technical re-audit separate. Preserve allprior ROMs/translations. MainV4701 unchanged;no separate unified package,promotion,pruning,commit orpush.")
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage)
    save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    temporary=builder.with_name('build_integrated_release_v8121.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v8066',
        parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        positive_proof=result['positive_proof'],negative_cases=result['negative_cases'],negative_count=413,
        all_negatives_reject_before_commit=True,expected_manifest_batches=638,accepted_layers=114,
        promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],
        producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimental V8122:638 expected batches/114 accepted;one new61-object manifest. Main/prior profiles preserved;no credit orpromotion.')
