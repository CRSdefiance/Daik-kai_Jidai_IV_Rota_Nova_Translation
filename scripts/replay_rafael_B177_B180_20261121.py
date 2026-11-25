"""Observe the original menu text, a tutorial page turn, and the return to port."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_rafael_B161_B169_20261121 as previous
from scripts import replay_rafael_rescue_and_lessons_20261121 as producer_template
from scripts import verify_rafael_B177_B180_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, PATH = display.stage, display.base, display.native, display.PATH
ROOT = stage.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
SELECTED = (
    (177, 100), (177, 114), (177, 117), (177, 144), (177, "menu"), (177, 180), (177, 183), (177, 221),
    (178, 16), (178, "menu"), (178, 64), (178, 127), (178, 131), (178, 214), (178, 231), (178, 234), (178, 339),
    (179, 87), (179, "menu"), (179, 134), (179, 122),
    (180, 13), (180, "menu"), (180, 82), (180, 89), (180, 102), (180, 110), (180, 113), (180, 139),
)
SELECT_SLOT = {177: 0, 178: 0, 179: 1, 180: 0}


def schedule(commands):
    clock, events, requests = 4000, [], []
    for command in commands:
        pos, plan = command["stored_offset"], command["plan"]
        if command["word"] == 0x2100:
            chosen = SELECT_SLOT[command["fixture_block"]]
            for slot in (0, 1):
                requests.append(dict(type="menu", offset=pos, slot=slot, holds=[clock - 135, clock - 95, clock - 45]))
                button = "DOWN" if slot == 0 else "UP" if chosen == 0 else "A"
                events.append(dict(start=clock, duration=5, buttons=[button]))
                clock += 300
            if chosen == 0:
                events.append(dict(start=clock, duration=5, buttons=["A"]))
                clock += 300
            continue
        for page in range(1, (plan["expected_native_pages"] if plan else 1) + 1):
            requests.append(dict(type="speech", offset=pos, page=page, holds=[clock - 45]))
            events.append(dict(start=clock, duration=5, buttons=["A"]))
            clock += 300
    return events, requests, clock + 420


producer = checked_text(producer_template.producer, {
    'groups[139]["commands"]': 'groups[180]["commands"]',
    '"Rafael_Rescue_And_Lessons_RESEARCH_ONLY.nds"': '"Rafael_B177_B180_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '            menus.append(observed)\n            pictures.append((f"B91 miracle choice, selected {observed[\'highlight\'] + 1}", image))':
        '''            observed["block"] = item["block"]
            menus.append(observed)
            pictures.append((f"B{item['block']} choice, highlighted {observed['highlight'] + 1}", image))''',
    '    assert not menus': '    assert [(m["block"], m["highlight"]) for m in menus] == [(b, i) for b in SELECT_SLOT for i in (0, 1)]',
    '["DK4_MES_B165_R0016", "DK4_MES_B166_R0069", "DK4_MES_B166_R0072"]':
        '["DK4_MES_B177_R0180", "DK4_MES_B177_R0183"]',
    '[1, 2, 1, 1]': '[1, 2, 1]',
    '1200, 300': '900, 300',
    'rafael_B161_B169_gameplay_': 'rafael_B177_B180_gameplay_',
    '''    observed = {r["id"] for r in holds}
    assert len(holds) == len(SELECTED) + 1
    assert observed == {f"DK4_MES_B{block}_R{index:04d}" for block, index in SELECTED}''':
        '''    speech_ids = {r["id"] for r in holds}
    expected_speech = {f"DK4_MES_B{block}_R{index:04d}" for block, index in SELECTED if isinstance(index, int)}
    assert speech_ids == expected_speech and len(holds) == len(expected_speech) + 1
    observed = speech_ids | {key for item in native_report["menus"] for key in item["record_ids"]}''',
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
