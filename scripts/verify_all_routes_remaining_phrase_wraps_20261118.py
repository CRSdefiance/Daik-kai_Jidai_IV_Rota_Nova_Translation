"""Verify all revised pages and record each change in native pagination."""

from inspect import getsource

from scripts import stage_all_routes_remaining_phrase_wraps_20261118 as build
from scripts import verify_all_routes_followup_phrase_wraps_20261118 as template
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"

source = checked_text(getsource(template.verify), {
    "base.load(build.parent.parent.RELEASE)": "base.load(build.parent.parent.parent.parent.parent.RELEASE)",
    "modified, retained, pictures = [], [], []": "modified, retained, pictures = [], [], []\n    pagination = {}",
    '            pictures.append((f"SC{route} {ident}", bytes.fromhex(page["native_plane_hex"])))':
        '''            pictures.append((f"SC{route} {ident}", bytes.fromhex(page["native_plane_hex"])))
            original = bytes.fromhex(cmd["current"])
            prior_body = prior.prior.default_text(original[6:original.index(0, 6)], names[route])
            old_renderer = paint if prior_body.isascii() else paint_cp932
            old_pages = len(old_renderer(arm, font, prior_body)["pages"])
            if old_pages != 1:
                pagination[ident] = [old_pages, 1]''',
    "len(modified) == 18 and len(retained) == 151 and len(pictures) == 18":
        "len(modified) == 31 and len(retained) == 132 and len(pictures) == 31",
    "contact_sheets=sheets, actual_gameplay=False))":
        "contact_sheets=sheets, pagination_before_after=pagination, actual_gameplay=False))",
    '    print("Verified 18 revised pages and 151 exact retentions.")':
        '    print(f"Verified 31 revised pages and 132 retentions. Pagination changes: {pagination}")',
})
env = vars(template) | globals()
exec(compile(source, __file__ + "::verify-native-pages", "exec"), env)

if __name__ == "__main__":
    env["verify"]()
