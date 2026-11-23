"""Verify both Lisbon revisions and the nine byte-exact retentions."""
from inspect import getsource

from scripts import stage_lisbon_fragrance_wraps_20261121 as build
from scripts import verify_moonlit_violin_20261121 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native = build.base, build.native
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
NAMES = {}


def main():
    source = checked_text(getsource(prior.main), {
        "build.review.OUTPUT": "build.author.OUTPUT",
        "build.review.TOKEN": "build.author.TOKEN",
        "build.review.logical": "build.author.logical",
        'assert command == before and raw.strip() == b"..."':
            'assert command == before and build.author.logical(raw.decode()) == row["english"]',
        "len(previews) == 5 and len(results) == 37": "len(previews) == 2 and len(results) == 11",
        "exact_speakerless_pause=not pages": "exact_retained_system_notice=not pages",
        "Five revised native pages passed. The 32 retentions keep their original controls and text.":
            "Two revised Lisbon pages passed. The nine retentions keep their original controls and text.",
    })
    scope = vars(prior) | globals()
    exec(compile(source, __file__ + "::verify-lisbon", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()

