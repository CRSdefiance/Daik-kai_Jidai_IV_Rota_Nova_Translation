"""Preserve B207's sole opaque A000 and guarded complete end;no invented item effect."""
from pathlib import Path
import struct,inspect
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B207_controls_v6344')
SOURCE=Path('work/analysis/lil_B207_source_v6338/all13_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[207] for im in images];group=packet['blocks'][0];leaves=[]
    assert len(group['all_clean_native_commands'])==len(group['all_current_native_commands'])==15
    for a,b in zip(group['all_clean_native_commands'],group['all_current_native_commands'],strict=True):
        assert (a['offset'],a['word'],a['native_extent'])==(b['offset'],b['word'],b['native_extent'])
        if a['word']!=0x4000:assert a['whole_command_hex']==b['whole_command_hex'];leaves.append(a)
    assert [(c['offset'],c['whole_command_hex']) for c in leaves]==[(642,'00a0ffff29000110'),(650,'00000000')]
    value=bytes.fromhex(leaves[0]['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;structural=[];ends=[]
    for version,image,block in zip(['clean','current'],images,blocks,strict=True):
        result=walk(image.read_file('/__arm9__.bin'),isolated);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['word']==0xA000 and result['rows'][0]['native_extent']==8
        structural.append(dict(version=version,**result));logical=8+struct.unpack_from('<H',block,4)[0];assert (len(block),logical)==(656,654) and block[logical:]==bytes(2) and block[650:654]==bytes(4)
        for previous in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=version,stored_bytes=656,logical_end=654,tailzeros=2,**end_case(image.read_file('/__arm9__.bin'),block,650,previous)))
    assert structural[0]['rows']==structural[1]['rows'] and structural[0]['opaque_effect_bridges']==structural[1]['opaque_effect_bridges'] and len(ends)==10
    ROOT.mkdir(parents=True);save(ROOT/'one_exact_A000_and_ten_guarded_complete_end_cases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),all2_source_current_nontext_leaves=leaves,one_A000_source_current_structural_pair=structural,ten_guarded_complete_end_cases=ends,isolated_A000_offset8_not_original_cursor=True,nondecode_effect_body_bridged_not_full_quest_inventory_or_eligibility_execution=True,no_source_picture_short47xx_typed_menu_relative_pause_FE_or_macro_assumptions=True,source_stored656_logical654_tail2_complete_end650=True,source_owned_adapters=dict(end=inspect.getsource(end_case),structural=inspect.getsource(walk)),actual_source_reachability_and_full_effects_unclaimed=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]},full_goal_complete=False));print('B207 one original A000 structural pair and10 guarded clean/current complete ends pass. Full quest effect/outer eligibility remain unclaimed.')
