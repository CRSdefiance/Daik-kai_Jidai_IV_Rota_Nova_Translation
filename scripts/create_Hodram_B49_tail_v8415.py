"""Bounded original possession-dialogue tail display fixtures;not earned inventory or event activation."""
import json,os,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_tail_v8415')
REFERENCE=Path('work/analysis/Hodram_B49_reference_v8403/research_image_receipt.json')
MAP=Path('work/analysis/Hodram_B49_relocation_v8398/reconstruction.json')
CURRENT=Path('work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json')
DOC=Path('translations/hodram_B49_editorial_manuscript_v2.json')
CALLERS=Path('work/analysis/Hodram_B49_references_v8405b/references.json')

if __name__=='__main__':
    assert not ROOT.exists();reference,mapping,current,doc,callers=map(read,[REFERENCE,MAP,CURRENT,DOC,CALLERS])
    assert callers['external_references_complete'] and mapping['manuscript_sha256']==sha(DOC.read_bytes())
    parentpath=Path(reference['parent']);parent=NdsImage.open(parentpath)
    revisedpath=Path(reference['research_ROM']);revised=NdsImage.open(revisedpath);clean=NdsImage.open('work/clean.nds')
    assert sha(parentpath.read_bytes())==reference['parent_sha256']==doc['current_ROM_sha256']
    assert sha(revisedpath.read_bytes())==reference['research_ROM_sha256']
    assert all(revised.read_file(p)==v for p,v in parent.iter_components())
    arm=parent.read_file('/__arm9__.bin');inventory,_,_=scoped_inventory();file='/data/SC1.DK4'
    bank=IlnkContainer.parse(parent.read_file(file)).blocks;opening=bank[42]
    cleanbank=IlnkContainer.parse(clean.read_file(file)).blocks
    commands,speeches=inventory(arm,opening);first=speeches[0]['offset'];prelude=opening[8:first]
    initializers=[c for c in commands if c['offset']<first]
    assert first==42 and len(prelude)==34 and len(initializers)==8 and prelude==cleanbank[42][8:first]
    group=mapping['groups'][0];cg=current['groups'][0];assert group['block']==cg['block']==49
    global_ordinals={c['offset']:i for i,c in enumerate(cg['all_source_commands'])}
    records=group['text_records'];fixtures=[];planned=[]
    for version in ['clean_Japanese','revised_English']:
        source_version=version=='clean_Japanese'
        selected=cleanbank[49] if source_version else IlnkContainer.parse(revised.read_file(file)).blocks[49]
        expected=cg['clean_block_sha256'] if source_version else group['target_block_sha256']
        assert sha(selected)==expected
        allcommands=cg['all_source_commands'] if source_version else group['all_target_commands']
        start=428 if source_version else 402;outer=424 if source_version else 398
        assert next(c for c in allcommands if c['offset']==start)['word']==0x4000
        entry=selected[8:12];assert [c['word'] for c in allcommands[:2]]==[0x6000,0x633d] and entry==bytes.fromhex('00603d63')
        selected_end=8+struct.unpack_from('<H',selected,4)[0]
        assert selected[selected_end:]==bytes(len(selected)-selected_end)
        logical=bytearray(opening[:8]+prelude+entry+selected[start:selected_end]);struct.pack_into('<H',logical,4,len(logical)-8)
        target=bytes(logical)+bytes(-len(logical)%4);shift=8+len(prelude)+len(entry)-start
        parsed,spoken=inventory(arm,target);chosen=allcommands[:2]+[c for c in allcommands if c['offset']>=start]
        assert len(chosen)==23 and len(parsed)==31 and len(spoken)==8 and len(target)<0x2400
        assert sum(c['word']==0 for c in parsed)==1 and parsed[-1]['offset']+4==len(logical)
        objects=[];membership=[];relative=0;menu_records=[]
        for command in chosen:
            at=command['offset']+34 if command['offset']<12 else command['offset']+shift
            actual=next(c for c in parsed if c['offset']==at)
            canonical=next(m['old_offset'] for m in group['command_map'] if m['new_offset']==command['offset']) if not source_version else command['offset']
            assert actual['word']==command['word'] and actual['native_extent']==command['native_extent'] and actual['whole_command_hex']==command['whole_command_hex']
            ancestors=[a+shift for a in command['ancestor_0100_offsets'] if a!=outer]
            assert actual['ancestor_0100_offsets']==ancestors
            if command['word'] in [0x100,0x200,0x300,0x400]:
                span=struct.unpack_from('<H',selected,command['offset']+2)[0]
                assert at+4+span==command['offset']+4+span+shift
                assert any(c['offset']==at+4+span for c in parsed) or at+4+span==len(logical)
                relative+=1
            record=next((r for r in records if r['source_reference']['header_offset']==canonical),None) if command['word']==0x4000 else None
            objects.append(dict(original_block=49,source_command_ordinal=global_ordinals[canonical],canonical_clean_offset=canonical,original_command_offset=command['offset'],fixture_command_offset=at,native_extent=command['native_extent'],word=command['word'],whole_command_hex=command['whole_command_hex'],text_ID=None if record is None else record['id'],original_0100_ancestors=command['ancestor_0100_offsets'],fixture_0100_ancestors=ancestors))
            if record is not None:
                assert target[at:at+6].hex()==record['source_complete_preamble_hex']
                membership.append(dict(id=record['id'],source_record_index=record['source_reference']['record_index'],source_selector=record['source_selector'],source_reference=record['source_reference'],fixture_command_offset=at,fixture_body_offset=at+5))
            if command['word']==0x2100:
                for row in doc['typed_choice_records']:
                    i=row['option_index'];ref=row['source_reference'] if source_version else group['choice_commands'][0]['label_references'][i]
                    original_at=ref['offset'] if source_version else ref['new_offset'];body=bytes.fromhex(row['source_hex']) if source_version else row['english'].encode('ascii')
                    pos=original_at+shift;assert target[pos:pos+len(body)+1]==body+b'\0'
                    menu_records.append(dict(id=row['id'],option_index=i,label=body.decode('cp932'),label_hex=body.hex(),original_reference=ref,fixture_header_offset=at,fixture_label_offset=pos,fixture_record_index=target[:pos].count(b'\0')))
        assert len(membership)==8 and relative==5 and len(menu_records)==2
        image=NdsImage.open(parentpath);blocks=list(bank);blocks[42]=target;image.replace_file(file,IlnkContainer(blocks).to_bytes())
        assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==[file] and all(image.read_file(p)==v for p,v in parent.iter_components())
        updated=IlnkContainer.parse(image.read_file(file)).blocks
        assert [i for i,(a,b) in enumerate(zip(bank,updated,strict=True)) if a!=b]==[42]
        payload=bytes(image.rom.save());image.replace_file(file,parent.read_file(file));assert bytes(image.rom.save())==parentpath.read_bytes()
        out=Path(f'out/Hodram_B49_tail_{version}_v8415_RESEARCH_ONLY.nds');assert not out.exists();planned.append((out,payload))
        fixtures.append(dict(route=1,route_identity='Hodram',version=version,source_block=49,research_ROM=str(out),research_ROM_sha256=sha(payload),parent=str(parentpath),parent_sha256=reference['parent_sha256'],source_file=file,source_block_sha256=expected,source_text_ROM=str(Path('work/clean.nds') if source_version else revisedpath),fixture_block=42,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),fixture_stored_bytes=len(target),fixture_logical_end=len(logical),fixture_storage_tail_bytes=len(target)-len(logical),original_opening_prelude_hex=prelude.hex(),original_opening_prelude_commands=initializers,original_B49_entry_commands=allcommands[:2],bounded_original_tail_start=start,canonical_clean_tail_start=428,omitted_outer_skip_command=outer,constant_tail_shift_bytes=shift,all_original_exchange_commands=objects,original_text_records=membership,original_menu_records=menu_records,all_fixture_commands=parsed,source_relative_sites=relative,no_selected_tail_speech_choice_branch_effect_picture_hide_orend_omitted=True,all_five_internal_relative_operands_unchanged=True,all_other_ROM_bytes_recoverable_by_exact_opening_inverse=True,bounded_original_possession_dialogue_tail_display_fixture=True,not_whole_B49_activation_orproof_of_possession_trade_eligibility_earned_progress_ororiginal_location=True,no_runtime_RAM_inventory_flags_RNG_roles_funds_orresults_forced=True))
    ROOT.mkdir(parents=True)
    for out,payload in planned:out.write_bytes(payload);assert sha(out.read_bytes())==sha(payload)
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before)
    assert all(Path(v['path']).resolve() not in {p.resolve() for p,_ in planned} for v in values)
    updated=values+[dict(path=str(p.resolve()),reason='B49 bounded original possession-dialogue tail display fixture afteroriginalHodram initialization;8speeches/2choices/5relatives/FE/item148layout0. Not earned inventory/eligibility orwholeeventactivation. Preserve every ROM. SHA256 '+sha(b)) for p,b in planned]
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');(ROOT/'pins.before.json').write_bytes(before)
    assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert json.loads(pins.read_bytes())==updated and updated[:-2]==values
    save(ROOT/'bounded_tail_fixtures.json',dict(fixtures=fixtures,parent=str(parentpath),parent_sha256=reference['parent_sha256'],original8_opening_initializers34bytes_andtwo_original_B49_entry_commands_preserved=True,each_fixture23_selected_source_commands8_speeches5_relatives2_typed_labels_one_FE_one_layout0_hide_andterminal=True,omitted_prefix_andouter_skip_explicit_not_whole_script_coverage=True,no_savestate_battery_RAM_inventory_quest_flags_RNG_roles_funds_orresult_forcing=True,controller_choice_return_andbacking_FE_mixed_ellipsis_transition_checks_pending=True,new_ROMs=2,new_credit=0,new_emulator_runs=0,registered_current_V8377_mainV4701_unchanged=True,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [REFERENCE,MAP,CURRENT,DOC,CALLERS,Path(__file__)]}))
    print('Pinned two bounded B49 tail display fixtures:8speeches/2choices/5originalrelatives/FE/item148layout0;8opening+2sceneinitializers.No runtime forcing,natural activation orcredit.')
