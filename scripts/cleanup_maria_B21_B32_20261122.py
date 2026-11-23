"""Clear redundant temporary files after the Maria candidate is verified on Drive."""

from scripts import cleanup_maria_opening_hodram_wraps_20261122 as previous
from scripts import register_maria_B21_B32_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.writer


def redundant_test_files(candidate_sha, patch_sha):
    return {
        stage.ROOT / "clean_rebuilt.nds": candidate_sha,
        stage.ROOT / "translation.xdelta": patch_sha,
    }


source = checked_text(previous.source, {
    '''    hodram = base.load(release.hodram.PROOF)
    retained.update({Path(p):h for p,h in hodram["evidence"].items()})
''': '',
    '''                 *live["return_frames"].values(),*(row["observed"] for row in hodram["holds"]),
                 hodram["final_hold"],*startup["exact_matching_frames"],startup["read_only_snapshot"]]:''':
    '''                 *live["return_frames"].values(), *startup["exact_matching_frames"],
                 startup["read_only_snapshot"]]:''',
    "release.live.REPORT.parent, release.hodram.REPORT.parent, release.STARTUP_CAPTURE.parent":
        "release.live.REPORT.parent, release.STARTUP_CAPTURE.parent",
    "release_stack_with_maria_opening_hodram_wraps.json": "release_stack_with_maria_B21_B32.json",
})
scope = previous.scope | globals()
exec(compile(source, __file__ + "::verified-Maria-cleanup", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()

