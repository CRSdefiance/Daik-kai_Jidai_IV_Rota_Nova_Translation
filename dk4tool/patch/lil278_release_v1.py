"""Pure Lil B299–B311 cumulative successor with exact scoped runtime reuse."""

import inspect
from pathlib import Path

from dk4tool.patch import lil269_release_v1 as previous
from scripts import finalize_lil278_research_v1 as finisher
from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


load, sha, require = previous.load, previous.sha, previous.require
BLOCKS = list(range(299, 312))
FINISHER = Path(finisher.__file__)
replay_source = checked_text(finisher.source, {
    'assert not any(p.exists() for p in [FINAL, NAMES, OUT])': 'assert all(p.exists() for p in [FINAL, NAMES, OUT])',
    '    OUT.mkdir()\n    save(FINAL, doc)\n    save(NAMES, names)': '    assert load(FINAL) == doc\n    assert load(NAMES) == names',
    '    save(source_plan, final_plan)': '    assert load(source_plan) == final_plan',
    "    save(OUT/'research_completion.json', dict(": '    expected_completion = dict(',
    'Path(__file__)]}))': "Path(__file__)]})\n    assert load(OUT/'research_completion.json') == expected_completion",
    "    print('Sealed 278 five-gate reviews and 10 scoped names. Registration and coverage credit remain.')": '',
})
require('save(' not in replay_source and 'mkdir(' not in replay_source, 'read-only complete research rehearsal')
replay_env = {'__file__': str(FINISHER.resolve()), '__name__': 'lil278_complete_research_rehearsal'}
exec(compile(replay_source, str(FINISHER), 'exec'), replay_env)


qualification = checked_text(inspect.getsource(previous.qualify_evidence), {
    '(269, 262, 246, 16, 7, 3, 25, 264, 990, 36, 64563)': '(278, 272, 133, 139, 6, 3, 10, 280, 670, 8, 25121)',
    '40 complete reviewed exchanges': '13 complete reviewed exchanges',
    '25 scoped name reviews': '10 scoped name reviews',
    """    require(native['runtime']['candidate_sha256'] == conf['parent_ROM_sha256']
        and native['runtime']['ARM9_sha256'] == conf['pre_runtime_ARM9_sha256'], 'exact parent runtime')""":
        """    runtime = native['runtime']
    ctx = RegisteredRuntime(runtime['release_proof'], runtime['startup_proof'], captain=conf['captain'])
    require(ctx.receipt() == runtime and runtime['ARM9_sha256'] == conf['pre_runtime_ARM9_sha256'], 'exact native runtime')
    scope = qualified_current_native_context(doc, ctx)
    require(scope == rebuilt['native_context_reuse'] == stored['native_context_reuse']
        and scope['target_candidate_sha256'] == conf['parent_ROM_sha256'], 'exact registered parent and scope dependencies')""",
    "for r in stored['records']) == 36, '36 complete original FE panels'":
        "for r in stored['records']) == 8, 'eight complete original FE panels'",
    "for index in range(3):": "for index in range(1):",
    "Path('work/Lil269_B243_B282_clean_20261110') / f'display_run{index}_v1/run_plan.json'":
        "Path('work/Lil278_B299_B311_clean_20261110') / f'actual_run{index}_v1/run_plan.json'",
})
exec(compile(qualification, __file__, 'exec'), globals())

source = checked_text(previous.source, {
    'dk4-reviewed-lil269-release-v1': 'dk4-reviewed-lil278-release-v1',
    "len(styles['objects']) == 2": "len(styles['objects']) == 18",
})
env = {**previous.env, 'qualify_evidence': qualify_evidence, '__file__': __file__}
exec(compile(source, __file__, 'exec'), env)
plan_release = env['plan_release']
