"""Source-lock whole-body B222 relocation; retain every command and all1112 source bytes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B222_relocation_tools_v7052')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/research_lil_B220_relocation_v6940.py').read_text('utf8');effect=next(s for s in source.splitlines() if s.startswith('    effects='))
    new_effect="    effects=[dict(source_offset=1100,target_offset=mapped(1100),extent=8,source_hex='00a0ffff44000110')];uis=[];ends=[dict(source_offset=1108,target_offset=mapped(1108),extent=4,source_hex='00000000')];assert mapped(1108)+4==len(logical)"
    changes={'B220':'B222','v6940':'v7052','editorial_manuscript_v2.json':'editorial_manuscript_v3.json','blocks[220]':'blocks[222]','block=220':'block=222','[220]':'[222]','1280':'1112',"struct.pack_into('<H',restored,4,1272)":"struct.pack_into('<H',restored,4,1104)",'len(patches)==17':'len(patches)==16','len(commands)==20 and len(speeches)==17':'len(commands)==18 and len(speeches)==16','SC2_block220_RESEARCH_ONLY':'SC2_block222_RESEARCH_ONLY','all20_original_commands':'all18_original_commands','all17_exact_source_current_compiled':'all16_exact_source_current_compiled','all17_objects20_commands_full1280_inverse_RESEARCH':'all16_objects18_commands_full1112_inverse_RESEARCH','Rebuild seventeen speech':'Rebuild sixteen speech',effect:new_effect}
    checked_text(source,changes);tool=derive('scripts/research_lil_B220_relocation_v6940.py','scripts/research_lil_B222_relocation_v7052.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_complete_body_relocation.json',dict(tool=tool,all_native_addresses_preserved=True,original_A000_exact_no_C200_no_choices_no_relatives=True,source1112_stored_logical_end_no_tail=True,new_credit=0,full_goal_complete=False))
