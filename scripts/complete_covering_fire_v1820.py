"""Close seven existing covering-fire paragraphs after fresh current verification."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from shutil import copy2
import os
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import reinforcement_faction_prose as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/covering_fire_completion_v1820')
FINAL=Path('translations/covering_fire_final_review_v1.json')
DOC=Path('translations/reinforcement_sniping_editorial_manuscript_v4.json')
ROM=Path('out/all_routes_combined_v1807_candidate.nds')
NATIVE=Path('work/analysis/covering_fire_current_v1818/current567_layouts_and22_native_planes.json')
ACTUAL=Path('work/analysis/covering_fire_actual_v1819/actual_covering_fire_verification.json')
COMMANDS=Path('work/analysis/covering_fire_actual_v1819/terminal_command_input_binding.json')
RELEASE=Path('work/analysis/reinforcement_faction_release_v1805/registered_release_verification.json')
STARTUP=Path('work/analysis/reinforcement_faction_release_v1805/ordinary_startup_verification.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1807 Covering fire verified')

if __name__=='__main__':
    assert not ROOT.exists()and not FINAL.exists()and not GUIDE.exists()
    doc,native,actual,commands,release,startup=map(read,(DOC,NATIVE,ACTUAL,COMMANDS,RELEASE,STARTUP))
    digest=sha(ROM.read_bytes());assert digest==native['candidate_sha256']==actual['candidate_sha256']==release['candidate_sha256']==startup['candidate_sha256']
    assert len(native['cases'])==567 and len(native['fresh_native_samples'])==22
    assert native['all567_current_original_printf_wraps_and_complete_font_planes_pass']
    assert native['original_voice_selector_and_source_table_bytes_exact']
    for r in native['fresh_native_samples']:assert sha(Path(r['preview']).read_bytes())==r['preview_sha256']
    for r in native['review_sheets']:assert sha(Path(r['path']).read_bytes())==r['sha256']
    assert len(actual['complete_actual_holds'])==2 and[f['owned_byte_count']for f in actual['exact_fixture_replays']]==[16,32]
    assert actual['normal_A_dismissal_enters_original_battle_without_blank_or_extra_page']
    assert actual['original_support_scan_loaded_existing_own_fleet57_as_player_support']
    assert commands['all_commands_validated_and_full_actual_input_schedule_exact']and commands['terminal_frame']==6310
    assert release['whole_reconstruction_byte_exact']and startup['all8_complete_startup_title_NewGame_frames_exact']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert sha(ROM.with_suffix('.manifest.json').read_bytes())==release['manifest_sha256']
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');conf=read(owned.CONFIG)
    current=owned.entries(image.read_file(owned.PATH),arm,conf['directory_sha256'])
    clean=NdsImage.open('work/clean.nds');source=common_message_entries(clean.read_file(owned.PATH),clean.read_file('/__arm9__.bin'))
    ids=set(range(1917,1924));rows=[]
    for original in doc['records']:
        n=original['message_id']
        if n not in ids:continue
        row=deepcopy(original);assert source[n].text.hex()==row['source_hex']and current[n].text==compiled(row)
        assert all(row['review'].values())
        row.update(previous_current_reference=row['current_reference'],previous_current_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(current[n]).items()if k!='text'},current_text_hex=current[n].text.hex(),
            current_English=row['english'],completed_candidate_reference=str(ROM),completed_candidate_sha256=digest,
            decision='revised-and-integrated'if row['editorial_decision']=='revise'else'retained-with-justification',
            status='complete-source-native-and-representative-original-gameplay',actual_proof=str(ACTUAL),
            current_native_reconciliation=str(NATIVE),individually_activated_in_current_build=n==1917,
            actual_scope='Current original1917 with Charles18 fallback andManuel23 regional fleet57. Full holds6010/6110,normal dismissal andoriginal battle/duel entry6310. Six other voice alternatives receive full source/native coverage;no individual actual-visit orduel-outcome claim.')
        if row['editorial_decision']=='retain':
            row['retained_wording_justification']={
                1921:'It looks like preserves source apparentness;nearby fleet andtoo preserve location andalso;help us is natural English for the older speakers offer ofassistance.',
                1922:'I hear preserves the source quoted/hearsay ending;nearby fleet andlend us a hand naturally express the youthful reported offer without inventing specific covering fire.',
                1923:'It seems preserves source apparentness;nearby fleet andtoo preserve the full report. Join our side refers to supporting this original battle,not a new faction allegiance.'}[n]
        rows.append(row)
    revised=sum(r['editorial_decision']=='revise'for r in rows);retained=len(rows)-revised
    assert(len(rows),revised,retained)==(7,4,3)
    raw=LEDGER.read_bytes();ledger=read(LEDGER);before=deepcopy(ledger)
    assert(ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(1509,1142,367)
    assert ids<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    family='Covering-fire-nearby-fleet-voice-variants7'
    assert not any(set(f.get('native_message_IDs',[]))&ids for f in ledger['completed_editorial_families'])
    ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(raw);(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    scope=('Seven COMMON covering-fire/support voice alternatives1917-1923 are complete in unchanged registered V1807:four previously integrated revisions andthree justified retained wordings. '
        'Clean Japanese,nearby location,apparent/hearsay tone,help versus explicit covering fire,relief andalso were reread. The native argument is the compact commander label,not a faction orfull character name. '
        'All567 current native printf/wrap/full independent font cases equal reviewed outputs.22 fresh native raster planes include every voice,14 fullwidth-F cases,seven maximum-length cases andthe actual Manuel case. '
        'Three complete native review sheets andactual portrait/nameplate/whole text/normal transition captures were viewed. '
        'Current original1917 uses Charles18 fallback andexisting own regional fleet57 underManuel23. Two complete native/independent/actual RGB holds6010/6110 pass. '
        'Normal A dismissal enters the original battle andduel screen6310. Two source-water-checked fixtures own16 then32 coordinate bytes only;all4MiB deltas replay exactly. '
        'Original anddisposable battery saves,input schedule,PNG/RAM hashes,native voice table/selector andresident message block pass. No RNG,message,health,identity,ownership,policy oroutcome override. '
        'This is one representative actual voice plus complete source/native alternatives,not seven individual visits,earned travel,a complete battle/duel orhardware verification. '
        'V1807 ROM/manifest/exact clean patch remain byte-identical to the V1814 checkpoint;all477 batches114 accepted layers,eight startup controls andevery existing translation remain preserved. '
        'Successful Lookout shot1924-1930 andnormal shot outcome/dismissal remain open;the source-bound level-preserving1798c fixture is offline approved buthas no successful live shot. '
        'Full editorial goal active:116 reviewed-incomplete COMMON entries,broader shared/routes/player prose,separate graphics/all18 plaques andlater older-record re-audit remain open. V1492 remains promoted.')
    visual=ROOT/'source_and_visual_review.json'
    save(visual,{'all7_clean_Japanese_and_current_English_reviewed':True,'four_revisions_three_justified_retentions':True,
        'three_current_native_review_sheets_viewed':native['review_sheets'],
        'actual_Charles_portrait_complete_Manuel_name_two_full_holds_andduel_transition_viewed':True,
        'complete_leading_trailing_CP932_glyphs_native_margins_bounds_andpagination_verified':True,
        'no_individual_actual_claim_for_other_six_voices':True,'successful_shot_andduel_outcome_unverified':True,
        'proofs':{str(p):sha(p.read_bytes())for p in(DOC,NATIVE,ACTUAL,COMMANDS,RELEASE,STARTUP)},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','file_path':owned.PATH,'native_message_IDs':sorted(ids),
        'records':rows,'record_IDs':[r['id']for r in rows],'manuscript':str(DOC),'candidate':str(ROM),'candidate_sha256':digest,
        'proofs':{str(p):sha(p.read_bytes())for p in(DOC,NATIVE,ACTUAL,COMMANDS,RELEASE,STARTUP,visual)},
        'actual_verification_scope':scope,'completed_entries':7,'revised':4,'retained':3,'ROM_bytes_changed_this_checkpoint':False,'full_goal_complete':False})
    ledger['completed_editorial_families'].append({'id':family,'file_path':owned.PATH,'native_message_IDs':sorted(ids),
        'record_IDs':[r['id']for r in rows],'records':rows,'final_review':str(FINAL),
        'documentation':'docs/covering_fire_v1820_completion.md','actual_verification_scope':scope})
    ledger['coverage_units'].append({'id':family,'file_path':owned.PATH,'native_message_IDs':sorted(ids),'status':'complete-source-native-and-representative-original-gameplay',
        'final_review':str(FINAL),'completed_entries_added':7,'source_prose_reviews_added':0,'full_goal_complete':False})
    ledger['records_editorially_completed']+=7;ledger['records_revised_and_integrated']+=4;ledger['retained_wordings_editorially_completed']+=3
    ledger['completed_editorial_record_counts_by_file'][owned.PATH]+=7
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs']if n not in ids]
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=[n for n in drafts['native_message_IDs']if n not in ids]
    for key,pending in drafts['manuscript_record_subsets_pending'].items():drafts['manuscript_record_subsets_pending'][key]=[n for n in pending if n not in ids]
    drafts.update(status='116-reviewed-COMMON-and-broader-prose-open',note='Reinforcement6,covering-fire7,fleet-sighting15 andLil opening/lessons complete. Successful Lookout shot,other116 reviewed COMMON andbroader shared/routes/player prose remain open.')
    ledger['pending_registered_reinforcement_sniping_candidate'].update(completed_native_message_IDs=list(range(1911,1924)),
        pending_final_review_native_message_IDs=list(range(1924,1931)),latest_covering_fire_actual_proof=str(ACTUAL),
        note='Historical V1034 artifact retained. Reinforcement6 andcovering-fire7 completed in current V1807;only successful-shot7 remains within this original20-row family.')
    ledger['formatting_watchlist'][family]={'final_review':str(FINAL),'current_native_name_layout_cases':567,'fresh_native_font_samples':22,
        'current_actual_holds':2,'all_complete_glyphs_and_normal_transition_verified':True,'broader_formatting_audit_open':True}
    ledger['current_integrated_candidate']['details']='V1820 adds current covering-fire7 completion without changing ROM bytes. '+scope
    ledger['latest_registered_editorial_candidate']['additional_completed_covering_fire_family']=str(FINAL)
    summary='V1820 completes seven covering-fire entries:1516 complete(1146 revised370 retained),1632 source/prose reviewed;116 reviewed-incomplete COMMON andbroader prose remain. '+scope
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1820-covering-fire7-complete','proof':str(ROOT/'completion_receipt.json'),
        'completed_entries_added':7,'source_prose_reviews_added':0,'previous_goal_turn_classification':'progress:six source-faithful reinforcement revisions integrated,patched,andcurrent-gameplay verified',
        'this_goal_turn_classification':'progress:current original covering-fire scene/native567-name matrix andnormal transition verified;seven previously reviewed rows complete',
        'full_goal_complete':False})
    for key in('unresolved_graphics_work','source_prose_reviewed_counts_by_file','records_with_source_and_prose_pass',
        'reviewed_but_incomplete_route_record_IDs','newly_observed_armed_latina_followup','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key]==before[key],key
    assert ledger['records_editorially_completed']==sum(ledger['completed_editorial_record_counts_by_file'].values())==1516
    assert ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed']==1516
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==len(drafts['native_message_IDs'])==116
    assert ledger['goal_status']=='active'and not ledger['full_goal_complete']
    pending=LEDGER.with_name('editorial_review_current_v1820_pending.json');assert not pending.exists()and LEDGER.read_bytes()==raw
    save(pending,ledger);os.replace(pending,LEDGER)
    GUIDE.mkdir(parents=True);pictures=[]
    for name,source_picture,frame in[('01_Original_covering_fire',Path(actual['complete_actual_holds'][1]['capture']),6110),
        ('02_Normal_original_duel_entry',Path(actual['actual_duel_entry_screenshot']),6310)]:
        destination=GUIDE/(name+'.png');copy2(source_picture,destination);assert sha(destination.read_bytes())==sha(source_picture.read_bytes())
        pictures.append({'guide':str(destination),'source':str(source_picture),'frame':frame,'sha256':sha(destination.read_bytes())})
    save(GUIDE/'capture_provenance.json',{'candidate':str(ROM),'candidate_sha256':digest,'captures':pictures,
        'original256x384_lossless_framebuffer_captures':True,'disclosed_fixture':'Two fixtures16/32 own/main-regional coordinates only;no earned travel oroutcome claim.',
        'source_and_disposable_battery_saves_unchanged':True,'no_savestate_or_RNG_message_health_result_override':True,
        'actual_proof':str(ACTUAL),'actual_proof_sha256':sha(ACTUAL.read_bytes())})
    document=Path('docs/covering_fire_v1820_completion.md');document.write_text('# V1820 covering-fire7 complete\n\n'+summary+
        '\n\nFinal review: '+str(FINAL)+'\n\nThree retained wordings are individually justified in the final review. All remaining successful-shot andbroader editorial work stays open.\n',encoding='utf-8')
    for name in('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with(Path('docs')/name).open('a',encoding='utf-8')as f:f.write('\n\n## V1820 covering-fire7 complete\n\n'+summary+'\n\nSee [completion](covering_fire_v1820_completion.md).\n')
    handoff=HANDOFF.read_text();assert handoff.startswith('# Current editorial handoff - V1814')
    handoff=handoff.replace('# Current editorial handoff - V1814','# Current editorial handoff - V1820',1)
    handoff=handoff.replace('1509 complete =1142 revised +367 retained.','1516 complete =1146 revised +370 retained.')
    handoff=handoff.replace('Completed per file:1395 COMMON +114 SC2','Completed per file:1402 COMMON +114 SC2')
    handoff=handoff.replace('Earlier123 reviewed-incomplete COMMON','Earlier116 reviewed-incomplete COMMON')
    anchor='## Latest completed family and next original-test evidence - V1814'
    assert handoff.count(anchor)==1
    added='## Latest completed family - V1820\n\n'+scope+'\n\n'+f'Final review: {FINAL.as_posix()}. Current native proof: {NATIVE.as_posix()}. Current actual proof: {ACTUAL.as_posix()}.\n\n'+'All current jobs areterminal;fresh covering-fire1817 ended6310 normally andsource/disposable saves arepreserved. No newROM orpatch wascreated. The prior Lookout1799 ended6471;its level-preserving successor1798c isoffline approved only.\n\n'+'Next: successful Lookout shot1924-1930 using a bounded source-guarded new cold-load test with1798c;or inventory the next original eligible Lil scene after normal Bruges return. Broader shared/routes/player prose remains in scope. Do notrepeat completed reinforcement6,covering-fire7 orLil opening/lessons without a concrete risk.\n\n'
    handoff=handoff.replace(anchor,added+anchor,1)
    handoff=handoff.replace('Pending COMMON:750-752;1917-1930;','Pending COMMON:750-752;1924-1930;')
    HANDOFF.write_text(handoff,encoding='utf-8')
    save(ROOT/'completion_receipt.json',{'candidate':str(ROM),'candidate_sha256':digest,'final_review':str(FINAL),
        'final_review_sha256':sha(FINAL.read_bytes()),'counts_before_after':[1509,1516],'revised_before_after':[1142,1146],
        'retained_before_after':[367,370],'source_prose_reviewed':1632,'reviewed_incomplete_COMMON':116,
        'ledger_sha256':sha(LEDGER.read_bytes()),'handoff_sha256':sha(HANDOFF.read_bytes()),'guide_captures':pictures,
        'ROM_patch_manifest_and_all184_output_ROMs_preserved':True,'successful_shot_remains_unverified_no_completion_credit':True,
        'full_editorial_goal_active_graphics_and_later_reaudit_separate':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Seven covering-fire entries complete:1516 total(1146 revised370 retained),1632 source/prose,116 older pending COMMON. V1807 unchanged;goal active.',flush=True)
