"""Stage33 native-approved whole-exchange reviews once as pending integration."""
import json
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B170_checkpoint_v4279')
PRIOR = Path('work/analysis/editorial_handoff_verification_v4259/verified_handoff.json')
APPROVAL = Path('work/analysis/lil_B170_native_approval_v4278/approval_receipt.json')
DOC = Path('translations/lil_B170_editorial_manuscript_v5.json')
FAMILY = 'Lil-B170-Yifa-collision-apology-Taoist-training-resolve-joining33'
NEXT = 'Complete B170 relocation and stored/native references,representative paired source/English content with the original figure,pause,resources,later A000,C200 and normal return;then atomic compiler tests,registered cumulative build,exact clean-input patch and fresh registered startup. Keep both source ends and distinguish decoder coverage from actual reachability. Continue B171-B180 and every wider editorial family. V4204 remains promoted main;V4251 remains the latest verified cumulative candidate. Preserve every ROM,translation,draft and executed producer/proof/failure.'
SUMMARY = "V4279 records33 fresh contextual/native reviews for the complete Lil SC2 B170 Yifa collision,argument,apology,flattery,Taoist-training and ship-passage exchange:21 proposed revisions and12 individually justified retentions. All33 clean Japanese speeches were read and individually glossed as one exchange before predecessor English comparison. Preserve the abrupt collision and rushed apology,Lil's insistence,Yifa's irritation,sudden admission of fault,Lil's flustered acceptance and vain response to flattery,the tentative request for advice,explicit Admiral boast,FO fleet explanation and admiration. Keep money as a question,Yifa running away because her teacher repeatedly scolded her during Taoist training,her refusal to quit,wish to travel while continuing practice and become much stronger,Lil's qualified sympathy,explicit request aboard Lil's ship,full determination-never-to-lose test,prior harsh-training endurance,agreement,names and work-hard encouragement. Remove unsupported big sis kinship and the teacher's male pronoun. Use native-bound Yifa in spoken introductions without adding catalogue-only Sol. Add no teacher gender,name,school,nationality,degree,abuse,expulsion,named spell,price,reward,romance or numeric skill threshold. Every12 retained wording has an individual contextual reason;the working short reactions and banter stay intact.\n\nFresh source/current contracts bind33 complete progressive preambles,selectors02/19 (Lil2/Yifa25),FI1/FO1,45 commands,twelve nonrelative leaves,two original630x resource words/20 boundary cases,six isolated presentation/pause structural sites,one C200 clean/current pair,one two-byte2000 pause at36/resume38,one later A000 and both consecutive endwords1852/1856. Four original progressive/full-name getters preserve owned scratch rings/writes and all4MiB restoration;both names are Lil Argot/Yifa Sol. The207-entry/eight-voice catalogue is rebound by exact runtime,COMMON,EV2,font and snapshot. Source19 remains Yifa's selector. Taoist arts is bound to two exact completed COMMON Yifa records. The source supplies Lil's Admiral claim here and leaves the teacher's gender unspecified;お姉さん is a familiar address to a female stranger,not a sister relationship. Source event170/action171 and its getter are bound without claiming eligibility. No relative sites,predicates,FE or typed choices exist in this block;the zero-site census makes no branch-execution claim. A000 raw words1019/2001 and C200 stay intact;full effect,figure,pause and normal-return behavior remain unexecuted. Keep the later older-record technical re-audit separate.\n\nNative approval V4278 covers all33 complete216x64 progressive planes and264 logical/compiled alignment cases. The final proof freshly checks16 alignment cases/two changed complete records and reuses248 exact cases/31 byte-identical records from the original264-case native proof,with exact runtime,source,English,encoded bytes,font plane and preview hashes bound. All33 QA plans are fresh and all five final sheets were viewed. Complete leading/internal/final glyphs,unique cells,zero row origins,four-row bounds and single-page consumption pass.13 source-consumer,two missing-macro and14 formatter rejection controls pass. Eleven narrow row-count notes exempt no glyph,bounds,pagination,macro,control,weak-ending,orphan or blank-page issue. Keep Come over here together and express Lil's qualified sympathy as I guess I understand;all source meanings and21/12 decisions remain intact. No authored breaks,padding,wording waiver or shared guard/metric change. No B170 actual gameplay or transition coverage is claimed yet.\n\nCoverage becomes5725 fresh contextual rereads:5692 integrated/completed and33 pending. Source/prose becomes5728,including3872 SC2 and unchanged64 SC3;reviewed/completed route objects4126/4093. Historical completed decisions stay3614 revised/2078 retained. B170 is credited once as pending,with no completion credit. The latest verified experimental cumulative build remains V4251,545 manuscript batches/114 accepted layers,with its exact clean-input patch. Promoted main remains V4204. Registry,builder,promoted pointer,canonical input,all prior completions and every earlier ROM/translation/draft/executed producer/proof/failure remain unchanged.\n\nRemaining B171-B180 has198 physical speeches and zero typed-choice-command leads,not a full Lil/project denominator. Every wider storyline,shared shop/town exchange,random scene,Help and other player-facing prose stays open. Preserve COMMON750-752,canonical Maria32 SC3 B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques remain separate;retain the later older-record technical re-audit/queued0D gap. Full goal active;all jobs terminal."

