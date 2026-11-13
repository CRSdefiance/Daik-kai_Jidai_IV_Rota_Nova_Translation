"""Checkpoint source/name/cultural review and bounded research without credit or release drift."""
import argparse,gzip,json,os
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.checkpoint_lil_B204_clean_v6060 import immutable_checks as old_immutable_checks
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_names_culture_checkpoint_v6090')
VERIFY=Path('work/analysis/editorial_handoff_verification_v6091')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v6061/verified_handoff.json')
KEY='Lil_B204_source_names_cultural_review_v6090'
SCOPE='unfinished_editorial_scope_v6090'
FINDINGS=Path('work/analysis/lil_B204_contextual_findings_v6088/twenty_source_current_findings_eight_proposed_retentions_twelve_revisions.json')
CULTURE=Path('work/analysis/shachihoko_source_context_v6075/four_complete_clean_exchanges_and_two_nonitem_sobriquet_contexts.json')
DESCRIPTION=Path('work/analysis/shachihoko_description_v6085/clean_description_neighbor_context_current_COMMON_and_staged_copy_lead.json')
GETTERS=Path('work/analysis/shachihoko_item_consumers_v6081b/all218_item_getters_two_original_callers_and_complete_native_title_plane.json')
ACTUAL=Path('work/analysis/shachihoko_B204_card_actual_v6084c/complete_source_path_and_unmasked_title_acquisition_prompt_frame_differences.json')
GLYPHS=Path('work/analysis/shachihoko_actual_name_glyphs_v6086/four_native_planes_and_all_actual_title_notice_holds_match.json')
VIEW=Path('work/analysis/shachihoko_actual_review_v6087/viewed_actual_title_acquisition_notice_and_measured_scope.json')
SOURCEVIEW=Path('work/analysis/lil_B204_source_view_v6077/complete_source_scenes_and_return_visual_review.json')
RESEARCH=Path('work/analysis/shachihoko_item_name_research_v6079/research_image_receipt.json')
EVIDENCE=[FINDINGS,CULTURE,DESCRIPTION,GETTERS,ACTUAL,GLYPHS,VIEW,SOURCEVIEW,RESEARCH,
    Path('work/analysis/lil_B204_source_v6062/all20_clean_current_complete_context.json'),
    Path('work/analysis/lil_B204_source_names_v6065/five_exact_source_name_fields_voices_and_distinct_name_consumers.json'),
    Path('work/analysis/lil_B204_dispatches_v6066/all20_source_current_dispatches_four_FE_letters_no_macros_and6_control_leaves.json'),
    Path('work/analysis/lil_B204_entry_v6067/source_EV2_B204_action_dependency_and_native_getter_binding.json'),
    Path('work/analysis/lil_B204_branches_v6068/original_relative_skip_operand_proof.json'),
    Path('work/analysis/lil_B204_controls_v6069/six_exact_leaves_picture47xx_two43xx_one_A000_structural_pairs_and_guarded_end.json'),
    Path('work/analysis/lil_B204_source_fixture_v6070/complete_B204_source_B22_fixture.json'),
    Path('work/analysis/shachihoko_B204_card_fixture_v6082/complete_B204_source_B22_fixture_with_provisional_item_name.json'),
    Path('work/analysis/shachihoko_current_context_v6078/four_complete_source_current_exchanges_and_raw_Orca_candidates.json'),
    Path('work/analysis/shachihoko_consumer_correction_v6081b/explicit_source_proven_native_root_correction.json'),
    Path('dk4tool/patch/shachihoko_item_name_data_v1.py')]
