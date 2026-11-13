"""Independent pending34 source/prose/native/research-payload and ledger audit."""
from pathlib import Path
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import common_message_entries
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v2671')
CHECKPOINT=Path('work/analysis/aftermath_remaining_checkpoint_v2670')
IDS={*range(1994,2011),*range(2022,2038),2192}

if __name__=='__main__':
    assert not ROOT.exists()
    rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    oldpath=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(oldpath)
    prior=read('work/analysis/editorial_handoff_verification_v2665/verified_handoff.json')
    assert sha(oldpath.read_bytes())==prior['ledger_sha256']
    oldreceipt=read(prior['handoff_receipt'])
    for p,digest in oldreceipt['updated_files'].items():
        backup=CHECKPOINT/(Path(p).name+'.before');assert sha((backup if backup.exists() else Path(p)).read_bytes())==digest,p
    keys={(r['file_path'],r['id']) for r in fresh['record_keys']}
    integrated={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}
    pending={(r['file_path'],r['id']) for r in fresh['pending_record_keys']}
    completed={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']}
    assert len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==2184
    assert integrated==completed and len(completed)==2150
    assert pending==keys-integrated=={('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') for n in IDS}
    assert not integrated&pending and len(fresh['pending_contextual_families'])==1
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2184,2150,34)
    assert Counter(p for p,n in keys)=={'/COMMON/MESFILE.DK4':1527,'/data/SC2.DK4':429,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    for field in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated',
                  'retained_wordings_editorially_completed','source_prose_reviewed_counts_by_file',
                  'records_with_source_and_prose_pass','records_with_source_prose_drafts',
                  'reviewed_but_incomplete_COMMON_IDs','current_integrated_candidate']:
        assert ledger[field]==before[field],field
    assert ledger['records_editorially_completed']==2150 and ledger['records_revised_and_integrated']==1504 and ledger['retained_wordings_editorially_completed']==646
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==2259 and len(ledger['reviewed_but_incomplete_COMMON_IDs'])==109
    assert IDS<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    dp=Path(fresh['latest_contextual_manuscript']);doc=read(dp);validate_natural_dialogue_batch(doc)
    assert doc['revised_IDs']==[2029] and doc['retained_count']==33 and not doc['formatting_review_pending']
    assert doc['registered_revision_integration_pending'] and doc['current_native_and_representative_reconciliation_pending']
    assert doc['all34_native_previews_viewed_on_four_sheets'] and doc['revision_native_loader_and_copy_verified_in_research_only']
    rom=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds');arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    en=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    for r in doc['records']:
        n=r['message_id'];assert n in IDS and all(r['review'].values()) and r['source_meaning'] and r['localization_note']
        assert r['source_hex']==jp[n].text.hex() and r['source_Japanese']==jp[n].text.decode('cp932') and r['source_reference']==ref(jp[n])
        assert r['current_reference']==ref(en[n]) and r['current_hex']==r['current_text_hex']==en[n].text.hex()
        assert r['current_English']==en[n].text[1:].decode('ascii') and r['current_stored_English']==en[n].text.decode('ascii')
        assert r['compiled_hex']==r['proposed_compiled_hex']==compiled(r).hex() and r['unwrapped_paragraph_hex']==r['english'].encode('ascii').hex()
        if n==2029:assert r['editorial_decision']=='revise' and compiled(r)!=en[n].text and r['english']=='You cannot win! I suggest you surrender at once!'
        else:assert r['editorial_decision']=='retain-wording' and compiled(r)==en[n].text and r['fresh_retained_wording_justification']
        assert not r['new_current_visit'] and 'qa_waivers' not in r
    packet=read(doc['source_context_packet']);context=read(doc['native_context_proof'])
    assert packet['selected_IDs']==[r['message_id'] for r in doc['records']]
    assert len(context['voice_tables'])==5 and sum(len(t['all207_original_actor_choices']) for t in context['voice_tables'])==1035
    names=context['all114_current_native_town_names_and_two_original_exchange_paths'];assert len(names)==114 and {n['town_index'] for n in names}==set(range(114))
    assert all(len(n['unassigned_original_report_only_calls'])==1 and len(n['assigned_original_three_turn_calls'])==3 for n in names)
    assert len(context['CPU_assigned_First_Mate_fixture']['one_roster_byte_changed'])==1
    font=read(doc['current_native_font_proof']);plan=read(doc['revision_payload_plan'])
    assert len(font['cases'])==712 and len(font['complete_native_planes'])==len(font['current_deployed_original_pipelines'])==34
    assert len(font['current_deployed_cold_warm_copies'])==68 and font['findings']==[]
    assert font['all114_real_town_names_for_each_of6_templates']==684 and font['no_historical_synthetic_name_waivers_transferred']
    assert all(c['no_orphan_or_weak_line_end'] for c in font['cases'])
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    assert len(font['review_sheets'])==4 and next(c for c in font['cases'] if c['message_ID']==2029)['proposed_input_not_current_COMMON']
    assert next(c for c in font['current_deployed_original_pipelines'] if c['message_ID']==2029)['current2029_still_old_wording']
    targetarm=Path(plan['target_ARM9']).read_bytes();targetcommon=Path(plan['target_COMMON']).read_bytes()
    assert sha(targetarm)==plan['target_ARM9_sha256'] and sha(targetcommon)==plan['target_COMMON_sha256']
    targets=owned_entries(targetcommon,targetarm,plan['directory_sha256']);oldblocks=IlnkContainer.parse(common).blocks;newblocks=IlnkContainer.parse(targetcommon).blocks
    assert len(oldblocks)==len(newblocks)==41 and [i for i,(a,b) in enumerate(zip(oldblocks,newblocks,strict=True)) if a!=b]==[22]
    assert len(oldblocks[22])==5378 and len(newblocks[22])==5392 and len(targets)==len(en)==3668
    for old,new in zip(en,targets,strict=True):
        expected=bytes.fromhex(next(r['proposed_compiled_hex'] for r in doc['records'] if r['message_id']==2029)) if old.message_id==2029 else old.text
        assert new.text==expected
        if old.message_id!=2029:assert oldblocks[old.block][old.block_offset:old.copy_end]==newblocks[new.block][new.block_offset:new.copy_end]
    restored=bytearray(targetarm)
    for p in plan['all_ARM9_changes_are_declared_directory_or_offset_metadata']:
        at=p['offset'];old=bytes.fromhex(p['source_hex']);new=bytes.fromhex(p['target_hex'])
        assert arm[at:at+len(old)]==old and targetarm[at:at+len(new)]==new
        restored[at:at+len(old)]=old
    assert bytes(restored)==arm and plan['code_font_geometry_sections_BSS_cache_and_staged123040_unchanged']
    assert len(plan['native_cold_warm_copies_all123_repacked_records'])==246
    assert plan['new2029_loaded_template_hex']==targets[2029].text.hex()
    assert plan['new2029_complete_source_selected_direct_actor_loader_printf_macro_wrap_pipeline']['formatted_hex']==next(c['formatted_hex'] for c in font['complete_native_planes'] if c['message_ID']==2029)
    assert plan['no_playable_ROM_created_or_promoted'] and plan['registered_profile_ROM_clean_patch_and_startup_still_pending']
    manifestpath=Path(doc['current_ROM']).with_suffix('.manifest.json');manifest=read(manifestpath);registry=read('translations/release_stack.json')
    release=read('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json')
    assert sha(Path(doc['current_ROM']).read_bytes())==release['candidate_sha256']==receipt['candidate_sha256']
    assert sha(arm)==release['ARM9_sha256'] and sha(common)==release['COMMON_sha256'] and sha(manifestpath.read_bytes())==release['manifest_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']==receipt['patch_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    assert sha(Path('translations/release_stack.json').read_bytes())==manifest['release_stack_sha256']
    assert len(manifest['batches'])==493 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==read('work/analysis/refit_spritsail_registration_v2283/registration_receipt.json')['builder_sha256']
    assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256'] and sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
    handoff=Path('docs/editorial_handoff_current.md').read_text();assert handoff.startswith('# Current editorial handoff - V2670')
    assert '2184 reread /2150 integrated-reconciled /34pending' in handoff and 'later older-record technical re-audit remain open' in handoff
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2670',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),
        fresh_records=2184,fresh_integrated=2150,fresh_pending=34,new_completed_records=0,proposed_revision_IDs=[2029],justified_retention_drafts=33,
        source_prose=2259,incomplete_COMMON=109,all34_clean_current_and_proposed_boundaries_verified=True,
        source1035_voice_choices114names228exchange_paths_and_native712layouts34planes68current_copies_verified=True,
        research_one_record_COMMON22_growth14_metadata_only_and246copies_and_original_loader_pipeline_verified=True,
        current_deployed2029_old_and_proposed_research2029_new_correctly_distinguished=True,
        prior_ledger_and_updated_file_backup_chain_verified=True,handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        no_playable_ROM_registry_builder_profile_manifest_or_patch_change=True,prior_clean_input_reconstruction_proof_still_bound=True,
        representative_scope_registered_integration_patch_and_startup_pending=True,new_emulator_runs=0,all_jobs_terminal=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Independent V2670 audit passes:34fresh reviews andone research-verified tone revision;2184reread/2150reconciled/34pending. Current ROM/stack unchanged;integration and representative gates remain open.')
