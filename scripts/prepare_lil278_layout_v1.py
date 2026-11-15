"""Run the existing prose and layout gates against Lil361 with qualified runtime reuse."""
import argparse
import inspect
import linecache
from pathlib import Path
import sys

from scripts import finalize_clean_editorial_prose_v2 as prose_gate
from scripts.prepare_lil278_prose_v1 import PROSE, ROOT
from scripts.source_locked_derivation_v5118 import checked_text

CAPTAIN_FORMATTER = Path('scripts/prepare_captain_clean_formatting_v1.py')
CAPTAIN_PLANNER = Path('scripts/plan_captain_clean_editorial_v1.py')


def run_prose_gate():
    source = checked_text(prose_gate.source, {
        "runtime=runtime,current_ROM=runtime['candidate'],current_ROM_sha256=runtime['candidate_sha256'],": """
        runtime=runtime,current_ROM=proposals['current_ROM'],current_ROM_sha256=proposals['current_ROM_sha256'],
        exact_existing_native_context_reuse=proposals['exact_native_context_reuse'],
""".strip(),
        "    assert len(terms['items'])==cfg['item_bindings']": """    assert len(terms['items'])==cfg['item_bindings']
    reuse = proposals['exact_native_context_reuse']
    assert reuse == terms['exact_native_context_reuse'] and reuse['native_runtime'] == runtime
    assert reuse['target_candidate'] == proposals['current_ROM']
    assert reuse['target_candidate_sha256'] == digest(proposals['current_ROM']) == proposals['current_ROM_sha256']
    assert digest(reuse['target_release']) == reuse['target_release_sha256']""",
    })
    sys.argv = [sys.argv[0], '--config', str(ROOT / 'prose_config_v1.json')]
    env = {**prose_gate.env, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


def run_formatter():
    source = checked_text(CAPTAIN_FORMATTER.read_text(encoding='utf-8'), {
        "args.root/'dynamic_roles_current_v1.json'": "args.root/'dynamic_roles_all_v1.json'",
        "    assert ctx.receipt()==runtime and digest('translations/release_stack.json')==ctx.release['registry_sha256']":
            """    assert ctx.receipt() == runtime
    from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
    assert qualified_current_native_context(doc, ctx) == current['exact_native_context_reuse']""",
    })
    prior = 'work/Lil361_B283_B298_clean_20261110/formatting_v1/native_macro_measurements.json'
    sys.argv = [sys.argv[0], '--root', str(ROOT), '--prose', str(PROSE),
        '--FE-source-macros', prior, '--captain', '2']
    exec(compile(source, __file__, 'exec'), {'__file__': __file__, '__name__': '__main__'})


def run_planner(arguments):
    from scripts import plan_hodram_B211_B230_v2 as planner
    retention_guard = checked_text(inspect.getsource(planner.main), {
        "assert row['id'] in {'DK4_MES_B142_R0159','DK4_MES_B201_R0074'}":
            """assert row['id'] in {'DK4_MES_B142_R0159','DK4_MES_B201_R0074'} or (
                    row['id'] == 'SC2_B299_STYLE_1816_50'
                    and row['english'] == 'Admiral, that was uncalled for. You just took off...'
                    and retention.get('line_index') == 0
                    and retention['exact_line'] == 'Admiral, that was uncalled for.')""",
    })
    filename = __file__ + '::complete-uncalled-for-sentence'
    linecache.cache[filename] = (len(retention_guard), None, retention_guard.splitlines(keepends=True), filename)
    env = {**planner.main.__globals__, '__file__': __file__}
    exec(compile(retention_guard, filename, 'exec'), env)
    planner.main = env['main']
    strict_identity = "    assert digest(doc['current_ROM'])==doc['current_ROM_sha256']==doc['runtime']['candidate_sha256']"
    qualified_identity = """    from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
    from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
    runtime = doc['runtime']
    ctx = RegisteredRuntime(runtime['release_proof'], runtime['startup_proof'], captain=runtime['captain'])
    assert ctx.receipt() == runtime
    assert digest(doc['current_ROM']) == doc['current_ROM_sha256']
    assert qualified_current_native_context(doc, ctx) == current['exact_native_context_reuse']"""
    entry = "    source = checked_text(Path('scripts/plan_maria301_v1.py').read_text(encoding='utf-8'), {"
    source = checked_text(CAPTAIN_PLANNER.read_text(encoding='utf-8'), {
        entry: f'{entry}\n        {strict_identity!r}: {qualified_identity!r},',
    })
    sys.argv = [sys.argv[0], '--root', str(ROOT), *arguments]
    exec(compile(source, __file__, 'exec'), {'__file__': __file__, '__name__': '__main__'})


def main():
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser.add_argument('stage', choices=['prose', 'format', 'plan'])
    args, remaining = parser.parse_known_args()
    if args.stage == 'plan':
        run_planner(remaining)
    else:
        assert not remaining
        (run_prose_gate if args.stage == 'prose' else run_formatter)()


if __name__ == '__main__':
    main()
