"""Apply the qualified offline approval to the final Lil menu and style receipts."""

from scripts import approve_scoped_clean_offline_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    source = checked_text(previous.source, {
        "menu=root/'menu_native_v1/group_verification.json'": "menu=root/'menu_native_v2/group_verification.json'",
        "styles=root/'compiled_styles_v1/compiled_style_objects.json'":
            "styles=root/'style_native_final_v1/compiled_style_objects.json'",
    })
    env = {**previous.previous.env, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
