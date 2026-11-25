"""Reuse the source-qualified excerpt selection with the exact stored English commands."""
import os
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ROOT=Path('work/analysis/Hodram_B156_cinematic_English_fixture_20261102')
REBUILT=Path('work/analysis/Hodram_B151_B170_rebuilt_20261102/reconstruction.json')
SOURCE=Path('work/analysis/Hodram_B156_cinematic_source_probe_20261102/fixture.json')
STORED=Path('work/analysis/Hodram_B151_B170_stored_20261102/stored_native_verification.json')

if __name__=='__main__':
    assert not ROOT.exists();rebuilt,source,stored=map(load,[REBUILT,SOURCE,STORED])
    assert stored['reconstruction_sha256']==sha(REBUILT.read_bytes()) and stored['complete_stored_pages']==650
    parent=Path(rebuilt['research_ROM']);assert sha(parent.read_bytes())==rebuilt['research_ROM_sha256']
    image=NdsImage.open(parent);arm=image.read_file('/__arm9__.bin');path='/data/SC1.DK4';archive=image.read_file(path);bank=IlnkContainer.parse(archive).blocks
    group=next(g for g in rebuilt['groups'] if g['block']==156);assert sha(bank[156])==group['target_sha256']
    inventory,_,_=scoped_inventory();opening,speeches=inventory(arm,bank[42]);first=speeches[0]['offset'];assert first==42
    initializers=[c for c in opening if c['offset']<first];assert initializers==source['original_B42_initializer_commands']
    target_commands={c['offset']:c for c in group['all_target_commands']};maps={c['old_offset']:c for c in group['command_map']}
    records={r['id']:r for r in load(rebuilt['manuscript'])['records']};texts={r['id']:r for r in group['text_records']}
    logical=bytearray(bank[42][:8]+bank[42][8:first]);mapped=[];fe=[]
    for selected in source['selected_source_commands']:
        old=selected['source_offset'];at=maps[old]['new_offset'];c=target_commands[at];raw=bytes.fromhex(c['whole_command_hex'])
        assert c['word']==selected['word'] and c['word'] not in [0x100,0x200,0x300,0x400,0]
        assert bank[156][at:at+len(raw)]==raw
        if c['word']==0x4000:
            r=records[selected['id']];text=texts[r['id']];encoded=bytes.fromhex(text['stored_hex'])
            assert raw[:6]==bytes.fromhex(selected['whole_source_command_hex'])[:6]
            assert raw[5:6+len(encoded)]==encoded+b'\0'
            # Native command extent can include one nontext alignment NUL.
            assert len(raw)-6-len(encoded) in [0,1] and not any(raw[6+len(encoded):])
            body=encoded[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
            if r['source_selector']==254:fe.append(body.hex())
        else:
            assert raw.hex()==selected['whole_source_command_hex'];body=None
        mapped.append(dict(id=selected['id'],source_offset=old,stored_offset=at,fixture_offset=len(logical),word=c['word'],
            whole_target_command_hex=raw.hex(),expected_expanded_body_hex=None if body is None else body.hex(),
            source_selector=None if selected['id'] is None else records[selected['id']]['source_selector']))
        logical+=raw
    logical+=b'\0'*4;struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    commands,spoken=inventory(arm,target);assert len(commands)==67 and len(spoken)==31 and len(fe)==23
    for row in mapped:
        actual=next(c for c in commands if c['offset']==row['fixture_offset']);assert actual['whole_command_hex']==row['whole_target_command_hex']
    changed=list(bank);changed[42]=target;image.replace_file(path,IlnkContainer(changed).to_bytes());baseline=NdsImage.open(parent)
    assert all(image.read_file(p)==v for p,v in baseline.iter_components()) and [p for _,p,v in baseline.iter_files() if image.read_file(p)!=v]==[path]
    restored=list(changed);restored[42]=bank[42];assert IlnkContainer(restored).to_bytes()==archive
    ROOT.mkdir(parents=True);rom=ROOT/'Hodram_B156_cinematic_English_RESEARCH_ONLY.nds';image.save(rom)
    inputs=ROOT/'inputs.json';assert sha(Path(source['inputs']).read_bytes())==source['inputs_sha256'];save(inputs,load(source['inputs']))
    save(ROOT/'fixture.json',dict(parent=str(parent),parent_sha256=sha(parent.read_bytes()),research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),
        text_language='reviewed-English',source_fixture=str(SOURCE),source_fixture_sha256=sha(SOURCE.read_bytes()),
        source_spans=source['source_spans'],selected_target_commands=mapped,expected_FE_bodies_hex=fe,fixture_speeches=31,source_FE_speeches=23,
        original_initializer_commands=initializers,fixture_block_hex=target.hex(),frames=15001,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),
        all_selected_source_controls_andEnglish_stored_commands_preserved=True,source_wrapper_andother_dialogue_still_explicitly_excluded=True,
        source_selection_not_reinvented_or_condition_results_overridden=True,no_savestate_battery_RAM_roster_money_orRNG_override=True,
        not_natural_endgame_activation_or_earned_plot_progress=True,not_registered_release_or_testing_handoff=True,
        stored_verification=str(STORED),stored_verification_sha256=sha(STORED.read_bytes()),new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [REBUILT,SOURCE,STORED,Path(__file__)]}))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins);assert not any(Path(p['path']).resolve()==rom.resolve() for p in values)
    values.append(dict(path=str(rom.resolve()),reason='English B156 cinematic source-qualified QA fixture;preserve all ROMs. SHA256 '+sha(rom.read_bytes())))
    (ROOT/'pins.before.json').write_bytes(before);tmp=pins.with_name('rom_retention_pins.B156_English.pending.json');assert not tmp.exists();save(tmp,values)
    assert pins.read_bytes()==before;os.replace(tmp,pins)
    print('One pinned English content fixture:31 stored speeches/all23 cinematic FE panels;original effects/initializers andexact source selection retained. Not natural endgame activation.')
