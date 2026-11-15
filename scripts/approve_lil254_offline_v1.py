"""Select the final Lil B312–B319 native and visual receipts."""

from scripts import approve_scoped_clean_offline_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text


if __name__ == '__main__':
    source = checked_text(previous.source, {
        "root/'native_final_selection_v1/resume_selection.json'":
            "root/'native_final_selection_v2/resume_selection.json'",
        "root/'compiled_styles_v1/compiled_style_objects.json'":
            "root/'style_native_final_v1/compiled_style_objects.json'",
    })
    env = {**previous.previous.env, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
