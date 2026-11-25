"""Reversible zero-credit Hodram28 native/stored/actual-display progress checkpoint."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B50_v8184 import COUNTERS,AFTER
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_display_checkpoint_v8285b')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8286b')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8268/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
OLD_KEY='Gerhard_Adernkatz_registered_V8259_Hodram28_pending_stored_names_actual_policy_release_v8267'
KEY='Hodram28_stored_names_actual_display_approved_pending_frozen_policy_atomic_registered_v8285b'
SCOPE='unfinished_editorial_scope_v8285b'
PROOFS={
 'manuscript':'translations/hodram_B137_B45_B46_editorial_manuscript_v4.json',
 'names':'translations/hodram_B137_B45_B46_speaker_name_review_v4.json',
 'display':'work/analysis/Hodram_display_review_v8284/display_review_receipt.json',
 'own_current':'work/analysis/Hodram_current_binding_v8270/own_Hodram_startup_andstrict_captain1_context.json',
 'own_current_input':'work/analysis/current_V8259_Hodram_native_v8270/current_native_input.json',
 'names_native':'work/analysis/Hodram_target_names_v8271/six_current_identities12_getters6_native_nameplanes_own_captain1_context.json',
 'review_rebind':'work/analysis/Hodram_current_review_binding_v8272/current_review_andnative_reuse_receipt.json',
 'relocation':'work/analysis/Hodram_three_block_relocation_v8273/three_blocks28_speeches8_relative_sites40_native_cases_full_inverses.json',
 'stored':'work/analysis/Hodram_three_block_stored_v8274/28_stored_bodies44_fresh68_reused_alignments28_exact_native_pages.json',
 'controls':'work/analysis/Hodram_final_controls_v8275/28_final_dispatches24_controls6_raw_evaluations_original4800_4700_requests.json',
 'reference':'work/analysis/Hodram_reference_v8276/research_image_receipt.json',
 'loaders':'work/analysis/Hodram_loaders_v8277/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
 'callers':'work/analysis/Hodram_reference_census_v8278/all60_commands8_relative_sites28_records_three_EV1_entries_shipped_callers.json',
 'fixtures':'work/analysis/Hodram_scene_fixtures_v8279/six_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json',
 'models':'work/analysis/Hodram_actual_models_v8281b/28_clean_native_bodies28_exact_revised_reuses_six_current_headers.json',
 'comparison':'work/analysis/Hodram_actual_comparison_v8283/three_paired_whole_exchanges_controls_scenes_returns_bounded_later_state.json',
 **{f'actual_B{b}':f'work/analysis/Hodram_actual_v8282/B{b}/paired_actual_dialogue_headers_flow_returns.json' for b in [137,45,46]},
}
SUMMARY="""Registered cumulative V8259 remains current; mainV4701 and the canonical baseline are unchanged. Full editorial goal remains active across all four stories, earlier translated dialogue, shared shops/towns/random scenes, Help, remaining prose, all207 names/roles/aliases and retrospective premature wraps. No separate unified test package, promotion, pruning, commit orpush. Every ROM, translation, draft, executed producer, proof andfailure remains. Counts remain7171completed/7174credited source-prose-and-drafts/4455integrated revisions/2716retentions:SC0368,SC191,SC24915,SC3197,COMMON1600complete1603source-prose,route subset5571. Hodram28 remain outside completion credit until registered integration. The roughly20000 candidate estimate is not an exact player-facing denominator orpercentage.

Hodram SC1B137/B45/B46 now have all five per-record editorial/formatting gates in manuscriptv4:16 proposed revisions/12 individually justified retentions. Whole clean exchanges/27prior B44 callbacks, source facts, voices, logical English, exact source/current refs and all individual reasons are unchanged. Six scoped name retentions in namesv4 now include actual headers;Gerhard Adernkatz is an already registered dependency,not a pending name asset. Historical inconsistent pending fields andsurname findings are explicitly superseded andpreserved. Full207/catalogue/custom-name andwider PortWorker7 review remain open.

Own current V8259 Hodram ordinary NewGame8269 ran4001frames,actualcaptain1,strict target12eb ARM9/full12byte name inverse/Blades8/COMMON/directory/123264payload/actor/4MiB/current-instruction guards. Six whole startup PNG pairs andwholeactors match prior captain1 context;directly viewed. Twelve fresh name getters,six source voices,four synthetic default macro alignments andsix complete style11 nameplanes pass andwere viewed. Defaults6/9/15 remain source-bound;the28 source paragraphs have zero FI/FA/FO. Older exact112 compiled body cases are rebound through complete name-only code/font inverse ratherthan repeated.

Stored reconstruction8273 preserves all60 commands,28complete sixbyte preambles,eight relative sites,two raw8000 operands,opaque effects andcomplete fourbyte ends/tails. B1371240to1384,B4596to84,B46444to480(logical478/tail2). Allthree clean/predecessor blocks andwholeSC1archive invert exactly;322unowned blocks remain exact. Forty fresh native relative cases and75fresh targetseeded endcases pass;not allattainable gameplay paths. Eleven parity-tail records get44fresh alignments;17byte-identical bodies reuse68. All28stored glyphplanes equal viewed one-page bodies. Final28 dispatches,24nonrelative controls,six clean/current/target rawqueries andoriginal4800/layout0/4700 requests pass;normal ends carry the initial value ratherthan assumingzero. Two narrow ordinary weak-boundary waivers andfive infos remain;no global QA/font/width/manual-wrap changes.

