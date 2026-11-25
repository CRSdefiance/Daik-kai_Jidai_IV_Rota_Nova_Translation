"""Check complete name planes while reusing only exact compatible cached strings."""
from pathlib import Path
from scripts import check_hodram_B251_B280_name_planes_v1 as previous
from scripts.review_hodram_B281_B300_names_v1 import ROOT,NATIVE,REVIEW
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'name_planes_v1';INPUT=ROOT/'name_plane_inputs_v1'
PRIOR=Path('work/Hodram_B251_B280_clean_20261107/name_planes_v1/native_name_planes.json')
RELEASE=Path('work/hodram_B251_B280_release_v1/registered_release_verification.json')
STARTUP=ROOT/'own_parent_startup_v1/own_route_context.json'
source=checked_text(previous.source,{
    "len(doc['records'])==len(bound['name_bindings'])==21":"len(doc['records'])==len(bound['name_bindings'])==18",
    'assert len(planes)==18 and fresh+reused==18':'assert len(planes)==17 and fresh+reused==17',
    'scoped_actors=21,distinct_strings=18':'scoped_actors=18,distinct_strings=17',
    "print(f'21actors/18strings:":"print(f'18actors/17strings:",
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-complete-name-pixels-and-exact-cache-reuse','exec'),env)
if __name__=='__main__':env['main']()
