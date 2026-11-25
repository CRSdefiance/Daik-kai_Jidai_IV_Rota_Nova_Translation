"""Reversible progress checkpoint: new Hodram prose/native bodies; Gerhard policy sealed, atomic stage pending."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.gerhard_surname_profile_v1 import validate_approved_batch
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B50_v8184 import COUNTERS,AFTER
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_prose_Gerhard_policy_checkpoint_v8249')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8250')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8235/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
OLD_KEY='Gerhard_Adernkatz_scoped_actual_format_approved_pending_policy_atomic_registered_andHodram28_v8234'
KEY='Hodram28_contextual_prose_native_bodies_Gerhard_frozen_policy_pending_atomic_actual_registered_v8249'
SCOPE='unfinished_editorial_scope_v8249'
PROOFS={
 'Hodram_current':'work/analysis/Hodram_B137_B45_B46_current_v8239/28_exact_clean_current_refs_after_whole_source_glosses.json',
 'Hodram_effective':'work/analysis/Hodram_B137_B45_B46_effective_v8240/all28_effective_English_templates56_original_dispatches_no_FE.json',
 'Hodram_manuscript':'translations/hodram_B137_B45_B46_editorial_manuscript_v2.json',
 'Hodram_prose':'work/analysis/Hodram_B137_B45_B46_prose_v8241b/28_contextual_decisions_three_exchanges_individual_revisions_retentions.json',
 'Hodram_logical':'work/analysis/Hodram_B137_B45_B46_refinement_v8244/28_logical_paragraphs4_fresh108_exact_reused_alignments.json',
 'Hodram_plan':'work/analysis/Hodram_B137_B45_B46_layout_v8245/28_automatic_Hodram_plans_full_native_width.json',
 'Hodram_pages':'work/analysis/Hodram_B137_B45_B46_pages_v8246/28_complete_native_paragraphs28_pages112_compiled_alignments.json',
 'Hodram_native_view':'work/analysis/Hodram_B137_B45_B46_native_review_v8247/28_native_pages_directly_viewed_two_exact_boundary_reviews.json',
 'Hodram_names':'translations/hodram_B137_B45_B46_speaker_name_review_v2.json',
 'Gerhard_frozen':'work/analysis/Gerhard_policy_v8236/frozen_policy_receipt.json',
 'Gerhard_policy_tests':'work/analysis/Gerhard_policy_validation_v8237/five_body_one_name_policy_positives_andexpected_guard_rejections.json',
 'Gerhard_manuscript':'translations/gerhard_surname_consistency_manuscript_v3.json',
 'Gerhard_map':'translations/gerhard_surname_editorial_relocation_map_v1.json',
 'Gerhard_seal':'work/analysis/Gerhard_reference_seal_v8238/five_body_one_name_exact_reference_andactual_scope_approved.json',
 'Gerhard_risk_recompute':'work/analysis/Gerhard_risk_helper_v8248/independent8phase_RAM_bytes_andexact_replay_recomputation.json',
}
SUMMARY="""Registered cumulative V8172 and main V4701 are unchanged. The full editorial goal remains active across all four stories, earlier dialogue, towns, shops, random scenes, Help, remaining prose, speaker names and retrospective early wraps. This checkpoint adds no completion or integration credit: the existing counters remain 7171 completed, 7174 credited source/prose-and-drafts, 4455 integrated revisions and 2716 retentions. The new 28 Hodram contextual drafts are explicitly pending outside those credited counters. Preserve all previous scope inventories, generated ROMs, translations, proofs and failures. No separate unified test package, promotion, pruning, commit or push.

The 28 Hodram SC1 B137/B45/B46 passages now have a complete clean-source/current-English contextual review: 16 proposed revisions and 12 individually justified retentions. Exact clean/current/preamble/control references are in the8239 map and manuscriptv2;56 original clean/current dispatches8240 bind all effective text and six static actors in the existing own captain1 context. One runtime catalogue match already corrects the obsolete stored Kamil sentence to Camille; that working effective name check is retained. Camille's apology, Charles's hostility, Hodram's restrained reassurance and Gerhard's practical staffing advice form a complete exchange. Lil's challenge concerns reported regional wealth, a map-deciphering key and finding treasure first. Corrections remove Duel, captain-limited wealth and reveals a map; restore maritime-trade context, both Lisbon/Seville, capable people and possible rather than guaranteed recruitment. Do not invent kinship, rank, romance, a map gift, accepted contest, victory or completed routes. Three original silences and the casual Argot Company boss invitation are retained with individual reasons.

