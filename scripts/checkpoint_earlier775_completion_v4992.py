"""Losslessly record the integrated retrospective correction with zero duplicate credit."""
from pathlib import Path
from copy import deepcopy
import argparse,gzip,json,os
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch import earlier775_reflow_v1 as owned
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.duel_editorial import owned_entries
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from scripts.checkpoint_lil_B182_references_v4910 import WIDER

ROOT=Path('work/analysis/earlier775_completion_v4992')
VERIFY=Path('work/analysis/editorial_handoff_verification_v4993')
KEY='earlier_COMMON_wraps_completion_v4992'
PREVIOUS='previous_latest_checkpoint_before_earlier775_completion_v4992'
PARENT_KEY='previous_integrated_candidate_before_earlier775_completion_v4992'
SCOPE_KEY='unfinished_editorial_scope_v4992'
FINAL=Path('translations/earlier_common_wraps_contextual_final_review_v1.json')
DOC=Path('translations/earlier_common_wraps_editorial_manuscript_v2.json')
RELEASE=Path('work/analysis/earlier775_release_v4988/registered_release_verification.json')
START=Path('work/analysis/earlier775_startup_v4990/cold_boot_Lil_startup_town_verification.json')
VIEW=START.parent/'current_six_frame_visual_review.json'
ACTUAL=Path('work/analysis/recommendation_actual_verification_v4985/viewed_original_reward_transition_approval.json')
REG=Path('work/analysis/earlier775_registration_v4986/registration_receipt.json')
MARIA=Path('work/analysis/maria_B97_clean_glosses_v4996/all32_clean_exchange_and_fresh_glosses.json')
NEXT=(
    'Continue canonical Maria SC3 B97 from fresh clean-only full inventory4995 and32 whole-exchange glosses4996 before consulting predecessor English. '
    'The exchange moves from whispers and identification of the Sao Jorge raiders through a livelihood complaint,the village\'s devastation,slave trading and military plunder,to a challenge against indiscriminate revenge,a political alternative,the invitation,voluntary trust,welcome and tentative ruins/tablet handover. '
    'Preserve the seriousness of the grievance and atrocities;keep moral judgments,political aims and confidence as character statements. Do not invent historical absolution,casualties,perpetrators,kinship,ranks or a promised retaliatory act. '
    'Bind03/0A/B4 native names and voices,one impersonal FE,FO faction,approved Sao Jorge alias and Proof terminology. Do not infer speaker identity from another route or reuse donor captain1 as a Maria-story source selector. '
    'Map all40 source commands/32 complete preambles,leading6000/4620/633E,two A000s at1750/1888,4820 at1884,4700 at1896,and end1898 with1904 stored bytes. '
    'Do not inherit B183 linear/no-presentation assumptions or guess effect semantics,dependency prefixes or earned recruitment/artifact state. These32 source leads remain uncredited. '
    'Retrospective COMMON682/764/774 decisions and775 reflow are complete in V4987;do not repeat their passed checks without a concrete risk or add duplicate credit. '
    'Continue analogous earlier wrapping and every remaining storyline/shared exchange/random scene/Help/player prose. '+WIDER)
