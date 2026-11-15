"""Run unchanged native pre-macro catalogue guards on all310 stored bodies."""
from scripts.check_maria301_stored_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/Maria_B0_B32_clean_20261109/':'work/Maria_B51_B57_clean_20261109/',
    '==299':'==310',
    'all299_stored_effective_body_bindings.json':'all310_stored_effective_body_bindings.json',
    'all299_ordinary_and_style_bodies_checked':'all310_ordinary_bodies_checked',
    '299 stored ordinary and alternate-voice bodies pass':'310 stored ordinary bodies pass',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-native-buffers-input-SP-and4MiB-guards310','exec'),globals())
