"""Bind all330 stored physical bodies through the original guarded pre-macro lookup."""
from scripts.check_maria328_catalogue_v1 import TEMPLATE,source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/Maria_B73_B95_clean_20261109/':'work/Maria_B96_B124_clean_20261109/',
    '==314':'==330',
    'all314_stored_effective_body_bindings.json':'all330_stored_effective_body_bindings.json',
    'all314_physical_bodies_checked':'all330_physical_bodies_checked',
    "r['id']=='DK4_MES_B87_R0139'":"r['id'] in ['DK4_MES_B116_R0041','DK4_MES_B116_R0051']",
    'source_editorial_objects=328':'source_editorial_objects=330',
    '314 physical bodies for328 source objects pass':'330 physical bodies for330 source objects pass',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-buffer-SP-input-and4MiB-stored-catalogue-guards330','exec'),globals())
