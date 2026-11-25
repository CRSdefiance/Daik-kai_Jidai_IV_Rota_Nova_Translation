"""Finish the exact planned Lil261 ledger write after the disk-full interruption."""

import inspect

from scripts import checkpoint_lil261_stored_v1 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint, source
from scripts.source_locked_derivation_v5118 import checked_text


if __name__ == '__main__':
    start = source.index('    updates = {document: document_text}')
    end = source.index('    os.replace(staged, ledger_path)', start)
    recovered = checked_text(source, {
        '    assert not mutation.exists() and not document.exists()':
            '    assert mutation.is_dir() and document.is_file()',
        source[start:end]: """    encoded = encode_ledger(ledger)
    planned = load(mutation / 'mutation_plan.json')
    assert planned['new_credit'] == 0 and planned['protected'] == protected
    assert planned['ledger_before_sha256'] == sha(before) and planned['ledger_after_sha256'] == sha(encoded)
    assert gzip.decompress((mutation / 'ledger.before.json.gz').read_bytes()) == before
    for entry in planned['documentation']:
        assert sha(Path(entry['path']).read_bytes()) == entry['after_sha256']
    staged = ledger_path.with_name(ledger_path.stem + '.pending_' + mutation.name + '.json')
    assert staged.is_file() and staged.stat().st_size == 0
    assert ledger_path.read_bytes() == before
    with staged.open('r+b') as handle:
        for offset in range(0, len(encoded), 1024 * 1024):
            handle.write(encoded[offset:offset + 1024 * 1024])
    assert sha(staged.read_bytes()) == planned['ledger_after_sha256']
""",
    })
    recovery_env = {**checkpoint.__globals__, '__file__': __file__}
    exec(compile(recovered, __file__, 'exec'), recovery_env)
    replay = checked_text(inspect.getsource(previous.main), {
        '    assert not ARCHIVE.exists()': '    assert ARCHIVE.is_dir()',
        '    assert not delta_path.exists()': '    assert delta_path.is_file()',
        '        packed.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))': '        assert packed.is_file()',
        "no_batch_worker_live=not (ROOT / 'actual_run0_v1/run_plan.json').exists() or (ROOT / 'actual_run0_v1/terminal.json').exists(),":
            'no_batch_worker_live=False,',
    })

    def compare_existing(path, value):
        assert load(path) == value

    env = {**vars(previous), 'checkpoint': recovery_env['checkpoint'], 'save': compare_existing}
    exec(compile(replay, __file__, 'exec'), env)
    env['main']()
