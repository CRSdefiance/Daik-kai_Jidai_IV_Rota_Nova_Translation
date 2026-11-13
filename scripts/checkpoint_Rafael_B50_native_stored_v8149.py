"""Checkpoint reviewed B50 native/stored/control proofs without credit before actual registered release."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B49_v8127d import COUNTERS,AFTER
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_native_stored_checkpoint_v8149')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8150')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8128/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/rafael_B50_editorial_manuscript_v2.json')
NAMES=Path('translations/rafael_B50_speaker_name_review_v2.json')
KEY='Rafael_SC0B50_source_prose_native_stored_pending_actual_release_v8149'
OLD_KEY='Rafael_SC0B50_source_gloss_pending_controls_current_andrelease_v8127'
SCOPE='unfinished_editorial_scope_v8149'
PROOFS={'source': 'work/analysis/Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json', 'clean_names': 'work/analysis/Rafael_B50_clean_names_v8130/three_clean_static_identity_fields_before_current_English.json', 'first_gloss': 'work/analysis/Rafael_B50_clean_gloss_v8131/28_first_clean_glosses_three_source_identities_before_current_English.json', 'source_controls': 'work/analysis/Rafael_B50_source_controls_v8132/source_EV0_entry37_commands28_speeches_no_relative_predicate25_seeded_ends.json', 'source_macros': 'work/analysis/Rafael_B50_macros_names_v8133/three_clean_FA_FI_paragraphs12_fresh_alignments_six_exact_reused_name_getters.json', 'item': 'work/analysis/Rafael_B50_pigment_v8134/original4821_descriptor181_clean_current_Red_Dye_andbounded_consumer_path.json', 'callback_titles': 'work/analysis/Rafael_B50_context_v8135/complete13_clean_Lil_B131_dye_map_context_andfive_B44_title_refs.json', 'refined_gloss': 'work/analysis/Rafael_B50_context_v8135/28_refined_glosses_dye_identity_FA_FI_title_context_before_current_B50_English.json', 'names': 'work/analysis/Rafael_B50_names_current_v8136/three_static_speakers_six_reused_getters_three_reused_voices_exact_V8122_binding.json', 'current': 'work/analysis/Rafael_B50_current_v8136/all28_complete_source_current_refs_before_new_English_manuscript.json', 'effective': 'work/analysis/Rafael_B50_effective_v8137/all28_effective_English_templates56_original_dispatches_no_FE.json', 'prose': 'work/analysis/Rafael_B50_prose_v8138/28_contextual_decisions_one_complete_exchange_individual_revisions_retentions.json', 'logical': 'work/analysis/Rafael_B50_logical_v8139/28_logical_paragraphs112_original_native_alignments_no_FE.json', 'plan': 'work/analysis/Rafael_B50_layout_v8140b/28_automatic_plans_full_native_width_exact_source00_02_09_FA2_FI1.json', 'initial_native': 'work/analysis/Rafael_B50_pages_v8141/28_complete_native_paragraphs28_pages112_compiled_alignments.json', 'source_names': 'work/analysis/Rafael_B50_source_name_planes_v8142/28_complete_source_pages3_names0_fresh12_reused_literal_alignments.json', 'final_native': 'work/analysis/Rafael_B50_pages_refined_v8143/28_final_native_pages20_fresh92_reused_alignments.json', 'name_sheet': 'work/analysis/Rafael_B50_name_review_assets_v8144/review_sheet_receipt.json', 'native_review': 'work/analysis/Rafael_B50_native_review_v8145/28_native_pages3_names_two_scoped_warnings18_infos_wrap_review.json', 'branches': 'work/analysis/Rafael_B50_archive_tools_v8146/zero_source_current_relative_operands37_commands_nine_nontext_pairs.json', 'relocation': 'work/analysis/Rafael_B50_relocation_v8146/one_block28_speeches_zero_relative_cases_exact_full_inverse.json', 'stored': 'work/analysis/Rafael_B50_stored_v8147/all28_stored_bodies_full_native_alignment_and28_exact_viewed_pages.json', 'final_controls': 'work/analysis/Rafael_B50_relocated_controls_v8148/28_stored_dispatches_nine_controls_zero_relatives_relocated4821_25_seeded_ends.json'}
SUMMARY="Current registered cumulative ROM remains V8122; main V4701 is unchanged. Counts remain 7,143 completed, 7,146 source/prose records and drafts, 4,442 integrated revisions and 2,701 retentions. SC0 has 340 completed records; the route subset has 5,543. B49 is complete and credited once, with 638 manifest batches, 114 accepted layers, 18 release checks, 110 regressions, exact clean-input patch, full-reference equality and fresh own-current startup verified. B50 has no completion or source/prose credit and is not integrated.\n\nB50 has 28 complete contextual decisions: 13 revisions and 15 individually justified retentions in translations/rafael_B50_editorial_manuscript_v2.json. All four prose gates pass; all 28 formatting gates remain false pending stored/actual/reference/release completion. Stored and final controls are now separately verified. Names are translations/rafael_B50_speaker_name_review_v2.json: Rafael Castor, Lil Argot and approved Camille Overijssel retain individual clean-source reasons; Camille's Marinus remains in the full getter. No name asset or new biography is introduced.\n\nComplete clean B50 Japanese, three clean identities, all 28 first glosses, native source event entry/control/end checks and exact FA/FI source expansion preceded current English. The complete 13-speech clean Lil SC2 B131 callback explains Red Dye applied to parchment revealing a North Sea Proof of Conquest map. All 13 callback source records match their already completed review; no duplicate credit. All 117 prior opening source references are bound, with five exact title references: ship captain, fleet admiral and company leader are distinct source roles. The callback does not prove Rafael owns the parchment or has enacted Lil's route events. Event50/category5/action51 has no explicit prerequisite/exclusion list; outer eligibility and chronology are not inferred from B49/B50 numbering.\n\nThe review restores Rafael's awkward acknowledgment rather than an invented apology, Lil's map-deciphering aid, her dye reference and future nonuse, the tentative long-time-no-see reunion, her personal discovery of a life beyond money, and Rafael's promise to try rather than guarantee success. Source FA is the surname token (default Castor) in R40/R61; FI is the given-name token (Rafael) in R108. All three exact Japanese macro paragraphs pass 12 fresh native alignments; six identical name getters and three voices are bound to V8122 under unchanged code/font/fields and whole-actor/captain startup controls. No new Commander rank follows from the company-head address. Working banter, the private bluff, both thanks, departure and final unanswered celebration question remain. The occasion and preparations stay unnamed; do not invent marriage, romance, pregnancy, retirement or a new occupation.\n\nThe original4821 at source244 decodes to descriptor[0,181,1,5] and layout[2,0,1]. Clean item181 metadata names 紅色の顔料; its exact registered/current English is Red Dye. The original category0 index bounds and call to4A930 are bound, with unchanged clean/current code. The relocated request is identical under guarded native execution. The resource body, inventory-award semantics, full item-card geometry and natural event activation are not claimed executed. Preserve original A00000a0ffff0100b530,4720 and4681 rather than guessing a new mechanic or life event.\n\nFinal automatic layout is work/analysis/Rafael_B50_layout_v8140b/28_automatic_plans_full_native_width_exact_source00_02_09_FA2_FI1.json. Initial8140 is preserved. Five paragraphs improve within the same row/page counts and unchanged prose: R49 keeps it's been; R69 You're as; R103 no idea; R108 Come on; R114 keeps its thanks sentence and I'll do. Native width216px/four physical rows, fonts, global profile, body NUL guard and complete source00/02/09 preambles remain. Ten source00 objects have ten unique bodies. All source FA2/FI1 substitutions survive. All28 English paragraphs are complete single pages, with112 initial fresh alignments and20fresh/92exact reused final bindings. All28 clean Japanese pages and three complete style11 names pass. Header literal cases12 and the synthetic Camille full-getter4 cases are exact reuses with current raster equality, not fresh literal executions or actual catalogue UI.\n\nAll six final sheets were directly viewed: five body sheets and one name sheet. Ten total direct views include four superseded body sheets. All18 original line-break-count infos and two exact warnings remain: R61line1the/North, R114line2to/live. Each exception binds ID, source, logical English, compiled bytes, line, last/next words, exact issue and reason. R61 keeps North Sea complete in two rows. R114 keeps the complete effort/expectations phrase in three rows. No diagnostic is removed, global rule relaxed, word dropped or guard weakened. R37's remaining clause needs38text cells plus a continuation guard after its standalone greeting; R73's alternative remainder needs39plus1. Their ordinary complete-word boundaries retain fuller rows rather than inventing extra staging or shortening meaning. Broader weak-before-row/page-before-readability/phrase-coherence retrospective leads remain open.\n\nResearch archive work/analysis/Rafael_B50_relocation_v8146/SC0_B50_RESEARCH_ONLY.DK4 changes only B50: original/current1520stored/1518logical/tail2 becomes1376stored/1374logical/tail2, with full four-byte terminal at1370. All28 six-byte preambles,37commands and nine nontext controls remain. There are genuinely zero relative sites, raw predicates and completion queries; no branch-case execution is fabricated. Complete clean/predecessor block and whole predecessor archive inverses pass;342otherSC0blocks are exact. Fifteen parity tails have60fresh stored alignments;13exact bodies reuse52. All28 stored planes equal directly viewed pages, with no extra/blank page or lost glyph. All28 final actor/voice/body dispatches, nine opaque control maps, relocated4821 request and25seeded normal value-carry ends pass. Actual full scene/4720/4681 behavior, full-reference loaders/callers, frozen policy, atomic stage and registered integration remain pending. No new emulator frames or B50 ROM exist. All sessions terminal/reaped; preserve every artifact and the full editorial objective."
NEXT="Continue from verified V8150/current registered V8122. Use translations/rafael_B50_editorial_manuscript_v2.json and rafael_B50_speaker_name_review_v2.json. Final plan is8140b, not initial8140. Native8143 binds20fresh/92reused cases; source/name8142, viewed review8145, research relocation8146, stored8147 and final controls8148 pass. Reuse verified source/context/name/macro/prose/native/stored/inverse work unless a new change or concrete risk requires another check. B50 remains uncredited; all28 formatting gates are false.\n\nNext build and pin a full isolated research reference from V8122 plus the exact reviewed SC0 archive. Bind342otherblocks and everyotherfile/component, all343native load/cache paths and686parent modes, all37command maps/zero relative operands, originalEV0entry8 and shipped callers. Current own-Rafael input is work/analysis/current_V8122_Rafael_native_v8125/current_native_input.json; other-route contexts remain historical until rebound or recaptured. No natural event50/region/chronology claim follows from the opening snapshot.\n\nThen capture paired Japanese/English initialized full-scene fixtures after every original B44 initializer, retaining all37original B50commands/28speeches,4821,item picture,A000,4720,4681 andfullend. Do not force RAM,party,roster,roles,funds,seed,conditions or results, flatten or omit controls, or retime one language's ordinary input to hide differences. Use an adequate horizon for all28speeches, the picture transition and normalreturn;16001frames is a plausible starting horizon, not verified coverage or an assumed result. Focus on allthree complete names,FA surname/FI given-name text,actual RedDye picture/appearance/hide,4720 and final4681 transition, internal thoughts and normalvaluecarry. All source/English paragraphs are single-page; no invented multi-page turn is needed. Actual selection and full completion must be observed.\n\nMeasure complete glyph/page/name masks, exact selected command results/UIrequests and all timing/RNG/later component/calendar/RGB differences with honest limits. Source-only 4821 has its resource body explicitly unexecuted. Only then approve formatting, freeze source/prose/per-record capacity/two warning scopes, implement independent atomic production and meaningful precommit challenges, register after the completeV8122stack and build via build_integrated_release.py. Verify full-reference equality, exact clean-input patch, appropriate regressions and own-current startup before once-only credit. Expected639manifest batches/114accepted layers/mainV4701unchanged. Projected7171completed/7174source-prose-drafts/4455revisions/2716retentions,SC0368,route5571 are not current counts.\n\nKeep the full objective across allfourstorylines, earlier translated dialogue, sharedshop/town/random/Help/remainingprose, all207names/roles/aliases and retrospective premature wrapping. Preserve allpriorunfinishedinventories, twelvecontraction/question-tag leads, unscannedrecords beyond558plans and all inherited planner/item/counterpart/display leads. Keep Pasar distinct from Pasha; retain Cristina/Christina,HansRetzel/Letzel,Trader/PortWorker/Guildmaster,Sailor151-159 versusRetainer consumers,COMMON750-752,preLF6435,ArmadilloHide/SteelHide,HerophilusMedicine,AksumGoldSeal,AlShin/AlFeridShin,イギリス and everyrecorded lead. Keep graphics/all18plaques and the later older-record technical re-audit separate, including normal-end carry,source-onlyB35R65/B48R129nineteenth cells,B48stale relocation label,B47corrected registration receipt and every measured timing/highlight/RNG/component/calendar/RGB/fixture-reentry limit. Preserve all ROMs,translations,drafts,failures,executed producers andproofs. No separate unified package,promotion,pruning,commit orpush; full goal stays active."

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result
def gates():
    prior,doc,names=map(read,[PRIOR,DOC,NAMES]);data={k:read(p) for k,p in PROOFS.items()}
    assert prior['completed']==7143 and prior['manifest_batches']==638
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    assert len(doc['records'])==28 and doc['revised']==13 and doc['retained']==15
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert len(names['records'])==3 and all(r['native_name_plane_directly_viewed'] and not r['review']['formatting'] for r in names['records'])
    review=data['native_review'];assert review['native_page_count']==28 and len(review['all_original_infos'])==18 and len(review['narrow_warning_exceptions'])==2
    assert len(review['directly_viewed_sheets'])==6 and all(s['directly_viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in review['directly_viewed_sheets'])
    assert data['final_native']['plan_sha256']==sha(Path(PROOFS['plan']).read_bytes()) and data['final_native']['fresh_compiled_alignment_cases']==20 and data['final_native']['reused_compiled_alignment_cases']==92
    relocation=data['relocation'];assert relocation['relocated_native_skip_cases']==0 and len(relocation['groups'][0]['command_map'])==37 and not relocation['groups'][0]['relative_fixups']
    assert relocation['complete_clean_source_block_reconstructed_exactly'] and relocation['all_full_predecessor_archive_bytes_reconstructed_exactly']
    assert sha(Path(relocation['target_archive']).read_bytes())==relocation['target_archive_sha256']
    assert data['stored']['fresh_native_alignment_cases']==60 and data['stored']['exact_reused_native_alignment_cases']==52 and data['stored']['total_bound_alignment_cases']==112
    assert len(data['final_controls']['final_dispatches'])==28 and not data['final_controls']['relocated_predicates_andqueries'] and len(data['final_controls']['normal_seeded_ends'])==25 and len(data['final_controls']['original_nontext_control_maps'])==9
    assert data['item']['current_English']=='Red Dye' and data['source_macros']['fresh_source_macro_alignment_cases']==12
    assert len(data['callback_titles']['callback_records'])==13 and len(data['callback_titles']['five_clean_title_references'])==5
    return prior,data

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,data=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==AFTER
        assert old['goal_status']=='active' and not old['full_goal_complete'] and KEY not in old and SCOPE not in old and OLD_KEY in old
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);exists=key in parent
            ops.append(dict(path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
        previous_scope=old[prior['unfinished_scope']]
        assert sha(Path(previous_scope['path']).read_bytes())==previous_scope['sha256']
        inventory=deepcopy(read(previous_scope['path']));inventory['next_focus']=NEXT
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,DOC,NAMES,Path(__file__),*map(Path,PROOFS.values())]}
        pending=dict(status='28-source-context-prose-native-stored-approved-pending-fullreference-actual-policy-atomic-registered-release',
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
            file_path='/data/SC0.DK4',block=49,objects=28,revisions=13,retentions=15,current_English_unread=False,
            all28_final_formatting_gates_false=True,native_pages=28,source_commands=37,relative_sites=0,relocated_cases=0,
            final_plan=PROOFS['plan'],final_native=PROOFS['final_native'],viewed_final_sheets=6,
            original_QA_infos=18,exact_warning_exceptions=2,
            stored_fresh_alignment_cases=60,stored_exact_reused_alignment_cases=52,
            native_actual_B50_gameplay_runs=0,all_proofs=PROOFS,current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],
            new_credit=0,new_emulator_runs=0,full_goal_complete=False)
        inventory[KEY]=deepcopy(pending)
        if OLD_KEY in inventory:inventory[OLD_KEY]['superseded_by']=dict(checkpoint=KEY,native_pages_names_wrapping_stored_andcontrols_now_pass=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        put([OLD_KEY,'superseded_by'],dict(checkpoint=KEY,native_pages_names_wrapping_stored_andcontrols_now_pass=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        new[KEY]=dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',all_sessions_terminal_andreaped=True)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V8149: B50 complete native pages, names and stored reconstruction; actual/release pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V8149; V8122 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,unchanged_counters=list(AFTER),new_credit=0,full_goal_complete=False))
        print('B50 native/stored checkpoint staged;six targets,zero credit.Deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),
                deep_inverse_recovers_every_prior_root_family_record_counter_andcandidate=True,
                full_goal_all_prior_leads_andnew_native_stored_limits_preserved=True,new_credit=0,full_goal_complete=False))
            print('Deep inverse passes;every prior ledger value,candidate,count andunfinished lead recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_prior_values_reversible=True,new_credit=0,full_goal_complete=False))
            print('B50 native/stored checkpoint applied;currentV8122 andallcompletion counts unchanged.Full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
                previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,
                B50_native_pages=28,B50_names_native_planes=3,B50_final_viewed_sheets=6,
                B50_stored_fresh_alignment_cases=60,B50_stored_exact_reused_alignment_cases=52,
                B50_all37_commands_zero_relative_cases_full_inverses_pass=True,
                B50_actual_gameplay_runs=0,B50_native_font_layout_stored_actual_policy_atomic_registered_integration_pending=False,
                B50_fullreference_actual_policy_atomic_registered_integration_pending=True,
                new_credit=0,new_emulator_runs=0,new_actual_frames=0,all_sessions_terminal_andreaped=True,
                all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,
                producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8150/currentV8122:7143completed;B50 28decisions/28pages/three names/stored controls pass.Fullreference/actual/release pending.Full goal active.')
