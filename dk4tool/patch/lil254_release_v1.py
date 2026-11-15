"""Pure Lil B312–B319 cumulative successor with exact scoped runtime reuse."""

from pathlib import Path

from dk4tool.patch import lil278_release_v1 as previous
from scripts import finalize_lil254_research_v1 as finisher
from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


load, sha, require = previous.load, previous.sha, previous.require
BLOCKS = list(range(312, 320))
FINISHER = Path(finisher.__file__)
replay_source = checked_text(finisher.source, {
    'assert not any(p.exists() for p in [FINAL, NAMES, OUT])': 'assert all(p.exists() for p in [FINAL, NAMES, OUT])',
    '    OUT.mkdir()\n    save(FINAL, doc)\n    save(NAMES, names)': '    assert load(FINAL) == doc\n    assert load(NAMES) == names',
    '    save(source_plan, final_plan)': '    assert load(source_plan) == final_plan',
    "    save(OUT/'research_completion.json', dict(": '    expected_completion = dict(',
    'Path(__file__)]}))': "Path(__file__)]})\n    assert load(OUT/'research_completion.json') == expected_completion",
    "    print('Sealed 254 five-gate reviews and 10 scoped names. Registration and coverage credit remain.')": '',
})
require('save(' not in replay_source and 'mkdir(' not in replay_source, 'read-only complete research rehearsal')
replay_env = {'__file__': str(FINISHER.resolve()), '__name__': 'lil254_complete_research_rehearsal'}
exec(compile(replay_source, str(FINISHER), 'exec'), replay_env)


qualification = checked_text(previous.qualification, {
    '(278, 272, 133, 139, 6, 3, 10, 280, 670, 8, 25121)': '(254, 246, 88, 158, 8, 3, 10, 251, 330, 7, 25841)',
    '13 complete reviewed exchanges': '8 complete reviewed exchanges',
    "for r in stored['records']) == 8, 'eight complete original FE panels'":
        "for r in stored['records']) == 7, 'seven complete original FE panels'",
    'work/Lil278_B299_B311_clean_20261110': 'work/Lil254_B312_B319_clean_20261110',
})
exec(compile(qualification, __file__, 'exec'), globals())

source = checked_text(previous.source, {
    'dk4-reviewed-lil278-release-v1': 'dk4-reviewed-lil254-release-v1',
    "len(styles['objects']) == 18": "len(styles['objects']) == 27",
})
env = {**previous.env, 'qualify_evidence': qualify_evidence, '__file__': __file__}
exec(compile(source, __file__, 'exec'), env)
plan_release = env['plan_release']
