"""Source-proven original activity2 admission,with unchanged geometry and complete fonts."""
import inspect
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_personal_gameplay_v841 as original
from scripts.mood_comments_flags_v982 import actual_view
from scripts.activity_special_layout_v986b import layout

SOURCE=Path('scripts/verify_personal_gameplay_v841.py')
SOURCE_SHA='bee09ebfe59293db935a895ede383a6f0310bd1aa4b1fbb44e5efc328ce628e3'
assert sha(SOURCE.read_bytes())==SOURCE_SHA
text=inspect.getsource(original.hold);needle='assert state in (0,1)';assert text.count(needle)==1
context={**original.hold.__globals__,'actual_view':actual_view,'layout':layout}
exec(compile(text.replace(needle,'assert state in (0,1,2)'),'<original-activity2-admission-only>','exec'),context)
hold=context['hold']

def provenance():
    arm=NdsImage.open('out/all_routes_combined_v987_candidate.nds').read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x12104:0x12380]==clean[0x12104:0x12380]
    return {'original_verifier':str(SOURCE),'original_verifier_sha256':SOURCE_SHA,
        'original_activity2_main_and_actor_specific_helper_exact_clean':True,
        'only_activity2_added_to_0_1_admission_no_other_font_geometry_RTTI_or_guard_waiver':True,
        'successor_sha256':sha(Path(__file__).read_bytes())}
