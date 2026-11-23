"""Trace the legacy fleet branches during the ordinary Fleet Info replay."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import observe_legacy_fleet_text_20261123 as legacy
from scripts import observe_online_gallery_common_v1 as playback
from scripts.observe_seoul_tavern_decline_20261123 import RELEASE
from scripts.replay_faction_information_20261115 import FLEET_REFERENCE
from scripts.stage_cartridge_title_20261123 import NdsImage, REGISTRY, digest, read, reference, write
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_plaque_release_v247 import find_mask


ROOT = Path("E:/Rota Nova translations/Generated/work/current_fleet_info_20261123")
OUT = Path("translations/editorial_checkpoints/shared_display_20261123/fleet_info_ordinary_20261123.json")
TARGETS = legacy.TARGETS | {
    0x0203FDD8: "information_menu",
    0x020406E4: "fleet_info_list",
    0x020407E0: "fleet_info_selected_detail",
    0x0208C308: "world_panel_fleet_dispatch",
    0x0208C33C: "world_panel_current_order_detail",
    0x0208C368: "world_panel_legacy_detail",
    0x02036DB8: "legacy_fleet_factory",
    0x0203D728: "legacy_total_power_field",
    0x0202BFEC: "missionary_name_getter",
}


def schedule(case):
    assert case == "fleet"
    previous = read(FLEET_REFERENCE)
    assert previous["cold_boot"] and not previous["savestate_loaded"] and not previous["callback_errors"]
    assert not any(value for key, value in previous.items() if key.startswith("synthetic_"))
    donor = previous["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    frames = (3200, 15600, 16000, 16400, 16800, 17000, 17100, 17200, 17400)
    return previous["scripted_input_schedule"], frames, 17401, FLEET_REFERENCE, donor


def main():
    release = read(RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"]
    parent = SimpleNamespace(ROM=Path(release["candidate"]), RELEASE=RELEASE)
    env = vars(legacy) | dict(ROOT=ROOT, TARGETS=TARGETS, __file__=__file__)
    exec(compile(getsource(legacy.observer), __file__ + "::fleet_info_trace", "exec"), env)
    scope = vars(playback) | dict(ROOT=ROOT, parent=parent, observer=env["observer"], get_schedule=schedule,
                                  FOCUS=set(), __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + "::fleet_info_controls", "exec"), scope)
    scope["main"]("fleet")


def verify():
    folder = ROOT / "fleet"
    paths = [folder / key for key in ("capture/capture_report.json", "terminal.json", "requests.json", "source_contract.json")]
    release = read(RELEASE)
    capture, terminal, trace, contract = map(read, paths)
    assert capture["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"] == digest(release["candidate"])
    assert digest(REGISTRY) == release["registry_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert not any(value for key, value in capture.items() if key.startswith("synthetic_"))
    schedule_bytes, holds, frames, source, donor = schedule("fleet")
    assert capture["frames"] == frames and capture["scripted_input_schedule"] == schedule_bytes
    assert capture["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["source_contract_sha256"] == digest(paths[-1])
    assert contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert {row["PC"] for row in contract["targets"]} == TARGETS.keys()
    rows = trace["rows"]
    assert rows == terminal["caption_calls"] and [r["PC"] for r in rows] == [
        0x0203FDD8, 0x0203FDD8, 0x020406E4, 0x020407E0, 0x02036DB8, 0x0203D728,
    ]
    assert rows[3]["frame"] == rows[4]["frame"] and rows[4]["LR"] == 0x020407E4
    seen = {r["frame"]: r for r in capture["frames_captured"] if not r["path"].endswith("_final.png")}
    assert set(holds) <= seen.keys()
    picture = captured(seen[17200])
    font = GameAsciiFont.from_arm9(NdsImage.open(release["candidate"]).read_file("/__arm9__.bin"))
    bounds = (
        ("Bergstrom Fleet", (0, 0, 256, 16)),
        ("Hodram Joakim Bergstrom", (72, 36, 256, 60)),
        ("Hodram Fleet", (0, 192, 256, 208)),
        ("Hodram Joakim Bergstrom", (72, 228, 256, 252)),
        ("Vestaros", (16, 288, 96, 310)),
    )
    glyphs = [find_mask(font, text, picture, region) for text, region in bounds]
    screen = OUT.with_suffix(".png")
    picture.save(screen)
    write(OUT, dict(registered_release=reference(RELEASE), candidate_sha256=release["candidate_sha256"],
                    previous_ordinary_controller_source=reference(source), exact_verified_donor=reference(donor["source"]),
                    run_evidence=[reference(p) for p in paths], ordinary_gameplay=True,
                    trace=rows, legacy_fleet_factory_reached=True,
                    observed_calls=dict(destination_formatter=0, finance_formatter=0, missionary_getter=0),
                    visible_title_and_name_masks=glyphs, visible_frame=seen[17200], copied_evidence=reference(screen),
                    limited_to_this_selected_fleet_and_display_path=True,
                    new_editorial_credit=0, ROM_changed=False, full_goal_complete=False))
    print("Ordinary Fleet Info reached the legacy builder and verified five complete caption and name masks.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--verify-only", action="store_true")
    if cli.parse_args().verify_only:
        verify()
    else:
        main()
