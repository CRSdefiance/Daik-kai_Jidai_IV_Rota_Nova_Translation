"""Trace the special town-table object's own state in an ordinary Riga replay."""

from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import register_deck_skill_guidance_20261124 as current
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read

ROOT = current.ROM.parent.with_name("editorial_20261124_riga_port_trend")
HISTORY = current.build.ROOT / "riga/capture_report.json"
BASE, END = 0x02000000, 17600
OBJECT, FLEETS = 0x022D8DB0, 0x022D8DB8
OBJECT_TARGETS = (
    0x02021274, 0x0202BFDC, 0x0202BFEC, 0x0202C014, 0x0202C0DC, 0x0202C0EC,
    0x0202C134, 0x0205E4E0, 0x020B1C40, 0x020B1CA0, 0x020B1CB8, 0x020B6800,
)
WRITERS = (0x020347A4, 0x02035A28)
TARGETS = (*playback.REQUESTS, *OBJECT_TARGETS, *WRITERS)
FRAMES = (3200, 5200, 6000, 7600, 9600, 12000, 14800, 17420, END)


def schedule(case):
    report = read(HISTORY)
    recent = read(current.RELEASE)
    assert case == "riga" and report["ROM_sha256"] == recent["candidate_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    return report["scripted_input_schedule"], FRAMES, END, HISTORY, report["battery_save_preloaded"]


def observe(rom, folder):
    source = checked_text(getsource(playback.observer), {
        'REQUESTS=REQUESTS, ONLINE=ONLINE, GALLERY=GALLERY)':
            'REQUESTS=REQUESTS, ONLINE=ONLINE, GALLERY=GALLERY, OBJECT=OBJECT, BASE=BASE, OBJECT_TARGETS=OBJECT_TARGETS, WRITERS=WRITERS, __file__=__file__)',
        '    ptr=v[6]\n': '''    if pc in WRITERS:
     value = (v[5] if pc == 0x020347A4 else v[6]) & 255
     key = pc, v[18], value
     if key not in self.seen:
      self.seen.add(key)
      self.rows.append(dict(PC=pc, frame=frame, kind="fleet_byte", caller_LR=v[18], owner=v[4], value=value))
     return
    assert pc in OBJECT_TARGETS
    port, good = ct.string_at(self.wram + OBJECT - BASE + 4, 2)
    self.rows.append(dict(PC=pc, frame=frame, kind="special_object", caller_LR=v[18],
       registers_r0_to_r8=list(v[4:13]), port_field=port, good_field=good))
    return
    ptr=v[6]
''',
    })
    region = vars(playback) | dict(TARGETS=TARGETS, OBJECT_TARGETS=OBJECT_TARGETS, WRITERS=WRITERS,
        OBJECT=OBJECT, BASE=BASE, __file__=__file__)
    exec(compile(source, __file__ + "::port-trend-observer", "exec"), region)
    return region["observer"](rom, folder)


def main():
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(current.ROM) == release["candidate_sha256"]
    ROOT.mkdir()
    source = checked_text(getsource(playback.main), {
        "'--capture-at', *map(str, frames)]": "'--dump-capture-ram', '--capture-at', *map(str, frames)]",
    })
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, get_schedule=schedule, observer=observe,
        FOCUS={284, 318, 750, 751, 752}, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-riga-state", "exec"), scope)
    scope["main"]("riga")


if __name__ == "__main__":
    main()
