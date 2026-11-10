"""Bridge sealed drafts with pending gates without manufacturing editorial approval."""
import inspect
from scripts import prepare_editorial_clean_current_inputs_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(inspect.getsource(previous.main), {
    "assert meanings['no_current_English_dialogue_consulted_for_eligible_records']":
        "assert meanings['all_source_meanings_read_as_complete_exchanges_before_existing_English'] and drafts['current_eligible_story_English_not_extracted']",
    "'source_meaning','exchange_context'": "'source_meaning','whole_exchange_context'",
    "assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)":
        "assert row['review']==dict(source=False,context=False,localization=False,naturalness=False,formatting=False)",
})
env={**vars(previous),'__file__':__file__}
exec(compile(source,__file__+'::same-sealed-draft-source-control-guards-no-approval-inferred','exec'),env)

if __name__=='__main__':
    env['main']()
