"""Check ten distinct name strings for eleven scoped actors on the unchanged consumer."""
from pathlib import Path
from scripts import check_hodram_B301_B310_name_planes_v1 as wrapper
from scripts.review_hodram_B311_B324_names_v1 import ROOT, NATIVE, REVIEW
from scripts.source_locked_derivation_v5118 import checked_text

OUT = ROOT / 'name_planes_v1'
INPUT = ROOT / 'name_plane_inputs_v1'
PRIOR = Path('work/Hodram_B281_B300_clean_20261107/name_planes_v2/native_name_planes.json')
RELEASE = Path('work/hodram_B301_B310_release_v1/registered_release_verification.json')
STARTUP = ROOT / 'own_parent_startup_v1/own_route_context.json'
source = checked_text(wrapper.source, {
    "len(doc['records'])==len(bound['name_bindings'])==8": "len(doc['records'])==len(bound['name_bindings'])==11",
    'assert len(planes)==8 and fresh+reused==8': 'assert len(planes)==10 and fresh+reused==10',
    'scoped_actors=8,distinct_strings=8': 'scoped_actors=11,distinct_strings=10',
    "print(f'8actors/8strings:": "print(f'11actors/10strings:",
})
env = {**wrapper.env, **globals(), 'previous': wrapper.env['previous'], '__file__': __file__}
exec(compile(source, __file__ + '::same-native-name-glyph-checks-and-exact-cache-contract-new-scope', 'exec'), env)
if __name__ == '__main__':
    env['main']()
