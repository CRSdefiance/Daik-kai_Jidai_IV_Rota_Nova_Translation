"""Reconcile34 only after registered build,patch and actual current startup."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Kuhn_Alliance_completion_v2887')
DOC=Path('translations/lil_kuhn_alliance_editorial_manuscript_v9.json')
FINAL=Path('translations/lil_kuhn_alliance_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_Kuhn_Alliance_release_v2884/registered_release_verification.json')
START=Path('work/analysis/lil_Kuhn_Alliance_startup_v2886/cold_boot_Lil_startup_town_verification.json')
FAMILY='Lil-Kuhn-Alliance-B47-B48-B49-B50-82-contextual-completed'
SUMMARY='V2887 completes 82 fresh contextual reviews in registered cumulative experimental V2883:63 revisions and19 individually justified retentions across LilSC2B47/B48/B49/B50. Every speech has exact clean/current/integrated references, fresh gloss/context/localization notes and allfive review gates. The complete exchanges preserve Jam self-important joke and pain reaction, Georg courteous coercion and5000 currency-gold offer, Lil skepticism/business interest and later hurt/confusion, Camille private shock at Kuhn, shaking hands, failed explanations, denial and departure, every crew alternative, the private Marinus identity report and unspecified arrangements, and the conditional later alliance approach. Do not turn anti-Pereira allegations into fact, make private knowledge audible, prove a death, invent who strikes Jam, or award an unearned payment/pact. Restore approved Camille; retain Kuhn feminine-nickname characterization respectfully and remove invented Lord ranks. Native56 is Georg,40 Antony Kuhn; catalog composites/legacy glyphs are evidence, not new name edits or observed nameplates. Original event48 requires47,49 requires48,50 requires48andnot54/121/55/56. All195 native commands/82 complete preambles/60 relative sites/300 relocated branch cases/15 relocated predicates and inverse restoration pass; all600 source clean-current cases and164 historical dispatcher contexts remain bound. There are no8100 event queries, FE panels or choices in this batch. The15 original predicates preserve operands/results and zero event-getter calls; only original four-byte alignment-read scratch may change and restoring it recovers all4MiB. Both images pass336 whole-block loads/cache hits and672 parent entry modes; three shipped-entry censuses preserve the original interpreter call and all332 otherSC2 blocks. Complete82 native216x64 planes/656 logical-compiled macro alignments and328 final parity cases preserve first/interior/final glyphs, paper, origins, bounds, four rows and pagination. All11 initial sheets, seven changed2869 sheets and final2872 sheet3 were viewed; unchanged finals match viewed predecessors by hash. Fourteen formatter rejections and82 complete English/control/macro invariants pass. Only22 individual ordinary Japanese/English row-count notes remain; no weak-ending, orphan, control, glyph, overflow or blank-page waiver. Source-faithful business understatement resolves the dense paragraph, while local automatic rules keep questions/negation and key phrasal boundaries intact. Every failed plan and producer remains preserved, including the inherited census-filename mismatch corrected in2879b/2880b. All global helpers/runtime bytes remain unchanged. Historical actual progressive ink/gray/blank/B74 return and shared consumers inherit by exact ARM9/COMMON/EV2/font/B74 bytes. Offline CPU/font checks stay distinct from actual gameplay; individual conditional/speaker/nameplate visits are unnecessary absent a concrete distinct unresolved risk. One guarded optional stage extends fullV2840;17 negative cases reject before mutation. V2883 has502 manifest batches/114 accepted layers; onlySC2B47/B48/B49/B50 differ fromV2840. Every other file/component, ARM9/COMMON, fonts/graphics, cache/BSS extents and123040 staged bytes remains exact. The clean-input xdelta reconstructs the whole ROM byte for byte. Two fresh targeted headless coldboots complete4001 LilNewGame and17401 town/Refit frames; all31 whole framebuffers matchV2840, five actor/captain checks and source/disposable donor hashes pass, and the six-frame current sheet was viewed. The inherited five-ship Copenhagen battery and three access fixtures remain unearned and disclosed; no new fixture, observer or savestate is added. No selected Kuhn activation, new nameplate, full-route or hardware claim is made. Fresh coverage is2753 reread /2753 integrated-reconciled /zero pending. Completion2753 comprises1938 historically revised and815 retained; source/prose2756 includes926SC2. Completed file counts1599COMMON/926SC2/117SC0/73SC1/38SC3; all1154 reviewed route objects are integrated. COMMON750-752, every untouched storyline/shared shop-town/random/player prose family, the uncredited Source Items/Local Product terminology lead, five uncredited named-target leads, raw rejected-object classification, SC3B109, separate graphics/all18 plaques and later older-record technical re-audit remain open. BothB66 andB121 true-name/backstory alternatives still need fresh review. Preserve every ROM, earlier translation, profile, clean/canonical input and executed proof; V1492 remains promoted. Full goal active; all jobs terminal.'

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    prior=Path('work/analysis/editorial_handoff_verification_v2875c/verified_handoff.json')
    assert sha(lp.read_bytes())==read(prior)['ledger_sha256']
    release,start=read(RELEASE),read(START)
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all502_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V2840'] and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_selected_Kuhn_Alliance_IDs']==[] and sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    # The six current frames were viewed before executing this producer.
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':63,'retain-wording':19}
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
            integrated_hex=value.hex(),completed_candidate_reference=release['candidate'],registered_prose_owner='lil_kuhn_alliance_editorial',
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
    assert len(selected)==82 and {(r['file_path'],r['id']) for r in fresh['pending_record_keys']}==selected
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2753,2671,82)
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert not oldkeys&selected
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2874')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    review=ROOT/'current_six_frame_visual_review.json';save(review,dict(sheet=start['review_sheet'],sha256=start['review_sheet_sha256'],viewed=True,
        findings='Lil selection and opening dialogue and inherited town/Refit component screens are legible and match V2840. Current startup only; no selectedKuhn-alliance activation.'))
    proofpaths=[DOC,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['representative_proof']),Path(doc['historical_representative_sheet_review']),Path(doc['prior_current_sheet_review']),RELEASE,START,prior,review,Path(__file__),
        Path('work/analysis/lil_Kuhn_Alliance_registration_v2882/registration_receipt.json'),Path('work/analysis/lil_Kuhn_Alliance_registration_v2882/negative_cases.json'),
        Path('work/analysis/lil_Kuhn_Alliance_research_v2877/research_image_receipt.json'),
        Path('work/analysis/lil_Kuhn_Alliance_reference_census_v2879b/all195_commands60_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_Kuhn_Alliance_loader_v2878/whole_SC2_and_four_selected_blocks_initial_entry_proof.json')]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    save(FINAL,dict(format='dk4-natural-dialogue-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        id=FAMILY,manuscript=str(DOC),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        revised=63,retained=19,records=rows,summary=SUMMARY,evidence=evidence,actual_selected_Kuhn_Alliance_IDs=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=0,current_six_frame_sheet_viewed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[47,48,49,50],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),revised_count=63,retained_count=19,fresh_revisions=63,fresh_retentions=19,
        actual_verification_scope='Historical shared progressive rules plus two current cold-start/story/town samples. All90are originalprogressive;noFEorchoices inthisbatch. No selectedKuhn-alliance activation.',records=rows))
    ledger.update(records_editorially_completed=2753,records_revised_and_integrated=1938,retained_wordings_editorially_completed=815)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=926
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][p]=[ident for ident in ids if ('/data/SC2.DK4',ident) not in selected]
    for p in [DOC]:
        if str(p) not in active['manuscripts']:active['manuscripts'].append(str(p))
        active['route_record_subsets_pending'][str(p)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='2753 fresh rereads integrated/reconciled;source/prose2756. MarketCOMMON750-752caller context unresolved;all wider untouched prose remains in scope.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=2753,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=82,final_review=str(FINAL),new_revisions=63,justified_retentions=19,new_completed_records=82,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=63,retained=19),actual_selected_Kuhn_Alliance_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0))
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1154,completed_route_records=1154,next='Continue untouched route/shared/town/random/player prose. All-route review remains open.')
        if unit['id']=='Lil-Kuhn-Alliance-B47-B48-B49-B50-82':unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,completion_credit_added=82,final_review=str(FINAL),full_goal_complete=False)
    watch=ledger['formatting_watchlist']['lil_Kuhn_Alliance_v2874']
    watch.update(status='complete-through-V2887',reference_map_pending=False,
        representative_reconciliation_pending=False,superseded_by='lil_Kuhn_Alliance_v2887',final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_Kuhn_Alliance_v2887']=dict(status='all82-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),evidence=evidence,
        actual_selected_Kuhn_Alliance_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,no_orphan_predicate_or_missing_glyph_waivers=True)
    oldcandidate=deepcopy(ledger['current_integrated_candidate']);ledger['previous_current_integrated_candidate_before_V2883']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(oldcandidate)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False,
        **{key+'_sha256':digest for key,digest in release['story_hashes'].items()})
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2874']['path']))
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,
        next_focus='Continue untouched source/story exchanges,includingB51onward andbothB66/B121CamilleKuhnbackstory alternatives,andallotherstorylines/sharedshop-town/random/player prose;marketCOMMON750-752callers,rawrejected-objectclassification,separategraphics andlaterolder-recordtechnicalreaudit remainopen.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1154,completed_route_records=1154,source_prose_pending_records=0,source_prose_pending_family=None,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2887']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,full_goal_complete=False)
    ledger['lil_Kuhn_Alliance_completion_v2887']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}=={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert len(keys)==len(fresh['integrated_record_keys'])==2753
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2756
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    release_note=('Release details: experimental profile `'+release['profile']+'`. Candidate `'+release['candidate']+'`, SHA-256 `'+release['candidate_sha256']+'`. '
        'Canonical base `'+release['canonical_base']+'`, SHA-256 `'+release['canonical_base_sha256']+'`. '
        'Clean-input patch `'+release['patch']+'`, SHA-256 `'+release['patch_sha256']+'`. '
        'The manifest enumerates all502 batches and114 accepted layers, including the full V2840 stack and the new82-speech manuscript. '
        'Internal delta from V2840: `/data/SC2.DK4` blocks47/48/49/50 only; every other file and component is exact. '
        'Verifiers: source/relocation/reference/native-font/padding checks,17 compiler rejections, `verify_lil_kuhn_alliance_release_v2884.py` and `verify_lil_kuhn_alliance_startup_v2886.py`. '
        'Current cold-boot areas are title/character selection,Lil opening,andtown/Refit. Human cold-boot acceptance is still required for promotion; V1492 remains promoted.\n\n')
    section='## V2887:90 Kuhn alliance reviews completed in V2883\n\n'+SUMMARY+'\n\n'+release_note+'Final review: '+FINAL.as_posix()+'. Release/patch: '+RELEASE.as_posix()+'. Current startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Current COMMON parser remains dk4tool.patch.surrender_advice_contextual_v1.current_entries;bounded context remains scripts/current_common_native_context_v2677.py because ARM9/COMMON are byte-identical.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V2887' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2887',summary=SUMMARY,evidence={**evidence,str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=82,new_source_prose_reviews=0,revisions=63,justified_retentions=19,
        fresh_reread=2753,fresh_integrated=2753,fresh_pending=0,source_prose=2756,completed=2753,historical_revised=1938,historical_retained=815,incomplete_COMMON=3,incomplete_route=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        actual_selected_Kuhn_Alliance_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2887:82completed in registeredV2883;63revisions/19retentions;2753reread/integrated,source-prose2756. COMMON3andall widerprose remainopen;fullgoalactive.')
