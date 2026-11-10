"""Project the363 sealed clean-first drafts; preserve all source/control guards."""
import inspect
from scripts import prepare_clean_editorial_current_inputs_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "    assert drafts['whole_clean_exchanges_read_before_drafting']":
        "    assert drafts['all363_independent_drafts_saved'] and drafts['complete_exchanges']==37\n    assert all(r['source_meaning_reviewed_from_complete_clean_exchange'] for r in drafts['records'])",
    "r['current_English_comparison_pending']":"r['contextual_comparison_pending']",
})
env={**vars(previous),'__file__':__file__}
exec(compile(source,__file__+'::same-source-style-menu-andpreamble-guards','exec'),env)
if __name__=='__main__':env['main']()
