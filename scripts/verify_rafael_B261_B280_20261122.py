"""Verify both ruins voice tables, including every revised body and choice caption."""

from inspect import getsource

from scripts import stage_rafael_B261_B280_20261122 as stage
from scripts import verify_rafael_B221_B240_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"

panels = checked_text(getsource(previous.qualified_panels), {
    'len(panels) == 3': 'len(panels) == 17',
})
verification = checked_text(previous.verification, {
    'len(entries) == 270 and fe_count == 3 and len(style_objects) == 4':
        'len(entries) == 135 and fe_count == 17 and len(style_objects) == 2',
    '[224, 224, 233] and [m["count"] for m in choices] == [2, 3, 2]':
        '[261, 261] and [m["count"] for m in choices] == [3, 2]',
    'assert raw == old and all(r["decision"] == "retention" for r in members)':
        'assert (raw != old) == any(r["decision"] == "revision" for r in members)',
    '"rafael_B221_B240_progressive"': '"rafael_B261_B280_progressive"',
})
names = checked_text(previous.names, {
    '("B221_B240",)': '("B261_B280",)',
    'if r["kind"] == "progressive"}':
        'if r["kind"] == "progressive" and r["source_selector"] < 207}',
    ''''selectors = {r["source_selector"] for r in review["records"] if r["kind"] == "progressive"}' '''.strip():
        ''''selectors = {r["source_selector"] for r in review["records"] if r["kind"] == "progressive" and r["source_selector"] < 207}' '''.strip(),
})
scope = previous.scope | globals()
for script in (panels, verification, names):
    exec(compile(script, __file__ + "::stored-native-display", "exec"), scope)


if __name__ == "__main__":
    scope["verify"]()
    scope["verify_names"]()
