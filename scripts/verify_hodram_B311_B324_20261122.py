"""Check the native expedition displays and source-bound nameplates."""

from inspect import getsource
from types import FunctionType

from scripts import generic_name_macro_owned_v5886b as macro
from scripts import stage_hodram_B311_B324_20261122 as stage
from scripts import verify_hodram_B292_B310_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage":stage})
verify_menu_with_block = FunctionType(previous.verify_menu_with_block.__code__,
    previous.verify_menu_with_block.__globals__ | {"ROOT":ROOT})
panels = checked_text(previous.panels, {
    'assert len(panels) == 17 and len(pictures) == 18': 'assert len(panels) == 21 and len(pictures) == 23',
    '                assert test == [(0, 0, f"{name}{stage.FE_MACROS[ident]}")]':
        '''                if ident == stage.INJURY:
                    expected = preflight["name_width_rows"][name]
                    assert [list(row) for row in test] == expected["rows"]
                    assert native.digest(raster) == expected["raster_sha256"]
                else:
                    assert test == [(0, 0, f"{name}{stage.FE_MACROS[ident]}")]''',
})
def original_expander():
    source = checked_text(getsource(macro.expand), {
        "assert identity==prefix and captain==2":
            "assert captain == 1 and (0 <= identity < 207 if 207 <= prefix < 224 else identity == prefix)",
    })
    env = vars(macro).copy()
    exec(compile(source, __file__ + "::native-roster-roles", "exec"), env)
    return env["expand"]


verification = checked_text(previous.verification, {
    'paint, expand = display.clipped_renderer(ctx), display.original_expander()': 'paint, expand = display.clipped_renderer(ctx), original_expander()',
    'len(entries) == 439 and fe_count == 17 and len(style_objects) == 26':
        'len(entries) == 590 and fe_count == 21 and len(style_objects) == 58',
    '[(294, 2), (300, 2), (302, 2), (302, 2), (304, 2), (309, 3)]':
        '[(294, 2), (302, 2), (302, 2), (309, 3), (311, 2), (311, 2), (313, 3), (316, 2), (316, 2), (317, 2)]',
    'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 175':
        'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 366',
    '"hodram_B292_B310_progressive"': '"hodram_B311_B324_progressive"',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        0: "Rafael Castor remains the approved nameplate for the speaker in the incense-burner scene and for the other searcher. Castor Company is his stated affiliation.",
        1: "Hodram Bergstrom remains the approved caption for the captain. The injury notice uses his given-name substitution.",
        2: "Lil Argot remains the approved caption for the character who recognizes Charles's book in her conditional scene.",
        16: "Gerhard Adernkatz gives the warning about the smoke in the carried forest exchange.",
        18: "Charles Rochefort keeps his approved short label and distinctive excitement about the book.",
        22: "Samwell Khan retains his approved nameplate for the tentative python identification.",
        151: "Sailor is the original shared crew role, including the first alarm, injury reactions and the survey report.",
        161: "Villager is the shared role for the elder's conversations. The dialogue supplies no additional title.",
        179: "Villager is the shared role for the guide and the witness to the monk's death. Individual scenes give them different functions.",
        192: "Matilda gives the Colosseum clue in the carried exchange. Retain her approved spelling.",
        204: "Verisa retains her approved nameplate across the incense-burner request, warning, and fortune.",
        205: "Silvia gives the map rumor. Keep her established spelling and the original captain-name address.",
        206: "Isabel recounts the customer's story about the missing monk and asks the captain to inquire.",
    }
''',
})
scope = previous.scope | globals()
for source in (panels, verification, names):
    exec(compile(source, __file__ + "::native-expeditions", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
