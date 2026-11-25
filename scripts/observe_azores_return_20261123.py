"""Trace both ordinary Azores docking questions through their original name arguments."""

from argparse import ArgumentParser
from functools import partial
from inspect import getsource
from pathlib import Path
from struct import pack
from types import SimpleNamespace

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as observer
from scripts.probe_common_display_name_hook import branch_link
from scripts.reconcile_queued_sailing_hints_20261123 import RELEASE, REGISTRY, digest, read
from scripts.source_locked_derivation_v5118 import checked_text


VISIT = Path(".codex-release-work/shared_display_20261123/azores_developed_return/capture/capture_report.json")
VISIT_SHA = "72905582bc1993239899880b076349ee152b96b6614acd9684c995b9969f1374"
ROOT = VISIT.parents[2] / "azores_return_name_calls"
VILLAGE_NAME_RETURN = 0x0207895C
TOWN_NAME_CALL, TOWN_NAME_RETURN = 0x020790D0, 0x020790D4
TOWN_FORMAT_CALL = 0x020790E0
FRAMES = (8550, 13160, 13440, 13600, 13880, 15050, 15900, 16400, 17240, 17520, 17800, 18360)


def read_only_trace(rom, folder, expected):
    source = checked_text(getsource(observer.scoped_observer), {
        "'REQUESTS': REQUESTS}": "'REQUESTS': REQUESTS, 'WATCH': WATCH, 'TOWN_NAME_CALL': TOWN_NAME_CALL, "
            "'TOWN_FORMAT_CALL': TOWN_FORMAT_CALL, 'EXPECTED': EXPECTED}",
        "'for pc in REQUESTS:',": "'for pc in (*REQUESTS, *WATCH):',\n"
            "        'arm[at:at+4]==clean[at:at+4]': 'arm[at:at+4]==EXPECTED.get(pc,clean[at:at+4])',",
        '    self.requests.append(dict(frame=frame, PC=pc, message_ID=v[REQUESTS[pc]], caller_LR=v[18]))':
            '''    if pc in WATCH:
     if pc==TOWN_NAME_CALL:
      owner=v[4]
      vtable,=struct.unpack('<I',ct.string_at(self.wram+owner-0x02000000,4))
      self.rows.append(dict(frame=frame,PC=pc,object_address=owner,vtable=vtable,getter=v[5]))
      return
     at=v[6] if pc==TOWN_FORMAT_CALL else v[4]
     assert 0x02000000<=at<=0x023fff80
     text=ct.string_at(self.wram+at-0x02000000,64).split(bytes(1),1)[0]
     self.rows.append(dict(frame=frame,PC=pc,text_address=at,text_hex=text.hex(),LR=v[18]))
     return
    self.requests.append(dict(frame=frame, PC=pc, message_ID=v[REQUESTS[pc]], caller_LR=v[18]))''',
    })
    scope = vars(observer) | dict(WATCH=(VILLAGE_NAME_RETURN, TOWN_NAME_CALL, TOWN_NAME_RETURN, TOWN_FORMAT_CALL),
                                  TOWN_NAME_CALL=TOWN_NAME_CALL, TOWN_FORMAT_CALL=TOWN_FORMAT_CALL,
                                  EXPECTED=expected)
    exec(compile(source, __file__ + "::name-arguments", "exec"), scope)
    return scope["scoped_observer"](rom, folder)


def schedule(case):
    assert case in {"current", "revised"}
    assert digest(VISIT) == VISIT_SHA
    visit = read(VISIT)
    assert visit["cold_boot"] and not visit["savestate_loaded"]
    assert not any(value for key, value in visit.items() if key.startswith("synthetic_"))
    return visit["scripted_input_schedule"], FRAMES, visit["frames"], VISIT, visit["battery_save_preloaded"]


def main(stage=None):
    active = read(RELEASE)
    assert digest(REGISTRY) == active["registry_sha256"]
    case, selected = ("revised", stage) if stage else ("current", RELEASE)
    receipt = read(selected)
    expected = {}
    if stage:
        assert receipt["verified_predecessor_sha256"] == active["candidate_sha256"]
        assert receipt["added_call"] == TOWN_NAME_CALL
        expected[TOWN_NAME_CALL] = pack("<I", branch_link(TOWN_NAME_CALL, receipt["wrapper"]))
    rom = Path(receipt["candidate"])
    parent = SimpleNamespace(ROM=rom, RELEASE=selected)
    scope = vars(playback) | dict(parent=parent, ROOT=ROOT, observer=partial(read_only_trace, expected=expected),
                                  get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + "::ordinary-redocking", "exec"), scope)
    scope["main"](case)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--stage", type=Path)
    main(cli.parse_args().stage)
