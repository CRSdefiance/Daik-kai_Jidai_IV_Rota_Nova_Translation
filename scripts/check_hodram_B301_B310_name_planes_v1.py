"""Paint eight scoped name strings, reusing only byte-compatible cached planes."""
from pathlib import Path
from scripts import check_hodram_B251_B280_name_planes_v1 as wrapper
from scripts.review_hodram_B301_B310_names_v1 import ROOT,NATIVE,REVIEW
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'name_planes_v1';INPUT=ROOT/'name_plane_inputs_v1'
PRIOR=Path('work/Hodram_B281_B300_clean_20261107/name_planes_v2/native_name_planes.json')
RELEASE=Path('work/hodram_B281_B300_release_v1/registered_release_verification.json')
STARTUP=ROOT/'own_parent_startup_v1/own_route_context.json'
source=checked_text(wrapper.source,{
    "len(doc['records'])==len(bound['name_bindings'])==21":"len(doc['records'])==len(bound['name_bindings'])==8",
    'assert len(planes)==18 and fresh+reused==18':'assert len(planes)==8 and fresh+reused==8',
    'scoped_actors=21,distinct_strings=18':'scoped_actors=8,distinct_strings=8',
    "print(f'21actors/18strings:":"print(f'8actors/8strings:",
})
env={**wrapper.env,**globals(),'previous':wrapper.env['previous'],'__file__':__file__}
exec(compile(source,__file__+'::same-complete-native-name-glyph-and-cache-contract','exec'),env)
if __name__=='__main__':env['main']()
