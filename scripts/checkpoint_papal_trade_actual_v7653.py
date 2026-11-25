"""Checkpoint36 unintegrated prose decisions and exact native proofs without credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_actual_checkpoint_v7653')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7654')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7637/verified_handoff.json')
KEY='papal_trade_SC0_SC1_actual_reference_pending_release_v7653'
SCOPE='unfinished_editorial_scope_v7653'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
VALUES=(6801,6804,6804,4251,2550)
IDENTITY=Path('work/analysis/papal_trade_route_identity_v7624/route_identity_correction_no_ROM_prose_reference_orcredit_change.json')
ROUTES=Path('work/analysis/papal_trade_route_native_v7626/two_own_current_route_contexts_actual_captains0_1_strict2b6.json')
CONSUMERS=Path('work/analysis/papal_trade_consumers_v7627b/two_routes36_effective_bodies72_dispatches_eight_getters.json')
ENTRY=Path('work/analysis/papal_trade_entries_v7628/original_EV0_EV1_events_actions_dependencies_andactual_route_getters.json')
NAMES=Path('translations/papal_trade_speaker_name_review_v2.json')
NAME_FONTS=Path('work/analysis/papal_trade_name_inputs_v7629/two_routes40_fresh_literal_alignments_five_exact_reused_font_planes.json')
CONTROLS=Path('work/analysis/papal_trade_controls_v7630/two_current_blocks50_fresh_seeded_ends_exact_effect_andclean_end_reuse.json')
PROSE=Path('work/analysis/papal_trade_prose_v7631/two_complete_exchanges36_decisions26_revisions10_justified_retentions_display_pending.json')
LOGICAL=Path('work/analysis/papal_trade_logical_inputs_v7633/all36_new_logical_bodies144_fresh_native_literal_IF_alignment_cases.json')
PLAN=Path('work/analysis/papal_trade_layout_v7632b/two_routes36_automatic_full_width_plans_all_base_QA_preserved.json')
NATIVE=Path('work/analysis/papal_trade_native_pages_v7634/two_routes36_complete_pages144_fresh_compiled_alignments_exact_logical_andfont_reuse.json')
VIEW=Path('work/analysis/papal_trade_actual_view_v7652/all72_panes17_sheets_viewed_scoped_names_all_late_limits_preserved.json')
POLICY=Path('work/analysis/papal_trade_policy_validation_v7639/36_positives174_expected_actual_changing_rejections_before_mutation.json')
RELOCATION=Path('work/analysis/papal_trade_relocation_v7640/two_archives36_speeches40_commands_exact_predecessor_inverse_RESEARCH.json')
STORED=Path('work/analysis/papal_trade_stored_v7641/all36_stored_targets144_alignments16_zero_ink_tails36_complete_pages.json')
REFERENCE=Path('work/analysis/papal_trade_reference_v7642/research_image_receipt.json')
LOADER=Path('work/analysis/papal_trade_loaders_v7643/668_whole_native_loads_cache_hits1336_initial_parent_modes.json')
CENSUS=Path('work/analysis/papal_trade_reference_census_v7644/all40_commands_two_block_entries_one_fresh_shipped_caller_census.json')
RELOCATED=Path('work/analysis/papal_trade_relocated_controls_v7645/all36_final_dispatches_two_A000_exact_reuse50_fresh_seeded_ends.json')
INITIALIZERS=Path('work/analysis/papal_trade_initializer_binding_v7647/two_actual_opening_preludes18_commands_bound_before_optional_scene_fixture.json')
FIXTURES=Path('work/analysis/papal_trade_scene_fixtures_v7648/four_complete_source_English_original_route_prelude_fixtures.json')
ACTUAL=Path('work/analysis/papal_trade_actual_v7650/four_complete_scene_captures72_speech_occurrences_exact_body_headers_andnormal_returns.json')
LATER=Path('work/analysis/papal_trade_actual_comparison_v7651b/36_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGBl_limits.json')
EXTRA_PATHS=[POLICY,RELOCATION,STORED,REFERENCE,LOADER,CENSUS,RELOCATED,INITIALIZERS,FIXTURES,ACTUAL,LATER]
SUMMARY="V7611 remains the current registered experimental cumulative ROM, with626 batches,114 accepted layers,18 passing release checks,110 release regressions andits exact clean-input patch. MainV4701 andevery prior ROM,translation,draft,executed producer,failure,trace andproof remain. Counters stay6801 completed,6804 source-prose/drafts,4251 revisions,2550 retentions;SC2 4915 androute5201/5201 are subsets,not the full denominator. The36 Rafael SC0B246/Hodram SC1B237 whole-exchange decisions remain uncredited until registered integration:26 revisions and10 individually justified retentions atR5/R12/R29/R47/R60 perroute. Correct SC0 Rafael/SC1 Hodram/SC2 Lil/SC3 Maria identity andthe explicit historical SC1-Maria metadata correction remain. The full clean-Japanese American-English objective is active.\n\nThe exact36 source/current/gloss/English references, actual-captain0/1 strict2b6 contexts,72 source/current dispatches,eight name getters,masks1/2,EV0 event246/action247 andEV1 event237/action238 bindings remain. Clean full1468-byte Japanese blocks are identical to completed LilB234,so the earlier18 glosses were bound before current English andexplicitly reused,not freshly authored orderived from English. Stored This man andHodram's full-width F were native-processor-confirmed wording issues. All source facts,qualifiers,cultural religious context,familiar Carlo/Filippo banter,unspecified tentative recovery,aboard-ship fact,explicit merchant great-grandfather,papal direct rule almost toVenice,donations,ancestral profits/decline/envy,reported occasional finds,prospective blessings,divine-aid echo andconditional discovery remain. No invented kinship,rank,nationality,recovery cause,current city/date,modern history,shipping route,authenticity,precise site orguaranteed effect/reward is introduced. Item106 andall shared name/item assets remain unchanged.\n\nV7638 freezes exact36 paragraphs with separate Raphael/Hodram guarded profiles,file-qualified block/runtime locks,all baseQA,two exactR33 line1 article-the boundaries keeping Papal States whole,and16 individual row-count reasons. V7639 passes36 positives and174 actual-changing expected ValueError guard rejections before ROM/registry/ledger mutation;this frozen-text guard isnot a semantic oracle for unseen prose. The unchanged global F/I,font,macro,viewport,pair-phase andweak-ending policies remain. Prior144 fresh logical and144 fresh compiled alignments,18 distinct native pages(six fresh/12 exact reuse),all36 one-page paragraphs andthree viewed native sheets remain;no replay was needed.\n\nV7640 reconstructs both full predecessor blocks andarchives exactly. Each source1468/logical1468/tail0 becomes target1508/logical1506/tail2. Eight zero-ink parity spaces perroute preserve16 final stored strings' phase;all36 stored targets pass144 alignment cases(64 fresh/80 exact route-specific reuse),with eight distinct stored-font renders andsecond-route exact reuse. All40 commands,36 complete preambles including printable0x68,A0001456->1494/raw00a0ffff6a000110 andfour-byte end1464->1502 remain;the separate two-byte storage tail isnot an end command. Source-owned archives change onlyB246 in343-block SC0 andB237 in325-block SC1. A pinned reversible V7642 research reference changes onlythose two files from completeV7611;342 SC0 and324 SC1 other blocks andallother files/components remain exact. It isnot a registered release,test package,handoff ornew parent.\n\nV7643 passes668 fresh whole-archive loads/cache hits and1336 original initial parent modes,with only original SDK I/O bridges. EV0/EV1 select whole blocks byindex andboth parent modes begin atpayload+8. V7644 binds all40 clean/current/target commands andone fresh shipped caller census;decoded native units support exact prior census reuse. V7645 passes36 final actor/body/voice dispatches and50 fresh relocated seeded normal ends;the unchanged isolated A000 bytes andwhole ARM9 support exact effect-proof reuse,not full item/blessing/ownership/reward semantics.\n\nFresh ordinary V7611 New Games with read-only command observation bind Rafael's originalB44 ten-command prelude(firstspeech40/frame3256) andHodram's originalB42 eight-command prelude(firstspeech42/frame2816). All18 original initializer entry/return pairs,operands,extents andwhole resident bytes match;all callbacks preserve CPU/RAM/configuration andrestore host slots. These extra traces answer the previously missing initializer question;earlier no-observer route/captain captures are preserved. Both jobs are terminal/reaped. No optional encounter was activated.\n\nFour pinned source/English ROM fixtures append the complete20-command18-speech exchanges behind each actually observed original opening prelude. All original speech commands,opaque effect andnormal end are retained;only the disclosed opening block isreplaced ineach fixture,not runtimecode/RAM/roles/roster/funds/RNG/conditions/results. Each route's Japanese/English runs useidentical ordinary NewGame andA4000..15500/240 inputs for16001 frames. All four are terminal/reaped. Each observes18 complete one-page speeches: Rafael63 complete body63 headers ineach language/30 commands;Hodram70 body70 headers ineach language/28 commands. There arezero incomplete sampled holds orunknown trace sources. All original command results/UI words agree. Source/English exits8095/8094 forboth routes,normal return[0,0],townsample8170. Source/English scene/portrait/header upperRGB pairs agree for all36 speeches. R5's allthree CP932 ellipses have18 black18 light-gray pixels inallfour runs,with no mistaken ASCII dark-gray shadow.\n\nAll72 source/English speech panes,12 six-speech sheets,four transition sheets andone unmasked return/midpoint/final comparison sheet were individually viewed;every saved enlarged pane equals its whole-frame crop. Four contextual Carlo Sinat/Trader name retentions now have complete actual fixture headers in translations/papal_trade_speaker_name_review_v2.json. The null middle fields andseparate regional European metadata remain;European isexcluded from both getters andisnot a surname orapproved nationality. Filippo remains the explicit spoken alias,not a global actor104 relabel. Full catalogue UI,natural optional activation andthe wider207-name/role/alias review remain open. Incidental Julio,sailing tutorials,Sailor andresource messages earnno editorial credit. Lisbon/Stockholm areinitialized opening backgrounds/returns,not proven original optional event locations.\n\nRetain all19 command-comparison rows andseven duration differences perroute. Of133 later sampled wholeRGB frames,three differ forRafael and53 forHodram. Rafael's five queried components andwhole actors agree,with both final seeds2470616159. Hodram's state/tasks/calendar agree,butmodels/persistent_objects andwhole actors differ;final seeds3950740296/3249748893. Raw calendars receive no invented date interpretation. Final16001 showsRafael Sea View andHodram Sailor Water has run out;the late differences remain explicitly preserved. No fullRAM,everyframe,futuresequence,broadsimulation orcomplete causal-equivalence claim ismade. Keep these measurements for the later older-record technical re-audit. The initial V7651 comparison stopped before output onan incorrect expected final frame16000;source-locked7651b includes both requested16000 andautomatic16001. No replay,retiming orcapture change occurred,andthe failed producer ispreserved,not counted as a rejection.\n\nFull registered integration ispending: seal final manuscripts/native/external-reference maps,prepare source-owned atomic production support andfocused actual-changing challenges,register the complete cumulative profile,build withthe registered builder,verify exact clean-input reconstruction andall release regressions,then own-ROM startup/native controls before granting36 decisions once. The canceled separate unified test package stays canceled. No promotion,pruning,commit orpush occurs. Preserve the full four-storyline,earlier dialogue,shared shop/town,random,Help,remaining prose,207 names/roles/aliases andretrospective premature-wrap objective,all completed history andunresolved leads. Graphics/all18 plaques andthe later older-record technical re-audit stay separate."
NEXT="Continue from the complete policy/stored/reference/actual andvisual proofs;do not replay unchanged source/gloss extraction,route contexts,consumers,getters,EV entries,native fonts,stored alignments,loader/caller checks,initializers orfour scene captures. Current remainsV7611. Use actual-captain0/1 strict route inputs at work/analysis/papal_trade_route_native_v7626/route0/current_native_input.json androute1/current_native_input.json,never Lil's captain2 input. Seal exact36 five-gate manuscripts andfile-qualified relocation maps with all source/current/compiled/stored references;bind the actual-view/name successor andall late differences. Prepare source-owned atomic two-archive production support that revalidates every paragraph,source block,full inverse,command,preamble,opaque operand,normal end,separate storage tail,name/item field anddependency before one final write. Challenge actual-changing corruptions before mutation,includingboth route qualifications andtarget1508/logical1506/tail2. Register the whole cumulative stack andbuild through scripts/build_integrated_release.py;prove byte equality to the pinned research reference,exact clean-input xdelta reconstruction andall required release checks. Then verify own-current startup/native inputs andgrant26 integrated revisions/10 justified retentions once. Preserve the entire broad objective andevery prior artifact. Keep the measured3/133 and53/133 lateRGB differences,models/actors/RNG limits,failed7651 final-frame assertion,all prior failures andlater technical re-audit. No canceled package,promotion,pruning,commit orpush."

def restore(value):
    out=deepcopy(value);entry=out.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(out,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return out

def gates():
    ledger=read(LEDGER);prior=read(PRIOR);prose,native,view=map(read,[PROSE,NATIVE,VIEW])
    assert tuple(ledger[k] for k in COUNTERS)==VALUES and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    candidate=ledger['current_integrated_candidate'];manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert candidate['sha256']==prior['candidate_sha256']==sha(Path(candidate['path']).read_bytes()) and candidate['profile']=='all-routes-unified-v7611'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(manifest['batches'])==626 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert prose['total_source_current_references']==len(prose['records'])==36 and prose['revised']==26 and prose['retained']==10
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in prose['records'])
    for m in prose['manuscripts']:assert sha(Path(m['path']).read_bytes())==m['sha256']
    assert native['fresh_compiled_alignment_cases']==144 and native['exact_reused_logical_alignment_cases']==144 and view['all72_complete_source_English_speech_panes_individually_viewed']
    assert read(CONSUMERS)['actual_original_captain_IDs']==[0,1] and read(IDENTITY)['correct_route_names']=={'SC0':'Rafael','SC1':'Hodram','SC2':'Lil','SC3':'Maria'}
    assert read(POLICY)['negative_count']==174 and read(STORED)['fresh_alignment_cases']==64 and read(LOADER)['fresh_initial_parent_modes']==1336 and read(ACTUAL)['total_actual_speech_occurrences']==72 and view['later_RGB_differences_by_route']==[3,53]
    return prior,prose

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase;prior,prose=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256'];new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
            ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        scope=old['unfinished_editorial_scope_v7636'];assert sha(Path(scope['path']).read_bytes())==scope['sha256'];inventory=deepcopy(read(scope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(route_identity_correction=str(IDENTITY),prose_decisions=str(PROSE),native_review=str(VIEW),manuscripts=prose['manuscripts'],file_qualified_positions=36,proposed_revisions=26,proposed_retentions=10,source_prose_or_completion_credit_added=0,stored_actual_policy_reference_complete_atomic_release_pending=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
        ROOT.mkdir(parents=True);inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
        put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),all_broader_objective_andprior_leads_preserved=True,SC0_Rafael_B246_SC1_Hodram_B237_36_prose_decisions_native_reviewed_uncredited=True,full_goal_complete=False))
        put(['formatting_watchlist','papal_trade_SC0_SC1_v7653'],dict(status='prose-policy-stored-reference-actual-reviewed-atomic-release-pending',native_review=str(VIEW),exact_R33_article_boundary_each_file_no_global_rule_change=True,all_formatting_gates_false=True,no_new_credit=True))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
        assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5201;put(['coverage_units',ri,'next'],NEXT)
        paths=[IDENTITY,ROUTES,CONSUMERS,ENTRY,NAMES,NAME_FONTS,CONTROLS,PROSE,LOGICAL,PLAN,NATIVE,VIEW,*EXTRA_PATHS,PRIOR,inv,Path('translations/release_stack.json'),Path(__file__)]
        evidence={str(p):sha(p.read_bytes()) for p in paths}
        new[KEY]=dict(records=deepcopy(prose['records']),file_qualified_source_current_refs=36,proposed_revisions=26,proposed_retentions=10,reviewed_names=str(NAMES),native_review=str(VIEW),source_prose_or_completion_credit_added=0,new_source_prose_reviews=0,new_completed_records=0,new_revisions=0,new_retentions=0,current_ROM_families_all_five_credit_counters_andprior_records_unchanged=True,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['completed_editorial_families']==old['completed_editorial_families']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V7653: Rafael B246 / Hodram B237 stored and actual research complete; registered integration pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            p=Path('docs')/name;prefix=('# Current editorial handoff - V7653; V7611 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[p]=prefix.replace('\n','\r\n').encode()+p.read_bytes()
        files=[]
        for i,(p,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if p!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0))
            files.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,zero_credit=True,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six-target36-decision stored/actual checkpoint staged; zero credit, V7611/families/counters unchanged.')
    else:
        staged=ROOT/'staged_checkpoint.json';plan=read(staged);old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==VALUES
        for e in plan['files']:
            assert sha(Path(e['planned']).read_bytes())==e['planned_sha256']
            assert sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha(staged.read_bytes()),all_prior_roots_records_families_counters_andROM_refs_recover_exactly=True,zero_credit=True,full_goal_complete=False))
            print('Deep inverse audit passes: every prior root, record, family, counter and ROM reference recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha(staged.read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,no_ROM_orcredit_counter_change=True,full_goal_complete=False))
            print('Six audited checkpoint targets applied; 36 uncredited decisions, unchanged V7611.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),all_prior_roots_records_families_counters_andROM_refs_recover_exactly=True,correct_SC0_Rafael_SC1_Hodram_route_identity=True,SC0B246_SC1B237_36_uncredited_prose_decisions26_revisions10_retentions=True,own_route_captain0_1_strict_native_contexts_bound=True,new36_logical_andcompiled_native_alignments288=True,all18_distinct_native_pages_viewed_six_fresh12_exact_reuse=True,stored_actual_policy_reference_complete_registered_integration_pending=True,actual72_speech_occurrences_all17_sheets_viewed=True,late_RGB_differences_by_route=[3,53],all_late_components_actors_RNG_andframe_limits_preserved=True,all_new_formatting_gates_false=True,new_credit=0,pending_checkpoint=str(ROOT/'application_receipt.json'),full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            verified['historical_V7622_pending_consumers_flag_superseded']=verified.pop('current_raw_wording_findings_effective_runtime_prose_entry_names_native_actual_release_pending',None)
            save(VERIFY/'verified_handoff.json',verified)
            print('V7653 verified:36 policy/stored/reference/actual decisions pending registered integration; V7611/6801 completed unchanged. Full goal active.')
