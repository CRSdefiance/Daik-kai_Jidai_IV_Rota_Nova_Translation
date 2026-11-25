"""Render retained nameplates with the proven style 11 consumer."""
from pathlib import Path
import sys

from scripts.qualify_rafael_plett_relocation_v1 import REFERENCE
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B261_B280_contextual_v1 import INPUTS, LABELS, ROOT, load, save, sha


TEMPLATE = Path('scripts/check_rafael_B61_B80_scoped_name_planes.py')
BASE_ROOT = ROOT
NAMES = ROOT / 'progressive_name_decisions_v1.json'
BINDINGS = INPUTS[3]
RETAINED = ROOT / 'retained_name_planes_v1/native_name_planes.json'
CORRECTED = REFERENCE / 'native_v1/native_name_fields_verification.json'
FINAL = ROOT / 'focused_name_planes_v1.json'


def prepare():
    assert not NAMES.exists()
    labels = load(LABELS)
    assert len(labels['records']) == 18
    rows = []
    for row in labels['records']:
        rows.append(dict(**row, english=row['approved_forms']['progressive-nameplate'],
            source_reference=[field['source'] for field in row['source_andcurrent_fields']],
            current_reference=[field['current'] for field in row['source_andcurrent_fields']]))
    save(NAMES, {**labels, 'records': rows})


def combine():
    assert not FINAL.exists()
    retained, corrected, decisions = map(load, (RETAINED, CORRECTED, NAMES))
    assert retained['scoped_actors'] == 16 and corrected['original_progressive_andfull_name_getters_pass']
    planes = retained['planes']
    for row in corrected['planes']:
        if row['version'] == 'proposed' and row['style'] == 11:
            assert row['complete_glyphs_bounds_andindependent_pixels_pass']
            assert sha(Path(row['plane']).read_bytes()) == row['plane_sha256']
            planes.append(dict(text=row['text'], native_plane=row['plane'], native_plane_sha256=row['plane_sha256'],
                preview=row['preview'], preview_sha256=row['preview_sha256']))
    assert {row['text'] for row in planes} == {row['english'] for row in decisions['records']}
    save(FINAL, {**retained, 'planes': planes, 'scoped_actors': 18, 'name_decisions': str(NAMES),
         'name_decisions_sha256': sha(NAMES.read_bytes()), 'corrected_name_receipt': str(CORRECTED),
         'corrected_name_receipt_sha256': sha(CORRECTED.read_bytes()),
         'retained_nameplanes_bound_to_parent_and_changed_names_to_exact_proposed_ARM9': True})


source = checked_text(TEMPLATE.read_text(encoding='utf-8'), {
    """    doc,bound,qual,prior=map(load,[NAMES,BINDINGS,QUAL,PRIOR])
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    assert qual['runtime']==ctx.receipt() and qual['previous_runtime']==bound['runtime']
    assert prior['proposed_ARM9_sha256']==sha(ctx.arm)
    assert len(doc['records'])==len(bound['name_bindings'])==22""":
        """    ROOT=RETAINED.parent
    NAMES=BASE_ROOT/'progressive_name_decisions_v1.json'
    BINDINGS=BINDINGS_PATH
    doc,bound=map(load,[NAMES,BINDINGS])
    runtime=doc['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=0)
    assert ctx.receipt()==runtime==bound['runtime']
    assert len(doc['records'])==len(bound['name_bindings'])==18
    doc['records']=[row for row in doc['records'] if row['decision']=='retention']
    assert len(doc['records'])==16""",
    "    assert not ROOT.exists()": "    assert not RETAINED.parent.exists()",
    "    cache={r['text']:deepcopy(r) for r in prior['planes']}": "    cache={}",
    'assert len(planes)==21 and fresh+reused==21': 'assert len(planes)==fresh==len({r["english"] for r in doc["records"]})',
    'scoped_actors=22,distinct_strings=21': 'scoped_actors=len(actors),distinct_strings=len(planes)',
    '[NAMES,BINDINGS,QUAL,PRIOR,RELEASE,Path(__file__)]': '[NAMES,BINDINGS,TEMPLATE,Path(__file__)]',
    "print(f'22actors/21strings:": "print(f'{len(actors)}actors/{len(planes)}strings:",
})


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    elif sys.argv[1:] == ['--combine']:
        combine()
    else:
        BINDINGS_PATH = BINDINGS
        exec(compile(source, __file__ + '::native-retained-style11', 'exec'), globals())