Pinned fullreference8276 changes onlySC1B45/B46/B137 after V8259;allother files/components andfullparent inverse pass. ResearchSHA faa113ab70d4dc10b23068c4319eb2e1f8e21b19dc7e391c3323228a0aa65dc8. Native wholeSC1 loader/cache325cases and650initialparentmodes pass. Onefresh shipped-code caller census matches exact priorcode;all60commands/eightrelatives/28records andthree originalEV1 block-index entries are bound. This is controlled native CPU evidence,not natural optional activation.

Six paired clean-Japanese/revised-English whole-exchange ROM fixtures run100006frames with identical ordinary inputs andreadonly original-command traces. OnlyB42 is replaced for each disclosed fixture,after its exact eight original initializers34bytes;everyselected source speech/branch/effect/resource/relative/end remains,with constant34byte shift andfullarchive inverse. No savestate,battery,RAM/eventflag/roster/role/funds/RNG/condition/result forcing orcontroller retiming. These are initialized Hodramopening fixtures,not original optional-event locations,eligibility,earned progress,allattainable effects,fullroute orhardware coverage.

Actual captures show all28 Japanese and28 revised single pages,all six headers andallthree original silences. All262 complete body/name holds match independent native masks,including leading/internal/final characters,bounds andno blank/extra page. All12 actual review sheets were directly viewed. Original4800 shows item181 Red Dye withcomplete icon/name/Mystery Item panel;original4700clears it. Normalreturns: B1378815 [0,0],B454016 [0,0],B465455 [0,1] inbothversions. All28 sameframe upper-scene/portrait/header pairs match. Source/English command differences17/1/5 include native text lengths;duration differences4/0/0 are preserved. UIrequest words match,asdo final five component sets,wholeactors andPRNGperpair,andall532 later wholeRGBpairs. B137 fixture later entersSC0B44/captain0/party0 inbothversions;this isnot normal Hodram route continuity. B45/B46finalcaptain1. No everyframe causal/future-outcome/broad simulation equivalence claim. Keep these limits for the later older-record audit.

Original8281 model producer failed after oneJapanese plane because duplicate metadata keys were assembled;preserved. Source-locked8281b fixes only metadata assembly,keeping native constants/guards/fonts unchanged. Six fixtureROMs andfullreference are pinned;all seven new runs are terminal/reaped. No registered ROM orcompletioncredit change. Graphics/all18plaques andlater older-record technical re-audit stay separate.
"""
NEXT="""Continue from verifiedV8286b/currentregisteredV8259. Do not repeat completed source/prose/native/stored/actual/loader/caller checks without a new change orconcrete risk. Freeze source/prose/layout/actual controls andscopedname approval from manuscriptv4/namesv4/display8284;retain exact two warnings/five infos andallactual scope limits. Implement orderive an independent production reconstruction for onlySC1B137/B45/B46 afterthe full V8259 stack,with explicit registered Gerhard Adernkatz dependency. Validate complete clean/current/target maps,all60commands/eightrelatives/preambles/twoqueries/normalvaluecarry/4800layout0/4700,28complete masks/names/actual holds,source/current/fullROM inverses,325loads650modes andcaller census. Meaningful actual-changing policy andprecommit semantic corruption cases must reject before any mutation,even with dependency digest checks deliberately bypassed;positive commit exactlyone wholeNDS object matching8276reference. Then register cumulative experimental profile,build through sole integrated builder,verify fullreference/exactclean-input patch/appropriate18checks110regressions andown registered startup. Credit28 once onlyafter these gates (projected7199completed/7202sourceprose/4471revised/2728retained;verify first). No separate requestedpackage,promotion,pruning,commit orpush.

