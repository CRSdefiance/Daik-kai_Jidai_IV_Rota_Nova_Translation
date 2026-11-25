"""Derive a Maria-only source-locked relocation test; do not rewrite old producers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_relocation_tools_v7696')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/research_papal_trade_relocation_v7640.py','scripts/research_Maria_B207_relocation_v7696.py',{
        'Relocate both full exchanges; preserve commands and reconstruct each predecessor exactly.':'Relocate the complete Maria exchange; preserve CS0101 and reconstruct predecessor andclean source exactly.',
        'papal_trade_profile_v1':'maria_B207_profile_v1','papal_trade_layout_v1':'maria_B207_layout_v1',
        'from scripts.draft_papal_trade_prose_v7631 import MANUSCRIPTS,CURRENT':'from scripts.draft_Maria_B207_prose_v7687 import MANUSCRIPT,CURRENT,CLEAN\nMANUSCRIPTS={3:MANUSCRIPT}',
        'papal_trade_relocation_v7640':'maria_B207_relocation_v7696',
        'papal_trade_policy_validation_v7639/36_positives174_expected_actual_changing_rejections_before_mutation':'maria_B207_policy_validation_v7695/18_positives89_expected_actual_changing_rejections_before_mutation',
        "policy['positive_count']==36 and policy['negative_count']==174":"policy['positive_count']==18 and policy['negative_count']==89",
        "spec=current['groups'][route]":"spec=current",
        "assert bytes(restored)==source":"assert bytes(restored)==source\n        assert source[:8].hex()=='43530101b4050000' and target[:4]==source[:4]\n        cleanpacket=read(CLEAN);cleanblock=bytes.fromhex(cleanpacket['clean_block_hex']);cleanrestored=bytearray(target[:len(logical)]);struct.pack_into('<H',cleanrestored,4,len(cleanblock)-8)\n        byid={r['id']:r for r in doc['records']}\n        for p in reversed(patches):\n            at=mapped(p['start']);cleanrestored[at:at+len(p['value'])]=bytes.fromhex(byid[p['id']]['source_hex'])\n        assert bytes(cleanrestored)==cleanblock",
        'external_references_complete=False))':'clean_source_block_inverse_exact=True,complete_CS0101_header_preserved=True,external_references_complete=False))',
        "assert Path(groups[0]['research_block']).read_bytes()==Path(groups[1]['research_block']).read_bytes()":"assert len(groups)==1 and groups[0]['route']==3 and groups[0]['clean_source_block_inverse_exact']",
        'two_archives36_speeches40_commands_exact_predecessor_inverse_RESEARCH':'Maria18_speeches20_commands_exact_clean_andpredecessor_inverse_RESEARCH',
        'both_target_blocks_byte_identical=True,all36_source_current_compiled_stored_references_bound=True,all40_commands_complete_preambles_opaque_operands_andfour_byte_ends_preserved=True,both_full_predecessor_archives_reconstruct_exactly=True':'distinct_CS0101_header_preserved=True,all18_source_current_compiled_stored_references_bound=True,all20_commands_complete_preambles_opaque_operands_andfour_byte_end_preserved=True,complete_clean_source_block_andfull_predecessor_archive_reconstruct_exactly=True',
        'translations/papal_trade_native_contract_v1.json':'translations/maria_B207_native_contract_v1.json',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_Maria_complete_block_relocation.json',dict(derivation=result,no_native_high_constant_oroperand_change=True,new_credit=0,full_goal_complete=False))
