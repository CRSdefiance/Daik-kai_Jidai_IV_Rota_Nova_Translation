"""Verify all 70 revised pages and record changes in native pagination."""

from inspect import getsource

from scripts import stage_all_routes_final_flagged_wraps_20261118 as build
from scripts import verify_all_routes_remaining_phrase_wraps_20261118 as previous
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"

source = checked_text(previous.source, {
    "base.load(build.parent.parent.parent.parent.parent.RELEASE)": "base.load(build.parent.parent.parent.parent.parent.parent.RELEASE)",
    "len(modified) == 31 and len(retained) == 132 and len(pictures) == 31":
        "len(modified) == 70 and len(retained) == 105 and len(pictures) == 70",
    "Verified 31 revised pages and 132 retentions.": "Verified 70 revised pages and 105 retentions.",
})
env = vars(previous.template) | globals()
exec(compile(source, __file__ + "::verify-native-pages", "exec"), env)

if __name__ == "__main__":
    build.verify_staged()
    env["verify"]()
