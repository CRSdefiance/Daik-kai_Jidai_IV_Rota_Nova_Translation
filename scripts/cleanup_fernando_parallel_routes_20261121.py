"""Remove redundant non-ROM staging files after the verified release."""
from inspect import getsource
from pathlib import Path

from scripts import cleanup_parallel_ship_lessons_20261121 as template
from scripts import register_fernando_parallel_routes_20261121 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage


main_source = checked_text(getsource(template.main), {
    '    fixture = base.load(release.live.replay.ROOT / "fixture.json")':
        '    fixtures = [base.load(release.live.replay.ROOT / f"route{r}/fixture.json") for r in (1, 2)]',
    'Path(fixture["fixture"]): fixture["fixture_sha256"]}':
        '**{Path(fixture["fixture"]): fixture["fixture_sha256"] for fixture in fixtures}}',
    '"release_stack_with_parallel_ship_lessons.json"': '"release_stack_with_fernando_parallel_routes.json"',
})
scope = vars(template) | globals()
exec(compile(main_source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
