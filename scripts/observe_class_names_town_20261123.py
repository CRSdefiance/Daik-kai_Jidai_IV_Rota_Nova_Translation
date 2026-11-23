"""Trace the town-name getter through the normal Lisbon Town Summary screen."""

from inspect import getsource
from types import SimpleNamespace

from scripts import observe_class_names_20261123 as labels
from scripts import observe_town_summary_20261119 as town_summary
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = labels.ROOT
TOWN_CALLS = {0x020B6058, 0x020C134C, 0x020A1458}
TOWN_PAINT_RETURNS = {0x020B6068, 0x020C1360, 0x020A1468}


def observer(rom, folder):
    source = checked_text(getsource(labels.observer), {
        "def observer(rom, folder):": "def town_observer(rom, folder):",
        "ORDER=ORDER, TARGETS=(*GETTERS, PAINTER, ORDER), __file__=__file__)":
            "ORDER=ORDER, TOWN_CALLS=TOWN_CALLS, TOWN_PAINT_RETURNS=TOWN_PAINT_RETURNS, "
            "TARGETS=(*GETTERS, PAINTER, *TOWN_CALLS), __file__=__file__)",
        "if all(text!=entry[0] for entry in GETTERS.values()):return":
            "if v[18] not in TOWN_PAINT_RETURNS and all(text!=entry[0] for entry in GETTERS.values()):return",
        "assert pc==ORDER\n     vtable=None":
            """assert pc in TOWN_CALLS
     owner=v[4];assert 0x02000000<=owner<0x023fff80
     vtable,=struct.unpack('<I',ct.string_at(self.wram+owner-0x02000000,4))""",
    })
    scope = vars(labels) | dict(TOWN_CALLS=TOWN_CALLS, TOWN_PAINT_RETURNS=TOWN_PAINT_RETURNS, __file__=__file__)
    exec(compile(source, __file__ + "::town-observer", "exec"), scope)
    return scope["town_observer"](rom, folder)


def main():
    release = labels.read(labels.RELEASE)
    assert labels.digest("translations/release_stack.json") == release["registry_sha256"]
    parent = SimpleNamespace(ROM=labels.Path(release["candidate"]), RELEASE=labels.RELEASE)
    playback = labels.playback
    scope = vars(playback) | dict(ROOT=ROOT, parent=parent, observer=observer, FOCUS=set(),
        get_schedule=town_summary.schedule, __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + "::ordinary-town-summary", "exec"), scope)
    scope["main"]("lisbon")


if __name__ == "__main__":
    main()
