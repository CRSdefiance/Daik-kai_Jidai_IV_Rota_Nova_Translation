"""Bind the reviewed names and role labels to their original style-11 planes."""
import sys

from scripts import check_rafael_B261_B280_retained_name_planes_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_rafael_B281_B300_display_v1 import NAME as CORRECTED
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest as file_digest
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B281_B300_contextual_v1 import INPUTS, LABELS, ROOT


BASE_ROOT = ROOT
NAMES = ROOT / 'progressive_name_decisions_v1.json'
BINDINGS_PATH = INPUTS[3]
RETAINED = ROOT / 'retained_name_planes_v1/native_name_planes.json'
FINAL = ROOT / 'focused_name_planes_v1.json'
TEMPLATE = previous.TEMPLATE
source = checked_text(previous.source, {
    "len(bound['name_bindings'])==18": "len(bound['name_bindings'])==17",
})


def prepare():
    assert not NAMES.exists()
    labels = load(LABELS)
    assert len(labels['records']) == 17
    rows = []
    for row in labels['records']:
        rows.append({**row, 'english': row['approved_forms']['progressive-nameplate'],
                     'source_reference': [field['source'] for field in row['source_andcurrent_fields']],
                     'current_reference': [field['current'] for field in row['source_andcurrent_fields']]})
    save(NAMES, {**labels, 'records': rows})


def combine():
    assert not FINAL.exists()
    retained, corrected, decisions = map(load, (RETAINED, CORRECTED, NAMES))
    assert retained['scoped_actors'] == 16 and corrected['original_progressive_andfull_name_getters_pass']
    planes = list(retained['planes'])
    new, = [row for row in corrected['planes'] if row['version'] == 'proposed' and row['style'] == 11]
    assert new['complete_glyphs_bounds_andindependent_pixels_pass']
    assert file_digest(new['plane']) == new['plane_sha256']
    planes.append(dict(text=new['text'], native_plane=new['plane'], native_plane_sha256=new['plane_sha256'],
                       preview=new['preview'], preview_sha256=new['preview_sha256']))
    assert {row['text'] for row in planes} == {row['english'] for row in decisions['records']}
    save(FINAL, {**retained, 'planes': planes, 'scoped_actors': 17, 'name_decisions': str(NAMES),
         'name_decisions_sha256': file_digest(NAMES), 'corrected_name_receipt': str(CORRECTED),
         'corrected_name_receipt_sha256': file_digest(CORRECTED),
         'retained_nameplanes_bound_to_parent_and_changed_names_to_exact_proposed_ARM9': True})


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    elif sys.argv[1:] == ['--combine']:
        combine()
    else:
        exec(compile(source, __file__ + '::native-retained-style11', 'exec'), globals())
