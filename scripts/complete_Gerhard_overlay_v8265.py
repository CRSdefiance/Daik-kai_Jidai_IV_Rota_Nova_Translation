"""Reversible zero-credit registered overlay for five old revisions andone owned name; full objective stays active."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.gerhard_surname_profile_v1 import validate_approved_batch,validate_runtime
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B50_v8184 import COUNTERS,AFTER
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Gerhard_registered_overlay_v8265')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8266')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8250/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/gerhard_surname_consistency_manuscript_v3.json')
OLD_KEY='Hodram28_contextual_prose_native_bodies_Gerhard_frozen_policy_pending_atomic_actual_registered_v8249'
KEY='Gerhard_Adernkatz_registered_V8259_Hodram28_pending_stored_names_actual_policy_release_v8265'
SCOPE='unfinished_editorial_scope_v8265'
PROOFS={
 'release':'work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json',
 'startup':'work/analysis/Gerhard_registered_binding_v8262/own_registered_startup_andstrict_captain2_context.json',
 'startup_view':'work/analysis/Gerhard_registered_startup_view_v8263/own_registered_startup6_RGBpairs_actor_equal8_fresh_getters_direct_view.json',
 'own_Lil_input':'work/analysis/current_V8259_Lil_native_v8262/current_native_input.json',
 'policy_tests':'work/analysis/Gerhard_policy_validation_v8237/five_body_one_name_policy_positives_andexpected_guard_rejections.json',
 'reference_seal':'work/analysis/Gerhard_reference_seal_v8238/five_body_one_name_exact_reference_andactual_scope_approved.json',
 'atomic_positive':'work/analysis/Gerhard_atomic_positive_v8256/one_whole_NDS_commit_exact_reference_andunchanged_precommit_input.json',
 'atomic_negatives':'work/analysis/Gerhard_atomic_challenges_v8257/actual_changing_semantic_precommit_rejections.json',
 'native_actual':'work/analysis/Gerhard_independent_evidence_v8251/native_models_actual_masks_commands_andfixtures_independently_revalidated.json',
 'native_comparison':'work/analysis/Gerhard_independent_comparison_v8252/all_saved_command_RGB_andfinal_native_values_recomputed.json',
 'registration':'work/analysis/Gerhard_surname_registration_v8258/registration_receipt.json',
 'Hodram_manuscript':'translations/hodram_B137_B45_B46_editorial_manuscript_v2.json',
 'Hodram_view':'work/analysis/Hodram_B137_B45_B46_native_review_v8247/28_native_pages_directly_viewed_two_exact_boundary_reviews.json',
 'remaining_estimate':'work/analysis/editorial_remaining_estimate_v8264/rough_candidate_estimate_not_full_goal_denominator.json',
}
SUMMARY="""Gerhard Adernkatz consistency is integrated in registered experimental cumulative V8259 after the complete V8172 stack. Candidate out/all_routes_combined_v8259_candidate.nds SHA256 a3f11bad910fd7ffa2ba87fc85d82caeb5025b1863da7a2a1405725ff94ec42f; clean-input patch SHA256609030a09f4569570e5e797bb6755c3a0d34e8dcfcbbf6bdcf2a3f9241731364. All640 manifest batches/114accepted layers/18release checks/110regressions pass. The whole ROM equals pinned approved research8215 and reconstructs exactly from clean f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d. Canonical3cb827e4 remains unchanged; mainV4701 unchanged. No separate unified test package, promotion, pruning, commit or push. All generated ROMs and earlier translations/proofs/failures remain.

