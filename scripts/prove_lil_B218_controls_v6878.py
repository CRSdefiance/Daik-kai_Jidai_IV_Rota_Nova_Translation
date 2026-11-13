"""Bind the sole A000 command and normal terminal without inventing predicates or branches."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B218_controls_v6878');SOURCE=Path('work/analysis/lil_B218_source_v6875/thirteen_clean_current_Ares_legend_exchange_source_references.json');SEEDED=Path('work/analysis/lil_B212_seeded_ends_v6634/150_native_terminal_seed_cases_normal_residual_and_flagged_zero.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);spec=packet['blocks'][0];assert packet['source_relative_sites']==packet['source_typed_commands']==0 and packet['source_A000']==1
    adapter=read(SEEDED)['source_owned_adapter'];env=dict(end_case.__globals__);exec(compile(adapter,__file__+'::source-owned-end','exec'),env);structural=[];ends=[]
    for label,path,key in [('clean-source','work/clean.nds','all_clean_native_commands'),('current',packet['current_ROM'],'all_current_native_commands')]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[218];commands=spec[key];assert len(block)==1088 and 8+struct.unpack_from('<H',block,4)[0]==1088 and block[1084:]==bytes(4) and len(commands)==15 and {c['word'] for c in commands}=={0x4000,0xA000,0}
        command=next(c for c in commands if c['word']==0xA000);assert command['offset']==1076 and command['whole_command_hex']=='00a0ffff2e000110' and command['native_extent']==8
        raw=bytes.fromhex(command['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;result=walk(arm,isolated);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['word']==0xA000 and result['rows'][0]['native_extent']==8;structural.append(dict(version=label,original_offset=1076,source_command_hex=raw.hex(),**result))
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for seed in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,**env['end_case'](arm,block,1084,previous,seed)))
    assert len(structural)==2 and structural[0]['rows']==structural[1]['rows'] and structural[0]['opaque_effect_bridges']==structural[1]['opaque_effect_bridges'] and len(ends)==50 and all(not e['flagged_terminal'] and e['native_result'][0]==0 and e['native_result'][1]==e['initial_value_word'] for e in ends)
    ROOT.mkdir(parents=True);save(ROOT/'two_A000_structural_cases50_normal_seeded_ends_no_relative_or_predicate.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_A000_structural_cases=structural,normal_terminal_seed_cases=ends,normal_state0_retains_seeded_value_word_in_all50_cases=True,original_end1084_full4bytes_and_no_tail_preserved=True,no_relative_predicate_typed_choice_style_letter_or_picture_commands=True,opaque_A000_body_bridged_not_fully_explained_or_actual_effect_claim=True,source_owned_seeded_end_adapter=adapter,no_gameplay_result_role_roster_funds_RNG_or_event_flags_forced=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,SEEDED,Path(__file__)]},full_goal_complete=False));print('Two source/current A000 structural cases and50 normal-end seed cases pass. No branches,predicates or typed controls. Full effects/actual gameplay separate.')
