"""Clear redundant checkpoint files after release and verified Drive readback."""

from scripts import cleanup_hodram_B81_B89_20261122 as previous
from scripts import register_hodram_B91_B110_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage


def redundant_test_files(candidate_sha, patch_sha):
    prior_stage = stage.ROOT.with_name("B91_B110_staged")
    prior_rom = prior_stage / stage.ROM.name
    prior_copy = prior_stage / "clean_rebuilt.nds"
    prior_sha = base.digest(prior_rom)
    assert prior_sha == "4b6cf0bfb70bfc88cebf3a3e573855cdd246b2957609c0115e29d8eaa78053d0"
    assert prior_sha != candidate_sha and base.digest(prior_copy) == prior_sha
    redundant = {
        prior_copy: prior_sha,
        stage.ROOT / "clean_rebuilt.nds": candidate_sha,
        stage.ROOT / "translation.xdelta": patch_sha,
    }
    # Reuse the accepted touch-run captures when a rejected startup capture is byte-identical.
    rejected = stage.ROOT / "startup/capture"
    accepted = release.STARTUP_CAPTURE.parent
    for path in rejected.rglob("*"):
        if path.is_file() and path.suffix in {".png", ".dsv", ".bin"}:
            twin = accepted / path.relative_to(rejected)
            if twin.is_file() and base.digest(path) == base.digest(twin):
                redundant[path] = base.digest(twin)
    return redundant


source = checked_text(previous.source, {
    '"release_stack_with_hodram_B81_B89.json"': '"release_stack_with_hodram_B91_B110.json"',
    '    retained.update({Path(p): h for p, h in (visual | live["evidence"]).items()})': '''    branch = base.load(release.branches.PROOF)
    assert branch["candidate_sha256"] == sha
    retained.update({Path(p): h for p, h in (visual | live["evidence"] | branch["evidence"]).items()})
    retained[release.branches.PROOF] = base.digest(release.branches.PROOF)
    for result in branch["outcomes"].values():
        for shot in (result["choice_frame"], result["final_frame"], *(row["screenshot"] for row in result["notices"])):
            retained[Path(shot["path"])] = shot["PNG_sha256"]''',
    'captures = [release.live.REPORT.parent, release.STARTUP_CAPTURE.parent]':
        'captures = [release.live.REPORT.parent, release.STARTUP_CAPTURE.parent,\n'
        '                *(release.branches.branch.ROOT / mode / "capture" for mode in release.branches.NOTICE_PAIRS)]',
})
scope = previous.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

