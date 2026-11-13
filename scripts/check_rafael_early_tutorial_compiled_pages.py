"""Keep complete native page checks with the measured current Rafael own context."""
from scripts.check_editorial_compiled_pages_v8 import source as original,check_FE_rows,validate_documented_layouts
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(original,{
    'from scripts.registered_editorial_runtime import RegisteredRuntime':'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    'ctx=RegisteredRuntime(args.release,args.startup)':'ctx=RegisteredRuntime(args.release,args.startup,captain=0)',
    "MACROS = Path('work/analysis/Hodram_B61_B70_logical_v8891/logical_paragraphs.json')":
        "MACROS = Path('work/analysis/Rafael_early_tutorial_B42_B43_source_display_20261104/40_native_selectors_macros_andcomplete_preamble_bindings.json')",
    "'Hodram'":"'Rafael'","'Bergstrom'":"'Castor'","'Bergstrom Fleet'":"'Castor Co.'",
    "'assert identity==prefix and captain==1':'assert captain==1 and identity==(prefix if prefix<207 else DYNAMIC_BINDINGS[prefix])'":
        "'assert identity==prefix and captain==0':'assert captain==0 and identity==(prefix if prefix<207 else DYNAMIC_BINDINGS[prefix])'",
})
exec(compile(source,__file__+'::same-native-pages-current-Rafael-defaults-andzero-authored-layouts','exec'),globals())
