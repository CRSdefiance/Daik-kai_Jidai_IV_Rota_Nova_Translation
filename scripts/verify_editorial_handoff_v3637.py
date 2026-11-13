"""Independently freeze the59-review checkpoint without release or gameplay credit."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3637')
CHECKPOINT=Path('work/analysis/lil_B152_B154_checkpoint_v3636')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,d in receipt[group].items():assert sha(Path(p).read_bytes())==d,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256']
    previous=read(prior['handoff_receipt']);assert sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,d in previous['updated_files'].items():assert sha((CHECKPOINT/(Path(p).name+'.before')).read_bytes())==d,p
    for k in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286']:assert ledger[k]==before[k],k
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];old=before['contextual_story_natural_dialogue_pass_v1871'];reviewed={historical_key(r) for r in fresh['record_keys']};integrated={historical_key(r) for r in fresh['integrated_record_keys']};pending={historical_key(r) for r in fresh['pending_record_keys']};completed=[r for g in ledger['completed_editorial_families'] for r in g['records']]
    assert len(reviewed)==len(fresh['record_keys'])==5128 and len(integrated)==len(completed)==5069 and len(pending)==59 and reviewed==integrated|pending and not integrated&pending
    assert fresh['integrated_record_keys']==old['integrated_record_keys'] and fresh['record_keys'][:5069]==old['record_keys'] and (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5128,5069,59)
    assert (ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'],ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5131,5131,5069,3297,1772)
    counts=dict(before['source_prose_reviewed_counts_by_file']);counts['/data/SC2.DK4']+=59;assert ledger['source_prose_reviewed_counts_by_file']==counts and sum(counts.values())==5131 and counts['/data/SC2.DK4']==3275 and counts['/data/SC3.DK4']==64
    unit=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert (unit['reviewed_route_records'],unit['completed_route_records'])==(3529,3470)
    family=fresh['pending_contextual_families'];assert len(family)==1;family=family[0];doc=read(family['manuscript']);rows=doc['records'];assert family['records']==len(rows)==59 and {historical_key(r) for r in rows}==pending and Counter(r['editorial_decision'] for r in rows)=={'revise':22,'retain-wording':37}
    candidate=ledger['current_integrated_candidate'];rom=NdsImage.open(candidate['path']);clean=NdsImage.open('work/clean.nds');blocks=IlnkContainer.parse(rom.read_file('/data/SC2.DK4')).blocks;jp=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==doc['current_ROM_sha256']==prior['candidate_sha256'] and sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==prior['patch_sha256']
    manifest=read(candidate['manifest']);registry=read('translations/release_stack.json');assert manifest['profile']==candidate['profile']=='all-routes-unified-v3607' and len(manifest['batches'])==528 and all(manifest['checks'].values()) and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    context=read(doc['source_context']);gloss={r['id']:r for r in read(doc['whole_exchange_context_notes'])['records']};assert len(context['records'])==len(gloss)==59 and context['source_native_commands']==104 and context['source_relative_sites']==8 and doc['fresh_source_glosses_precede_current_comparison_and_localized_English']
    assert Counter(r['block'] for r in rows)=={152:6,153:9,154:44} and {r['source_selector'] for r in rows}=={2,9,14,17,20,92,115,148}
    for r in rows:
        assert all(r['review'].values()) and r['fresh_source_gloss']==r['source_meaning']==gloss[r['id']]['fresh_source_gloss'] and r['whole_exchange_context']==gloss[r['id']]['whole_exchange_context'] and r['full_clean_context_precedes_comparison']
        for key,hexkey,bank in [('source_reference','source_hex',jp),('current_reference','current_hex',blocks)]:
            at=r[key]['offset'];v=bytes.fromhex(r[hexkey]);b=bank[r['block']];assert b[at:at+len(v)]==v and b[at+len(v)]==0 and b[at-5:at+1].hex()==r['source_complete_preamble_hex']
        assert all(bytes.fromhex(r['source_hex']).count(k.encode())==r['english'].count('{MACRO:'+k+'}') for k in ['FI','FA','FO'])
        if r['editorial_decision']=='retain-wording':assert r['fresh_retained_wording_justification'] and r['english'].split('}',1)[1]==r['effective_predecessor_macro_paragraph']==r['effective_predecessor_paragraph']
    assert sum(bytes.fromhex(r['source_hex']).count(b'FI') for r in rows)==3 and sum(bytes.fromhex(r['source_hex']).count(b'FA') for r in rows)==1
    font=read(doc['native_font_proof']);assert sha(Path(doc['native_font_proof']).read_bytes())==doc['native_font_proof_sha256'] and len(font['cases'])==59 and font['current_original_macro_alignment_calls']==472 and len(font['source_consumer_negative_controls'])==25 and len(font['source_bound_formatter_negatives'])==14
    for c in font['cases']:assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and16px_rows_within4rows'] and sha(Path(c['preview']).read_bytes())==c['preview_sha256']
    assert len(font['review_sheets'])==8
    for s in font['review_sheets']:assert s['review'].startswith('Viewed') and sha(Path(s['path']).read_bytes())==s['sha256']
    mapping=read('work/analysis/lil_B152_B160_next_source_v3614/all342_unreviewed_clean_current_and99_prior_exact_source_keys.json');parent=read(context['complete_parent_source_packet']);assert len(parent['records'])==len(mapping['records'])==342 and mapping['excluded_already_reviewed_records']==99 and len({historical_key(r) for r in parent['records']}-pending)==283 and not {historical_key(r) for r in parent['records']}&integrated
    req=read(CHECKPOINT/'next_registered_integration_requirements.json');assert req['commands']==104 and req['relative_sites']==8 and req['target_relative_cases']==40 and req['final_stored_macro_alignment_cases']==236 and req['B154_two_declared_end_words_require_exact_preservation']
    scope=ledger['unfinished_editorial_scope_v3636'];assert sha(Path(scope['path']).read_bytes())==scope['sha256'] and scope['incomplete_route_source_prose']==59 and scope['canonical_Maria32_pending_uncredited'] and scope['Proof_terminology_consistency_open'];assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==3 and ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3636')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3636',ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_reread=5128,integrated=5069,pending=59,source_prose=5131,revised=3297,retained=1772,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],manifest_batches=528,accepted_layers=114,all59_clean_current_references_glosses_gates_and_retentions_verified=True,source104_commands_eight_relative_sites_and_B154_two_end_words_bound=True,all_prior_completed_records_candidate_and_wider_scope_unchanged=True,other283_B155_B160_objects_not_gloss_approved=True,new_emulator_runs=0,all_jobs_terminal=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('V3636 independently verified:5128 reread/5069 integrated/59 pending;5131 source-prose;V3607/528 batches unchanged. Full goal active.')
