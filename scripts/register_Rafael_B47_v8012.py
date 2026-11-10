"""Register fifteen B47 decisions after the complete V7964 stack."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import rafael_B47_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Rafael_B47_release_paths_v8006 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_registration_v8012')
PROFILE='all-routes-unified-v8013'
VALIDATION=Path('work/analysis/Rafael_B47_atomic_challenges_v8011/atomic_validation_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and Path(owned.CONFIG).exists()
    result=read(VALIDATION);config=Path(result['config']);conf=read(config);cases=read(result['negative_cases'])
    assert result['positive_records']==15 and result['negative_count']==len(cases)==202
    assert result['all_negatives_reject_before_any_files_list_commit'] and result['config_dependency_digests_deliberately_bypassed']
    assert all(c['rejected'] and c['commit_calls']==0 for c in cases)
    assert sha(config.read_bytes())==result['config_sha256'] and sha(PARENT.read_bytes())==conf['parent_ROM_sha256']
    assert sha(Path(result['positive_proof']).read_bytes())==result['positive_proof_sha256']
    assert sha(Path(result['negative_cases']).read_bytes())==result['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v8008/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==635
    stage=b"""    rafael_B47_editorial_config = profile_config.get('rafael_B47_editorial')
    if rafael_B47_editorial_config:
        from dk4tool.patch.rafael_B47_editorial_v1 import apply_release as apply_rafael_B47_editorial

        rafael_B47_editorial_report = apply_rafael_B47_editorial(candidate, baseline, rafael_B47_editorial_config)
        for rafael_B47_editorial_file in rafael_B47_editorial_report['files']:
            rafael_B47_editorial_path = rafael_B47_editorial_file['file_path']
            grouped.setdefault(rafael_B47_editorial_path, [])
            changed_records.setdefault(rafael_B47_editorial_path, []).extend(row['id'] for row in rafael_B47_editorial_file['changed_records'])
            relocation_checks.setdefault(rafael_B47_editorial_path, {})['rafael_B47_editorial'] = {
                'release_config': rafael_B47_editorial_config,
                'release_config_sha256': sha256(Path(rafael_B47_editorial_config).read_bytes()),
                'proof': rafael_B47_editorial_report}
        for rafael_B47_editorial_manuscript in rafael_B47_editorial_report['manuscripts']:
            more_batch = Path(rafael_B47_editorial_manuscript)
            if more_batch in release_batches:
                raise ValueError('Rafael B47 must run once after the complete V7964 stack')
            release_batches.append(more_batch)

"""
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('rafael_B47_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('rafael_B46_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7964'])
    profile.update(status='experimental',rafael_B47_editorial=owned.CONFIG,
        description="Complete V7964 plus Rafael B47:15 speeches;eight source-grounded revisions andseven contextual retentions.",
        note="Clean Japanese/B37 prerequisite,whole conditional exchange andsource-bound glosses before current English. Rafael Castor,Janus Pasar,Claudio Manaus,Julio Erneco retained;Pasar is distinct from Pasha. Valdes/Pasha/Hayreddin component-only retentions;full207 review remains open. Preserve guarded Mediterranean passage,eastern-half Ottoman territory,conditional enemy initiative,qualified recruitment,cautious trading,ship/personal preparation andrenewed resolve. Automatic216px/four-row geometry;15 paragraphs/16 pages,R53 alone two pages withordinary A4720 transition andfollowing R70. Six original infos/two exact source/text/compiled/line-bound warning exceptions;R5/R63 fuller three-row wrapping without word loss. All48 commands/24 relatives/six raw predicates/61FF/A000/fullend andcomplete preambles/source00/zero macros/inverses preserved.343 loads/686parent modes. Two disclosed original-entry fixture runs32002frames,11actual speeches each language/88complete holds;eight viewed sheets.Four conditional speeches/Janus header native-only. Normal[0,0] at6416/6655. Preserve24command/four duration differences,English+58LCGsteps at exit,later-7833,157/157laterRGBdifferences,models/persistent objects/actors/calendar differences andallrawmeasurements. No natural activation,fullroute,hardware,future-state/fullsimulation/completecausal claim.15policy positives/302guard rejections;whole-ROM atomic positive/202independent precommit rejections. One manifest batch includes15objects once. Fullgoal/allfour stories/earlier dialogue/shared shops/towns/random/Help/wraps/names remain active;graphics/later older-record re-audit separate. MainV4701 unchanged;no separate unified package,promotion,pruning,commit orpush.")
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage)
    save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    temporary=builder.with_name('build_integrated_release_v8012.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7964',
        parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        positive_proof=result['positive_proof'],negative_cases=result['negative_cases'],negative_count=187,
        all_negatives_reject_before_commit=True,expected_manifest_batches=635,accepted_layers=114,
        promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],
        producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimental V7964:635 expected batches/114 accepted;two new manifests for26objects. Main/prior profiles preserved;no credit orpromotion.')
