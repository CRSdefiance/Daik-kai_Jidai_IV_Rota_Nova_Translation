"""Reconcile24 unchanged paragraphs after current native/visual/source gates."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.surrender_advice_contextual_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.ship_loss_surrender_native_plan_v1444 import compiled,IDS
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ship_loss_completion_v2693')
OLD=Path('translations/ship_loss_contextual_editorial_manuscript_v1.json')
DOC=Path('translations/ship_loss_contextual_editorial_manuscript_v2.json')
FINAL=Path('translations/ship_loss_contextual_final_review_v1.json')
FONT=Path('work/analysis/ship_loss_fonts_v2690b/native_font_and_pipeline_proof.json')
SAMPLE=Path('work/analysis/ship_loss_sampling_v2692/representative_reconciliation.json')
PALETTE=Path('work/analysis/ship_loss_palette_v2691/palette_review.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2674 Ship loss surrender24 contextual retentions verified')
FAMILY='Ship-loss-surrender24-contextual-completed'
SUMMARY=(
    'V2693 completes24 previously incomplete capture and surrender reports2074-2081and2090-2105 as fresh individually justified retentions. '
    'The clean Japanese and complete original status-event context preserve capture versus surrender versus sinking,all Admiral addresses,and formal,familiar,rough,distressed andolder-style voices. '
    'These are three alternative eight-voice families.2091/2103/2105retain apparent surrender;2099keeps the observed white flag followed by inference;2104keeps reported intent. '
    'No rank,relationship,weapon,crew death,fleet-wide outcome orpermanent prize ownership is invented. '
    'Fresh source tests bind621actor/voice choices,three original role1tables,five live name providers/four unique names,andthe captured18-byte rename cap. This cap does not certify every keyboard page orlegacy name. '
    'Current native tests pass768whole selection/loader/printf/macro/wrap pipelines andcomplete228x64native/independent font planes for32names per record. All624historical full-palette cases match;144additional cases pass. '
    'Stored text has no authored leading guard;the formatter supplies it. The sole original%s,all ordered glyphs,x6 margin,35cells/four rows,16px stride andblank paper pass. Complete proper-name-plus-punctuation final rows receive individual exact-case justifications;partial names andisolated predicates/titles receive no waiver. '
    'Three voice0reports use unchanged logicalCharles18withanempty physicalFirstMate;21other choices use disclosed original-setter one-duty-byte CPU fixtures. Actor models andexecuted current instructions remain exact under bounded immutable overlays;earned staffing is not claimed. '
    'Forty-eight current cold/warm copies andeight COMMON22/23boundary-cache checks pass. Thirty selected coverage previews onthree sheets andsix source-palette previews onone sheet were viewed. '
    'Initial2690stopped before pipelines because historical own/enemy26-name sets have27names inunion;preserved2690buses the correct32-name combined catalog. No failure receives completion credit. '
    'The still-current V2684representative proof is reused without new emulator/RGBexecution:four historical actual2082named-target capture and2138role1defeat holds match whole current ink,gray detail andblank masks,withnine rejected corruptions andnormal-return evidence. Its sheet was viewed. '
    'These are other report IDs,not activation of these24. Original72484surrender probability,7251Cstatus processing,constructor andreturn code remain clean exact. No new translation-specific display/control finding requires individual conditional visits under the user sampling policy. '
    'No selected24activation,new emulator run,forced Hull/crew/RNG/result,current startup,full-route orhardware claim is made. '
    'All24reconcile through registered ship_loss_surrender_editorial/manuscriptv3 withzero current prose ormetadata changes andno ROM build. '
    'Fresh coverage is2224 reread /2224 integrated-reconciled /zero pending. Completion is2224(1559historically revised,665retained);source/prose2259 and35incompleteCOMMON reconcile. These24were historically revised;this fresh pass retains all24. '
    'Registered cumulative experimentalV2674 remains494batches/114accepted layers with its exactly reconstructable clean-input patch. ROM,runtime,geometry,registry,builder,profile,manifest andpatch are unchanged;V1492 remains promoted. All ROMs,earlier translations,andcanonical/clean inputs are preserved. '
    'Remaining drafts are market3andbattle-reactions32. Five named-target2187-2191leads remain separately uncredited. Every never-reviewed storyline,shared shop/town dialogue,random scene andremaining player-facing prose stays in scope. '
    'Separate graphics/all18 plaques,raw rejected-record coverage,SC3B109 classification andlater older-record technical re-audit remain open. Full goal active;all jobs terminal.'
)
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,DOC,FINAL,GUIDE])
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);priorpath=Path('work/analysis/editorial_handoff_verification_v2687/verified_handoff.json');prior=read(priorpath)
    assert sha(lp.read_bytes())==prior['ledger_sha256'];fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2200,2200,0)
    doc=deepcopy(read(OLD));font,sample,palette=map(read,[FONT,SAMPLE,PALETTE])
    assert font['manuscript_sha256']==sha(OLD.read_bytes()) and len(font['cases'])==768 and len(font['all48_current_cold_warm_copies'])==48 and font['findings']==[]
    assert len(font['COMMON22_23_boundary_cache_sequence'])==8 and sum(c['matches_prior_full_native_case'] for c in font['cases'])==624
    assert sample['no_open_translation_specific_display_or_control_finding'] and len(sample['reused_historical_holds'])==4 and len(sample['reused_negative_controls'])==9
    assert sample['actual_selected_capture_surrender_IDs']==[] and all(c['rejected'] for c in sample['reused_negative_controls'])
    sheets=font['review_sheets']+[dict(path=palette['review_sheet'],sha256=palette['review_sheet_sha256']),dict(path=sample['review_sheet'],sha256=sample['review_sheet_sha256'])]
    assert len(sheets)==5 and len(palette['samples'])==6
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    owner=doc['registered_prose_owner_bindings'][0];source_rows={r['message_id']:r for r in read(owner['manuscript'])['records']}
    assert Counter(source_rows[n]['editorial_decision'] for n in IDS)=={'revise':24}
    rompath=Path(doc['current_ROM']);image=NdsImage.open(rompath);entries=current_entries(image.read_file('/COMMON/MESFILE.DK4'),image.read_file('/__arm9__.bin'))
    for row in doc['records']:
        n=row['message_id'];assert compiled(row)==entries[n].text
        row['review']['formatting']=True
        row.update(status='complete-contextual-current-native-representative-and-registered-retention',integrated_hex=row['current_hex'],integrated_reference=row['current_reference'],completed_candidate_reference=str(rompath),decision='revised-and-integrated',
            current_complete_native_cases=[c for c in font['cases'] if c['message_ID']==n],actual_selected_capture_surrender_holds=[],individual_actual_activation_not_claimed=True,all_source_native_representative_and_registered_gates_pass=True)
    doc.update(formatting_review_pending=False,current_native_and_representative_reconciliation_pending=False,status='complete-contextual-current-native-and-registered-retention',current_native_font_proof=str(FONT),current_native_font_proof_sha256=sha(FONT.read_bytes()),
        representative_reconciliation=str(SAMPLE),representative_reconciliation_sha256=sha(SAMPLE.read_bytes()),palette_review=str(PALETTE),palette_review_sha256=sha(PALETTE.read_bytes()),all_five_review_sheets_viewed=True,actual_selected_capture_surrender_IDs=[],new_emulator_runs=0,completion_credit_added=24,source_prose_credit_added=0)
    validate_natural_dialogue_batch(doc)
    releasepath=Path('work/analysis/surrender_advice_release_v2675/registered_release_verification.json');release=read(releasepath)
    assert sha(rompath.read_bytes())==release['candidate_sha256']==doc['current_ROM_sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2686')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    save(DOC,doc)
    paths=[OLD,DOC,FONT,SAMPLE,PALETTE,releasepath,Path(owner['config']),Path(owner['manuscript']),Path(doc['source_context_packet']),Path(doc['native_context_proof']),Path(doc['fresh_ordinary_supplement']),priorpath,Path(__file__),*[Path(s['path']) for s in sheets]]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    save(FINAL,dict(format='dk4-editorial-final-review-v1',family=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=list(IDS),revised_count=0,retained_count=24,new_completed_records=24,historical_decisions_newly_completed=dict(revised=24,retained=0),
        records=doc['records'],summary=SUMMARY,evidence=evidence,registered_prose_owner_binding=owner,candidate=str(rompath),candidate_sha256=release['candidate_sha256'],profile='all-routes-unified-v2674',patch=release['patch'],patch_sha256=release['patch_sha256'],
        whole_clean_input_reconstruction_exact=True,no_ROM_registry_builder_profile_manifest_or_patch_change=True,current_original_pipeline_and_full_font_cases=768,current_cold_warm_copies=48,boundary_cache_checks=8,historical_representative_IDs=[2082,2138],reused_historical_full_palette_holds=4,reused_negative_controls=9,actual_selected_capture_surrender_IDs=[],new_emulator_runs=0,all_review_sheets_viewed=True,full_goal_complete=False))
    existing={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};selected={('/COMMON/MESFILE.DK4',r['id']) for r in doc['records']}
    assert len(selected)==24 and not selected&existing
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=list(IDS),record_IDs=[r['id'] for r in doc['records']],final_review=str(FINAL),revised_count=24,retained_count=0,fresh_revisions=0,fresh_retentions=24,
        actual_verification_scope='768current native cases;still-current named-target/member historical RGBcontrols reused. No selected24capture/surrender activation claim.',records=doc['records']))
    ledger.update(records_editorially_completed=2224,records_revised_and_integrated=1559,retained_wordings_editorially_completed=665)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=1567
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    active=ledger['active_source_prose_drafts'];active['native_message_IDs']=[n for n in active['native_message_IDs'] if n not in IDS]
    for key,ns in active['manuscript_record_subsets_pending'].items():active['manuscript_record_subsets_pending'][key]=[n for n in ns if n not in IDS]
    fresh['record_keys'].extend(dict(file_path='/COMMON/MESFILE.DK4',id=r['id']) for r in doc['records']);fresh['record_IDs'].extend(r['id'] for r in doc['records'])
    fresh.update(fresh_pass_records_explicitly_reread=2224,fresh_pass_records_integrated=2224,fresh_pass_records_pending_native_actual_release=0,integrated_record_keys=deepcopy(fresh['record_keys']),pending_record_keys=[],pending_contextual_families=[],latest_pending_contextual_family=None,
        latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),latest_contextual_retention_review=str(FINAL),coverage_note='2224fresh rereads andreconciliations;24new capture/surrender completions retain current English. Source/prose2259 and35incompleteCOMMON remain;all never-reviewed prose andfive named-target leads stay in scope.')
    fresh['reconciled_families'].append(dict(id=FAMILY,records=24,final_review=str(FINAL),new_revisions=0,justified_retentions=24,new_completed_records=24,historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=24,retained=0),actual_selected_capture_surrender_IDs=[],new_emulator_runs=0,current_original_pipeline_and_full_font_cases=768))
    active['note']=fresh['coverage_note'];ledger['latest_checkpoint']=SUMMARY
    ledger['ship_loss_contextual_v2693']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['formatting_watchlist']['ship_loss_contextual_v2693']=dict(status='complete-current-native-representative-and-registered-retention',final_review=str(FINAL),no_runtime_or_geometry_change=True)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2686']['path']))
    inventory['incomplete_COMMON_source_prose_groups']=[g for g in inventory['incomplete_COMMON_source_prose_groups'] if g['family']!='ship-loss-surrender-unfinished']
    inventory.update(incomplete_COMMON_count=35,next_focus='Review market3andbattle-reactions32,then all never-reviewed route/shared/town/shop/random/player-facing prose,including thefive uncredited named-target outcomes. This is not the entire source universe.')
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    assert {n for g in inventory['incomplete_COMMON_source_prose_groups'] for n in g['IDs']}==set(ledger['reviewed_but_incomplete_COMMON_IDs']) and sum(g['count'] for g in inventory['incomplete_COMMON_source_prose_groups'])==35
    ledger['unfinished_editorial_scope_v2693']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=35,full_goal_complete=False);save(lp,ledger)
    section='## V2693: Ship-loss and surrender24 contextual retentions completed\n\n'+SUMMARY+'\n\nFinal review: '+FINAL.as_posix()+'. Current native proof: '+FONT.as_posix()+'. Reused representative evidence: '+SAMPLE.as_posix()+'. Palette preview: '+PALETTE.as_posix()+'. Current parser: dk4tool.patch.surrender_advice_contextual_v1.current_entries. Current bounded context: scripts/current_common_native_context_v2677.py. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1);p.write_text(('# Current editorial handoff - V2693' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    GUIDE.mkdir(parents=True);images=[]
    for i,s in enumerate(sheets):
        kind='current-native-coverage-mask' if i<3 else 'current-native-source-palette' if i==3 else 'historical-other-ID-not-selected24'
        target=GUIDE/(kind+'_'+Path(s['path']).name);copy2(s['path'],target);images.append(dict(path=str(target),sha256=s['sha256'],kind=kind))
    save(GUIDE/'scope.json',dict(candidate=str(rompath),candidate_sha256=release['candidate_sha256'],images=images,actual_selected_capture_surrender_IDs=[],new_emulator_runs=0,native_controlled_and_historical_scopes_distinct=True,full_goal_complete=False))
    evidence.update({str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())})
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2693',summary=SUMMARY,new_completed_records=24,new_current_prose_revisions=0,fresh_justified_retentions=24,historical_revisions_newly_completed=24,historical_retentions_newly_completed=0,
        fresh_reread=2224,fresh_integrated=2224,fresh_pending=0,completed_records=2224,historical_revised=1559,historical_retained=665,source_prose_reviewed=2259,COMMON_incomplete=35,candidate=str(rompath),candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],guide=str(GUIDE),
        evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs,DOC,FINAL]},goal_turn_classification='progress',actual_selected_capture_surrender_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V2693:24new retentions/completions;2224fresh reconciled,1559historical revisions/665retentions;2259source/prose,35incompleteCOMMON.2674ROM/patch unchanged;full goal active.')
