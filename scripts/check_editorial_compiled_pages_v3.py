"""Add source-bound dynamic-role validation without weakening static speaker checks."""
from scripts import check_editorial_compiled_pages_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    '    args=parser.parse_args()':
        "    parser.add_argument('--role-bindings',type=Path)\n    args=parser.parse_args()",
    '    progressive_env=dict(progressive_expand.__globals__)\n    exec(compile(macros[\'source_owned_progressive_adapter\'],__file__+\'::original-macro-ABI\',\'exec\'),progressive_env)':
    """    dynamic_selectors={r['source_selector'] for r in doc['records'] if 207<=r['source_selector']<224}
    role_bindings={}
    if dynamic_selectors:
        assert args.role_bindings is not None
        role_proof=load(args.role_bindings);assert role_proof['runtime']==ctx.receipt()
        role_bindings={r['source_selector']:r['resolved_actor_ID'] for r in role_proof['native_roles']['rows']}
        assert dynamic_selectors<=set(role_bindings)
        source_roles={r['id']:r for r in role_proof['source_records']}
        for row in doc['records']:
            if row['source_selector'] not in dynamic_selectors:continue
            bound=source_roles[row['id']]
            assert row['source_reference']==bound['source_reference'] and row['source_complete_preamble_hex']==bound['source_complete_preamble_hex']
    macro_adapter=checked_text(macros['source_owned_progressive_adapter'],{
        'assert identity==prefix and captain==1':'assert captain==1 and identity==(prefix if prefix<207 else DYNAMIC_BINDINGS[prefix])',
    })
    progressive_env={**progressive_expand.__globals__,'DYNAMIC_BINDINGS':role_bindings}
    exec(compile(macro_adapter,__file__+'::same-native-macro-ABI-source-bound-role','exec'),progressive_env)""",
    '        FE_factory_calibration=calibration,fullwidth_Latin_not_introduced=True,':
        '        FE_factory_calibration=calibration,dynamic_role_bindings=role_bindings,source_owned_progressive_macro_adapter=macro_adapter,fullwidth_Latin_not_introduced=True,',
})
exec(compile(source,__file__+'::static-plus-qualified-dynamic-speakers','exec'),globals())
