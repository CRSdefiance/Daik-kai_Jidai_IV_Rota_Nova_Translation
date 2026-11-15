"""Bind both complete clean counterparts and reuse only the byte-identical Japanese gloss."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_SC0_SC1_clean_v7619')
GLOSS=Path('work/analysis/lil_B234_clean_context_v7572/all18_clean_familiar_banter_greatgrandfather_papal_trade_andconditional_discovery_glosses_before_old_English.json')
LEAD=Path('work/analysis/lil_B234_clean_counterparts_v7578b/byte_identical_clean_papal_trade_exchange_counterpart_leads.json')
HANDOFF=Path('work/analysis/editorial_handoff_verification_v7618/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();gloss,lead,verified,ledger=map(read,[GLOSS,LEAD,HANDOFF,LEDGER])
    assert gloss['all18_clean_glosses_precede_old_English'] and gloss['prior_English_unread'] and len(gloss['records'])==18 and sha(LEDGER.read_bytes())==verified['ledger_sha256']
    assert ledger['current_integrated_candidate']['sha256']==verified['candidate_sha256'] and ledger['records_editorially_completed']==verified['completed']==6801 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    keys={historical_key(r) for family in ledger['completed_editorial_families'] for r in family['records']};assert len(keys)==6801
    clean=Path('work/clean.nds');image=NdsImage.open(clean);arm=image.read_file('/__arm9__.bin')
    assert sha(clean.read_bytes())==gloss['source_ROM_sha256'] and sha(arm)==gloss['clean_ARM9_sha256']
    original=bytes.fromhex(gloss['clean_block_hex']);assert len(original)==1468 and int.from_bytes(original[4:6],'little')+8==1468
    inventory,walker,inventory_source=scoped_inventory();groups=[];allkeys=set()
    for route,blocknum in [(0,246),(1,237)]:
        file=f'/data/SC{route}.DK4';archive=image.read_file(file);block=IlnkContainer.parse(archive).blocks[blocknum]
        oldlead=next(r for r in lead['counterparts'] if r['file_path']==file and r['block']==blocknum)
        assert block==original and sha(block)==oldlead['whole_clean_block_sha256']==gloss['clean_block_sha256']
        commands,speeches=inventory(arm,block);assert commands==gloss['commands'] and len(commands)==20 and len(speeches)==18
        rows=[]
        for speech,known in zip(speeches,gloss['records'],strict=True):
            at=speech['offset']+5;end=block.index(0,at+1);raw=block[at:end];index=block[:at].count(b'\0')
            assert index==known['source_record_index'] and raw.hex()==known['source_hex'] and block[at-5:at+1].hex()==known['complete_preamble_hex'] and raw[1:].decode('cp932')==known['source_Japanese']
            row=dict(id=f'DK4_MES_B{blocknum}_R{index:04d}',file_path=file,block=blocknum,kind='progressive',source_record_index=index,source_selector=raw[0],source_hex=raw.hex(),source_complete_preamble_hex=block[at-5:at+1].hex(),source_Japanese=raw[1:].decode('cp932'),source_reference=dict(block=blocknum,offset=at,bytes=len(raw),record_index=index,header_offset=at-5),source_native_extent=speech['native_extent'],source_gloss=known['fresh_source_gloss'],source_gloss_reuse_mode='complete-clean-block-andrecord-byte-equality',prior_clean_gloss_reference=dict(path=str(GLOSS),sha256=sha(GLOSS.read_bytes()),id=known['id'],source_reference=deepcopy(known['source_reference'])),whole_clean_exchange_context=gloss['whole_exchange_context'],current_English_body_unread=True,route_specific_current_context_name_entry_native_actual_andrelease_pending=True,source_prose_or_completion_credit_added=0)
            key=historical_key(row);assert key not in keys and key not in allkeys;allkeys.add(key);rows.append(row)
        assert Counter(r['source_selector'] for r in rows)=={19:9,104:9}
        assert [(c['offset'],c['whole_command_hex']) for c in commands if c['word']!=0x4000]==[(1456,'00a0ffff6a000110'),(1464,'00000000')]
        groups.append(dict(file_path=file,route=route,block=blocknum,clean_archive_sha256=sha(archive),clean_block_sha256=sha(block),clean_block_hex=block.hex(),clean_stored_bytes=1468,clean_logical_end=1468,clean_tail_bytes=0,commands=commands,records=rows,previously_completed_file_qualified_keys=[],source_current_correspondence_not_yet_inspected=True))
    assert len(groups)==2 and sum(len(g['records']) for g in groups)==len(allkeys)==36
    ROOT.mkdir(parents=True);save(ROOT/'two_complete_clean_exchanges36_refs_exact_Japanese_gloss_reuse_before_current_English.json',dict(source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),clean_ARM9_sha256=sha(arm),verified_handoff=str(HANDOFF),verified_handoff_sha256=sha(HANDOFF.read_bytes()),ledger_sha256=sha(LEDGER.read_bytes()),current_registered_candidate=verified['candidate'],current_registered_candidate_sha256=verified['candidate_sha256'],prior_complete_clean_gloss=str(GLOSS),prior_complete_clean_gloss_sha256=sha(GLOSS.read_bytes()),earlier_clean_counterpart_lead=str(LEAD),earlier_clean_counterpart_lead_sha256=sha(LEAD.read_bytes()),groups=groups,complete_exchanges=2,source_speech_references=36,source_commands=40,source_actor_selectors=[19,104],all36_source_positions_uncredited_in_live6801_ledger=True,source_glosses_reused_by_exact_whole_block_andrecord_bytes_not_freshly_authored_orEnglish_derived=True,all36_clean_source_gloss_bindings_precede_other_route_current_English=True,other_route_current_English_bodies_not_read=True,original_full_preambles_A000_four_byte_ends_andzero_source_tails_preserved=True,no_automatic_current_English_context_entry_getter_name_display_orrelease_approval=True,no_cross_route_natural_activation_location_earned_progress_orfull_effect_claim=True,clean_inventory_walker=walker,clean_inventory_function=inventory_source,new_native_executions=0,new_emulator_runs=0,new_source_prose_reviews=0,new_completed_records=0,new_credit=0,full_editorial_objective_active=True,evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,LEAD,HANDOFF,Path(__file__)]},full_goal_complete=False))
    for r in groups[0]['records']:print(r['source_record_index'],format(r['source_selector'],'02X'),r['source_Japanese'].replace('\n',' / '))
    print('Two complete clean exchanges/36 file-qualified references:exact original Japanese/gloss reuse;zero existing coverage;other-route English/entry/names/display/release unreviewed;zero credit.')
