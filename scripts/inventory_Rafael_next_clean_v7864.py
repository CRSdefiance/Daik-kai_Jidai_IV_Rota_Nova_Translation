"""Inventory complete clean Rafael B45 andoriginal EV0 context;numeric adjacency proves no chronology."""
import traceback
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.prove_papal_trade_entries_v7628 import parse_events
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_next_clean_v7864')
HANDOFF=Path('work/analysis/editorial_handoff_verification_v7863/verified_handoff.json')
if __name__=='__main__':
    assert not ROOT.exists();verified=read(HANDOFF);lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    assert sha(lp.read_bytes())==verified['ledger_sha256'] and ledger['records_editorially_completed']==6938 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    keys={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']};assert len(keys)==6938
    clean=Path('work/clean.nds');image=NdsImage.open(clean);arm=image.read_file('/__arm9__.bin');file='/data/SC0.DK4';archive=image.read_file(file);bank=IlnkContainer.parse(archive).blocks
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    ev=image.read_file('/data/EV0.DK4');events=parse_events(ev);inventory,walker,inventory_source=scoped_inventory();groups=[];failures=[]
    for number in [45]:
        block=bank[number];logical=8+int.from_bytes(block[4:6],'little')
        try:commands,speeches=inventory(arm,block)
        except Exception as e:
            failures.append(dict(block=number,clean_block_sha256=sha(block),clean_block_hex=block.hex(),error_type=type(e).__name__,diagnostic=traceback.format_exc(),not_counted_as_review_orrejection=True));continue
        assert logical<=len(block) and block[logical:]==bytes(len(block)-logical);rows=[]
        for speech in speeches:
            at=speech['offset']+5;end=block.index(0,at+1);raw=block[at:end];index=block[:at].count(b'\0');ident=f'DK4_MES_B{number}_R{index:04d}'
            try:japanese=raw[1:].decode('cp932');error=None
            except UnicodeDecodeError as e:japanese=None;error=str(e)
            row=dict(id=ident,file_path=file,block=number,source_record_index=index,source_selector=raw[0],source_hex=raw.hex(),source_complete_preamble_hex=block[at-5:at+1].hex(),source_Japanese=japanese,source_decode_error=error,source_reference=dict(block=number,offset=at,bytes=len(raw),record_index=index,header_offset=at-5),source_native_extent=speech['native_extent'],source_0100_ancestors=speech['ancestor_0100_offsets'],source_presentation_consumer_not_yet_approved=True,current_English_body_unread=True)
            row['already_contextually_completed']=historical_key(row) in keys;rows.append(row)
        assert commands and commands[-1]['offset']+commands[-1]['native_extent']==logical and commands[-1]['word']==0
        selected=[r for r in events if r['script_block']==number]
        needed={*[r['event_ID'] for r in selected],*[v for r in selected for v in r['must_be_completed']+r['must_not_be_completed'] if v!=65535]}
        groups.append(dict(block=number,file_path=file,clean_block_sha256=sha(block),clean_block_hex=block.hex(),source_header_hex=block[:8].hex(),clean_stored_bytes=len(block),clean_logical_end=logical,clean_tail_bytes=len(block)-logical,commands=commands,records=rows,physical_speech_objects=len(rows),source_controls=sorted({r['word'] for r in commands}),source_event_records=selected,source_event_anddependencies=[r for r in events if r['event_ID'] in needed],completed_coverage_overlap=sum(r['already_contextually_completed'] for r in rows),uncredited_source_positions=sum(not r['already_contextually_completed'] for r in rows),numeric_adjacency_not_proven_conversation_orchronology=True,source_event_outer_conditions_native_getters_andactual_selection_unreviewed=True))
    ROOT.mkdir(parents=True);output=ROOT/'complete_clean_SC0_B45_EV0_andcoverage_before_current_English.json'
    save(output,dict(source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),clean_ARM9_sha256=sha(arm),file_path=file,clean_archive_sha256=sha(archive),EV0_sha256=sha(ev),groups=groups,inventory_failures=failures,all_original_source_events=events,live_ledger_sha256=sha(lp.read_bytes()),verified_handoff=str(HANDOFF),verified_handoff_sha256=sha(HANDOFF.read_bytes()),source_only_no_current_English_exposed_orused=True,source_gloss_full_context_names_controls_entry_native_actual_release_pending=True,selected_story_sequence_not_approved_from_block_numbers=True,clean_inventory_walker=walker,clean_inventory_function=inventory_source,source_owned_EV_parser_file=str(Path(parse_events.__code__.co_filename)),source_owned_EV_parser_file_sha256=sha(Path(parse_events.__code__.co_filename).read_bytes()),new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [HANDOFF,Path(__file__)]},full_goal_complete=False))
    for g in groups:
        print(dict(block=g['block'],stored=g['clean_stored_bytes'],logical=g['clean_logical_end'],tail=g['clean_tail_bytes'],commands=len(g['commands']),speeches=len(g['records']),overlap=g['completed_coverage_overlap'],uncredited=g['uncredited_source_positions'],controls=[hex(v) for v in g['source_controls']],events=[dict(id=r['event_ID'],category=r['category'],action=r['action_index'],requires=r['must_be_completed'],excludes=r['must_not_be_completed']) for r in g['source_event_records']]))
        if g['block']==45:
            for r in g['records']:print(r['source_record_index'],format(r['source_selector'],'02X'),r['source_Japanese'].replace('\n',' / ') if r['source_Japanese'] is not None else r['source_decode_error'])
    print('INVENTORY_FAILURES',[(r['block'],r['error_type']) for r in failures])
