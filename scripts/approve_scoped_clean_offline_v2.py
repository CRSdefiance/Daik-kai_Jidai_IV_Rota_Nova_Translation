"""Keep all exact offline guards with an explicit mixed visual receipt."""
import inspect
from scripts import approve_scoped_clean_offline_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(inspect.getsource(previous.main), {
    '    args=ap.parse_args();root=args.root':
        "    ap.add_argument('--mixed-visual',type=Path,required=True)\n    args=ap.parse_args();root=args.root",
    "mixed=root/'mixed_visual_review_v1.json'":'mixed=args.mixed_visual',
    'exact_prior_native_slot_and27_compiler_negative_cases_reused':
        'exact_prior_native_slot_andcompiler_negative_cases_reused',
})
env = {**vars(previous), '__file__': __file__}
exec(compile(source,__file__+'::same-native-tile-selection-andcomplete-consumer-guards-explicit-visual-receipt','exec'),env)
if __name__=='__main__':
    env['main']()
