"""Stage36 native-approved whole-exchange reviews once as pending integration."""
import json
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_checkpoint_v4231')
PRIOR = Path('work/analysis/promotion_v4226/promotion_receipt.json')
APPROVAL = Path('work/analysis/lil_B169_native_approval_v4230/approval_receipt.json')
DOC = Path('translations/lil_B169_editorial_manuscript_v4.json')
FAMILY = 'Lil-B169-Mikhail-Proof-legend-clues-ruins-tavern-give-and-take36'
NEXT = 'Complete B169 relocation and stored references, representative source/English content with the original three predicates, later numeric29/0001 A000 and normal return, then registered cumulative release, exact clean-input patch and startup. Continue B170-B180 and all wider editorial families. V4204 remains promoted main. Preserve all ROMs, translations, drafts and executed producers/proofs/failures.'
SUMMARY = '''V4231 records36 fresh contextual/native reviews for the complete Lil SC2 B169 Proof explanation:19 proposed revisions and17 individually justified retentions. All36 clean Japanese speeches were read as a complete exchange and individually glossed before predecessor English comparison. Preserve Camille's flustered correction to the flattering naturalist address Mikhail Letzel, Mikhail's boast and diversion to Lil, Lil's unwanted-touch threats and distrust, optional Julio/Ian/Fernando reactions, the seven treasures/Seven Sages/location marks on differently shaped maps, hearsay, mystery and eventual map destiny. Keep influential people often holding clues, the conditional evil holder, sealed Proof mysteries, big-town/nearby-ruins clues, the Women punchline and Lil's follow-up, sailors' worldwide daily tales, probable payment and shared treasure-value give-and-take. Add no degree, kinship, rank, specific blow, map assembly, military-only requirement, immediate award, source port, gift, price or romance. The current reviewed Help title Proof of Conquest and source abbreviations are bound; earlier exact-record Proof variant consistency remains open.

Source-owned contracts preserve36 progressive speeches, selectors2/6/9/20/21/76, FI5/FO2,53 commands,twelve relative sites/120 structural cases,three membership predicates,five nonrelative leaves,one later A000 and one end2558. Actor15 is Ian21;4C is Mikhail76. Twelve original progressive/full-name consumers preserve owned scratch rings/writes and all4MiB restoration. Keep source-spoken Mikhail Letzel without adding catalogue-only Volk. The later A000 has numeric29/0001 operands; no recruitment or earned flag effect is claimed. There are no FE,typed choices,resources,presentation or pause objects in this block. Offline probes do not establish source-event eligibility or full VM effects. The later older-record technical re-audit remains open.

Native approval V4230 covers all36 complete216x64 progressive planes and288 logical/compiled alignment cases, with every leading/internal/final glyph,unique cell,zero row origin,four-row bound and single-page target complete. All five final native sheets were viewed.21 source-consumer,two missing-macro and14 formatter rejection controls pass. Fourteen narrow row-count notes exempt no glyph,bounds,pagination,macro,control,weak-ending,orphan or blank-page issue. Three earlier phrase-flow findings are resolved with full-meaning prose refinements and stronger phrase boundaries; no wording waiver,authored break,padding,shared guard or metric change. No B169 actual gameplay or transition coverage is claimed yet.

Coverage becomes5692 fresh contextual rereads:5656 integrated/completed and36 pending. Source/prose becomes5695,including3839 SC2 and unchanged64 SC3;reviewed/completed route objects4093/4057. Historical completed decisions remain3595 revised/2061 retained. B169 is credited once as pending,with no completion credit. Promoted V4204 remains544 manuscript batches/114 accepted layers with its exact clean-input patch;registry,builder,promoted pointer,immutable canonical input and every prior completed record stay unchanged.

Remaining B170-B180 contains231 physical speeches and zero typed-choice-command leads,not a full Lil/project denominator. Every remaining storyline,shared shop/town exchange,random scene,Help page and other player-facing prose stays open. Preserve COMMON750-752,canonical Maria32 SC3 B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques remain separate;retain the later older-record technical re-audit/queued0D gap. Full goal active.'''

