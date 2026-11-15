"""Paint newly scoped name strings and reuse exact compatible native planes."""
import inspect
from pathlib import Path
from scripts import check_hodram_B231_B250_name_planes_v1 as wrapper
from scripts.review_hodram_B251_B280_names_v1 import ROOT,NATIVE,REVIEW
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'name_planes_v1';INPUT=ROOT/'name_plane_inputs_v1'
PRIOR=Path('work/Hodram_B231_B250_clean_20261107/name_planes_v1/native_name_planes.json')
RELEASE=Path('work/hodram_B231_B250_release_v1/registered_release_verification.json')
STARTUP=ROOT/'own_parent_startup_v1/own_route_context.json'
source=checked_text(inspect.getsource(wrapper.main),{
    "len(doc['records'])==len(bound['name_bindings'])==19":"len(doc['records'])==len(bound['name_bindings'])==21",
    'assert len(planes)==19 and fresh+reused==19':'assert len(planes)==18 and fresh+reused==18',
    'scoped_actors=19,distinct_strings=19':'scoped_actors=21,distinct_strings=18',
    "print(f'19actors/19strings:":"print(f'21actors/18strings:",
})
env={**vars(wrapper),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-complete-name-pixels-and-exact-cache-reuse','exec'),env)
if __name__=='__main__':env['main']()
