"""Bind the actually executed complete Maria B33 initialization, including original A-wait."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.maria_existing_unlock_contract_v7680 import validate_capture
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_initializer_binding_v7702')
TERMINAL=Path('work/analysis/maria_B207_original_initializer_v7701c/route3/terminal.json')
if __name__=='__main__':
    assert not ROOT.exists();t=read(TERMINAL);plan,report=[read(t[k]) for k in ['run_plan','report']]
    assert t['terminal'] and report['frames']==6001 and sha(Path(t['report']).read_bytes())==t['report_sha256'] and t['observer_host_slots_restored'];validate_capture(report)
    rom=Path(plan['candidate']);assert sha(rom.read_bytes())==t['candidate_sha256'];image=NdsImage.open(rom);clean=NdsImage.open('work/clean.nds')
    file='/data/SC3.DK4';block=IlnkContainer.parse(image.read_file(file)).blocks[33];jp=IlnkContainer.parse(clean.read_file(file)).blocks[33]
    inventory,_,_=scoped_inventory();commands,_=inventory(image.read_file('/__arm9__.bin'),block);first=next(i for i,c in enumerate(commands) if c['word']==0x4000);prelude=commands[:first]
    assert first==7 and commands[first]['offset']==34 and block[8:34]==jp[8:34] and block[:4]==jp[:4]==b'CS\1\1'
    assert [(c['offset'],c['word']) for c in prelude]==[(8,0x610F),(10,0x4500),(16,0x514),(18,0xA000),(26,0x4636),(30,0x514),(32,0x2000)]
    op=Path(plan['capture_folder'])/'observer/commands.json';observed=read(op)
    assert not observed['errors'] and observed['mismatches']==0 and observed['all_host_slots_restored_and_core_file_exact']
    entries=[(i,r) for i,r in enumerate(observed['rows']) if r['kind']=='before_command'];assert len(entries)==8 and len(observed['rows'])==15
    rows=[]
    for c,(i,r) in zip(prelude,entries[:-1],strict=True):
        s=r['source'];assert s['classification']=='original_SC_cache' and s['route']==3 and s['block']==33 and s['instruction_offset']==c['offset'] and s['first_word']==c['word']
        assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==s['registered_sha256']==sha(block) and Path(s['actual_payload_file']).read_bytes()==block
        assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
        after=observed['rows'][i+1];assert after['kind']=='after_command' and after['entry_row']==i and after['decoded_length']==c['native_extent'] and after['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
        rows.append(dict(original_command=c,entry_row=i,entry_frame=r['frame'],return_row=i+1,return_frame=after['frame'],result_words=after['result_words'],whole_original_resident_block_exact=True))
    firstspeech=entries[-1][1];assert firstspeech['source']['instruction_offset']==34 and firstspeech['source']['first_word']==0x4000
    wait=rows[-1];assert wait['entry_frame']==3940 and wait['return_frame']>=4200
    group=dict(route=3,route_identity='Maria',file_path=file,original_opening_block=33,original_opening_block_sha256=sha(block),original_prelude_hex=block[8:34].hex(),first_speech_offset=34,actual_original_prelude_commands=rows,first_original_opening_speech_entry_frame=firstspeech['frame'],first_speech_unreturned_at_capture_end=True,observer=str(op),observer_sha256=sha(op.read_bytes()),terminal=str(TERMINAL),terminal_sha256=sha(TERMINAL.read_bytes()),capture_report=t['report'],capture_report_sha256=t['report_sha256'],source_andcurrent_prelude_bytes_exact=True,no_optional_B207_ororiginal_location_ornew_prose_coverage_claim=True)
    ROOT.mkdir(parents=True);save(ROOT/'Maria_actual_B33_prelude7_commands_bound_before_optional_scene_fixture.json',dict(candidate=str(rom),candidate_sha256=sha(rom.read_bytes()),groups=[group],actual_original_initializer_commands=7,all7_entry_return_pairs_original_operands_extents_andresident_bytes_exact=True,ordinary_A4200_returns_original_2000_wait=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,no_savestate_ROM_RAM_roles_roster_funds_RNG_orresult_forcing=True,all_callbacks_readonly_host_slots_restored_andjob_terminal=True,first_original_speech_waiting_not_full_opening_orroute_completion=True,optional_scene_fixture_not_yet_created=True,full_optional_eligibility_activation_location_andmechanics_unproved=True,evidence={str(p):sha(p.read_bytes()) for p in [TERMINAL,Path(t['run_plan']),Path(t['report']),op,Path(__file__)]},new_credit=0,full_goal_complete=False))
    print(dict(original_B33_commands=7,first_speech_offset=34,first_speech_frame=firstspeech['frame'],wait_entry=wait['entry_frame'],wait_return=wait['return_frame'],earned_unlock=False,optional_B207_activation=False))
