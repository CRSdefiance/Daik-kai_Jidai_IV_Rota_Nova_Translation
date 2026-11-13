"""Correct a documented speaker title from clean Japanese without changing prose."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.dialogue.review import validate_natural_dialogue_batch
ROOT=Path('work/analysis/palace_guard_metadata_v2266');LEDGER=Path('translations/editorial_review_current_v1.json')
OLD=Path('translations/palace_inn_contextual_editorial_manuscript_v2.json');NOTES=Path('translations/palace_inn_contextual_editorial_manuscript_v3.json')
PREVIOUS=Path('translations/palace_inn_contextual_final_review_v1.json');FINAL=Path('translations/palace_inn_contextual_final_review_v2.json')
CONTEXT=Path('work/analysis/ceremony_context_v2264c/native_context.json')
SUMMARY=('V2266 corrects Palace speaker metadata:building role11/actor121 is clean Japanese衛兵,current Guard. The earlier minister label in Palace research/manuscripts was an inference andis superseded. Current native town/role lookup andsource name-record references establish the correction. No translated dialogue addresses the speaker as minister,so all54 Palace/Inn English paragraphs stay exact;no new review credit,ROM,profile,registry,manifest orpatch change. Source facts andNPC names take precedence over the earlier inferred title. '
 'Notes-only Palace/Inn v3 andfinal reviewv2 preserve the preceding frozen versions andretain every exact source/current span,individual retention reason,display proof andactual/historical scope. Fresh coverage1290 reconciled/0pending,historical2143,source/prose2259 and116 incompleteCOMMON unchanged. Next ceremony52 packet remains uncredited andpending fresh whole-exchange/native/representative-family reconciliation. '
 'Current V2171 remains492batches/114accepted layers with exact clean-input patch;all ROMs/earlier translations preserved,V1492 promoted andcanonical/clean unchanged. Full objective remains active,including every storyline/shared town/shop/random/player prose. Separate graphics/all18 plaques,SC3B109 classification andlater older-record technical re-audit stay open.')
if __name__=='__main__':
    assert not any(p.exists()for p in(ROOT,NOTES,FINAL));l=read(LEDGER);old=read(OLD);prior=read(PREVIOUS);context=read(CONTEXT)
    npc,=[r for r in context['town_role_name_mappings']if r['town_ID']==22 and r['role']==11];assert npc['actor_ID']==121 and npc['clean_name']=='衛兵'and npc['current_name']=='Guard'
    palace=read('work/analysis/palace_context_v2250d/native_context.json');assert npc['actor_pointer']==palace['minister_role11_actor121']
    f=l['contextual_story_natural_dialogue_pass_v1871'];assert(f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(1290,0)
    docs=[Path('docs')/p for p in('editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md')];ROOT.mkdir(parents=True)
    for p in[LEDGER,*docs]:(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
    proof=ROOT/'source_bound_guard_identity.json';save(proof,dict(current_context=str(CONTEXT),current_context_sha256=sha(CONTEXT.read_bytes()),source_bound_NPC=npc,prior_numerically_correct_but_mislabeled_field='minister_role11_actor121',source_Japanese='衛兵',current_approved_English='Guard',no_source_rank_minister=True,all54_English_paragraphs_unchanged=True,metadata_only_no_new_coverage_or_ROM=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    notes=deepcopy(old);changes=[]
    for r in notes['records']:
        before={k:r[k]for k in('speaker','context','localization_note','fresh_retained_wording_justification')};after={k:v.replace('minister','guard').replace('Minister','Guard')for k,v in before.items()}
        if before!=after:r.update(after);changes.append(dict(message_ID=r['message_id'],before=before,after=after));r['speaker_metadata_correction']=str(proof)
    assert changes and [r['english']for r in notes['records']]==[r['english']for r in old['records']]
    notes.update(previous_complete_manuscript=str(OLD),previous_complete_manuscript_sha256=sha(OLD.read_bytes()),speaker_identity_correction=str(proof),final_review=str(FINAL));validate_natural_dialogue_batch(notes);save(NOTES,notes)
    final=deepcopy(prior);final.update(records=notes['records'],summary=prior['summary'].replace('minister11/121','guard11/121')+' '+SUMMARY,previous_final_review=str(PREVIOUS),previous_final_review_sha256=sha(PREVIOUS.read_bytes()),speaker_metadata_correction=str(proof),source_bound_guard_metadata_complete=True)
    final['evidence'].update({str(p):sha(p.read_bytes())for p in(NOTES,proof,PREVIOUS,CONTEXT,Path(__file__))});save(FINAL,final)
    f.update(latest_contextual_manuscript=str(NOTES),latest_contextual_retention_review=str(FINAL),latest_final_review=str(FINAL))
    for row in f['reconciled_families']:
        if row['final_review']==str(PREVIOUS):row['final_review']=str(FINAL);row['speaker_metadata_correction']=str(proof)
    l['palace_inn_contextual_v2261']['latest_corrected_final_review']=str(FINAL);l['palace_guard_metadata_v2266']=dict(summary=SUMMARY,proof=str(proof),notes=str(NOTES),final_review=str(FINAL),changed_metadata_records=len(changes),new_coverage_credit=0,full_goal_complete=False);l['latest_checkpoint']=SUMMARY;save(LEDGER,l)
    section='## V2266: Source-bound Palace guard metadata correction\n\n'+SUMMARY+'\n\nIdentity proof: '+proof.as_posix()+'. Corrected complete review: '+FINAL.as_posix()+'. Continue the52-entry ceremony packet at work/analysis/ceremony_context_source_v2262/all52_clean_current_context_catalog.json. Current ceremony source replay2264c records hero-dependent towns andNPC providers;unpositioned hero inputs may return town115 anddo not prove valid-town orfacility eligibility. No new actual ceremony visit has yet been claimed.\n\n'
    text=docs[0].read_text();assert text.startswith('# Current editorial handoff - V2263');first,rest=text.split('\n',1);docs[0].write_text('# Current editorial handoff - V2266\n\n'+section+rest,newline='\n')
    for p in docs[1:]:
        first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+section+rest,newline='\n')
    save(ROOT/'correction_receipt.json',dict(checkpoint='V2266',classification='progress',changed_metadata_records=changes,fresh_integrated=1290,new_coverage_credit=0,no_English_or_ROM_change=True,updated_files={str(p):sha(p.read_bytes())for p in[LEDGER,*docs,NOTES,FINAL,proof]},full_goal_complete=False));print(dict(checkpoint='V2266',changed_speaker_metadata=len(changes),English_unchanged=True,fresh_integrated=1290,new_credit=0))
