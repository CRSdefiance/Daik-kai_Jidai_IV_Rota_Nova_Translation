"""Check complete progressive name and role glyphs on Rafael3894."""
import sys

from scripts import check_rafael_B281_B300_retained_name_planes_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_rafael_B301_B320_contextual_v1 import NAME_REVIEW, NAMES as BINDINGS_PATH, ROOT
from scripts.source_locked_derivation_v5118 import checked_text


BASE_ROOT = ROOT
NAMES = ROOT / 'progressive_name_decisions_v1.json'
RETAINED = ROOT / 'retained_name_planes_v1/native_name_planes.json'
TEMPLATE = previous.TEMPLATE
source = checked_text(previous.source, {
    "len(bound['name_bindings'])==17": "len(bound['name_bindings'])==19",
    "len(doc['records'])==16": "len(doc['records'])==19",
})


def prepare():
    assert not NAMES.exists()
    labels = load(NAME_REVIEW)
    assert len(labels['records']) == 19
    rows = []
    for row in labels['records']:
        rows.append({**row, 'english': row['approved_forms']['progressive-nameplate'],
                     'source_reference': [field['source'] for field in row['source_andcurrent_fields']],
                     'current_reference': [field['current'] for field in row['source_andcurrent_fields']]})
    save(NAMES, {**labels, 'records': rows})


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        assert not sys.argv[1:]
        exec(compile(source, __file__ + '::native-retained-style11', 'exec'), globals())
