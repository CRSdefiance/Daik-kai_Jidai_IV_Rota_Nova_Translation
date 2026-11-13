"""Pure Lil B323–B335 cumulative successor with exact scoped runtime reuse."""

from pathlib import Path

from dk4tool.patch import lil254_release_v1 as previous
from scripts import finalize_lil261_research_v1 as finisher
from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


load, sha, require = previous.load, previous.sha, previous.require
BLOCKS = list(range(323, 336))
FINISHER = Path(finisher.__file__)
replay_source = checked_text(finisher.source, {
    'assert not any(p.exists() for p in [FINAL, NAMES, OUT])': 'assert all(p.exists() for p in [FINAL, NAMES, OUT])',
    '    OUT.mkdir()\n    save(FINAL, doc)\n    save(NAMES, names)': '    assert load(FINAL) == doc\n    assert load(NAMES) == names',
    '    save(source_plan, final_plan)': '    assert load(source_plan) == final_plan',
    "    save(OUT/'research_completion.json', dict(": '    expected_completion = dict(',
    'Path(__file__)]}))': "Path(__file__)]})\n    assert load(OUT/'research_completion.json') == expected_completion",
    "    print('Sealed 261 five-gate reviews and nine scoped names. Registration and coverage credit remain.')": '',
})
require('save(' not in replay_source and 'mkdir(' not in replay_source, 'read-only complete research rehearsal')
replay_env = {'__file__': str(FINISHER.resolve()), '__name__': 'lil261_complete_research_rehearsal'}
exec(compile(replay_source, str(FINISHER), 'exec'), replay_env)

qualification = checked_text(previous.qualification, {
    "(254, 246, 88, 158, 8, 3, 10, 251, 330, 7, 25841)": "(261, 255, 136, 119, 6, 3, 9, 258, 455, 13, 26561)",
    "8 complete reviewed exchanges": "13 complete reviewed exchanges",
    "10 scoped name reviews": "9 scoped name reviews",
    "== 7, 'seven complete original FE panels'": "== 13, '13 complete original FE panels'",
    "Lil254_B312_B319_clean_20261110": "Lil261_B323_B335_clean_20261110",
})
exec(compile(qualification, __file__, 'exec'), globals())

source = checked_text(previous.source, {
    'dk4-reviewed-lil254-release-v1': 'dk4-reviewed-lil261-release-v1',
    "len(styles['objects']) == 27": "len(styles['objects']) == 18",
})
env = {**previous.env, 'qualify_evidence': qualify_evidence, '__file__': __file__}
exec(compile(source, __file__, 'exec'), env)
plan_release = env['plan_release']
