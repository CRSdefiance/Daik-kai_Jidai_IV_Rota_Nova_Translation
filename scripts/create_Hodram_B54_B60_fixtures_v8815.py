"""Complete clean/revised Hodram exchanges after the eight original opening initializers.

This is a disclosed ROM entry fixture, never natural optional-event activation.
"""
import json, os, struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/Hodram_B54_B60_fixtures_v8815')
REFERENCE=Path('work/analysis/Hodram_B54_B60_reference_v8812/research_image_receipt.json')
MAP=Path('work/analysis/Hodram_B54_B60_relocation_v8809/reconstruction.json')
CALLERS=Path('work/analysis/Hodram_B54_B60_references_v8814/references.json')

if __name__=='__main__':
    assert not ROOT.exists()
    reference,mapping,callers=map(read,[REFERENCE,MAP,CALLERS])
    assert callers['external_references_complete'] and callers['all152commands82fullpreambles24relatives6queries33nonprose_controls7normalends_bound']
    parentpath=Path(reference['parent']); parent=NdsImage.open(parentpath)
    revisedpath=Path(reference['research_ROM']); revised=NdsImage.open(revisedpath)
    assert sha(parentpath.read_bytes())==reference['parent_sha256'] and sha(revisedpath.read_bytes())==reference['research_ROM_sha256']
    cleanpath=Path('work/clean.nds'); clean=NdsImage.open(cleanpath)
    assert sha(cleanpath.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    file='/data/SC1.DK4'; inventory,_,_=scoped_inventory(); arm=parent.read_file('/__arm9__.bin')
    assert revised.read_file('/__arm9__.bin')==arm and all(revised.read_file(p)==v for p,v in parent.iter_components())
    bank=IlnkContainer.parse(parent.read_file(file)).blocks; cleanbank=IlnkContainer.parse(clean.read_file(file)).blocks
    revisedbank=IlnkContainer.parse(revised.read_file(file)).blocks
    opening=bank[42]; commands,speeches=inventory(arm,opening); first=speeches[0]['offset']; prelude=opening[8:first]; delta=len(prelude)
    initializers=[c for c in commands if c['offset']<first]
    assert first==42 and delta==34 and len(initializers)==8
    assert prelude==cleanbank[42][8:first]
    assert all(c['word'] not in [0x4000,0x100,0x200,0x300,0x400,0x8000,0x8100,0] for c in initializers)
    fixtures=[]; planned=[]
    current=read('work/analysis/Hodram_B54_B60_current_v8799/current_effective.json')
    assert current['current_ROM_sha256']==reference['parent_sha256']
    for group in mapping['groups']:
        if group['block']==55:continue
        group=dict(group,all_source_commands=next(g for g in current['groups'] if g['block']==group['block'])['all_source_commands'])
        number=group['block']; records=group['text_records']
        for version in ['clean_Japanese','revised_English']:
            selected=cleanbank[number] if version=='clean_Japanese' else revisedbank[number]
            selected_commands=group['all_source_commands'] if version=='clean_Japanese' else group['all_target_commands']
            expected=group['clean_block_sha256'] if version=='clean_Japanese' else group['target_block_sha256']
            assert sha(selected)==expected
            end=8+struct.unpack_from('<H',selected,4)[0]
            assert selected[end:]==bytes(len(selected)-end) and selected[:4]==opening[:4] and selected[6:8]==opening[6:8]
            logical=bytearray(opening[:8]+prelude+selected[8:end]); struct.pack_into('<H',logical,4,len(logical)-8)
            target=bytes(logical)+bytes(-len(logical)%4)
            parsed,texts=inventory(arm,target)
            assert len(parsed)==len(selected_commands)+8 and len(texts)==len(records) and len(target)<0x2400
            assert sum(c['word']==0 for c in parsed)==1 and parsed[-1]['offset']+4==len(logical)
            objects=[]; membership=[]; relative=0
            for ordinal,(source,command) in enumerate(zip(group['all_source_commands'],selected_commands,strict=True)):
                at=command['offset']+delta; actual=next(c for c in parsed if c['offset']==at)
                assert actual['word']==command['word']==source['word'] and actual['native_extent']==command['native_extent']
                assert actual['whole_command_hex']==command['whole_command_hex'] and actual['ancestor_0100_offsets']==[a+delta for a in command['ancestor_0100_offsets']]
                if command['word'] in [0x100,0x200,0x300,0x400]:
                    span=struct.unpack_from('<H',selected,command['offset']+2)[0]
                    assert struct.unpack_from('<H',target,at+2)[0]==span and at+4+span==command['offset']+4+span+delta
                    relative+=1
                record=next((r for r in records if r['source_reference']['header_offset']==source['offset']),None) if source['word']==0x4000 else None
                objects.append(dict(original_block=number,source_command_ordinal=ordinal,canonical_clean_offset=source['offset'],original_command_offset=command['offset'],
                    fixture_command_offset=at,native_extent=command['native_extent'],word=command['word'],whole_command_hex=command['whole_command_hex'],
                    text_ID=None if record is None else record['id'],original_0100_ancestors=command['ancestor_0100_offsets'],fixture_0100_ancestors=actual['ancestor_0100_offsets']))
                if command['word']==0x4000:
                    assert record is not None and target[at:at+6].hex()==record['source_complete_preamble_hex']
                    membership.append(dict(id=record['id'],source_record_index=record['source_reference']['record_index'],source_selector=record['source_selector'],
                        source_reference=record['source_reference'],fixture_command_offset=at,fixture_body_offset=at+5))
            assert len(membership)==len(records) and relative==len(group['relative_fixups'])
            image=NdsImage.open(parentpath); blocks=list(bank); blocks[42]=target
            image.replace_file(file,IlnkContainer(blocks).to_bytes())
            assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==[file]
            assert all(image.read_file(p)==v for p,v in parent.iter_components())
            after=IlnkContainer.parse(image.read_file(file)).blocks
            assert [i for i,(a,b) in enumerate(zip(bank,after,strict=True)) if a!=b]==[42]
            restored=list(after); restored[42]=opening; assert IlnkContainer(restored).to_bytes()==parent.read_file(file)
            payload=bytes(image.rom.save()); out=Path(f'out/Hodram_B{number}_{version}_v8815_RESEARCH_ONLY.nds')
            assert not out.exists(); planned.append((out,payload))
            fixtures.append(dict(route=1,route_identity='Hodram',version=version,source_block=number,research_ROM=str(out),research_ROM_sha256=sha(payload),
                parent=str(parentpath),parent_sha256=reference['parent_sha256'],source_file=file,source_block_sha256=expected,
                source_text_ROM=str(cleanpath if version=='clean_Japanese' else revisedpath),fixture_block=42,fixture_block_hex=target.hex(),
                fixture_block_sha256=sha(target),fixture_stored_bytes=len(target),fixture_logical_end=len(logical),fixture_storage_tail_bytes=len(target)-len(logical),
                original_opening_prelude_hex=prelude.hex(),original_opening_prelude_commands=initializers,constant_shift_bytes=delta,
                all_original_exchange_commands=objects,original_text_records=membership,all_fixture_commands=parsed,source_relative_sites=relative,
                no_original_speech_branch_resource_effect_orend_omitted=True,all_relative_operands_unchanged_under_constant34byte_shift=True,
                all_other_ROM_bytes_recoverable_by_exact_opening_archive_inverse=True,initialized_original_Hodram_opening_not_original_event_location_oractivation=True,
                no_conditions_RNG_party_roster_funds_orresults_forced=True,conditional_text_membership_to_be_measured=True))
    assert len(planned)==12 and sum(len(f['all_original_exchange_commands']) for f in fixtures)==298
    ROOT.mkdir(parents=True)
    for path,payload in planned:path.write_bytes(payload); assert sha(path.read_bytes())==sha(payload)
    pins=Path('translations/rom_retention_pins.json'); before=pins.read_bytes(); values=json.loads(before)
    assert all(Path(v['path']).resolve() not in {p.resolve() for p,_ in planned} for v in values)
    added=[dict(path=str(p.resolve()),reason='Hodram complete clean/revised B54/B56/B57/B58/B59/B60 with original eight opening initializers. Disclosed scene fixture; no forced runtime state or natural activation claim. Preserve every ROM. SHA256 '+sha(b)) for p,b in planned]
    updated=values+added; encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    (ROOT/'pins.before.json').write_bytes(before); assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert json.loads(pins.read_bytes())==updated and updated[:-12]==values
    save(ROOT/'twelve_whole_scripts.json',dict(fixtures=fixtures,
        paired_clean_Japanese_andrevised_English_whole_scripts_withcurrent_registered_names_UI=True,
        original8_initializer_commands34bytes_preserved=True,each_complete_selected_exchange_source_speeches_allrelatives_queries_opaquecontrols_andnormalend_preserved=True,
        no_savestate_RAM_eventflag_role_roster_money_seed_condition_orresult_forcing=True,
        actual_selected_path_body_name_pagination_FE_scene_controls_transitions_returns_pending=True,
        registered_current_V8778_mainV4701_unchanged=True,new_credit=0,new_ROMs=12,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [REFERENCE,MAP,CALLERS,Path(__file__)]}))
    print('Pinned12 representative source/English fixtures:6complete blocks/298exchange commands;original8initializers34bytes;B55offline-only fornow.No forced path,roster,progress,credit orrelease.')
