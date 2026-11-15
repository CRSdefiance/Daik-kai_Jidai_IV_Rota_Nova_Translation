"""Register the complete91-object B48 stage after verified V8013, without promotion."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import rafael_B48_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Rafael_B48_release_paths_v8060 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_registration_v8065')
PROFILE='all-routes-unified-v8066'
VALIDATION=Path('work/analysis/Rafael_B48_atomic_challenges_v8064/atomic_validation_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and Path(owned.CONFIG).exists()
    result=read(VALIDATION);config=Path(result['config']);conf=read(config);cases=read(result['negative_cases'])
    assert result['positive_records']==91 and result['negative_count']==len(cases)==455
    assert result['all_negatives_reject_before_any_files_list_commit'] and result['config_dependency_digests_deliberately_bypassed']
    assert result['trusted_frozen_contract_read_once_revalidated_after_all_cases'] and result['all_semantic_guards_andcommit_traps_active']
    assert all(c['rejected'] and c['commit_calls']==0 for c in cases)
    assert sha(config.read_bytes())==result['config_sha256'] and sha(PARENT.read_bytes())==conf['parent_ROM_sha256']
    assert sha(Path(result['positive_proof']).read_bytes())==result['positive_proof_sha256']
    assert sha(Path(result['negative_cases']).read_bytes())==result['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v8045/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==636
    stage=b"""    rafael_B48_editorial_config = profile_config.get('rafael_B48_editorial')
    if rafael_B48_editorial_config:
        from dk4tool.patch.rafael_B48_editorial_v1 import apply_release as apply_rafael_B48_editorial

        rafael_B48_editorial_report = apply_rafael_B48_editorial(candidate, baseline, rafael_B48_editorial_config)
        for rafael_B48_editorial_file in rafael_B48_editorial_report['files']:
            rafael_B48_editorial_path = rafael_B48_editorial_file['file_path']
            grouped.setdefault(rafael_B48_editorial_path, [])
            changed_records.setdefault(rafael_B48_editorial_path, []).extend(row['id'] for row in rafael_B48_editorial_file['changed_records'])
            relocation_checks.setdefault(rafael_B48_editorial_path, {})['rafael_B48_editorial'] = {
                'release_config': rafael_B48_editorial_config,
                'release_config_sha256': sha256(Path(rafael_B48_editorial_config).read_bytes()),
                'proof': rafael_B48_editorial_report}
        for rafael_B48_editorial_manuscript in rafael_B48_editorial_report['manuscripts']:
            more_batch = Path(rafael_B48_editorial_manuscript)
            if more_batch in release_batches:
                raise ValueError('Rafael B48 must run once after the complete V8013 stack')
            release_batches.append(more_batch)

"""
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('rafael_B48_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('rafael_B47_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v8013'])
    profile.update(status='experimental',rafael_B48_editorial=owned.CONFIG,
        description='Complete V8013 plus Rafael B48:91 speeches,42 contextual revisions and49 justified retentions.',
        note="Whole clean Japanese exchange, B128/B37 callback context and nine source identities reviewed before current English;32 complete text paths. Preserve Athens banter, naturalist Hans Letzel, assistant Arcadius Eudoxios, unfamiliarity and acquaintance without invented kinship or identity reveal, seven regional treasures/ancient Seven Sages/maps, reported destiny, ambition and an uncertain southern African rumor. Four original system panels retain the complete joining name, Deck restriction, item information and X instruction. Original00/4B/71 selectors, one FI,163 commands/28 relatives/five raw predicates/two completion queries/three A000 effects and full end/inverses are preserved. Native91 paragraphs/92 pages;R347 alone has two original four-row pages with ordinary A18400 turn.37 original infos/two exact warning exceptions.343 loads/686 parent modes;91 policy positives/1454 guard rejections;whole-ROM atomic positive/455 independent precommit rejections. Paired disclosed original-entry fixtures80002 frames,78 actual speeches per language,486 complete holds,31 viewed sheets;six headers actual/three native-only and13 speeches native-only. Japanese R129 has a complete nineteenth-cell question mark;English remains216px. Normal returns22735/22973;preserve129 command/34 duration differences,English exit+63/final-393LCG phases,285/285 later RGB differences,persistent-object/actor differences,state/models/tasks/calendar equality and later fixture re-entry. No natural Athens activation,full route,hardware,complete causal orfuture-state equivalence claim. Full editorial goal/allfour stories/earlier dialogue/shared shops/towns/random/Help/wraps/all207names stay active;graphics andlater older-record technical re-audit separate. Preserve all prior ROMs/translations. MainV4701 unchanged;no separate unified package,promotion,pruning,commit orpush.")
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage)
    save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    temporary=builder.with_name('build_integrated_release_v8065.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v8013',
        parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        positive_proof=result['positive_proof'],negative_cases=result['negative_cases'],negative_count=455,
        all_negatives_reject_before_commit=True,expected_manifest_batches=637,accepted_layers=114,
        promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],
        producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimental V8066:637 expected batches/114 accepted;one new91-object manifest. Main/prior profiles preserved;no credit orpromotion.')
