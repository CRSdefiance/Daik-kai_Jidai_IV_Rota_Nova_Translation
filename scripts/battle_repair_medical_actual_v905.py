"""New layout with the unchanged,hash-bound original actual Cabin verifier."""

from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_personal_gameplay_v841 as original
from scripts.battle_personal_actual_v898 import actual_view
from scripts.battle_repair_medical_layout_v902 import layout
from scripts.verify_village_wrap_v608 import read

SOURCE=Path('scripts/verify_personal_gameplay_v841.py')
SOURCE_SHA='bee09ebfe59293db935a895ede383a6f0310bd1aa4b1fbb44e5efc328ce628e3'
PARENT=Path('scripts/battle_personal_actual_v898.py')
assert sha(SOURCE.read_bytes())==SOURCE_SHA
previous=Path('work/analysis/battle_personal_v898/actual_gameplay_verification.json')
closure=read('work/analysis/battle_personal_v898/registered_release_completion.json')
assert sha(previous.read_bytes())==closure['actual_gameplay_proof_sha256']
PARENT_SHA=read(previous)['original_consumer_scope']['successor_sha256']
assert sha(PARENT.read_bytes())==PARENT_SHA
hold=FunctionType(original.hold.__code__,{**original.hold.__globals__,'actual_view':actual_view,'layout':layout})


def provenance():
    assert sha(SOURCE.read_bytes())==SOURCE_SHA and sha(PARENT.read_bytes())==PARENT_SHA
    return {'original_verifier':str(SOURCE),'original_verifier_sha256':SOURCE_SHA,
        'observed_format_flag_successor':str(PARENT),'observed_format_flag_successor_sha256':PARENT_SHA,
        'layout':'scripts/battle_repair_medical_layout_v902.py','layout_sha256':sha(Path('scripts/battle_repair_medical_layout_v902.py').read_bytes()),
        'successor_sha256':sha(Path(__file__).read_bytes()),
        'all_original_RTTI_geometry_numeric_selection_bitmap_and_RGB_guards_retained':True}
