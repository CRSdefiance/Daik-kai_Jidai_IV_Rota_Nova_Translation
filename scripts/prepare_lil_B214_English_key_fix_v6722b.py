"""Correct the exact existing metadata key and preflight every derivation key before generation."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B214_English_key_fix_v6722b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('scripts/research_lil_B214_English_fixture_v6722.py').exists()
    before=Path('scripts/prepare_lil_B214_English_fixture_v6722.py').read_text('utf8');changes={"'source_event209':'source_event214'":"'natural_event209':'natural_event214'"};planned=checked_text(before,changes)
    call=next(n for n in ast.walk(ast.parse(planned)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='derive');mapping=ast.literal_eval(call.args[2]);source=Path(ast.literal_eval(call.args[0])).read_text('utf8');assert all(key in source for key in mapping);checked_text(source,mapping)
    proof=derive('scripts/prepare_lil_B214_English_fixture_v6722.py','scripts/prepare_lil_B214_English_fixture_v6722b.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_metadata_key_correction.json',dict(derivation=proof,all_target_derivation_keys_preflighted_against_original_source=True,first_attempt_stopped_before_target_generation_or_ROM_mutation=True,no_source_prose_or_native_constant_change=True,full_goal_complete=False))
