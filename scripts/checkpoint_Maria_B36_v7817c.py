"""Reversible full-scope handoff for16 sealed decisions; credit awaits atomic registered release."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.Maria_B36_final_paths_v7816b import *
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B36_checkpoint_v7817c')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7817d')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7785b/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Maria_SC3B36_sealed_pending_v7817c'
SCOPE='unfinished_editorial_scope_v7817c'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
VALUES=(6922,6925,6925,4338,2584)
SUMMARY="""V7779 remains the registered experimental current ROM: 630 batches, 114 accepted layers, 18 passing release checks, 110 regressions and the exactly reconstructable clean-input patch. Main V4701 is unchanged. Counts remain 6,922 completed, 6,925 source/prose records and drafts, 4,338 integrated revisions and 2,584 retentions. Route 5,322/5,322 is a subset, not the full goal denominator.

The next Maria exchange, SC3 B36, is reviewed and sealed but not integrated or credited. Its 16 complete clean Japanese speeches were read and freshly glossed before current English. EV3 event36/action37/block36 requires completed35; additional eligibility, immediate chronology, natural activation and location are separate. Preserve Lil's departure question, Xien's recognition, Maria's direct introduction, Lil's fear of being killed, Maria's denial and purpose, Lil's beliefs about Kuhn helping Southeast Asia's people, her accusation about China's underworld, Maria's warning about Kuhn's intended use and elimination, Lil's proof challenge and refusal, and Maria's exasperation. These are attributed arguments, not narrator facts. No invented rank, kinship, romance, rescue, battle, method, deadline or guaranteed mechanic. Actor0A is Xien, not Camille09; inherited initialization graphics do not prove Camille attended.

Final English has nine revisions and seven individually justified retentions at R5/R9/R12/R16/R27/R31/R60. Manuscript v1 and its rejected R23 substitution order remain. V2 naturally says I'm with FO. My name is FI. Surely you've heard of me, preserving original FO before FI. All three real substitutions remain: FI2/FO1, no FA. Own-V7779 captain3 context measures FI5/FA2/FO7. Three static actors2/3/10 and six native progressive/full getters support Lil Argot, Maria Li/full Maria Huamei Li and Xien Yan. All three progressive headers are actually observed; full catalogue UI and all207 names/roles/aliases remain open. No name asset changed.

All 16 English speeches fit complete original216px/four-row single pages. Final logical and compiled coverage each totals64 alignments, with four fresh changed cases and60 exact own-context reuse; stored coverage64 has44 fresh parity-tail cases and20 exact compiled reuse. Eleven storage parity spaces add zero ink. Complete first/internal/final glyphs, independent font masks, bounds, canaries, guards and consumption pass. Nine individual line-count infos are explicitly justified; there are no warnings or waivers. A scoped ordinary soft-wrap preference keeps He's a great merchant! together, with no prose, width, font, global QA or authored-break change. Three original native sheets and one final changed preview were viewed; all earlier plans, failures and pixels remain.

The research archive changes only B36: previous/clean1068 bytes, logical1066/tail2 -> target1064 bytes, logical1064/tail0. All16 six-byte preambles, selectors, macro order, all22 native commands and six numeric leaves are preserved. There are no relative or in-block predicate commands. Original6000 setup,633D/632A resource boundaries,623D/A000 structural decoder cases and complete four-byte ends are bound; resource callee bodies and structural effects are not full mechanics. Twenty resource,ten setup and15 zero-initialized end boundary cases pass. Complete clean/previous block and full previous archive invert exactly;302 other SC3 blocks and every other file/component remain exact. Original303 full loads/cache hits,606 parent modes and the shipped caller census bind the new reference.

Two16001-frame headless source/English jobs are terminal and reaped. Their complete original exchange is behind the exact seven original B33 setup commands, with identical ordinary inputs and the existing exact system-only unlock, earned=false. No historical RAM overlay, savestate, runtime/role/roster/funds/RNG/condition/result forcing. Each plays all16 speeches and29 fixture commands, with16 complete single pages and66 complete body/nameplate holds; total32 panes/132 holds, zero partial sampled holds, unknown traces or unplayed lines. Source and English black, ASCII-gray, CP932-gray and full-name masks all match. All32 exact pane crops, six panel sheets, two transition sheets and one late-comparison sheet were viewed. All16 paired upper scenes/portraits/nameplates, command results and UI requests agree.

