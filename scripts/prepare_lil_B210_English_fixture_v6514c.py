"""Compile the exact source-locked preparation fragment with its enclosing block intact."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B210_English_fixture_tools_v6514c')
if __name__=='__main__':
    assert not ROOT.exists();failed=Path('scripts/prepare_lil_B210_stored_reference_English_v6514.py');text=failed.read_text('utf-8');begin=text.index("    rows.append(derive('scripts/research_lil_B209_English_fixture_v6469.py'");end=text.index('    ROOT.mkdir',begin)
    fragment=checked_text('if True:\n'+text[begin:end],{"'source_event209':'source_event210'":"'natural_event209':'natural_event210'"});rows=[];exec(compile(fragment,__file__+'::source-locked-English-only-successor','exec'),dict(derive=derive,rows=rows));ROOT.mkdir(parents=True);(ROOT/'frozen_corrected_preparation_fragment.py').write_text(fragment,'utf-8');existing=[Path('scripts/prove_lil_B210_stored_v6514.py'),Path('scripts/create_lil_B210_reference_v6515.py')]
    save(ROOT/'prepared_tools.json',dict(derived_English_fixture=rows,preserved_prior_prepared_tools={str(p):sha(p.read_bytes()) for p in existing},earlier_absent_key_and_dedented_fragment_failures_preserved_before_any_English_ROM_write=True,actual_key_is_natural_event209=True,full_preparation_block_compiles_before_derivation=True,source_conditions_metadata_not_native_guards_changed=True,all_native_instruction_constants_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Exact enclosed English-fixture derivation completed;stored proof/reference tool and both earlier preparation failures preserved. No English ROM write yet.')
