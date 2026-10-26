"""Reconcile172 only after registered build,patch and actual current startup."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Homecoming_Ian_completion_v3033')
DOC=Path('translations/lil_homecoming_ian_editorial_manuscript_v6.json')
FINAL=Path('translations/lil_homecoming_ian_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_Homecoming_Ian_release_v3030/registered_release_verification.json')
START=Path('work/analysis/lil_Homecoming_Ian_startup_v3032/cold_boot_Lil_startup_town_verification.json')
FAMILY='Lil-Homecoming-Ian-172-contextual-completed'
SUMMARY='V3033 completes all 172 speeches in complete Lil SC2 B70/B71 homecoming, crew retrospective, confession, wedding, Kuhn visit, completed-polder report and optional Ian shopping exchange. There are 120 revisions and 52 individually justified retentions, including both previously validated V678 wedding repairs. Every record has exact clean/current references, a fresh clean-source gloss, whole-exchange context, localization decisions and all five review gates. Preserve the source69 achievement query, source48 optional departure fragment and source48 Kuhn visit; the unconditional realization must still work without the departure clause. Restore the money-only self-assessment, widening dream from people in need to everyone, explicit romantic confession and several-years transition. Keep distinct crew voices, jokes and conditional reactions. Mikhail76 wants to remain as an onlooker and Julio rebukes him; no invented kinship. Kuhn is explicitly Camille father, while ResearchStudent171 remains the polder researcher rather than a priest. No invented shown-object identity, wedding vows, completed ceremony, universal prosperity or full family reconciliation. Camille hope about finding his path stays personal and qualified. The separate optional Ian scene does not become a post-wedding sequel; admiration versus love, Lil opinion about women, inferred jealousy and Camille denial remain distinct. He flees before any hit. All 390 commands,172 preambles,124 relative sites,1240 clean/current branch cases,344 historical dispatcher contexts,31 current predicates and three queries pass. All 158 ordinary216x64 planes and14 FE228x48 logical/228x64 physical planes pass with1376 original logical/compiled macro alignment cases, all glyphs, blank paper, origins, bounds and single-page consumption. All20 ordinary and two FE sheets were viewed. Twenty-eight metric/layout and13 source/consumer rejection tests pass. Only63 individually justified Japanese/English row-count notes remain; no orphan,weak-ending,control,glyph,bounds or pagination waiver. Failed3014 phrase plan, all manuscripts/producers/proofs and every ROM remain preserved. Existing actual wedding FE geometry and complete M26 movie evidence are hash-bound to current identical owned code,font and movie assets. Historical V666 was recovered exactly from its clean-input patch for research only. No new wedding fixture,selected-scene gameplay or hardware claim. Offline CPU/font evidence remains distinct from actual gameplay; new focused tests require concrete remaining risks. The mapped movie cursor4508 and original M26 arguments26,0,1,0 pass three focused original-handler cases at clean/current/relocated cursors, preserving source-owned scene reset and every unowned byte. Fresh coverage is3646 reread /3646 integrated-reconciled /zero pending; source/prose3649 including1819SC2. Completion3646 comprises2512 historically revised and1134 retained. All2047 reviewed route records are integrated. One guarded optional stage follows fullV2996;28compiler negatives reject beforemutation. V3029 contains507manifest batches/114acceptedlayers. OnlySC2B70/B71 differ fromV2996;334otherSC2blocks,everyotherfile/component,ARM9/COMMON,fonts/graphics,cache/BSS and123040stagedbytes remain exact. The clean-input xdelta reconstructs the entireROM byteforbyte. Two fresh targeted headless coldboots complete4001LilNewGame and17401town/Refitframes;all31wholeframebuffers matchV2996,five actor/captain controls anddonor hashes pass,andthe current six-frame sheet was viewed. All wider untouched storylines,shared shop-town,random scenes,help/player-facing prose,COMMON750-752 callers,SourceItems/LocalProduct,five named-target leads,raw rejected-object classification includingB141,SC3B109,separate graphics/all18 plaques and later older-record technical re-audit remain open. The exact0D wrong-consumer validation-gap lead remains queued for that later audit without asserting an older runtime defect. BothB66/B121 remain completed. Preserve clean/canonical inputs and prior releases; V1492 remains promoted. Full goal active; all jobs terminal.'

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    prior=Path('work/analysis/editorial_handoff_verification_v3020/verified_handoff.json')
    assert sha(lp.read_bytes())==read(prior)['ledger_sha256']
    release,start=read(RELEASE),read(START)
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all507_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V2996'] and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_selected_Homecoming_Ian_IDs']==[] and sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    # The six current frames were viewed before executing this producer.
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':120,'retain-wording':52}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] for r in rows)
    image=NdsImage.open(release['candidate']);blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    for row in rows:
        block=blocks[row['block']]
        spec=refs[row['id']];offset=spec['new_offset'];value=bytes.fromhex(spec['target_hex'])
        assert block[offset:offset+len(value)]==value and block[offset-5:offset]==bytes.fromhex('0040ffff00')
        row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in ['current_reference','current_hex','current_English','current_record_index','record_index'] if k in row}
        reference=dict(block=row['block'],offset=offset,header_offset=offset-5,bytes=len(value),record_index=block[:offset].count(b'\0'))
        row.update(current_reference=reference,current_hex=value.hex(),current_text_hex=value.hex(),integrated_reference=reference,
            integrated_hex=value.hex(),completed_candidate_reference=release['candidate'],registered_prose_owner='lil_homecoming_ian_editorial',
            registered_manuscript=str(DOC),
            historical_editorial_decision='revise' if row['editorial_decision']=='revise' else 'retain',
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            individual_actual_activation_not_claimed=True,all_source_native_representative_and_registered_gates_pass=True,
            status='complete-contextual-current-native-references-representative-and-registered-release')
        row['current_English']=value[1:].decode('ascii')
        if row['editorial_decision']=='retain-wording':row.setdefault('fresh_retained_wording_justification',row['localization_note'])
        if row['kind']!='typed-choice-label':
            row['current_record_index']=row['record_index']=reference['record_index']
    selected={(r['file_path'],r['id']) for r in rows};fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert len(selected)==172 and {(r['file_path'],r['id']) for r in fresh['pending_record_keys']}==selected
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(3646,3474,172)
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert not oldkeys&selected
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V3019')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    review=ROOT/'current_six_frame_visual_review.json';save(review,dict(sheet=start['review_sheet'],sha256=start['review_sheet_sha256'],viewed=True,
        findings='Lil selection and opening dialogue and inherited town/Refit component screens are legible and match V2996. Current startup only; no selectedHomecoming/Ian activation.'))
    proofpaths=[DOC,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['native_FE_font_proof']),Path(doc['representative_proof']),Path(doc['historical_representative_sheet_review']),Path(doc['prior_current_sheet_review']),RELEASE,START,prior,review,Path(__file__),
        Path('work/analysis/lil_Homecoming_Ian_registration_v3028/registration_receipt.json'),Path('work/analysis/lil_Homecoming_Ian_registration_v3028/negative_cases.json'),
        Path('work/analysis/lil_Homecoming_Ian_research_v3022/research_image_receipt.json'),
        Path('work/analysis/lil_Homecoming_Ian_reference_census_v3024/all390_commands124_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_Homecoming_Ian_loader_v3023/whole_SC2_and_two_selected_blocks_initial_entry_proof.json')]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    save(FINAL,dict(format='dk4-natural-dialogue-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        id=FAMILY,manuscript=str(DOC),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        revised=120,retained=52,records=rows,summary=SUMMARY,evidence=evidence,actual_selected_Homecoming_Ian_IDs=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=0,current_six_frame_sheet_viewed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[70,71],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),revised_count=120,retained_count=52,fresh_revisions=120,fresh_retentions=52,
        actual_verification_scope='Historical progressive/FE/wedding rules plus two current cold-start/story/town samples.158ordinary/14FE panels andoneFI bind current native fonts,paper andparity. Original chapter6 M26arguments andrelocatedcursor pass three focused native cases;no selectedHomecoming/Ian activation.',records=rows))
    ledger.update(records_editorially_completed=3646,records_revised_and_integrated=2512,retained_wordings_editorially_completed=1134)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=1819
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][p]=[ident for ident in ids if ('/data/SC2.DK4',ident) not in selected]
    for p in [DOC]:
        if str(p) not in active['manuscripts']:active['manuscripts'].append(str(p))
        active['route_record_subsets_pending'][str(p)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='3646 fresh rereads integrated/reconciled;source/prose3649. MarketCOMMON750-752caller context unresolved;all wider untouched prose remains in scope.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=3646,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=172,final_review=str(FINAL),new_revisions=120,justified_retentions=52,new_completed_records=172,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=120,retained=52),actual_selected_Homecoming_Ian_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0))
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=2047,completed_route_records=2047,next='Continue untouched route/shared/town/random/player prose. All-route review remains open.')
        if unit['id']=='Lil-Homecoming-Ian-172':unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,completion_credit_added=172,final_review=str(FINAL),full_goal_complete=False)
    watch=ledger['formatting_watchlist']['lil_Homecoming_Ian_v3019']
    watch.update(status='complete-through-V3033',reference_map_pending=False,
        representative_reconciliation_pending=False,superseded_by='lil_Homecoming_Ian_v3033',final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_Homecoming_Ian_v3033']=dict(status='all172-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),evidence=evidence,
        actual_selected_Homecoming_Ian_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,no_orphan_predicate_or_missing_glyph_waivers=True)
    oldcandidate=deepcopy(ledger['current_integrated_candidate']);ledger['previous_current_integrated_candidate_before_V3029']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(oldcandidate)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False,
        **{key+'_sha256':digest for key,digest in release['story_hashes'].items()})
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v3019']['path']))
    inventory['next_clean_only_uncredited_exchange_inventory_v2964'].setdefault('reconciled_subsets',[]).append(dict(blocks=[70,71],speeches=172,final_review=str(FINAL),checkpoint='V3033'))
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,
        next_focus='Continue every untouched storyline/shared shop-town/random/player prose family,includingB72-B73andlaterrecruitment/randomscenes. BothB66/B121remaincompleted. COMMON750-752callers,SourceItems/LocalProduct,fivenamed-target leads,raw rejected-object classification includingB141,SC3B109,separategraphics andlaterolder-recordtechnicalreaudit remainopen.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=2047,completed_route_records=2047,source_prose_pending_records=0,source_prose_pending_family=None,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v3033']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,full_goal_complete=False)
    ledger['lil_Homecoming_Ian_completion_v3033']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}=={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert len(keys)==len(fresh['integrated_record_keys'])==3646
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==3649
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    release_note=('Release details: experimental profile `'+release['profile']+'`. Candidate `'+release['candidate']+'`, SHA-256 `'+release['candidate_sha256']+'`. '
        'Canonical base `'+release['canonical_base']+'`, SHA-256 `'+release['canonical_base_sha256']+'`. '
        'Clean-input patch `'+release['patch']+'`, SHA-256 `'+release['patch_sha256']+'`. '
        'The manifest enumerates all507 batches and114 accepted layers, including the full V2996 stack and the new172-speech manuscript. '
        'Internal delta from V2996: `/data/SC2.DK4` blocks70/71 only; every other file and component is exact. '
        'Verifiers: source/relocation/reference/native-font/padding checks,28 compiler rejections, `verify_lil_homecoming_ian_release_v3030.py` and `verify_lil_homecoming_ian_startup_v3032.py`. '
        'Current cold-boot areas are title/character selection,Lil opening,andtown/Refit. Human cold-boot acceptance is still required for promotion; V1492 remains promoted.\n\n')
    section='## V3033:172 Homecoming/Ian reviews completed in V3029\n\n'+SUMMARY+'\n\n'+release_note+'Final review: '+FINAL.as_posix()+'. Release/patch: '+RELEASE.as_posix()+'. Current startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Current COMMON parser remains dk4tool.patch.surrender_advice_contextual_v1.current_entries;bounded context remains scripts/current_common_native_context_v2677.py because ARM9/COMMON are byte-identical.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V3033' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V3033',summary=SUMMARY,evidence={**evidence,str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=172,new_source_prose_reviews=0,revisions=120,justified_retentions=52,
        fresh_reread=3646,fresh_integrated=3646,fresh_pending=0,source_prose=3649,completed=3646,historical_revised=2512,historical_retained=1134,incomplete_COMMON=3,incomplete_route=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        actual_selected_Homecoming_Ian_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V3033:172completed inregisteredV3029;120revisions/52retentions;3646reread/integrated,source-prose3649. Fullgoalactive.')
