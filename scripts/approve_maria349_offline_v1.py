"""Keep every scoped offline guard with the freshly checked final style plan."""
import inspect
from scripts import approve_scoped_clean_offline_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "styles=root/'compiled_styles_v1/compiled_style_objects.json'":"styles=root/'compiled_styles_v3/compiled_style_objects.json'",
    "stylepath=root/'compiled_styles_v2/compiled_style_objects.json'":"stylepath=root/'compiled_styles_v4/compiled_style_objects.json'",
    "'exact_prior_native_slot_and27_compiler_negative_cases_reused':True":"'exact_prior_native_slot_and_source_bound_compiler_negatives_reused':True,'exact_reused_compiler_negative_cases':9*len(styles['objects'])",
})
env={**previous.main.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::all-source-current-native-visual-style-menu-andname-guards','exec'),env)
if __name__=='__main__':env['main']()
