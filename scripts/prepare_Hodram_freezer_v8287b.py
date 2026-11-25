"""Use the existing generated_lines waiver binding; preserve failed original freezer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_freezer_tools_v8287b');assert not root.exists()
    result=derive('scripts/freeze_Hodram_three_blocks_policy_v8287.py','scripts/freeze_Hodram_three_blocks_policy_v8287b.py',{
        'Hodram_three_block_policy_v8287':'Hodram_three_block_policy_v8287b',
        "assert scope['logical_English']==row['logical_English']":"assert scope['generated_lines']==p['lines'] and ' '.join(scope['generated_lines'])==row['logical_English']",
    })
    root.mkdir(parents=True);save(root/'existing_exact_waiver_schema_successor.json',dict(derivation=result,
        earlier_failure_before_any_policy_output_preserved=True,generated_lines_compile_source_andfull_logical_prose_bound=True))
