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

ROOT=Path('work/analysis/lil_Goods_Mediterranean_completion_v2844')
DOC=Path('translations/lil_goods_mediterranean_editorial_manuscript_v6.json')
FINAL=Path('translations/lil_goods_mediterranean_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_Goods_Mediterranean_release_v2841/registered_release_verification.json')
START=Path('work/analysis/lil_Goods_Mediterranean_startup_v2843/cold_boot_Lil_startup_town_verification.json')
FAMILY='Lil-Polder-Source-Goods-Mediterranean-B41-B43-B44-B45-B46-90-contextual-completed'
SUMMARY='V2844 completes90 fresh contextual reviews in registered cumulative experimentalV2840:67 revisions and23 justified retentions across LilSC2B41/B43/B44/B45/B46. The complete exchanges cover the governor office and400,000 gold gift, source-item use and market-share strategy, Africa-and-India trade and Mediterranean plans, Hayreddin downfall/subordination and crew praise, and Pasha downfall/subordination and uncertain treasure. Every entry has exact clean/current/integrated references, fresh meaning/context/localization notes and allfive review gates. Preserve the full governor-office name, currency versus cargo, future funding, source items versus ordinary goods, Market terminology, alternatives, rumor/appearance qualifiers, crew credit for Lil leadership and private Camille impressions. No new romance, rank, named courier, armor identity, earned funding/voyage/battle or gift is invented. Mikhail native4C remains executable presentation state; his context attribution is corrected from Julio while the original gloss and English were already correct. EmptyB42 is bounded without speech credit. The older item-category Local Product versus reviewed help Source Items remains an exact-referenced uncredited semantic reconciliation lead. All273 native commands/90 complete preambles/128 relative sites/640 relocated branch cases/32 relocated predicates, inverse restoration and every opaque byte pass. Clean/current1280 branch cases and180 historical dispatcher contexts remain bound. B44 completion20 queries at160/476 retain source operands, arguments0/1/2 and mapped incidental r3 source cursor; only original four-byte read-alignment scratch is permitted and restoration recovers all4MiB. Both images pass336 whole-block loaders/cache hits and672 parent modes; three shipped-entry censuses and331 other SC2 blocks are exact. Complete90 native216x64 planes/720 logical-compiled alignment cases and360 additional final parity cases preserve first/interior/final glyphs, blank paper, row origins, bounds, four rows and pagination. All12 original sheets and three changed successor sheets were viewed;86 cases/688 calls remain exact reused evidence andfour planes/32 calls were reexecuted. Fourteen formatter rejections/90 complete English-control-macro invariants pass. Only42 individually justified ordinary Japanese/English row-count notes are allowed; no weak-ending, orphan, control, missing-glyph, overflow or blank-page waiver. One conversational subject omission resolves the2824 compound split; local wrapping refinements preserve reviewed words and global helpers/runtime. Failed2833 relocation-count adaptation and2837 inherited-startup-key probes are preserved; corrected2833b and2837b pass. Historical actual progressive ink/gray/blank/B74 return and shared consumer rules inherit by exact ARM9/COMMON/EV2/font/B74 bytes. Offline CPU/font tests stay distinct from actual gameplay. Individual conditional/speaker/nameplate visits are not required absent a concrete unresolved distinct risk. One guarded stage extends fullV2814;17 negative cases reject before mutation. V2840 has501 manifest batches/114 accepted layers; onlySC2B41/B43/B44/B45/B46 differ fromV2814. All other files/components, ARM9/COMMON, graphics/fonts, cache/BSS extents and123040 staged bytes remain exact. Clean-input xdelta reconstructs the wholeROM byte-for-byte. Two new targeted headless coldboots finish4001 LilNewGame and17401 town/Refit frames; all31 complete framebuffers matchV2814, five actor/captain checks and source/disposable donor hashes pass, and the six-frame current sheet was viewed. The inherited five-ship Copenhagen battery and three access fixtures are unearned and disclosed; no new fixture/observer/savestate is added. No selected goods/Mediterranean scene activation, new nameplate, full-route or hardware claim is made. Fresh coverage is2671 reread /2671 integrated-reconciled /zero pending. Completion2671 comprises1875 historically revised and796 retained; source/prose2674 includes844SC2. Completed file counts1599COMMON/844SC2/117SC0/73SC1/38SC3; all1072 reviewed route objects are integrated. COMMON750-752, every untouched storyline/shared shop-town/random/player prose family, five uncredited named-target leads, raw rejected-object classification, SC3B109, separate graphics/all18 plaques and later older-record technical re-audit remain open. Every ROM, earlier translation, profile, clean/canonical input and executed proof is preserved; V1492 remains promoted. Full goal active; all jobs terminal.'

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    prior=Path('work/analysis/editorial_handoff_verification_v2832/verified_handoff.json')
    assert sha(lp.read_bytes())==read(prior)['ledger_sha256']
    release,start=read(RELEASE),read(START)
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all501_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V2814'] and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_selected_Goods_Mediterranean_IDs']==[] and sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    # The six current frames were viewed before executing this producer.
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':67,'retain-wording':23}
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
            integrated_hex=value.hex(),completed_candidate_reference=release['candidate'],registered_prose_owner='lil_goods_mediterranean_editorial',
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
    assert len(selected)==90 and {(r['file_path'],r['id']) for r in fresh['pending_record_keys']}==selected
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2671,2581,90)
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert not oldkeys&selected
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2831')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    review=ROOT/'current_six_frame_visual_review.json';save(review,dict(sheet=start['review_sheet'],sha256=start['review_sheet_sha256'],viewed=True,
        findings='Lil selection and opening dialogue and inherited town/Refit component screens are legible and match V2814. Current startup only; no selectedgoods/Mediterranean activation.'))
    proofpaths=[DOC,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['representative_proof']),Path(doc['historical_representative_sheet_review']),Path(doc['prior_current_sheet_review']),RELEASE,START,prior,review,Path(__file__),
        Path('work/analysis/lil_Goods_Mediterranean_registration_v2839/registration_receipt.json'),Path('work/analysis/lil_Goods_Mediterranean_registration_v2839/negative_cases.json'),
        Path('work/analysis/lil_Goods_Mediterranean_research_v2834b/research_image_receipt.json'),
        Path('work/analysis/lil_Goods_Mediterranean_reference_census_v2836/all273_commands128_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_Goods_Mediterranean_loader_v2835/whole_SC2_and_five_selected_blocks_initial_entry_proof.json')]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    save(FINAL,dict(format='dk4-natural-dialogue-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        id=FAMILY,manuscript=str(DOC),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        revised=67,retained=23,records=rows,summary=SUMMARY,evidence=evidence,actual_selected_Goods_Mediterranean_IDs=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=0,current_six_frame_sheet_viewed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[41,43,44,45,46],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),revised_count=67,retained_count=23,fresh_revisions=67,fresh_retentions=23,
        actual_verification_scope='Historical shared progressive rules plus two current cold-start/story/town samples. All90are originalprogressive;noFEorchoices inthisbatch. No selectedgoods/Mediterranean activation.',records=rows))
    ledger.update(records_editorially_completed=2671,records_revised_and_integrated=1875,retained_wordings_editorially_completed=796)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=844
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][p]=[ident for ident in ids if ('/data/SC2.DK4',ident) not in selected]
    for p in [DOC]:
        if str(p) not in active['manuscripts']:active['manuscripts'].append(str(p))
        active['route_record_subsets_pending'][str(p)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='2671 fresh rereads integrated/reconciled;source/prose2674. MarketCOMMON750-752caller context unresolved;all wider untouched prose remains in scope.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=2671,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=90,final_review=str(FINAL),new_revisions=67,justified_retentions=23,new_completed_records=90,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=67,retained=23),actual_selected_Goods_Mediterranean_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0))
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1072,completed_route_records=1072,next='Continue untouched route/shared/town/random/player prose. All-route review remains open.')
        if unit['id']=='Lil-Polder-Source-Goods-Mediterranean-B41-B43-B44-B45-B46-90':unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,completion_credit_added=90,final_review=str(FINAL),full_goal_complete=False)
    watch=ledger['formatting_watchlist']['lil_Goods_Mediterranean_v2831']
    watch.update(status='complete-through-V2844',reference_map_pending=False,
        representative_reconciliation_pending=False,superseded_by='lil_Goods_Mediterranean_v2844',final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_Goods_Mediterranean_v2844']=dict(status='all90-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),evidence=evidence,
        actual_selected_Goods_Mediterranean_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,no_orphan_predicate_or_missing_glyph_waivers=True)
    oldcandidate=deepcopy(ledger['current_integrated_candidate']);ledger['previous_current_integrated_candidate_before_V2840']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(oldcandidate)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False,
        **{key+'_sha256':digest for key,digest in release['story_hashes'].items()})
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2831']['path']))
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,
        next_focus='Continue untouched source/story exchanges,includingB47onward andCamilleKuhnbackstory,andallotherstorylines/sharedshop-town/random/player prose;marketCOMMON750-752callers,rawrejected-objectclassification,separategraphics andlaterolder-recordtechnicalreaudit remainopen.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1072,completed_route_records=1072,source_prose_pending_records=0,source_prose_pending_family=None,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2844']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,full_goal_complete=False)
    ledger['lil_Goods_Mediterranean_completion_v2844']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}=={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert len(keys)==len(fresh['integrated_record_keys'])==2671
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2674
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    release_note=('Release details: experimental profile `'+release['profile']+'`. Candidate `'+release['candidate']+'`, SHA-256 `'+release['candidate_sha256']+'`. '
        'Canonical base `'+release['canonical_base']+'`, SHA-256 `'+release['canonical_base_sha256']+'`. '
        'Clean-input patch `'+release['patch']+'`, SHA-256 `'+release['patch_sha256']+'`. '
        'The manifest enumerates all501 batches and114 accepted layers, including the full V2814 stack and the new90-speech manuscript. '
        'Internal delta from V2814: `/data/SC2.DK4` blocks41/43/44/45/46 only; every other file and component is exact. '
        'Verifiers: source/relocation/reference/native-font/padding checks,17 compiler rejections, `verify_lil_goods_mediterranean_release_v2841.py` and `verify_lil_goods_mediterranean_startup_v2843.py`. '
        'Current cold-boot areas are title/character selection,Lil opening,andtown/Refit. Human cold-boot acceptance is still required for promotion; V1492 remains promoted.\n\n')
    section='## V2844:90 polder, source-item and Mediterranean reviews completed in V2840\n\n'+SUMMARY+'\n\n'+release_note+'Final review: '+FINAL.as_posix()+'. Release/patch: '+RELEASE.as_posix()+'. Current startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Current COMMON parser remains dk4tool.patch.surrender_advice_contextual_v1.current_entries;bounded context remains scripts/current_common_native_context_v2677.py because ARM9/COMMON are byte-identical.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V2844' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2844',summary=SUMMARY,evidence={**evidence,str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=90,new_source_prose_reviews=0,revisions=67,justified_retentions=23,
        fresh_reread=2671,fresh_integrated=2671,fresh_pending=0,source_prose=2674,completed=2671,historical_revised=1875,historical_retained=796,incomplete_COMMON=3,incomplete_route=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        actual_selected_Goods_Mediterranean_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2844:90completed in registeredV2840;67revisions/23retentions;2671reread/integrated,source-prose2674. COMMON3andall widerprose remainopen;fullgoalactive.')
