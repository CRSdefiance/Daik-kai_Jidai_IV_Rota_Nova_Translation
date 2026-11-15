"""Keep all offline guards while selecting an explicit immutable formatting version."""
from scripts import approve_scoped_clean_offline_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    "    ap.add_argument('--mixed-visual',type=Path,required=True)":
        "    ap.add_argument('--mixed-visual',type=Path,required=True)\n    ap.add_argument('--formatting-root',type=Path,required=True)",
    "manuscript=root/'formatting_v1/formatting_input.json'":
        "manuscript=args.formatting_root/'formatting_input.json'",
    "macros=root/'formatting_v1/native_macro_measurements.json'":
        "macros=args.formatting_root/'native_macro_measurements.json'",
})

if __name__ == '__main__':
    env = {**previous.env, '__file__': __file__}
    exec(compile(source, __file__ + '::same-complete-native-visual-source-current-guards', 'exec'),
         env)
    env['main']()
