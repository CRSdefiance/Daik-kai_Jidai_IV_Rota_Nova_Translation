"""Verify stored dialogue, relative branches and native commands for B241–B260."""
from scripts.check_rafael_B221_B240_stored_v1 import prior, storage, compound_storage, source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "styles['native_target_slot_cases']==32": "styles['native_target_slot_cases']==16",
    "rebuilt['relative_sites']==34": "rebuilt['relative_sites']",
    "len(rows)==234 and len(style_records)==rebuilt['style_physical_speech_count']==29":
        "len(rows)==272 and len(style_records)==rebuilt['style_physical_speech_count']==14",
    "rebuilt['total_rendered_speech_count']==263": "rebuilt['total_rendered_speech_count']==286",
    "rebuilt['typed_choice_count']==7": "rebuilt['typed_choice_count']==6",
    "==[0x2100,0x2100,0x2200]": "==[0x2100]*3",
    "fresh_pages+reused_pages==279": "fresh_pages+reused_pages==294",
    'typed_labels_checked=7': 'typed_labels_checked=6',
})

if __name__ == '__main__':
    storage_env = dict(compound_storage.__globals__)
    exec(compile(storage, __file__+'::source-scope-neutral-storage', 'exec'), storage_env)
    env = {**prior.env, 'compound_storage': storage_env['compound_storage'], '__file__': __file__,
           '__name__': 'stored_B241_B260'}
    exec(compile(source, __file__+'::same-native-guards-with-five-compounds', 'exec'), env)
    env['main']()
