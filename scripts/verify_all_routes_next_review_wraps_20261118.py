"""Check each stored revision and both preserved FE continuations in the native renderer."""

from inspect import getsource

from scripts import stage_all_routes_next_review_wraps_20261118 as build
from scripts import verify_all_routes_followup_phrase_wraps_20261118 as template
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"

source = checked_text(getsource(template.verify), {
    "base.load(build.parent.parent.RELEASE)": "base.load(build.parent.parent.parent.parent.RELEASE)",
    "modified, retained, pictures = [], [], []": "modified, retained, pictures = [], [], []\n    preserved_pages = []",
    '            assert not build.review.TOKEN.findall(row["english"])':
        '''            assert not build.review.TOKEN.findall(row["english"])
            if ident == "DK4_MES_B116_R0024":
                preserved_pages = plan["exact_original_FE_continuations"]
                assert len(preserved_pages) == 2 and plan["allocation_padding_bytes"] > 0
                for panel in preserved_pages:
                    at = panel["command_offset"]
                    payload = bytes.fromhex(panel["exact_command_hex"])
                    assert block[at:at + len(payload)] == payload''',
    "len(modified) == 18 and len(retained) == 151 and len(pictures) == 18":
        '''len(modified) == 25 and len(retained) == 107 and len(pictures) == 25
    assert [(page["owner_id"], page["command_offset"]) for page in preserved_pages] == [
        ("DK4_MES_B116_R0041", 630), ("DK4_MES_B116_R0051", 1026)]''',
    "contact_sheets=sheets, actual_gameplay=False))":
        "contact_sheets=sheets, preserved_FE_pages=preserved_pages, actual_gameplay=False))",
    "Verified 18 revised pages and 151 exact retentions.":
        "Verified 25 revised pages, 107 retentions, and both exact FE continuations.",
})
env = vars(template) | globals()
exec(compile(source, __file__ + "::native-wrap-and-continuation-verification", "exec"), env)

if __name__ == "__main__":
    env["verify"]()
