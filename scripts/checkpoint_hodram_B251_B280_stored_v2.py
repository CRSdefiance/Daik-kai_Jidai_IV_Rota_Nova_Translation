"""Finish the exact disk-interrupted checkpoint, preserving all partial evidence."""
import gzip
import os
from pathlib import Path
from types import FunctionType
from scripts import checkpoint_hodram_B251_B280_stored_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def resume_checkpoint(**args):
    mutation = Path(args['mutation'])
    ledger_path = Path('translations/editorial_review_current_v1.json')
    plan = load(mutation / 'mutation_plan.json')
    before = gzip.decompress((mutation / 'ledger.before.json.gz').read_bytes())
    assert ledger_path.read_bytes() == before
    assert digest(ledger_path) == plan['ledger_before_sha256']
    prior = load(ledger_path)
    assert prior['records_editorially_completed'] == args['completed'] == 17533
    assert not prior['full_goal_complete']
    ledger = dict(prior)
    key = args['batch_key']
    assert args['batch_updates']['new_credit'] == 0
    ledger[key] = {**prior[key], **args['batch_updates']}
    for name, value in args['additional_updates'].items():
        assert prior[name].get('new_credit', 0) == value['new_credit'] == 0
        ledger[name] = {**prior[name], **value}
    ledger['latest_checkpoint'] = args['summary']
    assert all(ledger[k] == value for k, value in prior.items()
               if k not in [key, 'latest_checkpoint', *args['additional_updates']])
    encoded = encode_ledger(ledger)
    import hashlib
    assert hashlib.sha256(encoded).hexdigest() == plan['ledger_after_sha256']
    assert plan['protected'] == args['protected']
    for path, expected in args['protected'].items():
        assert digest(path) == expected
    for entry in plan['documentation']:
        assert digest(entry['path']) == entry['after_sha256']
    assert Path(args['document']).read_text(encoding='utf-8') == args['document_text']
    pending = ledger_path.with_name(ledger_path.stem + '.pending_' + mutation.name + '.json')
    preserved = mutation / 'disk_full_zero_length_pending_preserved.json'
    assert pending.exists() and pending.stat().st_size == 0 and not preserved.exists()
    os.replace(pending, preserved)
    pending.write_bytes(encoded)
    assert digest(pending) == plan['ledger_after_sha256'] and ledger_path.read_bytes() == before
    os.replace(pending, ledger_path)
    assert digest(ledger_path) == plan['ledger_after_sha256']
    for path, expected in args['protected'].items():
        assert digest(path) == expected
    save(mutation / 'verified_mutations.json', dict(ledger_sha256=digest(ledger_path), completed=17533,
        all_other_keys_preserved=True, protected_release_identities_unchanged=True, new_credit=0,
        full_goal_complete=False, exact_interrupted_checkpoint_resumed=True,
        zero_length_pending_preserved=str(preserved), resume_producer=__file__, resume_sha256=digest(__file__)))


if __name__ == '__main__':
    FunctionType(previous.main.__code__, {**previous.main.__globals__, 'checkpoint': resume_checkpoint})()