if __name__ == '__main__':
    assert not ROOT.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    ledger = read(lp)
    assert sha(lp.read_bytes()) == read(PRIOR)['ledger_sha256']
    approval, doc = read(APPROVAL), read(DOC)
    assert approval['manuscripts'] == {str(DOC):sha(DOC.read_bytes())}
    rows = doc['records']
    assert len(rows) == 33 and all(all(r['review'].values()) for r in rows)
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release']) == (5692,5692,0)
    selected = [dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    assert len({historical_key(r) for r in selected}) == 33
    assert not {historical_key(r) for r in selected} & {historical_key(r) for r in fresh['record_keys']}
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] == 3839
    assert ledger['records_with_source_and_prose_pass'] == 5695
    docs = [Path('docs')/name for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4258')
    ROOT.mkdir(parents=True)
    for path in [lp,*docs]:
        copy2(path,ROOT/(path.name+'.before'))
    ledger['records_with_source_and_prose_pass'] = ledger['records_with_source_prose_drafts'] = 5728
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] = 3872
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'] = [r['id'] for r in rows]
    active = ledger['active_source_prose_drafts']
    assert str(DOC) not in active['manuscripts']
    active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(DOC)] = [r['id'] for r in rows]
    note = '5725 fresh rereads:5692 integrated/33 pending;source/prose5728. B170 credited once as pending;no completion or actual scene credit.'
    active.update(status='3-reviewed-COMMON-incomplete;33-Lil-B170-native-approved-pending-release',note=note)
    pending = dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[170],records=33,record_keys=selected,
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),manuscripts=approval['manuscripts'],
        proposed_revisions=21,retentions=12,source_prose_reviews_added=33,completion_credit_added=0,
        pending=NEXT,new_emulator_runs=0,actual_selected_B170_IDs=[])
    fresh['record_keys'].extend(selected)
    fresh['record_IDs'].extend(r['id'] for r in rows)
    fresh.update(fresh_pass_records_explicitly_reread=5725,fresh_pass_records_integrated=5692,
        fresh_pass_records_pending_native_actual_release=33,pending_record_keys=selected,
        pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,
        latest_contextual_manuscript=str(DOC),coverage_note=note)
    for unit in ledger['coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4126,completed_route_records=4093,next=NEXT)
    ledger['coverage_units'].append({**pending,'status':doc['status'],'full_goal_complete':False})
    ledger['formatting_watchlist']['lil_B170_v4279'] = dict(status='native-approved;pending-relocation-representative-release',
        approval=str(APPROVAL),approval_sha256=sha(APPROVAL.read_bytes()),row_count_notes=11,
        all5_speech_sheets_viewed=True,actual_selected_B170_IDs=[],new_emulator_runs=0)
    previous = ledger['unfinished_editorial_scope_v4258']
    assert sha(Path(previous['path']).read_bytes()) == previous['sha256']
    inventory = deepcopy(read(previous['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=[170],count=33,record_IDs=[r['id'] for r in rows])],
        incomplete_route_source_prose_count=33,next_focus=NEXT)
    inventory['B170_fresh_context_review_checkpoint_v4279'] = pending
    inventory['remaining_B171_B180_unreviewed_uncredited'] = dict(physical_speeches=198,typed_choice_command_leads=0,not_full_Lil_or_project_denominator=True)
    inventory['earlier_B170_uncredited_leads_are_historical_after_V4279'] = True
    for unit in inventory['broader_coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4126,completed_route_records=4093,source_prose_pending_records=33,source_prose_pending_family=FAMILY,next=NEXT)
    inv = ROOT/'unfinished_editorial_scope_inventory.json'
    save(inv,inventory)
    ledger['unfinished_editorial_scope_v4279'] = dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,
        incomplete_route_source_prose=33,remaining_B171_B180_physical_speeches=198,remaining_choice_command_leads=0,
        canonical_Maria32_pending_uncredited=True,Proof_terminology_consistency_open=True,
        wider_story_shared_town_random_help_prose_open=True,full_goal_complete=False)
    paths = [PRIOR,APPROVAL,DOC,inv,Path(__file__),Path(approval['merged_native_proof'])]
    for key in ['source_context','control_contract','branch_proof','source_entry_proof','whole_exchange_context_notes',
                'effective_current_comparison','native_font_proof','actor_terminology_reconciliation',
                'source_effect_and_predicate_contract','source_nameplate_consumer_proof']:
        path = Path(doc[key])
        assert sha(path.read_bytes()) == doc[key+'_sha256']
        paths.append(path)
    evidence = {str(path):sha(path.read_bytes()) for path in paths}
    ledger['lil_B170_scope_reconciliation_v4279'] = dict(summary=SUMMARY,evidence=evidence,pending_family=pending,
        source_prose_reviews_added=33,completion_credit_added=0,full_goal_complete=False)
    ledger['latest_checkpoint'] = SUMMARY
    planned = {lp:(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')}
    section = '## V4279:33 B170 contextual/native reviews;integration pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\nNext: '+NEXT+'\n\n'
    for index,path in enumerate(docs):
        first,rest = path.read_text(encoding='utf-8').split('\n',1)
        planned[path] = (('# Current editorial handoff - V4279' if index==0 else first)+'\n\n'+section+rest).encode('utf-8')
    staged = ROOT/'staged'
    staged.mkdir()
    plan = []
    for index,(path,data) in enumerate(planned.items()):
        output = staged/(str(index)+'.planned')
        output.write_bytes(data)
        plan.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(output.resolve()),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',plan)
    stable = ['translations/release_stack.json','translations/promoted_build.json','scripts/build_integrated_release.py']
    save(ROOT/'staged_receipt.json',dict(checkpoint='V4279',evidence=evidence,
        preserved_release_files={p:sha(Path(p).read_bytes()) for p in stable},prior_verified_handoff=str(PRIOR),
        new_source_prose_reviews=33,new_completed_records=0,proposed_revisions=21,justified_retentions=12,
        fresh_reread=5725,fresh_integrated=5692,fresh_pending=33,source_prose=5728,completed=5692,
        historical_revised=3614,historical_retained=2078,new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V4279 staged:5725 reread/5692 integrated/33 pending;5728 source/prose. Latest V4251 and promoted V4204 unchanged;full goal active.')
