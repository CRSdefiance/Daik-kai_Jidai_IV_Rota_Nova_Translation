"""Reconcile32 unchanged paragraphs after current native/visual/source gates."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.surrender_advice_contextual_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_reaction_native_plan_v1484 import compiled,IDS
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_reactions_completion_v2699')
OLD=Path('translations/battle_reactions_contextual_editorial_manuscript_v1.json')
DOC=Path('translations/battle_reactions_contextual_editorial_manuscript_v2.json')
FINAL=Path('translations/battle_reactions_contextual_final_review_v1.json')
FONT=Path('work/analysis/battle_reactions_fonts_v2697/native_font_and_pipeline_proof.json')
SAMPLE=Path('work/analysis/battle_reactions_sampling_v2698/representative_reconciliation.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2674 Battle reactions32 contextual retentions verified')
FAMILY='Battle-reactions32-contextual-completed'
SUMMARY=(
    'V2699 completes32 previously incomplete battle reactions2147-2178 as fresh individually justified retentions. '
    'Each clean Japanese paragraph was reread in its complete original event context:two alternative battle-setup tables,own-ship-hit surprise andinjury. These are not32consecutive replies. '
    'Readiness,promises,confident boasts,confusion,stammers,pain,blood andregret remain distinct;piece of cake naturally preserves the Japanese easy-task idiom. The rough injury exclamation does not invent a tactical failure. '
    'No rank,relationship,weapon,attacker,death,healing orguaranteed victory is added. All32have new individual glosses andreasons for retaining their current English. '
    'Fresh source tests bind828actor/voice choices andfour original direct-actor tables. Optional setup RNG100==0,mood/voice gates andactor24exclusion remain exact. Other stored voices are not automatically claimed reachable through that caller. Surprise andpersistent-injury branches retain their original probability,10-14HPchange andhealth-state processing;no health,RNG,mood,eligibility,result or identity is forced. '
    'Current tests pass32whole original selection/loader/printf/macro/wrap pipelines andcomplete228x64native/independent font planes. All32historical formatted bytes,lines andfull-palette planes match. Zero original arguments/macros,complete ordered glyphs,uniform x6 margins,35cells/four rows,16px stride andblank paper pass withzero orphans orweak ends. Existing original actor objects are supplied directly;allactor models andexecuted current instructions remain exact under bounded immutable overlays. '
    'Sixty-four cold/warm copies and14compiler rejection controls pass. All32complete previews ontwo sheets were viewed. The2695bsource successor clarifies mood/voice wording while preserving2695andits proof. '
    'The still-current completed V2684proof is reused without repeating emulator/RGBexecution:four historical actual2082direct/named-target and2138role1holds match whole current ink,gray detail andblank masks,withnine rejected corruptions andnormal-return evidence. The representative sheet was viewed. These IDs are other reports,not selected reaction activation. '
    'Original reaction predicates,constructor andreturn code are clean exact. Under the user representative-sampling policy,no new translation-specific display/control finding requires individual conditional visits. No selected32activation,new emulator run,current startup,earned qualification,full-route orhardware claim is made. '
    'All32reconcile through existing registered battle_reaction_editorial/manuscriptv2 withzero current prose ormetadata changes andno ROM build. '
    'Fresh coverage is2256 reread /2256 integrated-reconciled /zero pending. Completion is2256(1575historically revised,681retained);source/prose2259 and3incompleteCOMMON reconcile. These32comprise16historical revisions and16retentions;this fresh pass retains all32. '
    'Registered cumulative experimentalV2674 remains494batches/114accepted layers with its exactly reconstructable clean-input patch. ROM,runtime,geometry,registry,builder,profile,manifest andpatch are unchanged;V1492 remains promoted. All ROMs,earlier translations,andcanonical/clean inputs are preserved. '
    'The remaining source/prose draft is market3. Five named-target2187-2191leads remain separately uncredited. Every never-reviewed storyline,shared shop/town dialogue,random scene andremaining player-facing prose stays in scope. '
    'Separate graphics/all18 plaques,raw rejected-record coverage,SC3B109 classification andlater older-record technical re-audit remain open. Full goal active;all jobs terminal.'
)
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,DOC,FINAL,GUIDE])
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);priorpath=Path('work/analysis/editorial_handoff_verification_v2694/verified_handoff.json');prior=read(priorpath)
    assert sha(lp.read_bytes())==prior['ledger_sha256'];fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2224,2224,0)
    doc=deepcopy(read(OLD));font,sample=map(read,[FONT,SAMPLE])
    assert font['manuscript_sha256']==sha(OLD.read_bytes()) and len(font['cases'])==32 and len(font['all64_current_cold_warm_copies'])==64 and font['findings']==[]
    assert len(font['invalid_compiler_inputs'])==14 and all(c['all_prior_formatted_bytes_lines_and_full_palette_plane_equal'] for c in font['cases'])
    assert sample['no_open_translation_specific_display_or_control_finding'] and len(sample['reused_historical_holds'])==4 and len(sample['reused_negative_controls'])==9
    assert sample['actual_selected_reaction_IDs']==[] and all(c['rejected'] for c in sample['reused_negative_controls'])
    sheets=font['review_sheets']+[dict(path=sample['review_sheet'],sha256=sample['review_sheet_sha256'])]
    assert len(sheets)==3
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    owner=doc['registered_prose_owner_bindings'][0];source_rows={r['message_id']:r for r in read(owner['manuscript'])['records']}
    assert Counter(source_rows[n]['editorial_decision'] for n in IDS)=={'revise':16,'retain':16}
    rompath=Path(doc['current_ROM']);image=NdsImage.open(rompath);entries=current_entries(image.read_file('/COMMON/MESFILE.DK4'),image.read_file('/__arm9__.bin'))
    for row in doc['records']:
        n=row['message_id'];assert compiled(row)==entries[n].text
        row['review']['formatting']=True
        row.update(status='complete-contextual-current-native-representative-and-registered-retention',integrated_hex=row['current_hex'],integrated_reference=row['current_reference'],completed_candidate_reference=str(rompath),decision='revised-and-integrated' if source_rows[n]['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            current_complete_native_cases=[c for c in font['cases'] if c['message_ID']==n],actual_selected_reaction_holds=[],individual_actual_activation_not_claimed=True,all_source_native_representative_and_registered_gates_pass=True)
    doc.update(formatting_review_pending=False,current_native_and_representative_reconciliation_pending=False,status='complete-contextual-current-native-and-registered-retention',current_native_font_proof=str(FONT),current_native_font_proof_sha256=sha(FONT.read_bytes()),
        representative_reconciliation=str(SAMPLE),representative_reconciliation_sha256=sha(SAMPLE.read_bytes()),all_three_review_sheets_viewed=True,actual_selected_reaction_IDs=[],new_emulator_runs=0,completion_credit_added=32,source_prose_credit_added=0)
    validate_natural_dialogue_batch(doc)
    releasepath=Path('work/analysis/surrender_advice_release_v2675/registered_release_verification.json');release=read(releasepath)
    assert sha(rompath.read_bytes())==release['candidate_sha256']==doc['current_ROM_sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2693')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    save(DOC,doc)
    paths=[OLD,DOC,FONT,SAMPLE,releasepath,Path(owner['config']),Path(owner['manuscript']),Path(doc['source_context_packet']),Path(doc['native_context_proof']),Path(doc['fresh_ordinary_supplement']),priorpath,Path(__file__),*[Path(s['path']) for s in sheets]]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    save(FINAL,dict(format='dk4-editorial-final-review-v1',family=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=list(IDS),revised_count=0,retained_count=32,new_completed_records=32,historical_decisions_newly_completed=dict(revised=16,retained=16),
        records=doc['records'],summary=SUMMARY,evidence=evidence,registered_prose_owner_binding=owner,candidate=str(rompath),candidate_sha256=release['candidate_sha256'],profile='all-routes-unified-v2674',patch=release['patch'],patch_sha256=release['patch_sha256'],
        whole_clean_input_reconstruction_exact=True,no_ROM_registry_builder_profile_manifest_or_patch_change=True,current_original_pipeline_and_full_font_cases=32,current_cold_warm_copies=64,compiler_rejections=14,historical_representative_IDs=[2082,2138],reused_historical_full_palette_holds=4,reused_negative_controls=9,actual_selected_reaction_IDs=[],new_emulator_runs=0,all_review_sheets_viewed=True,full_goal_complete=False))
    existing={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};selected={('/COMMON/MESFILE.DK4',r['id']) for r in doc['records']}
    assert len(selected)==32 and not selected&existing
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=list(IDS),record_IDs=[r['id'] for r in doc['records']],final_review=str(FINAL),revised_count=16,retained_count=16,fresh_revisions=0,fresh_retentions=32,
        actual_verification_scope='32current whole native/font cases,64copies and14compiler controls;still-current shared historical RGBproof reused. No selected32reaction activation claim.',records=doc['records']))
    ledger.update(records_editorially_completed=2256,records_revised_and_integrated=1575,retained_wordings_editorially_completed=681)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=1599
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    active=ledger['active_source_prose_drafts'];active['native_message_IDs']=[n for n in active['native_message_IDs'] if n not in IDS]
    for key,ns in active['manuscript_record_subsets_pending'].items():active['manuscript_record_subsets_pending'][key]=[n for n in ns if n not in IDS]
    fresh['record_keys'].extend(dict(file_path='/COMMON/MESFILE.DK4',id=r['id']) for r in doc['records']);fresh['record_IDs'].extend(r['id'] for r in doc['records'])
    fresh.update(fresh_pass_records_explicitly_reread=2256,fresh_pass_records_integrated=2256,fresh_pass_records_pending_native_actual_release=0,integrated_record_keys=deepcopy(fresh['record_keys']),pending_record_keys=[],pending_contextual_families=[],latest_pending_contextual_family=None,
        latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),latest_contextual_retention_review=str(FINAL),coverage_note='2256fresh rereads andreconciliations;32new reaction completions retain current English. Source/prose2259 and3incompleteCOMMON remain;all never-reviewed prose andfive named-target leads stay in scope.')
    fresh['reconciled_families'].append(dict(id=FAMILY,records=32,final_review=str(FINAL),new_revisions=0,justified_retentions=32,new_completed_records=32,historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=16,retained=16),actual_selected_reaction_IDs=[],new_emulator_runs=0,current_original_pipeline_and_full_font_cases=32))
    active['note']=fresh['coverage_note'];ledger['latest_checkpoint']=SUMMARY
    ledger['battle_reactions_contextual_v2699']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['formatting_watchlist']['battle_reactions_contextual_v2699']=dict(status='complete-current-native-representative-and-registered-retention',final_review=str(FINAL),no_runtime_or_geometry_change=True)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2693']['path']))
    inventory['incomplete_COMMON_source_prose_groups']=[g for g in inventory['incomplete_COMMON_source_prose_groups'] if g['family']!='battle-reactions-unfinished']
    inventory.update(incomplete_COMMON_count=3,next_focus='Review market3,then all never-reviewed route/shared/town/shop/random/player-facing prose,including thefive uncredited named-target outcomes. This is not the entire source universe.')
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    assert {n for g in inventory['incomplete_COMMON_source_prose_groups'] for n in g['IDs']}==set(ledger['reviewed_but_incomplete_COMMON_IDs']) and sum(g['count'] for g in inventory['incomplete_COMMON_source_prose_groups'])==3
    ledger['unfinished_editorial_scope_v2699']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,full_goal_complete=False);save(lp,ledger)
    section='## V2699: Battle reactions32 contextual retentions completed\n\n'+SUMMARY+'\n\nFinal review: '+FINAL.as_posix()+'. Current native proof: '+FONT.as_posix()+'. Reused representative evidence: '+SAMPLE.as_posix()+'. Current parser: dk4tool.patch.surrender_advice_contextual_v1.current_entries. Current bounded context: scripts/current_common_native_context_v2677.py. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1);p.write_text(('# Current editorial handoff - V2699' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    GUIDE.mkdir(parents=True);images=[]
    for i,s in enumerate(sheets):
        kind='current-native-coverage-mask' if i<2 else 'historical-other-ID-not-selected32'
        target=GUIDE/(kind+'_'+Path(s['path']).name);copy2(s['path'],target);images.append(dict(path=str(target),sha256=s['sha256'],kind=kind))
    save(GUIDE/'scope.json',dict(candidate=str(rompath),candidate_sha256=release['candidate_sha256'],images=images,actual_selected_reaction_IDs=[],new_emulator_runs=0,native_controlled_and_historical_scopes_distinct=True,full_goal_complete=False))
    evidence.update({str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())})
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2699',summary=SUMMARY,new_completed_records=32,new_current_prose_revisions=0,fresh_justified_retentions=32,historical_revisions_newly_completed=16,historical_retentions_newly_completed=16,
        fresh_reread=2256,fresh_integrated=2256,fresh_pending=0,completed_records=2256,historical_revised=1575,historical_retained=681,source_prose_reviewed=2259,COMMON_incomplete=3,candidate=str(rompath),candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],guide=str(GUIDE),
        evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs,DOC,FINAL]},goal_turn_classification='progress',actual_selected_reaction_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V2699:32new retentions/completions;2256fresh reconciled,1575historical revisions/681retentions;2259source/prose,3incompleteCOMMON.2674ROM/patch unchanged;full goal active.')
