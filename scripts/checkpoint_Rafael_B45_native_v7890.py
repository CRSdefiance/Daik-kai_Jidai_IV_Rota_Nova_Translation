"""Reversibly record the source-specific name retention without new dialogue credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Maria_B36_v7826b import COUNTERS,AFTER,INTRO,DETAILS,NEXT as PREVIOUS_NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_native_checkpoint_v7890')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7891')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7866/verified_handoff.json')
PROOF=Path('work/analysis/Rafael_B45_reference_census_v7889/all24_commands_five_relative_sites_EV0_entry_shipped_callers.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Rafael_SC0B45_native_actual_release_pending_v7890'
SCOPE='unfinished_editorial_scope_v7890'
FINDING="Current registered experimental V7857 and promoted main V4701 remain unchanged. The632-batch/114-accepted-layer cumulative stack retains its verified18 release checks,110 regressions,whole-ROM research-reference equality andexact clean-input patch reconstruction. All6938 completed/6941 source-prose anddrafts/4347 integrated wording revisions/2591 retentions remain unchanged;Rafael B45 is a pending batch andadds no review credit yet.\n\nRafael SC0 B45 now has a complete source-first whole-exchange draft:seven wording revisions andfive individually justified retentions across12 speeches. All clean Japanese glosses preceded the first current-English exposure. The24 original source/current dispatches bind the complete effective English withzero catalogue substitutions;the12 final stored dispatches also pass. The draft restores conditional Lisbon cargo,Julio's payment-to-the-local-ruler explanation,early minimum-fee advice,his Ceuta agreement andRafael's future responsibility,andthe optional sale. Clean Help150 is bound byte forbyte:market share limits purchases of local stock,while1percent permits unlimited selling. The FE panel therefore states FO's Ceuta20percent share andexplains the purchasable local stock without inventing a sales-volume cap,company ownership orprofit. Rafael's brief replies are retained with individual contextual reasons.\n\nA fresh4001-frame ordinary captain0 V7857 NewGame capture is terminal/reaped. Six whole-RGB pairs,whole actor data andcaptain ID match the prior startup control. This establishes the current Rafael native context,not B45 activation orfull-route coverage. Both progressive/full getters support Rafael Castor andJulio Erneco;the clean surname isエルネコ,notエルネスト. Retain the existing source-compatible spelling. Four name getters,two source voice classes andeight default macro alignments pass;measured FI6/FA6/FO10 match Rafael/Castor/Castor Co. FE254 is a separate null-actor information-panel selector,not a character.\n\nAll12 complete compiled native pages and48 compiled macro/literal alignments pass andboth sheets were directly viewed. Each automatic row boundary has an individual contextual reason. The four leading00 actor bytes remain in their exact six-byte native preambles,with ordinary NUL-free text formatting andits terminator guard unchanged. One early planner guessed a nonexistent profile;its immutable successor uses the registered Rafael profile with measured defaults. An initial FE plan mistook its228px bitmap for usable text width andthe native full-return check rejected it at104/117bytes. The forensic capture and32 boundary measurements show36 ASCII cells/216px usable text andthe pair-phase blank-row hazard;the corrected plan keeps every English word andfits the original228x48 logical/228x64 physical FE panel inone complete page. Preserve the failed producers/partial planes andall diagnostics;do not classify those failures as passed negative release tests.\n\nResearch-only relocation grows B45 from764stored/762logical/two-tail bytes to864stored/864logical/no tail. All24 command mappings,twelve six-byte preambles,the source FO token andall five relative operands/nested scopes remain bound. Five relocated sites/25 native skip cases pass. Exact inverse reconstruction recovers both the complete clean block andthe complete predecessor block/archive. Seven compiler-owned parity tails receive28 fresh native alignment cases andfresh complete-page checks;five unchanged bodies reuse20 exact existing cases. All12 stored ink planes match the viewed pages,withno additional orblank pages. Twelve final dispatches,one relocated original8000 predicate and25 cold isolated seeded normal-end cases pass;normal type0 preserves the value word. Thirty source resource-boundary cases andtwo61FF/C281 structural pairs are reused byexact command/code equality,without claiming that their bridged callee effects were executed.\n\nThe preserved unregistered research image out/Rafael_B45_reference_v7887_RESEARCH_ONLY.nds changes onlySC0 B45;342 otherSC0 blocks andevery other file/component remain exact. It is a focused-test reference,not the canceled separate unified package,a new parent,a promotion orregistered release. All343 original SC0 load/cache paths,686 original parent modes,a fresh shipped-caller census andall24 source/current/target command references pass. EV0 is unchanged anduses block indices. The original event45/action46 has no explicit dependency/exclusion;neither this nor numeric44/45 adjacency establishes natural activation,chronology orlocation. The original FE branch enters for previous predicate result1;other structural results skip it. No assumption that all12 stored speeches alwaysplay is allowed.\n\nThe pending manuscript translations/rafael_B45_editorial_manuscript_v3.json still has all12 formatting gates false. Actual B45 body/nameplate/FE/transitions andreturn observations,frozen policy/atomic production tests andregistered cumulative integration remain required. No new B45 gameplay,full mechanics,earned progression,custom-name,full catalogue UI orhardware coverage is claimed. All broader four-storyline,earlier translation,shared shop/town/random,Help/remaining prose,207-name andretrospective-wrap work remains open. Preserve all12 remaining wrap leads beyond the558-plan heuristic's limited coverage,Sailor151-159 versus separate Retainer consumers,every older unfinished inventory anditem/counterpart/display lead. Graphics/all18 plaques andlater older-record technical re-audit remain separate. Preserve every generated ROM,translation,draft,executed/failing producer andproof. No separate unified test package,promotion,pruning,commit orpush."
NEXT="Continue from verifiedV7891/currentV7857 andthe pending Rafael B45 native checkpoint. Use translations/rafael_B45_editorial_manuscript_v3.json,work/analysis/Rafael_B45_native_review_v7883/native_visual_review_andexact_plan_guard_rebinding.json,work/analysis/Rafael_B45_stored_v7885/all12_stored_bodies28_fresh20_reused_alignments_exact_viewed_planes.json,work/analysis/Rafael_B45_relocated_controls_v7886/12_stored_dispatches25_relocated_relative_cases_predicate25_seeded_ends.json andwork/analysis/Rafael_B45_reference_census_v7889/all24_commands_five_relative_sites_EV0_entry_shipped_callers.json. Native source/current names,macro wrappers,all12 complete compiled/stored planes,343load/cache paths,686parent modes,24command references andfive relocated native branches are checked;reuse those exact proofs without rerunning them.\n\nNext obtain representative paired source/English gameplay withthe complete original B45 exchange,including its conditional FE information panel and61FF/6300/6328/632B/C281 display transitions. A disclosed entry fixture maypreserve the actually observed original B44 ten-command startup prelude from work/analysis/papal_trade_initializer_binding_v7647/two_actual_opening_preludes18_commands_bound_before_optional_scene_fixture.json,after exact current B44/code/ordinary-input binding. Shift all B45 command references and0100 ancestors bythe prelude length while keeping original relative spans. Preserve every original B45 control andcondition;do not force roles,roster,funds,RNG,predicate results,event flags,RAM,battery orsave state to make FE execute. Natural Ceuta activation andoriginal location remain separate from a Lisbon-opening fixture. Treat FE as original24310 null actor then5473C,not progressive/fallback208. Verify complete glyph masks,percent words/FO,headers,all selected command results,pagination/transitions/normal return,andretain every measured timing/state difference. Exhaustive natural playthroughs are not required.\n\nAfter necessary actual checks,freeze the scoped natural-dialogue-v2 policy/profile andcomplete real changing-input rejection tests andatomic production validation. Integrate the twelve reviewed speeches into the registered cumulative release onlyonce those checks pass;require whole research-reference equality,all accepted layers/regressions,exact clean-input patch reconstruction andappropriate startup controls. Add7revision/5retention completion credit onlyafter registered integration;untilthen all current counters andV7857 remain unchanged. Keep00 actor bytes in complete native preambles,body embedded-NUL rejection,measured FI6/FA6/FO10,216px usable text,distinct FE228px bitmap,five relative fixups andtype0 normal-end value carry.\n\nOwn current Rafael input is work/analysis/current_V7857_Rafael_native_v7868/current_native_input.json;own current Lil input remains work/analysis/current_V7857_Lil_native_v7860/current_native_input.json. Maria's ownV7821 context remains historical toV7857;obtain a current route context when needed. All four storylines andearlier translated dialogue,shared shop/town/random scenes,Help/remaining player prose,all207 names/roles/aliases and12 remaining wrap leads stayopen. Extend the wrap review beyond the558plans;retain ordinary soft wraps withreasons. Preserve every earlier unfinished inventory,source-supported Sailor151-159/separate Retainer findings anditem/counterpart/display leads. Keep graphics/all18 plaques andthe later older-record technical re-audit separate. Preserve every prior artifact. MainV4701 stays;no canceled separate package,promotion,pruning,commit orpush."
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
    manuscript=read('translations/rafael_B45_editorial_manuscript_v3.json')
    native=read('work/analysis/Rafael_B45_native_review_v7883/native_visual_review_andexact_plan_guard_rebinding.json')
    stored=read('work/analysis/Rafael_B45_stored_v7885/all12_stored_bodies28_fresh20_reused_alignments_exact_viewed_planes.json')
    controls=read('work/analysis/Rafael_B45_relocated_controls_v7886/12_stored_dispatches25_relocated_relative_cases_predicate25_seeded_ends.json')
    reference=read('work/analysis/Rafael_B45_reference_v7887/research_image_receipt.json')
    assert len(manuscript['records'])==12 and sum(r['decision']=='revision' for r in manuscript['records'])==7
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in manuscript['records'])
    assert native['all12_individual_row_reasons'] and len(native['direct_visual_review'])==2 and all(s['directly_viewed'] for s in native['direct_visual_review'])
    assert stored['all12_native_ink_planes_exact_to_already_viewed'] and stored['seven_parity_tails_create_no_blank_oradditional_page']
    assert len(controls['final_dispatches'])==12 and len(controls['normal_seeded_ends'])==25
    assert len(proof['all_command_maps'])==24 and len(proof['relative_operand_maps'])==5
    assert proof['all_original_EV0_block_indices_and343_load_cache_paths686_parent_modes_verified']
    assert proof['research_ROM_sha256']==reference['research_ROM_sha256']==sha(Path(proof['research_ROM']).read_bytes())
    assert not reference['registered_candidate'] and reference['all_prior_ROM_pins_preserved']
    for packet in [proof,stored,controls,reference]:
        assert not packet['new_credit'] and not packet['new_emulator_runs']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==proof['parent_sha256']
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
        oldscope=old['unfinished_editorial_scope_v7865'];assert sha(Path(oldscope['path']).read_bytes())==oldscope['sha256']
        inventory=deepcopy(read(oldscope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(proof=str(PROOF),proof_sha256=sha(PROOF.read_bytes()),finding=FINDING,
            clean_source_speeches=12,pending_wording_revisions=7,pending_wording_retentions=5,current_English_bodies_unread=False,all_prior_inventories_andfull_scope_preserved=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_andfull_scope_preserved=True,new_credit=0,full_goal_complete=False))
        put(['formatting_watchlist',KEY],dict(proof=str(PROOF),finding=FINDING,native_names_macros_branches_current_English_compiled_andstored_pages_complete=True,actual_policy_atomic_registered_release_pending=True,new_credit=0))
        put(['Rafael_SC0B45_clean_gloss_pending_v7865','superseded_by'],KEY)
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        index=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
        put(['coverage_units',index,'next'],NEXT)
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,PROOF,scope,Path(__file__),
            Path('translations/rafael_B45_editorial_manuscript_v3.json'),Path('translations/rafael_B45_speaker_name_review_v1.json'),
            Path('work/analysis/Rafael_B45_context_binding_v7868/own_Rafael_startup_andstrict_captain0_context.json'),
            Path('work/analysis/Rafael_B45_names_v7869/two_static_speakers_four_getters_clean_fields_eight_macro_alignments.json'),
            Path('work/analysis/Rafael_B45_source_controls_v7870b/source_EV0_five_relative_sites_predicate_resources_structural_andnormal_end.json'),
            Path('work/analysis/Rafael_B45_effective_v7872/all12_effective_English_templates24_original_dispatches_distinct_FE.json'),
            Path('work/analysis/Rafael_B45_FE_boundary_v7880/32_FE_terminal_andbreak_pair_boundary_measurements.json'),
            Path('work/analysis/Rafael_B45_native_review_v7883/native_visual_review_andexact_plan_guard_rebinding.json'),
            Path('work/analysis/Rafael_B45_stored_v7885/all12_stored_bodies28_fresh20_reused_alignments_exact_viewed_planes.json'),
            Path('work/analysis/Rafael_B45_relocated_controls_v7886/12_stored_dispatches25_relocated_relative_cases_predicate25_seeded_ends.json'),
            Path('work/analysis/Rafael_B45_reference_v7887/research_image_receipt.json')]}
        new[KEY]=dict(summary=FINDING,next=NEXT,proof=str(PROOF),evidence=evidence,inverse_operations=ops,
            clean_source_speeches=12,pending_wording_revisions=7,pending_wording_retentions=5,no_source_prose_orcompletion_credit=True,
            new_credit=0,new_emulator_runs=1,new_actual_frames=4001,scoped_native_name_getter_checks=4,
            source_first12_drafts_native_pages_relocation_loaders_caller_verified_not_actual_B45_orrelease_approval=True,
            full_scope_remaining12_wrap_leads_andnames_remain_open=True,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['completed_editorial_families']==old['completed_editorial_families']
        assert new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        targets={LEDGER:encode_ledger(new)}
        section='## V7890: Rafael B45 contextual draft andnative checks; actual/integration pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V7890; V7857 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,zero_credit=True,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six Rafael native-progress checkpoint targets staged;all counts andcurrentROM unchanged.')
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
            print('Six audited Rafael native-progress checkpoint targets applied;V7857/6938completed unchanged.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_hash_exact']
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),
                previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                Rafael_B45_clean_source_review_pending=False,Rafael_B45_fresh_clean_glosses=12,Rafael_B45_current_English_bodies_unread=False,Rafael_B45_native_layout_relocation_andreferences_complete=True,Rafael_B45_actual_gameplay_policy_atomic_andintegration_pending=True,
                recorded_markup_plans_scanned=558,completed_records_not_in_markup_scan=6380,
                pending_Rafael_reference_proof=str(PROOF),pending_Rafael_reference_proof_sha256=sha(PROOF.read_bytes()),pending_Rafael_manuscript='translations/rafael_B45_editorial_manuscript_v3.json',
                Rafael_B45_own_current_route0_context_pending=False,strict_own_Rafael_current_input='work/analysis/current_V7857_Rafael_native_v7868/current_native_input.json',
                unfinished_scope=SCOPE,next_required=NEXT,latest_checkpoint=KEY,
                new_credit=0,new_emulator_runs=1,new_actual_frames=4001,scoped_native_name_getter_checks=4,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('V7891 verified:Rafael B45 draft/native/stored/relocation/loaders/callers complete;actual/policy/integration pending.V7857/6938completed unchanged.Fullgoal active.')
