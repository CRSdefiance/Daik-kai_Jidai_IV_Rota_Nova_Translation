"""Save34fresh reviews and verified14-byte research growth without release credit."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/aftermath_remaining_checkpoint_v2670')
OLD=Path('translations/aftermath_remaining_contextual_editorial_manuscript_v1.json')
DOC=Path('translations/aftermath_remaining_contextual_editorial_manuscript_v2.json')
FONT=Path('work/analysis/aftermath_remaining_fonts_v2668/native_layout_and_font_research.json')
PAYLOAD=Path('work/analysis/surrender_advice_payload_v2669/payload_plan.json')
FAMILY='Battle-aftermath-remaining34-contextual-native-release-pending'
SUMMARY=(
    'V2670 freshly reviews34 previously incomplete aftermath records:1994-2010,2022-2037,and2192. '
    'All clean Japanese is read in five distinct event families,not as a34line conversation. '
    'Town surrender preserves the original town name,physical First Mate demand,town representative white-flag reply and member report; '
    'an empty physical First Mate emits only the original fallback report. '
    'Fresh source tests bind1035 original voice choices,114 native town names and228 assigned/unassigned exchange prefixes. '
    'The assigned path uses one disclosed original-setter duty byte in copied RAM;no town surrender is claimed activated. '
    'Flagship defeat remains distinct from boarding capture;explicit sinking belongs to2004. Flooding warnings do not prematurely assert sinking or death. '
    'Ship surrender uses the original flagship captain or model spokesperson and concerns its own ship,not the entire fleet. '
    'All34 have fresh individual glosses and localization reasons. Thirty-three current paragraphs are retained. '
    'One proposed2029 correction restores the emphatic courteous recommendation ofするがよろしかろう: '
    'You cannot win! I suggest you surrender at once! replaces You cannot win! Surrender at once! '
    'No named person,rank,relationship,casualty count,weapon,prisoner-treatment promise or new outcome is invented. '
    'Current native tests pass712 paragraph/name layouts,including684 real-town cases,34 complete native/independent font planes,34 current deployed consumer pipelines and68 current cold/warm copies. '
    'All four sheets with34 full previews were viewed. Whole first/final/interior glyphs,blank paper,x6 margins,35-cell/four-row bounds and16px stride pass. '
    'No actual-town orphan or weak line ending remains;old synthetic-name waivers are historical only and are not transferred. '
    'The2029 font test initially used proposed input while its current deployed pipeline still loaded the old wording;these boundaries remain explicit. '
    'The new source-locked research payload then repacks only COMMON22 from5378to5392 bytes and updates only directory/offset metadata. '
    'All3667 other complete native copies and40other blocks remain exact;all other ARM9 bytes restore exactly,with code,font,geometry,sections,BSS,cache and123040-byte staged payload unchanged. '
    'The revised2029 now executes its complete original direct-actor selection/loader/printf/macro/wrap pipeline against the research payload. '
    'All123 repacked records pass246 cold/warm copies. No playable ROM is created. '
    'Fresh metadata separates the frozen source/prose predecessor fields,current deployed bytes,and proposed compiled bytes;no historical artifact is overwritten. '
    'The first2666 source probe refused an assumed newer config schema;preserved2666b uses the original owner dependency hash. '
    'Registered successor integration,exact clean-input patch,required startup checks and final representative event/transition reconciliation remain pending. '
    'Next add one optional registered stage after the full V2284 stack,using the reviewed manuscript and verified payload;do not edit the old owner config or build from a derivative ROM. '
    'Fresh coverage is2184 reread /2150 integrated-reconciled /34pending. Completion2150(1504revised,646retained),source/prose2259 and incompleteCOMMON109 are unchanged. '
    'These34 already belonged to source/prose coverage and gain no duplicate credit. '
    'The registered cumulative experimentalV2284 remains493batches/114accepted layers with its existing exactly reconstructable clean-input patch. '
    'ROM,registry,builder,profiles,manifest and patch are unchanged;V1492 remains promoted,all ROMs and earlier translations are preserved. '
    'No new current emulator run,actual surrender,earned duty assignment,current startup,full-route or hardware proof is claimed. '
    'All never-reviewed storylines,shared shop/town dialogue,random scenes and remaining player-facing prose stay in scope,including five separately uncredited named-target leads2187-2191. '
    'Separate graphics/all18 plaques,raw rejected-record coverage,SC3B109 classification and later older-record technical re-audit remain open. '
    'Full goal active;all jobs terminal.'
)

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    prior_audit_path=Path('work/analysis/editorial_handoff_verification_v2665/verified_handoff.json');prior=read(prior_audit_path)
    assert sha(lp.read_bytes())==prior['ledger_sha256']
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2150,2150,0)
    doc=deepcopy(read(OLD));font,plan=read(FONT),read(PAYLOAD)
    assert font['manuscript_sha256']==plan['manuscript_sha256']==sha(OLD.read_bytes())
    assert len(font['cases'])==712 and len(font['complete_native_planes'])==len(font['current_deployed_original_pipelines'])==34
    assert len(font['current_deployed_cold_warm_copies'])==68 and font['findings']==[]
    assert len(plan['native_cold_warm_copies_all123_repacked_records'])==246 and plan['actual_changed_message_IDs']==[2029]
    assert plan['new2029_loaded_template_hex']==next(r['proposed_compiled_hex'] for r in doc['records'] if r['message_id']==2029)
    for p in [Path(plan['target_ARM9']),Path(plan['target_COMMON'])]:
        key='target_ARM9_sha256' if p.suffix=='.bin' else 'target_COMMON_sha256';assert sha(p.read_bytes())==plan[key]
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    registered={r['message_id']:r for r in read(doc['registered_prose_owner_bindings'][0]['manuscript'])['records']}
    for row in doc['records']:
        n=row['message_id'];oldrow=registered[n]
        row['historical_source_prose_predecessor_fields']={k:oldrow[k] for k in ['current_reference','current_text_hex','current_English','compiled_hex','unwrapped_paragraph_hex'] if k in oldrow}
        raw=bytes.fromhex(row['current_hex']);assert raw.startswith(b' ')
        row.update(current_text_hex=row['current_hex'],current_English=raw[1:].decode('ascii'),
            compiled_hex=row['proposed_compiled_hex'],unwrapped_paragraph_hex=row['english'].encode('ascii').hex(),
            current_native_font_case=next(c for c in font['complete_native_planes'] if c['message_ID']==n),
            current_deployed_original_pipeline=next(c for c in font['current_deployed_original_pipelines'] if c['message_ID']==n),
            status='fresh-contextual-and-native-reviewed;representative-and-registered-release-pending',
            native_formatting_checked=True,new_current_visit=False,completion_credit_added=0)
        row['review']['formatting']=True
        if n==2029:row['research_payload_original_pipeline']=plan['new2029_complete_source_selected_direct_actor_loader_printf_macro_wrap_pipeline']
    doc.update(formatting_review_pending=False,status='34fresh-contextual-native-checked;one-prose-revision-payload-ready;registered-release-and-representative-scope-pending',
        current_native_font_proof=str(FONT),current_native_font_proof_sha256=sha(FONT.read_bytes()),
        revision_payload_plan=str(PAYLOAD),revision_payload_plan_sha256=sha(PAYLOAD.read_bytes()),
        prior_contextual_draft=str(OLD),prior_contextual_draft_sha256=sha(OLD.read_bytes()),
        all34_native_previews_viewed_on_four_sheets=True,revision_native_loader_and_copy_verified_in_research_only=True,
        current_native_and_representative_reconciliation_pending=True,registered_revision_integration_pending=True)
    validate_natural_dialogue_batch(doc)
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text().startswith('# Current editorial handoff - V2664')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    save(DOC,doc)
    ids=[r['message_id'] for r in doc['records']];selected=[dict(file_path='/COMMON/MESFILE.DK4',id=f'COMMON_MESSAGE_{n}') for n in ids]
    keys={(r['file_path'],r['id']) for r in fresh['record_keys']};assert all((r['file_path'],r['id']) not in keys for r in selected)
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(r['id'] for r in selected)
    pending=dict(id=FAMILY,records=34,record_keys=selected,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        proposed_revision_IDs=[2029],retentions=33,native_proof=str(FONT),payload_plan=str(PAYLOAD),
        pending='Representative event/transition reconciliation;new optional registered stage/profile after V2284;full cumulative build,exact clean patch andrequired startup checks.',
        source_prose_and_completed_credit_added=0,new_emulator_runs=0)
    fresh.update(fresh_pass_records_explicitly_reread=2184,fresh_pass_records_integrated=2150,fresh_pass_records_pending_native_actual_release=34,
        pending_record_keys=selected,pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,latest_contextual_manuscript=str(DOC),
        coverage_note='2184fresh contextual rereads include2150reconciled completions and34aftermath records pending representative/release completion. One2029tone revision is research-payload verified,not in the current playable ROM. Source/prose2259 and incompleteCOMMON109 unchanged. Full wider objective remains active.')
    active=ledger['active_source_prose_drafts'];active['manuscripts'].append(str(DOC));active['manuscript_record_subsets_pending'][str(DOC)]=ids;active['note']=fresh['coverage_note']
    ledger['latest_checkpoint']=SUMMARY;ledger['aftermath_remaining_contextual_v2670']=dict(summary=SUMMARY,**pending,goal_turn_classification='progress',full_goal_complete=False)
    ledger['formatting_watchlist']['aftermath_remaining_v2670']=dict(status='current-and-research-native-pass;representative-release-pending',manuscript=str(DOC),proposed_revision_IDs=[2029],payload_plan=str(PAYLOAD),no_runtime_code_or_geometry_change=True)
    save(lp,ledger)
    requirements=ROOT/'next_registered_integration_requirements.json';save(requirements,dict(parent_profile='all-routes-unified-v2284',
        source_ROM=doc['current_ROM'],source_ROM_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        payload_plan=str(PAYLOAD),payload_plan_sha256=sha(PAYLOAD.read_bytes()),revised_IDs=[2029],reviewed_IDs=ids,
        metadata_only_repack_COMMON22_growth14_native_copies_verified=True,
        preserve_all_previous_profiles_accepted114_promotedV1492_and_every_ROM=True,
        source_locks='Clean Japanese and immutable canonical baseline;full existing V2284 stage before the new optional override. Preserve old owner config/manuscript and all historical pins.',
        next='Bind representative direct/member/numeric town/ship aftermath controls. Add registered prose-only override and experimental profile;build through build_integrated_release.py;verify exact target pair,whole manifest/ancestry,all unselected copies,clean-input patch reconstruction and required cold startup samples. Then reconcile34 if all required gates pass.',
        no_new_ROM_profile_or_registration_created_here=True,full_goal_complete=False))
    section='## V2670: Aftermath34 fresh review;advisory-tone revision payload ready\n\n'+SUMMARY+'\n\nReviewed manuscript: '+DOC.as_posix()+'. Native proof: '+FONT.as_posix()+'. Payload: '+PAYLOAD.as_posix()+'. Next integration: '+requirements.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text().split('\n',1);p.write_text(('# Current editorial handoff - V2670' if i==0 else first)+'\n\n'+section+rest,newline='\n')
    paths=[OLD,DOC,FONT,PAYLOAD,requirements,Path(plan['target_ARM9']),Path(plan['target_COMMON']),
        Path(doc['source_context_packet']),Path(doc['native_context_proof']),Path(doc['fresh_ordinary_supplement']),
        prior_audit_path,Path(__file__),Path('scripts/prepare_aftermath_remaining_context_v2666b.py'),
        Path('scripts/review_aftermath_remaining_v2667.py'),Path('scripts/verify_aftermath_remaining_fonts_v2668.py'),
        Path('scripts/prepare_surrender_advice_payload_v2669.py'),*[Path(s['path']) for s in font['review_sheets']]]
    release=read('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json')
    assert sha(Path(doc['current_ROM']).read_bytes())==release['candidate_sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V2670',summary=SUMMARY,fresh_reread=2184,fresh_integrated=2150,fresh_pending=34,
        new_completed_records=0,proposed_prose_revisions=1,justified_retention_drafts=33,source_prose=2259,incomplete_COMMON=109,
        evidence={str(p):sha(p.read_bytes()) for p in paths},updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        no_playable_ROM_registry_builder_profile_manifest_or_patch_change=True,all_jobs_terminal=True,new_emulator_runs=0,
        goal_turn_classification='progress',full_goal_complete=False))
    print('V2670:2184reread/2150reconciled/34pending;one research-verified2029tone revision;current playable ROM and release stack unchanged;full goal active.')
