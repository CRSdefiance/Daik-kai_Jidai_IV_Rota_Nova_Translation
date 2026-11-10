"""Reversibly record the source-specific name retention without new dialogue credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Maria_B36_v7826b import COUNTERS,AFTER,INTRO,DETAILS,NEXT as PREVIOUS_NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_actual_checkpoint_v7899')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7900')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7891/verified_handoff.json')
PROOF=Path('work/analysis/Rafael_B45_actual_approval_v7898/12_source_context_native_actual_format_approved_policy_release_pending.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Rafael_SC0B45_actual_native_approved_pending_production_v7899'
SCOPE='unfinished_editorial_scope_v7899'
FINDING="The current registered cumulative ROM is still V7857; promoted main V4701 is unchanged. The 632-batch stack retains all 114 accepted layers, its verified 18 release checks and 110 regressions, whole-ROM research-reference equality, and exact clean-input patch reconstruction. The ledger remains at 6938 completed records / 6941 source-prose records and drafts / 4347 integrated wording revisions / 2591 retentions. Rafael B45 has not yet been integrated, so none of its twelve records receives completion credit at this checkpoint.\n\nRafael's complete SC0 B45 trade tutorial has now passed the fresh clean-Japanese whole-exchange review, source/current names and effective dispatch, native layout and stored-body checks, exact relocation and reference checks, and paired actual gameplay. The approved manuscript is translations/rafael_B45_editorial_manuscript_v4.json: seven wording revisions and five individually justified retentions, with all five per-record review gates true. This approves source, context, prose and formatting; the frozen policy, atomic production compiler and registered cumulative integration are still pending. Canonical speaker/macro markup now matches the exact previously tested plans without changing any English words or compiled bytes.\n\nThe revisions preserve conditional Lisbon cargo, the local ruler's contract fee paid at the Palace or Governor's Office, early minimum-fee advice, Julio's Ceuta contract and Rafael's future responsibility, and the optional sale. Clean Help150 supports specifying purchases in the market-share explanation: share limits the purchasable portion of local stock, while 1 percent permits unlimited selling. The FE panel preserves FO, Ceuta and 20 percent without inventing a proportional sales cap or company ownership. Rafael Castor and Julio Erneco are retained from the clean fields and original given/full getters; エルネコ does not justify changing Erneco to Ernesto. Both actual progressive nameplates are now verified. Other full-name catalogue UI and the wider 207-name/role/alias review remain open.\n\nTwo 16001-frame source/English headless emulator tests are terminal and their session handles were reaped. Both use identical ordinary New Game/A inputs, no battery or savestate, and a disclosed ROM entry fixture consisting of the exact source-bound original B44 ten-command prelude followed by the entire original B45 exchange. All twelve stored speeches play in each language, including the FE panel selected by the original unforced predicate result 1. Each trace has 32 completed commands: ten original setup commands plus 22 selected B45 commands. The original 0300 skips the 0400 and outer 0100 objects; those two have native five-result coverage, not individual gameplay execution. No source speech, branch, resource command, effect or end was omitted. All five relative spans remain unchanged under the constant 32-byte fixture shift.\n\nAll 24 complete actual source/English pages match their independent native masks across 90 complete holds: 84 progressive body/nameplate holds and six FE body/absent-nameplate holds, with zero partial eligible samples, unknown commands or unfinished calls. Both jobs reach the normal four-byte type-0 end at frame 6653 and preserve value 1. The source FE CP932 foreground and light-gray shadow, English FE ink, FO expansion, exact 20-percent wording, all leading/internal/trailing characters, both complete names and portrait/header transitions pass. All 24 panes across four sheets, two transition sheets, and the paired later-screen sheet were directly viewed. This is an initialized Lisbon fixture, not natural B45/Ceuta event selection, original event location, a complete route or hardware verification. Incidental Trader/trade UI after the return receives no new editorial credit.\n\nAll twelve paired upper scenes, portraits and header regions match. All selected command results and UI request words match. Both final full actor objects and the five measured state/model/persistent-object/task/calendar components match, as do all 157 unmasked later RGB pairs from frames 6730 through 16001. Preserve the 21 command-comparison difference rows and seven duration differences. Exact RNG state does differ: final seeds are 2420418440 and 1937175841, with English exactly one original LCG step ahead. The first divergence is Julio's R9 reply: source 237 frames/57 LCG advances versus English 240 frames/58 advances. Later speech waits add or remove single advances; the exchange has one net extra English advance, while the post-return step counts match. Every non-speech B45 command observes zero RNG advances.\n\nThe generator, seed address and cooperative-yield code are byte-identical to clean and the earlier source semantics proof. Original C9DA0 calls the generator and C9DA8 overwrites its return with zero. These facts support the observed difference being consistent with original discarded wait timing. No fresh every-call caller trace or complete causal/future-outcome equivalence is claimed. Keep the one-step difference, all timing rows and the later older-record technical re-audit; do not force seeds or retime inputs merely to make hashes equal. Passing images and sampled component equality do not prove identical future random outcomes.\n\nReuse the completed source/native work without replay: all twelve compiled/stored complete pages, measured FI6/FA6/FO10, the original 00 preambles and body-NUL guard, the distinct 228px FE bitmap with 216px usable text, five relative fixups/25 relocated native cases, exact clean/predecessor block and archive inverse, final dispatches and seeded ends, all 343 SC0 load/cache paths, 686 initial parent modes, and the shipped-caller census. The pinned research reference and both scene fixtures remain unregistered research, not the canceled separate unified package, new parents or promoted builds. Earlier failed schema/format producers, partial artifacts and all successful outputs are preserved.\n\nThe full objective remains active across all four storylines, earlier translated dialogue, shared shop/town/random scenes, Help and remaining player prose, all 207 names/roles/aliases, twelve remaining retrospective wrap leads and the unscanned portion beyond the 558-plan heuristic, and every older item/counterpart/display lead. Keep source-supported Sailor151-159 separate from the Retainer full-name consumer. Graphics/all 18 plaques and the later older-record technical re-audit stay separate. Preserve every generated ROM and earlier translation. No canceled separate package, promotion, pruning, commit or push."
NEXT="Continue from verified V7900/current V7857 and translations/rafael_B45_editorial_manuscript_v4.json plus translations/rafael_B45_speaker_name_review_v2.json. The authoritative actual approval is work/analysis/Rafael_B45_actual_approval_v7898/12_source_context_native_actual_format_approved_policy_release_pending.json. It binds the actual audit at work/analysis/Rafael_B45_actual_v7895b/paired12_source_English_actual_body_name_FE_branch_andnormal_return_audit.json, comparison at work/analysis/Rafael_B45_actual_comparison_v7896b/12_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json, and RNG limit at work/analysis/Rafael_B45_random_waits_v7897/actual_one_step_RNG_phase_andunchanged_source_discarded_wait_contract.json.\n\nNext freeze a strictly scoped natural-dialogue-v2 profile/formatter from the exact approved plans and final v4 markup. Require the original clean/current B45 record bodies, complete six-byte preambles, current ARM9/COMMON/font, measured FI6/FA6/FO10, the actual approved source/current consumer distinction and all native/reference proofs. Preserve the original body encoder's embedded-NUL rejection: actor00 belongs to the native preamble, not ordinary text. FE uses original null-actor24310 then5473C, with a 228px bitmap but measured216px usable text; do not revive the rejected bitmap-width plan. Replay the deterministic automatic planner and all QA for positives; test actual changing negative inputs, including source/body/speaker/macro/consumer/runtime/profile/manual-break/printf/record-gate corruption. Do not replace meaningful checks with report flags or blanket phrase waivers.\n\nThen implement and audit the atomic production stage, preserving all 24 commands, five relative fixups/nested scopes, exact two-way inverse and all 342 other SC0 blocks. Require exact whole research-reference ROM equality, meaningful production rejection tests before mutation, registered dependency order after the full V7857 stack, all 114 accepted layers and regressions, exact clean-input patch reconstruction and appropriate startup controls. Integrate the twelve reviewed records once these necessary checks pass; add seven revision/five retention credits only after registered integration. Expected counters after that single batch would be 6950 completed, 6953 source-prose/drafts, 4354 integrated wording revisions and 2596 retentions; current counters remain unchanged until then. Keep main V4701 unchanged.\n\nReuse the completed actual tests and native source/current/compiled/stored/loader/caller proofs by exact hashes. Both source/English tests already play all twelve speeches and the unforced FE path, with 90 complete holds, matching headers and normal [0,1] returns at6653; all seven actual/comparison sheets have been viewed. Retain the real one-step RNG phase difference and all timing rows without claiming exact future-random or full simulation equality. No need to replay the full scenes unless a new change or concrete unresolved risk requires it. All actual jobs are terminal/reaped.\n\nOwn current Rafael input remains work/analysis/current_V7857_Rafael_native_v7868/current_native_input.json; own current Lil input is work/analysis/current_V7857_Lil_native_v7860/current_native_input.json. The scene fixtures are not replacement current native contexts. Maria's V7821 context remains historical to V7857. Continue all four storylines and previous translations, practical broad town/shop/random capture, Help/remaining prose, names and retrospective wraps; preserve every older unfinished inventory and technical lead. Graphics/all 18 plaques and the later older-record technical re-audit stay separate. Preserve every ROM, translation, executed/failing producer and proof. No canceled separate package, promotion, pruning, commit or push."
SUMMARY=FINDING

def restore(value):
    new=deepcopy(value);entry=new.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(new,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return new

def gates():
    prior,proof=map(read,[PRIOR,PROOF])
    manuscript=read(proof['manuscript']);actual=read(proof['actual_proof'])
    comparison=read(proof['comparison']);rng=read(proof['RNG_measurement'])
    assert sha(Path(proof['manuscript']).read_bytes())==proof['manuscript_sha256']
    assert len(manuscript['records'])==12 and sum(r['decision']=='revision' for r in manuscript['records'])==7
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness','formatting']) for r in manuscript['records'])
    assert not manuscript['formatting_review_pending'] and not proof['new_credit'] and not proof['new_emulator_runs']
    for key in ['actual_proof','comparison','RNG_measurement','names']:
        assert sha(Path(proof[key]).read_bytes())==proof[key+'_sha256']
    assert not actual['unresolved'] and len(actual['groups'])==2
    assert sum(g['complete_body_holds'] for g in actual['groups'])==90
    assert all(g['actual_unique_speeches']==12 and g['native_terminal_result']==[0,1] and g['exit_frame']==6653 for g in actual['groups'])
    assert comparison['groups'][0]['later_sample_count']==157 and not comparison['groups'][0]['later_RGB_differences']
    assert all(comparison['groups'][0]['five_native_component_equality'].values()) and comparison['groups'][0]['whole_actors_equal']
    assert rng['English_exactly_one_LCG_step_ahead_at_end_andfinal'] and rng['exact_random_state_andfuture_random_outcome_equality_NOT_verified']
    assert len(proof['directly_viewed_sheets'])==7 and all(s['directly_viewed'] for s in proof['directly_viewed_sheets'])
    for g in actual['groups']:
        terminal=read('work/analysis/Rafael_B45_scene_runs_v7893/route0_'+g['version']+'/terminal.json')
        assert terminal['terminal'] and terminal['frames']==16001 and terminal['all_callbacks_readonly_andhost_slots_restored']
        assert sha(Path(g['capture_report']).read_bytes())==g['capture_report_sha256']
        assert sha(Path(g['observer_report']).read_bytes())==g['observer_report_sha256']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==manuscript['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    return prior,proof

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,proof=gates()
    if mode=='stage':
        assert not ROOT.exists()
        before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and KEY not in old
        assert tuple(old[k] for k in COUNTERS)==AFTER and old['goal_status']=='active' and not old['full_goal_complete']
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
            ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        oldscope=old['unfinished_editorial_scope_v7890'];assert sha(Path(oldscope['path']).read_bytes())==oldscope['sha256']
        inventory=deepcopy(read(oldscope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(proof=str(PROOF),proof_sha256=sha(PROOF.read_bytes()),finding=FINDING,
            clean_source_speeches=12,pending_wording_revisions=7,pending_wording_retentions=5,current_English_bodies_unread=False,all_prior_inventories_andfull_scope_preserved=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_andfull_scope_preserved=True,new_credit=0,full_goal_complete=False))
        put(['formatting_watchlist',KEY],dict(proof=str(PROOF),finding=FINDING,native_names_macros_branches_current_English_compiled_stored_andactual_pages_complete=True,policy_atomic_registered_release_pending=True,new_credit=0))
        put(['Rafael_SC0B45_native_actual_release_pending_v7890','superseded_by'],KEY)
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        index=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
        put(['coverage_units',index,'next'],NEXT)
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,PROOF,scope,Path(__file__),
            Path('translations/rafael_B45_editorial_manuscript_v4.json'),Path('translations/rafael_B45_speaker_name_review_v2.json'),
            Path('work/analysis/Rafael_B45_scene_fixtures_v7892/two_complete_source_English_original_Rafael_prelude_fixtures.json'),
            Path('work/analysis/Rafael_B45_scene_runs_v7893/route0_clean_Japanese/terminal.json'),
            Path('work/analysis/Rafael_B45_scene_runs_v7893/route0_English/terminal.json'),
            Path('work/analysis/Rafael_B45_source_name_planes_v7894/12_complete_source_pages2_names8_literal_alignments_distinct_FE.json'),
            Path('work/analysis/Rafael_B45_actual_v7895b/paired12_source_English_actual_body_name_FE_branch_andnormal_return_audit.json'),
            Path('work/analysis/Rafael_B45_actual_comparison_v7896b/12_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json'),
            Path('work/analysis/Rafael_B45_random_waits_v7897/actual_one_step_RNG_phase_andunchanged_source_discarded_wait_contract.json')]}
        new[KEY]=dict(summary=FINDING,next=NEXT,proof=str(PROOF),evidence=evidence,inverse_operations=ops,
            clean_source_speeches=12,pending_wording_revisions=7,pending_wording_retentions=5,no_source_prose_orcompletion_credit=True,
            new_credit=0,new_emulator_runs=2,new_actual_frames=32002,scoped_new_name_literal_alignment_cases=8,
            source_first12_native_actual_prose_andformat_approved_frozen_policy_atomic_registered_release_pending=True,
            full_scope_remaining12_wrap_leads_andnames_remain_open=True,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['completed_editorial_families']==old['completed_editorial_families']
        assert new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        targets={LEDGER:encode_ledger(new)}
        section='## V7899: Rafael B45 source/native/actual review approved; production/integration pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V7899; V7857 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,zero_credit=True,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six Rafael actual-progress checkpoint targets staged;all counts andcurrentROM unchanged.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER
        assert new['goal_status']=='active' and not new['full_goal_complete']
        assert new['completed_editorial_families']==old['completed_editorial_families'] and new['current_integrated_candidate']==old['current_integrated_candidate']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),
                all_prior_roots_families_counters_currentROM_andhistory_recover_exactly=True,zero_credit=True,full_goal_complete=False))
            print('Deep inverse andall six before/planned hashes pass;zero credit.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists()
            assert read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            workspace=Path.cwd().resolve()
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(workspace) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,no_ROM_orcredit_change=True,full_goal_complete=False))
            print('Six audited Rafael actual-progress checkpoint targets applied;V7857/6938completed unchanged.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_hash_exact']
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),
                previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                Rafael_B45_clean_source_review_pending=False,Rafael_B45_fresh_clean_glosses=12,Rafael_B45_current_English_bodies_unread=False,Rafael_B45_native_layout_relocation_andreferences_complete=True,Rafael_B45_actual_gameplay_policy_atomic_andintegration_pending=False,Rafael_B45_actual_gameplay_andvisual_review_approved=True,Rafael_B45_policy_atomic_registered_integration_pending=True,Rafael_B45_one_step_RNG_limit_retained=True,
                recorded_markup_plans_scanned=558,completed_records_not_in_markup_scan=6380,
                pending_Rafael_actual_approval=str(PROOF),pending_Rafael_actual_approval_sha256=sha(PROOF.read_bytes()),pending_Rafael_manuscript='translations/rafael_B45_editorial_manuscript_v4.json',
                Rafael_B45_own_current_route0_context_pending=False,strict_own_Rafael_current_input='work/analysis/current_V7857_Rafael_native_v7868/current_native_input.json',
                unfinished_scope=SCOPE,next_required=NEXT,latest_checkpoint=KEY,
                new_credit=0,new_emulator_runs=2,new_actual_frames=32002,scoped_new_name_literal_alignment_cases=8,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('V7900 verified:Rafael B45 all12 source/native/actual/formats approved;policy/atomic/integration pending.One-step RNG limit retained.V7857/6938completed unchanged.Fullgoal active.')
