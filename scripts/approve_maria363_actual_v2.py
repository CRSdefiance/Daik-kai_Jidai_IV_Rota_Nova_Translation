"""Account exactly for FE dismissal followed by a separately checked native menu."""
from scripts.approve_maria363_actual_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    """            if native_by_id[ident]['kind'] == 'system-FE':
                assert len(selected) == 1 and selected[0]['duration'] == 16""":
    """            if native_by_id[ident]['kind'] == 'system-FE':
                menu_between = [m for m in actual_menu['menus'] if m['preceding_speech'] == ident and m['following_speech'] == follow['id']]
                if menu_between:
                    exact = {(1,'DK4_MES_B221_R0011'):(8080,8320), (1,'DK4_MES_B221_R0143'):(11440,11680), (2,'DK4_MES_B221_R0011'):(26320,26560)}
                    assert len(menu_between) == 1 and len(selected) == 2
                    assert tuple(r['start'] for r in selected) == exact[(index,ident)]
                    assert all(r['duration'] == 16 for r in selected)
                    assert menu_between[0]['observed_default_return_A_input'] == selected[1]['start']
                    assert menu_between[0]['following_speech_frame'] == follow['frame']
                else:
                    assert len(selected) == 1 and selected[0]['duration'] == 16""",
    "'scripts/approve_maria305_actual_v1.py':digest('scripts/approve_maria305_actual_v1.py')}":
        "'scripts/approve_maria305_actual_v1.py':digest('scripts/approve_maria305_actual_v1.py'), 'scripts/approve_maria363_actual_v1.py':digest('scripts/approve_maria363_actual_v1.py')}",
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::exact-FE-dismissal-andmenu-A-intervals', 'exec'), globals())
