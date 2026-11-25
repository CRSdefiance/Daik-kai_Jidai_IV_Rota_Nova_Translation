"""Check the new stored scope and actual FE row membership with unchanged native consumers."""
from scripts import check_editorial_stored_batch_v3 as previous
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.source_locked_derivation_v5118 import checked_text

compound_storage = previous.compound_storage
source = checked_text(previous.source, {
    "rebuilt['style_physical_speech_count']==48": "rebuilt['style_physical_speech_count']==8",
    "rebuilt['total_rendered_speech_count']==308": "rebuilt['total_rendered_speech_count']==319",
    "rebuilt['typed_choice_count']==15": "rebuilt['typed_choice_count']==10",
    '                    rendered=painter(expanded)':
    "                    rendered=painter(expanded)\n                    rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)",
})
exec(compile(source, __file__ + '::stored-new-scope-plus-FE-row-membership', 'exec'), globals())
