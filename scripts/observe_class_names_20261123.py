"""Trace three remaining Japanese class names and their associated render calls."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_current_regional_orders_20261123 as regional
from scripts import observe_market_context_v2112 as native
from scripts import observe_online_gallery_common_v1 as playback
from scripts.reconcile_editorial_acceptance_20261123 import digest, read
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path(".codex-release-work/shared_display_20261123/native_class_names")
RELEASE = Path("releases/all_routes_editorial_20261123_supply_ratio_hint_candidate/verification/registered_release_verification.json")
GETTERS = {0x02021714: (0x02134444, (0x02134168,)),
           0x0202BFEC: (0x02134DA0, (0x02134D80,)),
           0x020CAF2C: (0x0215B6B8, (0x0215B4AC, 0x0215B710))}
PAINTER = 0x020D5404
ORDER = 0x0208AE5C


def observer(rom, folder):
    env = vars(native) | dict(ROOT=folder, ROM=rom, GETTERS=GETTERS, PAINTER=PAINTER,
        ORDER=ORDER, TARGETS=(*GETTERS, PAINTER, ORDER), __file__=__file__)
    setup = checked_text(getsource(native.prepare_contract), {"for pc in(REQUEST,FONT):": "for pc in TARGETS:"})
    exec(compile(setup, __file__ + "::interpreter-contract", "exec"), env)
    env["prepare_contract"]()
    source = getsource(native.Observer)
    start = source.index("    if frame<31000:return")
    end = source.index("   except BaseException as exc:", start)
    body = '''    owner=None;text=None
    if pc in GETTERS:
     text,classes=GETTERS[pc];owner=v[4]
     assert 0x02000000<=owner<0x023fff80
     vtable,=struct.unpack('<I',ct.string_at(self.wram+owner-0x02000000,4))
     assert vtable in classes
    elif pc==PAINTER:
     text=v[5]
     if all(text!=entry[0] for entry in GETTERS.values()):return
     vtable=None
    else:
     assert pc==ORDER
     vtable=None
    value=ct.string_at(self.wram+text-0x02000000,32).split(b'\\0',1)[0] if text else b''
    self.rows.append(dict(frame=frame,PC=pc,LR=v[18],object_address=owner,vtable=vtable,text_pointer=text,text_hex=value.hex()))
'''
    exec(compile(source[:start] + body + source[end:], __file__ + "::object-labels", "exec"), env)
    return env["Observer"]


def main():
    registered = read(RELEASE)
    assert digest("translations/release_stack.json") == registered["registry_sha256"]
    parent = SimpleNamespace(ROM=Path(registered["candidate"]), RELEASE=RELEASE)
    scope = vars(playback) | dict(ROOT=ROOT, parent=parent, observer=observer, FOCUS=set(),
                                  get_schedule=regional.schedule, __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + "::ordinary-regional-replay", "exec"), scope)
    scope["main"]("regional")


if __name__ == "__main__":
    main()
