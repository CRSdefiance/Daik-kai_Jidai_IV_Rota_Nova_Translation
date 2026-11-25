"""Remove unnecessary checkpoint copies after the published ROM is verified."""

from scripts import cleanup_rafael_ruins_and_proof_20261121 as prior
from scripts import register_rafael_rescue_and_lessons_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
source = checked_text(prior.source, {
    '"release_stack_with_rafael_ruins_and_proof.json"': '"release_stack_with_rafael_rescue_and_lessons.json"',
    '    assert all(base.digest(path) == h for path, h in retained.items())\n    keep = {path.resolve() for path in retained}':
        '''    for version in ("staged_v2", "staged_v3"):
        checkpoint = stage.ROOT.with_name(version)
        prior_play = base.load(checkpoint / "focused_gameplay/verified_gameplay.json")
        retained.update({Path(p): h for p, h in prior_play["evidence"].items()})
        retained.update({Path(sheet["path"]): sheet["sha256"] for sheet in prior_play["sheets"]})
        for shot in [*(r["observed"] for r in prior_play["holds"] + prior_play["menus"]),
                     prior_play["final_hold"], prior_play.get("reference_final_hold", prior_play["final_hold"])]:
            retained[Path(shot["path"])] = shot.get("PNG_sha256", shot.get("sha256"))
    assert all(base.digest(path) == h for path, h in retained.items())
    keep = {path.resolve() for path in retained}''',
    '    for capture in (earlier / "focused_gameplay/capture", release.live.REPORT.parent,':
        '''    for capture in (earlier / "focused_gameplay/capture",
                    stage.ROOT.with_name("staged_v2") / "focused_gameplay/capture",
                    stage.ROOT.with_name("staged_v3") / "focused_gameplay/capture",
                    release.live.REPORT.parent,''',
})
scope = prior.scope | globals()
exec(compile(source, __file__ + "::checkpoint-cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