Manuscriptv1 and syntax-failed producer8241 are preserved;8241b repairs only one surplus parenthesis before any outputs. A second whole-exchange reread polishes one inflated formal reply in manuscriptv2. Its four alignments are fresh;108 unchanged logical alignments reuse8242 exactly. Private Hodram automatic216px/four-row wrapping uses measured6/9/15 defaults, source actors01/02/09/10/12/71, zero FI/FA/FO and exact source-bound three ellipsis records. Global profiles, native fonts, NUL/guard/pair-phase rules and QA remain unchanged. Revised plan8245 supersedes8243 for this manuscript. All28 compiled body paragraphs have112 fresh native alignments and28 complete single pages through unchanged2b6 code, with independent full glyph planes, first/internal/final characters, bounds and consumption. All three offline preview sheets were directly viewed. Two original weak-ending warnings (B137R89 the/Mediterranean;R92 to/the towns) and five line-count infos remain recorded. Their exact source/prose/compiled boundaries have narrow readable-wrap reasons8247; no global weak-word waiver, manual wrap or shortened prose. These body proofs are offline native checks, not new emulator gameplay, nameheaders, stored script approval or event activation. All28 formatting gates remain false.

Gerhard Adernkatz now has a frozen source/prose/layout/name contract8236 and260 actual-changing policy rejections8237, plus five body/one name positive checks. Independent reconstruction8238 seals manuscriptv3 and the exact source/current/final map:225 commands,130 preambles,44 relatives,125 unowned speeches,334 other SC2 blocks, prior typed choice and complete predecessor block/archive/ROM inverses. It byte-matches the pinned research8215 image. Only the owned12-byte surname and five previously completed speeches change; protect the separate Blades8 string, all pointer fields and every other ARM9 byte. Fourteen existing consistent consumers and20 final Adernkatz occurrences remain bound. No duplicate dialogue credit or official Latin-canon claim. Independent risk helper8248 recomputes all eight sampled native RAM phases, every bounded byte difference and exact focused replay rows/selected framebuffers/final RAM from the existing captures. It is not a completed independent atomic production stage or its corruption suite.

All prior Gerhard actual limits remain: fullB27 selects35of51 and later enters SC0B44/captain0 in the initialized fixture; this is not normal Lil route continuity or natural Stockholm activation. FullB74 selects75of79, including all three corrected bodies and menu option0. Focused intro displays8 original speeches covering both other corrected bodies but bypasses the outer condition and remaining full-script effects. Eight terminal runs total176008 frames,30 complete bodyholds,262 relevant nameholds and117 scene/portrait pairs. Command/duration difference counts1/0,74/19,8/2; later RGB comparisons328/164/106 with0/0/29 differences. Intro final models/persistent/actors/RNG differences remain bounded. First seven sampled component sets match; final sample differs in2 fleet,150 actor and54 town bytes, with raw calendar535/[0,11,7] versus534/[0,11,6] before final convergence. Do not interpret dates or claim every-frame causality, full simulation, all branches, hardware or a natural playthrough. Graphics/all18 plaques and the later older-record technical re-audit remain separate.
"""
NEXT="""Continue from verifiedV8250/current registeredV8172. Reuse the Gerhard frozen contract8236,260 policy rejections8237, independently sealed references8238 and risk recomputation8248. Implement the independent production stage that validates both ARM9+SC2 changes completely in memory, then commits one final NDS object. It must reject semantic proof corruption even when dependency digests are deliberately bypassed; trap all commits on failure. Bind exact prose/gates, name12/Blades8/pointers/no interior literal aliases, native/stored/actual masks, controls, inverse, loaders/callers and every recorded scope/risk limit. Positive full-reference equality and meaningful precommit corruption challenges remain required. Then register the cumulative experimental profile after the entire V8172 stack, build through build_integrated_release.py, verify exact approved reference, clean-input patch, appropriate release checks/regressions and own registered startup. Do not promote, build a separate requested test package, prune, commit or push. Main4701 stays unchanged.

