"""Preserve complete Maria CS0101; reuse exact isolated effects and test its normal end."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_controls_v7686')
SOURCE=Path('work/analysis/maria_B207_current_v7670/all18_complete_Maria_clean_current_refs_CS0101_before_new_prose.json')
PRIOR=Path('work/analysis/lil_B234_controls_v7577/two_source_A000_structural50_normal_end_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,prior=map(read,[SOURCE,PRIOR]);old,current,clean=[NdsImage.open(p) for p in [prior['candidate'],packet['current_ROM'],'work/clean.nds']]
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256'] and sha(Path(packet['current_ROM']).read_bytes())==packet['current_ROM_sha256']
    assert old.read_file('/__arm9__.bin')==current.read_file('/__arm9__.bin')
    blocks=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks[207] for im in [clean,current]]
    commands=[packet['all_clean_native_commands'],packet['all_current_native_commands']]
    for block,cmd in zip(blocks,commands,strict=True):
        assert block[:8].hex()=='43530101b4050000' and len(block)==1468 and 8+int.from_bytes(block[4:6],'little')==1468
        assert [(c['offset'],c['whole_command_hex'],c['native_extent']) for c in cmd if c['word']!=0x4000]==[(1456,'00a0ffff6a000110',8),(1464,'00000000',4)]
    adapter=prior['source_owned_seeded_end_adapter'];env=dict(end_case.__globals__);exec(compile(adapter,__file__+'::source-normal-end','exec'),env)
    cases=[]
    for label,block in zip(['clean-Japanese','current-English'],blocks,strict=True):
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for seed in [0,1,2,3,0xFFFFFFFF]:
                case=env['end_case'](current.read_file('/__arm9__.bin'),block,1464,previous,seed)
                assert not case['flagged_terminal'] and case['native_result']==[0,case['initial_value_word']]
                cases.append(dict(version=label,**case))
    effects=deepcopy(prior['source_A000_structural_cases']);assert len(effects)==2
    for case in effects:assert case['source_command_hex']=='00a0ffff6a000110' and case['error'] is None and case['logical_end']==case['stopped_offset']==16
    ROOT.mkdir(parents=True);save(ROOT/'Maria_CS0101_50_fresh_seeded_ends_two_exact_isolated_effect_reuses.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),prior_effect_proof=str(PRIOR),prior_effect_proof_sha256=sha(PRIOR.read_bytes()),source_owned_seeded_end_adapter=adapter,normal_terminal_seed_cases=cases,fresh_normal_terminal_seed_cases=50,two_exact_isolated_A000_structural_cases=effects,whole_header_CS0101_preserved=True,source_current1468_logical1468_tail0_complete_four_byte_end1464=True,isolated_effect_reuse_exact_eight_bytes_andwhole_ARM9_not_full_block_reuse=True,no_full_item_blessing_ownership_location_reward_orordinary_event_activation_claim=True,new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,PRIOR,Path(__file__)]},full_goal_complete=False))
    print('Maria CS0101 clean/current:50 fresh seeded normal ends;two isolated exact A000 proofs reused.No full effects claim.')
