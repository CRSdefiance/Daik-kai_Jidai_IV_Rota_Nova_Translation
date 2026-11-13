"""Scoped actual Cabin checks admitting the observed native0E04 format flags."""

import inspect
from pathlib import Path
from types import FunctionType
from scripts import verify_personal_gameplay_v841 as original
from scripts.battle_personal_layout_v892 import layout
from dk4tool.patch.grand_race_menu_release import sha

SOURCE=Path('scripts/verify_personal_gameplay_v841.py')
SOURCE_SHA=''


def actual_view(raw):
    text=inspect.getsource(original.actual_view)
    old='h[0] in (4,0x1404)';new='h[0] in (4,0x1404,0x0E04)'
    assert text.count(old)==1
    context={**original.actual_view.__globals__}
    exec(compile(text.replace(old,new),'<V898-observed-native-format-flags>','exec'),context)
    result=context['actual_view'](raw)
    assert result[3][0] in (4,0x1404,0x0E04)
    return result


hold=FunctionType(original.hold.__code__,{**original.hold.__globals__,'actual_view':actual_view,'layout':layout})


def provenance():
    return {'original_verifier':str(SOURCE),'original_verifier_sha256':sha(SOURCE.read_bytes()),
        'successor_sha256':sha(Path(__file__).read_bytes()),
        'only_actual_view_header_admission_adds_observed0E04':True,
        'original01FF9344_LDRB_uses_low_byte4_format_as_in_existing_source_comment':True,
        'geometry_RTTI_pointer_span_and_complete_bitmap_RGB_checks_unchanged':True}
