"""Bind B179's opaque A000 and single tail end;no C200 is invented or executed."""
import inspect
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B179_controls_v4714')
SOURCE=Path('work/analysis/lil_B179_source_v4708/all14_clean_current_complete_context.json')
BRANCH=Path('work/analysis/lil_B179_branches_v4711/original_relative_skip_operand_proof.json')

if __name__=='__main__':
    assert not ROOT.exists()
    packet,branch=read(SOURCE),read(BRANCH);group=packet['blocks'][0]
    images=[NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[179] for im in images]
    commands=group['all_current_native_commands']
    assert len(commands)==16 and sum(c['word']==0x4000 for c in commands)==14
    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x8100,0x2100,0x4100,0x2000,0xC200] for c in commands)
    assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and not branch['cases'] and not branch['operands_requiring_adjustment_when_resizing']
    leaves=[]
    for a,b in zip(group['all_clean_native_commands'],commands,strict=True):
        if a['word']==0x4000:continue
        assert a['offset']==b['offset'] and a['whole_command_hex']==b['whole_command_hex']
        leaves.append(dict(block=179,offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_current_hex=a['whole_command_hex']))
    assert [(r['offset'],r['source_current_hex']) for r in leaves]==[(8,'00a0ffff01221da1'),(508,'00000000')]
    assert all(len(b)==8+struct.unpack_from('<H',b,4)[0]==512 for b in blocks)
    raw=bytes.fromhex(leaves[0]['source_current_hex']);synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
    for label,image in zip(['clean','current'],images,strict=True):
        result=walk(image.read_file('/__arm9__.bin'),synthetic)
        assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic)
        assert len(result['rows'])==1 and result['rows'][0]['word']==0xA000 and result['rows'][0]['native_extent']==8
        versions.append(dict(version=label,**result))
    assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
    ROOT.mkdir(parents=True)
    save(ROOT/'one_A000_no_C200_single_end_and2_source_leaves.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_predicate_cases=[],
        all2_source_current_nonrelative_nonspeech_leaves=leaves,source_C200_pairs=[],source_has_no_C200_and_no_C200_probe_invented=True,
        one_A000_structural_cases=[dict(source_site=leaves[0],versions=versions,isolated_offset8_matches_original_cursor=True,
            nondecode_effect_callee_bridged_zero_return_not_body_or_game_state_execution=True)],
        source_A000_hex_by_offset={'8':'00a0ffff01221da1'},source_A000_packed_operand_semantics_not_inferred=True,
        source_declared_end_offsets=[508],source_pause_resume_pairs=[],source_linear_path_command_offsets=[c['offset'] for c in commands],
        all14_speeches_on_complete_linear_structural_path=True,FE1_impersonal_notice_and_progressive13_dispatches_bound_separately=True,
        no_source_relative_predicate_2000_pause_2100_4100_C200_resources_or_presentation_sites=True,
        source_A000_full_body_actual_displays_and_earned_fashion_state_unexecuted_by_this_probe=True,
        source_owned_adapter=inspect.getsource(walk),evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,BRANCH,Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(nonrelative_leaves=2,A000_structural_pairs=1,C200=0,FE=1,progressive=13,end=508,actual_scene_unexecuted=True,credit=0))
