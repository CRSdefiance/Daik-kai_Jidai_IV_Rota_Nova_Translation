"""Create paired previous/proposed English fixtures with the same original B22 initialization."""
import json,os,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_scene_fixtures_v7844')
MAP=Path('work/analysis/retrospective_B218_relocation_v7839b/all13_bound_one_changed_wrap15_commands_complete_clean_predecessor_inverse.json')
REF=Path('work/analysis/retrospective_B218_reference_v7841/research_image_receipt.json')
LOAD=Path('work/analysis/retrospective_B218_loader_v7842/whole_SC2_336_loads_cache_hits672_original_parent_modes.json')
CENSUS=Path('work/analysis/retrospective_B218_caller_census_v7843/all15_commands_original_entry_andbounded_shipped_callers.json')
PRELUDE=Path('work/analysis/lil_B218_source_fixture_v6884/complete_B218_source_B22_fixture.json')
if __name__=='__main__':
    assert not ROOT.exists()
    mapping,ref,load,callers,prelude_proof=map(read,[MAP,REF,LOAD,CENSUS,PRELUDE])
    assert load['all336_native_loads_cache_hits_and672_modes_pass'] and callers['only_original24070_interpreter_call_andno_literal_alias']
    parent_path=Path(ref['parent']);parent=NdsImage.open(parent_path)
    assert sha(parent_path.read_bytes())==ref['parent_sha256']==mapping['candidate_sha256']
    bank=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks;inventory,_,_=scoped_inventory();arm=parent.read_file('/__arm9__.bin')
    original,_=inventory(arm,bank[22]);first=next(c['offset'] for c in original if c['word']==0x4000)
    prelude=bank[22][8:first]
    assert first==56 and len(original[:9])==9 and prelude.hex()==prelude_proof['fixtures'][0]['original_B22_prelude_hex']
    oldbank=bank[218];newbank=Path(mapping['target_block']).read_bytes()
    paths={case:Path(f'out/Lil_B218_wrap_{case}_v7844_RESEARCH_ONLY.nds') for case in ['previous_English','proposed_English']}
    for p in paths.values():assert not p.exists()
    runners=[]
    for case in paths:
        changes={
            'work/analysis/lil_B218_English_fixture_v6900/complete_B218_English_B22_fixture.json':str(ROOT/f'{case}_fixture.json').replace('\\','/'),
            "selected['case']=='reviewed_English'":f"selected['case']=='{case}'",
            'work/analysis/lil_B218_English_run_v6901':f'work/analysis/retrospective_B218_scene_runs_v7845/{case}',
            'work/emulation_v193/lil_B218_English_v6901':f'work/emulation_v193/Lil_B218_wrap_{case}_v7845',
        }
        target=f'scripts/run_retrospective_B218_{case}_v7845.py';assert not Path(target).exists()
        checked_text(Path('scripts/run_lil_B218_English_v6901.py').read_text(encoding='utf-8'),changes)
        runners.append(('scripts/run_lil_B218_English_v6901.py',target,changes))
    ROOT.mkdir(parents=True);fixtures=[]
    for case,block in [('previous_English',oldbank),('proposed_English',newbank)]:
        end=8+struct.unpack_from('<H',block,4)[0]
        assert len(block)-end in [0,2] and block[end:]==bytes(len(block)-end)
        logical=bytearray(bank[22][:8]+prelude+block[8:end]);struct.pack_into('<H',logical,4,len(logical)-8)
        target=bytes(logical)+bytes(-len(logical)%4);commands,speeches=inventory(arm,target);native,ns=inventory(arm,block)
        assert len(native)==15 and len(ns)==13 and len(commands)==24 and len(speeches)==13
        assert [c['word'] for c in commands]==[c['word'] for c in original[:9]]+[c['word'] for c in native]
        objects=[];texts=[]
        for command,native_speech in zip(native,commands[9:],strict=True):
            at=command['offset']+first-8
            assert native_speech['offset']==at and native_speech['whole_command_hex']==command['whole_command_hex']
            row=next((r for r in mapping['groups'][0]['text_records']
                if (r['old_offset'] if case=='previous_English' else r['new_offset'])-5==command['offset']),None)
            ident=None if row is None else row['id']
            objects.append(dict(source_block=218,block_command_offset=command['offset'],fixture_offset=at,
                native_extent=command['native_extent'],source_word=command['word'],whole_command_hex=command['whole_command_hex'],text_ID=ident))
            if row is not None:texts.append(dict(id=ident,source_block=218,fixture_command_offset=at,source_selector=row['source_selector'],
                native_extent=command['native_extent'],whole_command_hex=command['whole_command_hex']))
        assert len(texts)==13
        blocks=list(bank);blocks[22]=target;image=NdsImage.open(parent_path)
        image.replace_file('/data/SC2.DK4',IlnkContainer(blocks).to_bytes());image.save(paths[case])
        saved=NdsImage.open(paths[case]);after=IlnkContainer.parse(saved.read_file('/data/SC2.DK4')).blocks
        assert [i for i,(a,b) in enumerate(zip(bank,after,strict=True)) if a!=b]==[22]
        assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4']
        assert all(saved.read_file(p)==v for p,v in parent.iter_components())
        fixture=dict(case=case,source_block=218,research_ROM=str(paths[case]),research_ROM_sha256=sha(paths[case].read_bytes()),
            fixture_block=22,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),
            original_B22_prelude_hex=prelude.hex(),original_B22_prelude_commands=original[:9],
            selected_original_objects=objects,original_text_records=texts,explicitly_excluded_original_commands=[],
            all24_stored_fixture_commands=commands)
        fixtures.append(fixture)
        save(ROOT/f'{case}_fixture.json',dict(parent=str(parent_path),parent_sha256=ref['parent_sha256'],fixtures=[fixture],
            all15_original_commands_plus9_original_initializers=True,
            conditions_roster_roles_funds_RNG_results_RAM_battery_andsavestate_unforced=True,
            initialized_Amsterdam_B22_not_natural_B218_activation_orlocation=True,
            new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    before_pins=Path('translations/rom_retention_pins.json').read_bytes();pins=json.loads(before_pins)
    assert all(Path(v['path']).resolve() not in [p.resolve() for p in paths.values()] for v in pins)
    for f in fixtures:pins.append(dict(path=str(Path(f['research_ROM']).resolve()),
        reason=f"Paired B218 retrospective wrap {f['case']};13speeches/all24 original fixture commands,no runtime forcing. Preserve all ROMs. SHA256 {f['research_ROM_sha256']}"))
    encoded=(json.dumps(pins,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
    (ROOT/'pins.before.json').write_bytes(before_pins);pinpath=Path('translations/rom_retention_pins.json');assert pinpath.read_bytes()==before_pins
    with pinpath.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    derived=[derive(*job) for job in runners]
    save(ROOT/'paired_previous_proposed_fixtures_andrunners.json',dict(parent=str(parent_path),parent_sha256=ref['parent_sha256'],
        fixtures=fixtures,runners=derived,all13_previous_proposed_speech_commands_andoriginal_initializers_retained=True,
        only_original_B22_replaced_in_both_fixtures=True,all335_other_blocks_files_components_andname_assets_preserved=True,
        previous_andproposed_English_only_no_new_clean_Japanese_capture=True,
        paired_actual_capture_validation_transition_timing_andlate_state_review_pending=True,
        all_existing_pins_andROMs_preserved=True,pins_before_sha256=sha(before_pins),pins_after_sha256=sha(encoded),
        new_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [MAP,REF,LOAD,CENSUS,PRELUDE,Path(__file__)]},full_goal_complete=False))
    print('Paired previous/proposed B218 fixtures pinned:13speeches/all24 original commands each,same9 initializers,onlyB22changed.No runtime forcing;two ordinary-input runners ready.')
