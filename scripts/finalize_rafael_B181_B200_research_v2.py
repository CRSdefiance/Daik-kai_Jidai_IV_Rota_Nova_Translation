"""Supply the scoped name manuscript's encoder metadata and preserve the first attempt."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


parent = Path(__file__).with_name('finalize_rafael_B181_B200_research_v1.py')
source = checked_text(parent.read_text(encoding='utf-8'), {
    'Rafael_B181_B200_research_final_v1_20261106': 'Rafael_B181_B200_research_final_v2_20261106',
    'names.update(all_name_formatting_gates_pending=False,': "names.update(encoder='dialogue-relocatable-v1',all_name_formatting_gates_pending=False,",
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-evidence-guards-and-scoped-name-schema', 'exec'),globals())
