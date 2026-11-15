"""Read complete selected exchanges and clean speaker identities without current story English."""
import argparse,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string

ROOT=Path('work/Maria_B58_B70_clean_20261109')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('blocks',type=int,nargs='+');args=parser.parse_args()
    packet=load(ROOT/'clean_source_packet.json');assert packet['source_only_not_current_English']
    arm=NdsImage.open(packet['source_ROM']).read_file('/__arm9__.bin');base=struct.unpack_from('<I',arm,0xCDAC0)[0]-0x02000000
    groups=[g for g in packet['groups'] if g['block'] in args.blocks];assert {g['block'] for g in groups}==set(args.blocks)
    actors=sorted({int(r['source_hex'][:2],16) for g in groups for r in g['records'] if r['kind']=='ordinary-speech'})
    print('CLEAN SPEAKERS',[(i,[string(arm,a)['text'] if a else '' for a in struct.unpack_from('<3I',arm,base+32*i)]) for i in actors if i<207])
    for group in groups:
        print('\nCOMPLETE CLEAN BLOCK',group['block'])
        for row in group['records']:
            speaker='A'+str(int(row['source_hex'][:2],16)) if row['kind']=='ordinary-speech' else 'CHOICE'
            print(row['id'],speaker,':',row['source_Japanese'].replace('\n',' / '))
if __name__=='__main__':main()
