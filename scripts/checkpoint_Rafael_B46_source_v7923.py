"""Reversibly checkpoint fresh source/gloss/name/control progress; no new editorial credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B45_v7916 import COUNTERS,AFTER
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_source_checkpoint_v7923')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7924')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7917/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
SOURCE=Path('work/analysis/Rafael_next_clean_v7918/complete_clean_SC0_B46_EV0_andcoverage_before_current_English.json')
CONTEXT=Path('work/analysis/Rafael_B46_clean_context_v7919/complete_clean_SC0_B38_EV0_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Rafael_B46_clean_gloss_v7920b/24_speeches2_choices_fresh_clean_glosses_before_current_English.json')
NAMES=Path('work/analysis/Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json')
CONTROLS=Path('work/analysis/Rafael_B46_source_controls_v7922/source_EV0_entry_four_relative_sites20_cases25_seeded_ends_menu_scope.json')
KEY='Rafael_SC0B46_source_gloss_names_controls_pending_current_English_v7923'
SCOPE='unfinished_editorial_scope_v7923'
SUMMARY="""Current registered cumulative V7911 retains all633 batches/114 accepted layers,18 passing release checks/110 regressions, exact reviewed-reference ROM equality andclean-input patch reconstruction. MainV4701 is unchanged. The verified ledger remains6950 completed/6953 source-prose anddrafts/4354 integrated revisions/2596 retentions. RafaelB45 is completed andintegrated: seven revisions/five contextual retentions. Reuse the full V7917 release/native/actual/startup proof set without unnecessary replay, retaining its one-step RNG difference andall timing/scope limits.

The next untouched clean Rafael exchange,SC0 B46, has24 speeches including12 FE system panels andone2100 menu withtwo choices. All26 text units now have fresh English source glosses authored fromthe complete clean Japanese before any current B46 English exposure. Complete clean B38 context was also read: EV0 event46/category5/action47 requires38; event38 requires37. The Spanish-fleet threat andハイレディン intervention explain the opening relief, without proving immediate chronology, current location ornatural activation.

Preserve the progression fromClaudio's relief andRafael's subdued reply, throughJulio's warning andoffer to teach, toaccept/decline choices, three sea modes, acheck ofunderstanding, caution atsea andRafael's unfinished private future thought. Do not invent kinship/rank, guaranteed discoveries, omit town attacks orcomplete the final thought withan invented ambition. Source L cycles information→battle→search; R, oralternativelyY, cycles information→search→battle. Preserve magnifying-glass/sword/gray-frame marks, target types, land inside the search frame andA confirmations.

Fresh own-V7911 captain0 native probes verify six original progressive/full name getters forthree static speakers: Rafael Castor,Claudio Manaus,Julio Erneco. Exact clean fields support retaining these names; voices are2/4/5. Twelve synthetic default alignments measureFI6/FA6/FO10 butthe B46 source hasnoFI/FA/FO macros. FE254 remains a separate system consumer. Actual B46 headers/full catalogue UI/custom-name coverage andthe wider207-name/role/alias review remain open.

The original event pointer/completion-bit read preserves all4MiB. Four relative sites pass20 isolated native result cases;25 seeded normal ends retain type0/value carry. These are offline checks, not actual menu choices orscene activation. The original fiveA000 commands,2100 menu owner/returns/geometry,resource6300 effects, selected branch paths andactual display still require their own mapping. The complete source has37 commands,1696stored/1694logical/tail2. Current B46 English speeches andbothchoices remain unread. No localized manuscript, source-prose completion ornew editorial credit is claimed.

The initial gloss producer miscounted FE panels as14 andfailed anassert before output. It remains preserved withits diagnostic; its immutable successor records the measured12 FE panels andboth menu choices. No failed producer is counted aspassed validation. All prior ROMs, translations, drafts, producers andproofs remain. No separate unified package,promotion,pruning,commit orpush."""
NEXT="""Continue the full goal fromverifiedV7924/currentV7911 andthe B46 source-first packet at work/analysis/Rafael_B46_clean_gloss_v7920b/24_speeches2_choices_fresh_clean_glosses_before_current_English.json. Current B46 English remains unread. First bind the original2100 two-choice owner/actual return semantics andallfiveA000 setup leaves, source relative flow andselected acceptance/decline paths; preserve true checks asoffline evidence. Use own-V7911 Rafael context at work/analysis/current_V7911_Rafael_native_v7914/current_native_input.json. Names/voices andfour relative sites arealready measured; do notrepeat unchanged probes.

Then expose exact current effective English forall24 speeches andbothchoices asacomplete exchange, preserving a timestamped source-first boundary. Review natural American English incontext,retain good wording withindividual reasons, keepallbuttons/mode order/targets/icons andthe unfinished thought faithful. Format under validated native consumers, particularly12 distinct FE panels andthe2100 menu backing/view/highlight behavior; check complete glyphs,bounds,automatic wrapping andpagination. Use representative gameplay andfocused branch/transition tests forconcrete risks; exhaustive natural activation isnot required. Integrate avalidated batch through atomic registered cumulative release andexact clean-input patch, adding credit onlyafterallnecessarychecks.

