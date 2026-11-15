"""Select and aggregate exact native journals from the explicit scope runner."""

import inspect
import sys

from scripts import assemble_editorial_native_journals_v1 as assembly
from scripts import prepare_editorial_native_resume_v2 as selection
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text


PRODUCER = 'scripts/check_editorial_native_explicit_scope_v1.py'
PREVIOUS_PRODUCER = 'scripts/check_editorial_compiled_pages_explicit_captain_v2.py'


def verify_scope(doc, run):
    assert digest(run['manuscript']) == run['manuscript_sha256']
    run_doc = load(run['manuscript'])
    expected = doc['exact_existing_native_context_reuse']
    assert run_doc['exact_existing_native_context_reuse'] == expected
    blocks = run_doc['blocks']
    assert blocks and set(blocks) <= set(expected['exact_current_blocks'])
    hashes = expected['exact_current_block_sha256']
    subset = {**expected, 'exact_current_blocks': blocks,
              'exact_current_block_sha256': {key: hashes[key] for key in map(str, blocks)}}
    assert run['native_context_reuse'] == subset


def select():
    source = checked_text(selection.source, {
        "assert digest(doc['current_ROM'])==doc['runtime']['candidate_sha256']":
            "assert digest(doc['current_ROM'])==doc['current_ROM_sha256']==doc['exact_existing_native_context_reuse']['target_candidate_sha256']",
        f"            assert run['producer_sha256']==digest('{PREVIOUS_PRODUCER}')":
            "            verify_scope(doc, run)\n"
            f"            assert run['producer_sha256']==digest('{PRODUCER}')",
    })
    env = {**selection.main.__globals__, 'verify_scope': verify_scope, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


def assemble():
    source = checked_text(inspect.getsource(assembly.main), {
        f"        assert run['producer_sha256'] == digest('{PREVIOUS_PRODUCER}')":
            "        verify_scope(doc, run)\n"
            f"        assert run['producer_sha256'] == digest('{PRODUCER}')",
    })
    env = {**assembly.main.__globals__, 'verify_scope': verify_scope, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    commands = {'select': select, 'assemble': assemble}
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        raise SystemExit('Expected select or assemble before the runner arguments.')
    commands[sys.argv.pop(1)]()
