"""Prepare exact source display excerpts after original initialization; never a release."""
import os
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ROOT=Path('work/analysis/Hodram_B156_cinematic_source_probe_20261102')
SOURCE=Path('work/analysis/Hodram_B151_B170_clean_20261102/clean_source_packet.json')
PARENT=Path('out/all_routes_combined_hodram_b131_b150_names_20261102_candidate.nds')


if __name__=='__main__':
    assert not ROOT.exists()
    packet=load(SOURCE);source=next(g for g in packet['groups'] if g['block']==156)
    assert sha(PARENT.read_bytes())=='7fb6f6d78441a705c137003d8bfc92d4f5b43fd56b85178a59224f3b4570bc04'
    parent=NdsImage.open(PARENT);arm=parent.read_file('/__arm9__.bin');path='/data/SC1.DK4'
    archive=parent.read_file(path);bank=IlnkContainer.parse(archive).blocks
    clean=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file(path)).blocks
    jp=clean[156];assert sha(jp)==source['clean_block_sha256']
    inventory,_,_=scoped_inventory();opening,spoken=inventory(arm,bank[42]);first=spoken[0]['offset']
    assert first==42 and bank[42][8:first]==clean[42][8:first]
    initializers=[c for c in opening if c['offset']<first];assert len(initializers)==8
    spans=[(1978,3294),(3298,3306),(3382,3388),(4360,4530)]
    selected=[c for c in source['all_source_commands'] if any(a<=c['offset']<b for a,b in spans)]
    assert len(selected)==58 and sum(c['word']==0x4000 for c in selected)==31
    logical=bytearray(bank[42][:8]+bank[42][8:first]);mapped=[]
    for a,b in spans:
        members=[c for c in selected if a<=c['offset']<b]
        assert members[0]['offset']==a
        for command in members:
            raw=bytes.fromhex(command['whole_command_hex']);at=command['offset']
            assert jp[at:at+len(raw)]==raw and command['word'] not in [0x100,0x200,0x300,0x400,0]
            row=next((r for r in source['records'] if r['source_reference']['header_offset']==at),None)
            mapped.append(dict(source_block=156,source_offset=at,fixture_offset=len(logical),
                word=command['word'],whole_source_command_hex=raw.hex(),id=None if row is None else row['id']))
            logical+=raw
        assert members[-1]['offset']+len(bytes.fromhex(members[-1]['whole_command_hex']))==b
    logical+=b'\0'*4;struct.pack_into('<H',logical,4,len(logical)-8)
    target=bytes(logical)+bytes(-len(logical)%4)
    commands,speeches=inventory(arm,target)
    assert len(commands)==67 and len(speeches)==31 and commands[-1]['word']==0
    for row in mapped:
        actual=next(c for c in commands if c['offset']==row['fixture_offset'])
        assert actual['word']==row['word'] and actual['whole_command_hex']==row['whole_source_command_hex']
    fe=[r for r in source['records'] if r['source_selector']==254]
    assert len(fe)==23 and {r['id'] for r in fe}<={r['id'] for r in mapped}
    changed=list(bank);changed[42]=target
    image=NdsImage.open(PARENT);image.replace_file(path,IlnkContainer(changed).to_bytes())
    assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==[path]
    assert all(image.read_file(p)==v for p,v in parent.iter_components())
    restored=list(changed);restored[42]=bank[42];assert IlnkContainer(restored).to_bytes()==archive
    ROOT.mkdir(parents=True);rom=ROOT/'Hodram_B156_cinematic_source_RESEARCH_ONLY.nds';image.save(rom)
    ordinary=Path('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json')
    inputs=ROOT/'inputs.json';save(inputs,load(ordinary)+[dict(start=f,duration=5,buttons=['A']) for f in range(4000,14600,240)])
    save(ROOT/'fixture.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),source_spans=spans,selected_source_commands=mapped,
        source_FE_records=fe,expected_FE_bodies_hex=[r['source_Japanese'].replace('FI','Hodram').encode('cp932').hex() for r in fe],
        original_B42_initializer_commands=initializers,fixture_block=42,fixture_block_hex=target.hex(),fixture_speeches=31,source_FE_speeches=23,
        source_commands_preserved_byte_for_byte=True,source_condition_wrapper_andother_dialogue_explicitly_excluded=True,
        selected_original_effect_commands_preserved_not_claimed_purely_visual=True,
        no_savestate_battery_RAM_roster_money_RNG_orcondition_result_override=True,
        not_natural_endgame_activation_or_plot_completion=True,not_registered_candidate_orrelease_parent=True,
        complete_archive_andall_other_components_inverse_exact=True,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),frames=15001,
        actual_capture_andgeometry_qualification_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,ordinary,Path(__file__)]}))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    assert not any(Path(v['path']).resolve()==rom.resolve() for v in values)
    values.append(dict(path=str(rom.resolve()),reason='Source-qualified B156 cinematic geometry content fixture;preserve every ROM. SHA256 '+sha(rom.read_bytes())))
    (ROOT/'pins.before.json').write_bytes(before)
    temporary=pins.with_name('rom_retention_pins.B156_pending.json');assert not temporary.exists()
    save(temporary,values);assert pins.read_bytes()==before;os.replace(temporary,pins)
    print('Pinned one research source fixture:58 exact source commands/31 speeches/all23 cinematic FE bodies plus8 original initializers;no release orcoverage credit.')
