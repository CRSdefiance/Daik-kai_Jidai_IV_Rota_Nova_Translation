"""Check representative palace and alliance text with the cold-boot emulator fixture."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_rafael_rescue_and_lessons_20261121 as precedent
from scripts import verify_rafael_palace_and_alliance_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, PATH = display.stage, display.base, display.native, display.PATH
ROOT = stage.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
SELECTED = (
    (142, 26), (143, 123), (143, 126), (143, 129), (143, 133), (143, 189), (143, 192),
    (143, 354), (143, 424), (145, 15), (147, 12), (148, 37), (148, 167), (148, 224),
)
TRANSITION = ["DK4_MES_B143_R0123", "DK4_MES_B143_R0126", "DK4_MES_B143_R0129"]

producer = checked_text(precedent.producer, {
    'groups[139]["commands"]': 'groups[149]["commands"]',
    "Rafael_Rescue_And_Lessons_RESEARCH_ONLY.nds": "Rafael_Palace_And_Alliance_RESEARCH_ONLY.nds",
})
schedule = checked_text(precedent.schedule, {
    '{127: 1, 136: 1}[command["fixture_block"]]': '{143: 1, 146: 1, 148: 1}[command["fixture_block"]]',
})
checker = checked_text(precedent.check, {
    'expected["scope"] == "registered default"': 'expected["scope"] in ("registered default", "retained full-name substitution")',
    '[(127, 0), (127, 1), (136, 0), (136, 1)]': '[]',
    '    assert sum(h["id"].startswith(("SC0_B121_STYLE_", "SC0_B125_STYLE_")) for h in holds) == 4\n': '',
    '["DK4_MES_B127_R0029", "DK4_MES_B127_R0049", "DK4_MES_B127_R0054"]': 'TRANSITION',
    'if m["block"] in (127, 136)': 'if m["block"] in (143, 146, 148)',
    '[0, 900, 1200]': '[0, 300, 600]',
    'rafael_rescue_gameplay_': 'refined_palace_gameplay_',
    ' and four highlights across the sailing and Guiding Staff menus': ' across the final palace excerpts',
})
scope = precedent.scope | globals() | {"prior": precedent.scope["prior"]}
for code in (producer, schedule, checker):
    exec(compile(code, __file__ + "::gameplay", "exec"), scope)


def verify_and_reuse_prior_play():
    focused = ROOT / "focused_refinements.json"
    FunctionType(scope["check"].__code__, scope | {"PROOF": focused})()
    reference = display.first.ROOT / "focused_gameplay/verified_gameplay.json"
    old_native = display.first.ROOT / "native_display/native_display.json"
    previous, current, first, final = map(base.load, (reference, focused, old_native, display.PROOF))
    assert previous["candidate_sha256"] == first["candidate_sha256"] == base.digest(display.first.ROM)
    assert current["candidate_sha256"] == final["candidate_sha256"] == base.digest(stage.ROM)
    prior_image, final_image = map(base.NdsImage.open, (display.first.ROM, stage.ROM))
    assert all(prior_image.read_file(path) == final_image.read_file(path) for path in display.display.ASSETS)
    preludes = [native.IlnkContainer.parse(game.read_file(PATH)).blocks[44][:40] for game in (prior_image, final_image)]
    assert preludes[0] == preludes[1]
    renewed = {r["id"] for r in current["holds"]}
    reuse = [r for r in previous["holds"] if r["id"] not in renewed]
    old, new = ({r["id"]: r for r in proof["records"]} for proof in (first, final))
    menu_ids = {key for menu in final["menus"] for key in menu["record_ids"]}
    assert len(previous["menus"]) == len(menu_ids) == 6
    exact = {r["id"] for r in reuse} | menu_ids
    for key in exact:
        assert [p["stored"] for p in old[key]["stored_pages"]] == [p["stored"] for p in new[key]["stored_pages"]]
        assert old[key].get("layouts") == new[key].get("layouts") and old[key].get("system") == new[key].get("system")
    assert set(final["replaced_preview_ids"]) & set(previous["observed_ids"]) <= renewed
    evidence = previous["evidence"] | current["evidence"] | {
        str(reference): base.digest(reference), str(focused): base.digest(focused)}
    assert all(base.digest(path) == sha for path, sha in evidence.items())
    assert all(base.digest(r["observed"]["path"]) == r["observed"]["PNG_sha256"]
               for r in reuse + previous["menus"] + current["holds"])
    observed = exact | renewed
    base.save(PROOF, current | dict(holds=reuse + current["holds"], menus=previous["menus"], observed_ids=sorted(observed),
        earlier_gameplay_proof=str(reference), reused_speech_samples=len(reuse), reused_menu_highlights=6,
        superseded_earlier_ids=sorted({r["id"] for r in previous["holds"]} & renewed),
        sheets=previous["sheets"] + current["sheets"], evidence=evidence,
        earlier_final_hold=previous["final_hold"],
        offline_only=[r["id"] for r in base.load(stage.OUTPUT)["records"] if r["id"] not in observed]))
    print(f"Verified {len(current['holds'])} fresh and {len(reuse)} exact earlier speech samples, and six exact menu highlights.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    if parser.parse_args().action == "replay":
        scope["replay"]()
    else:
        verify_and_reuse_prior_play()
