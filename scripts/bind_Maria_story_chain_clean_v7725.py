"""Bind the explicit34->108->35 completion chain andall67 clean speeches before current English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_chain_clean_v7725')
PRIOR=Path('work/analysis/maria_story_clean_v7724/complete_clean_SC3_B34_B35_EV3_andcoverage_before_current_English.json')
if __name__=='__main__':
    assert not ROOT.exists();prior=read(PRIOR);ledger=read('translations/editorial_review_current_v1.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['live_ledger_sha256'] and ledger['records_editorially_completed']==6855
    keys={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']}
    image=NdsImage.open(prior['source_ROM']);arm=image.read_file('/__arm9__.bin');file='/data/SC3.DK4';bank=IlnkContainer.parse(image.read_file(file)).blocks;events=prior['all_original_source_events']
    assert sha(Path(prior['source_ROM']).read_bytes())==prior['source_ROM_sha256'] and sha(arm)==prior['clean_ARM9_sha256'] and sha(image.read_file('/data/EV3.DK4'))==prior['EV3_sha256']
    groups=[];inventory,walker,inventory_source=scoped_inventory()
    for number in [34,108,35]:
        if number!=108:
            group=deepcopy(next(g for g in prior['groups'] if g['block']==number));assert sha(bank[number])==group['clean_block_sha256'];group['native_inventory_mode']='exact-prior-clean-block-andnative-inventory-reuse'
        else:
            block=bank[number];commands,speeches=inventory(arm,block);logical=8+int.from_bytes(block[4:6],'little');rows=[]
            assert commands[-1]['word']==0 and commands[-1]['offset']+commands[-1]['native_extent']==logical and block[logical:]==bytes(len(block)-logical)
            for speech in speeches:
                at=speech['offset']+5;raw=block[at:block.index(0,at+1)];index=block[:at].count(b'\0')
                row=dict(id=f'DK4_MES_B{number}_R{index:04d}',file_path=file,block=number,source_record_index=index,source_selector=raw[0],source_hex=raw.hex(),source_complete_preamble_hex=block[at-5:at+1].hex(),source_Japanese=raw[1:].decode('cp932'),source_decode_error=None,source_reference=dict(block=number,offset=at,bytes=len(raw),record_index=index,header_offset=at-5),source_native_extent=speech['native_extent'],source_0100_ancestors=speech['ancestor_0100_offsets'],source_presentation_consumer_not_yet_approved=True,current_English_body_unread=True)
                row['already_contextually_completed']=historical_key(row) in keys;rows.append(row)
            selected=[r for r in events if r['script_block']==number];needed={*[r['event_ID'] for r in selected],*[v for r in selected for v in r['must_be_completed']+r['must_not_be_completed'] if v!=65535]}
            group=dict(block=number,file_path=file,clean_block_sha256=sha(block),clean_block_hex=block.hex(),source_header_hex=block[:8].hex(),clean_stored_bytes=len(block),clean_logical_end=logical,clean_tail_bytes=len(block)-logical,commands=commands,records=rows,physical_speech_objects=len(rows),source_controls=sorted({c['word'] for c in commands}),source_event_records=selected,source_event_anddependencies=[r for r in events if r['event_ID'] in needed],completed_coverage_overlap=sum(r['already_contextually_completed'] for r in rows),uncredited_source_positions=sum(not r['already_contextually_completed'] for r in rows),native_inventory_mode='fresh-clean-B108-complete-native-inventory',source_event_outer_conditions_native_getters_andactual_selection_unreviewed=True)
        assert not group['completed_coverage_overlap'] and all(r['source_Japanese'] is not None for r in group['records']);groups.append(group)
    selected=[g['source_event_records'][0] for g in groups];assert [(r['event_ID'],r['action_index'],r['script_block'],r['must_be_completed'],r['must_not_be_completed']) for r in selected]==[(34,35,34,[],[]),(108,109,108,[34],[]),(35,36,35,[108],[])]
    rows=[r for g in groups for r in g['records']];assert len(rows)==len({historical_key(r) for r in rows})==67 and [len(g['records']) for g in groups]==[8,31,28]
    ROOT.mkdir(parents=True);save(ROOT/'complete_clean_34_108_35_67_refs_explicit_source_dependency_chain_before_current_English.json',dict(source_ROM=prior['source_ROM'],source_ROM_sha256=prior['source_ROM_sha256'],clean_ARM9_sha256=prior['clean_ARM9_sha256'],file_path=file,clean_archive_sha256=prior['clean_archive_sha256'],EV3_sha256=prior['EV3_sha256'],groups=groups,source_dependency_chain=[34,108,35],all67_source_positions_uncredited=True,live_ledger_sha256=prior['live_ledger_sha256'],source_completion_dependency_order_not_numeric_adjacency=True,additional_conditions_elapsed_time_intervening_events_locations_andnatural_activation_unproved=True,prior_B34_B35_native_inventories_reused_without_replay=True,all67_clean_Japanese_read_as_three_complete_linked_exchanges_before_current_English=True,current_English_bodies_unread=True,branch_variants_not_assumed_all_spoken_inone_playthrough=True,source_gloss_name_macro_control_entry_native_actual_andrelease_pending=True,clean_B108_inventory_walker=walker,clean_B108_inventory_function=inventory_source,new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,Path(__file__)]},full_goal_complete=False))
    print('Three complete clean exchanges:8+31+28=67 uncredited source refs. Explicit EV3 completion chain34->108->35 bound;not immediate chronology,natural activation orall branch playback.Current English unread.')
