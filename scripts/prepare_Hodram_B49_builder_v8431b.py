"""Compile a stage fragment in its original suite context;preserve the rejected standalone-fragment attempt."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_builder_tools_v8431b');assert not root.exists();tools=[]
    tools.append(derive('dk4tool/patch/hodram_outcomes_builder_guard_v3.py','dk4tool/patch/hodram_outcomes_builder_guard_v4.py',{
        "STAGE_V4=checked_text(STAGE_V3,{'hodram_outcomes_editorial_v3':'hodram_outcomes_editorial_v4'})":"STAGE_V4=checked_text('if True:\\n'+STAGE_V3,{'hodram_outcomes_editorial_v3':'hodram_outcomes_editorial_v4'}).split('\\n',1)[1]",
    }))
    tools.append(derive('scripts/validate_Hodram_B49_builder_v8431.py','scripts/validate_Hodram_B49_builder_v8431b.py',{
        'hodram_outcomes_builder_guard_v3':'hodram_outcomes_builder_guard_v4',
        'Hodram_B49_builder_v8431':'Hodram_B49_builder_v8431b',
    }))
    root.mkdir(parents=True);save(root/'derivations.json',dict(derivations=tools,failed_import_before_any_builder_orregistry_change_preserved=True,only_indented_fragment_compilation_context_fixed=True,all_exact_stage_texts_full_inverse_andmutation_guards_unchanged=True,new_credit=0,full_goal_complete=False))
