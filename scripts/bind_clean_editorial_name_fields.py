"""Read exact clean name-table fields for a packet; this is not consumer approval."""
import argparse
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.audit_native_given_name_table import string

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ('packet','out'):parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists();packet=load(args.packet)
    source=Path(packet['source_ROM']);assert sha(source.read_bytes())==packet['source_ROM_sha256']
    arm=NdsImage.open(source).read_file('/__arm9__.bin');assert sha(arm)==packet['source_ARM9_sha256']
    table=struct.unpack_from('<I',arm,0xCDAC0)[0];selectors=sorted({r['source_selector'] for g in packet['groups'] for r in g['records']})
    rows=[]
    for ident in selectors:
        if ident>=207:continue
        fields=[]
        for column in [0,4,8]:
            at=table-0x02000000+32*ident+column;pointer=struct.unpack_from('<I',arm,at)[0]
            value=string(arm,pointer);assert value['status']=='printable-static-string'
            fields.append(dict(column=column,source_ARM9_field_offset=at,pointer_hex=arm[at:at+4].hex(),**value))
        rows.append(dict(actor_ID=ident,fields=fields))
    save(args.out,dict(source_packet=str(args.packet),source_packet_sha256=sha(args.packet.read_bytes()),source_ARM9_sha256=sha(arm),
        clean_table_pointer=table,records=rows,special_selectors_outside_ordinary_actor_table=[v for v in selectors if v>=207],
        source_metadata_only_not_a_native_name_voice_orportrait_approval=True,earlier_English_dialogue_unconsulted=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print([(r['actor_ID'],[f['text'] for f in r['fields']]) for r in rows]);print('Special source selectors:',[v for v in selectors if v>=207])

if __name__=='__main__':main()
