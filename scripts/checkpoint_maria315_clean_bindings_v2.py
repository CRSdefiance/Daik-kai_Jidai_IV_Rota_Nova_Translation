"""Keep all checkpoint guards with the native getter count's actual integer schema."""
import inspect
from scripts import checkpoint_maria315_clean_bindings_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "len(objects['native_style_getter_cases'])==136":"objects['native_style_getter_cases']==136",
    "ROOT/'all315_clean_meanings_v1.json',ROOT/'all315_independent_drafts_v1.json',Path(__file__)]":
        "ROOT/'all315_clean_meanings_v1.json',ROOT/'all315_independent_drafts_v1.json',Path('scripts/checkpoint_maria315_clean_bindings_v1.py'),Path(__file__)]",
})
env={**previous.main.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-checkpoint-source-draft-runtime-andzero-credit-contract','exec'),env)
if __name__=='__main__':env['main']()