Keep the entire four-storyline/earlier-dialogue/shared shop-town-random/Help/remaining-prose objective active, including broad practical capture, all207 names/roles/aliases, twelve retrospective contraction/question-tag leads andthe unscanned records beyond558 plans. Preserve every earlier unfinished inventory,item/counterpart/display lead, Sailor151-159 versusRetainer consumer distinction,normal-end value carry andB35R65 source-only nineteenth cell. LilV7857 andMariaV7821 native contexts remain historical toV7911; obtain each route's owncurrent context when needed. Graphics/all18 plaques andthe later older-record technical re-audit remain separate. Preserve every ROM andearlier translation. MainV4701 stays unchanged; no canceled separate package,promotion,pruning,commit orpush."""

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result

def gates():
    prior,gloss,names,controls=map(read,[PRIOR,GLOSS,NAMES,CONTROLS])
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    assert prior['completed']==6950 and prior['manifest_batches']==633 and prior['Rafael_B45_completed_once']
    assert len(gloss['records'])==24 and len(gloss['menu_choices'])==2 and gloss['FE_system_panels']==12
    assert all(r['current_English_body_unread'] and r['source_gloss_not_current_English_derived'] for r in gloss['records']+gloss['menu_choices'])
    assert names['source_gloss_sha256']==controls['source_gloss_sha256']==sha(GLOSS.read_bytes())
    assert names['candidate_sha256']==controls['candidate_sha256']==prior['candidate_sha256']
    assert len(names['native_six_progressive_andfull_getters']['rows'])==6
    assert len(controls['source_relative_cases'])==4 and sum(len(c['cases']) for c in controls['source_relative_cases'])==20
    assert len(controls['normal_seeded_ends'])==25 and controls['actual_B46_gameplay_observations']==0
    assert len(controls['five_original_A000_commands'])==5 and controls['current_English_bodies_andtwo_choices_still_unread']
    assert read(SOURCE)['groups'][0]['completed_coverage_overlap']==0
    return prior

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior=gates()
    if mode=='stage':
        assert not ROOT.exists()
        before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and KEY not in old and tuple(old[k] for k in COUNTERS)==AFTER
        assert old['goal_status']=='active' and not old['full_goal_complete']
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
            ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        oldscope=old['unfinished_editorial_scope_v7916'];assert sha(Path(oldscope['path']).read_bytes())==oldscope['sha256']
        inventory=deepcopy(read(oldscope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(source_gloss=str(GLOSS),names=str(NAMES),controls=str(CONTROLS),source_speeches=24,source_choices=2,
            current_English_unread=True,new_credit=0,all_prior_inventories_andfull_scope_preserved=True)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_andfull_scope_preserved=True,new_credit=0,full_goal_complete=False))
        put(['formatting_watchlist',KEY],dict(source_gloss=str(GLOSS),names=str(NAMES),controls=str(CONTROLS),
            source_names_andrelative_controls_checked_current_English_menu_owner_actual_andrelease_pending=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
        put(['coverage_units',ri,'next'],NEXT)
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,SOURCE,CONTEXT,GLOSS,NAMES,CONTROLS,scope,Path(__file__),
            Path('work/analysis/Rafael_B46_gloss_tools_v7920b/source_locked_derivation.json')]}
        new[KEY]=dict(summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,source_gloss=str(GLOSS),
            source_speeches=24,source_choices=2,source_FE_panels=12,current_English_unread=True,new_credit=0,
            new_emulator_runs=0,native_name_getters=6,native_macro_alignments=12,isolated_native_relative_cases=20,seeded_normal_ends=25,
            all_prior_completed_records_counts_ROM_references_andfull_scope_preserved=True,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['completed_editorial_families']==old['completed_editorial_families']
        assert new['current_integrated_candidate']==old['current_integrated_candidate'] and tuple(new[k] for k in COUNTERS)==AFTER
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        targets={LEDGER:encode_ledger(new)}
        section='## V7923: Rafael B46 source-first gloss, names andrelative controls; current English pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V7923; V7911 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        protected=[Path(prior['candidate']),Path(prior['patch']),Path('translations/release_stack.json'),Path('translations/rom_retention_pins.json')]
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,protected={str(p):sha(p.read_bytes()) for p in protected},new_credit=0,full_goal_complete=False))
        print('Six source-progress targets staged; all26 source text units, six names/20 relative cases/25 seeded ends. No credit.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in (plan['evidence']|plan['protected']).items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),deep_inverse_all_prior_values_exact=True,new_credit=0,full_goal_complete=False))
            print('Deep inverse/six hashes/all evidence pass. Prior completed coverage and ROM preserved.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists()
            assert read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            workspace=Path.cwd().resolve()
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(workspace) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,no_ROM_orcredit_change=True,full_goal_complete=False))
            print('Six audited source-progress checkpoint targets applied; V7911/6950 completed unchanged.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_hash_exact']
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
                previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),Rafael_B46_source_speeches=24,Rafael_B46_source_choices=2,
                Rafael_B46_source_FE_panels=12,Rafael_B46_current_English_unread=True,Rafael_B46_native_menu_owner_actual_andrelease_pending=True,
                pending_Rafael_source_gloss=str(GLOSS),pending_Rafael_source_gloss_sha256=sha(GLOSS.read_bytes()),
                pending_Rafael_names=str(NAMES),pending_Rafael_source_controls=str(CONTROLS),
                unfinished_scope=SCOPE,next_required=NEXT,latest_checkpoint=KEY,new_credit=0,new_emulator_runs=0,new_actual_frames=0,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('Verified V7924/currentV7911: 24 fresh source speech glosses/two choices/six name getters; no added credit. Full goal active.')
