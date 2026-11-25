"""Verify all newly stored Athens and London pages and byte-exact retentions."""
from inspect import getsource

from scripts import stage_athens_london_trends_20261121 as build
from scripts import verify_moonlit_violin_20261121 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native = build.base, build.native
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
NAMES = {}


def main():
    source = checked_text(getsource(prior.main), {
        'assert command == before and raw.strip() == b"..."':
            'assert command == before and build.review.logical(raw.decode()) == row["english"]',
        "len(previews) == 5 and len(results) == 37": "len(previews) == 10 and len(results) == 72",
        "exact_speakerless_pause=not pages": "exact_retained_system_notice=not pages",
        "Five revised native pages passed. The 32 retentions keep their original controls and text.":
            "Ten revised native pages passed. The 62 retentions keep their original controls and text.",
    })
    scope = vars(prior) | globals()
    exec(compile(source, __file__ + "::verify", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
