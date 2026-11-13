"""Derive the independent native-command reconstruction, preserving all native constants."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_independent_rebuild_tools_v8289')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('dk4tool/patch/gerhard_surname_rebuild_v1.py','dk4tool/patch/hodram_three_blocks_rebuild_v1.py',{
        'Independently reconstruct five sparse speeches and every affected relative operand in memory.':'Independently reconstruct all28 Hodram speeches and every affected relative operand in memory.',
        'len(container.blocks)!=336 or len(rows)!=5':'len(container.blocks)!=325 or len(rows)!=28',
        'for number in [27,74]:':'for number in [137,45,46]:',
        '[27,74]':'[45,46,137]',
        'Exact five sparse SC2 B27/B74 records and336 blocks required':'Exact28 SC1 B137/B45/B46 records and325 blocks required',
        'len(selected)!=(2 if number==27 else 3)':'len(selected)!={137:21,45:1,46:6}[number]',
        'Exact per-block sparse record count required':'Exact per-block complete speech count required',
        'value[0] not in [1,9,16]':'value[0] not in [1,2,9,16,18,113]',
        'full_clean_TEXT_inverse_not_claimed_for_sparse_change=True':'clean_source_inverse_checked_separately_by_sourcequalified_seal=True',
        'Exactly two reviewed blocks may change':'Exactly three reviewed blocks may change',
        "sum(len(g['all_target_commands']) for g in groups)!=225":"sum(len(g['all_target_commands']) for g in groups)!=60",
        "sum(len(g['relative_fixups']) for g in groups)!=44":"sum(len(g['relative_fixups']) for g in groups)!=8",
        "sum(g['unchanged_speeches'] for g in groups)!=125":"sum(g['unchanged_speeches'] for g in groups)!=0",
        'Complete225 commands/44relative sites/125unowned speeches required':'Complete60commands/eightrelative sites/all28speech bodies required',
        'unchanged_archive_blocks=334':'unchanged_archive_blocks=322',
    })
    ROOT.mkdir(parents=True);save(ROOT/'independent_native_command_rebuild_derivation.json',dict(derivation=result,
        no_research_block_payload_copy_sourcequalified_replacements_andnative_inventory=True,
        all_native_constants_limits_parity_relatives_full_terminal_andpredecessor_inverses_preserved=True,
        clean_source_inverse_reference_seal_next=True,new_credit=0,full_goal_complete=False))
    print('Independent Hodram archive reconstruction prepared:28 bodies/60commands/eightrelative sites/322otherblocks preserved.')
