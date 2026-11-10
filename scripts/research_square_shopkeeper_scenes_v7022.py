"""Prepare whole-exchange controls for static82 and staged85 nameplate behavior."""
import json,os,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/square_shopkeeper_scenes_v7022')
RECEIPT=Path('work/analysis/square_shopkeeper_data_v7018/research_image_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists();r=read(RECEIPT);proof=read('work/analysis/square_shopkeeper_names_v7021/all_name_field_voice_dynamic_macro_and_complete_native_label_consumers.json')
    assert proof['all414_parent_and414_target_getters_pass'] and proof['all621_parent_and621_target_field_consumers_pass']
    images={label:NdsImage.open(r[key]) for label,key in [('parent','parent'),('target','research_ROM')]}
    for label,key in [('parent','parent'),('target','research_ROM')]:assert sha(Path(r[key]).read_bytes())==r[key+'_sha256']
    inventory,_,_=scoped_inventory();source=images['parent'];arm=source.read_file('/__arm9__.bin')
    blocks=IlnkContainer.parse(source.read_file('/data/SC2.DK4')).blocks
    assert source.read_file('/data/SC2.DK4')==images['target'].read_file('/data/SC2.DK4')
    init,_=inventory(arm,blocks[22]);first=next(c['offset'] for c in init if c['word']==0x4000)
    assert first==56 and len(init[:9])==9;prelude=blocks[22][8:first];fixtures=[];outputs=[]
    for scene,number,actor,expected_commands,expected_speeches in [('static',189,82,20,17),('staged',221,85,21,14)]:
        body=blocks[number];native,speeches=inventory(arm,body);end=8+struct.unpack_from('<H',body,4)[0]
        assert len(native)==expected_commands and len(speeches)==expected_speeches and native[-1]['word']==0 and native[-1]['offset']+4==end
        assert end==len(body) and actor in {body[s['offset']+5] for s in speeches}
        logical=bytearray(blocks[22][:8]+prelude+body[8:end]);struct.pack_into('<H',logical,4,len(logical)-8)
        payload=bytes(logical)+bytes(-len(logical)%4);commands,selected=inventory(arm,payload)
        assert len(commands)==expected_commands+9 and len(selected)==expected_speeches
        mapped=[];texts=[]
        for command in native:
            at=command['offset']+first-8;other=next(c for c in commands if c['offset']==at)
            assert other['word']==command['word'] and other['whole_command_hex']==command['whole_command_hex'] and other['native_extent']==command['native_extent']
            assert other['ancestor_0100_offsets']==[a+first-8 for a in command['ancestor_0100_offsets']]
            ident=None
            if command['word']==0x4000:
                p=command['offset']+5;value=body[p:body.index(0,p+1)];ident=f'NAME_REVIEW_SC2_B{number}_C{command["offset"]}'
                texts.append(dict(id=ident,source_block=number,source_record_index=body[:p].count(b'\0'),source_selector=value[0],current_text_hex=value.hex(),
                    fixture_command_offset=at,native_extent=command['native_extent'],whole_command_hex=command['whole_command_hex']))
            mapped.append(dict(source_block=number,source_offset=command['offset'],source_word=command['word'],fixture_offset=at,native_extent=command['native_extent'],whole_command_hex=command['whole_command_hex'],text_ID=ident))
        if scene=='staged':
            previous=read('work/analysis/lil_B221_English_fixture_v7001/complete_B221_English_B22_fixture.json')['fixtures'][0]
            assert payload.hex()==previous['fixture_block_hex']
        for label in ['parent','target']:
            case=scene+'_'+label;out=Path(f'out/square_shopkeeper_{case}_v7022_RESEARCH_ONLY.nds');assert not out.exists()
            original=images[label];bank=list(blocks);bank[22]=payload;image=NdsImage.open(r['parent'] if label=='parent' else r['research_ROM'])
            image.replace_file('/data/SC2.DK4',IlnkContainer(bank).to_bytes());image.save(out);saved=NdsImage.open(out)
            assert [p for _,p,v in original.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4']
            assert all(saved.read_file(p)==v for p,v in original.iter_components())
            check=IlnkContainer.parse(saved.read_file('/data/SC2.DK4')).blocks
            assert [i for i,(a,b) in enumerate(zip(blocks,check,strict=True)) if a!=b]==[22]
            fixtures.append(dict(case=case,scene=scene,version=label,source_block=number,target_actor=actor,research_ROM=str(out),research_ROM_sha256=sha(out.read_bytes()),
                original_source_speech_count=expected_speeches,original_source_command_count=expected_commands,source_block_hex=body.hex(),source_block_sha256=sha(body),
                fixture_block=22,fixture_block_hex=payload.hex(),fixture_block_sha256=sha(payload),original_B22_prelude_hex=prelude.hex(),original_B22_prelude_commands=init[:9],
                selected_original_objects=mapped,original_text_records=texts,all_stored_fixture_commands=commands,explicitly_excluded_original_commands=[],
                no_source_prose_or_name_credit=True,complete_preexisting_prose_not_newly_editorially_approved=True,initialized_fixture_not_natural_activation_original_location_earned_progress_full_effects_or_route=True))
            outputs.append(out)
    ROOT.mkdir(parents=True)
    save(ROOT/'four_complete_static_staged_nameplate_fixtures.json',dict(parent=r['parent'],parent_sha256=r['parent_sha256'],target=r['research_ROM'],target_sha256=r['research_ROM_sha256'],fixtures=fixtures,
        all_current_source_words_controls_initializers_choices_relative_spans_and_end_bytes_preserved=True,no_RAM_roster_RNG_funds_roles_conditions_results_or_savestate_forced=True,
        four_fixtures_not_registered_release_parents=True,not_every_conditional_nameplate_or_catalogue_UI_visit=True,
        B189_existing_early_line_breaks_remain_separate_retrospective_editorial_queue=True,new_name_or_dialogue_credit=0,full_goal_complete=False))
    pins=Path('translations/rom_retention_pins.json');raw=pins.read_bytes();values=json.loads(raw)
    added=[dict(path=str(p.resolve()),reason='Complete static82/staged85 Shopkeeper parent/target nameplate fixture;all scene words preserved. Preserve every ROM. SHA256 '+sha(p.read_bytes())) for p in outputs]
    assert all(not any(Path(v['path']).resolve()==p.resolve() for v in values) for p in outputs)
    encoded=(json.dumps(values+added,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');(ROOT/'pins.before.json').write_bytes(raw)
    assert pins.read_bytes()==raw and json.loads(encoded)[:-4]==values
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'pin_receipt.json',dict(new_pins=added,all_prior_pins_preserved=True,ROMs_deleted=0,before_sha256=sha(raw),after_sha256=sha(encoded),full_goal_complete=False))
    print('Four complete static82/staged85 parent/target fixtures pinned;all controls and prose preserved. Representative ordinary-input runs pending.',flush=True)
