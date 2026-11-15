"""Check stored native pages and every relocated branch with the qualified adapter."""
from scripts import check_hodram_B281_B300_stored_v1 as previous
from scripts.prepare_hodram_B301_B310_formatting_v1 import ROOT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text

compound_storage=previous.compound_storage
check_FE_rows=previous.check_FE_rows
source=checked_text(previous.source,{
    "rebuilt['style_physical_speech_count']==131":"rebuilt['style_physical_speech_count']==152",
    "rebuilt['total_rendered_speech_count']==373":"rebuilt['total_rendered_speech_count']==225",
    "rebuilt['typed_choice_count']==11":"rebuilt['typed_choice_count']==9",
    "ROOT/'native_resume_v2/compiled_native_pages.json'":"ROOT/'native_resume_v3/compiled_native_pages.json'",
    digest(previous.ROOT/'native_resume_v2/compiled_native_pages.json'):
        digest(ROOT/'native_resume_v3/compiled_native_pages.json'),
})
exec(compile(source,__file__+'::same-stored-glyph-pagination-and-branch-contract-new-scope','exec'),globals())