Keep the entire four-story/sharedtown-shop/random/Help/remainingprose/207names/retrospectivewrap objective andallprior unfinishedscope leads. Preserve previous Gerhard bounded actual/RNG/calendar/fixture-tail limits,COMMON750-752,12contraction/question-tag leads,unscanned beyond558plans,weak-before-row/page-before-readability concerns,all item/counterpart/name leads,graphics andlater older-record technical re-audit.
"""

def restore(value):
    result=deepcopy(value)
    for op in reversed(value[KEY]['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result

def gates():
    prior=read(PRIOR);data={k:read(p) for k,p in PROOFS.items()};doc=data['manuscript'];display=data['display']
    assert len(doc['records'])==28 and doc['revised']==16 and doc['retained']==12 and all(all(r['review'].values()) for r in doc['records'])
    assert display['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes()) and display['name_review_sha256']==sha(Path(PROOFS['names']).read_bytes())
    assert display['all28_five_per_record_gates_true'] and display['actual_complete_body_andname_holds_both_versions']==262
    for sheet in display['all12_actual_review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    for proof in [display,data['comparison'],data['stored'],data['controls'],data['callers']]:
        for path,digest in proof.get('evidence',{}).items():assert sha(Path(path).read_bytes())==digest
    assert data['own_current']['all_strict_targetARM9_inverse_Blades_COMMON_directory_and123264_payload_guards_pass'] and data['own_current']['actual_original_captain_ID']==1
    assert data['loaders']['fresh_native_whole_loads_andcache_hits']==325 and data['loaders']['fresh_initial_parent_modes']==650 and data['callers']['external_references_complete']
    assert data['reference']['parent_sha256']==prior['candidate_sha256'] and sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    assert sha(Path(data['reference']['research_ROM']).read_bytes())==data['reference']['research_ROM_sha256']
    assert sum(g['actual_frames'] for b in [137,45,46] for g in data[f'actual_B{b}']['groups'])==100006
    return prior,data

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase;prior,data=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==AFTER and OLD_KEY in old and KEY not in old
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);exists=key in parent;ops.append(dict(path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
        scopebefore=old[prior['unfinished_scope']];assert sha(Path(scopebefore['path']).read_bytes())==scopebefore['sha256'];inventory=deepcopy(read(scopebefore['path']))
        pending=dict(status='Hodram28-all-scoped-editorial-formatting-gates-pass-pending-frozen-policy-independent-atomic-registered-integration',
            all_proofs=PROOFS,records=data['manuscript']['records'],name_records=data['names']['records'],
            Hodram_objects=28,Hodram_proposed_revisions=16,Hodram_proposed_retentions=12,Hodram_all_five_scoped_gates_true=True,
            pending28_outside_credited_counters=True,Gerhard_registered_name_dependency_fulfilled=True,
            own_current_V8259_captain1_context_verified=True,all60commands8relatives325loads650modes_reference_census_pass=True,
            native_andactual4800_layout0_hide4700_complete=True,six_paired_scene_runs100006frames_complete=True,
            registered_candidate_unchanged=prior['candidate'],registered_candidate_sha256=prior['candidate_sha256'],
            full_goal_all_previous_unfinished_families_andlimits_preserved=True,new_credit=0,new_emulator_runs=7,new_actual_frames=104007,new_research_ROMs=7,full_goal_complete=False)
        inventory[KEY]=deepcopy(pending);inventory['next_focus']=NEXT
        supersede=dict(checkpoint=KEY,Hodram_native_stored_actual_display_now_approved=True,frozen_policy_atomic_registered_still_pending=True,new_credit=0)
        inventory[OLD_KEY]['superseded_by']=supersede;ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,full_goal_complete=False))
        put([OLD_KEY,'superseded_by'],supersede);put(['latest_checkpoint'],SUMMARY+'\n'+NEXT);ops.append(dict(path=[KEY],existed=False,before=None))
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,Path(__file__),*map(Path,PROOFS.values())]}
        new[KEY]=dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=deepcopy(ops),goal_turn_classification='progress',all_sessions_terminal_andreaped=True)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate']
        assert new['completed_editorial_families']==old['completed_editorial_families']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V8285b: Hodram28 stored/native/actual display approved; frozen policy andregistered integration next\n\n'+SUMMARY+'\n'+NEXT+'\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V8285b; V8259 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,unchanged_counters=list(AFTER),new_credit=0,full_goal_complete=False))
        print('V8285b staged:six targets,zero-credit28 drafts,all old values/counters/candidate/families preserved;deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate']
        assert new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256'] and sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),deep_inverse_recovers_every_previous_ledger_value=True,new_credit=0,full_goal_complete=False))
            print('Deep inverse audit passed:all prior records/roots/counters/candidate/scope recover exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_prior_values_reversible=True,new_credit=0,full_goal_complete=False))
            print('V8285b applied:ROM/registry/counters unchanged;whole objective andallprior evidence preserved.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,new_credit=0,new_emulator_runs=7,new_actual_frames=104007,new_research_ROMs=7,
                all_sessions_terminal_andreaped=True,all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            verified['Hodram_source_native_checkpoint'].update(contextual_draft=PROOFS['manuscript'],contextual_draft_sha256=sha(Path(PROOFS['manuscript']).read_bytes()),
                proposed_revisions=16,individually_justified_retentions=12,all_formatting_gates_false=False,all_five_scoped_review_gates_true=True,
                own_V8259_captain1_input_pending=False,own_V8259_captain1_input=PROOFS['own_current_input'],surname_registered_asset_pending=False,
                stored_controls_actual4800_hide4700_andregistered_integration_pending=False,stored_controls_actual4800_hide4700_complete=True,
                frozen_policy_independent_atomic_andregistered_integration_pending=True,display_review=PROOFS['display'],actual_comparison=PROOFS['comparison'],
                six_whole_exchange_fixture_runs=6,actual_scene_frames=100006,complete_body_name_holds=262,
                original_event_activation_not_observed=True,B137_later_fixture_captain0_not_normal_Hodram_continuity=True)
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8286b/currentV8259:Hodram28source/native/stored/actual-approved;policy/atomic/registered integration next;7171completed/fullgoal active.')
