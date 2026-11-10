"""Checkpoint36 unintegrated prose decisions and exact native proofs without credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_native_checkpoint_v7636')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7637')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7623/verified_handoff.json')
KEY='papal_trade_SC0_SC1_prose_native_pending_v7636'
SCOPE='unfinished_editorial_scope_v7636'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
VALUES=(6801,6804,6804,4251,2550)
IDENTITY=Path('work/analysis/papal_trade_route_identity_v7624/route_identity_correction_no_ROM_prose_reference_orcredit_change.json')
ROUTES=Path('work/analysis/papal_trade_route_native_v7626/two_own_current_route_contexts_actual_captains0_1_strict2b6.json')
CONSUMERS=Path('work/analysis/papal_trade_consumers_v7627b/two_routes36_effective_bodies72_dispatches_eight_getters.json')
ENTRY=Path('work/analysis/papal_trade_entries_v7628/original_EV0_EV1_events_actions_dependencies_andactual_route_getters.json')
NAMES=Path('translations/papal_trade_speaker_name_review_v1.json')
NAME_FONTS=Path('work/analysis/papal_trade_name_inputs_v7629/two_routes40_fresh_literal_alignments_five_exact_reused_font_planes.json')
CONTROLS=Path('work/analysis/papal_trade_controls_v7630/two_current_blocks50_fresh_seeded_ends_exact_effect_andclean_end_reuse.json')
PROSE=Path('work/analysis/papal_trade_prose_v7631/two_complete_exchanges36_decisions26_revisions10_justified_retentions_display_pending.json')
LOGICAL=Path('work/analysis/papal_trade_logical_inputs_v7633/all36_new_logical_bodies144_fresh_native_literal_IF_alignment_cases.json')
PLAN=Path('work/analysis/papal_trade_layout_v7632b/two_routes36_automatic_full_width_plans_all_base_QA_preserved.json')
NATIVE=Path('work/analysis/papal_trade_native_pages_v7634/two_routes36_complete_pages144_fresh_compiled_alignments_exact_logical_andfont_reuse.json')
VIEW=Path('work/analysis/papal_trade_native_review_v7635/all36_native_paragraphs_viewed_two_exact_R33_boundaries16_row_infos_stored_actual_pending.json')
SUMMARY="""V7611 remains the current experimental registered cumulative ROM: 626 batches, 114 accepted layers, 18 passing release checks, 110 release regressions and an exactly reconstructable clean-input patch. Completed counters remain 6801 completed, 6804 source-prose/drafts, 4251 revisions and 2550 retentions. SC2 4915 and routes 5201/5201 are subsets, not the full editorial denominator. The 36 new decisions below have no source-prose, integrated or completion credit yet. Main V4701 and every earlier ROM, translation, draft, producer, failure, trace and proof remain preserved.

Route-name correction: SC0 is Rafael, SC1 is Hodram, SC2 is Lil and SC3 is Maria. Earlier progress wording and the V7621 finding key incorrectly called SC1 Maria; exact SC0B246/SC1B237 references and source/current bytes were always correct. V7624 explicitly supersedes that metadata without changing prose, ROMs or credit. Maria's SC3 story remains in the full objective. Fresh ordinary V7611 New Games captured actual captains0/1 and character-selection/opening screens; they do not activate these optional encounters. Each route now has its own strict2b6 context in work/analysis/papal_trade_route_native_v7626/route0/current_native_input.json or route1/current_native_input.json. Never use the captain2 V7616 input for SC0/SC1 route catalogue, getters or macro checks.

Both complete clean exchanges and all36 file-qualified source/current references remain bound from V7619/V7620. Exact whole-block Japanese equality supports reuse of the earlier18 glosses before current English was read; these are not freshly authored glosses or English-derived source. Fresh72 original dispatches, 36 effective bodies, eight name getters and route catalogue masks1/2 confirm Carlo Sinat/Trader, selectors19/104, voices7/0 and zero original/current FI/FA/FO macros. Stored This man and Hodram's full-width F pass unchanged through the original processor: they are wording issues, not evidence of a parser cause or permission for a global I/F/font change. EV0 event246/action247 and EV1 event237/action238 have no completion prerequisites or exclusions; original outer eligibility, natural activation, location, earned progress and full effects remain unproved.

