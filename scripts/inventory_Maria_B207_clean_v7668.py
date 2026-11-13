"""Inventory complete clean SC3B207 and neighboring source blocks before current English."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_clean_v7668')
HANDOFF=Path('work/analysis/editorial_handoff_verification_v7667/verified_handoff.json')
LEAD=Path('work/analysis/maria_B207_metadata_lead_v7665c/17_uncredited_SC3B207_metadata_refs_clean_complete_exchange_review_pending.json')
if __name__=='__main__':
    assert not ROOT.exists();verified=read(HANDOFF);lead=read(LEAD);lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    assert sha(lp.read_bytes())==verified['ledger_sha256'] and ledger['records_editorially_completed']==6837 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    keys={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']};assert len(keys)==6837
    clean=Path('work/clean.nds');image=NdsImage.open(clean);arm=image.read_file('/__arm9__.bin');file='/data/SC3.DK4';archive=image.read_file(file);bank=IlnkContainer.parse(archive).blocks
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    inventory,walker,inventory_source=scoped_inventory();groups=[]
    for number in [206,207,208]:
        block=bank[number];commands,speeches=inventory(arm,block);logical=8+int.from_bytes(block[4:6],'little');rows=[]
        assert logical<=len(block) and block[logical:]==bytes(len(block)-logical)
        for speech in speeches:
            at=speech['offset']+5;end=block.index(0,at+1);raw=block[at:end];index=block[:at].count(b'\0')
            rows.append(dict(id=f'DK4_MES_B{number}_R{index:04d}',file_path=file,block=number,source_record_index=index,source_selector=raw[0],source_hex=raw.hex(),source_complete_preamble_hex=block[at-5:at+1].hex(),source_Japanese=raw[1:].decode('cp932'),source_reference=dict(block=number,offset=at,bytes=len(raw),record_index=index,header_offset=at-5),source_native_extent=speech['native_extent'],source_presentation_consumer_not_yet_approved=True,current_English_body_unread=True))
        assert commands and commands[-1]['offset']+commands[-1]['native_extent']==logical and commands[-1]['word']==0
        groups.append(dict(block=number,file_path=file,clean_block_sha256=sha(block),clean_block_hex=block.hex(),clean_stored_bytes=len(block),clean_logical_end=logical,clean_tail_bytes=len(block)-logical,commands=commands,records=rows,physical_speech_objects=len(rows),source_controls=sorted({r['word'] for r in commands}),spatially_adjacent_block_not_automatic_conversation_orchronology=True))
    selected=groups[1];overlap=[r['id'] for r in selected['records'] if historical_key(r) in keys]
    assert not overlap and {r['id'] for r in lead['records']}=={r['id'] for r in selected['records']}
    ROOT.mkdir(parents=True)
    save(ROOT/'complete_clean_SC3B207_andadjacent_source_blocks_before_current_English.json',dict(source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),clean_ARM9_sha256=sha(arm),file_path=file,clean_archive_sha256=sha(archive),groups=groups,selected_block=207,selected_source_records=len(selected['records']),all_selected_source_keys_uncredited=True,live_ledger_sha256=sha(lp.read_bytes()),verified_handoff=str(HANDOFF),verified_handoff_sha256=sha(HANDOFF.read_bytes()),metadata_lead=str(LEAD),metadata_lead_sha256=sha(LEAD.read_bytes()),source_only_no_current_English_compared=True,neighboring_blocks_not_assumed_same_exchange_orapproved=True,source_gloss_names_consumers_controls_entry_native_actual_andrelease_all_pending=True,clean_inventory_walker=walker,clean_inventory_function=inventory_source,new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [HANDOFF,LEAD,Path(__file__)]},full_goal_complete=False))
    for r in selected['records']:print(r['source_record_index'],format(r['source_selector'],'02X'),r['source_Japanese'].replace('\n',' / '))
    for g in groups:print(dict(block=g['block'],stored=g['clean_stored_bytes'],logical=g['clean_logical_end'],tail=g['clean_tail_bytes'],commands=len(g['commands']),speeches=len(g['records']),controls=[hex(x) for x in g['source_controls']]))
