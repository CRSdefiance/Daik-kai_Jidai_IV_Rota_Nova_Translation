"""Check staged Hodram dialogue, native alternatives, and existing role labels."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import stage_hodram_opening_20261122 as stage
from scripts import verify_hodram_alexandria_tutorial_20261121 as historical
from scripts import verify_rafael_B221_B240_20261122 as template
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = stage.base, stage.native, stage.parent
PATH = stage.paired.ARCHIVE
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
DEFAULT_NAMES = {"FI": "Hodram", "FA": "Bergstrom", "FO": "Bergstrom Fleet", "FU": "Hodram Joakim Bergstrom"}
CONTEXT_SHORT_NAMES = {
    "DK4_MES_B44_R0021": ("Lil", "Lil Argot"),
    "DK4_MES_B44_R0084": ("Camille", "Camille Overijssel"),
}
display = template.display
inherited = template.previous.previous.previous.previous
check_progressive = FunctionType(inherited.check_progressive.__code__,
    inherited.check_progressive.__globals__ | {"DEFAULT_NAMES": DEFAULT_NAMES, "stage": stage})


def current_runtime(image):
    release = historical.stage.parent.RELEASE
    startup = historical.ROOT / "ordinary_Hodram_snapshot.json"
    old = base.load(historical.PROOF)
    prior = base.load(release)
    assert base.load(startup)["candidate_sha256"] == prior["candidate_sha256"]
    assert old["candidate_sha256"] == base.digest(historical.stage.ROM)
    runtime = native.RegisteredRuntime(release, startup, captain=1)
    assert all(runtime.image.read_file(path) == image.read_file(path) for path in display.ASSETS)
    return runtime


panel_source = checked_text(getsource(template.qualified_panels), {"len(panels) == 3": "len(panels) == 9"})
style_source = checked_text(getsource(template.styles.parts), {r'b"\0\xd0"': r'b"\0\xd6"'})
style_scope = vars(template.styles).copy()
exec(compile(style_source, __file__ + "::lookout-selector", "exec"), style_scope)
styles = SimpleNamespace(parts=style_scope["parts"])
verification = checked_text(template.verification, {
    'len(entries) == 270 and fe_count == 3 and len(style_objects) == 4':
        'len(entries) == 120 and fe_count == 9 and len(style_objects) == 1',
    '[224, 224, 233] and [m["count"] for m in choices] == [2, 3, 2]':
        '[49, 52] and [m["count"] for m in choices] == [2, 2]',
    '"rafael_B221_B240_progressive"': '"hodram_B24_B53_progressive"',
    '(stage.PROOF, stage.MANUSCRIPT)': '(stage.PROOF, stage.OUTPUT)',
    'base.digest(stage.MANUSCRIPT)': 'base.digest(stage.OUTPUT)',
})
original_names = getsource(inherited.verify_names)
start, end = original_names.index("    notes = {}"), original_names.index("    assert set(notes)")
names = checked_text(original_names, {
    original_names[start:end]: '''    notes = {
        1: "Hodram Bergstrom is the installed short nameplate. The full-name substitution remains Hodram Joakim Bergstrom.",
        2: "Lil Argot is the approved company captain. Her challenge and bargaining keep her own direct voice.",
        9: "Camille Overijssel is the approved name. Camille tries to de-escalate Lil's argument and leaves with her.",
        16: "Gerhard Adernkatz is the established officer name. He formally asks Hodram to address the crew.",
        18: "Charles Rochefort is the established officer name. He relays the warning and comments on the fleet budget.",
        23: "Manuel Almeida is the established officer name. His dry proverb follows Hodram's reaction to Lil.",
        71: "William Clive is the established personal name. His curses come after capture, with no added title.",
        72: "Hernan Berio is the established personal name. He tries to save face after defeat.",
        73: "Iscal Yasar is the established personal name. Both cries retain the same speaker and portrait.",
        113: "Port Worker is the localized source role. His traffic and territorial advice give no distinct rank or proper name.",
    }
''',
    'base.load(stage.MANUSCRIPT)': 'base.load(stage.OUTPUT)',
    'OUTPUT=stage.MANUSCRIPT': 'OUTPUT=stage.OUTPUT',
    'if r["kind"] == "progressive"}': 'if r["kind"] == "progressive" and r["source_selector"] < 207}',
    ''''selectors = {r["source_selector"] for r in review["records"] if r["kind"] == "progressive"}' '''.strip():
        ''''selectors = {r["source_selector"] for r in review["records"] if r["kind"] == "progressive" and r["source_selector"] < 207}' '''.strip(),
    '    scope = vars(names) |': '''    source = checked_text(source, {
        "captain=0": "captain=1",
        'assert {r["speaker"] for r in review["records"] if r["source_selector"] == ident} == {getters[0]["text"]}':
            'for row in (r for r in review["records"] if r["source_selector"] == ident):\\n'
            '            source, displayed = CONTEXT_SHORT_NAMES.get(row["id"], (row["speaker"], row["speaker"]))\\n'
            '            assert row["speaker"] == source and displayed == getters[0]["text"]',
        'offline_native_getters_only=True': 'contextual_short_labels=CONTEXT_SHORT_NAMES, offline_native_getters_only=True',
    })
    scope = vars(names) | {"CONTEXT_SHORT_NAMES": CONTEXT_SHORT_NAMES} |''',
})
scope = template.scope | globals()
for source in (panel_source, verification, names):
    exec(compile(source, __file__ + "::hodram-native-display", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
