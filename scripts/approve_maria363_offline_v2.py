"""Keep the full offline contract and bind the original dictionary-label source anchor."""
import inspect
from scripts import approve_scoped_clean_offline_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "manuscript=root/'formatting_v1/formatting_input.json'":"manuscript=root/'formatting_v1/formatting_input_v2.json'",
    "'exact_prior_native_slot_and27_compiler_negative_cases_reused':True":
        "'exact_prior_native_slot_and_source_bound_compiler_negatives_reused':True,'exact_reused_compiler_negative_cases':9*len(styles['objects'])",
})
env={**previous.main.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-every-record-tile-native-ABI-menu-name-andstyle-approval-contract','exec'),env)
if __name__=='__main__':env['main']()
