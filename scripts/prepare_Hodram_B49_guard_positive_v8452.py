"""Extend exact builder challenges andpreceding whole-image positive to corrected B49 ownership."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    source=Path('scripts/validate_Hodram_B49_builder_v8431b.py').read_text('utf8');start=source.index('from dk4tool.patch.hodram_outcomes_builder_guard_v4 import (');end=source.index('from scripts.verify_village_wrap',start)
    derive('scripts/validate_Hodram_B49_builder_v8431b.py','scripts/validate_Hodram_B49_builder_v8452.py',{
        source[start:end]:"from dk4tool.patch.hodram_outcomes_builder_guard_v4 import BUILDER,STAGE_V3,LEGACY_STAGE,ANCHOR\nfrom dk4tool.patch.hodram_outcomes_builder_guard_v5 import STAGE_V5 as STAGE_V4,STAGE_B49_V2 as STAGE_B49,validate_builder_bytes\n",
        'Hodram_B49_builder_v8431b':'Hodram_B49_builder_v8452',
        "('changed-B49-module',planned.replace(b'hodram_B49_editorial_v1 import',b'hodram_B49_editorial_v2 import',1))":"('changed-B49-module',planned.replace(b'hodram_B49_editorial_v2 import',b'hodram_B49_editorial_v3 import',1))",
        "('changed-outcomes-module',planned.replace(b'hodram_outcomes_editorial_v4 import',b'hodram_outcomes_editorial_v5 import',1))":"('changed-outcomes-module',planned.replace(b'hodram_outcomes_editorial_v5 import',b'hodram_outcomes_editorial_v6 import',1))",
        "Path('dk4tool/patch/hodram_outcomes_builder_guard_v4.py')":"Path('dk4tool/patch/hodram_outcomes_builder_guard_v5.py')",
        'compatible-v4-only':'compatible-v5-only','compatible-v4-plus-B49':'compatible-v5-plus-B49-v2',
    })
    derive('scripts/validate_Hodram_outcome_atomic_positive_v8445.py','scripts/validate_Hodram_outcome_atomic_positive_v8453.py',{
        'hodram_outcomes_editorial_v4':'hodram_outcomes_editorial_v5','Hodram_outcome_atomic_positive_v8445':'Hodram_outcome_atomic_positive_v8453','compatible_v4_configuration':'compatible_v5_configuration',
    })
