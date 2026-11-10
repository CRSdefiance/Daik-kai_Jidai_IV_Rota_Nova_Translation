"""Apply the unchanged stored-scene checks to the qualified B251-B280 scope."""
from scripts import check_hodram_B231_B250_stored_v1 as previous
from scripts.prepare_hodram_B251_B280_formatting_v1 import ROOT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text

compound_storage = previous.compound_storage
check_FE_rows = previous.check_FE_rows
source = checked_text(previous.source, {
    "rebuilt['style_physical_speech_count']==14": "rebuilt['style_physical_speech_count']==16",
    "rebuilt['total_rendered_speech_count']==223": "rebuilt['total_rendered_speech_count']==209",
    "rebuilt['typed_choice_count']==2": "rebuilt['typed_choice_count']==7",
    "ROOT/'native_initial_v1/compiled_native_pages.json'": "ROOT/'native_resume_v2/compiled_native_pages.json'",
    '89de39104208d8e5a9f72c5c88ff22b66f5bb655e551b8f81669d4b80141b0cb':
        '727a3d43698883e1647a5c170c7c582ed0303160c1aef94688ed106feb9ea8b7',
})
exec(compile(source, __file__ + '::same-stored-checks-new-qualified-scope', 'exec'), globals())
