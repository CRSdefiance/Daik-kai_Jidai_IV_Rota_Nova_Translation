"""Independently audit exact B167 pending credit, source/current bytes and native proofs."""
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B167_layout_v6 as codec
from dk4tool.dialogue.lil_B167_profile import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.checkpoint_lil_B167_v4136 import UNCHANGED
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v4137')
CHECKPOINT=Path('work/analysis/lil_B167_checkpoint_v4136')
if __name__=='__main__':
    assert not ROOT.exists();receipt=read(CHECKPOINT/'checkpoint_receipt.json')
    for p,digest in {**receipt['evidence'],**receipt['updated_files'],**receipt['preserved_release_files']}.items():assert sha(Path(p).read_bytes())==digest,p
    assert sha(Path(receipt['partial_write_recovery']).read_bytes())==receipt['partial_write_recovery_sha256']
    lp=Path('translations/editorial_review_current_v1.json');l=read(lp);before=read(CHECKPOINT/(lp.name+'.before'));prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/(lp.name+'.before')).read_bytes())==prior['ledger_sha256']
    f=l['contextual_story_natural_dialogue_pass_v1871']
    assert (f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(5602,5573,29)
    keys,integrated,pending=[{historical_key(r) for r in f[k]} for k in ['record_keys','integrated_record_keys','pending_record_keys']]
    assert len(keys)==len(f['record_keys'])==5602 and len(integrated)==5573 and len(pending)==29
    assert not integrated&pending and keys==integrated|pending
    completed=[r for family in l['completed_editorial_families'] for r in family['records']]
    assert len(completed)==len({historical_key(r) for r in completed})==5573 and {historical_key(r) for r in completed}==integrated
    assert (l['records_with_source_and_prose_pass'],l['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'],l['source_prose_reviewed_counts_by_file']['/data/SC3.DK4'],l['records_editorially_completed'],l['records_revised_and_integrated'],l['retained_wordings_editorially_completed'])==(5605,3749,64,5573,3551,2022)
    unit=next(u for u in l['coverage_units'] if u['id']=='all-route-scenes');assert (unit['reviewed_route_records'],unit['completed_route_records'])==(4003,3974)
    approval=read('work/analysis/lil_B167_native_approval_v4135/approval_receipt.json')
    for p,digest in approval['manuscripts'].items():assert sha(Path(p).read_bytes())==digest
    docs=[read(p) for p in approval['manuscripts']];rows=[r for d in docs for r in d['records']]
    assert len(rows)==29 and {historical_key(r) for r in rows}==pending
    assert Counter(r['kind'] for r in rows)=={'progressive':27,'typed-choice-label':2}
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':16,'retain-wording':13}
    d=next(d for d in docs if len(d['records'])==27);image=NdsImage.open(d['current_ROM']);clean=NdsImage.open('work/clean.nds')
    assert sha(Path(d['current_ROM']).read_bytes())==d['current_ROM_sha256']==prior['candidate_sha256']
    block,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[167] for im in [image,clean]]
    p=profile_for(image.read_file('/__arm9__.bin'),block);font=read(d['native_font_proof'])
    assert sha(Path(d['native_font_proof']).read_bytes())==d['native_font_proof_sha256']
    fonts={r['id']:r for r in font['cases']};notes=0
    for r in rows:
        assert all(r['review'].values()) and r['source_meaning']==r['fresh_source_gloss']
        assert r['full_clean_context_precedes_comparison'] and r['clean_source_complete_exchange_read_before_predecessor_English']
        raw,old=bytes.fromhex(r['source_hex']),bytes.fromhex(r['current_hex']);sa,ca=r['source_reference']['offset'],r['current_reference']['offset']
        assert jp[sa:sa+len(raw)]==raw and block[ca:ca+len(old)]==old and jp[sa+len(raw)]==block[ca+len(old)]==0
        if r['kind']=='progressive':
            assert raw[0]==old[0]==r['source_selector'] in [2,4,13,23,109]
            assert jp[sa-5:sa+1]==block[ca-5:ca+1]==bytes.fromhex(r['source_complete_preamble_hex'])
            assert raw[1:].decode('cp932')==r['source_Japanese']
            encoded=codec.encode_relocatable_dialogue(raw,r['english'],p);c=fonts[r['id']]
            assert encoded.encoded.hex()==r['compiled_hex']==c['encoded_hex']
            assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and16px_rows_within4rows']
            assert sum(len(x['cases']) for x in c['current_native_macro_pipelines'])==8
            assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
            qa=codec.audit_relocatable_dialogue_record(raw,r['english'],p)
            assert not [i for i in qa['issues'] if i['severity'] in ['error','warning'] and not(i['severity']=='warning' and i['code']=='line-break-count' and r.get('qa_waiver_reason'))]
            assert r.get('qa_waivers') in [None,['line-break-count']];notes+=bool(r.get('qa_waivers'))
            assert all(raw.count(k.encode())==r['english'].count('{MACRO:'+k+'}')==0 for k in ['FI','FA','FO'])
        else:
            assert raw.decode('cp932')==r['source_Japanese'] and r['english']==['Okay','No thanks'][r['option_index']]
        if r['editorial_decision']=='retain-wording':
            assert r['fresh_retained_wording_justification'] and (r['english'].split('}',1)[1] if r['kind']=='progressive' else r['english'])==r['effective_predecessor_paragraph']
    assert notes==11 and len(font['cases'])==27 and font['current_original_macro_alignment_calls']==216
    assert len(font['source_consumer_negative_controls'])==19 and len(font['source_bound_formatter_negatives'])==14
    assert all(r['rejected'] for r in font['source_bound_formatter_negatives'])
    assert approval['new_emulator_runs']==approval['actual_B167_speech_or_choice_return_coverage_added']==0
    scope=l['unfinished_editorial_scope_v4136'];assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    assert (scope['incomplete_COMMON'],scope['incomplete_route_source_prose'],scope['remaining_B168_B180_physical_speeches'],scope['remaining_choice_command_leads'])==(3,29,321,0)
    inventory=read(scope['path']);assert inventory['remaining_B167_B180_unreviewed_uncredited']==read(before['unfinished_editorial_scope_v4114']['path'])['remaining_B167_B180_unreviewed_uncredited']
    assert inventory['remaining_B167_B180_inventory_is_historical_at_V4114'] and inventory['remaining_B168_B180_unreviewed_uncredited']['physical_speeches']==321
    for key in UNCHANGED:assert l[key]==before[key],key
    candidate=l['current_integrated_candidate'];assert sha(Path(candidate['path']).read_bytes())==candidate['sha256'] and sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']
    assert read('translations/release_stack.json')['latest_promoted_build']['profile']=='all-routes-unified-v4046'
    assert l['goal_status']=='active' and not l['full_goal_complete']
    for path in receipt['updated_files']:
        if path.startswith('docs'):assert '## V4136: 29 B167 contextual/native reviews; integration pending' in Path(path).read_text(encoding='utf-8')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4136',ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(CHECKPOINT/'checkpoint_receipt.json'),handoff_receipt_sha256=sha((CHECKPOINT/'checkpoint_receipt.json').read_bytes()),fresh_reread=5602,integrated=5573,pending=29,source_prose=5605,revised=3551,retained=2022,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],manifest_batches=541,accepted_layers=114,all29_exact_source_current_gloss_context_retention_and_native_references_verified=True,partial_documentation_write_recovered_without_duplicate_credit=True,V4046_promoted_main_and_V4110_verified_experimental_unchanged=True,new_ROM_registry_emulator_or_completion_credit=False,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4136 independently verified:5602 reread/5573 integrated/29 pending;source/prose5605. Exact references,retentions,native proofs and wider scope pass.')
