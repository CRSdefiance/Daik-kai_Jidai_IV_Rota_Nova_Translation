"""Complete16 retained reports with explicit native/representative scope."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.surrender_advice_contextual_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.ship_sinking_native_plan_v1330 import compiled
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ship_sinking_completion_v2686')
OLD=Path('translations/ship_sinking_contextual_editorial_manuscript_v1.json')
DOC=Path('translations/ship_sinking_contextual_editorial_manuscript_v2.json')
FINAL=Path('translations/ship_sinking_contextual_final_review_v1.json')
FONT=Path('work/analysis/ship_sinking_fonts_v2683/native_font_and_pipeline_proof.json')
SAMPLE=Path('work/analysis/ship_sinking_sampling_v2684/representative_control_and_rgb_reconciliation.json')
PALETTE=Path('work/analysis/ship_sinking_palette_v2685/palette_review.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2674 Ship sinking16 contextual retentions verified')
IDS=list(range(2058,2074));FAMILY='Ship-sinking16-contextual-completed'
SUMMARY=(
    'V2686 completes16 previously incomplete named-vessel sinking reports2058-2073 as fresh individually justified retentions. '
    'Clean Japanese and complete original status/projectile event contexts preserve ongoing2059going under versus completed sinking,passive was sunk,explicit Admiral addresses andexcited enemy success. '
    'No ship ownership,weapon,crew deaths,rank,kinship orwhole-fleet victory is invented. '
    'Two original consumers,414valid actor/voice choices,five current historical-model live name providers/four unique names,twelve original speaker-getter argument cases,andthe captured18-byte rename cap are source-bound. '
    'The cap does not certify arbitrary legacy names or every keyboard page. '
    'Current native tests pass496 whole original selection/loader/printf/macro/wrap pipelines andcomplete228x64native/independent planes for31names per record. '
    'All416earlier full-palette cases match exactly;80additional current-name/percent-data cases pass. ASCII lengths1-18,macro-like names,apostrophes,CJK/full-width names andinserted percent text remain literal andcomplete. '
    'Source strings keep exactly one%s argument andcompiler-owned guards. Ordered first/final/interior glyphs,blank paper,x6 inset,35cells/four rows and16px stride pass,with no orphan orweak line end. '
    'Eight own-report voice alternatives use original-setter one-duty-byte CPU fixtures;the eight enemy-report alternatives pass existing original actor objects directly. '
    'All actor models remain exact;all executed pipeline instructions are current-ROM exact under bounded immutable overlays. These are not earned duty or gunner assignments. '
    'Thirty-two cold/warm native copies pass. Twenty-two complete preview cases on three sheets were viewed. '
    'Four additional source-palette previews preserve native gray detail,including Japanese andfull-width names. Binary coverage masks andcolor previews are labeled distinctly;no font/graphics defect orasset change is inferred. '
    'Four preserved historical named-target capture2082androle1defeat2138holds freshly match current full native ink,gray-shadow andblank RGB masks. '
    'Original55DC4(attacker,8),virtual ship-name getter+4,Hanse Cog,Hull30/Crew0,andactual Charles18 are freshly verified for the capture sample;it is not sinking. '
    'Nine offline corruptions reject erased first/final glyphs,wrong name through the current pipeline,andstray ink/gray pixels. '
    'The named-target return to sailing androle1defeat/title return remain historical representative samples. Constructor/return/status/projectile/getter code is clean/current/historical exact. '
    'The representative sheet was viewed. Under the user representative-sampling policy,the established member/direct/named-target panel rules plus exhaustive current native checks leave no new translation-specific display/control finding that requires a conditional sinking visit. '
    'Earlier gunnery pilots that showed no sinking notice still receive no sinking credit. No actual sinking ID,new emulator run,forced Hull/crew/RNG/result,current startup,earned qualification,full-route orhardware claim is made. '
    'All16 reconcile through existing registered ship_sinking_editorial/manuscriptv4;there are zero current prose ormetadata revisions andno ROM build. '
    'Fresh coverage is2200 reread /2200 integrated-reconciled /zero pending. Completion is2200(1535historically revised,665retained);source/prose2259 andincompleteCOMMON59 reconcile exactly. '
    'The16new completions comprise8historically revised and8retained entries;this fresh pass retains all16current paragraphs. '
    'Registered cumulative experimentalV2674 remains494batches/114accepted layers with its exactly reconstructable clean-input patch. ROM,runtime,geometry,registry,builder,profile,manifest andpatch are unchanged;V1492 remains promoted. '
    'All ROMs,earlier translations,andcanonical/clean inputs are preserved. '
    'Remaining drafts are market3,ship-loss/surrender24 andbattle-reactions32. Five named-target2187-2191leads remain separately uncredited. '
    'Every never-reviewed storyline,shared shop/town dialogue,random scene andremaining player-facing prose stays in scope. '
    'Separate graphics/all18 plaques,raw rejected-record coverage,SC3B109 classification andlater older-record technical re-audit remain open. Full goal active;all jobs terminal.'
)

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,DOC,FINAL,GUIDE])
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    prior_audit_path=Path('work/analysis/editorial_handoff_verification_v2680/verified_handoff.json');prior=read(prior_audit_path)
    assert sha(lp.read_bytes())==prior['ledger_sha256']
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2184,2184,0)
    doc=deepcopy(read(OLD));font,sample,palette=map(read,[FONT,SAMPLE,PALETTE])
    assert font['manuscript_sha256']==sha(OLD.read_bytes()) and len(font['cases'])==496 and len(font['all32_current_cold_warm_copies'])==32 and font['findings']==[]
    assert sample['no_open_translation_specific_display_or_control_finding'] and len(sample['historical_holds'])==4 and len(sample['negative_controls'])==9
    assert all(c['rejected'] for c in sample['negative_controls']) and sample['actual_sinking_IDs']==[]
    sheets=font['review_sheets']+[dict(path=palette['review_sheet'],sha256=palette['review_sheet_sha256']),dict(path=sample['review_sheet'],sha256=sample['review_sheet_sha256'])]
    assert len(sheets)==5
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    owner=doc['registered_prose_owner_bindings'][0];source_rows={r['message_id']:r for r in read(owner['manuscript'])['records']}
    assert Counter(source_rows[n]['editorial_decision'] for n in IDS)=={'revise':8,'retain':8}
    rompath=Path(doc['current_ROM']);image=NdsImage.open(rompath);entries=current_entries(image.read_file('/COMMON/MESFILE.DK4'),image.read_file('/__arm9__.bin'))
    for row in doc['records']:
        n=row['message_id'];assert compiled(row)==entries[n].text
        row['review']['formatting']=True
        row.update(status='complete-contextual-current-native-representative-and-registered-retention',
            integrated_hex=row['current_hex'],integrated_reference=row['current_reference'],completed_candidate_reference=str(rompath),
            decision='revised-and-integrated' if source_rows[n]['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            current_complete_native_cases=[c for c in font['cases'] if c['message_ID']==n],
            actual_sinking_holds=[],individual_actual_activation_not_claimed=True,
            all_source_native_representative_and_registered_gates_pass=True)
    doc.update(formatting_review_pending=False,current_native_and_representative_reconciliation_pending=False,
        status='complete-contextual-current-native-and-registered-retention',
        current_native_font_proof=str(FONT),current_native_font_proof_sha256=sha(FONT.read_bytes()),
        representative_reconciliation=str(SAMPLE),representative_reconciliation_sha256=sha(SAMPLE.read_bytes()),
        palette_review=str(PALETTE),palette_review_sha256=sha(PALETTE.read_bytes()),
        all_five_review_sheets_viewed=True,actual_sinking_IDs=[],new_emulator_runs=0,completion_credit_added=16,source_prose_credit_added=0)
    validate_natural_dialogue_batch(doc)
    releasepath=Path('work/analysis/surrender_advice_release_v2675/registered_release_verification.json');release=read(releasepath)
    assert sha(rompath.read_bytes())==release['candidate_sha256']==doc['current_ROM_sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text().startswith('# Current editorial handoff - V2679')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    save(DOC,doc)
    paths=[OLD,DOC,FONT,SAMPLE,PALETTE,releasepath,Path(owner['config']),Path(owner['manuscript']),
        Path(doc['source_context_packet']),Path(doc['native_context_proof']),Path(doc['fresh_ordinary_supplement']),
        prior_audit_path,Path(__file__),*[Path(s['path']) for s in sheets]]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    save(FINAL,dict(format='dk4-editorial-final-review-v1',family=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=IDS,
        revised_count=0,retained_count=16,new_completed_records=16,historical_decisions_newly_completed=dict(revised=8,retained=8),
        records=doc['records'],summary=SUMMARY,evidence=evidence,registered_prose_owner_binding=owner,
        candidate=str(rompath),candidate_sha256=release['candidate_sha256'],profile='all-routes-unified-v2674',patch=release['patch'],patch_sha256=release['patch_sha256'],
        whole_clean_input_reconstruction_exact=True,no_ROM_registry_builder_profile_manifest_or_patch_change=True,
        current_original_pipeline_and_full_font_cases=496,current_cold_warm_copies=32,historical_representative_IDs=[2082,2138],
        historical_full_palette_holds=4,negative_controls=9,actual_sinking_IDs=[],new_emulator_runs=0,all_review_sheets_viewed=True,full_goal_complete=False))
    existing={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};selected={('/COMMON/MESFILE.DK4',r['id']) for r in doc['records']}
    assert len(selected)==16 and not selected&existing
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=IDS,
        record_IDs=[r['id'] for r in doc['records']],final_review=str(FINAL),revised_count=8,retained_count=8,
        fresh_revisions=0,fresh_retentions=16,actual_verification_scope='496current native cases andshared named-target/direct/member historical controls;no individual sinking activation claim.',records=doc['records']))
    ledger['records_editorially_completed']=2200;ledger['records_revised_and_integrated']=1535;ledger['retained_wordings_editorially_completed']=665
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=1543
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    active=ledger['active_source_prose_drafts'];active['native_message_IDs']=[n for n in active['native_message_IDs'] if n not in IDS]
    for key,ns in active['manuscript_record_subsets_pending'].items():active['manuscript_record_subsets_pending'][key]=[n for n in ns if n not in IDS]
    newkeys=[dict(file_path='/COMMON/MESFILE.DK4',id=r['id']) for r in doc['records']]
    fresh['record_keys'].extend(newkeys);fresh['record_IDs'].extend(r['id'] for r in doc['records'])
    fresh.update(fresh_pass_records_explicitly_reread=2200,fresh_pass_records_integrated=2200,fresh_pass_records_pending_native_actual_release=0,
        integrated_record_keys=deepcopy(fresh['record_keys']),pending_record_keys=[],pending_contextual_families=[],latest_pending_contextual_family=None,
        latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),latest_contextual_retention_review=str(FINAL),
        coverage_note='2200fresh rereads andreconciliations;16new sinking-report completions retain their current English. Source/prose2259 and59incompleteCOMMON remain;all broader never-reviewed prose andfive named-target leads stay in scope.')
    fresh['reconciled_families'].append(dict(id=FAMILY,records=16,final_review=str(FINAL),new_revisions=0,justified_retentions=16,
        new_completed_records=16,historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=8,retained=8),
        actual_sinking_IDs=[],new_emulator_runs=0,current_original_pipeline_and_full_font_cases=496))
    active['note']=fresh['coverage_note'];ledger['latest_checkpoint']=SUMMARY
    ledger['ship_sinking_contextual_v2686']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['formatting_watchlist']['ship_sinking_contextual_v2686']=dict(status='complete-current-native-representative-and-registered-retention',final_review=str(FINAL),no_runtime_or_geometry_change=True)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2679']['path']))
    inventory['incomplete_COMMON_source_prose_groups']=[g for g in inventory['incomplete_COMMON_source_prose_groups'] if g['family']!='ship-sinking-unfinished']
    inventory.update(incomplete_COMMON_count=59,next_focus='Review market3,ship-loss/surrender24 andbattle-reactions32,then all never-reviewed route/shared/town/shop/random/player-facing prose,including thefive uncredited named-target outcomes. This is not the entire source universe.')
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    assert {n for g in inventory['incomplete_COMMON_source_prose_groups'] for n in g['IDs']}==set(ledger['reviewed_but_incomplete_COMMON_IDs']) and sum(g['count'] for g in inventory['incomplete_COMMON_source_prose_groups'])==59
    ledger['unfinished_editorial_scope_v2686']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=59,full_goal_complete=False)
    save(lp,ledger)
    section='## V2686: Ship-sinking16 contextual retentions completed\n\n'+SUMMARY+'\n\nFinal review: '+FINAL.as_posix()+'. Current native proof: '+FONT.as_posix()+'. Representative full RGB: '+SAMPLE.as_posix()+'. Palette preview: '+PALETTE.as_posix()+'. Current parser: dk4tool.patch.surrender_advice_contextual_v1.current_entries. Current bounded context: scripts/current_common_native_context_v2677.py. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text().split('\n',1);p.write_text(('# Current editorial handoff - V2686' if i==0 else first)+'\n\n'+section+rest,newline='\n')
    GUIDE.mkdir(parents=True);images=[]
    for i,s in enumerate(sheets):
        kind='current-native-coverage-mask' if i<3 else 'current-native-source-palette' if i==3 else 'historical-other-family-not-sinking'
        target=GUIDE/(kind+'_'+Path(s['path']).name);copy2(s['path'],target);images.append(dict(path=str(target),sha256=s['sha256'],kind=kind))
    save(GUIDE/'scope.json',dict(candidate=str(rompath),candidate_sha256=release['candidate_sha256'],images=images,
        actual_sinking_IDs=[],new_emulator_runs=0,native_controlled_and_historical_scopes_distinct=True,full_goal_complete=False))
    evidence.update({str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())})
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2686',summary=SUMMARY,new_completed_records=16,new_current_prose_revisions=0,fresh_justified_retentions=16,
        historical_revisions_newly_completed=8,historical_retentions_newly_completed=8,fresh_reread=2200,fresh_integrated=2200,fresh_pending=0,
        completed_records=2200,historical_revised=1535,historical_retained=665,source_prose_reviewed=2259,COMMON_incomplete=59,
        candidate=str(rompath),candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],guide=str(GUIDE),
        evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs,DOC,FINAL]},goal_turn_classification='progress',
        actual_sinking_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V2686:16new completions/retentions;2200fresh reconciled,1535historical revisions/665retentions;2259source/prose,59incompleteCOMMON.2674ROM/patch unchanged;full goal active.')
