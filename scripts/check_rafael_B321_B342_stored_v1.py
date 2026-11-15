"""Verify every relocated body, voice table, caption and branch under native consumers."""
from scripts import check_rafael_B301_B320_stored_v1 as previous
from scripts.plan_rafael_B321_B342_v1 import MACROS
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous.source, {
    "identity['all_scoped_getters_fresh_on_registered_ARM9']":
        "identity['exact_prior_ARM9_COMMON_actor_root_and_font']",
    "len(own['ten_logical_FI_records'])==10": "len(own['eleven_logical_macro_records'])==11",
    "styles['native_target_slot_cases']==152": "styles['native_target_slot_cases']==384",
    "len(rows)==297 and len(style_records)==rebuilt['style_physical_speech_count']==145":
        "len(rows)==242 and len(style_records)==rebuilt['style_physical_speech_count']==298",
    "rebuilt['total_rendered_speech_count']==442": "rebuilt['total_rendered_speech_count']==540",
    "len(typed)==5 and sum(len(item['labels']) for item in typed)==rebuilt['typed_choice_count']==11":
        "len(typed)==7 and sum(len(item['labels']) for item in typed)==rebuilt['typed_choice_count']==16",
    '==[0x2100]*4+[0x2200]': '==[0x2100]*5+[0x2200]*2',
    'fresh_pages+reused_pages==444': 'fresh_pages+reused_pages==552',
    'typed_labels_checked=11': 'typed_labels_checked=16',
})


if __name__ == '__main__':
    shared = previous.previous.previous.previous.previous
    storage = dict(shared.compound_storage.__globals__)
    exec(compile(shared.storage, __file__ + '::same-source-bound-compound-storage', 'exec'), storage)
    env = {**shared.prior.env, 'compound_storage': storage['compound_storage'],
           'MACROS': MACROS, '__file__': __file__, '__name__': 'stored_B321_B342'}
    exec(compile(source, __file__ + '::same-native-stored-page-and-branch-guards', 'exec'), env)
    env['main']()
