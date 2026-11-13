"""Check every stored body, compound object and relocated branch with unchanged native consumers."""
from scripts import check_hodram_B301_B310_stored_v1 as previous
from scripts.prepare_hodram_B311_B324_formatting_v1 import ROOT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text

compound_storage = previous.compound_storage
check_FE_rows = previous.check_FE_rows
source = checked_text(previous.source, {
    "rebuilt['style_physical_speech_count']==152": "rebuilt['style_physical_speech_count']==236",
    "rebuilt['total_rendered_speech_count']==225": "rebuilt['total_rendered_speech_count']==387",
    "rebuilt['typed_choice_count']==9": "rebuilt['typed_choice_count']==13",
    "ROOT/'native_resume_v3/compiled_native_pages.json'": "ROOT/'native_initial_v1/compiled_native_pages.json'",
    digest(previous.ROOT/'native_resume_v3/compiled_native_pages.json'):
        digest(ROOT/'native_initial_v1/compiled_native_pages.json'),
})
exec(compile(source, __file__+'::same-stored-native-glyph-pagination-and-branch-contract-new-scope', 'exec'), globals())
