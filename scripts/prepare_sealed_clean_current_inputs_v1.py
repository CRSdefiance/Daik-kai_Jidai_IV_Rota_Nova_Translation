"""Bridge generic sealed clean drafts without manufacturing review approval."""
from scripts.prepare_maria335_B137_B151_current_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    "drafts['independent_clean_drafts_before_current_English']":"drafts['all_independent_drafts_sealed_before_current_comparison']",
    "drafts['source_meanings']":"drafts['source_meaning_file']",
    "drafts['source_meanings_sha256']":"drafts['source_meaning_file_sha256']",
})
env={**__import__('scripts.prepare_clean_editorial_current_inputs_v1',fromlist=['']).__dict__,'__file__':__file__}
exec(compile(source,__file__+'::same-source-caption-control-andsealed-draft-guards','exec'),env)
if __name__=='__main__':env['main']()
