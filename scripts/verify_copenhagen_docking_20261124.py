"""Verify the ordinary Copenhagen landing, its two prompts, and the native field writes."""

from types import FunctionType

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_copenhagen_docking_20261124 as played
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.reconcile_fleet_destination_writers_20261123 import ARM, BASE, code_at, get_machine, read_ram
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write


OUT = panels.OUT.with_name("copenhagen_docking_current_20261124.json")
COMMON = "/COMMON/MESFILE.DK4"
FLEET_SIZE = 132
PROMPTS = {
    65: (4000, "Copenhagen", "Gerhard Adernkatz", "Dock at Copenhagen?",
         "Gerhard asks permission to put into the port ahead. The direct question keeps the town substitution and leaves the decision to the player."),
    49: (4800, "172", "Port Worker", "Want to resupply for 172 gold?",
         "The Port Worker quotes the price as a straightforward offer. The reply accepts the precise amount displayed."),
}


def state(arm, snapshot):
    raw = read_ram(snapshot)
    cpu, call = get_machine(arm, raw)
    root = call(0xCB1A8)
    fleet_index = call(0x2E58C)
    assert call(0x7F244) == fleet_index == 1
    fleet = root + 4 + fleet_index * FLEET_SIZE
    docks = [raw[root - BASE + 4 + i * FLEET_SIZE + 0x3C] for i in range(64)]
    results = dict(fleet=fleet, own_fleet_index=fleet_index, fleet_root=root, docking_byte=docks[fleet_index],
        current_town=call(0xB65E4), docking_getter=call(0x34674, fleet), all_docking_bytes=docks, snapshot=snapshot)
    assert bytes(cpu.mem_read(BASE, len(raw))) == raw
    return results


def main():
    directory = played.ROOT / "landing"
    paths = [directory / p for p in ("capture/capture_report.json", "terminal.json", "requests.json", "source_contract.json", "inputs.json")]
    report, terminal, trace, contract, inputs = map(read, paths)
    release = read(played.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(played.current.ROM) == release["candidate_sha256"] == report["ROM_sha256"] == terminal["ROM_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    expected, frames, end, _, donor = played.schedule("landing")
    assert report["scripted_input_schedule"] == inputs == expected and report["frames"] == terminal["completed_frames"] == end
    assert report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"] == digest(played.DONOR)
    assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert all(digest(path) == value for path, value in terminal["evidence"].items())
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["rows"] == terminal["caption_calls"] and trace["source_requests"] == terminal["target_COMMON_calls"]
    assert trace["source_contract_sha256"] == digest(paths[3])
    snaps = {row["frame"]: row for row in report["read_only_capture_RAM_snapshots"]}
    captures = {row["frame"]: row for row in report["frames_captured"] if row["path"].endswith("_cold_boot.png")}
    assert set(frames) <= captures.keys() and set(frames) == snaps.keys()
    clean, installed = map(NdsImage.open, (CLEAN, played.current.ROM))
    ja, arm = [image.read_file(ARM) for image in (clean, installed)]
    assert contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    lo, hi = played.NATIVE_DOCK_STORE, played.NATIVE_DOCK_STORE + 4
    store = code_at(arm, lo, hi)
    assert store == code_at(ja, lo, hi) == code_at(read_ram(snaps[4400]), lo, hi)
    before, after = [state(arm, snaps[n]) for n in (4000, 4400)]
    assert before["fleet"] == after["fleet"] and before["docking_getter"] == 115
    assert after["docking_byte"] == after["docking_getter"] == after["current_town"] == 9
    actor, = [r for r in trace["rows"] if r["fleet"] == before["fleet"]]
    assert actor["PC"] == lo and actor["LR"] == 0x02034724 and 4001 <= actor["frame"] < 4400
    assert actor["before"] == before["docking_byte"] == 7 and actor["town"] == 9
    background = [r for r in trace["rows"] if r is not actor]
    assert len(background) == 21
    assert all(r["PC"] == lo and 0 <= r["town"] < 90 and (r["fleet"] - (before["fleet_root"] + 4)) % FLEET_SIZE == 0
               and 0 <= (r["fleet"] - (before["fleet_root"] + 4)) // FLEET_SIZE < 64 and r["frame"] < actor["frame"]
               for r in background)

    font = GameAsciiFont.from_arm9(arm)
    source = common_message_entries(clean.read_file(COMMON), ja)
    current = common_rows(installed.read_file(COMMON), arm)
    records = []
    for key, (frame, argument, speaker, english, reason) in PROMPTS.items():
        opening, copy = [r for r in trace["source_requests"] if r["message_ID"] == key]
        assert opening["PC"] == 0x0205528C and copy == opening | {"PC": 0x020534F4} and opening["frame"] < frame
        jp, en = source[key], current[key]
        assert jp.text.count(b"%s") == en.text.count(b"%s") == 1
        assert (en.text % argument.encode("ascii")).decode("ascii").strip() == english
        screen = panels.picture(captures[frame])
        ink = panels.exact_body(font, (english,), screen)
        name = panels.nameplate(font, speaker, screen)
        controls = [panels.find_mask(font, text, screen, region) for text, region in
                    (("No", (121, 358, 162, 377)), ("Yes", (191, 358, 233, 377)))]
        records.append(dict(id=f"COMMON_MESSAGE_{key}", Japanese=jp.text.decode("cp932"), english=english,
            speaker=speaker, context="Ordinary manual Copenhagen arrival, followed by the Port Worker's resupply offer.",
            decision="retention", rationale=reason, review=dict.fromkeys(GATES, True), runtime_argument=argument,
            source_reference=panels.text_reference(jp) | {"exact_hex": jp.text.hex()},
            installed_reference=panels.text_reference(en) | {"exact_hex": en.text.hex()},
            exact_body_ink_pixels=ink, complete_nameplate=name, complete_prompt_controls=controls,
            request=opening, capture=captures[frame]))
    town_names = [panels.find_mask(font, "Copenhagen", panels.picture(captures[n]), (0, 10, 255, 36))
                  for n in (4400, 5600)]
    balances = [panels.find_mask(font, amount, panels.picture(captures[n]), (74, 348, 138, 364))
                for n, amount in ((4400, "44147"), (5200, "43975"))]
    assert 44147 - 43975 == 172
    later_level_notices = [r for r in trace["source_requests"] if r["message_ID"] == 97]
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": OUT})
    display = sheets("copenhagen_dock_and_supplies", [(row["english"], panels.picture(row["capture"])) for row in records], (0, 265, 256, 376))
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], release=reference(played.current.RELEASE),
        original_donor=reference(played.DONOR), ordinary_gameplay=True, evidence=list(map(reference, (*paths, played.HISTORY, played.PROOF))),
        exact_original_docking_store=store.hex(), player_accepted_approach_store=actor, other_fleet_docking_stores=background,
        town_names=town_names, after_ordinary_approach=after, before_ordinary_approach=before, records=records,
        gold_change=172, confirmed_balances=balances, returned_to_town=captures[5600], figures=display,
        unrendered_in_captured_holds_level_up_requests=later_level_notices, new_editorial_credit=0, ROM_changed=False))
    print(f"Verified both complete prompts, the 172-gold deduction, the player docking in slot 9, and {len(background)} other fleet writes.")


if __name__ == "__main__":
    main()
