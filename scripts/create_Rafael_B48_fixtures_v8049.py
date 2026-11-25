"""Preserve all48 B47 commands behind the source-bound original ten-command Rafael prelude."""
import json,os,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.create_Rafael_B48_reference_v8046 import PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_scene_fixtures_v8049')
INITIALIZERS=Path('work/analysis/papal_trade_initializer_binding_v7647/two_actual_opening_preludes18_commands_bound_before_optional_scene_fixture.json')
CURRENT=Path('work/analysis/Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json')
REFERENCES=Path('work/analysis/Rafael_B48_reference_census_v8048/all163_commands28_relative_sites91_speeches4_FE_EV0_entry_shipped_callers.json')
CONTROL=Path('work/analysis/Rafael_B48_relocated_controls_v8043/91_stored_dispatches5_raw_predicates2_queries140_relative_cases25_seeded_ends.json')
CURRENT_START=Path('work/analysis/Rafael_B47_context_runs_v8015/route0/run_plan.json')
if __name__=='__main__':
    assert not ROOT.exists()
    init,mapping,current,refs,controls,start=map(read,[INITIALIZERS,PLAN,CURRENT,REFERENCES,CONTROL,CURRENT_START])
    assert sha(PARENT.read_bytes())==mapping['candidate_sha256']==current['current_ROM_sha256']==start['candidate_sha256']
    assert len(controls['final_dispatches'])==91 and len(refs['all_command_maps'])==163
    old,parent,clean=[NdsImage.open(p) for p in [init['candidate'],PARENT,'work/clean.nds']]
    assert sha(Path(init['candidate']).read_bytes())==init['candidate_sha256']
    exact_fields=['/__arm9__.bin','/COMMON/MESFILE.DK4','/data/EV0.DK4','/GRP/KANJI.FNT']
    assert all(old.read_file(p)==parent.read_file(p) for p in exact_fields)
    ig=next(r for r in init['groups'] if r['route']==0);file=ig['file_path'];opening=ig['original_opening_block']
    assert file=='/data/SC0.DK4' and opening==44
    bank=IlnkContainer.parse(parent.read_file(file)).blocks;original=bank[opening]
    assert original==IlnkContainer.parse(old.read_file(file)).blocks[opening] and sha(original)==ig['original_opening_block_sha256']
    prelude=bytes.fromhex(ig['original_prelude_hex']);delta=len(prelude)
    assert original[8:ig['first_speech_offset']]==prelude and delta==32 and len(ig['actual_original_prelude_commands'])==10
    for key in ['observer','terminal','capture_report']:assert sha(Path(ig[key]).read_bytes())==ig[key+'_sha256']
    ordinary_inputs_path=Path('work/analysis/papal_trade_route_runs_v7625/route0/ordinary_NewGame_inputs.json')
    assert sha(ordinary_inputs_path.read_bytes())==start['source_inputs_sha256']==start['inputs_sha256']
    outputs=[Path(f'out/Rafael_B48_{v}_v8049_RESEARCH_ONLY.nds') for v in ['clean_Japanese','English']]
    assert all(not p.exists() for p in outputs)
    inventory,_,_=scoped_inventory();fixtures=[];planned=[]
    g,cg=mapping['groups'][0],current['groups'][0];assert g['block']==cg['block']==48
    for version,out in zip(['clean_Japanese','English'],outputs,strict=True):
        selected=IlnkContainer.parse(clean.read_file(file)).blocks[48] if version=='clean_Japanese' else Path(g['target_block']).read_bytes()
        expected=cg['clean_block_sha256'] if version=='clean_Japanese' else g['target_block_sha256'];assert sha(selected)==expected
        end=8+struct.unpack_from('<H',selected,4)[0];assert selected[end:]==bytes(len(selected)-end)
        assert selected[:4]==original[:4] and selected[6:8]==original[6:8]
        logical=bytearray(original[:8]+prelude+selected[8:end]);struct.pack_into('<H',logical,4,len(logical)-8)
        target=bytes(logical)+bytes(-len(logical)%4);commands,speeches=inventory(parent.read_file('/__arm9__.bin'),target)
        source_commands=cg['all_source_commands'] if version=='clean_Japanese' else g['all_target_commands']
        assert len(commands)==len(source_commands)+10==173 and len(speeches)==len(g['text_records'])==91 and len(target)<0x2400
        assert sum(c['word']==0 for c in commands)==1 and commands[-1]['offset']+4==len(logical)
        objects=[];texts=[];relative_count=0
        for command in source_commands:
            at=command['offset']+delta;actual=next(v for v in commands if v['offset']==at)
            assert actual['word']==command['word'] and actual['native_extent']==command['native_extent'] and actual['whole_command_hex']==command['whole_command_hex']
            assert actual['ancestor_0100_offsets']==[a+delta for a in command['ancestor_0100_offsets']]
            if command['word'] in [0x100,0x200,0x300,0x400]:
                span=struct.unpack_from('<H',selected,command['offset']+2)[0]
                assert struct.unpack_from('<H',target,at+2)[0]==span and at+4+span==command['offset']+4+span+delta
                relative_count+=1
            ref=next((r for r in g['text_records'] if (r['source_reference']['header_offset'] if version=='clean_Japanese' else r['new_offset']-5)==command['offset']),None)
            objects.append(dict(original_block=48,original_command_offset=command['offset'],fixture_command_offset=at,native_extent=command['native_extent'],
                word=command['word'],whole_command_hex=command['whole_command_hex'],text_ID=None if ref is None else ref['id'],
                original_0100_ancestors=command['ancestor_0100_offsets'],fixture_0100_ancestors=actual['ancestor_0100_offsets']))
            if ref is not None:
                texts.append(dict(id=ref['id'],source_record_index=ref['source_reference']['record_index'],source_selector=ref['source_selector'],
                    fixture_command_offset=at,fixture_body_offset=at+5,source_reference=ref['source_reference']))
        assert len(objects)==163 and len(texts)==91 and relative_count==28
        image=NdsImage.open(PARENT);blocks=list(bank);blocks[opening]=target;image.replace_file(file,IlnkContainer(blocks).to_bytes())
        payload=bytes(image.rom.save())
        assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==[file] and all(image.read_file(p)==v for p,v in parent.iter_components())
        after=IlnkContainer.parse(image.read_file(file)).blocks
        assert [i for i,(a,b) in enumerate(zip(bank,after,strict=True)) if a!=b]==[44]
        planned.append((out,payload))
        fixtures.append(dict(route=0,route_identity='Rafael',version=version,source_block=48,research_ROM=str(out),research_ROM_sha256=sha(payload),
            source_file=file,source_block_sha256=expected,fixture_block=44,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),
            fixture_stored_bytes=len(target),fixture_logical_end=len(logical),fixture_storage_tail_bytes=len(target)-len(logical),
            original_opening_prelude_hex=prelude.hex(),original_opening_prelude_commands=ig['actual_original_prelude_commands'],
            all_original_exchange_commands=objects,original_text_records=texts,all_fixture_commands=commands,
            no_original_speech_branch_resource_effect_orend_omitted=True,all28_relative_spans_unchanged_under_constant32_byte_shift=True,
            source_event_not_naturally_selected=True,initialized_opening_entry_not_original_event_location=True))
    ROOT.mkdir(parents=True)
    for path,payload in planned:
        assert not path.exists();path.write_bytes(payload);assert sha(path.read_bytes())==sha(payload)
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before);oldvalues=list(values)
    for f in fixtures:
        path=Path(f['research_ROM']).resolve();assert all(Path(v['path']).resolve()!=path for v in values)
        values.append(dict(path=str(path),reason=f"Rafael B48 complete {f['version']} 91-speech/163-command exchange with all28 relative sites,five raw predicates,two completion queries,four FEpanels andall scene/effect commands behind the exact B44 ten-command prelude. Disclosed ROM entry fixture;not natural B48 activation,original location,registered release,new parent orhandoff. Preserve every ROM. SHA256 "+f['research_ROM_sha256']))
    assert values[:-2]==oldvalues
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');(ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'two_complete_source_English_original_Rafael_prelude_fixtures.json',dict(
        parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),initializer_proof=str(INITIALIZERS),initializer_proof_sha256=sha(INITIALIZERS.read_bytes()),
        relocation_map=str(PLAN),relocation_map_sha256=sha(PLAN.read_bytes()),fixtures=fixtures,
        all91_source_speeches163_commands28_relatives_five_raw_predicates_two_queries_fourFE_andall_effects_preserved=True,
        original_prelude_evidence_reused_byexact_whole_B44_ARM9_COMMON_EV0_font_andordinary_start_inputs=True,
        current_prelude_command_execution_not_newly_captured=True,
        no_manual_conditions_roles_roster_funds_RNG_results_battery_save_state_RAM_orcode_forcing=True,
        only_disclosed_opening_ROM_entry_fixture_not_natural_B48_activation_ororiginal_location=True,
        all_other_parent_files_components_andROMs_preserved=True,pins_before_sha256=sha(before),pins_after_sha256=sha(encoded),
        not_registered_candidates_orhandoff_ornew_parents=True,actual_body_headers_R347_page_turn_fourFE_joining_transitions_andreturn_checks_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [INITIALIZERS,PLAN,CURRENT,REFERENCES,CONTROL,CURRENT_START,ordinary_inputs_path,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Two pinned complete B48 fixtures:91speeches/163commands/28relatives/5rawpredicates/2queries/fourFE/all scene effects plusoriginal10-command B44prelude.No state forcing.')
