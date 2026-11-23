"""Remove verified duplicates at the encounters and letters checkpoint."""

from pathlib import Path

from scripts import cleanup_hodram_B181_B200_20261122 as previous
from scripts import register_hodram_B201_B220_20261122 as release
from scripts import stage_hodram_B201_B220_20261122 as initial
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage


def redundant_test_files(candidate_sha, patch_sha):
    first, corrected = map(base.load, (release.display.INITIAL_PROOF, release.display.PROOF))
    replacements = {entry["sha256"] for entry in corrected["sheets"]}
    old_files = {Path(menu["sheet"]["path"]) for menu in first["menus"]}
    assert len(old_files) == 5
    duplicates = {path: base.digest(path) for path in old_files}
    assert all(sha in replacements for sha in duplicates.values())
    return duplicates | {
        stage.ROOT / "clean_rebuilt.nds": candidate_sha,
        stage.ROOT / "translation.xdelta": patch_sha,
        initial.ROOT / "clean_rebuilt.nds": base.digest(initial.ROM),
    }


source = checked_text(previous.source, {
    '"release_stack_with_hodram_B181_B200.json"': '"release_stack_with_hodram_B201_B220.json"',
})
scope = previous.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
