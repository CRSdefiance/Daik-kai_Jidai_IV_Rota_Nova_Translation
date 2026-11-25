"""Seal301 uncredited clean SC3 objects in32 complete exchanges, before current English."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Maria_B0_B32_clean_20261109')
CENSUS=Path('work/story_source_coverage_20261109_SC3_v1/coverage.json')
PACKET=CENSUS.parent/'residual_clean_source_packet.json'

def main():
    assert not ROOT.exists()
    census,packet=map(load,(CENSUS,PACKET));ledger=Path('translations/editorial_review_current_v1.json')
    assert digest(ledger)==census['ledger_sha256'] and load(ledger)['records_editorially_completed']==19161
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    clean_path=Path('work/clean.nds');image=NdsImage.open(clean_path);archive=image.read_file('/data/SC3.DK4');arm=image.read_file('/__arm9__.bin')
    assert digest(clean_path)==census['source_ROM_sha256']==packet['source_ROM_sha256']
    assert sha(archive)==census['source_archive_sha256']==packet['source_archive_sha256']
    blocks=IlnkContainer.parse(archive).blocks
    scope=list(range(15))+list(range(16,33));groups=[];allrows=[]
    for n in scope:
        group=deepcopy(next(g for g in packet['groups'] if g['block']==n));rawblock=blocks[n]
        assert bytes.fromhex(group['clean_block_hex'])==rawblock
        rows=group['records'];assert rows and all(not r['covered'] and not r['exact_credited_source_bindings'] for r in rows)
        commands={c['offset']:c for c in group['all_source_commands']}
        for row in rows:
            ref=row['source_reference'];at=ref['offset'];body=bytes.fromhex(row['source_hex']);command=commands[ref['command_offset']]
            assert rawblock[at:at+len(body)+1]==body+b'\0'
            row.update(source_record_index=rawblock[:at].count(b'\0'),source_command_offset=command['offset'],source_word=command['word'],
                source_0100_ancestors=command['ancestor_0100_offsets'],source_native_extent=command['native_extent'],
                current_English_unconsulted=True,source_meaning_pending=True,localized_draft_pending=True,new_credit=0,
                review=dict(source=False,context=False,localization=False,naturalness=False,formatting=False))
            ref.update(file_path='/data/SC3.DK4',record_index=row['source_record_index'])
            if row['kind']=='ordinary-speech':
                assert command['word']==0x4000 and at==command['offset']+5
                head=rawblock[at-5:at+1];assert head[:5]==bytes.fromhex('0040ffff00')
                row.update(source_selector=body[0],source_complete_preamble_hex=head.hex(),source_presentation_kind='system-FE' if body[0]==254 else 'progressive')
                ref['header_offset']=at-5
            elif row['kind']=='physical-style-alternative':
                raw=bytes.fromhex(command['whole_command_hex']);offsets=struct.unpack_from('<8H',raw,2);rel=at-command['offset']-20
                assert command['word']==0x4100 and raw[18]==0 and rel in offsets
                row.update(source_selector=raw[19],source_header_hex=raw[:20].hex(),source_object_hex=raw.hex(),source_style_indices=[i for i,v in enumerate(offsets) if v==rel])
            else:
                assert row['kind']=='typed-menu-caption' and command['word'] in [0x2100,0x2200]
                count=2 if command['word']==0x2100 else 3;raw=bytes.fromhex(command['whole_command_hex']);offsets=struct.unpack_from('<' + str(count)+'H',raw,2)
                matches=[i for i,v in enumerate(offsets) if command['offset']+2+2*count+v==at];assert len(matches)==1
                row.update(source_index=matches[0],source_choice_object_hex=raw.hex(),source_menu_count=count)
            allrows.append(row)
        group.update(clean_block_sha256=sha(rawblock),all_source_objects_in_block_included=True,
            numeric_order_not_asserted_as_event_chronology=True,current_English_unconsulted=True)
        groups.append(group)
    assert len(allrows)==len({(r['file_path'],r['id']) for r in allrows})==301 and len(groups)==32
    assert Counter(r['kind'] for r in allrows)==Counter({'ordinary-speech':292,'physical-style-alternative':7,'typed-menu-caption':2})
    sections=MainCodeFile(arm,0x02000000).sections
    def read(address,size):
        found=[s for s in sections if s.ramAddress<=address and address+size<=s.ramAddress+len(s.data)];assert len(found)==1
        s=found[0];return bytes(s.data[address-s.ramAddress:address-s.ramAddress+size])
    table=int.from_bytes(read(0x02000000+0xCDAC0,4),'little');actors=[]
    for actor in sorted({r['source_selector'] for r in allrows if r.get('source_selector',254)<207}):
        fields=[]
        for column in [0,4,8]:
            pointer=int.from_bytes(read(table+actor*32+column,4),'little')
            if pointer:
                data=bytearray()
                while (value:=read(pointer+len(data),1))!=b'\0':
                    data+=value;assert len(data)<256
                value=bytes(data)
            else:value=b''
            fields.append(dict(column=column,pointer=pointer,hex=value.hex(),text=value.decode('cp932') if pointer else None))
        actors.append(dict(actor_ID=actor,source_components=fields,components_not_automatic_biography_orconsumer_name_approval=True))
    ROOT.mkdir();save(ROOT/'clean_source_packet.json',dict(route=3,file_path='/data/SC3.DK4',source_ROM=str(clean_path),source_ROM_sha256=digest(clean_path),
        source_archive_sha256=sha(archive),source_ARM9_sha256=sha(arm),blocks=scope,groups=groups,records=301,ordinary_speeches=292,
        physical_style_alternatives=7,typed_captions=2,all301_positions_uncredited=True,current_English_unconsulted=True,
        source_meanings_drafts_contextual_comparisons_andfive_gates_pending=True,no_event_chronology_oractivation_claim=True,new_credit=0,
        evidence={str(p):digest(p) for p in [CENSUS,PACKET,ledger,Path(__file__)]}))
    save(ROOT/'clean_name_components.json',dict(records=actors,source_ARM9_sha256=sha(arm),source_table_pointer=table,
        dynamic_selectors=sorted({r['source_selector'] for r in allrows if 207<=r.get('source_selector',254)<224}),
        source_only_no_current_conversation_English=True,new_credit=0))
    for low,high in [(0,11),(11,22),(22,33)]:
        lines=[]
        for g in groups:
            if not low<=g['block']<high:continue
            lines.append(f"\nBLOCK {g['block']} ({len(g['records'])} objects)")
            for r in g['records']:
                selector='MENU'+str(r['source_index']) if r['kind']=='typed-menu-caption' else str(r['source_selector'])
                lines.append(r['id']+' ['+selector+'] '+r['source_Japanese'].replace('\n',' / '))
        (ROOT/f'clean_reading_B{low}_B{high-1}.txt').write_text('\n'.join(lines)+'\n',encoding='utf8')
    print('Sealed301 clean-source objects in32 complete exchanges:292 ordinary,7 physical styles,two captions;current English unread,zero credit.')

if __name__=='__main__':main()