DETAILS='''V6090 advances Lil B204 through complete clean-source gameplay,exact source names/roles/native controls and individual source/current findings. Source1312 bytes/26 commands/20 objects remains16 progressive speeches/four FE letter parts,with no macros,predicates,relative sites,choices or authored target prose. Five exact source actors/voices and ten distinct progressive/catalogue consumers support Lil Argot,Jam Ludwyan versus full Jam Jack Ludwyan,Guard,Daimyo and Innkeeper. Retain these supported names/roles in context;do not invent an aunt,royalty,new rank,nationality from unused metadata,or a family relationship. The initial Man/Woman/Stranger revisions already integrated in V5891 remain present;all207 proper names/roles/aliases and their retrospective consumers remain in scope. These contextual label retentions add no duplicate name/dialogue credit.

The complete Japanese B22 content fixture observes all20 objects/all35 commands,including nine original initializers,and all four FE letter parts/full signature. Nine source/context/return sheets were viewed. Source ends7894,then actually shows port UI/resupply/menu and later SC2B120 from9101;do not assume a B43 tutorial or an idle-town final endpoint. Exact40 dispatches,five static/eight null-actor FE cases,six command leaves,entry204/action205,picture116 descriptor[0,116,1,5]/layout[3,1,1] and guarded ends are preserved with their bounded native/structural scopes. Native resource/effect bodies,outer eligibility,earned inventory,original location,full route and hardware are not inferred from these proofs.

The all1307-block clean census finds four complete20-object castle variants at SC0B216/SC1B208/SC2B204/SC3B177. All80 source speeches were contextualized before current English comparison;retain each protagonist\'s distinct response. Two separate complete Maria sobriquet contexts SC3B28/B105 use 翔緋鯱 and are not item-name replacement targets. Jam\'s claimed thank-you gift,his presumptuous letter taking one spare,and the daimyo\'s explicit thief accusation remain in tension. The letter\'s ship/castle explanation stays an unreliable character claim. B204 now has20 exact-source/current findings:eight individually justified proposed word retentions/twelve revisions. Restore natural castle recognition,origin questions,boast/apparent judgment,panic,morning rather than unproved dawn,foreign writing,find rather than an invented arrest,and the salutation/sign-off/signature roles. Target English prose/native wrapping and final decisions remain pending;no new source/prose/completion credit is added.

Clean item116 鯱の像,spoken シャチホコ and the upturned ornament image expose a shared cultural-term lead. Shachihoko is a provisional title replacing Orca Figurehead in pinned data-only research. Original title storage/pointer ownership,all218 item rows/621 actor-name fields/aliases,and the exact11-byte-prefix inverse are bound. All other files/components,code/fonts/graphics/pointers/allocations and123040 staged bytes plus48-byte copy wrapper remain exact.218 parent+218 target original virtual/static getters and436+436 original virtual callers pass;only item116 changes. A fresh4001-frame research New Game supplies its own current snapshot;no historical initialized RAM overlay. A separate13001-frame unchanged-Japanese content run shows the new card and generated acquisition notice. Four complete native/independent glyph planes match20 title holds and four notice holds per version,including first/final/interior glyphs. The title uses original minus-one tracking;the notice uses zero tracking. The six-panel paired sheet was viewed. This notice is not a21st stored speech or new generic-notice editorial approval.

Measure the differences honestly:182 paired whole frames include128 exactly equal frames,20 title-difference frames,four acquisition-text frames and30 advance-prompt frames. All63 completed SC paths/results/decoded lengths agree;46 pairs have timing or interval-RNG differences. Parent/target scene ends are7894/7895. Complete duration differences and all frame differences are preserved;no masking,retiming,full-RAM/future-random or complete timing-cause claim. The initialized-Amsterdam fixture is not natural event204 activation or original location. All three jobs are terminal/reaped:this goal turn has three cold boots30003 frames,including the earlier source run,and three pinned research ROMs. No prior artifact is pruned.

The literal census also finds COMMON2931 and a staged literal copy. Its independent clean description says シャチ,describes the threatening upturned pose,and reports a storm-avoidance legend. Preserve that source distinction;do not pretend it literally says シャチホコ or that orca was an impossible dictionary reading. Seven clean neighbor descriptions and exact source/current/staged references are saved. A coordinated title/description decision must bind the active COMMON and staged consumers,format native output and pass representative/registered checks before integration. The title-only research is not a release parent. The original item-name/description batches,failed probes,corrected successors and all proof history stay preserved.

Experimental cumulative V6050 and its exact clean-input patch remain verified with591 batches/114 accepted/18 checks;main V4701 stays promoted. Coverage remains6349 completed/6352 source-prose/3968 integrated revisions/2381 justified retentions/SC24464/SC396/routes4750/4750,zero credited route drafts pending. The full four-storyline/earlier-dialogue/shared shop/town/random/Help/remaining prose objective stays active,including premature wraps and all207 names. Preserve B43 source-item/Local Product,Samwell middle field,Alexandria caller/display and every earlier unresolved lead. Graphics/all18 plaques and later older-record technical re-audit remain separate/open. No promotion,commit or push occurs in this research checkpoint.'''
NEXT='''Continue the coordinated item116 title/COMMON2931 description review from exact source6085 and actual/native results6081b/6084c/6086/6087. Bind all active description consumers and the staged literal rather than globally replacing Orca;Maria\'s source-owned sobriquet is separate. Preserve the clean シャチ/シャチホコ distinction,threatening pose and reported legend without guaranteed-effect or invented architectural claims. Finalize a faithful natural title/description together,verify native wrapping,complete glyphs,bounds,substitutions and relevant item/list/acquisition behavior,then integrate through a registered cumulative profile and exact clean-input patch once necessary checks pass. Never use a research ROM as the registered parent or change frozen older producers. If ARM9 data changes,rebind current snapshot/font guards using exact owned-data/code/font preservation proofs rather than weakening whole-hash checks. Then author B204 from its20 clean glosses and individual findings6088;eight retentions/twelve revisions are proposed,not immutable quotas or final approval. Preserve the five actors/voices,six leaves,four FE letter objects and full Jam Jack Ludwyan signature;write natural paragraphs and regenerate ordinary wraps. Use representative reviewed-English gameplay and necessary registered regression/startup checks,then credit disjoint integrated objects once. Retain all wider editorial/name/alias/retrospective-wrap scope,all existing artifacts and all unresolved leads. Reuse verified V6050/B203 checks absent a concrete changed-input risk. Graphics/all18 plaques and later older-record technical re-audit remain separate/open.'''

