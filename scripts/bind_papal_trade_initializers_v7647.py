"""Bind18 actually executed original opening commands, separately from optional activation."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_initializer_binding_v7647')
if __name__=='__main__':
    assert not ROOT.exists();groups=[];inventory,_,_=scoped_inventory();clean=NdsImage.open('work/clean.nds')
    for route,n,expected_first,expected_count in [(0,44,40,10),(1,42,42,8)]:
        terminal=Path(f'work/analysis/papal_trade_original_initializers_v7646/route{route}/terminal.json');t=read(terminal);plan=read(t['run_plan']);report=read(t['report'])
        assert t['terminal'] and report['frames']==4001 and sha(Path(t['report']).read_bytes())==t['report_sha256'] and t['observer_host_slots_restored']
        rom=Path(plan['candidate']);assert sha(rom.read_bytes())==t['candidate_sha256'];image=NdsImage.open(rom);file=f'/data/SC{route}.DK4';block=IlnkContainer.parse(image.read_file(file)).blocks[n]
        commands,_=inventory(image.read_file('/__arm9__.bin'),block);first=next(i for i,c in enumerate(commands) if c['word']==0x4000);prelude=commands[:first]
        assert first==expected_count and commands[first]['offset']==expected_first and commands[first]['word']==0x4000
        jp=IlnkContainer.parse(clean.read_file(file)).blocks[n];assert jp[8:expected_first]==block[8:expected_first]
        op=Path(plan['capture_folder'])/'observer/commands.json';observed=read(op)
        assert not observed['errors'] and observed['mismatches']==0 and observed['all_host_slots_restored_and_core_file_exact']
        entries=[(i,r) for i,r in enumerate(observed['rows']) if r['kind']=='before_command']
        assert len(entries)==expected_count+1 and len(observed['rows'])==2*expected_count+1
        rows=[]
        for c,(i,r) in zip(prelude,entries[:-1],strict=True):
            s=r['source'];assert s['classification']=='original_SC_cache' and s['route']==route and s['block']==n and s['instruction_offset']==c['offset'] and s['first_word']==c['word']
            assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==s['registered_sha256']==sha(block)
            assert Path(s['actual_payload_file']).read_bytes()==block and r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            after=observed['rows'][i+1];assert after['kind']=='after_command' and after['entry_row']==i and after['decoded_length']==c['native_extent']
            assert after['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            rows.append(dict(original_command=c,entry_row=i,entry_frame=r['frame'],return_row=i+1,return_frame=after['frame'],result_words=after['result_words'],whole_original_resident_block_exact=True))
        first_speech=entries[-1][1];assert first_speech['source']['instruction_offset']==expected_first and first_speech['source']['first_word']==0x4000
        groups.append(dict(route=route,route_identity={0:'Rafael',1:'Hodram'}[route],file_path=file,original_opening_block=n,original_opening_block_sha256=sha(block),original_prelude_hex=block[8:expected_first].hex(),first_speech_offset=expected_first,actual_original_prelude_commands=rows,first_original_opening_speech_entry_frame=first_speech['frame'],first_speech_unreturned_at_capture_end=True,observer=str(op),observer_sha256=sha(op.read_bytes()),terminal=str(terminal),terminal_sha256=sha(terminal.read_bytes()),capture_report=t['report'],capture_report_sha256=t['report_sha256'],source_andcurrent_prelude_bytes_exact=True,no_optional_papal_scene_orlocation_ornew_prose_coverage_claim=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'two_actual_opening_preludes18_commands_bound_before_optional_scene_fixture.json',dict(candidate=str(rom),candidate_sha256=sha(rom.read_bytes()),groups=groups,actual_original_initializer_commands=18,all18_entry_return_pairs_original_operands_extents_andresident_bytes_exact=True,ordinary_NewGame_no_save_savestate_ROM_RAM_roles_roster_funds_RNG_orresult_forcing=True,all_callbacks_readonly_host_slots_restored_andjobs_terminal=True,first_original_opening_speeches_waiting_not_full_opening_orroute_completion=True,optional_scene_fixture_not_yet_created=True,full_optional_eligibility_activation_location_andmechanics_unproved=True,evidence={g['terminal']:g['terminal_sha256'] for g in groups},producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Actual ordinary NewGames bind Rafael B44 ten-command prelude/first speech3256 andHodram B42 eight-command prelude/first speech2816. No optional encounter activation ornew editorial credit.')
