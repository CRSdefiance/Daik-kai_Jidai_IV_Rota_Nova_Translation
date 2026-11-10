"""Verify the sixteen scoped name labels on the exact Rafael4347 font."""
from pathlib import Path
import sys

from scripts import check_rafael_B301_B320_name_planes_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_rafael_B321_B331_contextual_v1 import INPUTS, LABELS
from scripts.plan_rafael_B321_B342_v1 import ROOT
from scripts.source_locked_derivation_v5118 import checked_text


BASE_ROOT = ROOT
BINDINGS_PATH = INPUTS[3]
NAMES = ROOT / 'progressive_name_decisions_v1.json'
RETAINED = ROOT / 'retained_name_planes_v1/native_name_planes.json'
TEMPLATE = previous.TEMPLATE
source = checked_text(previous.source, {
    "len(bound['name_bindings'])==19": "len(bound['name_bindings'])==16",
    "len(doc['records'])==19": "len(doc['records'])==16",
})


def prepare():
    assert not NAMES.exists()
    labels = load(LABELS)
    assert len(labels['records']) == 16
    rows = [{**row, 'english': row['approved_forms']['progressive-nameplate'],
             'source_reference': [field['source'] for field in row['source_andcurrent_fields']],
             'current_reference': [field['current'] for field in row['source_andcurrent_fields']]}
            for row in labels['records']]
    save(NAMES, {**labels, 'records': rows})


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        assert not sys.argv[1:]
        exec(compile(source, __file__ + '::same-complete-native-style11-proof', 'exec'), globals())
