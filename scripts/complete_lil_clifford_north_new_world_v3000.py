"""Reconcile143 only after registered build,patch and actual current startup."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Clifford_North_New_World_completion_v3000')
DOC=Path('translations/lil_clifford_north_new_world_editorial_manuscript_v8.json')
FINAL=Path('translations/lil_clifford_north_new_world_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_Clifford_North_New_World_release_v2997/registered_release_verification.json')
START=Path('work/analysis/lil_Clifford_North_New_World_startup_v2999/cold_boot_Lil_startup_town_verification.json')
FAMILY='Lil-Clifford-North-New-World-143-contextual-completed'
SUMMARY='V3000 completes143 speeches across six complete Lil SC2 exchanges B67/B68/B69/B149/B150/B151:Clifford downfall andsubmission rewards/letters,the worldwide-trade homeward suggestion,the Tang bamboo puzzle,Clifford New World strategy request andMaldonado private worries/public tavern confrontation. There are88revisions and55individually justified retentions,each with exact clean/current/integrated references,fresh gloss,complete-exchange context,localization notes andallfive review gates. No typed choices. Keep downfall/subordination outcomes andtwo letters distinct,includingthe67 northern address/heartfeltgift versus68 ordinary Dear FI heading andFEgift directions;both complete James Clifford signatures remain. Source61query controls stolen-Proof return material;no new earned reward orjourney claim. Camille views Clifford regret andCrown ties as his qualified interpretation. Lil prior belief stays personal,not proven knowledge. The earlier English Crown referent supports natural the Crown anaphora without losing the counterfactual. Homeward Amsterdam suggestion preserves concern about Camille own mother andLil private thanks without importing the later confession/wedding. Tang Bamboo Craft/Bamboo Assembly Plan match exact registered clean/current item pointers;the hidden East Asian Proof map is her confident inference,not aninvented spoken Chiron identification. Camille teasing/bonk/pain/discovery andFernando gambling comparison/reluctant task/boast remain distinct alternatives. Clifford three-force strategy is before betrayal despite storage order;first strike Maldonado whilegradually preparing forEscante,with uncertainty andFO macro intact. Maldonado private distrust/independence rumors/probable future threat/Crown-permission ambitions remain unproven andprivate. Jam Paris,France autobiography interruption,Lil FI FA self-introduction,rude woman address,small-country insults,freedom-to-trade retort,bottle throw that MISSES,coerced unpaid bill,Al anger/Gerhard restraint,andLil military dislike withHodram exception preserve intent andvoice. Remove invented actual injury,physical grip,home destination,guaranteed destruction,royal appointment orrank. All453native commands/143complete preambles/180relative sites/1800clean-current branchcases/286historical dispatcher cases/45current originalpredicates andfour eventqueries pass. Query67:282=26,68:12=61,68:1122=26,151:3246=121. Ordinary0D is actor13Cesare,notCRprose. A negative test exposed shared-encoder acceptance of0DunderwrongFEconsumer;the scoped formatter now explicitly requires prefix membership andthe exact source tag. Original dispatcher ownership was already sourcebound;no global helper/runtime edit. Failed2979andboth failed Crown-wrap plans remain preserved. The later older-record technical re-audit receives anexact validation-gap lead without asserting anolder runtime defect orstarting that audit early. Complete140ordinary216x64planes plus3FE228x48logical/228x64physicalplanes and1144logical-compiled macro cases preserve all leading/interior/trailing glyphs,blankpaper,origins,bounds,fourrows andsinglepage. The3FEbodies containtwo complete letters andanunlabeled Crash sound,no source name macros. Null-actor24310andtypedmode1paper are sourcebound;variadicr1isnotgeometry. All18ordinary sheets/oneFE sheet were viewed,all12changed successor sheets were viewed,sixunchanged sheets match viewedpredecessors. Twenty-three changed normalplanes/184macrocases rerun;117planes/936cases reuse exactEnglish/source/current/runtime/encodedbytes/previewhashes. FEbytes remain exact acrossguard-only andwrap changes. Twenty-eight formatter and11source/consumer negatives pass. Only44individual Japanese/English row-count notes;no weak-ending,orphan,control,overflow,glyph orblank-page waiver. All drafts/producers/proofs preserved. One guarded optional stage extends the full V2958 cumulative stack;27 compiler negatives reject before mutation. Failed registration templates2995/2995b stopped on stale helper/format metadata before anyROM/registry mutation;2995c corrected them andallfailedproducers remain preserved. V2996 has506manifest batches/114acceptedlayers. OnlySC2B67/B68/B69/B149/B150/B151differ fromV2958;330otherSC2blocks,everyotherfile/component,ARM9/COMMON,fonts/graphics,cache/BSS and123040stagedbytes remainexact. The clean-input xdelta reconstructs the entireROM byteforbyte. Two fresh targeted headless coldboots complete4001LilNewGame and17401town/Refitframes;all31wholeframebuffers matchV2958,five actor/captain checks anddonor hashespass,andthe current six-frame sheet was viewed. Historical progressive ink/gray/blank,B74return andFEactual paper rules inheritbyexactruntime/COMMON/EV2/font/B74bytes. OfflineCPU/font evidence staysdistinct fromselectedgameplay. Individualconditional/speaker/nameplate visits are unnecessary absentconcrete distinct unresolvedrisks. The inheritedfive-shipCopenhagenbattery andthreeaccessfixtures remainunearned/disclosed. No selectedClifford/north/NewWorldactivation,earnedtravel/funding/pact/battle,newfixture,newnameplate,fullroute orhardwareclaim. Fresh coverage is3474 reread /3474 integrated-reconciled /zero pending. Completion3474 comprises2392historically revised and1082retained;source/prose3477includes1647SC2. Completedfilecounts1599COMMON/1647SC2/117SC0/73SC1/38SC3;all1875reviewedrouteobjects areintegrated. BothB66/B121 remaincompleted. COMMON750-752callers,everywideruntouchedstoryline/sharedshop-town/random/playerprosefamily,SourceItems/LocalProduct,fivenamed-target leads,rawrejected-objectclassification includingB141,SC3B109,separategraphics/all18plaques andlaterolder-recordtechnicalreaudit remainopen. Keep the exact0Dwrong-consumer validation-gap lead queued for that later audit withoutclaiminganolderruntimedefect orstartingit prematurely. PreserveeveryROM,earliertranslation,clean/canonicalinput andexecutedproof. V1492remains promoted. Fullgoalactive;alljobs terminal.'

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    prior=Path('work/analysis/editorial_handoff_verification_v2988/verified_handoff.json')
    assert sha(lp.read_bytes())==read(prior)['ledger_sha256']
    release,start=read(RELEASE),read(START)
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all506_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V2958'] and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_selected_Clifford_North_New_World_IDs']==[] and sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    # The six current frames were viewed before executing this producer.
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':88,'retain-wording':55}
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
            integrated_hex=value.hex(),completed_candidate_reference=release['candidate'],registered_prose_owner='lil_clifford_north_new_world_editorial',
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
    assert len(selected)==143 and {(r['file_path'],r['id']) for r in fresh['pending_record_keys']}==selected
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(3474,3331,143)
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert not oldkeys&selected
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2987')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    review=ROOT/'current_six_frame_visual_review.json';save(review,dict(sheet=start['review_sheet'],sha256=start['review_sheet_sha256'],viewed=True,
        findings='Lil selection and opening dialogue and inherited town/Refit component screens are legible and match V2958. Current startup only; no selectedClifford/north/NewWorld activation.'))
    proofpaths=[DOC,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['native_FE_font_proof']),Path(doc['representative_proof']),Path(doc['historical_representative_sheet_review']),Path(doc['prior_current_sheet_review']),RELEASE,START,prior,review,Path(__file__),
        Path('work/analysis/lil_Clifford_North_New_World_registration_v2995c/registration_receipt.json'),Path('work/analysis/lil_Clifford_North_New_World_registration_v2995c/negative_cases.json'),
        Path('work/analysis/lil_Clifford_North_New_World_research_v2990/research_image_receipt.json'),
        Path('work/analysis/lil_Clifford_North_New_World_reference_census_v2992/all453_commands180_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_Clifford_North_New_World_loader_v2991/whole_SC2_and_six_selected_blocks_initial_entry_proof.json')]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    save(FINAL,dict(format='dk4-natural-dialogue-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        id=FAMILY,manuscript=str(DOC),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        revised=88,retained=55,records=rows,summary=SUMMARY,evidence=evidence,actual_selected_Clifford_North_New_World_IDs=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=0,current_six_frame_sheet_viewed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[67,68,69,149,150,151],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),revised_count=88,retained_count=55,fresh_revisions=88,fresh_retentions=55,
        actual_verification_scope='Historical shared progressive/FE rules plus two current cold-start/story/town samples. 140ordinary/3FE panels bind current native fonts,typed paper/parity;no FEname macros/nochoices. Source0Dactor13andwrong-consumer guard sourcebound. No selectedClifford/north/NewWorld activation.',records=rows))
    ledger.update(records_editorially_completed=3474,records_revised_and_integrated=2392,retained_wordings_editorially_completed=1082)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=1647
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][p]=[ident for ident in ids if ('/data/SC2.DK4',ident) not in selected]
    for p in [DOC]:
        if str(p) not in active['manuscripts']:active['manuscripts'].append(str(p))
        active['route_record_subsets_pending'][str(p)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='3474 fresh rereads integrated/reconciled;source/prose3477. MarketCOMMON750-752caller context unresolved;all wider untouched prose remains in scope.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=3474,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=143,final_review=str(FINAL),new_revisions=88,justified_retentions=55,new_completed_records=143,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=88,retained=55),actual_selected_Clifford_North_New_World_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0))
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1875,completed_route_records=1875,next='Continue untouched route/shared/town/random/player prose. All-route review remains open.')
        if unit['id']=='Lil-Clifford-North-New-World-143':unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,completion_credit_added=143,final_review=str(FINAL),full_goal_complete=False)
    watch=ledger['formatting_watchlist']['lil_Clifford_North_New_World_v2987']
    watch.update(status='complete-through-V3000',reference_map_pending=False,
        representative_reconciliation_pending=False,superseded_by='lil_Clifford_North_New_World_v3000',final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_Clifford_North_New_World_v3000']=dict(status='all143-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),evidence=evidence,
        actual_selected_Clifford_North_New_World_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,no_orphan_predicate_or_missing_glyph_waivers=True)
    oldcandidate=deepcopy(ledger['current_integrated_candidate']);ledger['previous_current_integrated_candidate_before_V2996']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(oldcandidate)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False,
        **{key+'_sha256':digest for key,digest in release['story_hashes'].items()})
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2987']['path']))
    inventory['next_clean_only_uncredited_exchange_inventory_v2964'].setdefault('reconciled_subsets',[]).append(dict(blocks=[67,68,69,149,150,151],speeches=143,final_review=str(FINAL),checkpoint='V3000'))
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,
        next_focus='Continue every untouched storyline/shared shop-town/random/player prose family,includingB70-B73andlaterrecruitment/randomscenes. BothB66/B121remaincompleted. COMMON750-752callers,SourceItems/LocalProduct,fivenamed-target leads,raw rejected-object classification includingB141,SC3B109,separategraphics andlaterolder-recordtechnicalreaudit remainopen.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1875,completed_route_records=1875,source_prose_pending_records=0,source_prose_pending_family=None,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v3000']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,full_goal_complete=False)
    ledger['lil_Clifford_North_New_World_completion_v3000']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}=={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert len(keys)==len(fresh['integrated_record_keys'])==3474
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==3477
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    release_note=('Release details: experimental profile `'+release['profile']+'`. Candidate `'+release['candidate']+'`, SHA-256 `'+release['candidate_sha256']+'`. '
        'Canonical base `'+release['canonical_base']+'`, SHA-256 `'+release['canonical_base_sha256']+'`. '
        'Clean-input patch `'+release['patch']+'`, SHA-256 `'+release['patch_sha256']+'`. '
        'The manifest enumerates all506 batches and114 accepted layers, including the full V2958 stack and the new143-speech manuscript. '
        'Internal delta from V2958: `/data/SC2.DK4` blocks67/68/69/149/150/151 only; every other file and component is exact. '
        'Verifiers: source/relocation/reference/native-font/padding checks,27 compiler rejections, `verify_lil_clifford_north_new_world_release_v2997.py` and `verify_lil_clifford_north_new_world_startup_v2999.py`. '
        'Current cold-boot areas are title/character selection,Lil opening,andtown/Refit. Human cold-boot acceptance is still required for promotion; V1492 remains promoted.\n\n')
    section='## V3000:143 Clifford/north/NewWorld reviews completed in V2996\n\n'+SUMMARY+'\n\n'+release_note+'Final review: '+FINAL.as_posix()+'. Release/patch: '+RELEASE.as_posix()+'. Current startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Current COMMON parser remains dk4tool.patch.surrender_advice_contextual_v1.current_entries;bounded context remains scripts/current_common_native_context_v2677.py because ARM9/COMMON are byte-identical.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V3000' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V3000',summary=SUMMARY,evidence={**evidence,str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=143,new_source_prose_reviews=0,revisions=88,justified_retentions=55,
        fresh_reread=3474,fresh_integrated=3474,fresh_pending=0,source_prose=3477,completed=3474,historical_revised=2392,historical_retained=1082,incomplete_COMMON=3,incomplete_route=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        actual_selected_Clifford_North_New_World_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V3000:143completed inregisteredV2996;88revisions/55retentions;3474reread/integrated,source-prose3477. COMMON3andallwiderprose remainopen;fullgoalactive.')
