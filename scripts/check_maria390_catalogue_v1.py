"""Check all373 stored bodies through the same original guarded catalogue lookup."""
from scripts.check_maria337_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/Maria_B125_B136_clean_20261109/':'work/Maria_B152_B175_clean_20261109/',
    '==335':'==373','all335_stored_effective_body_bindings.json':'all373_stored_effective_body_bindings.json',
    'all335_physical_bodies_checked':'all373_physical_bodies_checked',
    'source_editorial_objects=337':'source_editorial_objects=390',
    'body_count_excludes_two_captions':'body_count_excludes17_captions',
    '335 physical bodies for337 source objects pass':'373 physical bodies for390 source objects pass',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-native-source-SP-canary-and4MiB-catalogue-guards','exec'),globals())
