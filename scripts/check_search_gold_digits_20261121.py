"""Verify source-bound Search dialogue, amount, and live glyphs across both ROMs."""

from pathlib import Path
from struct import unpack_from
from unicodedata import normalize

from PIL import Image, ImageChops, ImageDraw

from scripts import replay_search_gold_20261121 as replay


stage, base = replay.stage, replay.base
PROOF = stage.ROOT / "verified_gameplay.json"
SHEET = stage.ROOT / "search_gold_live.png"
REPORT = 2316
HOLDS = (5500, 5600)


def main():
    assert not PROOF.exists()
    folders = [stage.ROOT / name for name in ("search_gold_before", "search_gold_after")]
    paths = [folder / "capture/capture_report.json" for folder in folders]
    reports = list(map(base.load, paths))
    staged = base.load(stage.PROOF)
    assert [r["ROM_sha256"] for r in reports] == [staged["parent_sha256"], staged["candidate_sha256"]]
    assert base.digest(stage.ROM) == staged["candidate_sha256"]
    assert all(r["cold_boot"] and r["frames"] == HOLDS[-1] and not r["savestate_loaded"] and not r["callback_errors"]
               for r in reports)
    for key in ("core_DLL_sha256", "core_options", "scripted_input_schedule"):
        assert reports[0][key] == reports[1][key]
    inputs, terrain = [[folder / name for folder in folders] for name in ("inputs.json", "terrain.json")]
    assert base.digest(inputs[0]) == base.digest(inputs[1]) and base.digest(terrain[0]) == base.digest(terrain[1])
    for field in ("source", "source_sha256", "copied_byte_exact_before_cold_boot"):
        assert reports[0]["battery_save_preloaded"][field] == reports[1]["battery_save_preloaded"][field]
    fixtures = [r["synthetic_battle_recovery_proximity_fixtures"][0] for r in reports]
    first = {k: v for k, v in fixtures[0].items() if not k.endswith("_sha256")}
    second = {k: v for k, v in fixtures[1].items() if not k.endswith("_sha256")}
    assert first == second and first["owned_bytes"] == 48 and first["stats_and_event_state_untouched"]
    assert first["frame"] == 5000

    pictures = [{r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_navigation.png")}
                for report in reports]
    assert pictures[0].keys() == pictures[1].keys()
    shared = stage.rewards.shared
    cases = [base.NdsImage.open(path) for path in (stage.parent.ROM, stage.ROM)]
    arms, values, wallets = [], [], []
    for image, report in zip(cases, reports, strict=True):
        arm = image.read_file(shared.ARM)
        ram = report["read_only_RAM_snapshot"]
        assert ram["read_only_export"] and base.digest(ram["path"]) == ram["sha256"]
        raw = Path(ram["path"]).read_bytes()
        buffers = unpack_from("<2I", arm, 0x54890)
        fields = [raw[addr - replay.BASE:addr - replay.BASE + 256].split(b"\0", 1)[0] for addr in buffers]
        assert fields[0] == fields[1]
        arms.append(arm)
        values.append(fields[0])
        _, get = replay.get_machine(arm, raw)
        at = get(0xCB160) + 4 + 76 * get(0x397D8) + 0xC - replay.BASE
        wallets.append(unpack_from("<I", raw, at)[0])
    assert len(set(wallets)) == 1
    assert values[0].decode("cp932") == "You received ３７０ gold."
    assert normalize("NFKC", values[0].decode("cp932")).encode("ascii") == values[1] == b"You received 370 gold."
    render = stage.rewards.discovery.mixed
    raster, _, _ = render.font_tools(cases[1])
    kanji = cases[1].read_file("/GRP/KANJI.FNT")
    expected, glyphs = render.render(raster, arms[1], kanji, values[1])
    assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord("Y"), ord("."))

    unchanged, displayed = [], []
    for n, old in pictures[0].items():
        new = pictures[1][n]
        assert all(base.digest(r["path"]) == r["PNG_sha256"] for r in (old, new))
        if n not in HOLDS:
            assert old["framebuffer_sha256"] == new["framebuffer_sha256"], n
            unchanged.append(n)
            continue
        before, after = [Image.open(r["path"]).convert("RGB") for r in (old, new)]
        box = (16, 296, 244, 344)
        assert bytes(c == (0, 8, 0) for c in after.crop(box).get_flattened_data()) == expected
        delta = ImageChops.difference(before, after).getbbox()
        assert delta and box[0] <= delta[0] < delta[2] <= box[2] and box[1] <= delta[1] < delta[3] <= box[1] + 16
        displayed.append(dict(frame=n, original=old, corrected=new, complete_glyphs=len(glyphs), difference_bounds=delta))
    assert [r["frame"] for r in displayed] == list(HOLDS)
    clean = base.NdsImage.open(shared.CLEAN)
    source = shared.workflow.common_message_entries(clean.read_file(shared.COMMON), clean.read_file(shared.ARM))[REPORT]
    row = shared.entries(cases[1])[REPORT]
    english = " ".join(row.text.decode("ascii").split())
    assert english == "It appears the expedition found something!"
    context = dict(message_ID=REPORT, speaker="Gerhard Adernkatz", source_hex=source.text.hex(),
                   source_Japanese=source.text.decode("cp932"), current_hex=row.text.hex(), english=english,
                   source_reference=shared.workflow.reference(source), current_reference=shared.workflow.reference(row),
                   frame=pictures[1][5350], decision="retention",
                   reason="Gerhard reports that the expedition seems to have found something before the result names the gold.")
    sheet = Image.new("RGB", (1024, 250), "#263238")
    draw = ImageDraw.Draw(sheet)
    for index, (side, label) in enumerate((("original", "Original wide digits"), ("corrected", "Regular English digits"))):
        draw.text((512 * index + 6, 6), label, fill="white")
        frame = Image.open(displayed[-1][side]["path"]).convert("RGB").crop((0, 271, 256, 384))
        sheet.paste(frame.resize((512, 226), Image.Resampling.NEAREST), (512 * index, 23))
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=staged["candidate_sha256"], parent_sha256=staged["parent_sha256"],
        amount=370, identical_wallet_after_award=wallets[0], normal_inputs=True, original_outcome_selection=True,
        position_fixture_bytes=48, crew_report=context, unchanged_frames=unchanged, corrected_holds=displayed,
        power_alternates_offline_only=True, return_from_gold_notice_observed=False, hardware_verified=False,
        sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)),
        source_evidence={str(p): base.digest(p) for p in (*paths, *inputs, *terrain)}))
    print("The original Search picked 370 gold in both runs. The crew dialogue matches and the full notice uses regular digits.")


if __name__ == "__main__":
    main()
