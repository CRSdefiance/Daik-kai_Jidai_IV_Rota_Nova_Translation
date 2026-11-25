"""Check remedy-scene text in the stored script and native dialogue renderer."""

from inspect import getsource

from scripts import stage_rafael_B306_B309_20261122 as stage
from scripts import verify_rafael_B161_B169_20261121 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
display = previous.display

verification = checked_text(getsource(previous.verify), {
    'qualified = stage.qualified_panels()': 'qualified = {}',
    'len(entries) == 368 and fe_count == 30': 'len(entries) == 61 and fe_count == 0',
    '"rafael_B161_B169_progressive"': '"rafael_B306_B309_progressive"',
    'panels = base.load(stage.FE_PROOF)["sheets"]': 'panels = []',
})
names_source = getsource(previous.verify_names)
notes_start, notes_end = names_source.index('    notes = {}'), names_source.index('    assert set(notes)')
names = checked_text(names_source, {
    names_source[notes_start:notes_end]: '''    notes = {
        0: "Rafael Castor is the approved full name. Claudio uses the captain's given name when speaking to him.",
        5: "Claudio Manaus is the established personal name. Keep the familiar tone as he reacts to the medicine.",
        19: "Carlo Sinat is the established personal name. The line about Eastern medicine is his reaction.",
        148: "Guildmaster is the source role. The exchange establishes that this guildmaster is the boy's father.",
        162: "Boy is the age-based source label. The father identifies the relationship in his dialogue.",
    }
''',
})
scope = vars(previous) | globals()
for source in (verification, names):
    exec(compile(source, __file__ + "::native-remedy-dialogue", "exec"), scope)


if __name__ == "__main__":
    scope["verify"]()
    scope["verify_names"]()
