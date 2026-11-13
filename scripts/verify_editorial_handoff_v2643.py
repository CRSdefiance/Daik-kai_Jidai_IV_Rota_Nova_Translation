"""Final audit with corrected two-speaker context and both receipt hash chains."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/verify_editorial_handoff_v2640.py').read_text()
 changes={
  "ROOT=Path('work/analysis/editorial_handoff_verification_v2640')":"ROOT=Path('work/analysis/editorial_handoff_verification_v2643')",
  "receiptpath=Path('work/analysis/sighting_completion_v2639/completion_receipt.json')":"receiptpath=Path('work/analysis/sighting_context_correction_v2642/completion_receipt.json')",
  "receipt['fresh_reconciliations']==receipt['justified_retentions']==15":"receipt['fresh_reconciliations']==receipt['justified_retentions']==0 and receipt['previous_editorial_batch_retained']==15",
  "fp=Path('translations/sighting_contextual_final_review_v1.json')":"fp=Path('translations/sighting_contextual_final_review_v2.json')",
  "np=Path('translations/sighting_contextual_editorial_manuscript_v2.json')":"np=Path('translations/sighting_contextual_editorial_manuscript_v3.json')",
  "fonts=read('work/analysis/sighting_fonts_v2637b/current2700_native_wrap_and_font_reconciliation.json')":"fonts=read('work/analysis/sighting_fonts_v2641/native_font_proof.json')",
  "handoff.startswith('# Current editorial handoff - V2639')":"handoff.startswith('# Current editorial handoff - V2642')",
  "checkpoint='V2639'":"checkpoint='V2642',retentions_checkpoint='V2639'",
  'Independent V2639 audit passes':'Independent V2642 audit passes',
 }
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 needle=" before=Path('work/analysis/sighting_completion_v2639/editorial_review_current_v1.json.before')"
 assert source.count(needle)==1
 extra=""" previous_receipt_path=Path(receipt['previous_retention_receipt']);assert sha(previous_receipt_path.read_bytes())==receipt['previous_retention_receipt_sha256'];previous_receipt=read(previous_receipt_path);assert previous_receipt['fresh_reconciliations']==previous_receipt['justified_retentions']==15
 for p,digest in previous_receipt['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
 for p,digest in previous_receipt['updated_files'].items():
  current=Path(p)
  if sha(current.read_bytes())!=digest:assert sha((Path('work/analysis/sighting_context_correction_v2642')/(current.name+'.before')).read_bytes())==digest,p
 correction_before=read('work/analysis/sighting_context_correction_v2642/editorial_review_current_v1.json.before');assert correction_before['contextual_story_natural_dialogue_pass_v1871']['record_keys']==fresh['record_keys']and correction_before['contextual_story_natural_dialogue_pass_v1871']['record_IDs']==fresh['record_IDs']
"""
 source=source.replace(needle,extra+needle)
 needle=" history=read(notes['historical_current_binding'])"
 assert source.count(needle)==1
 extra=""" assert fonts['corrected_unchanged_Charles18_pipeline_IDs']==[614,622]and fonts['unchanged_2700_matrix_15font_planes_30copies_and_other13_pipelines_hash_bound'];prior_font_path=Path(fonts['supersedes_native_speech_fixture_scope']);assert sha(prior_font_path.read_bytes())==fonts['supersedes_native_speech_fixture_scope_sha256'];prior_fonts=read(prior_font_path)
 for p,q in zip(fonts['all15_original_role1_speech_pipelines'],prior_fonts['all15_original_role1_speech_pipelines'],strict=True):
  if p['message_ID']in[614,622]:assert p['original_actor_choice']['actor_ID']==18 and p['CPU_only_voice_fixture']['no_roster_fixture']and p['native_pipeline']['formatted_hex']==q['native_pipeline']['formatted_hex']
  else:assert p==q
 for key in['cases','all15_complete_native_cases','fresh_current_native_full_font_samples','all30_native_cold_warm_copies','review_sheets','invalid_compiler_inputs_rejected']:assert fonts[key]==prior_fonts[key]
"""
 source=source.replace(needle,extra+needle)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
