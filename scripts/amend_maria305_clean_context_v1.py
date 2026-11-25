"""Correct provisional attribution against exact clean actor metadata before comparison."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string

ROOT=Path('work/Maria_B176_B195_clean_20261110')


def main():
    target=ROOT/'meanings_v2.txt';assert not target.exists()
    packet=load(ROOT/'clean_source_packet.json');arm=NdsImage.open(packet['source_ROM']).read_file('/__arm9__.bin')
    assert digest(packet['source_ROM'])==packet['source_ROM_sha256']
    base=struct.unpack_from('<I',arm,0xCDAC0)[0]-0x02000000
    bindings=[]
    for group in packet['groups']:
        for row in group['records']:
            if row['kind']!='ordinary-speech':continue
            actor=int(row['source_hex'][:2],16)
            if actor>=207:continue
            at=base+32*actor;fields=[]
            for column in (0,4,8):
                pointer=struct.unpack_from('<I',arm,at+column)[0]
                fields.append(dict(column=column,field_offset=at+column,field_hex=arm[at+column:at+column+4].hex(),
                    text=string(arm,pointer)['text'] if pointer else '',pointer=pointer))
            bindings.append(dict(id=row['id'],actor_ID=actor,source_reference=row['source_reference'],source_hex=row['source_hex'],fields=fields))
    expected={176:(76,'ミハイル'),178:(15,'アンジェロ'),180:(14,'エミリオ')}
    for block,(actor,name) in expected.items():
        relevant=[r for r in bindings if r['actor_ID']==actor and r['id'].startswith('DK4_MES_B'+str(block)+'_')]
        assert relevant and all(r['fields'][0]['text']==name for r in relevant)
    text=(ROOT/'meanings_v1.txt').read_text(encoding='utf-8');block=None;lines=[]
    for line in text.splitlines():
        if line.startswith('@'):block=int(line[1:].split('|',1)[0])
        if block==176:line=line.replace('Julio','Mikhail')
        elif block==178:line=line.replace('Emilio','Angelo')
        elif block==180:line=line.replace('Angelo','Emilio')
        lines.append(line)
    target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'clean_actor_context_amendment_v1.json',dict(
        records=bindings,provisional_contexts_corrected={str(k):v for k,v in expected.items()},
        individual_source_meanings_corrected_with_context=True,independent_spoken_English_unchanged=True,
        no_current_English_consulted=True,all_five_gates_pending=True,new_credit=0,
        source_metadata_not_native_role_name_orfont_approval=True,
        evidence={str(p):digest(p) for p in [ROOT/'clean_source_packet.json',ROOT/'meanings_v1.txt',target,ROOT/'drafts_authored_v1.txt',Path(__file__)]}))
    print('Corrected three clean actor contexts; original meanings/drafts preserved; current English still unconsulted.')


if __name__=='__main__':main()
