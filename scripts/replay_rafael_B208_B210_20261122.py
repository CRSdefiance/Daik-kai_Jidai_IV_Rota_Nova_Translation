"""Cold-boot focused excerpts with native choice, Charm, and unseen voice transitions."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_rafael_B177_B180_20261121 as previous
from scripts import verify_rafael_B208_B210_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, PATH = display.stage, display.base, display.native, display.PATH
ROOT = stage.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
SELECTED = (
    (208, 5), (208, 8), (208, 13), (208, 25), (208, "218"), (208, 43), (208, 46),
    (208, 65), (208, 77), (208, 157), (208, 183), (208, 264), (208, 294), (208, 310),
    (209, 5), (209, 14), (209, 21), (209, 24), (209, "230"), (209, 86), (209, 94), (209, 110),
    (210, 10), (210, 18), (210, 22), (210, 26), (210, 30), (210, 34), (210, 38),
    (210, 42), (210, 49), (210, 76), (210, 80),
)


def schedule(commands):
    clock, events, requests = 4000, [], []
    for command in commands:
        pos, plan = command["stored_offset"], command["plan"]
        if command["word"] in (0x2100, 0x2200):
            count = len(command["record_ids"])
            for slot in range(count):
                requests.append(dict(type="menu", offset=pos, slot=slot, holds=[clock - 135, clock - 95, clock - 45]))
                events.append(dict(start=clock, duration=5, buttons=["DOWN" if slot < count - 1 else "A"]))
                clock += 300
            continue
        for page in range(1, (plan["expected_native_pages"] if plan else 1) + 1):
            requests.append(dict(type="speech", offset=pos, page=page, holds=[clock - 45]))
            events.append(dict(start=clock, duration=5, buttons=["A"]))
            clock += 300
    return events, requests, clock + 420


producer = checked_text(previous.producer, {
    '''            word = 0x2100 if index == "menu" else 0x4100
            command, = [c for c in group["commands"] if c["word"] == word and
                        (word == 0x2100 or int(c["source"][38:40], 16) == int(index[5:]))]''':
        '''            command, = [c for c in group["commands"] if c["word"] in (0x2100, 0x2200)
                        and any(f"CHOICE_{index}_" in ident for ident in c["record_ids"])]''',
    'groups[180]["commands"]': 'groups[210]["commands"]',
    '"Rafael_B177_B180_FOCUSED_ONLY.nds"': '"Rafael_B208_B210_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '            observed["block"] = item["block"]':
        '            observed["block"] = item["block"]\n            observed["record_ids"] = item["ids"]',
    '[(b, i) for b in SELECT_SLOT for i in (0, 1)]': '[(208, 0), (208, 1), (209, 0), (209, 1), (209, 2)]',
    '["DK4_MES_B177_R0180", "DK4_MES_B177_R0183"]':
        '[f"DK4_MES_B210_R{n:04d}" for n in (18, 22, 26, 30, 34, 38)]',
    '[transition_ids[0], *transition_ids]': 'transition_ids',
    '[1, 2, 1]': '[1] * len(transition_ids)',
    '900, 300': 'len(transition_ids) * 300, 300',
    'rafael_B177_B180_gameplay_': 'rafael_B208_B210_gameplay_',
    'len(expected_speech) + 1': 'len(expected_speech)',
    '{key for item in native_report["menus"] for key in item["record_ids"]}':
        '{key for item in menus for key in item["record_ids"]}',
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
