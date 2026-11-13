"""Run both original name consumers and native glyph checks for both surnames."""
import inspect
from pathlib import Path
import sys

from scripts.prove_lil_B167_names_v4124b import names
from scripts.qualify_rafael_plett_relocation_v1 import REFERENCE
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B261_B280_contextual_v1 import LABELS, load, save


TEMPLATE = Path('scripts/check_owned_name_fields.py')
BINDING = REFERENCE / 'current_getters.json'
source = checked_text(TEMPLATE.read_text(encoding='utf-8'), {
    'from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields':
        'from scripts.qualify_rafael_plett_relocation_v1 import plan_surnames as plan_arm9_name_fields',
    "other=deepcopy(proposal);a,c=arm,clean;f=other['fields'][0]":
        "other=deepcopy(proposal);a,c=arm,clean;f=other['fields'][1]",
    "Path('dk4tool/patch/owned_name_fields_v2.py'),Path(__file__)":
        "Path('dk4tool/patch/owned_name_fields_v2.py'),Path('scripts/qualify_rafael_plett_relocation_v1.py'),TEMPLATE,Path(__file__)",
})


def prepare():
    assert not BINDING.exists()
    labels = load(LABELS)
    proposal = load(REFERENCE/'proposal.json')
    assert labels['runtime'] == proposal['runtime']
    current = [getter for row in labels['records'] if row['actor_ID'] in (65, 68)
               for getter in row['current_consumers']]
    assert len(current) == 4
    adapter = checked_text(inspect.getsource(names), {'for ident in [2,4,13,23,109]:': 'for ident in ACTORS:'})
    save(BINDING, dict(runtime=labels['runtime'], current_names=dict(rows=current), source_owned_current_adapter=adapter))


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        exec(compile(source, __file__ + '::same-native-constructor-and-glyph-plane-checks', 'exec'), globals())
