"""Preserve full source/English exchanges behind the actually observed Maria opening prelude."""
import json,os,struct
from pathlib import Path
from scripts.maria_existing_unlock_contract_v7680 import HISTORICAL,validate_fixture
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.create_Maria_B207_reference_v7698 import PARENT,PLAN
from scripts.draft_Maria_B207_prose_v7687 import CURRENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_scene_fixtures_v7704')
INITIALIZERS=Path('work/analysis/maria_B207_initializer_binding_v7702/Maria_actual_B33_prelude7_commands_bound_before_optional_scene_fixture.json')
REFERENCES=Path('work/analysis/maria_B207_reference_census_v7700/Maria_all20_commands_one_entry_one_fresh_shipped_caller_census.json')
CONTROL=Path('work/analysis/maria_B207_relocated_controls_v7703/Maria18_final_dispatches_two_effect_reuses25_relocated_seeded_ends.json')
if __name__=='__main__':
    assert not ROOT.exists();init,mapping,current,refs,controls=map(read,[INITIALIZERS,PLAN,CURRENT,REFERENCES,CONTROL])
    assert init['candidate_sha256']==mapping['candidate_sha256']==sha(PARENT.read_bytes()) and len(controls['dispatch_cases'])==18
    parent=NdsImage.open(PARENT);clean=NdsImage.open('work/clean.nds');inventory,_,_=scoped_inventory();fixtures=[]
    outputs=[Path(f'out/Maria_B207_route{route}_{version}_v7704_RESEARCH_ONLY.nds') for route in [3] for version in ['clean_Japanese','English']]
    assert all(not p.exists() for p in outputs);ROOT.mkdir(parents=True)
    for ig,g,cg,rg in zip(init['groups'],mapping['groups'],[current],refs['groups'],strict=True):
        route=g['route'];file=g['file_path'];opening=ig['original_opening_block'];bank=IlnkContainer.parse(parent.read_file(file)).blocks
        original=bank[opening];prelude=bytes.fromhex(ig['original_prelude_hex']);delta=len(prelude)
        assert sha(original)==ig['original_opening_block_sha256'] and original[8:ig['first_speech_offset']]==prelude
        assert delta==ig['first_speech_offset']-8 and len(ig['actual_original_prelude_commands'])=={3:7}[route]
        for version in ['clean_Japanese','English']:
            selected=IlnkContainer.parse(clean.read_file(file)).blocks[g['block']] if version=='clean_Japanese' else Path(g['research_block']).read_bytes()
            expected=cg['clean_block_sha256'] if version=='clean_Japanese' else g['research_block_sha256'];assert sha(selected)==expected
            end=8+struct.unpack_from('<H',selected,4)[0];assert end=={ 'clean_Japanese':1468,'English':1470}[version] and selected[end:]==(b'' if version=='clean_Japanese' else bytes(2))
            assert selected[:4]==original[:4] and selected[6:8]==original[6:8]
            logical=bytearray(original[:8]+prelude+selected[8:end]);struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
            native,speeches=inventory(parent.read_file('/__arm9__.bin'),target)
            assert len(native)==20+len(ig['actual_original_prelude_commands']) and len(speeches)==18 and len(target)<=0x2400
            assert sum(c['word']==0 for c in native)==1 and native[-1]['word']==0 and native[-1]['offset']+4==len(logical)
            source_commands=rg['native_walks']['clean' if version=='clean_Japanese' else 'research'];objects=[];texts=[]
            for command in source_commands:
                at=command['offset']+delta;actual=next(v for v in native if v['offset']==at)
                assert actual['word']==command['word'] and actual['whole_command_hex']==command['whole_command_hex'] and actual['native_extent']==command['native_extent'] and actual['ancestor_0100_offsets']==[]
                record=next((r for r in g['text_records'] if (r['source_reference']['header_offset'] if version=='clean_Japanese' else r['new_offset']-5)==command['offset']),None)
                objects.append(dict(original_block=g['block'],original_command_offset=command['offset'],fixture_command_offset=at,native_extent=command['native_extent'],word=command['word'],whole_command_hex=command['whole_command_hex'],text_ID=None if record is None else record['id']))
                if record is not None:texts.append(dict(id=record['id'],source_record_index=record['source_reference']['record_index'],source_selector=record['source_selector'],fixture_command_offset=at,native_extent=command['native_extent'],whole_command_hex=command['whole_command_hex']))
            assert len(objects)==20 and len(texts)==18
            out=Path(f'out/Maria_B207_route{route}_{version}_v7704_RESEARCH_ONLY.nds')
            blocks=list(bank);blocks[opening]=target;image=NdsImage.open(PARENT);image.replace_file(file,IlnkContainer(blocks).to_bytes());image.save(out)
            saved=NdsImage.open(out);after=IlnkContainer.parse(saved.read_file(file)).blocks
            assert [i for i,(a,b) in enumerate(zip(bank,after,strict=True)) if a!=b]==[opening]
            assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==[file] and all(saved.read_file(p)==v for p,v in parent.iter_components())
            fp=ROOT/('existing_system_unlock_'+version+'.json');unlock=read(HISTORICAL);unlock.update(production_ROM=str(out),production_ROM_sha256=sha(out.read_bytes()),current_test_scope='Complete Maria B207 initialized source/English scene;system-only unlock not earned.');save(fp,unlock);validate_fixture(fp)
            fixtures.append(dict(existing_system_unlock_manifest=str(fp),existing_system_unlock_manifest_sha256=sha(fp.read_bytes()),earned_unlock_verified=False,route=route,route_identity=g['route_identity'],version=version,research_ROM=str(out),research_ROM_sha256=sha(out.read_bytes()),source_file=file,source_block=g['block'],source_block_sha256=expected,fixture_block=opening,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),fixture_stored_bytes=len(target),fixture_logical_end=len(logical),fixture_storage_tail_bytes=len(target)-len(logical),original_opening_prelude_hex=prelude.hex(),original_opening_prelude_commands=ig['actual_original_prelude_commands'],all_original_exchange_commands=objects,original_text_records=texts,all_fixture_commands=native,no_original_exchange_command_omitted=True,source_event_not_naturally_selected=True,initialized_opening_background_not_original_optional_event_location=True))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before)
    for f in fixtures:
        out=Path(f['research_ROM']);assert not any(Path(v['path']).resolve()==out.resolve() for v in values)
        values.append(dict(path=str(out.resolve()),reason=f"Complete {f['route_identity']} {f['source_file']} B{f['source_block']} {f['version']}18-speech/20-command exchange behind its actually observed original opening prelude. Disclosed ROM fixture, not natural optional event, registered release ornew parent. Preserve every ROM. SHA256 "+f['research_ROM_sha256']))
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');(ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'Maria_two_complete_source_English_original_prelude_fixtures.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),initializer_proof=str(INITIALIZERS),initializer_proof_sha256=sha(INITIALIZERS.read_bytes()),relocation_map=str(PLAN),relocation_map_sha256=sha(PLAN.read_bytes()),fixtures=fixtures,both_complete18_speech20_command_exchanges_preserved=True,only_original_actually_observed_seven_command_Maria_prelude_added=True,existing_system_only_unlock_fixture_not_earned=True,no_manual_source_conditions_roles_roster_funds_RNG_results_savestate_orRAM_forcing=True,only_disclosed_opening_ROM_entry_fixture_not_natural_optional_activation=True,not_original_optional_location_orfull_route_coverage=True,all_other_parent_files_components_andROMs_preserved=True,pins_before_sha256=sha(before),pins_after_sha256=sha(encoded),not_registered_candidates_orhandoff_ornew_parents=True,actual_capture_body_header_palette_transition_andreturn_checks_pending=True,evidence={str(p):sha(p.read_bytes()) for p in [INITIALIZERS,PLAN,CURRENT,REFERENCES,CONTROL,Path(__file__)]},new_credit=0,full_goal_complete=False))
    print('Two pinned Maria source/English fixtures preserve all18 speeches/20 commands plusthe actual original seven-command prelude,including the A-wait. No natural optional activation/location orrelease claim.')
