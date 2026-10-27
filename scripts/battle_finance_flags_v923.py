"""Source-proven byte format4 with the additional observed native0C04 flags."""

import inspect
from pathlib import Path
from types import FunctionType
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_personal_gameplay_v841 as original
from scripts.battle_finance_layout_v920 import layout
from scripts.verify_village_wrap_v608 import read

SOURCE=Path('scripts/verify_personal_gameplay_v841.py')
SOURCE_SHA='bee09ebfe59293db935a895ede383a6f0310bd1aa4b1fbb44e5efc328ce628e3'
assert sha(SOURCE.read_bytes())==SOURCE_SHA


def format_instruction(arm):
    section=next(s for s in MainCodeFile(arm,0x02000000).sections if s.ramAddress<=0x01FF9344<s.ramAddress+len(s.data))
    at=0x01FF9344-section.ramAddress;return bytes(section.data[at:at+4])


def actual_view(raw):
    assert sha(SOURCE.read_bytes())==SOURCE_SHA
    text=inspect.getsource(original.actual_view);old='h[0] in (4,0x1404)'
    assert text.count(old)==1
    context={**original.actual_view.__globals__}
    exec(compile(text.replace(old,'h[0] in (4,0x1404,0x0E04,0x0C04)'),'<V923-observed-native0C04>','exec'),context)
    result=context['actual_view'](raw);assert result[3][0] in (4,0x1404,0x0E04,0x0C04)
    return result


hold=FunctionType(original.hold.__code__,{**original.hold.__globals__,'actual_view':actual_view,'layout':layout})


def provenance():
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    current=NdsImage.open('out/all_routes_combined_v922_candidate.nds').read_file('/__arm9__.bin')
    assert format_instruction(clean)==format_instruction(current)==bytes.fromhex('0000d6e5')
    return {'original_verifier':str(SOURCE),'original_verifier_sha256':SOURCE_SHA,
        'successor_sha256':sha(Path(__file__).read_bytes()),'original_format_read_address':0x01FF9344,
        'original_format_instruction_hex':'0000d6e5','original_instruction':'LDRB r0,[r6]',
        'only_observed0C04_added_to_prior4_1404_0E04_admission':True,
        'all_RTTI_geometry_kind_low_byte4_bitmap_RGB_and_guard_checks_preserved':True,
        'initial0C04_rejection_was_a_verifier_admission_limit_not_a_game_display_failure':True,
        'no_ROM_or_live_emulator_state_modified_by_verifier':True}
