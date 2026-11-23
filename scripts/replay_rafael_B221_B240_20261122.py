"""Observe both voice tables around Yukihisa's signed letter and selected later encounters."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_rafael_B208_B210_20261122 as previous
from scripts import verify_rafael_B221_B240_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, PATH = display.stage, display.base, display.native, display.PATH
ROOT = stage.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
SELECTED = (
    (221, "style8"), (221, 27), (221, 30), (221, 33), (221, "style702"), (221, 71),
    (223, 9), (223, 13), (223, 24), (223, 28), (223, 40),
    (224, "64"), (224, 32), (224, "242"), (224, 54),
    (226, "style8"), (226, 68), (227, 15), (227, 19), (227, 55),
    (228, 31), (230, 48), (232, 50),
    (233, "136"), (233, 41), (233, 52), (233, 64), (233, 67),
    (234, 35), (234, 59),
    (235, "style8"), (235, 28), (235, 31), (235, 48), (235, 56),
    (236, 26), (236, 32), (237, 28), (237, 49), (238, 51), (239, 16),
)
schedule = previous.schedule
producer = checked_text(previous.producer, {
    '''            command, = [c for c in group["commands"] if c["word"] in (0x2100, 0x2200)
                        and any(f"CHOICE_{index}_" in ident for ident in c["record_ids"])]''':
    '''            if index.startswith("style"):
                command, = [c for c in group["commands"] if c["word"] == 0x4100 and c["source_offset"] == int(index[5:])]
            else:
                command, = [c for c in group["commands"] if c["word"] in (0x2100, 0x2200)
                            and any(f"CHOICE_{index}_" in ident for ident in c["record_ids"])]''',
    'groups[210]["commands"]': 'groups[239]["commands"]',
    '"Rafael_B208_B210_FOCUSED_ONLY.nds"': '"Rafael_B221_B240_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '''        ident, = item["ids"]
        row, checked = rows[ident], native_rows[ident]
        page = req["page"]
        frame, = req["holds"]
        captured, image = town.read_frame(captures, frame)''':
    '''        page = req["page"]
        frame, = req["holds"]
        captured, image = town.read_frame(captures, frame)
        if item["word"] == 0x4100:
            selected = []
            for ident in item["ids"]:
                body = bytes.fromhex(native_rows[ident]["body_hex"])
                rendered = paint(arm, font, body)
                plane = bytes.fromhex(rendered["pages"][0]["native_plane_hex"])
                if match_panel(plane, False, image, ident):
                    selected.append(ident)
            assert selected, (item["block"], frame)
            assert len({native_rows[ident]["body_hex"] for ident in selected}) == 1
            ident = selected[0]
        else:
            ident, = item["ids"]
        row, checked = rows[ident], native_rows[ident]''',
    'current = bytes.fromhex(row["current_hex"])[1:].decode("ascii")':
        'current = bytes.fromhex(checked["body_hex"])[int(item["word"] != 0x4100):].decode("ascii")',
    'panel.complete_mask(name_font, row["speaker"], image, 16, 277, town.INKS[1])':
        'panel.complete_mask(name_font, "Sailor" if item["word"] == 0x4100 else row["speaker"], image, 16, 277, town.INKS[1])',
    '[(208, 0), (208, 1), (209, 0), (209, 1), (209, 2)]':
        '[(224, 0), (224, 1), (224, 0), (224, 1), (224, 2), (233, 0), (233, 1)]',
    '[f"DK4_MES_B210_R{n:04d}" for n in (18, 22, 26, 30, 34, 38)]':
        '["DK4_MES_B233_R0064", "DK4_MES_B233_R0067"]',
    'assert [h[0] for h in turn] == transition_ids': 'assert [h[0] for h in turn] == [transition_ids[0], *transition_ids]',
    'assert [h[1] for h in turn] == [1] * len(transition_ids)': 'assert [h[1] for h in turn] == [1, 2, 1]',
    'len(transition_ids) * 300, 300': '900, 300',
    'rafael_B208_B210_gameplay_': 'rafael_B221_B240_gameplay_',
    'assert speech_ids == expected_speech and len(holds) == len(expected_speech)':
        '''assert {i for i in speech_ids if "_STYLE_" not in i} == expected_speech
    assert len(holds) == len(expected_speech) + 6
    assert sum("_STYLE_" in hold["id"] for hold in holds) == 4''',
})
scope = previous.scope | globals() | dict(stage=SimpleNamespace(
    PROOF=stage.PROOF, ROM=stage.ROM, ROOT=stage.ROOT, OUTPUT=stage.MANUSCRIPT,
    review=SimpleNamespace(TOKEN=stage.TOKEN)))
for script in (producer, check):
    exec(compile(script, __file__ + "::focused-native-excerpts", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
