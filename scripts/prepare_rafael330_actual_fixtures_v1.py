"""Prepare one complete bullfight scene andfocused display/menu QA sequences from exact stored commands."""
import os,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ROOT=Path('work/analysis/Rafael330_actual_fixtures_20261105')
REBUILT=Path('work/analysis/Rafael330_stored_consumer_inputs_20261105/native_consumer_reconstruction.json')
STORED=Path('work/analysis/Rafael330_stored_native_20261105/stored_native_verification.json')
ORDINARY=Path('work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104/ordinary_Rafael_NewGame_inputs_v1.json')

if __name__=='__main__':
    assert not ROOT.exists();rebuilt,stored=map(load,[REBUILT,STORED])
    assert stored['reconstruction_sha256']==sha(REBUILT.read_bytes()) and stored['complete_stored_pages']==336
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    parent=Path(rebuilt['research_ROM']);assert sha(parent.read_bytes())==rebuilt['research_ROM_sha256']
    image=NdsImage.open(parent);arm=image.read_file('/__arm9__.bin');archive=image.read_file('/data/SC0.DK4')
    bank=IlnkContainer.parse(archive).blocks;inventory,_,_=scoped_inventory()
    opening,texts=inventory(arm,bank[44]);first=texts[0]['offset'];assert first==40
    initializers=[c for c in opening if c['offset']<first];assert len(initializers)==10
    doc=load(Path(rebuilt['manuscript']));byid={r['id']:r for r in doc['records']};groups={g['block']:g for g in rebuilt['groups']}
    byactor={};selected=set()
    native=load(Path(rebuilt['native']))
    for row in doc['records']:
        if row['source_selector']!=254:byactor.setdefault(row['source_selector'],row['id'])
        if row.get('source_editorial_ID') in ['DK4_MES_B84_R0470','DK4_MES_B84_R0539']:selected.add(row['id'])
        if row['id'] in ['DK4_MES_B82_R0133','DK4_MES_B84_R0060','DK4_MES_B84_R0093','DK4_MES_B84_R0507','DK4_MES_B84_R0566','DK4_MES_B84_R0577']:selected.add(row['id'])
    assert len(byactor)==16;selected.update(byactor.values())
    selected.update(r['id'] for r in native['records'] if len(r['complete_native_English_display'].get('pages',[]))>1)
    assert len([r for r in selected if '_FE_PAGE_' in r])==4
    ROOT.mkdir();created=[]
    for name,mode,frames in [('B81_complete_bullfight','whole',24001),('names_pages_FE_transitions','display',18001),('B84_two_andthree_choice','menus',10001)]:
        logical=bytearray(bank[44][:first]);copied=[];bindings=[];excluded=[];menus=[]
        blocklist=[81] if mode=='whole' else [84] if mode=='menus' else [81,82,83,84]
        for block in blocklist:
            group=groups[block];byoffset={t['new_offset']-5:t for t in group['text_records']}
            if mode=='whole':
                shift=len(logical)-8;logical+=bank[block][8:group['new_logical_end']]
                commands=group['all_target_commands']
            else:
                commands=[]
                for command in group['all_target_commands']:
                    text=byoffset.get(command['offset'])
                    keep=(text and text['id'] in selected) if mode=='display' else ((text and text['id'] in ['DK4_MES_B84_R0215','DK4_MES_B84_R0417','DK4_MES_B84_R0487']) or command['word'] in [0x2100,0x2200])
                    if keep:commands.append(command)
                    else:excluded.append(dict(block=block,**command))
            for command in commands:
                offset=command['offset'];at=offset+shift if mode=='whole' else len(logical)
                if mode!='whole':logical+=bytes.fromhex(command['whole_command_hex'])
                copied.append(dict(block=block,original_offset=offset,fixture_offset=at,whole_command_hex=command['whole_command_hex'],word=command['word']))
                if command['word']==0x4000:
                    text=byoffset[offset];row=byid[text['id']];encoded=bytes.fromhex(text['stored_hex'])
                    assert command['whole_command_hex'][:12]==row['source_complete_preamble_hex']
                    bindings.append(dict(id=row['id'],source_editorial_ID=row.get('source_editorial_ID',row['id']),block=block,
                        fixture_offset=at,stored_command_offset=offset,stored_hex=text['stored_hex'],selector=row['source_selector'],logical_English=row['english'],
                        expected_expanded_body_hex=encoded[1:].replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.').hex()))
                elif command['word'] in [0x2100,0x2200]:menus.append(dict(block=block,fixture_offset=at,stored_command_offset=offset,word=command['word'],command_hex=command['whole_command_hex']))
        if mode!='whole':logical+=bytes.fromhex(groups[84]['all_target_commands'][-1]['whole_command_hex'])
        struct.pack_into('<H',logical,4,len(logical)-8);fixtureblock=bytes(logical)+bytes(-len(logical)%4)
        commands,speeches=inventory(arm,fixtureblock);assert len(speeches)==len(bindings)
        assert commands[-1]['word']==0 and commands[-1]['offset']+4==len(logical)
        for c in copied:
            found=next(v for v in commands if v['offset']==c['fixture_offset']);assert found['whole_command_hex']==c['whole_command_hex'] and found['word']==c['word']
        if mode=='whole':assert len(copied)==101 and len(bindings)==51
        if mode=='display':assert {b['id'] for b in bindings}==selected and len({b['selector'] for b in bindings if b['selector']!=254})==16
        if mode=='menus':assert [m['word'] for m in menus]==[0x2100,0x2200] and len(bindings)==3
        changed=list(bank);changed[44]=fixtureblock;fixture=NdsImage.open(parent);fixture.replace_file('/data/SC0.DK4',IlnkContainer(changed).to_bytes())
        assert [p for _,p,v in image.iter_files() if fixture.read_file(p)!=v]==['/data/SC0.DK4']
        assert all(fixture.read_file(p)==v for p,v in image.iter_components())
        rom=ROOT/(name+'_RESEARCH_ONLY.nds');fixture.save(rom)
        inverse=NdsImage.open(rom);inverse.replace_file('/data/SC0.DK4',archive);assert bytes(inverse.rom.save())==parent.read_bytes()
        inputs=ROOT/(name+'_inputs.json');save(inputs,load(ORDINARY)+[dict(start=f,duration=5,buttons=['A']) for f in range(4000,frames-500,240)])
        proof=ROOT/(name+'_fixture.json');save(proof,dict(research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),parent=str(parent),parent_sha256=sha(parent.read_bytes()),
            text_language='reviewed-English',purpose=name,frames=frames,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),
            expected_FE_bodies_hex=[r['expected_expanded_body_hex'] for r in bindings if r['selector']==254],
            selected_records=bindings,selected_source_blocks=blocklist,copied_commands=copied,original_initializers=initializers,menus=menus,
            complete_original_scene_including_transitions_andbranches_retained=mode=='whole',excluded_nontext_commands=excluded,
            focused_fixture_not_a_complete_story_exchange=mode!='whole',all_selected_command_bytes_andcomplete_speaker_controls_exact=True,
            original_location_earned_chronology_natural_activation_fullroute_andhardware_unvisited=True,
            no_savestate_battery_RAM_roster_money_RNG_eventflag_orcondition_result_override=True,
            all_unowned_files_components_andserialized_parent_inverse_exact=True,
            not_registered_candidate_or_natural_activation=True,new_credit=0,guide_photos=False,
            evidence={str(p):sha(p.read_bytes()) for p in [REBUILT,STORED,ORDINARY,Path(__file__)]}))
        created.append(dict(fixture=str(proof),fixture_sha256=sha(proof.read_bytes()),path=str(rom),sha256=sha(rom.read_bytes()),records=len(bindings),menus=len(menus)))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    for item in created:
        path=Path(item['path']);assert not any(Path(v['path']).resolve()==path.resolve() for v in values)
        values.append(dict(path=str(path.resolve()),reason='Preserve initialized Rafael330 actual QA fixture. SHA256 '+item['sha256']))
    (ROOT/'pins.before.json').write_bytes(before);pending=pins.with_name('rom_retention_pins.Rafael330_actual.pending.json');assert not pending.exists();save(pending,values)
    assert pins.read_bytes()==before;os.replace(pending,pins)
    save(ROOT/'fixtures.json',dict(fixtures=created,actual_observation_pending=True,new_credit=0,guide_photos=False))
    print('Prepared full51-speech B81/101-command scene,focused16-name/FE/page sequence andtwo/three-choice fixture;actual observations pending.')
