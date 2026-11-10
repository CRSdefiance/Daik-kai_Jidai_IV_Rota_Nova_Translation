"""Reversibly checkpoint all26 B46 source/native/stored/actual approvals; production/integration pending."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B45_v7916 import COUNTERS,AFTER
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_actual_checkpoint_v7954')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7955')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7937/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
SOURCE=Path('work/analysis/Rafael_next_clean_v7918/complete_clean_SC0_B46_EV0_andcoverage_before_current_English.json')
CONTEXT=Path('work/analysis/Rafael_B46_clean_context_v7919/complete_clean_SC0_B38_EV0_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Rafael_B46_branch_gloss_v7926/24_speeches2_choices_fresh_branch_context_before_current_English.json')
NAMES=Path('work/analysis/Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json')
CONTROLS=Path('work/analysis/Rafael_B46_source_controls_v7922/source_EV0_entry_four_relative_sites20_cases25_seeded_ends_menu_scope.json')
CURRENT=Path('work/analysis/Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B46_effective_v7928/all24_effective_English_templates48_original_dispatches12_FE.json')
MANUSCRIPT=Path('translations/rafael_B46_editorial_manuscript_v3.json')
NATIVE_REVIEW=Path('work/analysis/Rafael_B46_actual_approval_v7953/26_source_context_native_actual_approved_policy_release_pending.json')
NAME_REVIEW=Path('translations/rafael_B46_speaker_name_review_v2.json')

KEY='Rafael_SC0B46_actual_approved_pending_production_v7954'
SCOPE='unfinished_editorial_scope_v7954'
SUMMARY="The current registered cumulative ROM remains V7911; main V4701 is unchanged. Its 633 batches, 114 accepted layers, 18 passing release checks, 110 regressions, whole-reference equality and exact clean-input patch remain verified. Counts stay at 6,950 completed, 6,953 source/prose records and drafts, 4,354 integrated wording revisions and 2,596 retentions. B46 is approved for source, context, prose and formatting, but is not integrated and has no completion credit yet.\n\nThe complete Rafael B46 draft is translations/rafael_B46_editorial_manuscript_v3.json: 24 speeches, including twelve FE panels, plus two menu choices. All 26 individual review gates are true, with seven wording revisions and nineteen individually justified retentions. Fresh clean Japanese, the B38 prerequisite context and corrected branch context preceded current English. Accepting the lesson leads to the tutorial/check/thanks; declining leads to Julio's caution and Rafael's acknowledgment. Both paths share the unfinished private thought. Approved names, Y/L/R/A instructions, opposite mode orders, icons, target classes and land inside the search frame remain faithful.\n\nStored reconstruction changes B46 from 1696 stored/1694 logical/tail2 to 1528 stored/1526 logical/tail2. All 24 complete speech preambles, the two-choice menu, five A000 commands, 6300, 61FF, four relative/nested spans and four-byte normal end are preserved. Both complete clean/predecessor block inverses and the full predecessor archive inverse pass. All 342 other SC0 blocks and every other file/component remain exact in the pinned research reference. Eleven zero-ink parity tails receive 44 fresh alignments; thirteen exact bodies reuse 52 cases. All stored planes match the viewed pages without extra or blank pages. The 30-byte menu passes both even header alignments, including its relocated offset242. Native loaders pass all343 load/cache paths and686 parent modes; all37 command maps and a fresh shipped caller census are bound.\n\nFour 16001-frame headless emulator jobs are terminal and their sessions reaped: clean Japanese and English, accepting and declining through ordinary inputs. The original ten-command B44 prelude and all37 B46 commands remain in the disclosed opening entry fixtures, including all five A000 commands. No source speech, resource, branch, effect or end is omitted. No RAM, seed, result, condition, role, roster, battery or savestate is forced. These are initialized Lisbon opening fixtures, not natural B46 event selection, earned prerequisites, original location, a full route or hardware verification.\n\nAcceptance plays22 speeches and43 total commands, returning [0,0] at9295/9294 in source/English. Declining plays7 speeches and28 commands, returning [0,1] at5695/5696. Each language's union covers all24 distinct speeches andall37 original B46 commands; other seeded native result values remain offline coverage. Across58 speech occurrences,214 complete body/name/FE holds match independent native masks withzero partial eligible samples or unresolved records. All48 unique source/English panes, four transition sheets, the menu sheet and later comparison sheet were directly viewed: fourteen sheets total.\n\nActual menu context/views confirm source84px and target66px caption widths inside the original256x36 backing. Twelve read-only memory snapshots and24 visible-label samples match complete independent CP932/ASCII glyphs, original view bounds and exact native background pixels. Both ordinary selected values0/1 and their highlights are observed. Source accept4930 has no visible highlight despite eventual selection0; its full glyphs and paper pixels remain exact, while English4930 still shows0. This measured phase difference is retained, without an invented causal animation explanation or frame exclusion. Failed coordinate/phase assumptions and their immutable successors remain preserved.\n\nAll29 paired upper scenes, portraits and complete headers match, as do every selected command result and UI request. Preserve acceptance27 comparison rows/six duration differences and decline12/two. Both begin with RNG848781860. The first phase difference occurs at the menu: source232 frames/77 LCG advances versus English234/78. English is mathematically one LCG step ahead at both B46 exits. Later samples do diverge: acceptance has41/113 RGB differences and final seeds1622437796/3229979821, with English159 steps behind; decline has96/173 and3730749937/3562773357, English316 behind. State/tasks match; models, persistent objects and whole actors differ on both paths. Acceptance calendars differ (ticks810/816, raw zero-based dates[0,16,42]/[0,17,0]); decline calendars match. Do not claim identical future random outcomes, full simulation equality or a complete causal trace. Original wait/generator code is unchanged; that supports consistency with timing differences, not broad equivalence. Retain every measurement for the later technical re-audit.\n\nAll three actual progressive nameplates verify Rafael Castor, Claudio Manaus and Julio Erneco. Full catalogue UI, custom names and the full207-name/role/alias review remain open; Hayreddin has only the scoped clean/current name-component retention. Incidental B127 and later Sailor sailing prose are captured leads, with no new editorial credit. All earlier translations, failed producers, proofs and ROMs remain. No separate unified test package, promotion, pruning, commit or push."
NEXT="Continue from verified V7955 and current V7911. Use translations/rafael_B46_editorial_manuscript_v3.json, translations/rafael_B46_speaker_name_review_v2.json and work/analysis/Rafael_B46_actual_approval_v7953/26_source_context_native_actual_approved_policy_release_pending.json. All26 source/context/prose/formatting gates pass. Reuse completed native, stored, inverse, loader/caller, four actual jobs,214 holds, menu-backing and fourteen viewed-sheet proofs without replay. Keep every source highlight-off and later timing/RNG/component/calendar/RGB limit.\n\nNext freeze the strictly scoped natural-dialogue-v2 formatting and typed-menu policy from the exact approved plans. Bind all24 clean/current speech bodies, full preambles, two choice texts/order/provider, current2b6 ARM9/COMMON/font, FI6/FA6/FO10 defaults withzero source macros, source-00 handling and the original distinct FE216px usable budget inside228px bitmap. Preserve all14 original row-count infos and reasons withno warning waiver. Both menu labels use native constructor sizing at66px, not authored padding. Test actual changing inputs for source/prose/speaker/macro/consumer/runtime/profile/manual breaks/printf/choice order, offsets and individual review gates.\n\nImplement and challenge an atomic production stage for the entire block. Require complete reconstruction and both inverses, allfour nested relative spans, all37 original commands, full stored-body/menu references and exactly one final files-list commit after every gate. Bind the actual menu [2,0]/[2,1] and normal [0,0]/[0,1] returns, all measured later differences and disclosed fixture scope. Reject corrupted proofs independently of dependency digests and before mutation. Preserve failed producers and genuine failures. The manuscript has24 speech records andtwo typed_choice_records; the registered workflow must include all26 exactly once, using the established mixed speech/menu approach as appropriate. Do not lose or double-credit the choices.\n\nIntegrate only after necessary checks pass through the complete registered stack afterV7911, retaining all114 accepted layers, release checks/regressions, exact whole research-reference equality, clean-input patch reconstruction and appropriate startup controls. Keep mainV4701 unchanged. Credit26 records/seven revisions/nineteen retentions only after registered integration. Expected counts then are6976 completed/6979 source-prose anddrafts/4361 revisions/2615 retentions, SC0 173; current counts remain6950/6953/4354/2596.\n\nThe full goal remains active across all four storylines, earlier translations, broad practical shop/town/random capture, Help and remaining player prose, all207 names/roles/aliases, twelve remaining retrospective wrap leads and the unscanned records beyond558 recorded plans. Preserve every older unfinished inventory, item/counterpart/display lead, Sailor151-159 versus Retainer consumer distinction, normal-end value carry and B35R65's source-only nineteenth cell. The actual B127/Sailor captures are leads, not reviewed prose or proof they were unread before capture. Use own-current Rafael input at work/analysis/current_V7911_Rafael_native_v7914/current_native_input.json; other routes' earlier contexts remain historical until properly rebound or recaptured. Graphics/all18 plaques and the later older-record technical re-audit stay separate. Preserve every ROM, translation, draft, executed/failing producer and proof. No separate package, promotion, pruning, commit or push."

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result

def gates():
    prior,doc,approval=map(read,[PRIOR,MANUSCRIPT,NATIVE_REVIEW])
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    assert prior['completed']==6950 and prior['manifest_batches']==633 and prior['Rafael_B45_completed_once']
    assert approval['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and approval['names_sha256']==sha(NAME_REVIEW.read_bytes())
    assert len(doc['records'])==24 and len(doc['typed_choice_records'])==2 and doc['revisions']==7 and doc['retentions']==19
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness','formatting']) for r in doc['records']+doc['typed_choice_records'])
    assert not doc['formatting_review_pending'] and approval['actual_four_runs_frames']==64004
    assert approval['actual_speech_occurrences']==58 and approval['actual_complete_holds']==214
    assert len(approval['directly_viewed_sheets'])==14 and all(s['directly_viewed'] for s in approval['directly_viewed_sheets'])
    for s in approval['directly_viewed_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    assert approval['normal_results_accept']==[0,0] and approval['normal_results_decline']==[0,1]
    assert approval['later_RGB_difference_counts']==[41,96] and approval['later_RGB_sample_counts']==[113,173]
    assert approval['no_causal_every_call_future_state_orbroad_simulation_equivalence_claim']
    assert len(read(EFFECTIVE)['source_current_dispatches'])==48
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
        oldscope=old['unfinished_editorial_scope_v7936'];assert sha(Path(oldscope['path']).read_bytes())==oldscope['sha256']
        inventory=deepcopy(read(oldscope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(source_gloss=str(GLOSS),names=str(NAMES),controls=str(CONTROLS),source_speeches=24,source_choices=2,
            current_English_unread=False,new_credit=0,all_prior_inventories_andfull_scope_preserved=True)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_andfull_scope_preserved=True,new_credit=0,full_goal_complete=False))
        put(['formatting_watchlist',KEY],dict(source_gloss=str(GLOSS),names=str(NAMES),controls=str(CONTROLS),
            source_context_native_stored_actual_approved_policy_atomic_registered_release_pending=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
        put(['coverage_units',ri,'next'],NEXT)
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,SOURCE,CONTEXT,GLOSS,NAMES,CONTROLS,scope,Path(__file__),
            Path('work/analysis/Rafael_B46_gloss_tools_v7920b/source_locked_derivation.json'),CURRENT,EFFECTIVE,MANUSCRIPT,NATIVE_REVIEW,NAME_REVIEW]}
        new[KEY]=dict(summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,source_gloss=str(GLOSS),
            source_speeches=24,source_choices=2,source_FE_panels=12,current_English_unread=False,new_credit=0,manuscript=str(MANUSCRIPT),native_review=str(NATIVE_REVIEW),proposed_revisions=7,proposed_retentions=19,compiled_native_pages=24,compiled_alignments=96,choice_native_style_planes=8,five_sheets_directly_viewed=True,actual_sheets_directly_viewed=14,actual_speech_occurrences=58,actual_complete_holds=214,
            new_emulator_runs=4,new_actual_frames=64004,native_name_getters=6,native_macro_alignments=12,isolated_native_relative_cases=20,seeded_normal_ends=25,
            all_prior_completed_records_counts_ROM_references_andfull_scope_preserved=True,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['completed_editorial_families']==old['completed_editorial_families']
        assert new['current_integrated_candidate']==old['current_integrated_candidate'] and tuple(new[k] for k in COUNTERS)==AFTER
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        targets={LEDGER:encode_ledger(new)}
        section='## V7954: Rafael B46 source/native/stored/actual approved; policy andregistered integration pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V7954; V7911 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        protected=[Path(prior['candidate']),Path(prior['patch']),Path('translations/release_stack.json'),Path('translations/rom_retention_pins.json')]
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,protected={str(p):sha(p.read_bytes()) for p in protected},new_credit=0,full_goal_complete=False))
        print('Six actual-approval progress targets staged:26 decisions/58 occurrences214 holds/four runs64004 frames. No credit.')
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
            print('Six audited actual-approval checkpoint targets applied;V7911/6950 completed unchanged.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_hash_exact']
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
                previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),Rafael_B46_source_speeches=24,Rafael_B46_source_choices=2,
                Rafael_B46_source_FE_panels=12,Rafael_B46_current_English_unread=False,Rafael_B46_native_menu_owner_actual_andrelease_pending=False,Rafael_B46_actual_source_native_stored_andformatting_approved=True,Rafael_B46_policy_atomic_registered_integration_pending=True,Rafael_B46_contextual_native24_pages2_choices_reviewed=True,pending_Rafael_manuscript=str(MANUSCRIPT),pending_Rafael_manuscript_sha256=sha(MANUSCRIPT.read_bytes()),pending_Rafael_native_review=str(NATIVE_REVIEW),
                pending_Rafael_source_gloss=str(GLOSS),pending_Rafael_source_gloss_sha256=sha(GLOSS.read_bytes()),
                pending_Rafael_names=str(NAME_REVIEW),pending_Rafael_source_controls=str(CONTROLS),
                unfinished_scope=SCOPE,next_required=NEXT,latest_checkpoint=KEY,new_credit=0,new_emulator_runs=4,new_actual_frames=64004,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV7955/currentV7911:all26 source/native/stored/actual approved;four runs58 occurrences214 holds. Policy/atomic/registered integration pending;no credit.Full goal active.')
