"""Find documented unchanged Japanese source allocations; no space is approved."""

import bisect
import json
import re
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_tavern_recruitment_v771 import CURRENT,ROOT
from scripts.inventory_shipyard_storage_v760 import units
from scripts.verify_village_wrap_v608 import save

BASE=0x02000000


def main():
    rom=NdsImage.open(CURRENT);arm=rom.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    limit=len(MainCodeFile(arm,BASE).sections[0].data)
    candidates={}
    for path in Path('translations').glob('*.json'):
        try:doc=json.loads(path.read_text(encoding='utf-8'))
        except (ValueError,UnicodeError):continue
        if not isinstance(doc,dict) or doc.get('file_path')!='/__arm9__.bin':continue
        for row in doc.get('records',[]):
            if not isinstance(row,dict) or not isinstance(row.get('offset'),int) or not isinstance(row.get('source_hex'),str):continue
            at=row['offset']
            try:raw=bytes.fromhex(row['source_hex'])
            except ValueError:continue
            if at<0 or len(raw)<24 or at+len(raw)>limit:continue
            if arm[at:at+len(raw)]!=raw or clean[at:at+len(raw)]!=raw:continue
            if 0x171E48<at+len(raw) and at<0x172464:continue
            end=raw.find(b'\0')
            if end<4 or any(raw[end:]):continue
            try:text=raw[:end].decode('cp932')
            except UnicodeError:continue
            if not any(ord(c)>127 for c in text) or any(ord(c)<32 and c not in '\n\r\t' for c in text):continue
            key=(BASE+at,BASE+at+len(raw))
            candidate=candidates.setdefault(key,{'lo':key[0],'hi':key[1],'bytes':len(raw),'Japanese':text,
                'source_hex':raw.hex(),'source_records':[],'absolute_aliases':[],'ARM_branch_leads':[],'ADR_leads':[]})
            candidate['source_records'].append({'batch':str(path),'id':row.get('id')})
    rows=sorted(candidates.values(),key=lambda r:(r['lo'],r['hi']));starts=[r['lo'] for r in rows]
    def owners(target):
        for r in rows[:bisect.bisect_right(starts,target)]:
            if target<r['hi']:yield r
    if rows:
        for name,base,raw in units(rom)+[('ARM7',rom.rom.arm7RamAddress,bytes(rom.rom.arm7))]:
            for match in re.finditer(rb'(?=(...\x02))',raw,re.DOTALL):
                target=int.from_bytes(match.group(1),'little')
                if starts[0]<=target<rows[-1]['hi']:
                    for row in owners(target):row['absolute_aliases'].append([name,base+match.start(),target])
            for offset in range(0,len(raw)-3,4):
                word=struct.unpack_from('<I',raw,offset)[0];target=None;kind=None
                if word&0x0E000000==0x0A000000:
                    delta=word&0xffffff
                    if delta&0x800000:delta-=0x1000000
                    target=base+offset+8+4*delta;kind='ARM_branch_leads'
                elif word&0x0E0F0000==0x020F0000 and (word>>21)&15 in(2,4):
                    v,shift=word&255,((word>>8)&15)*2
                    v=((v>>shift)|(v<<(32-shift)))&0xffffffff if shift else v
                    target=base+offset+8+(v if (word>>21)&15==4 else -v);kind='ADR_leads'
                if target is not None and starts[0]<=target<rows[-1]['hi']:
                    for row in owners(target):row[kind].append([name,base+offset,target])
    leads=[r for r in rows if not any(r[k] for k in('absolute_aliases','ARM_branch_leads','ADR_leads'))]
    save(ROOT/'unchanged_Japanese_allocations_NOT_FREE.json',{'source_ROM_sha256':sha(CURRENT.read_bytes()),
        'documented_exact_clean_and_current_Japanese_allocations':rows,'no_direct_reference_leads':leads,
        'scope':'Discovery only. Packed/computed references,crossing strings,original consumers,replacement ownership and runtime writes remain unproven. No storage approval or ROM change.',
        'producer_sha256':sha(Path(__file__).read_bytes())})
    for row in sorted(leads,key=lambda r:r['bytes'],reverse=True)[:20]:
        print(hex(row['lo']),row['bytes'],row['Japanese'].replace('\n',' / '),flush=True)
    print(f'{len(rows)} documented unchanged Japanese allocations;{len(leads)} unapproved no-direct-reference leads.',flush=True)


if __name__=='__main__':main()