def inverse(value):
    d=deepcopy(value);entry=d.pop(KEY);d.pop(SCOPE);d['latest_checkpoint']=entry['previous_latest_checkpoint'];return d

def gates():
    old_immutable_checks();prior=read(PRIOR)
    for k in ['candidate','patch']:assert sha(Path(prior[k]).read_bytes())==prior[k+'_sha256']
    f,c,d,g,a,p,v,s=map(read,[FINDINGS,CULTURE,DESCRIPTION,GETTERS,ACTUAL,GLYPHS,VIEW,SOURCEVIEW])
    assert len(f['records'])==20 and f['counts']=={'retain-wording':8,'revise':12} and all(r['target_prose_not_authored'] for r in f['records'])
    assert len(c['complete_four_source_exchanges'])==4 and sum(len(x['records']) for x in c['complete_four_source_exchanges'])==80 and len(c['excluded_nonitem_sobriquet_contexts'])==2
    assert d['no_shared_item_name_release_until_COMMON_description_and_active_staged_consumers_reconciled']
    assert g['only_item116_native_and_static_title_outputs_change'] and g['all217_other_item_names_and_late_runtime_names_exact'] and len(g['versions'])==2
    assert a['whole_frames_compared']==182 and a['whole_frames_equal']==128 and len(a['whole_frames_with_measured_differences'])==54 and a['target_end_return_frame']==7895 and len(a['command_timing_and_interval_RNG_differences'])==46
    assert p['all_four_complete_native_and_independent_planes_match_actual_RGB_foreground'] and len(p['cases'])==4
    assert v['viewed'] and v['measured_difference_frame_classes']==dict(item_title=20,acquisition_notice_text=4,advance_prompt=30) and sha(Path(v['sheet']).read_bytes())==v['sheet_sha256']
    assert s['all20_Japanese_objects_four_FE_letter_parts_and_full_signature_viewed'] and len(s['viewed_sheets'])==9
    for root in ['lil_B204_source_run_v6071_clean_Japanese','shachihoko_runs_v6080','shachihoko_B204_card_run_v6083_clean_Japanese']:
        terminal=Path('work/analysis')/root/('newgame_terminal.json' if root=='shachihoko_runs_v6080' else 'terminal.json');assert read(terminal)['terminal']
    for receipt in [read(RESEARCH),read('work/analysis/lil_B204_source_fixture_v6070/complete_B204_source_B22_fixture.json')['fixtures'][0],read('work/analysis/shachihoko_B204_card_fixture_v6082/complete_B204_source_B22_fixture_with_provisional_item_name.json')['fixtures'][0]]:
        assert sha(Path(receipt['research_ROM']).read_bytes())==receipt['research_ROM_sha256']
    return prior

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);mode=parser.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists();prior=gates();before=LEDGER.read_bytes();assert sha(before)==prior['ledger_sha256'];old=json.loads(before);new=deepcopy(old);assert KEY not in new and SCOPE not in new
        inventory=deepcopy(read(old['unfinished_editorial_scope_v6060']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B204_source_names_culture_uncredited_v6090']=dict(source_objects=20,source_commands=26,individual_findings=str(FINDINGS),individual_findings_sha256=sha(FINDINGS.read_bytes()),proposed_retentions=8,proposed_revisions=12,
            exact_names_roles_voices_controls_and_source_gameplay_bound=True,older_B204_English_now_contextually_compared=True,target_prose_not_yet_authored_or_approved=True,all_four_source_castle_variants_contextualized=True,
            provisional_item116_title_research_only=True,coordinated_COMMON2931_and_active_staged_description_consumer_review_pending=True,new_source_prose_or_completion_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        evidence={str(p):sha(p.read_bytes()) for p in [*EVIDENCE,PRIOR,Path(__file__)]}
        new[SCOPE]=dict(path=str(scope),sha256=sha(scope.read_bytes()),retrospective207_names_and_all_wider_editorial_families_preserved=True,full_goal_complete=False)
        summary=DETAILS+'\n\n'+NEXT
        new[KEY]=dict(summary=summary,next=NEXT,previous_latest_checkpoint=old['latest_checkpoint'],evidence=evidence,new_source_prose_reviews=0,new_completed_records=0,new_research_ROMs=3,new_emulator_runs=3,new_frames=30003,
            goal_turn_classification='progress',previous_goal_turn_classification='progress',full_goal_complete=False)
        new['latest_checkpoint']=summary;assert inverse(new)==old
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V6090: source names,cultural item and actual glyph research;V6050 preserved\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            target=Path('docs')/name;text=target.read_text('utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V6090\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[target]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False));print('Six checkpoint targets staged;20 uncredited findings/cultural shared-name risk,all history/current build preserved.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert inverse(new)==old;prior=gates()
        assert new['current_integrated_candidate']==old['current_integrated_candidate'] and new['records_editorially_completed']==6349 and new['records_with_source_and_prose_pass']==6352 and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,h in plan['evidence'].items():assert sha(Path(path).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'independent_audit.json').exists();save(ROOT/'independent_audit.json',dict(deep_inverse_preserves_all_history=True,all_six_targets_current_candidate_and_immutable_inputs_verified=True,staged_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),full_goal_complete=False));print('Six targets/deep inverse/native research gates/source references and immutable cumulative inputs audited.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'independent_audit.json')['staged_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,full_goal_complete=False));print('Six audited checkpoint files applied;all prior history retained.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            result=dict(prior,previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),ledger_sha256=sha(LEDGER.read_bytes()),all_prior_history_and_current_candidate_exactly_preserved=True,
                latest_checkpoint_key=KEY,next_Lil_B204_clean_review_pending=False,prior_English_B204_speech_unread=False,B204_source_names_native_controls_and_source_gameplay_bound=True,
                B204_individual_findings=20,B204_proposed_retentions=8,B204_proposed_revisions=12,B204_target_prose_not_authored_or_approved=True,
                item116_title_and_COMMON2931_coordinated_review_pending=True,new_source_prose_or_completion_credit=0,new_research_ROMs=3,new_emulator_runs=3,new_frames=30003,
                all_sessions_terminal_and_reaped=True,goal_turn_classification='progress',evidence=plan['evidence'],producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',result);print('V6090 verified:V6050/6349 complete unchanged;source/name/cultural/native research recorded,20 findings uncredited;full goal active.')
