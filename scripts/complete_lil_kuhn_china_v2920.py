"""Reconcile218 only after registered build,patch and actual current startup."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Kuhn_China_completion_v2920')
DOC=Path('translations/lil_kuhn_china_editorial_manuscript_v7.json')
FINAL=Path('translations/lil_kuhn_china_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_Kuhn_China_release_v2917/registered_release_verification.json')
START=Path('work/analysis/lil_Kuhn_China_startup_v2919/cold_boot_Lil_startup_town_verification.json')
FAMILY='Lil-Kuhn-China-B51-B52-B53-B54-B55-B56-B146-B147-B148-218-contextual-completed'
SUMMARY='V2920 completes218 fresh contextual reviews in registered cumulative experimentalV2916:152 revisions and66 individually justified retentions across LilSC2B51/B52/B53/B54/B55/B56/B146/B147/B148. Every speech has exact clean/current/integrated references, fresh source gloss, whole-exchange context, localization notes and allfive review gates. The connected exchanges preserve Georg allegations, the assassination and tentative crest inference, Lil money-and-worldwide-help ideals, anonymous questions and subsequent Maria identity reveal, the private false-flag plot, Li downfall/subordination alternatives, declaration of war, Camille disappearance and Hodram temporary voyage offer, and the bartender inquiry. Preserve first-person agency, qualifications, private knowledge, branches and emotional progression. Restore19 missing Mysterious Woman labels without revealing her name early; retain two Assassin labels and one Meanwhile Camille caption. Do not invent romance, kinship, ranks, assassin/mentor gender, elapsed years or destinations. Hodram source two-part spoken introduction does not authorize inserting Joakim into it. Translate the bartender feminine-nickname account respectfully; bothB66/B121 birth-name/backstory alternatives still require fresh review. All501 native commands/218 complete preambles/160 relative sites/800 relocated branch cases/40 relocated predicates and inverse restoration pass;1600 source clean-current cases/436 historical dispatcher contexts remain bound. Four original event queries preserve operands/results, getter arguments0/1/2 and mapped incidental r3 source cursor; original four-byte alignment scratch restores all4MiB. Both images pass336 whole loads/cache hits and672 parent modes; three shipped-entry censuses preserve the original interpreter call and327 otherSC2 blocks. Xien0A actor state is preserved. Twenty-two FE selectors precede fallback208 and use original24310 null actor, including independently verified FI substitution to Lil. Mode1 paper geometry comes the calibrated typed context; variadic5473C entryr1 is not a layout mode. Complete196 ordinary216x64 planes plus22 FE228x48 logical/228x64 physical planes,1744 logical/compiled macro alignments and872 final padded alignments preserve all glyphs, blank paper, origins, bounds, four rows and single-page return. All28 initial sheets were viewed, revised ordinary sheet7 was viewed, and24 unchanged successor sheets match viewed predecessors by hash. Twenty-eight formatter and11 source/consumer negatives pass. Only89 individual ordinary Japanese/English row-count notes remain; no weak-ending, orphan, control, glyph, overflow or blank-page waiver. A natural on-the-pretext-of-avenging construction preserves the bogus vengeance excuse. All failed producers and earlier drafts remain preserved; global helpers/runtime are unchanged. Historical progressive ink/gray/blank/B74 return and actual FE paper rules inherit by exact runtime/COMMON/EV2/font/B74 bytes. Offline CPU/font evidence stays distinct from actual gameplay; no individual conditional/speaker/nameplate visit is required absent a concrete unresolved distinct risk. One guarded optional stage extends fullV2883;24 compiler rejection cases pass before mutation. V2916 has503 manifest batches/114 accepted layers; only the nine selectedSC2 blocks differ fromV2883. Every other file/component, ARM9/COMMON, graphics/fonts, cache/BSS extents and123040 staged bytes remains exact. The clean-input xdelta reconstructs the whole ROM byte for byte. Two fresh targeted headless coldboots complete4001 LilNewGame and17401 town/Refit frames; all31 whole framebuffers matchV2883, five actor/captain checks and donor hashes pass, and the six-frame sheet was viewed. The inherited five-ship Copenhagen battery and three access fixtures remain unearned and disclosed; no new fixture, observer or savestate is added. No selected Kuhn/China activation, earned travel/funding/pact/battle, new nameplate, full-route or hardware claim. Fresh coverage is2971 reread /2971 integrated-reconciled /zero pending. Completion2971 comprises2090 historically revised and881 retained; source/prose2974 includes1144SC2. Completed file counts1599COMMON/1144SC2/117SC0/73SC1/38SC3; all1372 reviewed route objects are integrated. COMMON750-752, every untouched storyline/shared shop-town/random/player prose family, uncredited Source Items/Local Product and five named-target leads, raw rejected-object classification includingB141 inventory assertion, SC3B109, separate graphics/all18 plaques and later older-record technical re-audit remain open. Preserve every ROM, earlier translation, source/profile/proof and clean/canonical input; V1492 remains promoted. Full goal active; all jobs terminal.'

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    prior=Path('work/analysis/editorial_handoff_verification_v2907/verified_handoff.json')
    assert sha(lp.read_bytes())==read(prior)['ledger_sha256']
    release,start=read(RELEASE),read(START)
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all503_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V2883'] and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_selected_Kuhn_China_IDs']==[] and sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    # The six current frames were viewed before executing this producer.
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':152,'retain-wording':66}
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
            integrated_hex=value.hex(),completed_candidate_reference=release['candidate'],registered_prose_owner='lil_kuhn_china_editorial',
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
    assert len(selected)==218 and {(r['file_path'],r['id']) for r in fresh['pending_record_keys']}==selected
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2971,2753,218)
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert not oldkeys&selected
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2906')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    review=ROOT/'current_six_frame_visual_review.json';save(review,dict(sheet=start['review_sheet'],sha256=start['review_sheet_sha256'],viewed=True,
        findings='Lil selection and opening dialogue and inherited town/Refit component screens are legible and match V2883. Current startup only; no selectedKuhn/China activation.'))
    proofpaths=[DOC,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['native_FE_font_proof']),Path(doc['representative_proof']),Path(doc['historical_representative_sheet_review']),Path(doc['prior_current_sheet_review']),RELEASE,START,prior,review,Path(__file__),
        Path('work/analysis/lil_Kuhn_China_registration_v2915/registration_receipt.json'),Path('work/analysis/lil_Kuhn_China_registration_v2915/negative_cases.json'),
        Path('work/analysis/lil_Kuhn_China_research_v2910/research_image_receipt.json'),
        Path('work/analysis/lil_Kuhn_China_reference_census_v2912/all501_commands160_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_Kuhn_China_loader_v2911/whole_SC2_and_nine_selected_blocks_initial_entry_proof.json')]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    save(FINAL,dict(format='dk4-natural-dialogue-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        id=FAMILY,manuscript=str(DOC),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        revised=152,retained=66,records=rows,summary=SUMMARY,evidence=evidence,actual_selected_Kuhn_China_IDs=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=0,current_six_frame_sheet_viewed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[51,52,53,54,55,56,146,147,148],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),revised_count=152,retained_count=66,fresh_revisions=152,fresh_retentions=66,
        actual_verification_scope='Historical shared progressive/FE rules plus two current cold-start/story/town samples. 196ordinary and22FE panels bind current native fonts,typed paper,null-actor FI andparity;no choices. No selectedKuhn/China activation.',records=rows))
    ledger.update(records_editorially_completed=2971,records_revised_and_integrated=2090,retained_wordings_editorially_completed=881)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=1144
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][p]=[ident for ident in ids if ('/data/SC2.DK4',ident) not in selected]
    for p in [DOC]:
        if str(p) not in active['manuscripts']:active['manuscripts'].append(str(p))
        active['route_record_subsets_pending'][str(p)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='2971 fresh rereads integrated/reconciled;source/prose2974. MarketCOMMON750-752caller context unresolved;all wider untouched prose remains in scope.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=2971,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=218,final_review=str(FINAL),new_revisions=152,justified_retentions=66,new_completed_records=218,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=152,retained=66),actual_selected_Kuhn_China_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0))
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1372,completed_route_records=1372,next='Continue untouched route/shared/town/random/player prose. All-route review remains open.')
        if unit['id']=='Lil-Kuhn-China-B51-B52-B53-B54-B55-B56-B146-B147-B148-218':unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,completion_credit_added=218,final_review=str(FINAL),full_goal_complete=False)
    watch=ledger['formatting_watchlist']['lil_Kuhn_China_v2906']
    watch.update(status='complete-through-V2920',reference_map_pending=False,
        representative_reconciliation_pending=False,superseded_by='lil_Kuhn_China_v2920',final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_Kuhn_China_v2920']=dict(status='all218-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),evidence=evidence,
        actual_selected_Kuhn_China_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,no_orphan_predicate_or_missing_glyph_waivers=True)
    oldcandidate=deepcopy(ledger['current_integrated_candidate']);ledger['previous_current_integrated_candidate_before_V2916']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(oldcandidate)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False,
        **{key+'_sha256':digest for key,digest in release['story_hashes'].items()})
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2906']['path']))
    next_clean=Path('work/analysis/lil_after_China_clean_scope_v2922/clean_next_exchange_inventory.json');next_scope=read(next_clean)
    assert next_scope['editorial_credit_added']==0 and not next_scope['unclassified'] and sum(b['speeches'] for b in next_scope['blocks'])==358
    assert not {(r['file_path'],r['id']) for r in fresh['record_keys']}&{('/data/SC2.DK4',r['id']) for b in next_scope['blocks'] for r in b['records']}
    inventory['next_clean_only_uncredited_exchange_inventory']=dict(path=str(next_clean),sha256=sha(next_clean.read_bytes()),blocks=[57,58,59,60,61,62,63,64,65,66,121],speeches=358,source_prose_or_completion_credit_added=0,status='clean-only scope mapping;contextual and consumer reviews not yet done')
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,
        next_focus='Continue untouched source/story exchanges,includingB57onward andbothB66/B121CamilleKuhnbackstory alternatives,andallotherstorylines/sharedshop-town/random/player prose;marketCOMMON750-752callers,rawrejected-objectclassification,separategraphics andlaterolder-recordtechnicalreaudit remainopen.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1372,completed_route_records=1372,source_prose_pending_records=0,source_prose_pending_family=None,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2920']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,full_goal_complete=False)
    ledger['lil_Kuhn_China_completion_v2920']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}=={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert len(keys)==len(fresh['integrated_record_keys'])==2971
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2974
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    release_note=('Release details: experimental profile `'+release['profile']+'`. Candidate `'+release['candidate']+'`, SHA-256 `'+release['candidate_sha256']+'`. '
        'Canonical base `'+release['canonical_base']+'`, SHA-256 `'+release['canonical_base_sha256']+'`. '
        'Clean-input patch `'+release['patch']+'`, SHA-256 `'+release['patch_sha256']+'`. '
        'The manifest enumerates all503 batches and114 accepted layers, including the full V2883 stack and the new218-speech manuscript. '
        'Internal delta from V2883: `/data/SC2.DK4` blocks51/52/53/54/55/56/146/147/148 only; every other file and component is exact. '
        'Verifiers: source/relocation/reference/native-font/padding checks,24 compiler rejections, `verify_lil_kuhn_china_release_v2917.py` and `verify_lil_kuhn_china_startup_v2919.py`. '
        'Current cold-boot areas are title/character selection,Lil opening,andtown/Refit. Human cold-boot acceptance is still required for promotion; V1492 remains promoted.\n\n')
    section='## V2920:218 Kuhn/China reviews completed in V2916\n\n'+SUMMARY+'\n\n'+release_note+'Final review: '+FINAL.as_posix()+'. Release/patch: '+RELEASE.as_posix()+'. Current startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Current COMMON parser remains dk4tool.patch.surrender_advice_contextual_v1.current_entries;bounded context remains scripts/current_common_native_context_v2677.py because ARM9/COMMON are byte-identical.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V2920' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2920',summary=SUMMARY,evidence={**evidence,str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=218,new_source_prose_reviews=0,revisions=152,justified_retentions=66,
        fresh_reread=2971,fresh_integrated=2971,fresh_pending=0,source_prose=2974,completed=2971,historical_revised=2090,historical_retained=881,incomplete_COMMON=3,incomplete_route=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        actual_selected_Kuhn_China_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2920:218completed in registeredV2916;152revisions/66retentions;2971reread/integrated,source-prose2974. COMMON3andall widerprose remainopen;fullgoalactive.')
