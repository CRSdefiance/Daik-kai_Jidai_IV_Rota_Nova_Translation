"""Remove verified duplicate files after this registered candidate is read back from Drive."""

from scripts import cleanup_maria_B21_B32_20261122 as previous
from scripts import register_maria_hangzhou_followup_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.writer
redundant_test_files = previous.redundant_test_files


def staged_duplicates(candidate_sha, patch_sha):
    return {
        stage.ROOT / "clean_rebuilt.nds": candidate_sha,
        stage.ROOT / "translation.xdelta": patch_sha,
    }


source = checked_text(previous.source, {
    '    retained[release.live.REPORT] = live["report_sha256"]':
        '''    retained[release.live.REPORT] = live["report_sha256"]
    town=base.load(release.town.PROOF)
    retained[release.town.REPORT]=town["report_sha256"]''',
    '''                 *live["return_frames"].values(), *startup["exact_matching_frames"],
                 startup["read_only_snapshot"]]:''':
        '''                 *live["return_frames"].values(), *startup["exact_matching_frames"],
                 startup["read_only_snapshot"], *(panel["capture"] for panel in town["panels"]),
                 *town["observed_unchanged_menu_returns"]]:''',
    "release.live.REPORT.parent, release.STARTUP_CAPTURE.parent":
        "release.live.REPORT.parent, release.town.REPORT.parent, release.STARTUP_CAPTURE.parent",
    "release_stack_with_maria_B21_B32.json": "release_stack_with_maria_hangzhou_followup.json",
})
scope = previous.scope | globals() | {"redundant_test_files":staged_duplicates}
exec(compile(source,__file__+"::story-and-Hangzhou-cleanup","exec"),scope)

if __name__=="__main__":
    scope["main"]()

