"""Repeat the focused bubbles voyage from the previously verified starting position."""

from pathlib import Path

from scripts import replay_bubble_portrait_wraps_20261120 as earlier
from scripts.verify_personal_gameplay_v841 import get_machine


stage, base = earlier.stage, earlier.base
LIVE = stage.ROOT / 'focused_bubbles_anchored'
HISTORY = Path('work/sea_wrap_bubbles_v3/capture/capture_report.json')


def lead_position_offset(arm, raw):
    _, get = get_machine(arm, raw)
    assert get(0x7F244) == 1
    fleet = get(0xCB1A8) + 4 + 132 * get(0x2E58C)
    return get(0x36C70, fleet + 12) + 0x10 - earlier.prior.BASE


def set_condition(arm, raw, request):
    updated, receipt = earlier.set_condition(arm, raw, request)
    if request['mode'] != 'choose-bubbles':
        return updated, receipt
    old = base.load(HISTORY)
    source, = [row for row in old['read_only_pause_RAM_snapshots'] if row['frame'] == earlier.prior.PAUSE]
    anchor = Path(source['path']).read_bytes()
    assert source['read_only_export'] and base.digest(source['path']) == source['sha256']
    where = lead_position_offset(arm, raw)
    assert where == lead_position_offset(arm, anchor)
    assert raw[where - 16:where] == anchor[where - 16:where]
    assert raw[where + 8:where + 48] == anchor[where + 8:where + 48]
    positioned = updated[:where] + anchor[where:where + 8] + updated[where + 8:]
    changes = [dict(address=earlier.prior.BASE + i, before=raw[i], after=positioned[i])
               for i in range(where, where + 8) if raw[i] != positioned[i]]
    assert changes
    return positioned, receipt | dict(changes=receipt['changes'] + changes, voyage_coordinate_anchor=source)


if __name__ == '__main__':
    earlier.run(LIVE, 'from scripts.replay_bubble_portrait_anchored_20261120 import set_condition')
