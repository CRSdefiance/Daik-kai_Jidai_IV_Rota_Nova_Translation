"""Check all residual stored pages, compound objects and relocated branches."""
import inspect
from pathlib import Path
from scripts import check_hodram_B311_B324_stored_v1 as previous
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
check_FE_rows=previous.check_FE_rows
compound_source=checked_text(inspect.getsource(previous.compound_storage),{
    'exact_compiled_body_font_runtime_and64_slot_getter_proof_reuse':
        'exact_compiled_body_font_runtime_and56_slot_getter_proof_reuse',
})
compound_env=dict(previous.compound_storage.__globals__)
exec(compile(compound_source,__file__+'::same-stored-compound-objects-correct56-slot-scope','exec'),compound_env)
compound_storage=compound_env['compound_storage']
source=checked_text(previous.source,{
    "assert ctx.receipt()==runtime and rebuilt['parent_sha256']==runtime['candidate_sha256']":
        "assert ctx.receipt()==runtime\n    doc=load(rebuilt['manuscript'])\n    assert rebuilt['parent_sha256']==doc['current_ROM_sha256']==doc['exact_existing_native_context_reuse']['target_candidate_sha256']\n    assert runtime==doc['runtime']==doc['exact_existing_native_context_reuse']['native_runtime']",
    "ROOT/'native_initial_v1/compiled_native_pages.json'":"ROOT/'native_remaining_v1/compiled_native_pages.json'",
    digest(previous.ROOT/'native_initial_v1/compiled_native_pages.json'):
        digest(ROOT/'native_remaining_v1/compiled_native_pages.json'),
    "rebuilt['style_physical_speech_count']==236":"rebuilt['style_physical_speech_count']==47",
    "rebuilt['total_rendered_speech_count']==387":"rebuilt['total_rendered_speech_count']==388",
    "rebuilt['typed_choice_count']==13":"rebuilt['typed_choice_count']==6",
})
exec(compile(source,__file__+'::same-stored-native-pixels-parity-complete-consumption-and-relative-contracts','exec'),globals())
