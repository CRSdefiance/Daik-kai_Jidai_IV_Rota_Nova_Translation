"""Register one sealed B218 retrospective layer after V7821, preserving every previous profile andmain."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B218_retrospective_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.retrospective_B218_final_paths_v7853 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_registration_v7856')
PROFILE='all-routes-unified-v7857'
VALIDATION=Path('work/analysis/retrospective_B218_atomic_challenges_v7855/atomic_validation_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    result=read(VALIDATION);config=Path(result['config']);conf=read(config);cases=read(result['negative_cases'])
    assert result['positive_records']==13 and result['changed_records']==1 and result['negative_count']==len(cases)==128
    assert result['all_negatives_reject_before_any_files_list_commit'] and result['all_dependency_digests_deliberately_bypassed']
    assert all(c['rejected'] and c['commit_calls']==0 for c in cases)
    assert sha(config.read_bytes())==result['config_sha256'] and sha(PARENT.read_bytes())==result['parent_ROM_sha256']
    assert sha(Path(result['negative_cases']).read_bytes())==result['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7852/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==631
    stage=b"""    lil_B218_retrospective_config = profile_config.get('lil_B218_retrospective')
    if lil_B218_retrospective_config:
        from dk4tool.patch.lil_B218_retrospective_v2 import apply_release as apply_lil_B218_retrospective

        lil_B218_retrospective_report = apply_lil_B218_retrospective(candidate, baseline, lil_B218_retrospective_config)
        for lil_B218_retrospective_file in lil_B218_retrospective_report['files']:
            lil_B218_retrospective_path = lil_B218_retrospective_file['file_path']
            grouped.setdefault(lil_B218_retrospective_path, [])
            changed_records.setdefault(lil_B218_retrospective_path, []).extend(row['id'] for row in lil_B218_retrospective_file['changed_records'])
            relocation_checks.setdefault(lil_B218_retrospective_path, {})['lil_B218_retrospective'] = {
                'release_config': lil_B218_retrospective_config,
                'release_config_sha256': sha256(Path(lil_B218_retrospective_config).read_bytes()),
                'proof': lil_B218_retrospective_report}
        for lil_B218_retrospective_manuscript in lil_B218_retrospective_report['manuscripts']:
            more_batch = Path(lil_B218_retrospective_manuscript)
            if more_batch in release_batches:
                raise ValueError('B218 retrospective must run once after the complete V7821 stack')
            release_batches.append(more_batch)

"""
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('lil_B218_retrospective')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('maria_B36_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7821'])
    profile.update(status='experimental',lil_B218_retrospective=owned.CONFIG,
        description="Complete V7821 plus one retrospective automatic-wrap refinement in Lil SC2B218 R27. All13 existing English wordings are individually retained after complete clean/current context review;12 stored speeches remain exact. Keep That's a surprise together after the private question. No new words,story facts,names,controls,macros,font,width orduplicate editorial credit.",
        note='All13 individual review gates pass. Fresh own-V7821 Lil context,captain2/whole actors/six RGB controls;one changed native page/before-after planes/12 processor alignments,four stored parity-tail cases,all13 final dispatches,15 original commands13 preambles/no relative predicates ormenus,A000 andfour-byte end/tail2. Old1016/logical1016/tail0 ->1020/logical1018/tail2;both block inverses/full predecessor archive inverse,335 otherblocks/allotherfiles/components exact.336 native loads/cache hits672 parentmodes andbounded shippedcaller census. Paired previous/proposed16001-frame English fixtures each13 speeches/all24 commands,51complete body/name holds;26panes/102holds,eight sheets viewed,zero partials. Both exit5975;onlyeight offset/length comparison rows differ;no durations/results/UI/RNG/167 sampled laterRGB/five finalcomponents/wholeactors/seed differences. Keep natural activation,original location,fullmechanics,fullroute,hardware,everyframe/fullRAM/future/causal limits explicit.13 positive/221 policy rejections;one atomic positive/128 actual-changing production rejections withconfig dependency checks bypassed,no negative commits. Preserve all prior artifacts/fullgoal/207names/retrospectivewraps,graphicsseparation/latertechnicalaudit. MainV4701unchanged;no separatepackage,promotion,pruning,commit orpush.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage)
    save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf)
    temporary=builder.with_name('build_integrated_release_v7856.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7821',
        parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        positive_proof=result['positive_proof'],negative_cases=result['negative_cases'],negative_count=128,
        all_negatives_reject_before_commit=True,expected_manifest_batches=632,accepted_layers=114,
        promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],
        producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimentalV7857:632expectedbatches/114accepted;all prior profiles/mainV4701 preserved.No credit orpromotion.')
