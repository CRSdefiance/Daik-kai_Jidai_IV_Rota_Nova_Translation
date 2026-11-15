"""Check every stored page/object and relocated branch with unchanged native consumers."""
from scripts import check_hodram_B251_B280_stored_v1 as previous
from scripts.prepare_hodram_B281_B300_formatting_v1 import ROOT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text

compound_storage=previous.compound_storage
check_FE_rows=previous.check_FE_rows
source=checked_text(previous.source,{
    "rebuilt['style_physical_speech_count']==16":"rebuilt['style_physical_speech_count']==131",
    "rebuilt['total_rendered_speech_count']==209":"rebuilt['total_rendered_speech_count']==373",
    "rebuilt['typed_choice_count']==7":"rebuilt['typed_choice_count']==11",
    '727a3d43698883e1647a5c170c7c582ed0303160c1aef94688ed106feb9ea8b7':
        digest(ROOT/'native_resume_v2/compiled_native_pages.json'),
})
exec(compile(source,__file__+'::same-stored-native-glyph-and-branch-contract-new-scope','exec'),globals())
