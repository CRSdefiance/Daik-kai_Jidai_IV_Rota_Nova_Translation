"""Trace older fleet text owners during ordinary current-ROM regional orders."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_current_regional_orders_20261123 as regional
from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_market_context_v2112 as native
from scripts.reconcile_editorial_acceptance_20261123 import PACKAGE, digest, read
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path(".codex-release-work/shared_display_20261123/legacy_fleet_text")
RELEASE = PACKAGE / "verification/registered_release_verification.json"
TARGETS = {
    0x0203707C: "legacy_fleet_parent",
    0x02037138: "finance_parent_call",
    0x02037568: "target_city_owner",
    0x02037668: "target_city_format",
    0x02038D28: "finance_owner",
    0x02038DA8: "finance_format",
    0x0208AE5C: "regional_order_selection",
}


def observer(rom, folder):
    env = vars(native) | dict(ROOT=folder, ROM=rom, TARGETS=TARGETS, __file__=__file__)
    setup = checked_text(getsource(native.prepare_contract), {"for pc in(REQUEST,FONT):": "for pc in TARGETS:"})
    exec(compile(setup, __file__ + "::interpreter-contract", "exec"), env)
    env["prepare_contract"]()
    original = getsource(native.Observer)
    start = original.index("    if frame<31000:return")
    end = original.index("   except BaseException as exc:", start)
    body = '''    if pc in (0x02037668, 0x02038DA8):
     ptr=v[5];assert 0x02000000<=ptr<0x023fff80
     value=ct.string_at(self.wram+ptr-0x02000000,128).split(b'\\0',1)[0]
    else:
     ptr=None;value=b''
    # The fleet draw methods can run repeatedly while the menu is open.
    key=(pc, v[18], value, frame//100)
    if key in self.seen:return
    self.seen.add(key)
    self.rows.append(dict(frame=frame,PC=pc,owner=TARGETS[pc],LR=v[18],pointer=ptr,value_hex=value.hex()))
'''
    exec(compile(original[:start] + body + original[end:], __file__ + "::fleet-trace", "exec"), env)
    return env["Observer"]


def main():
    release = read(RELEASE)
    assert digest("translations/release_stack.json") == release["registry_sha256"]
    parent = SimpleNamespace(ROM=Path(release["candidate"]), RELEASE=RELEASE)
    scope = vars(playback) | dict(__file__=__file__, ROOT=ROOT, parent=parent, observer=observer,
                                  get_schedule=regional.schedule, FOCUS=set())
    exec(compile(getsource(playback.main), __file__ + "::ordinary-regional-replay", "exec"), scope)
    scope["main"]("regional")


if __name__ == "__main__":
    main()
