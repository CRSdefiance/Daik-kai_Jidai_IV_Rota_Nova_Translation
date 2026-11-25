"""Bind the final Lil261 plans to the viewed native pages and menu/name proofs."""

from scripts import approve_scoped_clean_offline_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text


if __name__ == '__main__':
    source = checked_text(previous.source, {
        "root/'compiled_styles_v1/compiled_style_objects.json'":
            "root/'style_native_final_v1/compiled_style_objects.json'",
    })
    env = {**previous.previous.env, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
