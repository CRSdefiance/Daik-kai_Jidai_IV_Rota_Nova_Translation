"""Register the approved twelve-speech Rafael B45 layer after the complete V7857 stack."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import rafael_B45_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Rafael_B45_release_paths_v7903 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_registration_v7910')
PROFILE='all-routes-unified-v7911'
VALIDATION=Path('work/analysis/Rafael_B45_atomic_challenges_v7909/atomic_validation_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and Path(owned.CONFIG).exists()
    result=read(VALIDATION);config=Path(result['config']);conf=read(config);cases=read(result['negative_cases'])
    assert result['positive_records']==12 and result['negative_count']==len(cases)==131
    assert result['all_negatives_reject_before_any_files_list_commit'] and result['config_dependency_digests_deliberately_bypassed']
    assert all(c['rejected'] and c['commit_calls']==0 for c in cases)
    assert sha(config.read_bytes())==result['config_sha256'] and sha(PARENT.read_bytes())==conf['parent_ROM_sha256']
    assert sha(Path(result['positive_proof']).read_bytes())==result['positive_proof_sha256']
    assert sha(Path(result['negative_cases']).read_bytes())==result['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7900/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==632
    stage=b"""    rafael_B45_editorial_config = profile_config.get('rafael_B45_editorial')
    if rafael_B45_editorial_config:
        from dk4tool.patch.rafael_B45_editorial_v2 import apply_release as apply_rafael_B45_editorial

        rafael_B45_editorial_report = apply_rafael_B45_editorial(candidate, baseline, rafael_B45_editorial_config)
        for rafael_B45_editorial_file in rafael_B45_editorial_report['files']:
            rafael_B45_editorial_path = rafael_B45_editorial_file['file_path']
            grouped.setdefault(rafael_B45_editorial_path, [])
            changed_records.setdefault(rafael_B45_editorial_path, []).extend(row['id'] for row in rafael_B45_editorial_file['changed_records'])
            relocation_checks.setdefault(rafael_B45_editorial_path, {})['rafael_B45_editorial'] = {
                'release_config': rafael_B45_editorial_config,
                'release_config_sha256': sha256(Path(rafael_B45_editorial_config).read_bytes()),
                'proof': rafael_B45_editorial_report}
        for rafael_B45_editorial_manuscript in rafael_B45_editorial_report['manuscripts']:
            more_batch = Path(rafael_B45_editorial_manuscript)
            if more_batch in release_batches:
                raise ValueError('Rafael B45 must run once after the complete V7857 stack')
            release_batches.append(more_batch)

"""
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('rafael_B45_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('lil_B218_retrospective')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7857'])
    profile.update(status='experimental',rafael_B45_editorial=owned.CONFIG,
        description="Complete V7857 plus Rafael's complete twelve-speech B45 trade tutorial: seven source-grounded wording revisions and five contextual retentions.",
        note="Fresh clean Japanese whole exchange and exact current comparison; Rafael Castor/Julio Erneco retained from source getters. Conditional Lisbon cargo, local ruler contract fee at Palace/Governor's Office, minimum-fee advice, Ceuta and optional sale preserved. Market share limits purchases, not selling. Original 00/06/FE selectors, six-byte preambles, FO, all24 commands/five relative spans preserved. Twelve complete native/stored pages, 48 compiled alignments, 28 fresh stored/20 reused alignments,343 loads/686 parent modes,25 relocated cases and full inverses. Paired disclosed entry fixtures play all12 speeches in both languages,90 complete holds,normal [0,1] returns6653. Preserve21 comparison rows/seven duration differences and English one LCG step ahead; future random outcomes not proven equal. 12 policy positives/159 rejections; atomic whole-ROM positive/131 independent rejections before commit. No natural activation/full route/hardware claim. Full207 names, four storylines, earlier dialogue, broad town/random,Help/remaining prose and wrap review remain open; graphics/later technical re-audit separate. MainV4701 unchanged; no separate package,promotion,pruning,commit orpush.")
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage)
    save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    temporary=builder.with_name('build_integrated_release_v7910.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7857',
        parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        positive_proof=result['positive_proof'],negative_cases=result['negative_cases'],negative_count=131,
        all_negatives_reject_before_commit=True,expected_manifest_batches=633,accepted_layers=114,
        promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],
        producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimental V7911:633 expected batches/114 accepted; prior profiles and main preserved. No credit or promotion.')