Preserve the actual exit difference8213/8216, all18 command-comparison rows and six duration differences. Later108/131 whole-RGB samples differ. State/tasks/calendar agree; models/persistent objects and whole actors differ. Final seeds are164302531/4157282706. Retain all raw timing, RNG, component, actor, calendar, following-command and RGB measurements. Initialized Hangzhou return8300 is not the original optional scene location or natural activation. Incidental later navigation/sailing and Maria level-up text earn no editorial credit. No every-frame/full-RAM/future/broad-simulation/causal-equivalence claim. Keep these measurements for the later older-record technical re-audit.

Frozen policy passes16 positives and81 actual-changing guard rejections, including three macro erasures and20 meaning corruptions. V3 individually approves all five review gates; v4 seals exact source/current/effective/compiled/stored/actual references and full inverse. Native rendering failures are not hidden:7793 rejected reordered FI/FO;7801 found missing written info reasons and7801b adds only metadata;7815's incorrect plan-schema key is corrected in planner/formatter v2;7816's code-generation quote failure is preserved and repaired by7816b. None is a ROM failure or counted policy rejection. All source-locked successors preserve original native numeric/ownership guards. Atomic production/challenges, registered cumulative reconstruction, exact clean-input patch, own-build startup and once-only completion credit remain pending.

The full four-storyline, earlier-translation, broad practical shared town/shop/random, Help/player prose, all207-name and retrospective premature-wrap objective remains active. Preserve every prior family, unfinished inventory, ROM, translation, draft, executed producer, failure, proof, trace and pin. Shared151–159 Sailor/Retainer semantics and all other role/item/counterpart leads remain open. Graphics/all18 plaques and the later older-record technical re-audit remain separate. No separate test package, promotion, pruning, commit or push."""
NEXT="""Continue from sealed Maria B36 v4 and the current V7779 registered ROM. Use scripts/Maria_B36_final_paths_v7816b.py for exact paths and scripts/Maria_B36_policy_paths_v7815b.py for the corrected immutable formatter/planner v2. Do not rerun the unchanged source glosses, name/macro/current dispatches, logical/compiled/stored fonts, original controls, loader/caller checks or paired scene captures.

Next implement one atomic SC3 production reconstruction using the existing maria_story_reconstruction_v1.py helper and the sealed single-group map. Bind16 decisions/9 revisions/7 retentions;22 commands, no relative or in-block predicate commands;11 parity tails; previous1068/logical1066/tail2 and target1064/logical1064/tail0. Preserve all302 unowned blocks and all other files/components. Add actual-changing production challenges with dependency digests bypassed and no commit before full validation. Reuse the unchanged source-bound native helpers, not older-route RAM or old67/20-branch counts.

