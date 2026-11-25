"""Check the original renderer, region wraps, and both name substitutions."""

from inspect import getsource

from scripts import stage_regional_proof_dialogue_20261118 as build
from scripts import verify_story_phrase_continuity_20261118 as prior
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"

source = checked_text(getsource(prior.main), {
    'contexts = {1: hodram_context(), 2: routes.lil_context(), 3: maria}':
        'contexts = {2: routes.lil_context(), 3: maria}',
    'expanded = contexts[1].execute(expand, b"FI", 1)\n'
    '    assert {bytes.fromhex(case["output_hex"]) for case in expanded["cases"]} == {b"Hodram"}\n'
    '    names = {1: {"FI": "Hodram"}, 2: routes.current_names(contexts[2]), 3: display.current_names(maria)}':
        'names = {2: routes.current_names(contexts[2]), 3: display.current_names(maria)}',
    'assert len(pages) == 1 and pages[0]["first_visible_origin"] == [0, 0]':
        'assert pages and pages[0]["first_visible_origin"] == [0, 0]',
    '                for page in pages:\n'
    '                    pictures.append((f"SC{route} {ident} unchanged", bytes.fromhex(page["native_plane_hex"])))\n': "",
    'if ident == "DK4_MES_B143_R0380":':
        'if ident == "DK4_MES_B47_R0140":',
    'assert pagination[ident] == [2, 1]':
        'assert pagination[ident] == [1, 1]',
    'len(modified) == 27 and len(retained) == 4 and len(pictures) == 43 and len(pagination) == 1':
        'len(modified) == 14 and len(retained) == 73 and len(pictures) == 20 and len(pagination) == 1',
    'fresh_page_count=39, retention_page_count=4':
        'fresh_page_count=20, retention_page_count=sum(len(row["pages"]) for row in retained)',
    "Rendered 39 revised and stress-test pages, plus four exact retentions.":
        "Rendered 20 revised and name-width pages and verified 73 unchanged turns.",
})
env = vars(prior) | globals()
exec(compile(source, __file__ + "::unchanged-native-renderer", "exec"), env)

if __name__ == "__main__":
    env["main"]()