New whole-exchange natural-dialogue-v2 manuscripts are translations/rafael_B246_editorial_manuscript_v1.json and translations/hodram_B237_editorial_manuscript_v1.json. Each has13 proposed revisions and five individually justified retentions at R5/R12/R29/R47/R60: 26 revisions and10 retentions across36 uncredited speeches. Preserve distracted silence, familiar Carlo/Filippo banter, tentative unspecified recovery, being aboard the companions' ship, apology, explicit merchant great-grandfather, papal direct rule almost to Venice, donation competition, ancestral profits/decline/envy, reported occasional finds, prospective blessings, reflective divine aid and the explicitly conditional discovery. Restore lost facts and qualifiers without inventing kinship, ranks, nationality, a recovery cause, current city/date, modern historical corrections, lord-to-lord shipping routes, taxes/bribes, authentic holy relics, exact sites or guaranteed effects/rewards. Item106 remains unchanged and the body introduces no formal title, pope ordinal or biography.

Four contextual name retentions in translations/papal_trade_speaker_name_review_v1.json preserve Carlo Sinat and Trader for the two complete exchanges. Both route-specific original getters support these strings. 親父 does not prove Carlo's father; the separate European metadata is excluded from returned names and supplies neither surname nor approved nationality. Filippo is the source-bound spoken address at R9/R16, not a global shared actor104 relabel. Forty fresh route literal alignment cases reuse five exact native font planes by whole ARM9/COMMON/FNT and field/getter equality; zero fresh name-font renders are claimed. Optional counterpart headers and full catalogue UI remain unvisited. The broader207-name/role/alias review remains open.

All36 logical paragraphs pass144 fresh route-specific native literal I/F alignments, and compiled bodies pass another144 fresh alignments. Both routes use their own guarded profiles. All36 retain one original216x64/four-row page. Eighteen distinct native pages comprise six fresh renders and12 exact prior compiled-body/font/runtime reuse; the second route reuses those18 identical body/font inputs. All three native sheets were viewed. Complete first/internal/final glyphs, bounds, canaries, consumption, pair phase and guards pass. Sixteen informational row-count changes have individual reasons. The only warnings are the exact R33 line1 article-the continuations, one per file, preserving Papal States together; every base QA issue is retained and no global weak-ending rule changes. R16 keeps on your face whole. R5 retains three original CP932 ellipses; the generic offline index15 shade does not claim the counterpart's actual palette.

Both current1468/logical1468/tail0 blocks preserve20 commands,18 complete preambles, A0001456/raw00a0ffff6a000110 and the four-byte end1464. Fifty fresh current seeded ends pass;25 shared exact clean ends and two exact isolated A000 structural cases are reused. These do not prove item, blessing, ownership or reward mechanics. Preserve failed7627's inherited captain2 voice assertion, which stopped before speech checks, and its strict-route7627b successor; preserve the missing-dependency diagnostic imports and failed7632 default literal-F guard before plan output. The7632b successor uses the existing native-guard policy only after all144 fresh logical cases, with native constants and global defaults unchanged. None of these failures counts as a negative-control rejection. Stored-script/policy/relocation proofs, representative actual English scene testing and full registered integration remain pending; every new formatting gate remains false.

