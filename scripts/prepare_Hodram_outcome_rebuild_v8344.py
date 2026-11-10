"""Source-lock sparse independent rebuild and exact-reference checks to two mixed FE/progressive outcomes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_rebuild_tools_v8344');assert not root.exists();tools=[]
    tools.append(derive('dk4tool/patch/hodram_three_blocks_rebuild_v1.py','dk4tool/patch/hodram_outcome_rebuild_v1.py',{
        'all28 Hodram speeches':'all6 Hodram outcome speeches','len(rows)!=28':'len(rows)!=6','[45,46,137]':'[47,48]','[137,45,46]':'[47,48]',
        'Exact28 SC1 B137/B45/B46':'Exact6 SC1 B47/B48','{137:21,45:1,46:6}':'{47:3,48:3}','[1,2,9,16,18,113]':'[2,254]',
        'Exactly three reviewed blocks':'Exactly two reviewed blocks',
        "sum(len(g['all_target_commands']) for g in groups)!=60":"sum(len(g['all_target_commands']) for g in groups)!=15",
        "sum(len(g['relative_fixups']) for g in groups)!=8":"sum(len(g['relative_fixups']) for g in groups)!=0",
        'Complete60commands/eightrelative sites/all28speech bodies':'Complete15commands/zerorelative sites/all6speech bodies',
        'unchanged_archive_blocks=322':'unchanged_archive_blocks=323',
    }))
    tools.append(derive('dk4tool/patch/hodram_three_blocks_references_v1.py','dk4tool/patch/hodram_outcome_references_v1.py',{
        'hodram_three_blocks_rebuild_v1':'hodram_outcome_rebuild_v1',
        "len(result['groups'])==len(research['groups'])==len(packet['groups'])==3":"len(result['groups'])==len(research['groups'])==len(packet['groups'])==2",
        "result['unchanged_archive_blocks']==322":"result['unchanged_archive_blocks']==323",'three complete groups/322 unowned blocks':'two complete groups/323 unowned blocks',
        '[137,45,46]':'[47,48]','(60,8,28)':'(15,0,6)','all60 commands/eight relatives/28speeches':'all15 commands/zero relatives/6speeches',
        '[45,46,137]':'[47,48]','only three owned blocks':'only two owned blocks',
    }))
    root.mkdir(parents=True);save(root/'source_locked_independent_sparse_rebuild_reference_derivations.json',dict(tools=tools,
        sparse_body_patch_rebuild_independent_of_commandwise_research_generator=True,native_high_integer_constants_andmultiplicity_preserved=True,original_FE_preamble_andone_FI_not_converted_to_text=True,new_credit=0,full_goal_complete=False))
