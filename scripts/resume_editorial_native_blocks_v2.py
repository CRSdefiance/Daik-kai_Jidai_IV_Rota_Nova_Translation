"""Keep each consumer's distinct ABI receipt keys,including FE's null actor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/resume_editorial_native_blocks.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    "c['original_macro_ABI_input_output_canaries_and_all_unowned4MiB_exact']":
        "(c['original_macro_ABI_input_output_canaries_and4MiB_exact'] and c['null_source_actor'] if row['kind']=='system-FE' else c['original_macro_ABI_input_output_canaries_and_all_unowned4MiB_exact'])",
})
exec(compile(source,__file__+'::original-distinct-static-andFE-contracts','exec'),globals())
