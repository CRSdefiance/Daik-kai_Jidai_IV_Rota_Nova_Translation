"""Tie ordinary Square panels on the registered candidate to their exact COMMON bodies."""

from collections import Counter
from pathlib import Path

from scripts import observe_shared_town_dialogue_20261123 as runs
from scripts import pair_shared_display_20261123 as shared
from scripts import verify_ceuta_and_lisbon_20261122 as previous

base = runs.base
check, masks, town, visual = previous.check, previous.masks, previous.town, previous.visual
OUTPUT = shared.OUTPUT.parent / "ordinary_gameplay.json"
SQUARE = {
    656: "The terse reply explains what the player can buy at the counter.",
    657: "The sailor's question tag stays intact before the referral to the Market.",
    658: "The small talk answers the player without claiming that business is brisk.",
    689: "The Dutch speaker describes the Netherlands' recent independence in familiar terms.",
    727: "The rumor keeps Kurushima's interest in ironclad ships and attributes it to his defeat by Nobunaga.",
}
VISITS = {"amsterdam": ("Amsterdam", 10901), "nagasaki": ("Nagasaki", 5150), "athens": ("Istanbul", 2950)}


def load_visit(case, candidate):
    root = runs.ROOT / case
    report_path = root / "capture/capture_report.json"
    trace_path = root / "requests.json"
    terminal_path = root / "terminal.json"
    report, trace, terminal = map(base.load, (report_path, trace_path, terminal_path))
    inputs, _, end, history, donor = runs.schedule(case)
    assert report["ROM_sha256"] == terminal["ROM_sha256"] == candidate
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["frames"] == end and report["scripted_input_schedule"] == inputs
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    battery = report.get("battery_save_preloaded")
    if donor:
        assert battery["copied_byte_exact_before_cold_boot"] and battery["source_sha256"] == donor["source_sha256"]
    else:
        assert battery is None
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    requests = trace["source_requests"]
    assert requests == terminal["target_COMMON_calls"]
    assert all(base.digest(path) == digest for path, digest in terminal["evidence"].items())
    paired = []
    for getter, copy in zip(requests[::2], requests[1::2], strict=True):
        assert (getter["PC"], copy["PC"]) == (0x0205528C, 0x020534F4)
        assert dict(getter, PC=copy["PC"]) == copy
        paired.append((getter, copy))
    return check.shots(report), paired, dict(input_schedule=inputs, historical_input_reference=str(history),
        donor_sha256=battery["source_sha256"] if battery else None, recorded_frames=end,
        report_sha256=base.digest(report_path), trace_sha256=base.digest(trace_path),
        terminal_sha256=base.digest(terminal_path), observer_dependency_hashes=terminal["evidence"])


def verify():
    assert not OUTPUT.exists()
    registered, worklist = map(base.load, (runs.release.RELEASE, shared.OUTPUT))
    candidate = base.digest(runs.release.ROM)
    assert candidate == registered["candidate_sha256"] == worklist["candidate_sha256"]
    assert base.digest(town.CLEAN) == registered["clean_input_sha256"] == worklist["clean_sha256"]
    clean, current = map(base.NdsImage.open, (town.CLEAN, runs.release.ROM))
    arm, common = (current.read_file(file) for file in (town.ARM, town.COMMON))
    assert check.sha256(arm).hexdigest() == registered["target_ARM9_sha256"]
    assert check.sha256(common).hexdigest() == registered["target_COMMON_sha256"]
    japanese = check.common_message_entries(clean.read_file(town.COMMON), clean.read_file(town.ARM))
    english = shared.prior.entries(current)
    runtime = town.RegisteredRuntime(runs.release.RELEASE, registered["own_registered_startup"], captain=3)
    assert runtime.image.read_file(town.ARM) == arm and runtime.common == common
    cpu, _, _ = runtime.machine(arm, common, runtime.raw, runtime.plan)
    renderer, _, _ = town.font_tools(runtime.image)
    kanji = runtime.image.read_file("/GRP/KANJI.FNT")
    font = check.GameAsciiFont.from_arm9(arm)
    pending = {row["message_ID"] for row in worklist["records"]}
    results = {}
    for case, (city, location_frame) in VISITS.items():
        frames, paired, proof = load_visit(case, candidate)
        location = check.captured(frames[location_frame]).convert("RGB")
        pictures = [(f"{city} / location", location)]
        checked, other_requests = [], []
        for getter, copy in paired:
            key = getter["message_ID"]
            jp, en = japanese[key], english[key]
            source_current = dict(source_reference=check.reference(jp), current_reference=check.reference(en))
            if key not in SQUARE:
                other_requests.append(dict(requests=(getter, copy), **source_current))
                continue
            assert getter["caller_LR"] == 0x02053FF8 and b"%" not in jp.text and b"%" not in en.text
            frame = min(n for n in frames if 0 < n - getter["frame"] <= 160)
            held = frames[frame]
            picture = check.captured(held).convert("RGB")
            rendered, lines = town.native_layout(cpu, en.text, key, ())
            pixels, glyphs = town.render_portrait(renderer, arm, kanji, rendered)
            assert 1 <= len(lines) <= 4 and " ".join(lines) == " ".join(en.text.decode("ascii").split())
            assert [glyph["code"] for glyph in glyphs] == town.glyph_codes(rendered)
            assert masks.mask_check(bytes(pixels), 228, picture), (case, key, frame, lines)
            name_ink, name_bounds = check.complete_mask(font, "Shopkeeper", picture, 16, 277, (98, 97, 98))
            checked.append(dict(message_ID=key, requests=(getter, copy), capture=held,
                Japanese=jp.text.decode("cp932"), English=en.text.decode("ascii"), lines=lines,
                native_plane_sha256=check.sha256(bytes(pixels)).hexdigest(),
                nameplate=dict(text="Shopkeeper", pixels=name_ink, bounds=name_bounds),
                prior_text_retained=SQUARE[key], **source_current))
            pictures.append((f"{city} / COMMON {key} / frame {frame}", picture))
        counts = Counter(getter["message_ID"] for getter, _ in paired)
        sheets = []
        for start in range(0, len(pictures), 6):
            path, digest = visual.make_sheet(OUTPUT.parent / f"{city.lower()}_ordinary_{start // 6 + 1}.png",
                pictures[start:start + 6])
            sheets.append(dict(path=path, sha256=digest))
        results[city] = dict(trace_case=case, location=frames[location_frame], square_holds=checked,
            other_requests=other_requests, request_counts=counts, open_shared_requests=sorted(pending & counts.keys()),
            evidence_sheets=sheets, **proof)
    assert {city: len(visit["square_holds"]) for city, visit in results.items()} == {
        "Amsterdam": 3, "Nagasaki": 7, "Istanbul": 0}
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=worklist["clean_sha256"],
        ordinary_controller_and_touch=True, hardware=False, new_editorial_credit=0,
        shared_ownership_remaining=len(pending), visits=results))


if __name__ == "__main__":
    verify()
