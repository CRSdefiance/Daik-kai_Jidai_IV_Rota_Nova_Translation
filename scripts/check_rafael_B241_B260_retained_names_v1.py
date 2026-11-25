"""Render the nineteen retained public labels on their registered runtime."""
from scripts.check_rafael_B166_B167_scoped_name_planes_v1 import TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "    assert qual['runtime']==ctx.receipt()==bound['runtime'] and bound['exact_unchanged_actor0_macro_dependencies']":
        "    assert qual['runtime']==ctx.receipt()==bound['runtime'] and bound['exact_prior_ARM9_COMMON_actor_root_and_font']",
    "    assert len(doc['records'])==len(bound['name_bindings']) and {r['actor_ID'] for r in doc['records']}==set(bound['actors'])":
        """    changed = [r for r in doc['records'] if r['actor_ID']==186]
    assert len(changed)==1 and changed[0]['english']=='Francisca'
    assert {r['actor_ID'] for r in doc['records']}=={r['actor_ID'] for r in bound['name_bindings']}
    doc['records'] = [r for r in doc['records'] if r['actor_ID']!=186]
    assert len(doc['records'])==19""",
    'all_scoped_progressive_names_ASCII_complete_andfit_native216px':
        'all_retained_progressive_names_ASCII_complete_andfit_native216px',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::nineteen-retained-nameplanes', 'exec'), globals())
