"""Check all335 stored bodies through the unchanged guarded pre-macro catalogue."""
from scripts.check_maria303_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/Maria_B58_B70_clean_20261109/':'work/Maria_B125_B136_clean_20261109/',
    '==299':'==335','all299_stored_effective_body_bindings.json':'all335_stored_effective_body_bindings.json',
    'all299_ordinary_and_style_bodies_checked':'all335_physical_bodies_checked',
    'no_code_font_orROM_changes=True,actual_gameplay=False':'no_code_font_orROM_changes=True,source_editorial_objects=337,body_count_excludes_two_captions=True,actual_gameplay=False',
    '299 stored ordinary and alternate-voice bodies pass':'335 physical bodies for337 source objects pass',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-source-buffer-SP-input-and4MiB-catalogue-guards','exec'),globals())