SUMMARY=(
    'V4992 completes the four retrospective COMMON682/764/774/775 decisions in registered cumulative V4987 without adding editorial credit. '
    'All four wordings are individually justified retentions.682 retains its coherent of my worries phrase;764 retains its complete opening sentence.774 still requires four complete-word rows at validated widths,and its existing noun phrase/thanks boundaries are better than the prototype. '
    'Only775 changes,from four rows to three:And I\'ll write you a letter / of recommendation to thank you for / selling us so many popular goods. Two generated terminal spaces preserve its exact105-byte allocation/NUL. '
    'The complete-word for ending is a scoped ordinary soft wrap;no authored breaks,padding,width,font,metric,guard,runtime filter or historical compiler changes. '
    'Eight complete native planes,14 formatter negatives,all7336 native warm/cold copies and ten cache sequences pass. All3668 selection/record/NUL boundaries and every other COMMON payload remain exact;inverse reconstruction restores the whole predecessor COMMON.\n\n'
    'Two12001-frame paired cold boots actually show original775->780->766 and normal Istanbul town/Port return. Six complete held text planes and all10 full paired screens were viewed. '
    'Source font calls at6023/6424/6827 and all seven measured font events agree in timing.74 nontext samples,all sampled post-farewell whole RGB,final RGB,five native state groups,whole1A04 actor,actual donor captain1 and PRNG260148687 agree. '
    'No causal PRNG,future-world or full-RAM equivalence claim. The stock fixture changes only eight owned cargo-ID,demand and company/share80 bytes at3200. '
    'One declared original-BBCA4 fixture supplies qualification2,reward quantity16 and bonus1,with exact CPU/WRAM/DTCM/ITCM ownership checks. The real sale contains two holds;no actual cargo quantity,code,PC,RNG or cash is written by that fixture. '
    'Source code,portraits and effect bodies remain intact;no earned inventory,share,large sale,qualification or recommendation claim. Source/disposable donor handling stays isolated and the original donor is unchanged. '
    'The stopped navigation-schedule assertion and donor-captain2 assumption are preserved;passing successors bind the original navigation API and measured captain1. '
    'Two current V4987 New Game4001 and inherited-battery town17401 cold boots match V4966 across31 whole frames and five actor/captain controls. Four new cold boots total45404 frames. No full-route or hardware claim.\n\n'
    'The atomic stage rejects42 meaningful negatives before mutation;78 release/dialogue regressions and18 cumulative checks pass. V4987 retains the complete V4966 stack:566 manifest batches/114 accepted layers. '
    'Only COMMON775 bytes change from V4966;all stories,other messages,fonts,graphics,ARM9/ARM7,staged123040 bytes and components remain exact. The candidate equals the reviewed one-message reference and exact clean-input patch reconstruction. '
    'Main V4701 and immutable canonical inputs are preserved. All generated ROMs and earlier translations remain retained.\n\n'
    'Coverage remains5966 completed contextual rereads,5969 source/prose,3780 integrated revisions/2186 retentions,SC24113 and route4367/4367,with zero pending credited route drafts. '
    'The four entries were already credited;this formatting revisit adds zero duplicate credit. Maria B97 has32 fresh clean-only glosses across40 commands and zero credit;all contextual/native/localization/actual/release gates remain. Full goal active.\n\n')

