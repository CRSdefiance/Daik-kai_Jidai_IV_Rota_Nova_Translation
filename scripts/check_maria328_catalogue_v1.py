"""Bind every physical body through the original pre-macro lookup, counting its owner once."""
from scripts.check_maria301_stored_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/Maria_B0_B32_clean_20261109/':'work/Maria_B73_B95_clean_20261109/',
    '==299':'==314',
    'all299_stored_effective_body_bindings.json':'all314_stored_effective_body_bindings.json',
    'all299_ordinary_and_style_bodies_checked':'all314_physical_bodies_checked',
    "previous_aliases=[r['id'] for g in current['groups'] for r in g['records'] if r['current_catalogue_selected']]":
        "previous_aliases=[r['id']+('_FE_PAGE_1' if r['id']=='DK4_MES_B87_R0139' else '') for g in current['groups'] for r in g['records'] if r['current_catalogue_selected']]",
    'no_code_font_orROM_changes=True,actual_gameplay=False':'no_code_font_orROM_changes=True,source_editorial_objects=328,FE_child_not_another_source_credit=True,actual_gameplay=False',
    '299 stored ordinary and alternate-voice bodies pass':'314 physical bodies for328 source objects pass',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-buffer-SP-input-and4MiB-lookup-guards-all314-bodies','exec'),globals())