Only the owned12-byte ARM9 surname and five previously completed SC2B27/B74 speeches change. Blades8, pointer fields and every other ARM9 byte remain exact. All20 final Latin occurrences use Adernkatz;14 previously consistent consumers remain. Sparse independent reconstruction preserves225commands/130preambles/44relatives/125unowned speeches/334otherSC2blocks, the prior reviewed typed choice, complete terminals/tails and full predecessor block/archive/ROM inverses. The full295-speech clean-name context and individual retentions justify the spelling; no officialLatin-canon, new rank, biography or relationship is claimed. The five old records retain their revised-and-integrated classification. Their latest current wording/references now point to V8259, with full prior record snapshots and reversible operations retained. Zero duplicate source/prose/completed/revised/retained credit:7171completed/7174credited source-prose-and-drafts/4455integrated revisions/2716retentions;SC0368,SC191,SC24915,SC3197,COMMON1600complete/1603source-prose,route subset5571.

Frozen policy8236/260actual-changing expected rejections8237 and independent reference seal8238 pass. Production v2 independently reconstructs native source/current/final refs, complete font/body/name masks, source-qualified final dispatch/query/terminal controls, actual command/RNG/UI/timing associations, all117scene and598laterRGB comparisons, final native components and eight focused RAM phases. Its positive test commits exactly one final complete NDS object only after both ARM9 andSC2 pass; the original NDS object stays byte-exact. All107 independent actual-changing proof-corruption cases reject before any commit, with dependency digests deliberately bypassed and trusted frozen/native guards preserved. All source/config/proof/ROM/registry/ledger/pin inputs remained exact through the challenge suite. Earlier passing productionv1 and all failures remain preserved.

Fresh own registered Lil NewGame8261 runs4001frames with ordinary original inputs, no battery/savestate/runtime overlay or optional-event forcing. Strict target ARM9 full12-byte inverse/Blades/COMMON/directory/123264deployed-pool/current-instruction/actor/4MiB guards pass. Six whole startup PNG pairs and wholeactors match V8172; selection/opening sheet directly viewed. Eight fresh progressive/full getters retain Hodram/Joakim/Lil/Camille/Marinus and show Gerhard Adernkatz. This captain2 input is current_V8259_Lil_native_v8262. It is not a Hodram captain1 input, catalogue-UI/custom-name test or natural optional scene visit. Earlier Rafael8175/Hodram8187 inputs remain historical to V8172 until independently rebound or recaptured for new work.

All previously measured actual surname limits remain. Full initialized B27 selects35of51 speeches and later enters SC0B44/captain0, not normal Lil continuity or natural Stockholm activation. FullB74 selects75of79, including all3corrected bodies and original menu option0; option1/fourother speeches unvisited. Focused B27 intro displays8original speeches covering the2other corrected bodies while bypassing the original outer condition/remaining effects. Eight scene runs total176008frames/30complete bodyholds/262nameholds. This turn adds only the4001-frame registered startup. Command/duration differences1/0,74/19,8/2;117scene/portrait pairs match. Later RGB328/164/106 with0/0/29differences; intro final models/persistent/actors/RNG differ. First7sampled component sets match;12000diff2fleet/150actor/54town bytes and rawcalendar535/[0,11,7] versus534/[0,11,6], converging atfinal12001. Rawdates uninterpreted; no every-frame causal, future-outcome, broad simulation, hardware, all-branch or fullroute claim. Keep all limits for the later older-record technical re-audit.

Hodram SC1B137/B45/B46 remain28pending contextual drafts:16proposed revisions/12individually justified retentions, not completion credit. Clean source/27prior B44 callbacks, exact current/effective mapping,56dispatches, manuscriptv2,112logical alignment bindings,112fresh compiled alignments and28viewed complete native body pages remain verified. Preserve Camille's hesitant apology, Charles's bluntness, Hodram's restraint, Gerhard's maritime-trade/capable-people/possible recruitment advice, Lil's reported regional wealth/serious treasure contest and Hodram's map-key confusion. Duel/reveals a map errors are corrected; no new kinship/rank/romance/recruit guarantee/map gift/accepted or won contest. Three silences retained. Two exact ordinary boundary reviews and five infos remain; global width/fonts/guards/QA are unchanged and all28 formatting gates remain false. Stored SC1/control/nameheader/actual4800-layout0-hide4700/policy/atomic/registered integration remain pending. The required Adernkatz asset dependency is now registered in V8259.