def gates(entry,candidate):
    for p,h in entry['evidence'].items():assert sha(Path(p).read_bytes())==h
    release,start,view,actual,reg=map(read,[RELEASE,START,VIEW,ACTUAL,REG])
    assert sha(Path(release['candidate']).read_bytes())==candidate['sha256']==release['candidate_sha256']==start['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert release['whole_ROM_reconstruction_byte_exact'] and release['only_COMMON775_bytes_change'] and release['all566_manifest_batches_and114_accepted_layers_present']
    assert Path(release['candidate']).read_bytes()==Path(release['exact_patch_reconstruction']).read_bytes()==Path('out/recommendation775_reference_v4983_RESEARCH_ONLY.nds').read_bytes()
    assert start['all_current_requested_and_final_framebuffers_equal_V4966'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and sha(Path(view['sheet']).read_bytes())==view['sha256']==start['review_sheet_sha256']
    assert actual['ten_full_screens_viewed'] and not actual['visual_review_pending'] and actual['actual_original_reward_sequence']==[775,780,766]
    assert actual['nontext_equal_samples']==74 and not actual['nontext_differences'] and actual['whole_final_RGB_equal']
    assert actual['versions'][0]['all_font_rows']==actual['versions'][1]['all_font_rows']
    assert all(actual['native_final_component_equality'].values()) and actual['whole_actor_and_actual_captain_equal']
    assert actual['actual_donor_captain_IDs']==[1,1] and actual['PRNG_seeds']==[260148687,260148687] and actual['PRNG_equal']
    assert reg['negative_count']==42 and reg['all_negatives_reject_before_mutation']
    tests=read('work/analysis/earlier775_release_tools_v4987/regression_test_results.json');assert tests['returncode']==0 and '78 passed' in tests['stdout']
    conf=read(owned.CONFIG);image=NdsImage.open(candidate['path']);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');parent=NdsImage.open(reg['parent_ROM'])
    stage=owned.apply_release(parent,baseline);assert stage==release['stage'] and parent.read_file(owned.PATH)==image.read_file(owned.PATH)
    final,doc=read(FINAL),read(DOC);assert len(final['records'])==4 and final['new_editorial_credit']==0
    entries=owned_entries(image.read_file(owned.PATH),image.read_file('/__arm9__.bin'),conf['directory_sha256'])
    clean=NdsImage.open('work/clean.nds');jp=common_message_entries(clean.read_file(owned.PATH),clean.read_file('/__arm9__.bin'))
    for row,old in zip(final['records'],doc['records'],strict=True):
        n=row['message_id'];assert row['english']==old['english'] and row['source_hex']==jp[n].text.hex()
        assert row['current_hex']==row['integrated_hex']==entries[n].text.hex()==old['target_hex'] and row['historical_pre_reflow_current_fields']['current_hex']==old['current_hex']
        assert all(row['review'].values()) and row['fresh_retained_wording_justification'] and row['layout_review_reason']
        assert row['actual_recommendation_branch_observed']==(n==775)
    manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert len(manifest['batches'])==566 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    maria=read(MARIA);assert len(maria['records'])==32 and maria['source_commands']==40 and maria['read_no_predecessor_English'] and maria['new_source_prose_or_completion_credit']==0

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['stage','audit','apply','post'],required=True);mode=p.parse_args().mode
    lp=Path('translations/editorial_review_current_v1.json')
    if mode=='stage':
        assert not ROOT.exists() and not FINAL.exists();before=lp.read_bytes();old=json.loads(before)
        assert sha(before)==read('work/analysis/editorial_handoff_verification_v4982/verified_handoff.json')['ledger_sha256']
        assert all(k not in old for k in [KEY,PREVIOUS,PARENT_KEY,SCOPE_KEY])
        release=read(RELEASE);doc=read(DOC);image=NdsImage.open(release['candidate']);conf=read(owned.CONFIG)
        entries=owned_entries(image.read_file(owned.PATH),image.read_file('/__arm9__.bin'),conf['directory_sha256'])
        rows=deepcopy(doc['records'])
        for r in rows:
            e=entries[r['message_id']];ref=dict(message_ID=e.message_id,block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text),record_index=e.record_index,table_offset=e.table_offset,start_in_record=e.start)
            r['historical_pre_reflow_current_fields']={k:deepcopy(r[k]) for k in ['current_reference','current_hex','native_cases']}
            r.update(current_reference=ref,current_hex=e.text.hex(),integrated_reference=ref,integrated_hex=e.text.hex(),
                completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],
                native_cases_are_frozen_pre_reflow_proofs=True,status='complete-retrospective-context-native-representative-and-registered-release',new_editorial_credit=0)
        paths=[DOC,RELEASE,START,VIEW,ACTUAL,REG,MARIA,Path(__file__),Path('work/analysis/earlier775_retention_v4991/pin_receipt.json'),Path('work/analysis/earlier775_release_tools_v4987/regression_test_results.json')]
        evidence={str(p):sha(p.read_bytes()) for p in paths};summary=SUMMARY+'Candidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
        ROOT.mkdir(parents=True);save(FINAL,dict(format='dk4-contextual-formatting-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=rows,changed_message_IDs=[775],retained_exact_layout_IDs=[682,764,774],
            all_wordings_retained=True,new_editorial_credit=0,candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],actual_scope=read(ACTUAL)['visual_review'],
            evidence=evidence,summary=summary,full_goal_complete=False))
        current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
            patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
        current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
        new=deepcopy(old);new[PARENT_KEY]=old['current_integrated_candidate'];new['current_integrated_candidate']=current;new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=summary
        new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),records=rows,evidence=evidence,
            source_prose_or_completion_credit_added=0,new_emulator_runs=4,total_new_frames=45404,retained_exact_layout_IDs=[682,764,774],integrated_reflow_IDs=[775],
            prior_native_checkpoint_resolved='earlier_COMMON_wraps_context_native_v4981',goal_turn_classification='progress',full_goal_complete=False)
        inventory=deepcopy(read(old['unfinished_editorial_scope_v4971']['path']));inventory['next_focus']=NEXT
        inventory['historical_earlier_wrap_leads_before_v4992']=inventory.get('next_earlier_wrap_revisit_leads',[682,764,774,775])
        inventory['earlier_COMMON_wraps_completed_v4992']=dict(final_review=str(FINAL),changed_IDs=[775],retained_exact_layout_IDs=[682,764,774],new_editorial_credit=0)
        inventory['fresh_canonical_Maria_B97_clean_v4996']=dict(path=str(MARIA),sha256=sha(MARIA.read_bytes()),records=32,commands=40,read_no_predecessor_English=True,new_editorial_credit=0)
        inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
        new[SCOPE_KEY]=dict(path=str(inv),sha256=sha(inv.read_bytes()),canonical_Maria_B97_records_uncredited=32,incomplete_COMMON=3,incomplete_route_source_prose=0,
            earlier775_reflow_integrated=True,earlier682_764_774_layout_retentions_complete=True,broader_earlier_wrapping_open=True,
            all_storylines_shared_town_shop_random_help_other_player_prose_open=True,separate_graphics_and_older_record_technical_reaudit_open=True,full_goal_complete=False)
        new['formatting_watchlist']['earlier775_v4992']=dict(status='complete-retrospective-context-native-representative-registered-release',final_review=str(FINAL),new_editorial_credit=0)
        gates(new[KEY],current)
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={lp:encode_ledger(new)}
        section='## V4992:retrospective wrapping correction integrated in cumulative V4987;full goal active\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            q=Path('docs')/name;text=q.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V4992\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest
            targets[q]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            assert target!=lp or len(data)<100*1024*1024
            staged=ROOT/f'{i:02d}.after';staged.write_bytes(data)
            if target!=lp:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),staged=str(staged.resolve()),after_sha256=sha(data)))
        save(ROOT/'mutation_plan.json',dict(files=files,all_original_history_and_counters_preserved=True,full_goal_complete=False))
        print('Staged six completion files;V4987 one-message reflow,three layout retentions,Maria32 fresh source leads,zero duplicate credit.');raise SystemExit(0)
    plan=read(ROOT/'mutation_plan.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));row=plan['files'][0];new=read(row['staged'])
    inverse=deepcopy(new);inverse['current_integrated_candidate']=inverse.pop(PARENT_KEY);inverse['latest_checkpoint']=inverse.pop(PREVIOUS);entry=inverse.pop(KEY);inverse.pop(SCOPE_KEY);inverse['formatting_watchlist'].pop('earlier775_v4992');assert inverse==old
    assert new['goal_status']=='active' and not new['full_goal_complete'] and new['completed_editorial_families']==old['completed_editorial_families']
    assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5966,5969,3780,2186)
    assert Path(row['staged']).read_bytes()==encode_ledger(new)
    for r in plan['files']:
        assert sha(Path(r['staged']).read_bytes())==r['after_sha256'] and sha(Path(r['target']).read_bytes())==r['after_sha256' if mode=='post' else 'before_sha256']
    gates(entry,new['current_integrated_candidate']);VERIFY.mkdir(parents=True,exist_ok=True)
    candidate=new['current_integrated_candidate'];receipt=dict(ledger_sha256=row['after_sha256'],candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,completed=5966,source_prose=5969,revised=3780,retained=2186,
        registered_reflow_IDs=[775],retained_exact_layout_IDs=[682,764,774],all566_manifest_entries114_accepted18_checks_verified=True,
        all_actual_reward_transition_and_disclosed_fixture_ownership_checks_verified=True,all31_current_startup_frames_and_five_actor_controls_match=True,
        canonical_Maria_B97_clean_only_uncredited_objects=32,new_editorial_credit=0,new_emulator_runs=4,total_new_frames=45404,
        main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
    if mode=='audit':assert not (VERIFY/'pre_apply_audit.json').exists();save(VERIFY/'pre_apply_audit.json',receipt)
    elif mode=='apply':
        assert read(VERIFY/'pre_apply_audit.json')==receipt and not (VERIFY/'applied_handoff.json').exists()
        for r in plan['files']:
            data=Path(r['staged']).read_bytes()
            with Path(r['target']).open('r+b') as stream:stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
            assert sha(Path(r['target']).read_bytes())==r['after_sha256']
        save(VERIFY/'applied_handoff.json',receipt)
    else:assert read(VERIFY/'applied_handoff.json')==receipt and not (VERIFY/'verified_handoff.json').exists();save(VERIFY/'verified_handoff.json',receipt)
    print(dict(mode=mode,files=6,cumulative='V4987',completed=5966,duplicate_credit=0,Maria_B97_uncredited=32,full_goal_active=True))
