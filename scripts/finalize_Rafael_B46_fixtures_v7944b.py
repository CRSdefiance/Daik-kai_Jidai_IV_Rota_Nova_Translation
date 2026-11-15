"""Recover the missing B46 manifest by exact in-memory ROM/pin reconstruction;never overwrite preserved artifacts."""
import json,os,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.create_Rafael_B46_reference_v7941 import PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_scene_fixtures_v7944')
INITIALIZERS=Path('work/analysis/papal_trade_initializer_binding_v7647/two_actual_opening_preludes18_commands_bound_before_optional_scene_fixture.json')
CURRENT=Path('work/analysis/Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json')
REFERENCES=Path('work/analysis/Rafael_B46_reference_census_v7943/all37_commands_four_relative_sites_two_choices_EV0_entry_shipped_callers.json')
CONTROL=Path('work/analysis/Rafael_B46_relocated_controls_v7940/24_stored_dispatches_two_choices20_relative_cases25_seeded_ends.json')
CURRENT_START=Path('work/analysis/Rafael_B45_context_runs_v7913/route0/run_plan.json')
if __name__=='__main__':
    assert ROOT.exists() and not (ROOT/'two_complete_source_English_original_Rafael_prelude_fixtures.json').exists();init,mapping,current,refs,controls,start=map(read,[INITIALIZERS,PLAN,CURRENT,REFERENCES,CONTROL,CURRENT_START])
    assert sha(PARENT.read_bytes())==mapping['candidate_sha256']==current['current_ROM_sha256']==start['candidate_sha256']
    assert len(controls['final_dispatches'])==24 and len(refs['all_command_maps'])==37
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
    base=Path('work/analysis/papal_trade_route_runs_v7625/route0/ordinary_NewGame_inputs.json')
    assert sha(base.read_bytes())==start['source_inputs_sha256']==start['inputs_sha256']
    outputs=[Path(f'out/Rafael_B46_{v}_v7944_RESEARCH_ONLY.nds') for v in ['clean_Japanese','English']]
    assert all(p.exists() for p in outputs)
    inventory,_,_=scoped_inventory();fixtures=[];assert ROOT.exists()
    g,cg=mapping['groups'][0],current['groups'][0];assert g['block']==cg['block']==46
    for version,out in zip(['clean_Japanese','English'],outputs,strict=True):
        selected=IlnkContainer.parse(clean.read_file(file)).blocks[46] if version=='clean_Japanese' else Path(g['target_block']).read_bytes()
        expected=cg['clean_block_sha256'] if version=='clean_Japanese' else g['target_block_sha256'];assert sha(selected)==expected
        end=8+struct.unpack_from('<H',selected,4)[0];assert selected[end:]==bytes(len(selected)-end)
        assert selected[:4]==original[:4] and selected[6:8]==original[6:8]
        logical=bytearray(original[:8]+prelude+selected[8:end]);struct.pack_into('<H',logical,4,len(logical)-8)
        target=bytes(logical)+bytes(-len(logical)%4);commands,speeches=inventory(parent.read_file('/__arm9__.bin'),target)
        source_commands=cg['all_source_commands'] if version=='clean_Japanese' else g['all_target_commands']
        assert len(commands)==len(source_commands)+10==47 and len(speeches)==len(g['text_records'])==24 and len(target)<0x2400
        assert sum(c['word']==0 for c in commands)==1 and commands[-1]['offset']+4==len(logical)
        objects=[];texts=[]
        for command in source_commands:
            at=command['offset']+delta;actual=next(v for v in commands if v['offset']==at)
            assert actual['word']==command['word'] and actual['native_extent']==command['native_extent'] and actual['whole_command_hex']==command['whole_command_hex']
            assert actual['ancestor_0100_offsets']==[a+delta for a in command['ancestor_0100_offsets']]
            if command['word'] in [0x100,0x200,0x300,0x400]:
                span=struct.unpack_from('<H',selected,command['offset']+2)[0]
                assert struct.unpack_from('<H',target,at+2)[0]==span
                assert at+4+span==command['offset']+4+span+delta
            ref=next((r for r in g['text_records'] if (r['source_reference']['header_offset'] if version=='clean_Japanese' else r['new_offset']-5)==command['offset']),None)
            objects.append(dict(original_block=46,original_command_offset=command['offset'],fixture_command_offset=at,native_extent=command['native_extent'],
                word=command['word'],whole_command_hex=command['whole_command_hex'],text_ID=None if ref is None else ref['id'],
                original_0100_ancestors=command['ancestor_0100_offsets'],fixture_0100_ancestors=actual['ancestor_0100_offsets']))
            if ref is not None:texts.append(dict(id=ref['id'],source_record_index=ref['source_reference']['record_index'],source_selector=ref['source_selector'],
                fixture_command_offset=at,native_extent=command['native_extent'],whole_command_hex=command['whole_command_hex']))
        assert len(texts)==24 and len(objects)==37
        mc=next(c for c in source_commands if c['word']==0x2100);menu_refs=[]
        for r in current['typed_choice_records']:
            i=r['option_index'];menu_base=mc['offset']+6;at=menu_base+struct.unpack_from('<H',selected,mc['offset']+2+2*i)[0]
            label=r['source_Japanese'] if version=='clean_Japanese' else g['choice_commands'][0]['labels'][i]
            value=label.encode('cp932');assert target[at+delta:at+delta+len(value)+1]==value+b'\0'
            menu_refs.append(dict(id=r['id'],option_index=i,fixture_command_offset=mc['offset']+delta,fixture_label_offset=at+delta,
                source_menu_command_offset=mc['offset'],label=label,label_hex=value.hex(),source_reference=r['source_reference']))
        assert len(menu_refs)==2
        image=NdsImage.open(PARENT);blocks=list(bank);blocks[opening]=target;image.replace_file(file,IlnkContainer(blocks).to_bytes());assert image.rom.save()==out.read_bytes()
        saved=NdsImage.open(out);after=IlnkContainer.parse(saved.read_file(file)).blocks
        assert [i for i,(a,b) in enumerate(zip(bank,after,strict=True)) if a!=b]==[44]
        assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==[file] and all(saved.read_file(p)==v for p,v in parent.iter_components())
        fixtures.append(dict(route=0,route_identity='Rafael',version=version,source_block=46,research_ROM=str(out),research_ROM_sha256=sha(out.read_bytes()),
            source_file=file,source_block_sha256=expected,fixture_block=44,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),
            fixture_stored_bytes=len(target),fixture_logical_end=len(logical),fixture_storage_tail_bytes=len(target)-len(logical),
            original_opening_prelude_hex=prelude.hex(),original_opening_prelude_commands=ig['actual_original_prelude_commands'],
            all_original_exchange_commands=objects,original_text_records=texts,original_menu_records=menu_refs,all_fixture_commands=commands,
            no_original_speech_branch_resource_effect_orend_omitted=True,all_four_relative_spans_unchanged_under_constant32_byte_shift=True,
            source_event_not_naturally_selected=True,initialized_opening_entry_not_original_event_location=True))
    pins=Path('translations/rom_retention_pins.json');before=(ROOT/'pins.before.json').read_bytes();values=json.loads(before);oldvalues=list(values)
    for f in fixtures:
        path=Path(f['research_ROM']).resolve();assert all(Path(v['path']).resolve()!=path for v in values)
        values.append(dict(path=str(path),reason=f"Rafael B46 complete {f['version']} 24-speech/37-command exchange/two choices with all four original relative sites behind the source-bound original B44 ten-command prelude. Disclosed ROM entry fixture;not natural B46 activation,original location,registered release,new parent orhandoff. Preserve every ROM. SHA256 "+f['research_ROM_sha256']))
    assert values[:-2]==oldvalues
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');assert pins.read_bytes()==encoded
    save(ROOT/'two_complete_source_English_original_Rafael_prelude_fixtures.json',dict(
        parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),initializer_proof=str(INITIALIZERS),initializer_proof_sha256=sha(INITIALIZERS.read_bytes()),
        relocation_map=str(PLAN),relocation_map_sha256=sha(PLAN.read_bytes()),fixtures=fixtures,
        all24_source_speeches37_commands_two_choices_four_relative_sites_preserved_in_both_languages=True,
        original_prelude_evidence_reused_byexact_whole_B44_ARM9_COMMON_EV0_font_andordinary_start_inputs=True,
        current_prelude_command_execution_not_newly_captured=True,
        no_manual_conditions_roles_roster_funds_RNG_results_battery_save_state_RAM_orcode_forcing=True,
        only_disclosed_opening_ROM_entry_fixture_not_natural_B46_activation_ororiginal_location=True,
        original_two_choice_control_paths_andunconditional_skips_unchanged=True,
        all_other_parent_files_components_andROMs_preserved=True,pins_before_sha256=sha(before),pins_after_sha256=sha(encoded),
        not_registered_candidates_orhandoff_ornew_parents=True,actual_capture_body_header_FE_transition_andreturn_checks_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [INITIALIZERS,PLAN,CURRENT,REFERENCES,CONTROL,CURRENT_START,base,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Two pinned B46 source/English fixtures:24 speeches/37 commands/two choices/four relative sites plusthe exact ten-command B44 prelude. No condition/state forcing ornatural activation claim.')
