"""Replay selected rescue, companion and tutorial text using exact installed commands."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_rafael_ruins_and_proof_20261121 as template
from scripts import verify_rafael_rescue_and_lessons_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native = display.stage, display.base, display.native
PATH = display.PATH
ROOT = stage.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
COMPANY_LINE = "DK4_MES_B123_R0115"
COMPANY_EXCERPT = ((123, 109), (123, 112), (123, 115), (123, 119))
REFERENCE = stage.ROOT.with_name("staged_v2")
SELECTED = (
    (121, 6), (121, "style214"), (121, 45), (121, 52), (121, 56), (121, "style215"), (121, 86),
    (121, 113), (121, 124), (121, 138),
    (122, 40), (123, 48), (123, 115), (123, 136), (123, 165), (124, 22),
    (125, "style209"), (125, "style220"), (126, 20),
    (127, 26), (127, 29), (127, "menu"), (127, 49), (127, 54), (127, 77),
    (128, 140), (128, 143), (128, 147), (128, 189),
    (129, 24), (132, 68), (133, 25), (133, 47), (134, 15), (135, 43),
    (136, 102), (136, "menu"), (136, 189), (136, 203),
    (138, 25), (139, 39), (139, 71),
)

producer = checked_text(template.producer, {
    '''        if index in ("menu", "style"):
            word = 0x2200 if index == "menu" else 0x4100
            command, = [c for c in group["commands"] if c["word"] == word]''':
    '''        if isinstance(index, str):
            word = 0x2100 if index == "menu" else 0x4100
            command, = [c for c in group["commands"] if c["word"] == word and
                        (word == 0x2100 or int(c["source"][38:40], 16) == int(index[5:]))]''',
    'end = groups[120]["commands"][-1]': 'end = groups[139]["commands"][-1]',
    "Rafael_Ruins_And_Proof_RESEARCH_ONLY.nds": "Rafael_Rescue_And_Lessons_RESEARCH_ONLY.nds",
})
check = checked_text(template.check, {
    '{207: "Rafael Castor", 208: "Sailor"}.get(row["source_selector"], row["speaker"])':
        '("Rafael Castor" if row["source_selector"] == 207 else "Sailor") if row["source_selector"] in (207, 208, 209, 214, 215, 220) else row["speaker"]',
    '''    assert [(m["block"], m["highlight"]) for m in menus] == [(118, 0), (118, 1), (118, 2), (119, 0), (119, 1)]
    assert sum(h["id"].startswith(("SC0_B113_STYLE_", "SC0_B119_STYLE_")) for h in holds) == 2
    transition_ids = ["DK4_MES_B118_R0023", "DK4_MES_B118_R0120", "DK4_MES_B118_R0125"]''':
    '''    assert [(m["block"], m["highlight"]) for m in menus] == [(127, 0), (127, 1), (136, 0), (136, 1)]
    assert sum(h["id"].startswith(("SC0_B121_STYLE_", "SC0_B125_STYLE_")) for h in holds) == 4
    transition_ids = ["DK4_MES_B127_R0029", "DK4_MES_B127_R0049", "DK4_MES_B127_R0054"]''',
    '''    assert [h[2] - turn[0][2] for h in turn] == [0, 1200, 1500]
    for first, following in (("DK4_MES_B101_R0068", "DK4_MES_B101_R0071"), ("DK4_MES_B103_R0042", "DK4_MES_B103_R0045")):
        a, b = [r for r in holds if r["id"] in (first, following)]
        assert (a["id"], a["page"], b["id"], b["page"], b["frame"] - a["frame"]) == (first, 1, following, 1, 300)''':
    '''    assert [h[2] - turn[0][2] for h in turn] == [0, 900, 1200]''',
    "rafael_ruins_gameplay_": "rafael_rescue_gameplay_",
    'if m["block"] in (118, 119)': 'if m["block"] in (127, 136)',
    "five highlights across two ruin menus": "four highlights across the sailing and Guiding Staff menus",
})
scope = template.scope | globals() | {"prior": template.scope["prior"]}
schedule = checked_text(getsource(template.schedule), {
    '{118: 2, 119: 1}[command["fixture_block"]]': '{127: 1, 136: 1}[command["fixture_block"]]',
})
for code in (producer, check, schedule):
    exec(compile(code, __file__ + "::gameplay", "exec"), scope)


def check_company_excerpt():
    proof = ROOT / "company_excerpt.json"
    source = check.split('    assert [(m["block"], m["highlight"])', 1)[0] + '''
    assert not menus and len(holds) == 4
    assert [h["id"] for h in holds] == [f"DK4_MES_B123_R{idx:04d}" for _, idx in COMPANY_EXCERPT]
    exact = native_rows[COMPANY_LINE]["layouts"][0]
    expanded = bytes.fromhex(exact["expanded_hex"]).decode("ascii")
    assert "Castor Co., that's who I'm with." == " ".join(expanded.split())
    final, _ = town.read_frame(captures, fixture["end"] - 1)
    path = ROOT / "company_gameplay.png"
    town.sheet(pictures, path)
    evidence = (fixture_file, inputs, REPORT, display.PROOF, fixture["fixture_ROM"])
    base.save(PROOF, dict(candidate_sha256=candidate, holds=holds, final_hold=final,
                         sheets=[dict(path=str(path), sha256=base.digest(path))],
                         evidence={str(path): base.digest(path) for path in evidence}))
'''
    namespace = scope | {"PROOF": proof}
    exec(compile(source, __file__ + "::focused-company-check", "exec"), namespace)
    namespace["check"]()
    return proof


def check_with_prior_play():
    focused = check_company_excerpt()
    previous = REFERENCE / "focused_gameplay/verified_gameplay.json"
    previous_native = REFERENCE / "native_display/native_display.json"
    earlier, old_native, new_native, current = map(base.load, (previous, previous_native, display.PROOF, focused))
    old_rom = REFERENCE / stage.ROM.name
    assert earlier["candidate_sha256"] == old_native["candidate_sha256"] == base.digest(old_rom)
    assert new_native["candidate_sha256"] == current["candidate_sha256"] == base.digest(stage.ROM)
    old_image, new_image = [base.NdsImage.open(rom) for rom in (old_rom, stage.ROM)]
    assert all(old_image.read_file(path) == new_image.read_file(path) for path in display.display.ASSETS)
    a, b = [native.IlnkContainer.parse(game.read_file(PATH)).blocks[44][:40] for game in (old_image, new_image)]
    assert a == b
    maps = [{r["id"]: r for r in d["records"]} for d in (old_native, new_native)]
    original, corrected = [m[COMPANY_LINE]["stored_pages"][0]["stored"] for m in maps]
    assert original != corrected
    assert len(earlier["holds"]) == 40 and len(earlier["menus"]) == 4
    keep = [r for r in earlier["holds"] if r["id"] != COMPANY_LINE]
    assert len(keep) == 39
    validated = {h["id"] for h in keep}
    for menu in new_native["menus"]:
        if menu["block"] in (127, 136):
            validated.update(menu["record_ids"])
    for key in validated:
        old, new = [m[key] for m in maps]
        assert [page["stored"] for page in old["stored_pages"]] == [page["stored"] for page in new["stored_pages"]]
        assert old.get("layouts") == new.get("layouts") and old.get("system") == new.get("system")
    selected = {r["id"] for r in current["holds"]}
    evidence = earlier["evidence"] | current["evidence"] | {str(previous): base.digest(previous), str(focused): base.digest(focused)}
    assert all(base.digest(path) == sha for path, sha in evidence.items())
    assert all(base.digest(r["observed"]["path"]) == r["observed"]["PNG_sha256"]
               for r in keep + earlier["menus"] + current["holds"])
    manifest = stage.base.load(stage.OUTPUT)
    ids = validated | selected
    base.save(PROOF, earlier | dict(candidate_sha256=current["candidate_sha256"], holds=keep + current["holds"],
        observed_ids=sorted(ids), prior_gameplay_proof=str(previous), prior_speech_samples_reused=len(keep),
        prior_menus_reused=len(earlier["menus"]), superseded_prior_record=COMPANY_LINE,
        final_hold=current["final_hold"], reference_final_hold=earlier["final_hold"],
        sheets=earlier["sheets"] + current["sheets"], evidence=evidence,
        offline_only=[row["id"] for row in manifest["records"] if row["id"] not in ids]))
    print("Verified four final company-exchange pages, 39 exact prior speech samples and four menu highlights.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    if parser.parse_args().action == "replay":
        FunctionType(scope["replay"].__code__, scope | {"SELECTED": COMPANY_EXCERPT})()
    else:
        check_with_prior_play()

