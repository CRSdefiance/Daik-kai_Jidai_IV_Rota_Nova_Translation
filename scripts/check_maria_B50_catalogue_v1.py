"""Check all17 physical bodies without treating the FE child as another source credit."""
from scripts.check_maria301_stored_catalogue_v1 import source as previous,TEMPLATE
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/Maria_B0_B32_clean_20261109/stored_catalogue_all_v1':'work/Maria_B50_FE_resolution_20261109_v3/catalogue_v1',
    'work/Maria_B0_B32_clean_20261109/stored_v1/stored_native_verification.json':'work/Maria_B50_FE_resolution_20261109_v3/stored_v1/stored_native_verification.json',
    'work/Maria_B0_B32_clean_20261109/current_v1/current_effective.json':'work/Maria_B50_FE_resolution_20261109_v3/source_and_runtime_binding.json',
    '==299':'==17','all299_stored_effective_body_bindings.json':'all17_stored_effective_body_bindings.json',
    'all299_ordinary_and_style_bodies_checked':'all17_physical_bodies_checked',
    "    previous_aliases=[r['id'] for g in current['groups'] for r in g['records'] if r['current_catalogue_selected']]":
        """    original_current_path=Path('work/Maria_B37_B50_clean_20261109/current_v1/current_effective.json')
    original_current=load(original_current_path)
    previous_aliases=[r['id']+('_FE_PAGE_1' if r['id']=='DK4_MES_B50_R0043' else '') for g in original_current['groups'] if g['block']==50 for r in g['records'] if r['current_catalogue_selected']]""",
    '299 stored ordinary and alternate-voice bodies pass':'17 physical bodies for16 sources pass',
    'no_code_font_orROM_changes=True,actual_gameplay=False':'no_code_font_orROM_changes=True,source_editorial_objects=16,virtual_FE_continuation_not_another_source_credit=True,actual_gameplay=False',
    'STORED,CURRENT,TEMPLATE,Path(original.__file__)':'STORED,CURRENT,original_current_path,TEMPLATE,Path(original.__file__)',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-buffer-native-pre-macro-lookup-all17-physical-bodies','exec'),globals())
