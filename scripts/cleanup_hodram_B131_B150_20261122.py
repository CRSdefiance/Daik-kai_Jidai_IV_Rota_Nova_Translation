"""Remove redundant artifacts after the registered Drive handoff."""

from scripts import cleanup_hodram_B81_B89_20261122 as previous
from scripts import register_hodram_B131_B150_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base,stage = release.base,release.stage


def redundant_test_files(candidate_sha,patch_sha):
    earlier = stage.ROOT.with_name("B131_B150_staged_v1")
    first = base.digest(earlier/stage.ROM.name)
    assert first == "4e3719b6c1269928698b9ae34746a89dab8e2771bf0143c050e4e80b93652719"
    assert first != candidate_sha and base.digest(earlier/"clean_rebuilt.nds") == first
    return {earlier/"clean_rebuilt.nds":first,stage.ROOT/"clean_rebuilt.nds":candidate_sha,
            stage.ROOT/"translation.xdelta":patch_sha}


source = checked_text(previous.source, {
    '"release_stack_with_hodram_B81_B89.json"':'"release_stack_with_hodram_B131_B150.json"',
})
scope = previous.scope | globals()
exec(compile(source,__file__+"::checkpoint-cleanup","exec"),scope)


if __name__ == "__main__":
    scope["main"]()

