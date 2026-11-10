"""Bind the original6329/A000 extents and normal seeded terminal with its two-byte tail."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B217_controls_v6834');SOURCE=Path('work/analysis/lil_B217_source_v6831/four_clean_current_Avalon_tavern_exchange_source_references.json');SEEDED=Path('work/analysis/lil_B212_seeded_ends_v6634/150_native_terminal_seed_cases_normal_residual_and_flagged_zero.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);spec=packet['blocks'][0];assert packet['source_relative_sites']==packet['source_typed_commands']==0 and packet['source_A000']==1;adapter=read(SEEDED)['source_owned_adapter'];env=dict(end_case.__globals__);exec(compile(adapter,__file__+'::original-seeded-end','exec'),env);structural=[];ends=[]
    for label,path,key in [('clean-source','work/clean.nds','all_clean_native_commands'),('current',packet['current_ROM'],'all_current_native_commands')]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[217];commands=spec[key];assert len(block)==304 and 8+struct.unpack_from('<H',block,4)[0]==302 and block[298:]==bytes(6) and len(commands)==7 and {c['word'] for c in commands}=={0x6329,0x4000,0xA000,0}
        for command in commands:
            if command['word'] not in [0x6329,0xA000]:continue
            assert (command['offset'],command['whole_command_hex'],command['native_extent']) in [(8,'2963',2),(290,'00a0ffff2f000110',8)];raw=bytes.fromhex(command['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;result=walk(arm,isolated);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['word']==command['word'] and result['rows'][0]['native_extent']==command['native_extent'];structural.append(dict(version=label,original_offset=command['offset'],word=command['word'],source_command_hex=raw.hex(),**result))
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for seed in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,**env['end_case'](arm,block,298,previous,seed)))
    assert len(structural)==4 and len(ends)==50 and all(not r['flagged_terminal'] and r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends)
    for a,b in zip(structural[:2],structural[2:],strict=True):assert a['source_command_hex']==b['source_command_hex'] and a['rows']==b['rows'] and a['opaque_effect_bridges']==b['opaque_effect_bridges']
    ROOT.mkdir(parents=True);save(ROOT/'four6329_A000_structural_cases50_normal_seeded_ends.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source6329_A000_structural_cases=structural,normal_terminal_seed_cases=ends,normal_state0_retains_seeded_value_in_all50_cases=True,source_owned_seeded_end_adapter=adapter,original_end298_full4bytes_and_tail2_preserved=True,no_relative_predicate_typed_choice_style_letter_or_picture_commands=True,opaque6329_A000_effect_bodies_bridged_not_fully_explained=True,no_forced_gameplay_RNG_roster_roles_or_results=True,new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,SEEDED,Path(__file__)]},full_goal_complete=False));print('Four source/current6329/A000 structural cases and50 normal seeded ends pass;no branches/predicate. Actual effects remain separate.')
