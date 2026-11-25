"""Observe the native docking write and port dialogue during an ordinary approach."""

from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import register_tavern_buy_a_round_20261124 as current
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read


ROOT = Path(".codex-release-work/shared_display_20261123/copenhagen_docking_20261124")
HISTORY = Path("work/emulation_v193/copenhagen_arrival_v419/capture_report.json")
PROOF = Path("work/analysis/copenhagen_arrival_v419/arrival_reload_proof.json")
DONOR = Path("E:/Rota Nova translations/Saves/hodram-copenhagen-approach-v414.dsv")
FRAMES = (3200, 4000, 4400, 4800, 5200, 5600)
NATIVE_DOCK_STORE = 0x020347A4
TARGETS = (*playback.REQUESTS, NATIVE_DOCK_STORE)


def schedule(case):
    assert case == "landing"
    history, proof = map(read, (HISTORY, PROOF))
    assert digest(HISTORY) == proof["arrival_report_sha256"] and proof["normal_Copenhagen_arrival_and_resupply"]
    assert history["cold_boot"] and not history["savestate_loaded"] and not history["callback_errors"]
    assert not any(v for k, v in history.items() if k.startswith("synthetic_"))
    donor = history["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == digest(DONOR)
    end = FRAMES[-1] + 1
    inputs = [row for row in history["scripted_input_schedule"] if row["start"] < end]
    return inputs, FRAMES, end, HISTORY, donor | {"source": str(DONOR)}


def observer(rom, folder):
    source = checked_text(getsource(playback.observer), {
        "    ptr=v[6]\n": '''    if pc == NATIVE_DOCK_STORE:
     fleet=v[10]
     assert 0x02000000<=fleet<=0x023fffab
     value=ct.c_ubyte.from_address(self.wram+fleet-0x02000000+0x3c).value
     self.rows.append(dict(frame=frame,PC=pc,LR=v[18],fleet=fleet,before=value,town=v[9]&255))
     return
    ptr=v[6]
''',
        "REQUESTS=REQUESTS, ONLINE=ONLINE, GALLERY=GALLERY)":
            "REQUESTS=REQUESTS, ONLINE=ONLINE, GALLERY=GALLERY, NATIVE_DOCK_STORE=NATIVE_DOCK_STORE, __file__=__file__)",
    })
    context = vars(playback) | globals()
    exec(compile(source, __file__ + "::docking-field-observer", "exec"), context)
    return context["observer"](rom, folder)


def main():
    assert digest(REGISTRY) == read(current.RELEASE)["registry_sha256"]
    source = checked_text(getsource(playback.main), {
        "'--capture-at', *map(str, frames)]": "'--dump-capture-ram', '--capture-at', *map(str, frames)]",
    })
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, get_schedule=schedule,
        observer=observer, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-port-replay", "exec"), scope)
    scope["main"]("landing")


if __name__ == "__main__":
    main()
