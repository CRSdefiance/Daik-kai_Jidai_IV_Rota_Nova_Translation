"""Apply the existing native nameplane checks with the exact Rafael1674 dependency binding."""
from scripts.check_qualified_scoped_name_planes_v2 import TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "bound['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified']":
        "bound['exact_unchanged_actor0_macro_dependencies']",
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-native-nameplane-proof-current-exact-runtime','exec'),globals())
