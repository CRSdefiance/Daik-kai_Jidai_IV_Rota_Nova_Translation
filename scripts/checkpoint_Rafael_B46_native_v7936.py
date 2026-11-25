"""Reversibly checkpoint complete B46 contextual/native progress; no new completion credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B45_v7916 import COUNTERS,AFTER
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_native_checkpoint_v7936')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7937')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7924/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
SOURCE=Path('work/analysis/Rafael_next_clean_v7918/complete_clean_SC0_B46_EV0_andcoverage_before_current_English.json')
CONTEXT=Path('work/analysis/Rafael_B46_clean_context_v7919/complete_clean_SC0_B38_EV0_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Rafael_B46_branch_gloss_v7926/24_speeches2_choices_fresh_branch_context_before_current_English.json')
NAMES=Path('work/analysis/Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json')
CONTROLS=Path('work/analysis/Rafael_B46_source_controls_v7922/source_EV0_entry_four_relative_sites20_cases25_seeded_ends_menu_scope.json')
CURRENT=Path('work/analysis/Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B46_effective_v7928/all24_effective_English_templates48_original_dispatches12_FE.json')
MANUSCRIPT=Path('translations/rafael_B46_editorial_manuscript_v2.json')
NATIVE_REVIEW=Path('work/analysis/Rafael_B46_native_review_v7935/24_pages2_choices_full_native_review_individual_wrap_reasons.json')

KEY='Rafael_SC0B46_contextual_native_pending_stored_actual_release_v7936'
SCOPE='unfinished_editorial_scope_v7936'
SUMMARY="The current registered cumulative ROM remains V7911: 633 batches, 114 accepted layers, 18 passing release checks and 110 regressions. Its reviewed-reference equality and exact clean-input patch reconstruction remain verified. Main V4701 is unchanged. Counts remain 6,950 completed, 6,953 source/prose records and drafts, 4,354 integrated wording revisions and 2,596 retentions. Rafael B45 is complete; reuse its proofs and retain its measured one-step RNG difference and all timing limits.\n\nRafael SC0 B46 now has a complete contextual English draft at translations/rafael_B46_editorial_manuscript_v2.json: 24 speeches, including twelve FE panels, and two menu choices. Seven wordings are revised and nineteen retained with individual reasons. Fresh clean-Japanese glosses, complete B38 context and the corrected conditional context preceded current English. Accepting the lesson leads through 22 speeches, including the tutorial and thanks. Declining leads through seven speeches, including Julio's caution and Rafael's acknowledgment. Both paths end with the unfinished private thought; their union is 24 distinct speech objects.\n\nThe source menu forwards bridged selections 0/1 as native state 2 and value 0/1. Combining these with four measured relative sites establishes the expected paths offline; it does not prove actual controller selection or complete interpreter execution. All 48 source/current speech dispatches bind 24 effective English templates with zero catalogue replacements. Both current menu labels pass native getters and widths. Replacing the 25 prose containers exactly recovers the entire clean 1,696-byte B46 block. Five A000 operands, four relative headers, 6300, 61FF and the normal end remain exact. Seven source/current opaque-command pairs pass fourteen structural cases; their effects remain bridged. Earlier twenty relative cases and twenty-five seeded normal ends remain valid offline evidence.\n\nThe revisions clarify Rafael's quiet assent, Julio's offer and introduction, possible coastal discoveries, land inside the search frame, the decline response and the unfinished American-English aside. All Y/L/R/A instructions, opposite mode orders, icons, targets and conditional context remain. No kinship, rank, alliance, guaranteed discovery or specific future ambition is added. Six original getters support Rafael Castor, Claudio Manaus and Julio Erneco, with voices 2/4/5. Hayreddin is bound only to the clean/current ハイレディン component. The wider 207-name review remains open.\n\nAll 24 compiled speeches pass 96 original native alignments, complete glyph-plane comparisons, bounds, consumption and single-page pagination. Twelve progressive pages use 216x64; twelve FE pages use the original 228x48 logical/228x64 physical bitmap with 216px usable text. The four actor-00 preambles remain separate from the unchanged body-NUL guard. All four page sheets were directly viewed. Fourteen original row-count infos have individual reasons, with no warnings or waivers. The warning's only feasible two-row split ends after may, so its three-row layout deliberately keeps may challenge together without narrowing the viewport.\n\nThe choice wordings remain Please do. and No, thanks. Removing storage-only spaces lets the native constructor reduce caption width from 84 to 66px and the menu object from 36 to 30 bytes. Eight current/target black/gray style planes pass full independent glyph, backing-model and canary checks under exact current instructions and the 123,264-byte staged payload. The fifth sheet was directly viewed. This is an offline test using the historical 256x36 backing model; actual B46 backing, views, highlights and input remain unobserved.\n\nB46 has no completion credit or ROM change yet. All 26 formatting gates remain false pending stored/control/reference/actual checks. Relocation, inverses, loaders/callers, representative source/English acceptance and decline tests, actual menu backing, transitions and normal returns, measured timing/RNG limits, frozen policy, atomic production and registered release remain pending. Keep the full four-storyline, earlier-dialogue, shop/town/random, Help, remaining-prose, names and wrap objective active. Preserve every ROM, translation, draft and executed or failing producer. Graphics and all 18 plaques, and the later older-record technical re-audit, remain separate. No separate package, promotion, pruning, commit or push."
NEXT="Continue from verified V7937 and current V7911 using translations/rafael_B46_editorial_manuscript_v2.json. Current B46 English has now been read. Reuse the 26 contextual decisions, 24 native pages, 96 compiled alignments, eight choice style planes, five viewed sheets and individual wrap reasons. Earlier source packets' unread flags describe their historical moment. Source/current dispatches, names, menu-provider semantics and relative/seeded-end proofs do not need unnecessary repetition.\n\nNext relocate the complete B46 block, preserving all 24 six-byte speech preambles, the 30-byte two-choice object, five A000 commands, 6300, 61FF and four relative/nested spans. Check exact stored bodies and parity, complete clean/predecessor block inverses and the full predecessor archive inverse. Keep all 342 other SC0 blocks and every other file/component unchanged; verify native loads, cache behavior and caller bounds. The original constructor must calculate the 66px caption width. Do not force backing dimensions, positions or padding. Preserve the ordinary embedded-NUL guard and handle the four source-00 preambles separately.\n\nUse representative full source/English entry fixtures and ordinary choices for both distinct paths. Acceptance includes 22 speeches, twelve FE panels, the understanding check and thanks; decline includes seven speeches, caution and acknowledgment. Their union is 24 distinct speeches plus two choices. Check actual menu backing/views/highlights, complete source/English body/name/FE planes, transitions and unforced normal-end value carry. Measure timing, RNG, components and later RGB differences honestly. Exhaustive natural activation or full-route playthroughs are not required. Preserve all five A000 setup commands; structural bridges do not prove full effects. Use work/analysis/current_V7911_Rafael_native_v7914/current_native_input.json for Rafael's own current context.\n\nAfter necessary checks pass, freeze a source-bound natural-dialogue-v2 policy and atomic compiler, challenge actual changing inputs before commit, integrate after the complete V7911 stack with the registered builder, and verify exact clean-input patch reconstruction and appropriate startup. Credit 26 records, seven revisions and nineteen retentions only after registered integration. Current counts remain 6950/6953/4354/2596.\n\nKeep all four storylines, earlier translations, broad practical town/shop/random capture, Help and remaining prose, all 207 names/roles/aliases, twelve retrospective wrap leads and unscanned records beyond the 558-plan heuristic active. Preserve every earlier unfinished inventory, item/counterpart/display lead, Sailor151-159 versus Retainer consumers, normal-end value carry and B35 R65's source-only nineteenth cell. Lil V7857 and Maria V7821 contexts remain historical; obtain each route's own current context when needed. Graphics/all 18 plaques and the later older-record technical re-audit stay separate. Preserve every ROM and earlier translation. Main V4701 stays unchanged; no separate package, promotion, pruning, commit or push."

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result

def gates():
    prior,doc,review,effective=map(read,[PRIOR,MANUSCRIPT,NATIVE_REVIEW,EFFECTIVE])
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256'] and prior['completed']==6950
    assert prior['manifest_batches']==633 and prior['Rafael_B45_completed_once']
    assert len(doc['records'])==24 and len(doc['typed_choice_records'])==2 and doc['revisions']==7 and doc['retentions']==19
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records']+doc['typed_choice_records'])
    assert review['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and review['native_page_count']==24 and review['compiled_alignment_cases']==96
    assert review['native_choice_style_planes']==8 and len(review['directly_viewed_sheets'])==5 and all(s['directly_viewed'] for s in review['directly_viewed_sheets'])
    assert review['row_count_infos']==14 and review['actual_B46_gameplay_coverage']==0
    assert len(effective['source_current_dispatches'])==48 and len(effective['effective_current_records'])==24
    assert effective['source_packet_sha256']==sha(CURRENT.read_bytes())
    assert all(not r['current_English_body_unread'] for r in read(CURRENT)['records']+read(CURRENT)['typed_choice_records'])
    assert read(SOURCE)['groups'][0]['completed_coverage_overlap']==0
    return prior

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior=gates()
    if mode=='stage':
        assert not ROOT.exists()
        before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and KEY not in old and tuple(old[k] for k in COUNTERS)==AFTER
        assert old['goal_status']=='active' and not old['full_goal_complete']
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
            ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        oldscope=old['unfinished_editorial_scope_v7923'];assert sha(Path(oldscope['path']).read_bytes())==oldscope['sha256']
        inventory=deepcopy(read(oldscope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(source_gloss=str(GLOSS),names=str(NAMES),controls=str(CONTROLS),source_speeches=24,source_choices=2,
            current_English_unread=False,new_credit=0,all_prior_inventories_andfull_scope_preserved=True)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_andfull_scope_preserved=True,new_credit=0,full_goal_complete=False))
        put(['formatting_watchlist',KEY],dict(source_gloss=str(GLOSS),names=str(NAMES),controls=str(CONTROLS),
            source_context_prose_names_compiled_pages_choices_checked_stored_actual_policy_release_pending=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
        put(['coverage_units',ri,'next'],NEXT)
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,SOURCE,CONTEXT,GLOSS,NAMES,CONTROLS,scope,Path(__file__),
            Path('work/analysis/Rafael_B46_gloss_tools_v7920b/source_locked_derivation.json'),CURRENT,EFFECTIVE,MANUSCRIPT,NATIVE_REVIEW]}
        new[KEY]=dict(summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,source_gloss=str(GLOSS),
            source_speeches=24,source_choices=2,source_FE_panels=12,current_English_unread=False,new_credit=0,manuscript=str(MANUSCRIPT),native_review=str(NATIVE_REVIEW),proposed_revisions=7,proposed_retentions=19,compiled_native_pages=24,compiled_alignments=96,choice_native_style_planes=8,five_sheets_directly_viewed=True,
            new_emulator_runs=0,native_name_getters=6,native_macro_alignments=12,isolated_native_relative_cases=20,seeded_normal_ends=25,
            all_prior_completed_records_counts_ROM_references_andfull_scope_preserved=True,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['completed_editorial_families']==old['completed_editorial_families']
        assert new['current_integrated_candidate']==old['current_integrated_candidate'] and tuple(new[k] for k in COUNTERS)==AFTER
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        targets={LEDGER:encode_ledger(new)}
        section='## V7936: Rafael B46 contextual/native pages andchoices reviewed; stored/actual/release pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V7936; V7911 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        protected=[Path(prior['candidate']),Path(prior['patch']),Path('translations/release_stack.json'),Path('translations/rom_retention_pins.json')]
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,protected={str(p):sha(p.read_bytes()) for p in protected},new_credit=0,full_goal_complete=False))
        print('Six contextual/native progress targets staged;26 decisions/seven revisions19 retentions/24 pages/eight choice planes. No credit.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in (plan['evidence']|plan['protected']).items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),deep_inverse_all_prior_values_exact=True,new_credit=0,full_goal_complete=False))
            print('Deep inverse/six hashes/all evidence pass. Prior completed coverage and ROM preserved.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists()
            assert read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            workspace=Path.cwd().resolve()
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(workspace) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,no_ROM_orcredit_change=True,full_goal_complete=False))
            print('Six audited contextual/native checkpoint targets applied;V7911/6950 completed unchanged.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_hash_exact']
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
                previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),Rafael_B46_source_speeches=24,Rafael_B46_source_choices=2,
                Rafael_B46_source_FE_panels=12,Rafael_B46_current_English_unread=False,Rafael_B46_native_menu_owner_actual_andrelease_pending=True,Rafael_B46_contextual_native24_pages2_choices_reviewed=True,pending_Rafael_manuscript=str(MANUSCRIPT),pending_Rafael_manuscript_sha256=sha(MANUSCRIPT.read_bytes()),pending_Rafael_native_review=str(NATIVE_REVIEW),
                pending_Rafael_source_gloss=str(GLOSS),pending_Rafael_source_gloss_sha256=sha(GLOSS.read_bytes()),
                pending_Rafael_names=str(NAMES),pending_Rafael_source_controls=str(CONTROLS),
                unfinished_scope=SCOPE,next_required=NEXT,latest_checkpoint=KEY,new_credit=0,new_emulator_runs=0,new_actual_frames=0,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV7937/currentV7911:26 decisions/seven revisions19 retentions/24 native pages/eight choice planes;stored/actual/release pending,no credit.Full goal active.')
