"""Remove verified redundant files from the Hodram assignments and expedition checkpoint."""

from scripts import cleanup_hodram_B241_B260_20261122 as previous
from scripts import register_hodram_B261_B291_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage


def redundant_test_files(candidate_sha, patch_sha):
    draft = stage.OUTPUT.with_name("B261_B291_scoped_manuscript_v1.json")
    before, after = map(base.load, (draft, stage.OUTPUT))
    assert before.pop("planned_FE") == {}
    assert set(after.pop("planned_FE")) == {"DK4_MES_B291_R0119"}
    assert before == after
    return {stage.ROOT / "clean_rebuilt.nds":candidate_sha, stage.ROOT / "translation.xdelta":patch_sha,
            draft:base.digest(draft)}


source = checked_text(previous.source, {
    '"release_stack_with_hodram_B241_B260.json"': '"release_stack_with_hodram_B261_B291.json"',
})
scope = previous.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
