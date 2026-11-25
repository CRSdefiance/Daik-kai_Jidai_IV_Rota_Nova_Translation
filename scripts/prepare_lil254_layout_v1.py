"""Run the reviewed Lil prose and native layout workflow for B312–B319."""

import argparse
import sys
from types import FunctionType

from scripts import prepare_lil278_layout_v1 as previous
from scripts.prepare_lil254_prose_v1 import PROSE, ROOT
from scripts.source_locked_derivation_v5118 import checked_text


def plan(arguments):
    entry = "    source = checked_text(Path('scripts/plan_maria301_v1.py').read_text(encoding='utf-8'), {"
    identity = "    assert digest(doc['current_ROM'])==doc['current_ROM_sha256']==doc['runtime']['candidate_sha256']"
    scope = """    from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
    from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
    runtime = doc['runtime']
    ctx = RegisteredRuntime(runtime['release_proof'], runtime['startup_proof'], captain=runtime['captain'])
    assert ctx.receipt() == runtime
    assert digest(doc['current_ROM']) == doc['current_ROM_sha256']
    assert qualified_current_native_context(doc, ctx) == current['exact_native_context_reuse']"""
    zero = """    zero_rows = [row for row in doc['records'] if row.get('source_selector') == 0]
    assert {row['id']: (row['block'], row['source_reference']['offset'], row['current_reference']['offset'])
            for row in zero_rows} == {'DK4_MES_B317_R0030': (317, 249, 249),
                                    'DK4_MES_B317_R0043': (317, 383, 383)}
    for row in zero_rows:
        assert row['kind'] == 'progressive' and not row.get('native_object_kind')
        assert row['source_complete_preamble_hex'] == '0040ffff0000'
        assert bytes.fromhex(row['source_hex'])[0] == bytes.fromhex(row['current_hex'])[0] == 0
        assert b'\\0' not in bytes.fromhex(row['source_hex'])[1:]
    return {bytes.fromhex(row['source_hex']) for row in zero_rows}, bindings"""
    source = checked_text(previous.CAPTAIN_PLANNER.read_text(encoding='utf-8'), {
        entry: f"{entry}\n        {identity!r}: {scope!r},\n        {'    return set(),bindings'!r}: {zero!r},",
    })
    sys.argv = [sys.argv[0], '--root', str(ROOT), *arguments]
    exec(compile(source, __file__, 'exec'), {'__file__': __file__, '__name__': '__main__'})


def main():
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser.add_argument('stage', choices=('prose', 'format', 'plan'))
    args, remaining = parser.parse_known_args()
    if args.stage == 'plan':
        plan(remaining)
        return
    original = {'prose': previous.run_prose_gate, 'format': previous.run_formatter}[args.stage]
    env = {**original.__globals__, 'ROOT': ROOT, 'PROSE': PROSE, '__file__': __file__}
    run = FunctionType(original.__code__, env)
    assert not remaining
    run()


if __name__ == '__main__':
    main()