if __name__ == '__main__':
    assert not ROOT.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    ledger = read(lp)
    assert sha(lp.read_bytes()) == read(PRIOR)['ledger_sha256']
    approval, doc = read(APPROVAL), read(DOC)
    assert approval['manuscripts'] == {str(DOC):sha(DOC.read_bytes())}
    rows = doc['records']
    assert len(rows) == 36 and all(all(r['review'].values()) for r in rows)
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release']) == (5656,5656,0)
    selected = [dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    assert len({historical_key(r) for r in selected}) == 36
    assert not {historical_key(r) for r in selected} & {historical_key(r) for r in fresh['record_keys']}
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] == 3803
    assert ledger['records_with_source_and_prose_pass'] == 5659
    docs = [Path('docs')/name for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4226')
    ROOT.mkdir(parents=True)
    for path in [lp,*docs]:
        copy2(path,ROOT/(path.name+'.before'))
    ledger['records_with_source_and_prose_pass'] = ledger['records_with_source_prose_drafts'] = 5695
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] = 3839
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'] = [r['id'] for r in rows]
    active = ledger['active_source_prose_drafts']
    assert str(DOC) not in active['manuscripts']
    active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(DOC)] = [r['id'] for r in rows]
    note = '5692 fresh rereads:5656 integrated/36 pending;source/prose5695. B169 credited once as pending;no completion or actual scene credit.'
    active.update(status='3-reviewed-COMMON-incomplete;36-Lil-B169-native-approved-pending-release',note=note)
    pending = dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[169],records=36,record_keys=selected,
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),manuscripts=approval['manuscripts'],
        proposed_revisions=19,retentions=17,source_prose_reviews_added=36,completion_credit_added=0,
        pending=NEXT,new_emulator_runs=0,actual_selected_B169_IDs=[])
    fresh['record_keys'].extend(selected)
    fresh['record_IDs'].extend(r['id'] for r in rows)
    fresh.update(fresh_pass_records_explicitly_reread=5692,fresh_pass_records_integrated=5656,
        fresh_pass_records_pending_native_actual_release=36,pending_record_keys=selected,
        pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,
        latest_contextual_manuscript=str(DOC),coverage_note=note)
    for unit in ledger['coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4093,completed_route_records=4057,next=NEXT)
    ledger['coverage_units'].append({**pending,'status':doc['status'],'full_goal_complete':False})
    ledger['formatting_watchlist']['lil_B169_v4231'] = dict(status='native-approved;pending-relocation-representative-release',
        approval=str(APPROVAL),approval_sha256=sha(APPROVAL.read_bytes()),row_count_notes=14,
        all5_speech_sheets_viewed=True,actual_selected_B169_IDs=[],new_emulator_runs=0)
    previous = ledger['unfinished_editorial_scope_v4208']
    assert sha(Path(previous['path']).read_bytes()) == previous['sha256']
    inventory = deepcopy(read(previous['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=[169],count=36,record_IDs=[r['id'] for r in rows])],
        incomplete_route_source_prose_count=36,next_focus=NEXT)
    inventory['B169_fresh_context_review_checkpoint_v4231'] = pending
    inventory['remaining_B170_B180_unreviewed_uncredited'] = dict(physical_speeches=231,typed_choice_command_leads=0,not_full_Lil_or_project_denominator=True)
    inventory['earlier_B169_uncredited_leads_are_historical_after_V4231'] = True
    for unit in inventory['broader_coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4093,completed_route_records=4057,source_prose_pending_records=36,source_prose_pending_family=FAMILY,next=NEXT)
    inv = ROOT/'unfinished_editorial_scope_inventory.json'
    save(inv,inventory)
    ledger['unfinished_editorial_scope_v4231'] = dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,
        incomplete_route_source_prose=36,remaining_B170_B180_physical_speeches=231,remaining_choice_command_leads=0,
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
    ledger['lil_B169_scope_reconciliation_v4231'] = dict(summary=SUMMARY,evidence=evidence,pending_family=pending,
        source_prose_reviews_added=36,completion_credit_added=0,full_goal_complete=False)
    ledger['latest_checkpoint'] = SUMMARY
    planned = {lp:(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')}
    section = '## V4231:36 B169 contextual/native reviews;integration pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\nNext: '+NEXT+'\n\n'
    for index,path in enumerate(docs):
        first,rest = path.read_text(encoding='utf-8').split('\n',1)
        planned[path] = (('# Current editorial handoff - V4231' if index==0 else first)+'\n\n'+section+rest).encode('utf-8')
    staged = ROOT/'staged'
    staged.mkdir()
    plan = []
    for index,(path,data) in enumerate(planned.items()):
        output = staged/(str(index)+'.planned')
        output.write_bytes(data)
        plan.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(output.resolve()),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',plan)
    stable = ['translations/release_stack.json','translations/promoted_build.json','scripts/build_integrated_release.py']
    save(ROOT/'staged_receipt.json',dict(checkpoint='V4231',evidence=evidence,
        preserved_release_files={p:sha(Path(p).read_bytes()) for p in stable},prior_verified_handoff=str(PRIOR),
        new_source_prose_reviews=36,new_completed_records=0,proposed_revisions=19,justified_retentions=17,
        fresh_reread=5692,fresh_integrated=5656,fresh_pending=36,source_prose=5695,completed=5656,
        historical_revised=3595,historical_retained=2061,new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V4231 staged:5692 reread/5656 integrated/36 pending;5695 source/prose. Promoted V4204 unchanged;full goal active.')
