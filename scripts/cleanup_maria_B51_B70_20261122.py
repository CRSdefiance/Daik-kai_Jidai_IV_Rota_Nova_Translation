"""Remove verified duplicates after the updated Maria testing candidate is read back from Drive."""

from scripts import cleanup_maria_B21_B32_20261122 as previous
from scripts import register_maria_B51_B70_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text

base, stage = release.base, release.writer


def redundant_test_files(candidate_sha, patch_sha):
    return {
        stage.ROOT/"clean_rebuilt.nds":candidate_sha,
        stage.ROOT/"translation.xdelta":patch_sha,
    }


source = checked_text(previous.source, {
    "release_stack_with_maria_B21_B32.json":"release_stack_with_maria_B51_B70.json",
})
scope = previous.scope | globals()
exec(compile(source,__file__+"::verified-Maria-cleanup","exec"),scope)

if __name__=="__main__":
    scope["main"]()

