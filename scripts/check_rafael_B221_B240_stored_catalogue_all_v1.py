"""Check the style alternatives as well as ordinary speech in the pre-macro catalogue."""
from scripts.check_rafael_B221_B240_stored_catalogue_v1 import TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "/stored_catalogue_v1')": "/stored_catalogue_all_v1')",
    """body=bytes.fromhex(item['stored_hex'])[1:]\\n""":
        """body=bytes.fromhex(item['stored_hex'])[0 if item.get('virtual_prefix_not_stored') else 1:]\\n""",
    "    rows=ctx.execute(env['native_lookup'],stored['records'])":
        "    inputs=stored['records']+stored['style_records']\n    rows=ctx.execute(env['native_lookup'],inputs)",
    "assert len(rows)==234 and {r['id'] for r in rows}=={r['id'] for r in stored['records']}":
        "assert len(rows)==len(inputs)==263 and {r['id'] for r in rows}=={r['id'] for r in inputs}",
    'all234_stored_effective_body_bindings.json': 'all263_stored_effective_body_bindings.json',
    'original_pre_macro_native_constants_preserved=True,':
        'original_pre_macro_native_constants_preserved=True, all263_ordinary_and_style_bodies_checked=True,',
    '234 stored story and town bodies pass': '263 stored ordinary and alternate-voice bodies pass',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::complete-pre-macro-catalogue-including-virtual-prefix-bodies', 'exec'), globals())

