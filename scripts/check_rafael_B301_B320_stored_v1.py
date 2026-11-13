"""Verify every stored page, typed object, and relocated branch under the original consumers."""
from scripts import check_rafael_B281_B300_stored_v1 as previous
from scripts.plan_rafael_B301_B320_v1 import MACROS
from scripts.source_locked_derivation_v5118 import checked_text


begin = previous.source.index("                        if text['id']=='DK4_MES_B284_R0054':")
last = "                            rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)"
end = previous.source.index(last, begin) + len(last)
source = checked_text(previous.source, {
    previous.source[begin:end]: "                        rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)",
    "len(own['four_logical_macro_records'])==4": "len(own['ten_logical_FI_records'])==10",
    "styles['native_target_slot_cases']==88": "styles['native_target_slot_cases']==152",
    "len(rows)==164 and len(style_records)==rebuilt['style_physical_speech_count']==76":
        "len(rows)==297 and len(style_records)==rebuilt['style_physical_speech_count']==145",
    "rebuilt['total_rendered_speech_count']==240": "rebuilt['total_rendered_speech_count']==442",
    "len(typed)==2 and sum(len(item['labels']) for item in typed)==rebuilt['typed_choice_count']==5":
        "len(typed)==5 and sum(len(item['labels']) for item in typed)==rebuilt['typed_choice_count']==11",
    '==[0x2100,0x2200]': '==[0x2100]*4+[0x2200]',
    'fresh_pages+reused_pages==248': 'fresh_pages+reused_pages==444',
    'typed_labels_checked=5': 'typed_labels_checked=11',
})


if __name__ == '__main__':
    shared = previous.previous.previous.previous
    storage = dict(shared.compound_storage.__globals__)
    exec(compile(shared.storage, __file__ + '::same-compound-storage', 'exec'), storage)
    env = {**shared.prior.env, 'compound_storage': storage['compound_storage'],
           'MACROS': MACROS, '__file__': __file__, '__name__': 'stored_B301_B320'}
    exec(compile(source, __file__ + '::all-stored-objects', 'exec'), env)
    env['main']()