Full goal remains active across all four storylines, earlier translations, shared shops/towns/random scenes, Help/remaining prose, all207 names/roles/aliases and retrospective early wraps. The requested planning estimate is about20000 lexical text candidates still to classify/review in the five main text files, not an exact player-facing remaining count or fullgoal denominator; Help/names/otherfiles/revisits add separate work. All previous unfinished families and leads remain in the copied scope inventory. Graphics/all18 plaques and later older-record technical re-audit remain separate.
"""
NEXT="""Continue from verifiedV8266/current registeredV8259. Do not repeat the completed Gerhard native/actual/policy/atomic/cumulative/clean-patch/startup checks without a new change or concrete risk. The Gerhard correction is a registered dependency, with zero duplicate credit, not pending policy or integration. Preserve mainV4701 and all prior artifacts.

Return to Hodram28 from manuscriptv2, plan8245, native bodies8246/view8247, source controls8188,4800 Red Dye/layout0 proof8190b, paths8191 and six-name reviewv2. Reconstruct stored SC1B137/B45/B46 after the entire V8259 stack, preserving all60commands/eight relatives/two raw8000 operands/full terminals/tails. Validate stored parity/fullglyphs and every source-qualified map. Obtain an own V8259 captain1 context with full targetARM9 inverse/Blades/COMMON/directory/123264pool/actor/current-instruction guards; never borrow the captain2 input. Rebind unchanged body proofs by exact code/font/source hashes where appropriate; do not pretend the old2b6 complete ARM9 hash is current. Review six complete nameplanes and representative actual headers, source silences, distinct4800/layout0 andhide4700 behavior, transitions and normal returns with disclosed fixtures, preserving all original branch/effect bytes and no forced runtime state. Complete per-record formatting, frozen source/prose/layout contract, independent atomic guards, registered cumulative integration and exact clean patch before once-only completion credit. The current stored SC1 bytes are identical to the prior map, but native scene/header context remains pending.

