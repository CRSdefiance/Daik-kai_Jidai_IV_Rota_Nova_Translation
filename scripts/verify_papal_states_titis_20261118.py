"""Verify the source-bound Papal States and Titis pages in the original renderer."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import research_lil_B209_native_pages_v6461 as renderer
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.square_shopkeeper_font_oracles_v7020 import _expected
from scripts import stage_papal_states_titis_20261118 as build
from scripts import verify_story_phrase_continuity_20261118 as prior
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"


def source_pause(arm, font, text):
    assert text == bytes.fromhex("816381638163")
    receipt = Path("work/analysis/lil_B234_native_pages_v7587/all18_paragraphs18_complete_native_pages144_alignments.json")
    prior = base.load(receipt)
    old = next(row["pages"][0] for row in prior["records"] if row["compiled_hex"] == "68816381638163")
    adapter = checked_text(prior["source_owned_2b6_page_adapter"], {
        "2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a": native.digest(arm),
    })
    namespace = vars(renderer) | {"expected_pixels": _expected, "codes": codes}
    exec(compile(adapter, __file__ + "::original-CP932-pause", "exec"), namespace)
    out = namespace["pages"](arm, font, text)
    page, = out["pages"]
    assert base.digest(old["native_plane"]) == old["native_plane_sha256"]
    assert native.digest(bytes.fromhex(page["native_plane_hex"])) == old["native_plane_sha256"]
    return out


snapshot = checked_text(getsource(prior.hodram_context), {
    "hodram_context": "rafael_context",
    "hodram_snapshot": "rafael_snapshot",
    "hodram_native_context": "rafael_native_context",
    "hodram_native_ROM_identity": "rafael_native_ROM_identity",
    "actual_captain_getter=1": "actual_captain_getter=0",
    "captain=1": "captain=0",
})
env = vars(prior) | globals()
env["hodram_context"] = prior.hodram_context
exec(compile(snapshot, __file__ + "::rafael-context", "exec"), env)

source = checked_text(getsource(prior.main), {
    "contexts = {1: hodram_context(), 2: routes.lil_context(), 3: maria}":
        "contexts = {0: rafael_context(), 1: hodram_context(), 2: routes.lil_context(), 3: maria}",
    "captain in (1, 2, 3)": "captain in range(4)",
    '    expanded = contexts[1].execute(expand, b"FI", 1)\n'
    '    assert {bytes.fromhex(case["output_hex"]) for case in expanded["cases"]} == {b"Hodram"}\n'
    '    names = {1: {"FI": "Hodram"}, 2: routes.current_names(contexts[2]), 3: display.current_names(maria)}':
        '    names = {0: {"FI": "Rafael"}, 1: {"FI": "Hodram"}, 2: routes.current_names(contexts[2]), 3: display.current_names(maria)}\n'
        '    for route in (0, 1):\n'
        '        expanded = contexts[route].execute(expand, b"FI", route)\n'
        '        assert {bytes.fromhex(case["output_hex"]) for case in expanded["cases"]} == {names[route]["FI"].encode("ascii")}',
    '                for page in pages:\n'
    '                    pictures.append((f"SC{route} {ident} unchanged", bytes.fromhex(page["native_plane_hex"])))\n': "",
    '            if route == 0:\n'
    '                assert not build.review.TOKEN.search(row["english"])\n': "",
    '''            if ident == "DK4_MES_B143_R0380":
                old = bytes.fromhex(cmd["current"])
                before = paint(maria.arm, font, old[6:old.index(0, 6)])
                pagination[ident] = [len(before["pages"]), len(result["layouts"][0]["pages"])]
                assert pagination[ident] == [2, 1]
''': "",
    'surface = paint(maria.arm, font, value[1:])':
        'if value.hex() == row["source_hex"] == "68816381638163":\n'
        '                    surface = source_pause(maria.arm, font, value[1:])\n'
        '                else:\n'
        '                    surface = paint(maria.arm, font, value[1:])',
    'len(modified) == 27 and len(retained) == 4 and len(pictures) == 43 and len(pagination) == 1':
        'len(modified) == 49 and len(retained) == 35 and len(pictures) == 61',
    '    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(pictures)':
        '''    identical = {}
    for label, plane in pictures:
        identical.setdefault(plane, []).append(label)
    unique = [(labels[0], plane) for plane, labels in identical.items()]
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(unique)''',
    "fresh_page_count=39, retention_page_count=4": "fresh_page_count=61, retention_page_count=35",
    "retained_records=retained, pagination_before_after=pagination, contact_sheets=sheets":
        "retained_records=retained, pagination_before_after=pagination, contact_sheets=sheets, "
        "unique_visual_pages=len(unique), identical_plane_labels=[labels for labels in identical.values()]",
    'print("Rendered 39 revised and stress-test pages, plus four exact retentions.")':
        'print(f"Checked 61 revised and name-width pages ({len(unique)} distinct pictures) and 35 exact retentions.")',
})
exec(compile(source, __file__ + "::original-renderer", "exec"), env)

if __name__ == "__main__":
    env["main"]()