The full four-storyline, earlier translated dialogue, shared shop/town, random scene, Help, remaining player-facing prose, full207 names/roles/aliases and retrospective premature-wrap objective remains active. All previous completed history and unresolved leads remain. Graphics/all18 plaques and the later older-record technical re-audit stay separate. No separate unified test package, promotion, pruning, commit or push is performed."""
NEXT="""Continue from the36 complete prose decisions and reviewed native plans; do not repeat clean extraction, gloss reuse, route New Games, consumers, EV getters, literal ABI cases or unchanged native pages. Use the two actual-captain strict route inputs, never the Lil captain2 input. Freeze exact source/current/English/compiled bindings, all base QA and narrowly justified R33 boundaries; validate source-owned policy with actual-changing negative cases before any shared mutation. Map both complete current blocks for relocation, preserve every command/preamble/opaque operand/end/tail, prove exact inverse and unchanged unowned files, and validate final stored alignments and pagination. Plan representative disclosed original-initializer gameplay for the distinct SC0/SC1 entry/display and transitions, reusing exact source/font evidence honestly; no exhaustive conditional playthrough is required. Integrate only after necessary checks through the registered cumulative stack and exactly reconstructable clean-input patch, then own-ROM startup/native checks and grant36 source-prose/completion decisions once. Preserve all previous artifacts, the broad unfinished inventory, graphics separation and later older-record re-audit. No canceled test package, automatic promotion, pruning, commit or push."""

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
    assert native['fresh_compiled_alignment_cases']==144 and native['exact_reused_logical_alignment_cases']==144 and view['all_three_distinct_native_page_sheets_individually_viewed']
    assert read(CONSUMERS)['actual_original_captain_IDs']==[0,1] and read(IDENTITY)['correct_route_names']=={'SC0':'Rafael','SC1':'Hodram','SC2':'Lil','SC3':'Maria'}
    return prior,prose

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase;prior,prose=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256'];new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
            ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        scope=old['unfinished_editorial_scope_v7622'];assert sha(Path(scope['path']).read_bytes())==scope['sha256'];inventory=deepcopy(read(scope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(route_identity_correction=str(IDENTITY),prose_decisions=str(PROSE),native_review=str(VIEW),manuscripts=prose['manuscripts'],file_qualified_positions=36,proposed_revisions=26,proposed_retentions=10,source_prose_or_completion_credit_added=0,stored_actual_policy_reference_andrelease_pending=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
        ROOT.mkdir(parents=True);inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
        put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),all_broader_objective_andprior_leads_preserved=True,SC0_Rafael_B246_SC1_Hodram_B237_36_prose_decisions_native_reviewed_uncredited=True,full_goal_complete=False))
        put(['formatting_watchlist','papal_trade_SC0_SC1_v7636'],dict(status='prose-native-reviewed-stored-actual-policy-release-pending',native_review=str(VIEW),exact_R33_article_boundary_each_file_no_global_rule_change=True,all_formatting_gates_false=True,no_new_credit=True))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
        assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5201;put(['coverage_units',ri,'next'],NEXT)
        paths=[IDENTITY,ROUTES,CONSUMERS,ENTRY,NAMES,NAME_FONTS,CONTROLS,PROSE,LOGICAL,PLAN,NATIVE,VIEW,PRIOR,inv,Path('translations/release_stack.json'),Path(__file__)]
        evidence={str(p):sha(p.read_bytes()) for p in paths}
        new[KEY]=dict(records=deepcopy(prose['records']),file_qualified_source_current_refs=36,proposed_revisions=26,proposed_retentions=10,reviewed_names=str(NAMES),native_review=str(VIEW),source_prose_or_completion_credit_added=0,new_source_prose_reviews=0,new_completed_records=0,new_revisions=0,new_retentions=0,current_ROM_families_all_five_credit_counters_andprior_records_unchanged=True,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['completed_editorial_families']==old['completed_editorial_families']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V7636: Rafael B246 / Hodram B237 prose and native review; stored/actual/release pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            p=Path('docs')/name;prefix=('# Current editorial handoff - V7636; V7611 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[p]=prefix.replace('\n','\r\n').encode()+p.read_bytes()
        files=[]
        for i,(p,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if p!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0))
            files.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,zero_credit=True,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six-target36-decision native/prose checkpoint staged; zero credit, V7611/families/counters unchanged.')
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
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),all_prior_roots_records_families_counters_andROM_refs_recover_exactly=True,correct_SC0_Rafael_SC1_Hodram_route_identity=True,SC0B246_SC1B237_36_uncredited_prose_decisions26_revisions10_retentions=True,own_route_captain0_1_strict_native_contexts_bound=True,new36_logical_andcompiled_native_alignments288=True,all18_distinct_native_pages_viewed_six_fresh12_exact_reuse=True,stored_actual_policy_reference_andregistered_integration_pending=True,all_new_formatting_gates_false=True,new_credit=0,pending_checkpoint=str(ROOT/'application_receipt.json'),full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            verified['historical_V7622_pending_consumers_flag_superseded']=verified.pop('current_raw_wording_findings_effective_runtime_prose_entry_names_native_actual_release_pending',None)
            save(VERIFY/'verified_handoff.json',verified)
            print('V7636 verified:36 prose/native decisions pending stored/actual/release; V7611/6801 completed unchanged. Full goal active.')
