"""Preserve exact compiled-byte reuse andrefresh only changed pages with the explicit current ABI."""
from scripts import refresh_editorial_compiled_pages_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    '    args=parser.parse_args()':
        "    parser.add_argument('--captain',type=int,choices=range(4),required=True)\n    parser.add_argument('--macro-proof',type=Path,required=True)\n    parser.add_argument('--role-bindings',type=Path,required=True)\n    args=parser.parse_args()",
    '    runtime=previous[\'runtime\']':
        "    runtime=previous['runtime']\n    assert runtime['captain']==args.captain\n    assert load(args.macro_proof)['runtime']==load(args.role_bindings)['runtime']==runtime",
    "sum(r['source_macros'][key] for r in subset['records'])":
        "sum(r.get('source_macros',{}).get(key,0) for r in subset['records'])",
    "sys.executable,'scripts/check_editorial_compiled_pages.py',":
        "sys.executable,'scripts/check_editorial_compiled_pages_explicit_captain_v1.py',",
    "        '--release',runtime['release_proof'],'--startup',runtime['startup_proof'],":
        "        '--release',runtime['release_proof'],'--startup',runtime['startup_proof'],\n        '--captain',str(args.captain),'--macro-proof',str(args.macro_proof),'--role-bindings',str(args.role_bindings),",
})
exec(compile(source,__file__+'::same-all-byte-bindings-input-font-runtime-guards-refresh-only-changed-layouts','exec'),globals())
