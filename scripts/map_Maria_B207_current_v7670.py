"""Expose current English only after complete18 clean gloss bindings; preserve CS0101."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.lil_B234_source_span_binding_v7574 import source_span_matches_registered_renderer_branches
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_current_v7670')
SOURCE=Path('work/analysis/maria_B207_clean_gloss_v7669/all18_exact_Japanese_gloss_bindings_distinct_CS0101_before_current_English.json')
HANDOFF=Path('work/analysis/editorial_handoff_verification_v7667/verified_handoff.json')
if __name__=='__main__':
    assert not ROOT.exists();source,verified=map(read,[SOURCE,HANDOFF]);assert source['all18_source_gloss_bindings_precede_current_English'] and source['current_English_body_unread']
    clean,current=[NdsImage.open(p) for p in [source['source_ROM'],verified['candidate']]];jp,arm=[im.read_file('/__arm9__.bin') for im in [clean,current]]
    assert sha(Path(verified['candidate']).read_bytes())==verified['candidate_sha256'] and sha(jp)==source['clean_ARM9_sha256'] and sha(arm)==verified['ARM9_sha256']=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
    for a,b in [(0x2425C,0x243A0),(0x29BD0,0x29D34),(0x2A154,0x2A1D8),(0x7E988,0x7E9A0)]:assert source_span_matches_registered_renderer_branches(arm,jp,a,b)
    file='/data/SC3.DK4';archive=current.read_file(file);old=bytes.fromhex(source['clean_block_hex']);now=IlnkContainer.parse(archive).blocks[207]
    inv,_,_=scoped_inventory();before,after=[inv(a,b)[0] for a,b in [(jp,old),(arm,now)]]
    assert before==source['all20_source_commands'] and len(before)==len(after)==20 and [c['word'] for c in before]==[c['word'] for c in after]
    assert old[:4]==now[:4]==b'CS\1\1' and old[6:8]==now[6:8] and not any(c['ancestor_0100_offsets'] for c in [*before,*after])
    oldend,end=[8+int.from_bytes(b[4:6],'little') for b in [old,now]]
    for block,commands,logical in [(old,before,oldend),(now,after,end)]:
        assert commands[0]['offset']==8 and commands[-1]['offset']+commands[-1]['native_extent']==logical
        assert all(a['offset']+a['native_extent']==b['offset'] for a,b in zip(commands,commands[1:])) and block[logical:]==bytes(len(block)-logical) and len(block)-logical in range(4)
    rows=[];mapping=[];inverse=[old[:8]]
    for a,b in zip(before,after,strict=True):
        ao,bo=a['offset'],b['offset'];av,bv=old[ao:ao+a['native_extent']],now[bo:bo+b['native_extent']]
        mapping.append(dict(word=a['word'],source_offset=ao,current_offset=bo,source_extent=a['native_extent'],current_extent=b['native_extent']))
        if a['word']!=0x4000:assert av==bv;inverse.append(bv);continue
        assert av[:6]==bv[:6];at,ca=ao+5,bo+5;raw=now[ca:now.index(0,ca+1)];r=next(r for r in source['records'] if r['source_reference']['header_offset']==ao)
        assert raw[0]==r['source_selector'];row=deepcopy(r);row.update(kind='progressive',source_kind='progressive',current_reference=dict(block=207,offset=ca,bytes=len(raw),header_offset=bo,record_index=now[:ca].count(b'\0')),current_hex=raw.hex(),current_record_index=now[:ca].count(b'\0'),current_native_extent=b['native_extent'],current_raw_storage_English=raw[1:].decode('cp932'),raw_storage_comparison_paragraph=' '.join(raw[1:].decode('cp932').split()),current_English_body_unread=False,current_effective_body_getter_voice_catalogue_andheader_effect_pending=True);rows.append(row);inverse.append(av)
    assert len(rows)==18 and b''.join(inverse)+old[oldend:]==old and clean.read_file('/data/EV3.DK4')==current.read_file('/data/EV3.DK4')
    ROOT.mkdir(parents=True);save(ROOT/'all18_complete_Maria_clean_current_refs_CS0101_before_new_prose.json',dict(source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),current_ROM=verified['candidate'],current_ROM_sha256=verified['candidate_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(current.read_file('/COMMON/MESFILE.DK4')),file_path=file,block=207,current_archive_sha256=sha(archive),clean_block_sha256=sha(old),current_block_sha256=sha(now),source_header_hex=old[:8].hex(),current_header_hex=now[:8].hex(),complete_CS0101_header_preserved_not_normalized=True,clean_stored_bytes=len(old),clean_logical_end=oldend,clean_tail_bytes=len(old)-oldend,current_stored_bytes=len(now),current_logical_end=end,current_tail_bytes=len(now)-end,all_clean_native_commands=before,all_current_native_commands=after,all20_complete_command_boundaries=mapping,records=rows,all18_source_gloss_bindings_precede_first_current_English=True,complete_source_block_inverse_from_original_nontext_andall_source_speech_containers=True,all18_complete_six_byte_preambles_A000_operands_andnormal_end_exact=True,source_macro_counts={m:sum(bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for r in rows) for m in ['FI','FA','FO']},current_raw_macro_counts={m:sum(bytes.fromhex(r['current_hex'])[1:].count(m.encode()) for r in rows) for m in ['FI','FA','FO']},source_EV3_file_preserved_entry_dependencies_not_yet_interpreted=True,no_captain0_1_2_snapshot_used_for_Maria_dynamic_consumers=True,shared_native_code_spans_exact_by2b6_runtime_not_route_approval=True,raw_storage_not_effective_runtime_orlocalization_approval=True,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,HANDOFF,Path(__file__)]},full_goal_complete=False))
    for r in rows:print(r['source_record_index'],repr(r['raw_storage_comparison_paragraph']))
    print(dict(current_stored=len(now),current_logical=end,current_tail=len(now)-end,source_header=old[:8].hex(),current_header=now[:8].hex(),records=18,credit=0))
