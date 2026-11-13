"""Use exact clean commands to check the four source actor-8 headers and named FE contrast."""
from copy import deepcopy
from pathlib import Path
import os
import struct

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.prepare_reviewed_dialogue_fixtures_v1 import ORDINARY

ROOT=Path('work/analysis/Rafael_B166_B167_current1674_20261105')
CLEAN=Path('work/clean.nds')
SOURCE=ROOT/'current_effective.json'
OUT=ROOT/'source_actor8_fixture_v1'
PINS=Path('translations/rom_retention_pins.json')
FILE='/data/SC0.DK4'
SELECTORS={
    584:[(0x8000,'0080ffff08ff0030')],
    658:[(0x8000,'0080ffff08ff0030')],
    770:[(0x8100,'00819f00')],
    779:[],
}


def main():
    assert not OUT.exists()
    assert sha(CLEAN.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    clean=NdsImage.open(CLEAN)
    arm=clean.read_file('/__arm9__.bin')
    archive=clean.read_file(FILE)
    blocks=IlnkContainer.parse(archive).blocks
    inventory,_,_=scoped_inventory()
    opening,opening_speeches=inventory(arm,blocks[44])
    first=opening_speeches[0]['offset']
    assert first==40 and len([c for c in opening if c['offset']<first])==10
    group=next(g for g in load(SOURCE)['groups'] if g['block']==166)
    commands=group['all_source_commands']
    assert sha(blocks[166])==group['clean_block_sha256']
    assert inventory(arm,blocks[166])[0]==commands
    rows={r['source_reference']['record_index']:r for r in group['records']}
    block=bytearray(blocks[44][:first])
    copied=[]
    for index in (183,584,658,770,779):
        row=rows[index]
        off=row['source_reference']['header_offset']
        pos=next(i for i,c in enumerate(commands) if c['offset']==off)
        speech=commands[pos]
        assert speech['word']==0x4000
        assert row['source_selector']==(254 if index==183 else 8)
        query=SELECTORS.get(index,[])
        context=commands[max(0,pos-6):pos]
        extras=[]
        for word,raw in query:
            choices=[c for c in context if (c['word'],c['whole_command_hex'])==(word,raw)]
            assert len(choices)==1
            extras.extend(choices)
        for command in (*extras,speech):
            copied.append(dict(id=row['id'],source_offset=command['offset'],fixture_offset=len(block),
                word=command['word'],whole_command_hex=command['whole_command_hex'],source_speaker=row['source_selector']))
            block+=bytes.fromhex(command['whole_command_hex'])
    end=commands[-1]
    assert end['word']==0
    block+=bytes.fromhex(end['whole_command_hex'])
    struct.pack_into('<H',block,4,len(block)-8)
    block+=bytes(-len(block)%4)
    fixture_commands,texts=inventory(arm,bytes(block))
    assert len(texts)==5 and all(next(c for c in fixture_commands if c['offset']==r['fixture_offset'])['whole_command_hex']
        ==r['whole_command_hex'] for r in copied)
    out=deepcopy(clean)
    changed=list(blocks);changed[44]=bytes(block)
    out.replace_file(FILE,IlnkContainer(changed).to_bytes())
    assert [p for _,p,b in clean.iter_files() if out.read_file(p)!=b]==[FILE]
    assert all(out.read_file(p)==b for p,b in clean.iter_components())
    OUT.mkdir()
    rom=OUT/'source_actor8_RESEARCH_ONLY.nds'
    out.save(rom)
    inverse=NdsImage.open(rom);inverse.replace_file(FILE,archive)
    assert bytes(inverse.rom.save())==CLEAN.read_bytes()
    controls=OUT/'ordinary_inputs.json'
    frames=6201
    save(controls,load(ORDINARY)+[dict(start=f,duration=5,buttons=['A']) for f in range(4000,frames-500,240)])
    save(OUT/'fixture.json',dict(rom=str(rom),rom_sha256=sha(rom.read_bytes()),frames=frames,inputs=str(controls),
        inputs_sha256=sha(controls.read_bytes()),clean_ROM_sha256=sha(CLEAN.read_bytes()),copied=copied,
        clean_content_and_native_renderer_with_disclosed_B44_initializer=True,original_branches_and_full_route=False,
        exact_source_queries_and_speech_commands=True,branch_outcomes_not_simulated=True,full_parent_inverse=True))
    pins=load(PINS)
    before=PINS.read_bytes()
    assert not any(Path(p['path']).resolve()==rom.resolve() for p in pins)
    pins.append(dict(path=str(rom.resolve()),reason='Preserve exact clean actor-8 source fixture and inverse. SHA256 '+sha(rom.read_bytes())))
    pending=PINS.with_name('rom_retention_pins.source_actor8_v1.pending.json')
    assert not pending.exists()
    save(pending,pins)
    assert PINS.read_bytes()==before
    os.replace(pending,PINS)
    print(rom,sha(rom.read_bytes()))


if __name__=='__main__':
    main()
