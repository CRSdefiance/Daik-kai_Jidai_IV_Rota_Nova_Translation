"""Check all333 stored bodies through the original guarded catalogue lookup."""
from scripts.check_maria337_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/Maria_B125_B136_clean_20261109/':'work/Maria_B137_B151_clean_20261109/',
    '==335':'==333','all335_stored_effective_body_bindings.json':'all333_stored_effective_body_bindings.json',
    'all335_physical_bodies_checked':'all333_physical_bodies_checked',
    'source_editorial_objects=337':'source_editorial_objects=335',
    '335 physical bodies for337 source objects pass':'333 physical bodies for335 source objects pass',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-source-buffer-SP-canaries-and4MiB-native-catalogue-guards','exec'),globals())
