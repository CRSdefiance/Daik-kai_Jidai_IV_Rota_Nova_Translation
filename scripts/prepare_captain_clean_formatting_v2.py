"""Allow an explicit expanded name proof without replacing earlier bindings."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/prepare_captain_clean_formatting_v1.py').read_text(encoding='utf-8'), {
    "    ap.add_argument('--captain',type=int,choices=range(4),required=True)":
        "    ap.add_argument('--captain',type=int,choices=range(4),required=True)\n    ap.add_argument('--names',type=Path,required=True)",
    "namespath = args.root/'scoped_names_macros_reference_v1.json'":"namespath = args.names",
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-native-macro-source-prose-roles-andformatting-contract','exec'),globals())
