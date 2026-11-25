"""Keep every native page guard while requiring current captain andmeasured default macros."""
from scripts import check_editorial_compiled_pages_v8 as previous
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.check_editorial_compiled_pages_v7 import validate_documented_layouts
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'from scripts.registered_editorial_runtime import RegisteredRuntime':
        'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    '    args=parser.parse_args()':
        "    parser.add_argument('--captain',type=int,choices=range(4),required=True)\n    parser.add_argument('--macro-proof',type=Path,required=True)\n    args=parser.parse_args()",
    'doc,plans,source,macros=map(load,[args.manuscript,args.plan,SOURCE,MACROS])':
        'doc,plans,source,macros=map(load,[args.manuscript,args.plan,SOURCE,args.macro_proof])',
    'ctx=RegisteredRuntime(args.release,args.startup)':
        "ctx=RegisteredRuntime(args.release,args.startup,captain=args.captain)\n    assert macros['runtime']==ctx.receipt()\n    defaults={k:v['text'] for k,v in macros['defaults'].items()}\n    assert {k:len(v) for k,v in defaults.items()}==macros['macro_ascii_lengths']\n    def expand_body(body):\n        for token,value in defaults.items():body=body.replace(token.encode(),value.encode())\n        return body\n    def expand_logical(text):\n        for token,value in defaults.items():text=text.replace('{MACRO:'+token+'}',value)\n        return text.replace('{LB}',' ')",
    "    macro_adapter=checked_text(macros['source_owned_progressive_adapter'],{\n        'assert identity==prefix and captain==1':'assert captain==1 and identity==(prefix if prefix<207 else DYNAMIC_BINDINGS[prefix])',\n    })":
        "    macro_adapter=macros['source_owned_progressive_adapter']\n    assert f'assert captain=={args.captain} and identity==(prefix if prefix<207 else DYNAMIC_BINDINGS[prefix])' in macro_adapter",
    '    painter,calibration=fe_factory(ctx.image)':
        "    if any(r['kind']=='system-FE' for r in doc['records']):\n        painter,calibration=fe_factory(ctx.image)\n    else:\n        painter,calibration=None,dict(not_executed_no_FE_records=True,no_FE_display_approval_inferred=True)",
    "expected=body.replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')":
        'expected=expand_body(body)',
    "logical=row['english'].replace('{LB}',' ').replace('{MACRO:FI}','Hodram').replace('{MACRO:FA}','Bergstrom').replace('{MACRO:FO}','Bergstrom Fleet')":
        "logical=expand_logical(row['english'])",
    'args.manuscript,args.plan,SOURCE,MACROS,':
        'args.manuscript,args.plan,SOURCE,args.macro_proof,',
})
exec(compile(source,__file__+'::same-native-code-pixels-consumption-canaries-pagination-explicit-captain-andmacros','exec'),globals())
