"""Source-only 4100 physical alternatives andeight-slot aliases; no English intake."""
import argparse
import struct
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ['packet','out']:parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists();packet=load(args.packet);objects=[];rows=[]
    for group in packet['groups']:
        block=bytes.fromhex(group['clean_block_hex'])
        for command in group['all_source_commands']:
            if command['word']!=0x4100:continue
            at=command['offset'];raw=bytes.fromhex(command['whole_command_hex'])
            assert raw==block[at:at+command['native_extent']] and raw[:2]==b'\0\x41' and raw[18]==0
            offsets=list(struct.unpack_from('<8H',raw,2));physical=[];occupied=set()
            for offset in sorted(set(offsets)):
                start=20+offset;end=raw.index(0,start);value=raw[start:end]
                assert value and all(b>=32 or b==10 for b in value)
                padded_end=end+1+(end+1)%2
                assert not occupied.intersection(range(start,padded_end));occupied.update(range(start,padded_end))
                assert all(v==0 for v in raw[end:padded_end])
                row=dict(id=f'SC{packet["route"]}_B{group["block"]}_STYLE_{at}_{offset}',file_path=group['file_path'],block=group['block'],kind='actor-style-alternative',
                    source_command_offset=at,source_native_extent=len(raw),source_selector=raw[19],source_header_hex=raw[:20].hex(),source_choice_object_hex=raw.hex(),
                    source_style_indices=[i for i,v in enumerate(offsets) if v==offset],source_hex=value.hex(),source_Japanese=value.decode('cp932'),
                    source_reference=dict(file_path=group['file_path'],block=group['block'],command_offset=at,offset=at+start,length=len(value),physical_record_index=block[:at+start].count(b'\0')),
                    virtual_formatter_prefix_is_not_part_of_stored_alternative_text=True,source_macros={m:value.count(m.encode()) for m in ['FI','FA','FO']},
                    earlier_English_unconsulted=True,native_style_dispatch_andall_five_review_gates_pending=True,new_credit=0)
                physical.append(row);rows.append(row)
            assert occupied==set(range(20,len(raw)))
            objects.append(dict(block=group['block'],offset=at,source_native_extent=len(raw),source_header_hex=raw[:20].hex(),source_hex=raw.hex(),virtual_selector=raw[19],
                style_offsets=offsets,physical_alternative_IDs=[r['id'] for r in physical],all8_alias_slots_preserved=True))
    save(args.out,dict(source_packet=str(args.packet),source_packet_sha256=sha(args.packet.read_bytes()),objects=objects,records=rows,
        object_count=len(objects),physical_alternatives=len(rows),style_alias_slots=8*len(objects),
        source_format_reference='dk4tool/patch/lil_B111_B119_editorial.py:source-proven20-byte header,eight aliases,virtual selector excluded fromstored body',
        source_only_not_current_orlocalized_English=True,native_dependency_reuse_andindividual_meanings_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(objects=len(objects),physical_alternatives=len(rows),alias_slots=8*len(objects),old_English_unconsulted=True))

if __name__=='__main__':main()
