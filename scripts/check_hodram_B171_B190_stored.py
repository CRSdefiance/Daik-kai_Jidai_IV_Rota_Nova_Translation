"""Check stored parity, complete glyph rows and relocated native commands for this scope."""
from scripts import check_editorial_stored_batch_v4 as previous
from scripts.source_locked_derivation_v5118 import checked_text

compound_storage = previous.compound_storage
check_FE_rows = previous.check_FE_rows
source = checked_text(previous.source, {
    "rebuilt['style_physical_speech_count']==8": "rebuilt['style_physical_speech_count']==0",
    "rebuilt['total_rendered_speech_count']==319": "rebuilt['total_rendered_speech_count']==433",
    "rebuilt['typed_choice_count']==10": "rebuilt['typed_choice_count']==2",
})
exec(compile(source, __file__ + '::same-stored-native-consumers-current-complete-scope', 'exec'), globals())
