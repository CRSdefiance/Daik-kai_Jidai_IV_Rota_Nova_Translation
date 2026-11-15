"""Bind all five B208 leaves without inventing attribute/item or effect semantics."""
from pathlib import Path
import struct,inspect
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B208_controls_v6396');SOURCE=Path('work/analysis/lil_B208_source_v6390/all24_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[208] for im in images];g=packet['blocks'][0];leaves=[]
    assert len(g['all_clean_native_commands'])==len(g['all_current_native_commands'])==29
    for a,b in zip(g['all_clean_native_commands'],g['all_current_native_commands'],strict=True):
        assert (a['offset'],a['word'],a['native_extent'])==(b['offset'],b['word'],b['native_extent'])
        if a['word']!=0x4000:assert a['whole_command_hex']==b['whole_command_hex'];leaves.append(a)
    assert [(c['offset'],c['whole_command_hex']) for c in leaves]==[(1118,'0560'),(1120,'2e63'),(1166,'00a0ffff01020760'),(1174,'00a0ffff28000110'),(1182,'00000000')]
    structural=[];ends=[]
    for c in leaves[:-1]:
        value=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;pair=[]
        for version,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),isolated);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['word']==c['word'] and result['rows'][0]['native_extent']==c['native_extent'];pair.append(dict(version=version,**result))
        assert pair[0]['rows']==pair[1]['rows'] and pair[0]['opaque_effect_bridges']==pair[1]['opaque_effect_bridges'];structural.append(dict(source_offset=c['offset'],word=c['word'],source_command_hex=value.hex(),cases=pair,isolated_offset8_not_original_cursor=True,nondecode_bodies_bridged_not_full_effects_or_gameplay=True))
    for version,image,b in zip(['clean','current'],images,blocks,strict=True):
        logical=8+struct.unpack_from('<H',b,4)[0];assert (len(b),logical)==(1188,1186) and b[logical:]==bytes(2) and b[1182:1186]==bytes(4)
        for previous in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=version,stored_bytes=1188,logical_end=1186,tailzeros=2,**end_case(image.read_file('/__arm9__.bin'),b,1182,previous)))
    assert len(structural)==4 and len(ends)==10
    ROOT.mkdir(parents=True);save(ROOT/'four_source_current_structural_pairs_and_ten_guarded_complete_end_cases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),all5_source_current_nontext_leaves=leaves,source6005_632E_two_A000_structural_pairs=structural,ten_guarded_complete_end_cases=ends,source_stored1188_logical1186_tail2_complete_end1182=True,all_original_operands_and_native_result_extents_preserved=True,isolated_effect_bodies_bridged_not_stat_item_inventory_quest_or_eligibility_proof=True,no_inherited_B207_A000_operand_or_zero_FE_assumption=True,source_23_progressive_one_FE_private_thought_and_literal_character_notice_preserved=True,source_owned_adapters=dict(end=inspect.getsource(end_case),structural=inspect.getsource(walk)),actual_source_reachability_and_full_effects_unclaimed=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]},full_goal_complete=False));print('B208 four source/current structural pairs(6005,632E,two A000) and10 guarded ends pass. Actual stat/item/full effects remain unclaimed.')
