"""Check every stored body,including physical style bodies whose selector lives inthe header."""
from scripts import check_qualified_rafael_stored_catalogue_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE=previous.TEMPLATE
source=checked_text(previous.source,{
    "body=bytes.fromhex(item['stored_hex'])[1:]":
        "body=bytes.fromhex(item['stored_hex']) if item.get('virtual_prefix_not_stored') else bytes.fromhex(item['stored_hex'])[1:]",
    "    rows=ctx.execute(env['native_lookup'],stored['records'])":
        "    items=[*stored['records'],*stored['style_records']]\n    rows=ctx.execute(env['native_lookup'],items)",
    "assert len(rows)==len(stored['records']) and {r['id'] for r in rows}=={r['id'] for r in stored['records']}":
        "assert len(rows)==len(items)==243 and {r['id'] for r in rows}=={r['id'] for r in items}",
    'all_new_effective_bodies_byte_exact_before_original_macro_expansion=True,':
        'all_new_effective_bodies_byte_exact_before_original_macro_expansion=True,all243_ordinary_andphysical_style_bodies_checked=True,virtual_style_selector_not_stripped_from_physical_bodies=True,',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-full-buffer-native-lookup-with-physical-style-body-ownership', 'exec'),globals())
