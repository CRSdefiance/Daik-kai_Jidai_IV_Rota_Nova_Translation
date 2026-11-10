"""Bind both B210 leaves without inventing attribute/item or effect semantics."""
from pathlib import Path
import struct,inspect
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B210_controls_v6505');SOURCE=Path('work/analysis/lil_B210_source_v6498/ten_clean_current_complete_exchange_source_references.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[210] for im in images];g=packet['blocks'][0];leaves=[]
    assert len(g['all_clean_native_commands'])==len(g['all_current_native_commands'])==12
    for a,b in zip(g['all_clean_native_commands'],g['all_current_native_commands'],strict=True):
        assert (a['offset'],a['word'],a['native_extent'])==(b['offset'],b['word'],b['native_extent'])
        if a['word']!=0x4000:assert a['whole_command_hex']==b['whole_command_hex'];leaves.append(a)
    assert [(c['offset'],c['whole_command_hex']) for c in leaves]==[(674,'00a0ffff24000110'),(682,'00000000')]
    structural=[];ends=[]
    for c in leaves[:-1]:
        value=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;pair=[]
        for version,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),isolated);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['word']==c['word'] and result['rows'][0]['native_extent']==c['native_extent'];pair.append(dict(version=version,**result))
        assert pair[0]['rows']==pair[1]['rows'] and pair[0]['opaque_effect_bridges']==pair[1]['opaque_effect_bridges'];structural.append(dict(source_offset=c['offset'],word=c['word'],source_command_hex=value.hex(),cases=pair,isolated_offset8_not_original_cursor=True,nondecode_bodies_bridged_not_full_effects_or_gameplay=True))
    for version,image,b in zip(['clean','current'],images,blocks,strict=True):
        logical=8+struct.unpack_from('<H',b,4)[0];assert (len(b),logical)==(688,686) and b[logical:]==bytes(2) and b[682:686]==bytes(4)
        for previous in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=version,stored_bytes=688,logical_end=686,tailzeros=2,**end_case(image.read_file('/__arm9__.bin'),b,682,previous)))
    assert len(structural)==1 and len(ends)==10
    ROOT.mkdir(parents=True);save(ROOT/'one_source_current_structural_pair_and_ten_guarded_complete_end_cases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),all2_source_current_nontext_leaves=leaves,source_A000_structural_pair=structural,ten_guarded_complete_end_cases=ends,source_stored688_logical686_tail2_complete_end682=True,all_original_operands_and_native_result_extents_preserved=True,isolated_effect_bodies_bridged_not_stat_item_inventory_quest_or_eligibility_proof=True,no_inherited_B209_typed_relative_predicate_or_A000_operand_assumption=True,source10_static_progressive_speeches_no_FE_or_macro_preserved=True,source_owned_adapters=dict(end=inspect.getsource(end_case),structural=inspect.getsource(walk)),actual_source_reachability_and_full_effects_unclaimed=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]},full_goal_complete=False));print('B210 one source/current A000 structural pair and10 guarded ends pass. Actual stat/item/full effects remain unclaimed.')
