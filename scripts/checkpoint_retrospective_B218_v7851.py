"""Reversibly record the source-specific name retention without new dialogue credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Maria_B36_v7826b import COUNTERS,AFTER,INTRO,DETAILS,NEXT as PREVIOUS_NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_checkpoint_v7851')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7852')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7835/verified_handoff.json')
PROOF=Path('translations/lil_B218_retrospective_layout_manuscript_v2.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='retrospective_B218_native_actual_policy_pending_integration_v7851'
SCOPE='unfinished_editorial_scope_v7851'
FINDING="The B218 retrospective automatic-wrap refinement is now approved through source/context, native compiled/stored display, controls/inverses, actual paired English scenes, visual review and frozen-policy validation. Atomic production, registered cumulative build/clean-input patch, affected startup and metadata completion remain pending. The current registered ROM stays V7821; all6938 completed/6941 source-prose/4347 revisions/2591 retentions are unchanged. Revisiting these13 already credited speeches adds no duplicate source/prose/completion/revision/retention credit.\n\nAll13 B218 speeches were reread as a complete clean/current exchange. Each English wording is retained with an individual reason. Only R27's automatic layout changes from (Ian's interested? That's / a surprise.) to (Ian's interested? / That's a surprise.). The remaining12 compiled/stored bodies are exact. No words, punctuation, selectors, macros, font or216px/four-row geometry change. A source-bound soft that's/a preference applies only to this exact paragraph; it is not a global wrapping rule.\n\nThe fresh own-V7821 Lil New Game runs4001 frames with ordinary inputs and no battery/unlock fixture. All six previous whole-RGB pairs, whole actors and captain2 match. Strict2b6/COMMON/directory/all123264 deployed bytes pass. Use work/analysis/current_V7821_Lil_native_v7837/current_native_input.json for further Lil native work. The changed paragraph passes12 logical/previous/proposed alignment cases and two complete before/after native planes. Its one zero-ink stored parity tail passes four more alignments and an exact complete plane. All13 final speech dispatches preserve actors2/21, voices3/1 and zero macros. Both startup/native sheets were viewed.\n\nB218 changes1016 stored/logical/tail0 bytes to1020 stored/1018 logical/tail2. All13 six-byte preambles and15 original commands remain; there are no relative, predicate or typed-menu commands. Original A000 00a0ffff2e000110 stays eight bytes; the complete four-byte normal end moves1012->1014 and the two zero tail bytes remain separate.25 isolated seeded normal ends preserve type0 and the prior value word. The opaque A000 structural bridge does not establish full effect mechanics. Clean/predecessor block inverses and the full predecessor archive inverse are exact; all335 other SC2 blocks and every other file/component remain unchanged. The research image passes336 native full loads/cache hits and672 original parent modes. One fresh bounded shipped-unit caller census finds only original24070 and no literal alias; arbitrary dynamic mutation and natural eligibility remain separate.\n\nTwo fresh16001-frame previous/proposed English gameplay fixtures use the same nine original B22 initialization commands and all15 B218 commands, with identical ordinary inputs and read-only observation. Both jobs are terminal/reaped; callback slots and core files remain exact. Each covers13 complete single pages and51 complete body/nameplate holds:26 pages/102 holds total,zero partial sampled holds or unreturned commands. All26 exact panes/eight sheets were directly viewed. Lil Argot and Ian Dukov headers and all13 paired upper scenes/portraits/nameplates agree. No new Japanese capture is claimed.\n\nBoth scenes exit5975 with actual normal result[0,0]. All24 command results/UI requests agree; there are no duration or RNG differences. Eight comparison rows differ only in decoded length or relocated offsets. All167 later whole-RGB comparisons agree, as do final state/models/persistent objects/tasks/calendar, whole actors and seed3000421369. Preserve every raw measurement without claiming every-frame/full-RAM/future/causal/full-mechanics/full-route or hardware equivalence. Initialized Amsterdam and later sailing are not natural B218 location/activation; incidental later text receives no editorial credit.\n\nThe frozen retrospective contract binds all13 exact source/current paragraphs, two source-supported actors, zero macros, unchanged geometry, nine individual informational row-count reasons, the12 unchanged plans and one revised plan. All13 positive cases and221 actual-changing source/character/meaning/macro/manual-layout/profile/runtime/block corruptions pass; no no-op/schema failure or QA warning waiver is counted. Manuscriptv2 individually approves all five gates and still requires atomic registered integration. The unrelated Maria CS0101 header assumption was rejected before any ROM write; preserved source-locked successors bind clean/current Lil's exact CS0001 header and retain all other guards. All failed producers, earlier manuscripts, ROMs, traces and proofs remain.\n\nThe original shared151-159 progressive-nameplate finding remains: clean 水夫 supports Sailor, separately from 配下/Retainer full-name data. The full207 names/roles/aliases and remaining consumers remain open. Preserve all13 earlier wrap leads; R27 is approved but not integrated, and the other12 remain candidates requiring individual contextual decisions. The markup-only scan covered558/6938 records, not all completed dialogue. Continue all four storylines and earlier translations, broad practical shared shop/town/random capture, Help and remaining player prose. Graphics/all18 plaques and later older-record technical re-audit stay separate. MainV4701 remains unchanged; no canceled separate test package, promotion, pruning, commit or push."
NEXT="Continue from verified V7852/current V7821. The approved retrospective B218 manuscript is translations/lil_B218_retrospective_layout_manuscript_v2.json; frozen contract/profile/formatter/planner are lil_B218_retrospective_*_v1. The map is work/analysis/retrospective_B218_relocation_v7839b/all13_bound_one_changed_wrap15_commands_complete_clean_predecessor_inverse.json and the reusable exact reconstruction helper is dk4tool/patch/retrospective_SC2_reconstruction_v2.py. Do not rerun completed source/gloss/native/stored/control/inverse/load/caller/paired actual/visual/policy checks without a new reason.\n\nNext implement and validate one atomic final SC2 files-list commit for the source-bound13-record block, preserving all335 unowned blocks and every other file/component; only R27 stored bytes should change. Bind13 wording retentions,one automatic wrap revision,12 exact stored retentions,15 original commands/no relative sites,old1016/logical1016/tail0 and new1020/logical1018/tail2. Challenge actual-changing production corruption with dependency checks deliberately bypassed and reject before any commit. Seal exact immutable references, register the layer after V7821, build through the registered cumulative builder, run required checks, prove exact clean-input patch reconstruction and affected own-ROM startup. Update the existing family/references reversibly without adding duplicate editorial credit. Keep mainV4701 and all prior ROMs/translations.\n\nUse Lil's strict own-V7821 input at work/analysis/current_V7821_Lil_native_v7837/current_native_input.json and Maria's separate own-V7821 captain3 input at work/analysis/current_V7821_native_v7824/route3/current_native_input.json. Do not substitute one route's RAM for another's or relabel an older capture as current. Capture another route's own current context when needed.\n\nKeep the13 retrospective leads and558-plan scan limitations fromV7831. Review remaining candidates as complete source/current exchanges, retain ordinary wraps with reasons, and extend coverage through exact current consumers. Continue all four storylines and earlier translated dialogue, shared shop/town/random/Help/remaining prose, all207 names/roles/aliases and every earlier unfinished inventory/counterpart/item/display lead. Keep the source-supported151-159 Sailor retention and their separate full-name/indirect/typed/COMMON/UI review. Preserve every artifact and all earlier measured limits. Graphics/all18 plaques and the later older-record technical re-audit remain separate. No separate unified test package, automatic promotion, pruning, commit or push."
SUMMARY=INTRO+'\n\n'+FINDING+'\n\n'+DETAILS

def restore(value):
    new=deepcopy(value);entry=new.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(new,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return new

def gates():
    prior,proof=map(read,[PRIOR,PROOF])
    approval=read('work/analysis/retrospective_B218_approval_v7850/all13_five_gates_approved_one_wrap_no_duplicate_credit.json')
    actual=read('work/analysis/retrospective_B218_actual_v7846/two_English_scenes_complete_masks_commands_andall_measured_late_limits.json')
    policy=read('work/analysis/retrospective_B218_policy_validation_v7849/13_positives221_actual_changing_policy_rejections.json')
    assert approval['manuscript_sha256']==sha(PROOF.read_bytes()) and approval['all13_individual_five_gates_approved']
    assert len(proof['records'])==13 and all(all(r['review'].values()) for r in proof['records'])
    assert proof['wording_retentions']==13 and proof['proposed_automatic_layout_revisions']==1 and proof['unchanged_exact_compiled_plans']==12
    assert proof['atomic_registered_release_andmetadata_completion_pending'] and not proof['new_credit']
    assert actual['both_jobs_terminal_andreaped'] and actual['total_actual_pages']==26 and actual['total_actual_complete_body_andheader_holds']==102
    assert actual['total_incomplete_sampled_holds']==0 and actual['all24_original_command_results_andUI_equal']
    assert policy['positive_count']==13 and policy['negative_count']==221 and policy['all_negative_inputs_actually_changed_andrejected']
    assert proof['current_ROM_sha256']==prior['candidate_sha256']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
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
        oldscope=old['unfinished_editorial_scope_v7834'];assert sha(Path(oldscope['path']).read_bytes())==oldscope['sha256']
        inventory=deepcopy(read(oldscope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(proof=str(PROOF),proof_sha256=sha(PROOF.read_bytes()),finding=FINDING,
            wordings_retained=13,pending_layout_revisions=1,other_exact_compiled_reuses=12,all_prior_inventories_andfull_scope_preserved=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_andfull_scope_preserved=True,new_credit=0,full_goal_complete=False))
        put(['formatting_watchlist',KEY],dict(proof=str(PROOF),finding=FINDING,native_actual_policy_complete_atomic_registered_release_pending=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        index=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
        put(['coverage_units',index,'next'],NEXT)
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,PROOF,scope,Path(__file__),
            Path('work/analysis/completed_contraction_wrap_leads_v7831/completed_layout_contraction_andquestion_tag_leads_with_live_storage_refs.json'),
            Path('work/analysis/retrospective_B218_wrap_gloss_v7832/thirteen_fresh_clean_exchange_glosses_before_full_current_layout_review.json'),
            Path('work/analysis/retrospective_B218_predicate_plan_v7833/one_changed_automatic_plan12_exact_reuses_all13_unmodified_base_QA.json'),
            Path('scripts/plan_retrospective_B218_predicate_v7833.py'),
            Path('work/analysis/retrospective_B218_approval_v7850/all13_five_gates_approved_one_wrap_no_duplicate_credit.json'),
            Path('work/analysis/retrospective_B218_policy_validation_v7849/13_positives221_actual_changing_policy_rejections.json'),
            Path('work/analysis/retrospective_B218_actual_view_v7847/26_actual_panes_eight_sheets_andall_measured_limits_viewed.json'),
            Path('work/analysis/retrospective_B218_actual_v7846/two_English_scenes_complete_masks_commands_andall_measured_late_limits.json'),
            Path('work/analysis/retrospective_B218_relocation_v7839b/all13_bound_one_changed_wrap15_commands_complete_clean_predecessor_inverse.json'),
            Path('work/analysis/retrospective_B218_relocation_repair_v7839b/provenance.json'),
            Path('work/analysis/current_V7821_Lil_native_v7837/current_native_input.json'),
            Path('translations/lil_B218_retrospective_native_contract_v1.json'),
            Path('dk4tool/dialogue/lil_B218_retrospective_profile_v1.py'),
            Path('dk4tool/dialogue/lil_B218_retrospective_layout_v1.py'),
            Path('dk4tool/dialogue/lil_B218_retrospective_plan_v1.py')]}
        new[KEY]=dict(summary=FINDING,next=NEXT,proof=str(PROOF),evidence=evidence,inverse_operations=ops,
            wording_retentions=13,pending_automatic_wrap_revisions=1,no_duplicate_dialogue_credit=True,
            new_credit=0,new_emulator_runs=3,new_actual_frames=36003,new_native_getter_executions=0,
            only13_metadata_leads_andone_pending_changed_plan_not_broad_wrap_approval=True,
            full_scope_all13_other_wrap_leads_andnames_remain_open=True,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['completed_editorial_families']==old['completed_editorial_families']
        assert new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        targets={LEDGER:encode_ledger(new)}
        section='## V7851: B218 wrap native/actual/policy approved; atomic registered integration pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V7851; V7821 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,zero_credit=True,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six retrospective-wrap checkpoint targets staged;all counts andcurrentROM unchanged.')
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
            print('Six audited retrospective-wrap checkpoint targets applied;V7821/6938completed unchanged.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_hash_exact']
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),
                previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                retrospective_B218_R27_layout_pending=True,retrospective_B218_native_actual_policy_complete=True,retrospective_wrap_leads=13,
                recorded_markup_plans_scanned=558,completed_records_not_in_markup_scan=6380,
                pending_layout_manuscript=str(PROOF),pending_layout_manuscript_sha256=sha(PROOF.read_bytes()),
                strict_own_Lil_current_input='work/analysis/current_V7821_Lil_native_v7837/current_native_input.json',
                unfinished_scope=SCOPE,next_required=NEXT,latest_checkpoint=KEY,
                new_credit=0,new_emulator_runs=3,new_actual_frames=36003,new_native_getter_executions=0,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('V7852 verified:B218 wrap native/actual/policy approved;atomic integration pending;V7821/6938complete remain.Fullobjective active.')
