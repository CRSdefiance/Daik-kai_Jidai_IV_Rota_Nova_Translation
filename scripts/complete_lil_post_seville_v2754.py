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

ROOT=Path('work/analysis/lil_post_Seville_completion_v2754')
DOC=Path('translations/lil_post_seville_and_egypt_warning_editorial_manuscript_v5.json')
FINAL=Path('translations/lil_post_seville_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_post_Seville_release_v2751/registered_release_verification.json')
START=Path('work/analysis/lil_post_Seville_startup_v2753/cold_boot_Lil_startup_town_verification.json')
FAMILY='Lil-post-Seville-and-Egypt-warning-B30-B31-B132-34-contextual-completed'
SUMMARY='V2754 completes34 contextual reviews in Lil SC2B30/B31/B132 through registered cumulative experimental V2750:22revisions and12individually justified retentions. The clean-Japanese full exchanges preserve Valdes defeat and shocked shame before his sovereign,both alternative alliance descriptions,Clifford explanation that their alliance confused Valdes into dividing his forces,Lil uneasy question about Clifford plans,and his dependence on royal orders. The Crown and my sovereign avoid the old unsupported male-monarch claim. Existing greetings,qualified hope,uneasy fragment and reciprocal farewells remain where they already work. The port-worker and barkeep exchanges restore the full Pirate King of the Mediterranean title,local rumors,Egypt location,departure sequence,urgency,Janus fear and exact FI substitution,Fernando commercial reasoning,and the earlier warning. Native8100atB31offset132queries completion132;the positive branch reaches Lil recognition of the B132barkeep warning. The unsupported Clifford attribution is removed. Barkeep ojisan does not become invented kinship. Gerhard two private thoughts remain separate conditional objects without naming the man. All34 have fresh glosses,localization notes,exact clean/current/integrated references andallfive per-record review gates. Complete source-bound preambles preserve ordinary actor2/4/9/16/20/28/31/92/113,including printable71/5C,without changing global profiles or native code. No relationship,new rank,casualty,guaranteed future war orselected player action is invented. Current checks bind34complete native/independent216x64planes,272logical/compiled macro alignment cases and136additional final-parity cases. All leading,interior andtrailing glyphs,blank paper,origin0,16pxrows,bounds andsingle-page limits pass. Four visual phrase-flow findings from2737are resolved in unwrapped prose by2738;2739reruns four planes/32macro cases and reuses30unchanged planes/240cases under exact input/runtime/profile hashes. Allfive sheets were viewed orhash-identical. Eleven individual source-line-count notes remain;no orphan,predicate,weak-ending,control,overflow,missing-glyph orblank-page waiver is granted. All91native command types,complete headers,32relative spans/160relocated cases and every unowned logical byte are preserved. Eight original predicates execute at their relocated addresses with identical operands,results andevent-getter arguments0/1/2. The diagnostic2747/2747bstops are preserved;2747c proves incidental r3is the exactly mapped source-command cursor. The original unaligned-read helper may copy only the proven four-byte operand to source-owned02279600scratch through2A5D8;restoring that word recovers the entire4MiB context. Actor,event,roster,RNG andunowned state remain exact. All336whole SC2load/cache cases and672parent-entry modes pass for parent and research images. Three shipped entry censuses bind the original interpreter call with no literal alias. B30grows592to680bytes,B31grows800to848,andB132grows484to524;333other blocks remain exact. Historical Lil/Gerhard complete ink,gray andblank-mask samples are reused through exact ARM9/COMMON/font/B74 identity. Prior current V2724Lil/town startup and unchangedB22 provide separate inherited representative evidence. Historical menu/FE samples are context only;all34new speeches use ordinary54020progressive. No new translation-specific display/control finding requires individual conditional ornew speaker-nameplate visits under the user representative policy. No B30/B31/B132activation ornew nameplate observation is claimed. Inherited travel/funds access fixtures and five-ship town battery remain disclosed andunearned. One guarded optional stage extends the full V2724stack. Seventeen negative cases reject before mutation. Registered V2750contains497batches/114accepted layers;onlySC2B30/B31/B132changes fromV2724. ARM9,COMMON,every other file/component,graphics,fonts,section/BSS/cache extents and123040staged bytes remain exact. The clean-input xdelta reconstructs the whole registered ROM byte for byte. Every prior profile and V1492promotion is preserved. Two new targeted headless cold boots complete4001LilNewGame and17401town/Refitframes. All31captured whole framebuffers match V2724;five postload actor/captain controls,Lil2andresidentB22payload,andsource/disposable town-donor hashes pass. The town sample uses the inherited five-ship Copenhagen battery and ends at the Refit component screen. The six-frame current sheet was viewed. No new RAM/code/gameplay fixture,observer orsavestate is used;no deep-story,full-route orhardware claim is made. Fresh coverage is2310 reread /2310 integrated-reconciled /zero pending. Completion is2310(1614historically revised,696retained);source/prose remains2313. Completed file counts are1599COMMON,483SC2,117SC0,73SC1and38SC3. All711reviewed route objects are now integrated. Three marketCOMMON750-752remain incomplete;every untouched storyline,shared shop/town dialogue,random scene andremaining player-facing prose remains in scope. All ROMs,earlier translations,canonical/clean inputs andexecuted proofs are preserved. Five named-target2187-2191leads remain uncredited. Raw rejected-object classification,SC3B109,separate graphics/all18plaques andlater older-record technical re-audit remain open. Full goal active;all jobs terminal.'

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    prior=Path('work/analysis/editorial_handoff_verification_v2742/verified_handoff.json')
    assert sha(lp.read_bytes())==read(prior)['ledger_sha256']
    release,start=read(RELEASE),read(START)
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all497_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V2724'] and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_B30_B31_B132_IDs']==[] and sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    # The six current frames were viewed before executing this producer.
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':22,'retain-wording':12}
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
            integrated_hex=value.hex(),completed_candidate_reference=release['candidate'],registered_prose_owner='lil_post_seville_editorial',
            registered_manuscript=str(DOC),
            historical_editorial_decision='revise' if row['editorial_decision']=='revise' else 'retain',
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            individual_actual_activation_not_claimed=True,all_source_native_representative_and_registered_gates_pass=True,
            status='complete-contextual-current-native-references-representative-and-registered-release')
        row['current_English']=value[1:].decode('ascii')
        if row['kind']!='typed-choice-label':
            row['current_record_index']=row['record_index']=reference['record_index']
    selected={(r['file_path'],r['id']) for r in rows};fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert len(selected)==34 and {(r['file_path'],r['id']) for r in fresh['pending_record_keys']}==selected
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2310,2276,34)
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert not oldkeys&selected
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2741')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    review=ROOT/'current_six_frame_visual_review.json';save(review,dict(sheet=start['review_sheet'],sha256=start['review_sheet_sha256'],viewed=True,
        findings='Lil selection and opening dialogue and inherited town/Refit component screens are legible and match V2724. Current startup only; no B30/B31/B132 activation.'))
    proofpaths=[DOC,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['representative_proof']),Path(doc['historical_representative_sheet_review']),Path(doc['prior_current_sheet_review']),RELEASE,START,prior,review,Path(__file__),
        Path('work/analysis/lil_post_Seville_registration_v2749/registration_receipt.json'),Path('work/analysis/lil_post_Seville_registration_v2749/negative_cases.json'),
        Path('work/analysis/lil_post_Seville_research_v2744/research_image_receipt.json'),
        Path('work/analysis/lil_post_Seville_reference_census_v2746/all91_commands32_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_post_Seville_loader_v2745/whole_SC2_and_B30_B31_B132_initial_entry_proof.json')]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    save(FINAL,dict(format='dk4-natural-dialogue-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        id=FAMILY,manuscript=str(DOC),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        revised=22,retained=12,records=rows,summary=SUMMARY,evidence=evidence,actual_B30_B31_B132_IDs=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=0,current_six_frame_sheet_viewed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[30,31,132],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),revised_count=22,retained_count=12,fresh_revisions=22,fresh_retentions=12,
        actual_verification_scope='Historical shared progressive rules plus two current cold-start/story/town samples. Menu/FE are context-only; all34are progressive. No B30/B31/B132 activation.',records=rows))
    ledger.update(records_editorially_completed=2310,records_revised_and_integrated=1614,retained_wordings_editorially_completed=696)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=483
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][p]=[ident for ident in ids if ('/data/SC2.DK4',ident) not in selected]
    for p in [DOC]:
        if str(p) not in active['manuscripts']:active['manuscripts'].append(str(p))
        active['route_record_subsets_pending'][str(p)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='2310fresh rereads integrated/reconciled;source/prose2313. MarketCOMMON750-752caller context unresolved;all wider untouched prose remains in scope.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=2310,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=34,final_review=str(FINAL),new_revisions=22,justified_retentions=12,new_completed_records=34,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=22,retained=12),actual_B30_B31_B132_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0))
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=711,completed_route_records=711,next='Continue untouched route/shared/town/random/player prose. All-route review remains open.')
        if unit['id']=='Lil-post-Seville-and-Egypt-warning-B30-B31-B132-34':unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,completion_credit_added=34,final_review=str(FINAL),full_goal_complete=False)
    watch=ledger['formatting_watchlist']['lil_post_Seville_v2741']
    watch.update(status='complete-through-V2754',reference_map_pending=False,
        representative_reconciliation_pending=False,superseded_by='lil_post_Seville_v2754',final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_post_Seville_v2754']=dict(status='all34-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),evidence=evidence,
        actual_B30_B31_B132_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,no_orphan_predicate_or_missing_glyph_waivers=True)
    oldcandidate=deepcopy(ledger['current_integrated_candidate']);ledger['previous_current_integrated_candidate_before_V2750']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(oldcandidate)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False,
        **{key+'_sha256':digest for key,digest in release['story_hashes'].items()})
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2741']['path']))
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,
        next_focus='Continue untouched source/story exchanges beyond Seville and shared shop/town/random/player prose;marketCOMMON750-752callers andraw rejected-object classification remain open.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=711,completed_route_records=711,source_prose_pending_records=0,source_prose_pending_family=None,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2754']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,full_goal_complete=False)
    ledger['lil_post_Seville_completion_v2754']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}=={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert len(keys)==len(fresh['integrated_record_keys'])==2310
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2313
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    release_note=('Release details: experimental profile `'+release['profile']+'`. Candidate `'+release['candidate']+'`, SHA-256 `'+release['candidate_sha256']+'`. '
        'Canonical base `'+release['canonical_base']+'`, SHA-256 `'+release['canonical_base_sha256']+'`. '
        'Clean-input patch `'+release['patch']+'`, SHA-256 `'+release['patch_sha256']+'`. '
        'The manifest enumerates all497 batches and114 accepted layers, including the full V2724 stack and the new34-speech manuscript. '
        'Internal delta from V2724: `/data/SC2.DK4` blocks30/31/132 only; every other file and component is exact. '
        'Verifiers: source/relocation/reference/native-font/padding checks,17 compiler rejections, `verify_lil_post_seville_release_v2751.py` and `verify_lil_post_seville_startup_v2753.py`. '
        'Current cold-boot areas are title/character selection,Lil opening,andtown/Refit. Human cold-boot acceptance is still required for promotion; V1492 remains promoted.\n\n')
    section='## V2754:34 post-Seville and Egypt-warning entries completed in V2750\n\n'+SUMMARY+'\n\n'+release_note+'Final review: '+FINAL.as_posix()+'. Release/patch: '+RELEASE.as_posix()+'. Current startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Current COMMON parser remains dk4tool.patch.surrender_advice_contextual_v1.current_entries;bounded context remains scripts/current_common_native_context_v2677.py because ARM9/COMMON are byte-identical.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V2754' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2754',summary=SUMMARY,evidence={**evidence,str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=34,new_source_prose_reviews=0,revisions=22,justified_retentions=12,
        fresh_reread=2310,fresh_integrated=2310,fresh_pending=0,source_prose=2313,completed=2310,historical_revised=1614,historical_retained=696,incomplete_COMMON=3,incomplete_route=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        actual_B30_B31_B132_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2754:34completed in registeredV2750;22revisions/12retentions;2310reread/integrated,source/prose2313. COMMON3andall wider prose remain open;full goal active.')
