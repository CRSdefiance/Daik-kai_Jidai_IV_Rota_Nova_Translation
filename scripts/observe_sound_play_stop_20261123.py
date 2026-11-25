"""Follow the Play and Stop text choices through ordinary Sound Setup controls."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_market_context_v2112 as native
from scripts import observe_online_gallery_common_v1 as playback
from scripts.reconcile_editorial_acceptance_20261123 import digest, read
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path(".codex-release-work/sound_play_stop_20261123")
RELEASE = Path("releases/all_routes_editorial_20261123_pirate_affiliation_candidate/verification/registered_release_verification.json")
STOP, PLAY = 0x02107FC0, 0x02107FE0
TARGETS = {STOP, PLAY}
FRAMES = (2650, 3200, 3310, 3500, 3900, 4150, 4510, 4650, 4850, 5100, 5490, 5800)


def schedule(case):
    assert case in ("current", "staged")
    controls = [(1601, "START"), (2101, "DOWN"), (2401, "A"), (2801, "A"), (3301, "A"),
                (3851, "A"), (4201, "DOWN"), (4451, "A"), (4701, "RIGHT"), (4901, "A"),
                (5301, "B"), (5601, "B")]
    events = [dict(start=n, duration=8, buttons=[key]) for n, key in controls]
    return events, FRAMES, FRAMES[-1], None, None


def observer(rom, folder):
    env = vars(native) | dict(ROOT=folder, ROM=rom, TARGETS=TARGETS, __file__=__file__)
    setup = checked_text(getsource(native.prepare_contract), {"for pc in(REQUEST,FONT):": "for pc in TARGETS:"})
    exec(compile(setup, __file__ + "::sound-controls-contract", "exec"), env)
    env["prepare_contract"]()
    original = getsource(native.Observer)
    start = original.index("    if frame<31000:return")
    end = original.index("   except BaseException as exc:", start)
    body = '''    ptr=v[4]
    assert ptr in (0x02170280, 0x02170288)
    address=v[18]
    assert 0x02000000<=address<0x023ffc1c
    playing,=struct.unpack('<I',ct.string_at(self.wram+address+0x11c-0x02000000,4))
    value=ct.string_at(self.wram+ptr-0x02000000,8).split(b'\\0',1)[0]
    key=(pc,value,playing)
    if key!=self.last:
     self.rows.append(dict(frame=frame,PC=pc,pointer=ptr,text_hex=value.hex(),playing=playing))
     self.last=key
'''
    exec(compile(original[:start] + body + original[end:], __file__ + "::observe-play-stop", "exec"), env)
    return env["Observer"]


def main(case):
    parent = read(RELEASE)
    assert digest("translations/release_stack.json") == parent["registry_sha256"]
    source = RELEASE if case == "current" else ROOT / "staged_rom/stored_proof.json"
    target = read(source)
    assert case == "current" or parent["candidate_sha256"] == target["predecessor_sha256"]
    release = SimpleNamespace(ROM=Path(target["candidate"]), RELEASE=source)
    env = vars(playback) | dict(__file__=__file__, ROOT=ROOT, parent=release, observer=observer,
                                get_schedule=schedule, FOCUS=set())
    exec(compile(getsource(playback.main), __file__ + "::ordinary-sound-controls", "exec"), env)
    env["main"](case)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("current", "staged"))
    main(parser.parse_args().case)
