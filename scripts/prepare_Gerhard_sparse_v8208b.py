"""Preserve the approved Hamburg translated choice while binding every other control exactly."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_sparse_tools_v8208b')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/relocate_Gerhard_sparse_v8208.py','scripts/relocate_Gerhard_sparse_v8208b.py',{
        'Gerhard_sparse_relocation_v8208':'Gerhard_sparse_relocation_v8208b',
        "INPUT=Path('work/analysis/current_V8172_Lil_native_v8198/current_native_input.json')":
        "INPUT=Path('work/analysis/current_V8172_Lil_native_v8198/current_native_input.json')\nCHOICE=Path('translations/lil_hamburg_editorial_relocation_map_v1.json')",
        "assert not ROOT.exists();current,doc,plan,view=map(read,[CURRENT,MANUSCRIPT,PLAN,VIEW])":
        "assert not ROOT.exists();current,doc,plan,view=map(read,[CURRENT,MANUSCRIPT,PLAN,VIEW]);prior_choice=read(CHOICE)['blocks'][0]\n    assert prior_choice['block']==74 and len(prior_choice['choice_commands'])==1",
        "else:assert source['whole_command_hex']==command['whole_command_hex']":
        """elif word==0x2100:
                    choice=prior_choice['choice_commands'][0]
                    assert number==74 and spec['clean_block_sha256']==prior_choice['clean_block_sha256'] and spec['current_block_sha256']==prior_choice['target_block_sha256']
                    assert source['offset']==choice['old_offset']==3504 and source['native_extent']==choice['old_length']==48
                    assert command['offset']==choice['new_offset']==3572 and command['native_extent']==choice['new_length']==30
                    assert command['whole_command_hex']==choice['target_hex'] and choice['labels']==['Yes, please.','No need.']
                else:assert source['whole_command_hex']==command['whole_command_hex']""",
        'complete_clean_command_order_preambles_relative_targets_andopaque_controls_exact=True':
        'complete_clean_command_order_preambles_relative_targets_opaque_controls_andexact_prior_typed_choice_preserved=True',
        'stored_fonts_end_valuecarry_fullreference_callers_loaders_actual_policy_production_andregistered_release_pending=True,':
        "stored_fonts_end_valuecarry_fullreference_callers_loaders_actual_policy_production_andregistered_release_pending=True,\n        exact_prior_translated_Hamburg_choice=prior_choice['choice_commands'],\n        preserved_failure='scripts/relocate_Gerhard_sparse_v8208.py stopped on the already translated choice;partial research block27 only,no ROM/archive/registry writes',",
        '[CURRENT,MANUSCRIPT,PLAN,VIEW,INPUT,Path(__file__)]':'[CURRENT,MANUSCRIPT,PLAN,VIEW,INPUT,CHOICE,Path(__file__)]',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared exact prior typed-choice preservation;all other source/current and target controls unchanged.')
