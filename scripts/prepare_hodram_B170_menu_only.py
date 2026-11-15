"""Omit the already-checked page/name prefix and exercise only the original long-menu tail."""
from pathlib import Path
import os
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ROOT=Path('work/analysis/Hodram_B170_menu_only_20261102')
PREVIOUS=Path('work/analysis/Hodram_B151_B170_focused_20261102/fixture.json')
if __name__=='__main__':
    assert not ROOT.exists();prior=load(PREVIOUS);reference=Path(prior['parent']);assert sha(reference.read_bytes())==prior['parent_sha256']
    image=NdsImage.open(reference);arm=image.read_file('/__arm9__.bin');path='/data/SC1.DK4';archive=image.read_file(path);bank=IlnkContainer.parse(archive).blocks
    start,end=prior['source_tail_offset'],prior['source_tail_end'];tail=bank[170][start:end]
    inventory,_,_=scoped_inventory();commands,speeches=inventory(arm,bank[42]);assert speeches[0]['offset']==42
    logical=bytearray(bank[42][:42]+tail);struct.pack_into('<H',logical,4,len(logical)-8);block=bytes(logical)+bytes(-len(logical)%4)
    actual,texts=inventory(arm,block);assert actual[-1]['word']==0 and len(texts)==len([r for r in prior['selected_records'] if r['block']==170])
    old_commands,_=inventory(arm,bank[170]);selected=[c for c in old_commands if c['offset']>=start];shift=42-start
    for old in selected:
        new=next(c for c in actual if c['offset']==old['offset']+shift);assert old['whole_command_hex']==new['whole_command_hex']
    changed=list(bank);changed[42]=block;image.replace_file(path,IlnkContainer(changed).to_bytes());parent=NdsImage.open(reference)
    assert all(image.read_file(p)==v for p,v in parent.iter_components()) and [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==[path]
    restored=list(changed);restored[42]=bank[42];assert IlnkContainer(restored).to_bytes()==archive
    ROOT.mkdir(parents=True);rom=ROOT/'Hodram_B170_long_menu_second_index_RESEARCH_ONLY.nds';image.save(rom)
    ordinary=Path('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json');inputs=ROOT/'inputs.json'
    save(inputs,load(ordinary)+[dict(start=3600,duration=3,buttons=['DOWN'])]+[dict(start=f,duration=5,buttons=['A']) for f in range(4000,9500,240)])
    rows=[]
    for old in prior['selected_records']:
        if old['block']!=170:continue
        row={**old,'fixture_offset':old['stored_command_offset']+shift};rows.append(row)
    save(ROOT/'fixture.json',dict(research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),text_language='reviewed-English',
        parent=str(reference),parent_sha256=sha(reference.read_bytes()),source_menu_tail_only=True,source_menu_tail_andall_effects_byte_exact=True,
        original_menu_source_block=170,original_menu_source_command_offset=1314,long_menu_labels=prior['long_menu_labels'],selected_records=rows,
        long_menu_fixture_offset=42,frames=10001,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),expected_FE_bodies_hex=[],
        only_original_initializers_andcomplete_original_menu_tail_used=True,already_tested_page_speaker_prefix_not_replayed=True,
        planned_second_index_not_a_result_claim=True,no_savestate_battery_RAM_flags_roster_money_orRNG_override=True,
        outer_story_conditions_excluded_not_natural_quest_activation=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PREVIOUS,ordinary,Path(__file__)]}))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    assert not any(Path(p['path']).resolve()==rom.resolve() for p in values);values.append(dict(path=str(rom.resolve()),reason='Focused second-index long-menu controller test;preserve all ROMs. SHA256 '+sha(rom.read_bytes())))
    (ROOT/'pins.before.json').write_bytes(before);tmp=pins.with_name('rom_retention_pins.B170_menu.pending.json');assert not tmp.exists();save(tmp,values)
    assert pins.read_bytes()==before;os.replace(tmp,pins)
    print('Pinned menu-only second-index fixture;the previously checked page/name prefix is excluded. Actual selection/highlight/response pending.')
