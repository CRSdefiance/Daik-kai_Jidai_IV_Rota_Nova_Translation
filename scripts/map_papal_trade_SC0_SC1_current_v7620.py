"""Read both complete current exchanges only after all clean Japanese/gloss bindings."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.lil_B234_source_span_binding_v7574 import source_span_matches_registered_renderer_branches
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_SC0_SC1_current_v7620')
SOURCE=Path('work/analysis/papal_trade_SC0_SC1_clean_v7619/two_complete_clean_exchanges36_refs_exact_Japanese_gloss_reuse_before_current_English.json')
INPUT=Path('work/analysis/current_V7611_native_v7616/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);inp=read(INPUT)
    assert source['all36_clean_source_gloss_bindings_precede_other_route_current_English'] and source['other_route_current_English_bodies_not_read'] and source['source_speech_references']==36
    assert inp['current_ROM_sha256']==source['current_registered_candidate_sha256']==sha(Path(source['current_registered_candidate']).read_bytes())
    clean,current=[NdsImage.open(p) for p in [source['source_ROM'],source['current_registered_candidate']]]
    original,arm=[im.read_file('/__arm9__.bin') for im in [clean,current]];assert sha(original)==source['clean_ARM9_sha256'] and sha(arm)==inp['current_ARM9_sha256']
    for start,end in [(0x2425C,0x243A0),(0x29BD0,0x29D34),(0x2A154,0x2A1D8),(0x7E988,0x7E9A0)]:assert source_span_matches_registered_renderer_branches(arm,original,start,end)
    assert clean.read_file('/data/EV0.DK4')==current.read_file('/data/EV0.DK4') and clean.read_file('/data/EV1.DK4')==current.read_file('/data/EV1.DK4')
    native,walker,invsource=scoped_inventory();groups=[]
    for group in source['groups']:
        file,n=group['file_path'],group['block'];archive=current.read_file(file);old=bytes.fromhex(group['clean_block_hex']);now=IlnkContainer.parse(archive).blocks[n]
        before,after=native(original,old)[0],native(arm,now)[0]
        assert before==group['commands'] and len(before)==len(after)==20 and [c['word'] for c in before]==[c['word'] for c in after] and sum(c['word']==0x4000 for c in after)==18
        assert old[:4]==now[:4] and old[6:8]==now[6:8] and not any(c['ancestor_0100_offsets'] for c in [*before,*after])
        oldend=8+int.from_bytes(old[4:6],'little');end=8+int.from_bytes(now[4:6],'little')
        for data,commands,logical in [(old,before,oldend),(now,after,end)]:
            assert commands[0]['offset']==8 and commands[-1]['offset']+commands[-1]['native_extent']==logical
            assert all(a['offset']+a['native_extent']==b['offset'] for a,b in zip(commands,commands[1:]))
            assert len(data)-logical in range(4) and data[logical:]==bytes(len(data)-logical)
        rows=[];mapping=[];inverse=[old[:8]]
        for a,b in zip(before,after,strict=True):
            ao,bo=a['offset'],b['offset'];ar,br=old[ao:ao+a['native_extent']],now[bo:bo+b['native_extent']]
            mapping.append(dict(word=a['word'],source_offset=ao,current_offset=bo,source_extent=a['native_extent'],current_extent=b['native_extent']))
            if a['word']!=0x4000:
                assert ar==br and a['whole_command_hex']==b['whole_command_hex'];inverse.append(br);continue
            assert ar[:6]==br[:6]
            at,ca=ao+5,bo+5;raw=now[ca:now.index(0,ca+1)];known=next(r for r in group['records'] if r['source_reference']['header_offset']==ao)
            assert raw[0]==known['source_selector'] and old[at:old.index(0,at+1)].hex()==known['source_hex']
            row=deepcopy(known);row.update(source_kind='progressive',current_reference=dict(block=n,offset=ca,bytes=len(raw),header_offset=bo,record_index=now[:ca].count(b'\0')),current_hex=raw.hex(),current_record_index=now[:ca].count(b'\0'),current_native_extent=b['native_extent'],current_raw_storage_English=raw[1:].decode('cp932'),raw_storage_comparison_paragraph=' '.join(raw[1:].decode('cp932').split()),current_English_body_unread=False,current_effective_runtime_body_getter_voice_andcatalog_binding_pending=True,all_five_editorial_native_actual_andrelease_gates_pending=True)
            rows.append(row);inverse.append(ar)
        assert len(rows)==18 and b''.join(inverse)+old[oldend:]==old
        groups.append(dict(file_path=file,route=group['route'],block=n,clean_block_sha256=sha(old),current_block_sha256=sha(now),current_archive_sha256=sha(archive),clean_stored_bytes=len(old),clean_logical_end=oldend,clean_tail_bytes=len(old)-oldend,current_stored_bytes=len(now),current_logical_end=end,current_tail_bytes=len(now)-end,all_clean_native_commands=before,all_current_native_commands=after,all20_complete_command_boundaries=mapping,complete_source_inverse_from_current_nontext_andsource_speech_containers=True,all_complete_six_byte_preambles_andopaque_A000_end_operands_exact=True,source_macro_counts={m:sum(bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for r in rows) for m in ['FI','FA','FO']},current_raw_macro_counts={m:sum(bytes.fromhex(r['current_hex'])[1:].count(m.encode()) for r in rows) for m in ['FI','FA','FO']},records=rows))
    ROOT.mkdir(parents=True);save(ROOT/'two_complete_current_exchanges36_source_current_refs_before_new_prose.json',dict(source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),current_ROM=source['current_registered_candidate'],current_ROM_sha256=source['current_registered_candidate_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(current.read_file('/COMMON/MESFILE.DK4')),current_strict_native_input=str(INPUT),current_strict_native_input_sha256=sha(INPUT.read_bytes()),groups=groups,records=[r for g in groups for r in g['records']],total_source_speeches=36,all36_clean_Japanese_gloss_bindings_precede_first_other_route_current_English_comparison=True,source_gloss_reused_by_exact_whole_clean_block_not_from_English=True,current_storage_comparison_not_effective_runtime_or_localization_approval=True,route_specific_EV0_EV1_files_preserved_but_entry_dependencies_not_yet_interpreted=True,shared_native_instruction_guard_reused_only_by_exact2b6_ARM9_bytes=True,all_names_aliases_voices_getters_complete_context_decisions_native_actual_andrelease_pending=True,new_emulator_runs=0,new_source_prose_reviews=0,new_completed_records=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path('scripts/lil_B234_source_span_binding_v7574.py'),Path(__file__)]},full_goal_complete=False))
    for g in groups:
        print(g['file_path'],'B'+str(g['block']),'stored/logical/tail',g['current_stored_bytes'],g['current_logical_end'],g['current_tail_bytes'])
        for r in g['records']:print(r['source_record_index'],repr(r['raw_storage_comparison_paragraph']))
    print('36 exact source/current references;raw storage only,effective native consumers,individual findings andrelease pending;zero credit.')
