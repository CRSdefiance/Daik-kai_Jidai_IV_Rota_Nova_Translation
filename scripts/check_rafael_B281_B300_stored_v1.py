"""Check rebuilt text, commands and original runtime display after storage parity."""
from scripts import check_rafael_B261_B280_stored_v2 as previous
from scripts.plan_rafael_B281_B300_v1 import MACROS
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous.source, {
    "len(own['three_logical_FI_records'])==3": "len(own['four_logical_macro_records'])==4",
    "'DYNAMIC_BINDINGS':native['dynamic_role_bindings']":
        "'DYNAMIC_BINDINGS':{int(selector): actor for selector, actor in native['dynamic_role_bindings'].items()}",
    "text['id']=='DK4_MES_B276_R0047'": "text['id']=='DK4_MES_B284_R0054'",
    "b'Your share in Hamburg rose slightly! '": "b'Your share in Malacca rose slightly! '",
    "len(rows)==114 and len(style_records)==rebuilt['style_physical_speech_count']==16":
        "len(rows)==164 and len(style_records)==rebuilt['style_physical_speech_count']==76",
    "styles['native_target_slot_cases']==16": "styles['native_target_slot_cases']==88",
    "rebuilt['total_rendered_speech_count']==130": "rebuilt['total_rendered_speech_count']==240",
    "fresh_pages+reused_pages==131": "fresh_pages+reused_pages==248",
})


if __name__ == '__main__':
    shared = previous.previous.previous
    storage = dict(shared.compound_storage.__globals__)
    exec(compile(shared.storage, __file__ + '::same-compound-storage', 'exec'), storage)
    env = {**shared.prior.env, 'compound_storage': storage['compound_storage'],
           'MACROS': MACROS, '__file__': __file__, '__name__': 'stored_B281_B300'}
    exec(compile(source, __file__ + '::exact-malacca-zero-ink-parity-scope', 'exec'), env)
    env['main']()
