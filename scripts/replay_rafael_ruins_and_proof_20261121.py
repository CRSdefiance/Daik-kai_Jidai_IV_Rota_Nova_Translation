"""Replay exact companion objects, ruin riddles and the move from FE notice to dialogue."""

from argparse import ArgumentParser
from inspect import getsource

from scripts import replay_rafael_followup_encounters_20261121 as prior
from scripts import verify_rafael_ruins_and_proof_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native = display.stage, display.base, display.native
ROOT = stage.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
SELECTED = (
    (101, 23), (101, 49), (101, 68), (101, 71), (102, 46), (103, 42), (103, 45),
    (104, 43), (105, 39), (110, 13),
    (113, "style"), (113, 29), (113, 33), (113, 37),
    (114, 24), (114, 36), (114, 152), (114, 167), (114, 185),
    (115, 28), (116, 29), (116, 89), (117, 21),
    (118, 7), (118, 19), (118, 23), (118, "menu"), (118, 120), (118, 125),
    (119, "style"), (119, 33), (119, 36), (119, 39), (119, "menu"),
    (119, 66), (119, 101), (120, 56), (120, 72), (120, 83),
)


def schedule(commands):
    clock = 4000
    events, requests = [], []
    for command in commands:
        pos, plan = command["stored_offset"], command["plan"]
        if command["word"] in (0x2100, 0x2200):
            final_slot = {118: 2, 119: 1}[command["fixture_block"]]
            for slot in range(final_slot + 1):
                requests.append(dict(type="menu", offset=pos, slot=slot, holds=[clock - 135, clock - 95, clock - 45]))
                events.append(dict(start=clock, duration=5, buttons=["A" if slot == final_slot else "DOWN"]))
                clock += 300
            continue
        for page in range(1, (plan["expected_native_pages"] if plan else 1) + 1):
            requests.append(dict(type="speech", offset=pos, page=page, holds=[clock - 45]))
            events.append(dict(start=clock, duration=5, buttons=["A"]))
            clock += 300
    return events, requests, clock + 420


producer = checked_text(getsource(prior.replay), {
    '''        if index == "menu":
            command, = [c for c in group["commands"] if c["word"] == 0x2100]''':
    '''        if index in ("menu", "style"):
            word = 0x2200 if index == "menu" else 0x4100
            command, = [c for c in group["commands"] if c["word"] == word]''',
    '"stored_offset": len(logical), "plan": plan': '"stored_offset": len(logical), "plan": plan, "fixture_block": block',
    'end = groups[91]["commands"][-1]': 'end = groups[120]["commands"][-1]',
    "Rafael_Followup_Encounters_RESEARCH_ONLY.nds": "Rafael_Ruins_And_Proof_RESEARCH_ONLY.nds",
    "driver.make_schedule(compiled)": "schedule(compiled)",
})
check = checked_text(getsource(prior.check), {
    '''            menus.append(observed)
            pictures.append((f"B91 miracle choice, selected {observed['highlight'] + 1}", image))''':
    '''            observed["block"] = item["block"]
            menus.append(observed)
            pictures.append((f"B{item['block']} choice, selected {observed['highlight'] + 1}", image))''',
    '''        ident, = item["ids"]
        row, checked = rows[ident], native_rows[ident]
        page = req["page"]
        frame, = req["holds"]
        captured, image = town.read_frame(captures, frame)''':
    '''        page = req["page"]
        frame, = req["holds"]
        captured, image = town.read_frame(captures, frame)
        if item["word"] == 0x4100:
            choices = []
            for key in item["ids"]:
                body = bytes.fromhex(native_rows[key]["body_hex"])
                view = paint(arm, font, body)
                plane = bytes.fromhex(view["pages"][0]["native_plane_hex"])
                if panel.mask_check(plane, 216, image):
                    choices.append(key)
            assert choices, (item["block"], frame)
            ident = choices[0]
            assert len({native_rows[key]["body_hex"] for key in choices}) == 1
        else:
            ident, = item["ids"]
        row, checked = rows[ident], native_rows[ident]''',
    '''                current = bytes.fromhex(row["current_hex"])[1:].decode("ascii")''':
    '''                current = bytes.fromhex(checked["body_hex"])[int(item["word"] != 0x4100):].decode("ascii")''',
    'panel.complete_mask(name_font, row["speaker"], image, 16, 277, town.INKS[1])':
        '''triggered = {207: "Rafael Castor", 208: "Sailor"}.get(row["source_selector"], row["speaker"])
            panel.complete_mask(name_font, triggered, image, 16, 277, town.INKS[1])''',
    '''    assert [m["highlight"] for m in menus] == [0, 1]
    transition_ids = ["DK4_MES_B91_R0101", "DK4_MES_B91_R0109", "DK4_MES_B91_R0112", "DK4_MES_B92_R0005"]''':
    '''    assert [(m["block"], m["highlight"]) for m in menus] == [(118, 0), (118, 1), (118, 2), (119, 0), (119, 1)]
    assert sum(h["id"].startswith(("SC0_B113_STYLE_", "SC0_B119_STYLE_")) for h in holds) == 2
    transition_ids = ["DK4_MES_B118_R0023", "DK4_MES_B118_R0120", "DK4_MES_B118_R0125"]''',
    '''    assert [h[2] for h in turn] == list(range(turn[0][2], turn[0][2] + 1200, 300))''':
    '''    assert [h[2] - turn[0][2] for h in turn] == [0, 1200, 1500]
    for first, following in (("DK4_MES_B101_R0068", "DK4_MES_B101_R0071"), ("DK4_MES_B103_R0042", "DK4_MES_B103_R0045")):
        a, b = [r for r in holds if r["id"] in (first, following)]
        assert (a["id"], a["page"], b["id"], b["page"], b["frame"] - a["frame"]) == (first, 1, following, 1, 300)''',
    "rafael_encounters_gameplay_": "rafael_ruins_gameplay_",
    '''    miracle_menu, = [m for m in native_report["menus"] if m["block"] == 91]
    observed = {r["id"] for r in holds} | set(miracle_menu["record_ids"])''':
    '''    observed = {r["id"] for r in holds} | {key for m in native_report["menus"] if m["block"] in (118, 119) for key in m["record_ids"]}''',
    "two miracle menu highlights": "five highlights across two ruin menus",
})
scope = vars(prior) | globals() | {"prior": prior.prior}
exec(compile(producer, __file__ + "::replay", "exec"), scope)
exec(compile(check, __file__ + "::check", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()

