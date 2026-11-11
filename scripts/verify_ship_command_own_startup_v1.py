"""Bind the exact ship-label candidate's own startup and protected name getters."""

from pathlib import Path
import sys

from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_ship_command_release_v1 import OUT


def main():
    mode = sys.argv.pop(1)
    assert not sys.argv[1:]
    if mode == 'render':
        from scripts.render_lil361_startup_v1 import source
        source = checked_text(source, {
            'work/lil361_B283_B298_release_v1': OUT.as_posix(),
            'Own Lil361 cumulative': 'Own ship-label cumulative',
        })
    elif mode == 'bind':
        source = checked_text(Path('scripts/bind_lil269_startup_visual_v1.py').read_text(encoding='utf-8'), {
            'work/lil269_B243_B282_release_v1': OUT.as_posix(),
            'No new Lil event activation or hardware coverage.': 'Hardware was unvisited.',
        })
    else:
        assert mode in ['verify', 'getters']
        from scripts.verify_lil361_startup_v1 import source
        source = checked_text(source, {
            'from scripts.build_registered_lil361_v1 import STAGED,STARTUP,GETTERS,PARENT,OUT,ARCHIVE':
                'from scripts.stage_ship_command_release_v1 import STAGED,STARTUP,GETTERS,PARENT,OUT,ARM\n'
                'from dk4tool.patch.ship_command_label_v1 import FIELD,NEW_POINTER,MARKET_FIELDS,NEW_FORMAT,transform',
            "assert [p for _,p,v in parent_image.iter_files() if image.read_file(p) != v] == [ARCHIVE]":
                "assert list(parent_image.iter_files()) == list(image.iter_files())",
            'assert all(image.read_file(p) == v for p,v in parent_image.iter_components())':
                "assert [p for p,v in parent_image.iter_components() if image.read_file(p) != v] == [ARM]\n"
                "    assert image.read_file(ARM) == transform(parent_image.read_file(ARM))[0]",
            "    save(STARTUP,dict(candidate=":
                """    visual_path = OUT/'own_startup_visual_v1/direct_visual_review.json'
    visual = load(visual_path)
    assert visual['all_six_original_captures_andexact_composite_directly_viewed']
    assert visual['selected_captures'] == selected and digest(visual['sheet']) == visual['sheet_sha256']
    assert int.from_bytes(raw[FIELD:FIELD+4], 'little') == NEW_POINTER
    assert all(int.from_bytes(raw[field:field+4], 'little') == NEW_FORMAT for field in MARKET_FIELDS)
    save(STARTUP,dict(candidate=""",
            'ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True':
                'only_owned_ARM9_label_data_changed_and_original_COMMON_HELP_font_exact=True,\n'
                'new_ship_andboth_preserved_market_pointers_present_in_actual_startup_WRAM=True',
            '[CAPTURE,plan_path,PARENT,old_report_path,Path(__file__)]':
                '[CAPTURE,plan_path,PARENT,old_report_path,visual_path,Path(__file__)]',
        })
        if mode == 'getters':
            sys.argv.append('--getters')
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})


if __name__ == '__main__':
    main()
