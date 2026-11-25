"""Verify the complete revised pages, name substitutions, and exact Sphinx continuation."""

from inspect import getsource

from scripts import stage_all_routes_continuing_phrase_wraps_20261118 as build
from scripts import verify_all_routes_followup_phrase_wraps_20261118 as template
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
prior = template.prior.prior
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"

source = checked_text(getsource(template.verify), {
    "base.load(build.parent.parent.RELEASE)": "base.load(build.parent.parent.parent.RELEASE)",
    "modified, retained, pictures = [], [], []": "modified, retained, pictures = [], [], []\n    pagination, sphinx = {}, None",
    '''            assert not build.review.TOKEN.findall(row["english"])''':
        '''            tokens = build.review.TOKEN.findall(row["english"])
            assert tokens == (["FI"] if ident == "DK4_MES_B87_R0198" else [])
            if tokens:
                sphinx = plan["exact_original_FE_continuation"]
                at = sphinx["command_offset"]
                raw_extra = bytes.fromhex(sphinx["exact_command_hex"])
                assert at == 712 and block[at:at + len(raw_extra)] == raw_extra''',
    '''            layout, = entry["layouts"]
            page, = layout["pages"]
            pictures.append((f"SC{route} {ident}", bytes.fromhex(page["native_plane_hex"])))''':
        '''            for layout in entry["layouts"]:
                page, = layout["pages"]
                pictures.append((f"SC{route} {ident} {layout['scope']}", bytes.fromhex(page["native_plane_hex"])))
            if ident == "DK4_MES_B252_R0116":
                older = bytes.fromhex(cmd["current"])
                old_body = older[6:older.index(0, 6)]
                pagination[ident] = [len(paint(arm, font, old_body)["pages"]), len(entry["layouts"][0]["pages"])]''',
    "len(modified) == 18 and len(retained) == 151 and len(pictures) == 18":
        '''len(modified) == 24 and len(retained) == 134 and len(pictures) == 27
    assert pagination == {"DK4_MES_B252_R0116": [2, 1]} and sphinx is not None''',
    '''        checked_records=modified, retained_records=retained, contact_sheets=sheets, actual_gameplay=False))''':
        '''        checked_records=modified, retained_records=retained, contact_sheets=sheets, actual_gameplay=False,
        pagination_before_after=pagination, exact_original_sphinx_continuation=sphinx))''',
    "Verified 18 revised pages and 151 exact retentions.":
        "Verified 24 revised pages, three name-width cases and 134 retentions. The tavern handover is one page.",
})
env = vars(template) | {"build": build, "ROOT": ROOT, "PROOF": PROOF}
exec(compile(source, __file__ + "::all-pages-and-protected-continuation", "exec"), env)

if __name__ == "__main__":
    env["verify"]()
