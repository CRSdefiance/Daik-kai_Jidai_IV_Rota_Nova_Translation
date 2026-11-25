"""Display complete clean exchanges, source actor names and exact style consumers only."""
import argparse
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--packet',type=Path,required=True)
    ap.add_argument('--blocks',type=int,nargs='+',required=True);args=ap.parse_args()
    packet=load(args.packet);assert packet['source_only_not_current_English']
    groups=[g for g in packet['groups'] if g['block'] in args.blocks]
    assert {g['block'] for g in groups}==set(args.blocks)
    arm=NdsImage.open(packet['source_ROM']).read_file('/__arm9__.bin')
    base=struct.unpack_from('<I',arm,0xCDAC0)[0]-0x02000000
    actors=sorted({int(r['source_hex'][:2],16) for g in groups for r in g['records'] if r['kind']=='ordinary-speech'})
    print('CLEAN ACTORS',[(i,[string(arm,p)['text'] if p else '' for p in struct.unpack_from('<3I',arm,base+32*i)]) for i in actors if i<207])
    for group in groups:
        print('\nCOMPLETE CLEAN BLOCK',group['block'])
        for row in group['records']:
            if row['kind']=='ordinary-speech':speaker='A'+str(int(row['source_hex'][:2],16))
            elif row['kind']=='physical-style-alternative':
                at=row['source_reference']['offset']
                command=next(c for c in group['all_source_commands'] if c['word']==0x4100 and c['offset']<=at<c['offset']+c['native_extent'])
                raw=bytes.fromhex(command['whole_command_hex']);offsets=struct.unpack_from('<8H',raw,2)
                slots=[i for i,o in enumerate(offsets) if command['offset']+20+o==at];assert slots
                speaker='STYLE A'+str(raw[19])+' slots'+str(slots)
            else:speaker='CHOICE'
            print(row['id'],speaker,':',row['source_Japanese'].replace('\n',' / '))

if __name__=='__main__':main()