After production guards pass, register the new layer after V7779 and use only the registered cumulative builder, all required checks, exact clean-input patch and own-build representative startup. Credit16 source/prose/completion records once only after necessary release checks pass. Keep all measured differences and source-fixture/unlock limits. Continue the remaining full editorial/name/town/random/Help/prose and retrospective-wrap work; the short contracted-predicate wrap finding is also a lead for earlier reviewed paragraphs, with no duplicate credit or global QA waiver. MainV4701 remains; no canceled separate unified test package, automatic promotion, pruning, commit or push."""
def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result
def gates():
    prior,doc,approval,seal,policy=map(read,[PRIOR,SEALED,APPROVAL,SEAL,POLICY])
    assert sha(PARENT.read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    assert seal['manuscript_sha256']==sha(SEALED.read_bytes()) and approval['all16_individual_five_gates_approved']
    assert len(doc['records'])==16 and all(all(r['review'].values()) for r in doc['records'])
    assert policy['positive_count']==16 and policy['negative_count']==81 and read(VIEW)['complete_body_andheader_holds']==132
    assert read(ACTUAL)['total_actual_speech_occurrences']==32 and not read(ACTUAL)['unresolved']
    return prior,doc
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,doc=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256']
        assert tuple(old[k] for k in COUNTERS)==VALUES and old['goal_status']=='active' and not old['full_goal_complete']
        candidate=old['current_integrated_candidate'];manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
        assert candidate['profile']=='all-routes-unified-v7779' and len(manifest['batches'])==630 and len(manifest['checks'])==18 and all(manifest['checks'].values())
        assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
        assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
        completed={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
        assert len(completed)==6922 and not completed&{historical_key(r) for r in doc['records']}
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);exists=key in parent if isinstance(parent,dict) else key<len(parent)
            ops.append(dict(path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
        previous=old['unfinished_editorial_scope_v7784b'];assert sha(Path(previous['path']).read_bytes())==previous['sha256']
        inventory=deepcopy(read(previous['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(manuscript=str(SEALED),reference_map=str(MAP),actual_view=str(VIEW),records=16,revisions=9,retentions=7,
            all_five_gates_true=True,atomic_production_registered_release_pending=True,new_credit=0)
        inventory['retrospective_short_contracted_predicate_wrap_lead_v7817c']=dict(
            example_plan='work/analysis/maria_confrontation_wrap_v7799/16_plans_one_sentence_coherence_refinement_no_prose_change.json',
            original_boundary="He's / a great merchant!",source_scoped_soft_wrap_preference=True,
            earlier_reviewed_paragraphs_require_current_source_context_andconsumer_binding_before_any_change=True,
            no_global_QA_orwidth_change_no_duplicate_credit=True)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_full_scope_andhistory_preserved=True,new_credit=0,full_goal_complete=False))
        put(['formatting_watchlist',KEY],dict(all16_native_stored_actual_policy_andreference_gates_pass=True,
            final16_single_pages=True,info_reasons=9,warnings=0,all_old_failures_andsuccessors_preserved=True,
            atomic_registered_release_pending=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        i=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes');put(['coverage_units',i,'next'],NEXT)
        paths=[PRIOR,DRAFT,APPROVED,SEALED,MAP,APPROVAL,SEAL,RELOCATION,PLAN,*map(Path,proofs().values()),
            Path('work/analysis/maria_confrontation_scene_tools_v7805/provenance.json'),
            Path('work/analysis/maria_confrontation_row_reasons_v7801b/binding_receipt.json'),
            Path('work/analysis/maria_confrontation_policy_validation_tools_v7815b/provenance.json'),
            Path('work/analysis/maria_B36_approval_repair_tools_v7816b/provenance.json'),
            Path('scripts/Maria_B36_final_paths_v7816b.py'),Path('scripts/Maria_B36_policy_paths_v7815b.py'),
            Path('dk4tool/dialogue/maria_B36_layout_v2.py'),Path('dk4tool/dialogue/maria_B36_plan_v2.py'),
            Path('dk4tool/patch/maria_story_reconstruction_v1.py'),scope,Path(__file__)]
        terminals=list(Path('work/analysis/maria_confrontation_scene_runs_v7809').glob('*/terminal.json'))
        assert len(terminals)==2 and all(read(p)['terminal'] and read(p)['frames']==16001 for p in terminals)
        evidence={str(p):sha(p.read_bytes()) for p in [*paths,*terminals]}
        new[KEY]=dict(records=deepcopy(doc['records']),proposed_revisions=9,proposed_retentions=7,summary=SUMMARY,next=NEXT,
            evidence=evidence,inverse_operations=ops,new_source_prose_reviews=0,new_completed_records=0,new_revisions=0,new_retentions=0,
            no_ROM_registry_completed_family_orcounter_changes=True,new_emulator_runs=2,new_actual_frames=32002,
            actual_speeches_each_language=16,actual_pages=32,complete_body_andheader_holds=132,
            all_native_actual_policy_reference_gates_pass_atomic_registered_release_pending=True,
            goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['completed_editorial_families']==old['completed_editorial_families'] and new['current_integrated_candidate']==candidate
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V7817c: Maria–Lil confrontation16 sealed; atomic registered integration pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V7817c; V7779 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,zero_credit=True,full_goal_complete=False))
        print('Six checkpoint targets staged;16sealed/uncredited,currentV7779/6922completed unchanged.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==VALUES and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),
                all_prior_roots_families_records_counters_andROMs_recover_exactly=True,zero_credit=True,full_goal_complete=False))
            print('Deep inverse audit passes;all prior roots/families/counters/currentROM/history preserved.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            workspace=Path.cwd().resolve()
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(workspace) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,no_ROM_orcredit_counter_change=True,full_goal_complete=False))
            print('Six audited checkpoint targets applied;16uncredited,currentV7779/mainV4701 unchanged.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                Maria_B36_sealed_uncredited=True,Maria_B36_manuscript=str(SEALED),Maria_B36_manuscript_sha256=sha(SEALED.read_bytes()),
                Maria_B36_revisions=9,Maria_B36_retentions=7,Maria_B36_actual_speeches_each_language=16,
                Maria_B36_actual_pages=32,Maria_B36_complete_body_andheader_holds=132,
                Maria_B36_policy_positive16_negative81=True,Maria_B36_reference_seal=str(SEAL),
                next_required=NEXT,unfinished_scope=SCOPE,pending_checkpoint=str(ROOT/'application_receipt.json'),
                new_credit=0,new_emulator_runs=2,new_actual_frames=32002,full_goal_active=True,full_goal_complete=False,
                producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',verified)
            print('V7817c verified:Maria B36 16sealed/native/actual/policy/reference done;atomic release pending.V7779/6922completed unchanged.Fullgoal active.')