Keep all four routes, shared shop/town/random/Help/remaining prose, all207 names/role/alias consumers and retrospective premature-wrap leads. Retain COMMON750-752,12contraction/question-tag leads, unscanned beyond558plans, weak-before-row/page-before-readability concerns, source-specific typography and all item/counterpart/name leads from the previous inventory. Preserve graphics and the later technical audit, including normal endcarry, B35R65/B48R129 source19thcells, stale B48/B50 labels, corrected B47 receipt, timing/RNG/component/byte/calendar/RGB and fixture-reentry limits. No separate unified test package, promotion, pruning, commit or push.
"""

def restore(value):
    result=deepcopy(value);operations=deepcopy(result[KEY]['inverse_operations'])
    for op in reversed(operations):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result

def gates():
    prior=read(PRIOR);data={k:read(p) for k,p in PROOFS.items()};doc=read(DOC);validate_approved_batch(doc)
    release,view=data['release'],data['startup_view'];image=NdsImage.open(release['candidate'])
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256'] and release['whole_clean_input_ROM_reconstruction_byte_exact']
    assert sha(Path(release['exact_patch_reconstruction']).read_bytes())==release['candidate_sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert release['manifest_batches']==640 and release['accepted_layers']==114 and release['all18_registered_release_checks_pass'] and release['all110_release_dialogue_regressions_pass']
    assert read(release['manifest'])['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    validate_runtime(image,'target')
    assert view['viewed'] and view['fresh_ordinary_registered_coldboot_frames']==4001 and len(view['six_whole_RGB_pairs'])==6
    assert len(view['native_eight_getters_from_actual_own_registered_snapshot']['rows'])==8 and view['target_family_bytes_andprotected_Blades_measured_inactual_coldboot_RAM']
    assert data['startup']['registered_candidate'] and data['startup']['candidate_sha256']==release['candidate_sha256'] and data['startup']['all_strict_targetARM9_inverse_COMMON_directory_and123264_payload_guards_pass']
    assert data['own_Lil_input']['current_ROM_sha256']==release['candidate_sha256'] and data['own_Lil_input']['expected_original_captain_ID']==2
    assert data['atomic_positive']['single_complete_NDS_commit'] and data['atomic_negatives']['negative_count']==107 and all(c['rejected'] and c['commit_calls']==0 for c in data['atomic_negatives']['cases'])
    assert data['policy_tests']['negative_count']==260 and data['reference_seal']['independent_reconstruction_byte_equal_reference']
    h=data['Hodram_manuscript'];assert len(h['records'])==28 and h['revised']==16 and h['retained']==12 and all(not r['review']['formatting'] for r in h['records'])
    assert data['Hodram_view']['all28_complete_bodies_visually_read'] and len(data['Hodram_view']['original_warnings'])==2 and len(data['Hodram_view']['original_infos'])==5
    assert data['remaining_estimate']['exact_player_facing_remaining_count_not_established']
    return prior,data,doc

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,data,doc=gates();release=data['release']
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==AFTER and OLD_KEY in old and KEY not in old and SCOPE not in old
        new=deepcopy(old);ops=[];overlays=[]
        def put(path,value):
            parent,key=parent_at(new,path);exists=key in parent;ops.append(dict(path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
        for row in doc['records']:
            found=[(fi,ri,r) for fi,f in enumerate(old['completed_editorial_families']) for ri,r in enumerate(f['records']) if r.get('file_path',f.get('file_path'))==row['file_path'] and r['id']==row['id']]
            assert len(found)==1;fi,ri,record=found[0];assert record['decision']=='revised-and-integrated' and record['source_hex']==row['source_hex']
            target=row['integrated_reference_pending'];raw=bytes.fromhex(row['final_stored_hex']);body=raw[1:].decode('cp932')
            overlay=dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_reference=row['source_reference'],predecessor_reference=row['current_reference'],integrated_reference=target,
                source_hex=row['source_hex'],previous_stored_hex=row['current_hex'],integrated_stored_hex=row['final_stored_hex'],logical_English=row['english'],
                reason=row['localization_note'],review=row['review'],candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
                source_context_manuscript=str(DOC),source_context_manuscript_sha256=sha(DOC.read_bytes()),actual_display_observations=row['actual_display_observations'],
                previous_credited_record_preserved=deepcopy(record),previous_classification_retained='revised-and-integrated',new_completion_revision_retention_credit=0)
            base=['completed_editorial_families',fi,'records',ri]
            put(base+['latest_integrated_editorial_overlay_v8265'],overlay)
            for field,value in dict(english=row['english'],current_English=' '.join(body.split()),current_stored_English=body,current_reference=target,current_text_hex=row['final_stored_hex'],
                compiled_hex=row['compiled_hex'],completed_candidate_reference=target,completed_candidate_sha256=release['candidate_sha256'],speaker=row['speaker']).items():put(base+[field],value)
            if 'current_native_macro_English' in record:put(base+['current_native_macro_English'],body.replace('FI','Lil').replace('FA','Argot').replace('FO','Argot Co.'))
            if 'current_native_macro_output_hex' in record:put(base+['current_native_macro_output_hex'],raw[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.').hex())
            overlays.append({k:v for k,v in overlay.items() if k!='previous_credited_record_preserved'})
        current=deepcopy(old['current_integrated_candidate']);current.update(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],
            MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
            status='experimental-registered-exact-clean-patch-own-startup-verified',details=SUMMARY,full_goal_complete=False,
            **{f'SC{r}_sha256':release['story_hashes'][f'SC{r}'] for r in range(4)})
        put(['current_integrated_candidate'],current)
        oldscope=old[prior['unfinished_scope']];assert sha(Path(oldscope['path']).read_bytes())==oldscope['sha256'];inventory=deepcopy(read(oldscope['path']))
        pending=dict(status='Gerhard-registered-overlay-complete-Hodram28-contextual-native-body-drafts-pending-stored-names-actual-policy-release',
            all_proofs=PROOFS,Gerhard_owned_name_record=doc['name_records'][0],Gerhard_five_prior_revised_records=overlays,Gerhard_registered_asset_dependency_fulfilled=True,
            Gerhard_frozen_policy_andatomic_registered_cleanpatch_startup_complete=True,Gerhard_new_duplicate_credit=0,
            Hodram_objects=28,Hodram_proposed_revisions=16,Hodram_proposed_retentions=12,Hodram_native_body_pages=28,Hodram_all_formatting_gates_false=True,
            Hodram_new_actual_scene_runs=0,Hodram_own_current_V8259_captain1_context_pending=True,own_current_V8259_captain2_input=PROOFS['own_Lil_input'],
            full_goal_all_prior_unfinished_families_andlimits_preserved=True,new_credit=0,new_emulator_runs=1,new_actual_frames=4001,full_goal_complete=False)
        inventory[KEY]=deepcopy(pending);inventory['next_focus']=NEXT;inventory[OLD_KEY]['superseded_by']=dict(checkpoint=KEY,Gerhard_frozen_policy_atomic_registered_release_now_complete=True,Hodram_stored_names_actual_policy_registered_still_pending=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,full_goal_complete=False))
        put([OLD_KEY,'superseded_by'],inventory[OLD_KEY]['superseded_by']);put(['latest_checkpoint'],SUMMARY+'\n'+NEXT)
        ops.append(dict(path=[KEY],existed=False,before=None))
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,DOC,Path(__file__),*map(Path,PROOFS.values())]}
        new[KEY]=dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=deepcopy(ops),goal_turn_classification='progress',all_sessions_terminal_andreaped=True)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and len(new['completed_editorial_families'])==len(old['completed_editorial_families'])
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V8265: Gerhard Adernkatz registered in V8259; Hodram28 contextual drafts continue\n\n'+SUMMARY+'\n'+NEXT+'\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V8265; V8259 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,unchanged_counters=list(AFTER),previous_record_snapshots_andcomplete_deep_inverse_preserved=True,new_credit=0,full_goal_complete=False))
        print('V8265 registered-name overlay staged;5old revision snapshots retained/six targets/zero duplicatecredit;deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256'] and sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),every_prior_ledger_value_andfive_old_record_snapshots_recover_exactly=True,new_credit=0,full_goal_complete=False))
            print('Deep inverse passed:every old ledger value/family/record/count/candidate/unfinished lead recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_prior_values_reversible=True,new_credit=0,full_goal_complete=False))
            print('V8265 applied:registeredcurrentV8259;counts unchanged7171;main4701/fullgoal preserved.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
                ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,
                manifest_batches=640,accepted_layers=114,release_checks=18,regressions=110,strict_own_Lil_current_input=PROOFS['own_Lil_input'],
                previous_strict_Rafael_Hodram_inputs_are_V8172_historical_until_rebound=True,new_credit=0,new_emulator_runs=1,new_actual_frames=4001,new_research_ROMs=0,
                all_sessions_terminal_andreaped=True,all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            verified['Gerhard_surname_correction_checkpoint'].update(registered_correction_complete=True,registered_candidate=release['candidate'],registered_candidate_sha256=release['candidate_sha256'],
                registered_release=PROOFS['release'],fresh_registered_startup=PROOFS['startup_view'],independent_atomic_rejections=107,all_five_record_updates_preserve_previous_snapshots=True,
                independent_atomic_production_semantic_challenges_andregistered_release_pending=False,frozen_policy_atomic_andregistered_release_pending=False,new_duplicate_credit=0)
            verified['Hodram_source_native_checkpoint'].update(surname_registered_asset_pending=False,registered_Adernkatz_dependency_fulfilled_in_V8259=True,
                own_V8259_captain1_input_pending=True,stored_controls_actual4800_hide4700_andregistered_integration_pending=True,all_formatting_gates_false=True)
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8266/currentV8259:640batches/18checks/110regressions/exactcleanpatch/ownstartup;Gerhard overlay complete0credit;Hodram28/fullgoal active.')
