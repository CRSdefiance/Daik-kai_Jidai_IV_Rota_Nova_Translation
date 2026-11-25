"""Close15 already-integrated sighting entries after current native/live checks."""
from copy import deepcopy
from dataclasses import asdict
import os
from pathlib import Path
from shutil import copy2
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.search_reports_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.sighting_layout_v1069 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_completion_v1794')
FINAL=Path('translations/sighting_editorial_final_review_v1.json')
DOC=Path('translations/sighting_editorial_manuscript_v9.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
ROM=Path('out/all_routes_combined_v1775_candidate.nds')
MATRIX=Path('work/analysis/current_sighting_matrix_v1792/current2700_native_wrap_and_font_reconciliation.json')
ACTUAL=Path('work/analysis/close_sighting_terminal_v1791/complete_close_range_scene_and_fixture_audit.json')
NEGATIVE=Path('work/analysis/close_loading_findings_v1793/negative_pilot_and_original_admission_rule.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1775 Fleet sighting verified')

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists() and not GUIDE.exists()
    doc,matrix,actual,negative=map(read,(DOC,MATRIX,ACTUAL,NEGATIVE))
    digest=sha(ROM.read_bytes());image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin')
    assert digest==matrix['candidate_sha256']==actual['candidate_sha256']==negative['candidate_sha256']
    release=read('work/analysis/lil_lessons_release_v1774/registered_release_verification.json')
    assert digest==release['candidate_sha256'] and release['complete_reconstruction_byte_exact']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert sha(ROM.with_suffix('.manifest.json').read_bytes())==release['manifest_sha256']
    assert sha(Path('translations/release_stack.json').read_bytes())==release['release_stack_sha256']
    assert read('translations/release_stack.json')['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert len(matrix['cases'])==2700 and len(matrix['fresh_current_native_full_font_samples'])==15
    assert matrix['all2700_current_native_expansions_and_wraps_equal_reviewed_outputs']
    assert matrix['all2700_current_independent_font_planes_equal_prior_complete_native_planes']
    assert len(actual['all13_fixtures_independently_replayed_entire4MiB'])==13
    assert actual['normal_single_A_dismissal_to_viewed_Sea_View']
    assert actual['seen_flag_changes_only_after_original_gameplay_step_not_fixture']
    assert len(negative['original14_loading_predicate_cases'])==14
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert doc['formatting_review_pending'] is False and len(doc['records'])==15
    assert all(r['editorial_decision']=='revise' and all(r['review'].values())for r in doc['records'])
    clean_path=Path('work/clean.nds');assert sha(clean_path.read_bytes())==doc['source_clean_ROM_sha256']
    clean=NdsImage.open(clean_path)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    current=current_entries(image.read_file('/COMMON/MESFILE.DK4'),arm)
    for lo,hi in ((0x53F4C,0x53FE4),(0x774BC,0x77EC4)):
        assert arm[lo:hi]==clean.read_file('/__arm9__.bin')[lo:hi]
    for at in (0x118540,0x118560):assert arm[at:at+32]==clean.read_file('/__arm9__.bin')[at:at+32]
    rows=[]
    for original in doc['records']:
        row=deepcopy(original);n=row['message_id']
        assert jp[n].text.hex()==row['source_hex'] and current[n].text==compiled(row)
        row.update(previous_current_reference=row['current_reference'],previous_current_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(current[n]).items()if k!='text'},
            current_text_hex=current[n].text.hex(),current_English=row['english'],
            completed_candidate_reference=str(ROM),completed_candidate_sha256=digest,
            decision='revised-and-integrated',status='complete-source-native-and-representative-original-gameplay',
            current_native_reconciliation=str(MATRIX),actual_proof=str(ACTUAL),
            individually_activated_in_current_build=n==614,
            original_historical_individual_sample=n in (614,622),
            actual_scope='Current V1775 close-range614;earlier original compass614/incoming622 samples inherit exact reviewed templates andcurrent2700 expansion/font reconciliation. Other voice alternatives receive native/source coverage,not individual actual claims.')
        rows.append(row)
    scope=('All15 COMMON fleet-sighting voice variants614-628 are source/context/prose reviewed andalready integrated in registered V1775. '
        'Current native printf/wrap replays cover2700 combinations of15 messages,nine bearings and20 full faction labels;all outputs equal reviewed layouts. '
        'All2700 current independent complete font planes match previously verified native planes,with15 fresh current complete native raster samples,one pervoice. '
        'Both new review sheets were viewed;complete words,first/last letters,margins,bounds andpagination pass. '
        'Actual current close-range614 displays vicinity andCenturione Co. withoriginal role1 fallback Charles18;two complete native/independent/RGB holds pass. '
        'The original game loads unseen fleet8 atmedium range,then selects its first-sighting flag after the close approach.13 location/initial-relation fixtures replay exactly acrossall4MiB;enemy state,loaded groups,RNG,actors,health,templates andoutcomes were not injected. '
        'One normal A dismissal returns to viewed Sea View withoriginal pending battle context[0,1,8]. Source/disposable battery saves stayunchanged;no savestate,earned progression,complete battle orhardware claim. '
        'Earlier compass614 andincoming622 are historical actual samples,withcurrent exact native text/format/font reconciliation;this doesnot claim15 individual current gameplay visits. '
        'The unsuccessful direct-close pilot is audited through150 exact location footprints and14 native admission cases;normal loading uses the160..319 band,explaining its missed event without a ROM defect. '
        'V1775 ROM/manifest/exact clean patch are unchanged. Armed Latina actual name UI,successful Lookout shot,129 earlier reviewed COMMON entries,broader prose andseparate graphics/all18 plaques remain open. '
        'V1492 remains promoted;full editorial goal active.')
    raw=LEDGER.read_bytes();ledger=read(LEDGER);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1488,1121,367,1632)
    ids=set(range(614,629));assert ids<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    family='Fleet-sighting-voice-variants15';assert not any(f['id']==family for f in ledger['completed_editorial_families'])
    prior_ids={str(x)for f in ledger['completed_editorial_families']for x in f.get('record_IDs',[])}
    assert not any(str(n)in prior_ids or f'COMMON_MESSAGE_{n}'in prior_ids for n in ids)
    ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(raw);(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    visual=ROOT/'current_source_native_and_actual_visual_review.json'
    save(visual,{'all15_Japanese_source_and_English_voice_variants_rechecked':True,
        'preparation_vs_actual_attack_meaning_both_argument_positions_andfull_faction_names_preserved':True,
        'current_both_native_review_sheets_all15_panels_actually_viewed':True,
        'current_actual_close_range_notice_Charles_portrait_nameplate_andnormal_Sea_View_return_actually_viewed':True,
        'complete_leading_trailing_letters_natural_word_boundaries_anduniform_left_margins':True,
        'historical_compass614_andincoming622_are_not_new_current_visits':True,
        'Armed_Latina_actual_UI_and_Lookout_successful_shot_remain_open':True,
        'proofs':{str(p):sha(p.read_bytes())for p in [DOC,MATRIX,ACTUAL,NEGATIVE]},'full_goal_complete':False})
    proof_paths=[DOC,MATRIX,ACTUAL,NEGATIVE,visual,Path(doc['native_font_proof']),Path(doc['visual_review']),
        Path('work/analysis/sighting_grammar_release_v1104/registered_release_verification.json'),
        Path('work/analysis/sighting_grammar_actual_v1106b/actual_compass_and_covering_fire_verification.json'),
        Path('work/analysis/sighting_incoming_actual_v1109/actual_compass_and_covering_fire_verification.json'),
        Path('work/analysis/lil_lessons_release_v1774/registered_release_verification.json')]
    proofs={str(p):sha(p.read_bytes())for p in proof_paths}
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','file_path':'/COMMON/MESFILE.DK4',
        'native_message_IDs':sorted(ids),'records':rows,'record_IDs':[r['id']for r in rows],
        'manuscript':str(DOC),'candidate':str(ROM),'candidate_sha256':digest,'proofs':proofs,
        'actual_verification_scope':scope,'completed_entries':15,'revised':15,'retained':0,'full_goal_complete':False})
    ledger['completed_editorial_families'].append({'id':family,'file_path':'/COMMON/MESFILE.DK4',
        'native_message_IDs':sorted(ids),'record_IDs':[r['id']for r in rows],'records':rows,'final_review':str(FINAL),
        'documentation':'docs/sighting_v1794_completion.md','actual_verification_scope':scope})
    ledger['coverage_units'].append({'id':family,'file_path':'/COMMON/MESFILE.DK4','native_message_IDs':sorted(ids),
        'record_IDs':[r['id']for r in rows],'status':'complete-source-native-and-representative-original-gameplay',
        'final_review':str(FINAL),'completed_entries_added':15,'source_prose_reviews_added':0,'full_goal_complete':False})
    ledger['records_editorially_completed']+=15;ledger['records_revised_and_integrated']+=15
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']+=15
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs']if n not in ids]
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=[n for n in drafts['native_message_IDs']if n not in ids]
    for key,pending in drafts['manuscript_record_subsets_pending'].items():drafts['manuscript_record_subsets_pending'][key]=[n for n in pending if n not in ids]
    drafts.update(status='129-reviewed-COMMON-and-broader-prose-open',
        note='Fleet-sighting15 andLil opening/lessons arecomplete. Earlier129 reviewed COMMON entries andbroader shared/routes/player prose remain. Armed Latina actual UI andsuccessful Lookout shot areseparate open checks.')
    ledger['newly_observed_sighting_followup'].update(status='complete15-in-V1775;current-close-range-and2700-native-cases-verified',
        close_range_Japanese_provider_remains_open=False,final_review=str(FINAL),actual_close_range_proof=str(ACTUAL),
        current_native_reconciliation=str(MATRIX),completed_entries_added=15)
    ledger['latest_sighting_editorial_family']={'status':'complete15','final_review':str(FINAL),
        'current_actual_close_range':str(ACTUAL),'native_reconciliation':str(MATRIX),
        'original_loading_rule_and_negative_test':str(NEGATIVE),'ROM_bytes_changed':False,'full_goal_complete':False}
    ledger['formatting_watchlist']['Fleet_sighting_voice_variants15']={'status':'completed-in-existing-V1775',
        'current_native_substitution_cases':2700,'fresh_complete_native_font_samples':15,
        'current_actual_close_range_holds':2,'final_review':str(FINAL),'broader_formatting_audit_open':True}
    ledger.setdefault('integrated_candidate_reference_history',[]).append(deepcopy(ledger['current_integrated_candidate']))
    ledger['current_integrated_candidate']['details']='V1775 bytes unchanged;Lil opening49/lessons64 andfleet-sighting15 verified. '+scope
    ledger['latest_registered_editorial_candidate']['additional_verified_sighting_family']=str(FINAL)
    summary='V1794 closes15 older fleet-sighting entries:1503 complete(1136 revised367 retained),1632 source/prose reviewed;129 reviewed-incomplete COMMON andbroader prose remain. '+scope
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1794-fleet-sighting15-complete','proof':str(ROOT/'completion_receipt.json'),
        'completed_entries_added':15,'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in ('unresolved_graphics_work','source_prose_reviewed_counts_by_file','records_with_source_and_prose_pass',
        'reviewed_but_incomplete_route_record_IDs','newly_observed_armed_latina_followup'):
        assert ledger[key]==before[key],key
    assert ledger['goal_status']=='active' and ledger['full_goal_complete'] is False
    assert ledger['records_editorially_completed']==sum(ledger['completed_editorial_record_counts_by_file'].values())==1503
    assert ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed']==1503
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==len(drafts['native_message_IDs'])==129
    pending=LEDGER.with_name('editorial_review_current_v1794_pending.json');assert not pending.exists() and LEDGER.read_bytes()==raw
    save(pending,ledger);assert read(pending)==ledger and LEDGER.read_bytes()==raw;os.replace(pending,LEDGER)
    GUIDE.mkdir(parents=True);pictures=[]
    for name,source,frame in [('01_Close_range_fleet_sighting',Path(actual['two_complete_current_native_independent_actual_holds'][1]['capture']),5443),
        ('02_Normal_Sea_View_return',Path(actual['terminal_capture']),5503)]:
        target=GUIDE/(name+'.png');copy2(source,target);assert sha(target.read_bytes())==sha(source.read_bytes())
        pictures.append({'guide':str(target),'source':str(source),'sha256':sha(source.read_bytes()),'frame':frame})
    save(GUIDE/'capture_provenance.json',{'candidate':str(ROM),'candidate_sha256':digest,'captures':pictures,
        'original256x384_lossless_framebuffer_captures':True,'disclosed_fixtures':'13 location/initial-relation fixtures;no enemy flags,loaded groups,RNG,actor health,dialogue oroutcomes edited.',
        'source_and_disposable_battery_saves_unchanged':True,'no_savestate_orcomplete_battle_hardware_claim':True,'proof':str(ACTUAL)})
    Path('docs/sighting_v1794_completion.md').write_text('# V1794 fleet-sighting15 complete\n\n'+summary+
        '\n\nThe15 paragraphs were already integrated. This checkpoint closes the missing close-range actual display gate andrefreshes current native coverage. No ROM orpatch bytes changed.\n\n'
        'Final review: '+str(FINAL)+'\n\nActual proof: '+str(ACTUAL)+'\n\nGuide captures: '+str(GUIDE)+'\n',encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8')as f:f.write('\n\n## V1794 fleet-sighting15 complete\n\n'+summary+'\n\nSee [completion](sighting_v1794_completion.md).\n')
    handoff=HANDOFF.read_text(encoding='utf-8');assert handoff.startswith('# Current editorial handoff - V1779')
    replacements={
        '# Current editorial handoff - V1779':'# Current editorial handoff - V1794',
        '1488 complete =1121 revised +367 retained.':'1503 complete =1136 revised +367 retained.',
        'Completed per file:1374 COMMON +114 SC2':'Completed per file:1389 COMMON +114 SC2',
        'Earlier144 reviewed-incomplete COMMON':'Earlier129 reviewed-incomplete COMMON',
        'earlier144 COMMON entries':'earlier129 COMMON entries',
        'Pending COMMON:614-628;750-752;':'Pending COMMON:750-752;'}
    for old,new in replacements.items():assert old in handoff;handoff=handoff.replace(old,new)
    at=handoff.index('## Completed lesson evidence')
    latest='''## Latest completed shared-dialogue work - V1794

Fleet-sighting15 (COMMON614-628) is complete in unchanged V1775. Final review: translations/sighting_editorial_final_review_v1.json. Completion receipt: work/analysis/sighting_completion_v1794/completion_receipt.json. All15 Japanese voice variants andcurrent English were reread;preparation versus incoming attack,faction names,bearing-first/faction-second arguments andvoice remain faithful. The phrases use established compass abbreviations orvicinity;no faction/name/provider was shortened forstorage.

Current proof: work/analysis/current_sighting_matrix_v1792/current2700_native_wrap_and_font_reconciliation.json. All2700 current native printf/wrap outputs equal reviewed layouts (15 messages,nine bearings,20 factions). All2700 independent current complete font planes match previous complete native planes;15 fresh current full native raster samples,one pervoice,pass. Both new sheets were viewed. This isnot2700 new native raster runs oractual visits.

Actual close-range proof: work/analysis/close_sighting_terminal_v1791/complete_close_range_scene_and_fixture_audit.json. Fresh V1775 cold load ofa disposable regional battery save reaches614 withoriginal Charles18 role1 fallback,vicinity andCenturione Co. Two full native/independent/actual holds5413/5443 pass;one normal A dismissal returns to viewed Sea View5503 withoriginal pending battle context[0,1,8].13 full4MiB fixture replays,input/PNG/RAM hashes andunchanged source/disposable saves pass. Initial fixture owns16 coordinate bytes plusone original diplomatic prerequisite byte;later fixtures ownonly16 coordinates. Enemy seen flags,loaded groups,RNG,actors,health,messages andoutcomes areuntouched. No savestate,earned travel,full battle orhardware claim. Historical compass614 andincoming622 samples are inherited through exact reviewed templates/current2700 native reconciliation;do notclaim15 individual current visits.

The missed close tests were test-context issues. Source proof work/analysis/close_loading_findings_v1793/negative_pilot_and_original_admission_rule.json independently audits150 location footprints and14 original loading cases. Original normal Sea View setsR8=0 at7BF8C andpasses mode0 to77EDC at7C194. Mode0 loads the160..319 distance band;initial mode1 loads inner<160. Direct close placement ofan unloaded fleet bypasses normal admission. The successful run lets original fleet8 load unseen atmedium range,observes two loaded states,then approaches withsource-observed motion compensation. Never manually insert loaded groups orclear seen flags. This isnota ROM bug orproduction fix.

Successful producers: native_two_stage_sighting_v1786b.py,run_two_stage_sighting_v1787b.py,navigate_two_stage_sighting_v1788.py,verify_close_sighting_live_v1790.py,audit_close_sighting_terminal_v1791.py,verify_current_sighting_matrix_v1792.py,audit_close_loading_findings_v1793.py. Preserve failed1786/1787 import attempt and1783 duration rejection;successors were explicit. The rejected duration appliedno input/fixture;the same1782 emulator continued,then stopped5250 withouttarget credit. The successful separate1787 test stopped5503 normally. Guide screenshots: E:/Rota Nova translations/Guide screenshots/V1775 Fleet sighting verified.

Armed Latina actual name UI remains open separately. Successful Lookout shot1911-1930 also remains open. The newly proven native loading/contact context may help those tests;do notrepeat blind direct-close placement. V1775 ROM/manifest/patch andV1492 promotion remain unchanged. Full editorial andseparate graphics goals remain open.

'''
    handoff=handoff[:at]+latest+handoff[at:]
    start=handoff.index('All current jobs are terminal:')
    end=handoff.index('Before ROM changes,',start)
    handoff=handoff[:start]+('All current jobs are terminal. Negative runner60408 stopped5250;successful runner46394 stopped5503. Navigators97885 (timeout after rejected command),75731 and34702 areterminal;audits88734/32025 and1793 arecomplete. No live emulator remains. Never restart solely after an observation timeout. All source/disposable saves and183 existing output ROMs arepreserved. Previous handoff/ledger arein the current completion folder;prior archiveV1780 remains available.\n\n')+handoff[end:]
    HANDOFF.write_text(handoff,encoding='utf-8')
    save(ROOT/'completion_receipt.json',{'candidate':str(ROM),'candidate_sha256':digest,'ROM_manifest_and_patch_bytes_changed':False,
        'newly_completed':15,'newly_revised':15,'newly_retained':0,'completed':1503,'revised':1136,'retained':367,
        'source_prose':1632,'reviewed_incomplete_COMMON':129,'complete_COMMON':1389,'complete_SC2':114,
        'final_review':str(FINAL),'proofs':proofs,'guide':str(GUIDE),'screenshots':pictures,
        'all_current_jobs_terminal':True,'Armed_Latina_UI_andsuccessful_Lookout_shot_remain_open':True,
        'graphics_all18_plaques_andbroader_editorial_scope_preserved':True,
        'ledger_sha256':sha(LEDGER.read_bytes()),'handoff_sha256':sha(HANDOFF.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    assert sha(ROM.read_bytes())==digest and sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    print({'newly_completed':15,'complete':1503,'revised':1136,'retained':367,'source_prose':1632,
        'pending_reviewed_COMMON':129,'ROM_unchanged':'V1775','full_goal':'active'},flush=True)
