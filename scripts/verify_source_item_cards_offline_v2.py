"""Verify the item geometry using the current ROM's source-identical overlay."""

import inspect
from pathlib import Path

from ndspy.code import loadOverlayTable

from scripts import probe_item_parent_crops as crops
from scripts import probe_item_source_canvas as canvas
from scripts import stage_source_item_cards_and_coin_v1 as stage
from scripts.source_locked_derivation_v5118 import checked_text


def parent_crops(arm):
    source, current = map(stage.NdsImage.open, ('work/clean.nds', stage.ROM))
    old, new = (loadOverlayTable(image.rom.arm9OverlayTable, lambda oid, fid: image.files[fid])
                for image in (source, current))
    assert old.keys() == new.keys() == {0}
    assert old[0].ramAddress == new[0].ramAddress and bytes(old[0].data) == bytes(new[0].data)
    original = checked_text(inspect.getsource(canvas.source_canvas), {
        "NdsImage.open('out/all_routes_combined_v158_candidate.nds')": 'current_rom',
    })
    env = vars(canvas) | {'current_rom': current}
    exec(compile(original, __file__ + '::source-identical-current-overlay', 'exec'), env)
    env = vars(crops) | {'source_canvas': env['source_canvas']}
    exec(compile(inspect.getsource(crops.verify), __file__ + '::original-item-parent-crops', 'exec'), env)
    return env['verify'](arm)


def main():
    source = checked_text(inspect.getsource(stage.offline), {
        'Path(make_execute.__code__.co_filename))': 'Path(make_execute.__code__.co_filename), Path(__file__))',
    })
    env = vars(stage) | globals()
    exec(compile(source, __file__ + '::item-offline-current-overlay', 'exec'), env)
    env['offline']()


if __name__ == '__main__':
    main()

