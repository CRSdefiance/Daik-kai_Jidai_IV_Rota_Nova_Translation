"""Six full source/English fixtures behind Maria's exact previously observed original prelude."""
import json,os,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.maria_existing_unlock_contract_v7680 import HISTORICAL,validate_fixture
from scripts.create_Maria_confrontation_reference_v7805 import PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_scene_fixtures_v7808')
INITIALIZERS=Path('work/analysis/maria_B207_initializer_binding_v7702/Maria_actual_B33_prelude7_commands_bound_before_optional_scene_fixture.json')
CURRENT=Path('work/analysis/maria_confrontation_current_v7789/all16_complete_source_current_refs_before_new_English_manuscript.json')
REFERENCES=Path('work/analysis/maria_confrontation_reference_census_v7807/all22_commands_original_B36_entry_no_relative_sites_shipped_callers.json')
CONTROL=Path('work/analysis/maria_confrontation_controls_v7804/16_final_dispatches_six_numeric_leaves_623D_resources_setup_ends.json')
if __name__=='__main__':
    assert not ROOT.exists();init,mapping,current,refs,controls=map(read,[INITIALIZERS,PLAN,CURRENT,REFERENCES,CONTROL])
    assert sha(PARENT.read_bytes())==mapping['candidate_sha256']==current['current_ROM_sha256']
    assert len(controls['final_dispatches'])==16 and len(refs['groups'])==1
    old,parent,clean=[NdsImage.open(p) for p in [init['candidate'],PARENT,'work/clean.nds']]
    assert sha(Path(init['candidate']).read_bytes())==init['candidate_sha256']
    for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/data/EV3.DK4','/GRP/KANJI.FNT']:
        assert old.read_file(p)==parent.read_file(p)
    ig=init['groups'][0];file=ig['file_path'];opening=ig['original_opening_block'];assert opening==33 and ig['route']==3
    bank=IlnkContainer.parse(parent.read_file(file)).blocks;original=bank[opening]
    assert original==IlnkContainer.parse(old.read_file(file)).blocks[opening] and sha(original)==ig['original_opening_block_sha256']
    prelude=bytes.fromhex(ig['original_prelude_hex']);delta=len(prelude)
    assert original[8:ig['first_speech_offset']]==prelude and delta==26 and len(ig['actual_original_prelude_commands'])==7
    outputs=[Path(f'out/Maria_story_B{g["block"]}_{v}_v7808_RESEARCH_ONLY.nds') for g in mapping['groups'] for v in ['clean_Japanese','English']]
    assert all(not p.exists() for p in outputs)
    inventory,_,_=scoped_inventory();fixtures=[];ROOT.mkdir(parents=True)
    for g,cg in zip(mapping['groups'],current['groups'],strict=True):
        assert g['block']==cg['block'];number=g['block'];cleanbank=IlnkContainer.parse(clean.read_file(file)).blocks
        for version in ['clean_Japanese','English']:
            selected=cleanbank[number] if version=='clean_Japanese' else Path(g['target_block']).read_bytes()
            expected=cg['clean_block_sha256'] if version=='clean_Japanese' else g['target_block_sha256'];assert sha(selected)==expected
            end=8+struct.unpack_from('<H',selected,4)[0];assert selected[end:]==bytes(len(selected)-end)
            assert selected[:4]==original[:4] and selected[6:8]==original[6:8]
            logical=bytearray(original[:8]+prelude+selected[8:end]);struct.pack_into('<H',logical,4,len(logical)-8)
            target=bytes(logical)+bytes(-len(logical)%4);commands,speeches=inventory(parent.read_file('/__arm9__.bin'),target)
            source_commands=cg['all_source_commands'] if version=='clean_Japanese' else g['all_target_commands']
            assert len(commands)==len(source_commands)+7 and len(speeches)==len(g['text_records']) and len(target)<0x2400
            assert sum(c['word']==0 for c in commands)==1 and commands[-1]['offset']+4==len(logical)
            objects=[];texts=[]
            for command in source_commands:
                at=command['offset']+delta;actual=next(v for v in commands if v['offset']==at)
                assert actual['word']==command['word'] and actual['native_extent']==command['native_extent'] and actual['whole_command_hex']==command['whole_command_hex']
                assert actual['ancestor_0100_offsets']==[a+delta for a in command['ancestor_0100_offsets']]
                ref=next((r for r in g['text_records'] if (r['source_reference']['header_offset'] if version=='clean_Japanese' else r['new_offset']-5)==command['offset']),None)
                objects.append(dict(original_block=number,original_command_offset=command['offset'],fixture_command_offset=at,native_extent=command['native_extent'],
                    word=command['word'],whole_command_hex=command['whole_command_hex'],text_ID=None if ref is None else ref['id'],
                    original_0100_ancestors=command['ancestor_0100_offsets'],fixture_0100_ancestors=actual['ancestor_0100_offsets']))
                if ref is not None:texts.append(dict(id=ref['id'],source_record_index=ref['source_reference']['record_index'],source_selector=ref['source_selector'],
                    fixture_command_offset=at,native_extent=command['native_extent'],whole_command_hex=command['whole_command_hex']))
            assert len(texts)==len(g['text_records'])
            out=Path(f'out/Maria_story_B{number}_{version}_v7808_RESEARCH_ONLY.nds');image=NdsImage.open(PARENT);blocks=list(bank);blocks[opening]=target
            image.replace_file(file,IlnkContainer(blocks).to_bytes());image.save(out);saved=NdsImage.open(out);after=IlnkContainer.parse(saved.read_file(file)).blocks
            assert [i for i,(a,b) in enumerate(zip(bank,after,strict=True)) if a!=b]==[opening]
            assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==[file] and all(saved.read_file(p)==v for p,v in parent.iter_components())
            fp=ROOT/f'existing_system_unlock_B{number}_{version}.json';unlock=read(HISTORICAL)
            unlock.update(production_ROM=str(out),production_ROM_sha256=sha(out.read_bytes()),current_test_scope=f'Complete Maria B{number} initialized {version} scene;system-only unlock not earned.')
            save(fp,unlock);validate_fixture(fp)
            fixtures.append(dict(route=3,route_identity='Maria',version=version,source_block=number,research_ROM=str(out),research_ROM_sha256=sha(out.read_bytes()),
                source_file=file,source_block_sha256=expected,fixture_block=opening,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),
                fixture_stored_bytes=len(target),fixture_logical_end=len(logical),fixture_storage_tail_bytes=len(target)-len(logical),
                original_opening_prelude_hex=prelude.hex(),original_opening_prelude_commands=ig['actual_original_prelude_commands'],
                all_original_exchange_commands=objects,original_text_records=texts,all_fixture_commands=commands,
                existing_system_unlock_manifest=str(fp),existing_system_unlock_manifest_sha256=sha(fp.read_bytes()),earned_unlock_verified=False,
                no_original_speech_branch_effect_pause_orend_omitted=True,all_relative_spans_unchanged_under_constant_prelude_shift=True,
                original_prelude_actual_evidence_reused_byexact_whole_B33_ARM9_COMMON_EV3_font_not_new_V7717_initializer_capture=True,
                source_event_not_naturally_selected=True,initialized_opening_background_not_original_optional_event_location=True))
            print('FIXTURE',number,version,len(commands),'commands',len(texts),'speeches',flush=True)
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before);oldvalues=list(values)
    for f in fixtures:
        path=Path(f['research_ROM']).resolve();assert all(Path(v['path']).resolve()!=path for v in values)
        values.append(dict(path=str(path),reason=f'Maria B{f["source_block"]} complete {f["version"]} original-prelude focused scene fixture. Exact seven original B33 setup commands andall exchange controls,branches,speeches andend preserved. Existing system-only unlock isnot earned. Not natural activation,original optional location,registered release,new parent orhandoff. Preserve every ROM. SHA256 '+f['research_ROM_sha256']))
    assert values[:-2]==oldvalues
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');(ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'two_complete_source_English_original_prelude_fixtures.json',dict(
        parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),original_initializer_binding=str(INITIALIZERS),original_initializer_binding_sha256=sha(INITIALIZERS.read_bytes()),
        fixtures=fixtures,exact_historical_original_B33_prelude_reuse_not_fresh_initializer_playthrough=True,
        current_andprior_whole_B33_ARM9_COMMON_EV3_andfont_equal=True,one_complete_exchange16_positions_preserved_in_both_languages=True,
        all_original_relative_spans_andancestor_maps_preserved_under26byte_shift=True,
        no_savestate_historical_RAM_runtime_patch_oractor_role_roster_funds_RNG_conditions_orresults_forced=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,not_natural_optional_activation_original_location_orfull_route_coverage=True,
        all_other_parent_files_components_andROMs_preserved=True,pins_before_sha256=sha(before),pins_after_sha256=sha(encoded),
        unregistered_research_fixtures_not_handoff_ornew_parents=True,actual_body_header_palette_page_button_transition_return_andlate_state_checks_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [INITIALIZERS,PLAN,CURRENT,REFERENCES,CONTROL,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Two pinned full source/English original-prelude fixtures ready. No new actual gameplay claim until captures complete.')
