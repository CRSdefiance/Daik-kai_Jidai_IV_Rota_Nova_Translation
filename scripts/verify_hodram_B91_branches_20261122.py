"""Compare the complete B91 replay outcomes with the native stat notice masks."""

from types import SimpleNamespace

from scripts import replay_hodram_B91_branches_20261122 as branch
from scripts import replay_hodram_B91_B110_20261122 as live
from scripts import verify_hodram_B91_B110_20261122 as display


base, native = branch.base, branch.native
PROOF = branch.ROOT / "verified_branches_v2.json"
NOTICE_PAIRS = {"accept": (84, 87), "decline": (103, 106)}


def main():
    assert not PROOF.exists()
    fixture = base.load(branch.FIXTURE)
    renderer = base.load(display.PROOF)
    assert fixture["initialized_complete_script"] and fixture["unchanged_source_commands_and_relative_branches"]
    assert base.digest(display.stage.ROM) == fixture["candidate_sha256"] == renderer["candidate_sha256"]
    assert base.digest(branch.ROM) == fixture["fixture_sha256"]
    game = base.NdsImage.open(display.stage.ROM)
    town = live.scope["town"]
    paint = town.current_fe_painter(SimpleNamespace(image=game, arm=game.read_file(native.ARM)))
    panels = {}
    for n in (*NOTICE_PAIRS["accept"], *NOTICE_PAIRS["decline"]):
        ident = f"DK4_MES_B91_R{n:04d}"
        obj, = [r["system"][0] for r in renderer["records"] if r["id"] == ident]
        body = bytes.fromhex(obj["expanded_hex"])
        plane = paint(body)["physical"]
        assert native.digest(plane) == obj["plane_sha256"]
        panels[n] = ident, body.decode("ascii").strip(), plane
    outcomes, sheets = {}, []
    inputs, evidence = {}, {str(p): base.digest(p) for p in (branch.FIXTURE, branch.ROM, display.PROOF)}
    for mode, expected in NOTICE_PAIRS.items():
        input_path = branch.ROOT / mode / "inputs.json"
        report_path = branch.ROOT / mode / "capture/capture_report.json"
        evidence.update({str(p): base.digest(p) for p in (input_path, report_path)})
        report = base.load(report_path)
        inputs[mode] = schedule = base.load(input_path)
        assert schedule == report["scripted_input_schedule"] and report["ROM_sha256"] == fixture["fixture_sha256"]
        assert report["cold_boot"] and not (report["savestate_loaded"] or report.get("battery_save_preloaded") or report["callback_errors"])
        assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
        captures = {shot["frame"]: shot for shot in report["frames_captured"] if shot["path"].endswith("_cold_boot.png")}
        found, pictures = {}, []
        menu, image = town.read_frame(captures, 4680)
        pictures.append((f"{mode.title()} / choice", image))
        for t in sorted(k for k in captures if 4800 <= k < report["frames"] - 1):
            shot, screen = town.read_frame(captures, t)
            for n, (ident, text, plane) in panels.items():
                if n not in found and live.match_panel(plane, True, screen, ident):
                    found[n] = dict(id=ident, notice=text, frame=t, screenshot=shot)
                    pictures.append((text, screen))
        assert tuple(found) == expected, (mode, tuple(found))
        final, image = town.read_frame(captures, report["frames"] - 1)
        pictures.append(("Port menu after accepting" if mode == "accept" else "Later choice after declining", image))
        sheet = branch.ROOT / f"hodram_B91_{mode}_gameplay_v2.png"
        town.sheet(pictures, sheet)
        sheets.append(dict(path=str(sheet), sha256=base.digest(sheet)))
        outcomes[mode] = dict(choice_frame=menu, notices=list(found.values()), final_frame=final)
    assert [item for item in inputs["decline"] if item not in inputs["accept"]] == [
        dict(start=4600, duration=5, buttons=["DOWN"])]
    assert [i for i in inputs["accept"] if i["start"] < 6000] == [
        i for i in inputs["decline"] if i["start"] < 6000 and i["buttons"] != ["DOWN"]]
    base.save(PROOF, dict(candidate_sha256=fixture["candidate_sha256"], fixture_sha256=fixture["fixture_sha256"],
        initialized_complete_script=True, natural_activation=False, hardware_verified=False, exact_visible_notice_masks=True,
        outcomes=outcomes, sheets=sheets, evidence=evidence))


if __name__ == "__main__":
    main()

