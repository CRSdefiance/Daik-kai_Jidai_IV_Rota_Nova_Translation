"""Disclose a bounded display fixture covering names, glyphs and changed page breaks."""
import os,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ROOT=Path('work/analysis/Rafael_B36_B41_focused_actual_fixture_20261104')
REBUILT=Path('work/analysis/Rafael_B36_B41_rebuilt_20261104/reconstruction.json')
STORED=Path('work/analysis/Rafael_B36_B41_stored_native_20261104/stored_native_verification.json')
ORDINARY=Path('work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104/ordinary_Rafael_NewGame_inputs_v1.json')
RISKS={'DK4_MES_B36_R0046','DK4_MES_B37_R0099','DK4_MES_B37_R0254','DK4_MES_B37_R0267','DK4_MES_B39_R0024','DK4_MES_B41_R0131'}

if __name__=='__main__':
    assert not ROOT.exists()
    rebuilt,stored=map(load,[REBUILT,STORED]);doc=load(rebuilt['manuscript'])
    assert rebuilt['old_stored_native_sha256']==sha(STORED.read_bytes()) and rebuilt['all_prior_tutorial_changes_preserved']
    parent=Path(rebuilt['research_ROM']);assert sha(parent.read_bytes())==rebuilt['research_ROM_sha256']
    image=NdsImage.open(parent);arm=image.read_file('/__arm9__.bin');archive=image.read_file(doc['file_path'])
    bank=IlnkContainer.parse(archive).blocks;inventory,_,_=scoped_inventory()
    opening,texts=inventory(arm,bank[44]);first=texts[0]['offset']
    assert first==40 and len([c for c in opening if c['offset']<first])==10
    by_actor={}
    for row in doc['records']:by_actor.setdefault(row['source_selector'],row['id'])
    assert set(by_actor)=={0,4,5,6,8,31,34,51,75,151,153}
    selected=RISKS|set(by_actor.values());rows={r['id']:r for r in doc['records']}
    commands={t['id']:(g,next(c for c in g['all_target_commands'] if c['offset']==t['new_offset']-5),t)
        for g in rebuilt['groups'] for t in g['text_records']}
    expanded={r['id']:r['expanded_hex'] for r in stored['records']}
    logical=bytearray(bank[44][:first]);bindings=[];copied=[]
    for row in doc['records']:
        if row['id'] not in selected:continue
        group,command,text=commands[row['id']];raw=bytes.fromhex(command['whole_command_hex'])
        encoded=bytes.fromhex(text['stored_hex'])
        assert raw[:6].hex()==row['source_complete_preamble_hex'] and raw[5:6+len(encoded)]==encoded+b'\0'
        at=len(logical);logical+=raw
        bindings.append(dict(id=row['id'],block=row['block'],selector=row['source_selector'],fixture_offset=at,
            stored_command_offset=command['offset'],stored_hex=text['stored_hex'],expected_expanded_body_hex=expanded[row['id']],logical_English=row['english']))
        copied.append(dict(block=row['block'],original_offset=command['offset'],fixture_offset=at,whole_command_hex=command['whole_command_hex'],word=command['word']))
    terminal=rebuilt['groups'][-1]['all_target_commands'][-1];assert terminal['word']==0
    logical+=bytes.fromhex(terminal['whole_command_hex']);struct.pack_into('<H',logical,4,len(logical)-8)
    block=bytes(logical)+bytes(-len(logical)%4);actual,actual_texts=inventory(arm,block)
    assert len(actual_texts)==len(selected) and actual[-1]['word']==0 and actual[-1]['offset']+4==len(logical)
    assert all(next(c for c in actual if c['offset']==r['fixture_offset'])['whole_command_hex']==r['whole_command_hex'] for r in copied)
    changed=list(bank);changed[44]=block
    fixture=NdsImage.open(parent);fixture.replace_file(doc['file_path'],IlnkContainer(changed).to_bytes())
    assert [p for _,p,v in image.iter_files() if fixture.read_file(p)!=v]==[doc['file_path']]
    assert all(fixture.read_file(p)==v for p,v in image.iter_components())
    ROOT.mkdir();rom=ROOT/'focused_display_RESEARCH_ONLY.nds';fixture.save(rom)
    restored=NdsImage.open(rom);restored.replace_file(doc['file_path'],archive);assert bytes(restored.rom.save())==parent.read_bytes()
    inputs=ROOT/'focused_inputs.json';save(inputs,load(ORDINARY)+[dict(start=f,duration=5,buttons=['A']) for f in range(4000,9500,240)])
    save(ROOT/'focused_fixture.json',dict(research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),parent=str(parent),parent_sha256=sha(parent.read_bytes()),
        text_language='reviewed-English',purpose='Rafael_B36_B41_names_FU_two_ASCII_I_four_wrap_andtwo_page_display_cases',frames=10001,
        inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),expected_FE_bodies_hex=[],selected_records=bindings,selected_source_blocks=list(range(36,42)),
        copied_commands=copied,original_initializers=[c for c in opening if c['offset']<first],required_risk_IDs=sorted(RISKS),ordinary_actor_IDs=sorted(by_actor),
        initialized_opening_content_fixture=True,synthetic_cross_scene_QA_sequence_not_a_story_exchange=True,
        complete_original_scene_including_transitions_andbranches_retained=False,all_selected_speech_commands_andpreambles_byte_exact=True,
        omitted_source_speeches=175-len(selected),omitted_conditions_branches_andscene_effects=True,
        all175_complete_conversations_reviewed_offline_butnot_claimed_observed=True,original_location_earned_chronology_fullroute_andhardware_unvisited=True,
        no_savestate_battery_RAM_roster_money_RNG_orcondition_result_override=True,all_unowned_files_components_andserialized_parent_inverse_exact=True,
        not_registered_candidate_or_natural_activation=True,catalogue_name_changes_not_applied=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [REBUILT,STORED,ORDINARY,Path(__file__)]}))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    assert not any(Path(v['path']).resolve()==rom.resolve() for v in values)
    values.append(dict(path=str(rom.resolve()),reason='Preserve disclosed bounded Rafael display fixture;all earlier ROMs retained. SHA256 '+sha(rom.read_bytes())))
    (ROOT/'pins.before.json').write_bytes(before);temporary=pins.with_name('rom_retention_pins.Rafael_B36_B41_focused.pending.json');assert not temporary.exists()
    save(temporary,values);assert pins.read_bytes()==before;os.replace(temporary,pins)
    print('Prepared',len(selected),'exact speech commands covering11 actors,six concrete glyph/wrap risks;synthetic display fixture only.')
