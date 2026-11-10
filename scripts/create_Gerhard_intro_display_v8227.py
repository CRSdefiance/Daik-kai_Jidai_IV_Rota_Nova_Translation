"""Focused original eight-speech B27 introduction display; not a full conditional scene or natural event."""
import json,os,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_intro_display_fixtures_v8227')
WHOLE=Path('work/analysis/Gerhard_scene_fixtures_v8224/four_complete_parent_revised_SC2_scripts_original_Lil_prelude_fixtures.json')
CURRENT=Path('work/analysis/Gerhard_surname_five_v8199/five_prior_completed_source_current_refs_andwhole295_source_context_receipt.json')
MAP=Path('work/analysis/Gerhard_sparse_relocation_v8208b/two_blocks_five_sparse_revisions_all_commands_native_relative_cases_full_predecessor_inverse.json')
CENSUS=Path('work/analysis/Gerhard_surname_consumers_v8196/all20_current_Latin_occurrences_five_whole_clean_exchanges.json')
if __name__=='__main__':
    assert not ROOT.exists();whole,current,mapping,census=map(read,[WHOLE,CURRENT,MAP,CENSUS])
    spec=next(g for g in current['groups'] if g['block']==27);mapped=next(g for g in mapping['groups'] if g['block']==27)
    canonical=next(g for g in census['groups'] if g['file_path']=='/data/SC2.DK4' and g['block']==27)
    source_records={r['source_reference']['header_offset']:r for r in canonical['complete_clean_source_records']}
    selected_ids=['DK4_MES_B27_R0091','DK4_MES_B27_R0094'];selected=[r for r in current['records'] if r['id'] in selected_ids]
    assert len(selected)==2 and selected[0]['current_0100_ancestors']==selected[1]['current_0100_ancestors'] and len(selected[0]['current_0100_ancestors'])==1
    old_outer=selected[0]['current_0100_ancestors'][0]
    inventory,_,_=scoped_inventory();fixtures=[];planned=[]
    for version in ['parent_English','revised_English']:
        original_fixture=next(f for f in whole['fixtures'] if f['source_block']==27 and f['version']==version)
        parentpath=Path(original_fixture['parent']);assert sha(parentpath.read_bytes())==original_fixture['parent_sha256']
        parent=NdsImage.open(parentpath);file=original_fixture['source_file'];bank=IlnkContainer.parse(parent.read_file(file)).blocks;opening=bank[22];block=bank[27]
        assert sha(block)==original_fixture['source_block_sha256']
        commands=spec['all_current_commands'] if version=='parent_English' else mapped['all_target_commands']
        outer_offset=old_outer if version=='parent_English' else next(m['new_offset'] for m in mapped['command_map'] if m['old_offset']==old_outer)
        outer=next(c for c in commands if c['offset']==outer_offset);assert outer['word']==0x100
        begin,end=outer_offset+4,outer_offset+outer['native_extent'];slice_commands=[(i,c) for i,c in enumerate(commands) if begin<=c['offset']<end]
        assert len(slice_commands)==9 and sum(c['word']==0x4000 for _,c in slice_commands)==8
        assert slice_commands[-1][1]['word']==0x100 and slice_commands[-1][1]['whole_command_hex']=='00010000'
        assert all(c['word'] in [0x4000,0x100] for _,c in slice_commands)
        prelude=bytes.fromhex(original_fixture['original_opening_prelude_hex']);assert len(prelude)==48 and opening[8:56]==prelude
        terminal=commands[-1];assert terminal['word']==0 and terminal['native_extent']==4
        logical=bytearray(opening[:8]+prelude+block[begin:end]+block[terminal['offset']:terminal['offset']+4]);struct.pack_into('<H',logical,4,len(logical)-8)
        target=bytes(logical)+bytes(-len(logical)%4);decoded,speeches=inventory(parent.read_file('/__arm9__.bin'),target)
        assert len(decoded)==19 and len(speeches)==8 and decoded[-1]['word']==0 and decoded[-1]['offset']+4==len(logical)
        objects=[];texts=[]
        for ordinal,command in slice_commands:
            at=56+command['offset']-begin;actual=next(c for c in decoded if c['offset']==at)
            assert actual['whole_command_hex']==command['whole_command_hex'] and actual['native_extent']==command['native_extent']
            assert actual['ancestor_0100_offsets']==[] and command['ancestor_0100_offsets']==[outer_offset]
            source=spec['all_source_commands'][ordinal];record=source_records.get(source['offset']) if command['word']==0x4000 else None
            objects.append(dict(original_block=27,source_command_ordinal=ordinal,canonical_clean_offset=source['offset'],original_command_offset=command['offset'],
                fixture_command_offset=at,native_extent=command['native_extent'],word=command['word'],whole_command_hex=command['whole_command_hex'],
                text_ID=None if record is None else record['id'],original_0100_ancestors=command['ancestor_0100_offsets'],fixture_0100_ancestors=[]))
            if record is not None:texts.append(dict(id=record['id'],source_record_index=record['source_record_index'],source_selector=record['source_selector'],fixture_command_offset=at,
                fixture_body_offset=at+5,source_reference=record['source_reference'],corrected_surname_body=record['id'] in selected_ids))
        last=decoded[-1];objects.append(dict(original_block=27,source_command_ordinal=len(commands)-1,canonical_clean_offset=spec['all_source_commands'][-1]['offset'],
            original_command_offset=terminal['offset'],fixture_command_offset=last['offset'],native_extent=4,word=0,whole_command_hex='00000000',text_ID=None,
            original_0100_ancestors=[],fixture_0100_ancestors=[]))
        assert len(objects)==10 and len(texts)==8 and sum(r['corrected_surname_body'] for r in texts)==2
        image=NdsImage.open(parentpath);blocks=list(bank);blocks[22]=target;image.replace_file(file,IlnkContainer(blocks).to_bytes())
        assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==[file] and all(image.read_file(p)==v for p,v in parent.iter_components())
        payload=bytes(image.rom.save());out=Path(f'out/Gerhard_B27_intro_{version}_v8227_RESEARCH_ONLY.nds');assert not out.exists();planned.append((out,payload))
        fixtures.append(dict(route=2,route_identity='Lil',version=version,source_block=27,research_ROM=str(out),research_ROM_sha256=sha(payload),parent=str(parentpath),parent_sha256=original_fixture['parent_sha256'],
            source_file=file,source_block_sha256=sha(block),fixture_block=22,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),fixture_stored_bytes=len(target),
            fixture_logical_end=len(logical),fixture_storage_tail_bytes=len(target)-len(logical),original_opening_prelude_hex=prelude.hex(),
            original_opening_prelude_commands=original_fixture['original_opening_prelude_commands'],all_original_exchange_commands=objects,original_text_records=texts,all_fixture_commands=decoded,
            selected_source_outer_0100_offset=outer_offset,selected_original_body_slice=dict(begin=begin,end=end,hex=block[begin:end].hex()),
            fixture_kind='focused-eight-speech-introduction-display-only',all8_original_speech_commands_andclosing_zero_skip_preserved=True,
            original_full_B27_conditions_andremaining_effects_NOT_executed_bythis_display_fixture=True,
            outer_branch_selection_bypassed_by_standalone_ROM_display_fixture=True,no_runtime_predicate_result_orstory_flag_forced=True,
            not_full_B27_controlflow_ororiginal_location_natural_activation_earned_progress_orfullroute=True))
    ROOT.mkdir(parents=True)
    for path,payload in planned:path.write_bytes(payload);assert sha(path.read_bytes())==sha(payload)
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before);assert all(Path(v['path']).resolve() not in {p.resolve() for p,_ in planned} for v in values)
    updated=values+[dict(path=str(p.resolve()),reason='Focused B27 eight-speech introduction display with source-original commands and Lil prelude;outerbranch notexecuted,notfullscene/naturalactivation/registeredhandoff. Preserve every ROM. SHA256 '+sha(b)) for p,b in planned]
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');(ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert json.loads(pins.read_bytes())==updated and updated[:-2]==values
    save(ROOT/'two_focused_parent_revised_eight_speech_intro_display_fixtures.json',dict(fixtures=fixtures,
        actual_full_B27_run_selected35_speeches_andnormal_return_butskipped_Gerhard_intro=True,
        additional_test_only_for_complete_surname_body_andnameplate_display_risk=True,
        all_production_conditions_andfull_research_reference_preserved_separately=True,
        source_context295_speeches_separate_from_focused_actual_display_scope=True,
        full_scene_membership_eligibility_conditional_effects_NOT_proved_byfocused_slice=True,
        no_actor_party_roster_funds_RNG_eventflag_orpredicate_return_RAM_forcing=True,
        new_ROMs=2,new_emulator_runs=0,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [WHOLE,CURRENT,MAP,CENSUS,Path(__file__)]}))
    print('Pinned2 focused introduction display fixtures:8unaltered original speeches+closing skip+normal end;outercondition explicitly unexecuted.No fullscene claim.')
