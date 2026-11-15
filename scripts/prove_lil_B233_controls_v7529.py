"""Check source/current A000 and every normal-end seed pair without assigning item effects."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B233_controls_v7529');SOURCE=Path('work/analysis/lil_B233_source_v7526/eleven_clean_current_chisel_library_fragment_tools_joke_source_references.json');SEEDED=Path('work/analysis/lil_B212_seeded_ends_v6634/150_native_terminal_seed_cases_normal_residual_and_flagged_zero.json')
if __name__=='__main__':
    assert not ROOT.exists();p=read(SOURCE);spec=p['blocks'][0];assert p['source_relative_sites']==p['source_typed_commands']==p['source_C200']==p['source_630B']==0 and p['source_A000']==1
    adapter=read(SEEDED)['source_owned_adapter'];env=dict(end_case.__globals__);exec(compile(adapter,__file__+'::source-normal-end','exec'),env);structural=[];ends=[];leaves=[]
    for label,path,key in [('clean-Japanese','work/clean.nds','all_clean_native_commands'),('current-English',p['current_ROM'],'all_current_native_commands')]:
        im=NdsImage.open(path);arm=im.read_file('/__arm9__.bin');block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[233];commands=spec[key]
        assert len(block)==964 and 8+struct.unpack_from('<H',block,4)[0]==962 and block[958:]==bytes(6) and len(commands)==13
        other=[c for c in commands if c['word']!=0x4000];assert [(c['offset'],c['whole_command_hex'],c['native_extent']) for c in other]==[(950,'00a0ffff61000110',8),(958,'00000000',4)];leaves.append(dict(version=label,non_speech_commands=other))
        c=other[0];raw=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;r=walk(arm,isolated);assert r['error'] is None and r['stopped_offset']==r['logical_end']==len(isolated) and len(r['rows'])==1 and r['rows'][0]['word']==0xA000 and r['rows'][0]['native_extent']==8;structural.append(dict(version=label,original_offset=950,word=0xA000,source_command_hex=raw.hex(),**r))
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for seed in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,**env['end_case'](arm,block,958,previous,seed)))
    a,b=structural;assert a['rows']==b['rows'] and a['opaque_effect_bridges']==b['opaque_effect_bridges'] and a['source_command_hex']==b['source_command_hex']
    assert len(ends)==50 and all(not e['flagged_terminal'] and e['native_result'][0]==0 and e['native_result'][1]==e['initial_value_word'] for e in ends)
    ROOT.mkdir(parents=True);save(ROOT/'two_source_A000_structural50_normal_end_cases.json',dict(candidate=p['current_ROM'],candidate_sha256=p['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_A000_structural_cases=structural,source_current_two_exact_non_speech_leaves=leaves,normal_terminal_seed_cases=ends,normal_state0_retains_seeded_value_in_all50_cases=True,source_stored964_logical962_tail2_complete_end958_preserved=True,opaque_A000_effect_bodies_bridged_not_fully_explained=True,no_confirmed_chisel_power_repair_mechanic_discovery_ownership_location_or_gameplay_result_inferred=True,source_owned_seeded_end_adapter=adapter,no_gameplay_result_role_roster_funds_RNG_or_event_flags_forced=True,new_emulator_runs=0,new_credit=0,evidence={str(x):sha(x.read_bytes()) for x in [SOURCE,SEEDED,Path(__file__)]},full_goal_complete=False));print('B233:two exact source/current A000 structural cases and50 seeded normal ends pass. Original964-byte storage/logical962/tail2 remains;opaque effects andnatural activation unproved;zero credit.')
