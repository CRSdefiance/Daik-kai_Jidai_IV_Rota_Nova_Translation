"""Clear redundant checkpoint artifacts after the registered Drive handoff."""

from scripts import cleanup_hodram_B81_B89_20261122 as previous
from scripts import register_hodram_B111_B130_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage


def redundant_test_files(candidate_sha, patch_sha):
    former = stage.ROOT.with_name("B111_B130_staged_v2")
    prior_rom = former / stage.ROM.name
    prior_copy = former / "clean_rebuilt.nds"
    prior_sha = base.digest(prior_rom)
    assert prior_sha == "e6a5d16f0953cd7f04c111f31f91682e84ebf8150d97b208ef57d4bfb5eb846d"
    assert prior_sha != candidate_sha and base.digest(prior_copy) == prior_sha
    return {prior_copy: prior_sha, stage.ROOT / "clean_rebuilt.nds": candidate_sha,
            stage.ROOT / "translation.xdelta": patch_sha}


source = checked_text(previous.source, {
    '"release_stack_with_hodram_B81_B89.json"': '"release_stack_with_hodram_B111_B130.json"',
})
scope = previous.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