Resume Hodram from manuscriptv2 and viewed native28 bodies8246/8247, not from the old unconsulted-English status. Source controls8188,4800 Red Dye/layout0 proof8190b, paths8191, names8192 and own captain1 input8187 remain verified. Next reconstruct stored SC1 B137/B45/B46 with exact60 commands/eight relative sites/two raw8000 operands/full ends; verify parity and stored glyphs. Review complete nameplanes and representative actual headers, source silences, distinct4800/layout0 and hide4700 behavior, normal returns and transitions using disclosed fixtures without state/branch forcing. Formatting, frozen policy, atomic production and registered integration remain pending. Every H1 integration must explicitly include the registered Adernkatz name-asset dependency; the captain2 research context is not a Hodram context. Retain all207-name/role/alias, whole-story, shared/town/random/Help, earlier-wrap, graphics and later-audit leads from the previous inventory without narrowing the objective.
"""

def restore(value):
    result=deepcopy(value);operations=deepcopy(result[KEY]['inverse_operations'])
    for op in reversed(operations):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result

def gates():
    prior=read(PRIOR);data={k:read(p) for k,p in PROOFS.items()}
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    manifest=read(prior['manifest']);registry=read('translations/release_stack.json')
    assert sha(Path('translations/release_stack.json').read_bytes())==manifest['release_stack_sha256']
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    doc=data['Hodram_manuscript'];assert len(doc['records'])==28 and doc['revised']==16 and doc['retained']==12
    assert all(all(r['review'][g] is True for g in ['source','context','localization','naturalness']) and r['review']['formatting'] is False for r in doc['records'])
    assert data['Hodram_effective']['source_packet_sha256']==sha(Path(PROOFS['Hodram_current']).read_bytes())
    assert len(data['Hodram_effective']['source_current_dispatches'])==56
    assert sum(r['registered_catalogue_match'] is not None for r in data['Hodram_effective']['effective_current_records'])==1
    assert data['Hodram_logical']['total_bound_alignment_cases']==112 and data['Hodram_logical']['fresh_native_alignment_cases']==4 and data['Hodram_logical']['exact_reused_native_alignment_cases']==108
    assert not data['Hodram_plan']['failures'] and len(data['Hodram_plan']['records'])==28
    assert data['Hodram_pages']['complete_progressive_pages']==28 and data['Hodram_pages']['fresh_compiled_alignment_cases']==112
    assert data['Hodram_native_view']['all28_complete_bodies_visually_read'] and len(data['Hodram_native_view']['original_warnings'])==2 and len(data['Hodram_native_view']['original_infos'])==5
    assert all(s['directly_viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in data['Hodram_native_view']['directly_viewed_sheets'])
    for key in ['Hodram_logical','Hodram_plan','Hodram_pages','Hodram_native_view']:assert data[key]['manuscript_sha256']==sha(Path(PROOFS['Hodram_manuscript']).read_bytes())
    validate_approved_batch(data['Gerhard_manuscript'])
    assert data['Gerhard_policy_tests']['negative_count']==260 and data['Gerhard_policy_tests']['all_rejections_match_expected_semantic_guard']
    assert data['Gerhard_seal']['independent_reconstruction_byte_equal_reference'] and data['Gerhard_seal']['every_predecessor_block_archive_andwholeROM_byte_reconstructed_exactly']
    assert data['Gerhard_seal']['manuscript_sha256']==sha(Path(PROOFS['Gerhard_manuscript']).read_bytes()) and data['Gerhard_seal']['reference_map_sha256']==sha(Path(PROOFS['Gerhard_map']).read_bytes())
    assert data['Gerhard_risk_recompute']['eight_native_RAM_phase_values_andall_byte_differences_recomputed'] and data['Gerhard_risk_recompute']['not_independent_atomic_production_approval']
    return prior,data

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,data=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==AFTER and old['goal_status']=='active' and not old['full_goal_complete']
        assert OLD_KEY in old and KEY not in old and SCOPE not in old
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);exists=key in parent;ops.append(dict(path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
        previous_scope=old[prior['unfinished_scope']];assert sha(Path(previous_scope['path']).read_bytes())==previous_scope['sha256']
        inventory=deepcopy(read(previous_scope['path']));inventory['next_focus']=NEXT
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,Path(__file__),*map(Path,PROOFS.values())]}
        pending=dict(status='Hodram28-source-context-prose-native-body-pages-reviewed-Gerhard-policy-sealed-both-registered-integrations-pending',
            all_proofs=PROOFS,Hodram_objects=28,Hodram_proposed_revisions=16,Hodram_proposed_retentions=12,Hodram_current_English_unconsulted=False,
            Hodram_native_body_pages=28,Hodram_compiled_alignment_cases=112,Hodram_all_formatting_gates_false=True,Hodram_new_actual_scene_runs=0,
            Hodram_pending_source_prose_drafts_not_yet_added_to_credited_counters=28,
            Gerhard_policy_actual_changing_rejections=260,Gerhard_independent_fullreference_sealed=True,
            Gerhard_independent_atomic_production_andcorruption_suite_pending=True,Gerhard_registered_name_asset_pending=True,
            H1_requires_explicit_registered_Adernkatz_dependency=True,registered_candidate=prior['candidate'],registered_candidate_sha256=prior['candidate_sha256'],
            full_goal_all_previous_unfinished_families_andlimits_preserved=True,new_credit=0,new_emulator_runs=0,new_ROMs=0,full_goal_complete=False,
            records=[{k:r[k] for k in ['id','file_path','block','source_reference','source_hex','source_Japanese','source_complete_preamble_hex','current_reference','current_hex',
                'effective_predecessor_template_hex','registered_catalogue_match','english','speaker','source_meaning','context','decision','localization_note','retention_reason','review']} for r in data['Hodram_manuscript']['records']])
        inventory[KEY]=deepcopy(pending);inventory[OLD_KEY]['superseded_by']=dict(checkpoint=KEY,Hodram_prose_andnative_body_pages_now_reviewed=True,Gerhard_frozen_policy_andreference_seal_now_pass=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,full_goal_complete=False))
        put([OLD_KEY,'superseded_by'],inventory[OLD_KEY]['superseded_by'])
        put(['latest_checkpoint'],SUMMARY+'\n'+NEXT)
        ops.append(dict(path=[KEY],existed=False,before=None))
        new[KEY]=dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=deepcopy(ops),goal_turn_classification='progress',all_sessions_terminal_andreaped=True)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V8249: Hodram28 contextual prose and native bodies; Gerhard policy/reference sealed\n\n'+SUMMARY+'\n'+NEXT+'\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V8249; V8172 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,unchanged_counters=list(AFTER),new_credit=0,full_goal_complete=False))
        print('V8249 progress staged for six targets;exact deep inverse audit pending.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),deep_inverse_recovers_every_previous_ledger_value=True,new_credit=0,full_goal_complete=False))
            print('Deep inverse passed;all previous ledger values,counters,candidate andscope recover exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_prior_values_reversible=True,new_credit=0,full_goal_complete=False))
            print('V8249 checkpoint applied;ROM,registry,counters andfullgoal preserved.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,new_credit=0,new_emulator_runs=0,new_actual_frames=0,new_research_ROMs=0,
                all_sessions_terminal_andreaped=True,all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            verified['Hodram_source_native_checkpoint'].update(current_dialogue_English_unconsulted=False,contextual_draft=str(PROOFS['Hodram_manuscript']),contextual_draft_sha256=sha(Path(PROOFS['Hodram_manuscript']).read_bytes()),
                proposed_revisions=16,individually_justified_retentions=12,native_body_pages=28,compiled_alignment_cases=112,all_formatting_gates_false=True,new_optional_scene_runs=0,
                stored_controls_actual4800_hide4700_andregistered_integration_pending=True,surname_registered_asset_pending=True)
            verified['Gerhard_surname_correction_checkpoint'].update(frozen_policy_passed=True,policy_expected_guard_rejections=260,independent_reference_seal=PROOFS['Gerhard_seal'],
                independent8phase_RAM_andreplay_recompute=PROOFS['Gerhard_risk_recompute'],independent_atomic_production_semantic_challenges_andregistered_release_pending=True)
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8250/currentV8172:28Hodram contextual drafts/nativebodypages;Gerhard frozenpolicy/seal;fullgoalactive andno newintegrationcredit.')
