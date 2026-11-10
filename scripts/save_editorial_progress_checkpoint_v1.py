"""Save uncredited editorial progress with exact backups and protected release identities."""
import gzip
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger


def checkpoint(*, mutation, batch_key, batch_updates, summary, document, document_text, completed, protected):
    mutation, document = Path(mutation), Path(document)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    assert not mutation.exists() and not document.exists()
    for path, digest in protected.items():
        assert sha(Path(path).read_bytes()) == digest, path
    before = ledger_path.read_bytes()
    prior = load(ledger_path)
    assert prior['records_editorially_completed'] == completed and not prior['full_goal_complete']
    assert batch_key in prior and batch_updates['new_credit'] == 0
    ledger = dict(prior)
    ledger[batch_key] = {**prior[batch_key], **batch_updates}
    ledger['latest_checkpoint'] = summary
    assert all(ledger[k] == v for k, v in prior.items() if k not in [batch_key, 'latest_checkpoint'])
    updates = {document: document_text}
    for name in ['editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md', 'known_issues.md', 'todo.md']:
        path = Path('docs') / name
        updates[path] = ('# Current editorial checkpoint - 2026-11-04\n\n' + summary + '\n\nContinue from [' +
            document.stem + '](' + document.name + '). Reuse the completed checks; earlier entries below are historical.\n\n' +
            path.read_text(encoding='utf-8'))
    encoded = encode_ledger(ledger)
    mutation.mkdir(parents=True)
    backup = mutation / 'ledger.before.json.gz'
    backup.write_bytes(gzip.compress(before, compresslevel=1, mtime=0))
    assert gzip.decompress(backup.read_bytes()) == before
    plan = []
    for index, (path, content) in enumerate(updates.items()):
        old = path.read_bytes() if path.exists() else None
        if old is not None:
            (mutation / f'{index}.before').write_bytes(old)
        plan.append(dict(path=str(path), before_sha256=sha(old) if old is not None else None,
            after_sha256=sha(content.encode('utf-8'))))
    save(mutation / 'mutation_plan.json', dict(documentation=plan, ledger_before_sha256=sha(before),
        ledger_after_sha256=sha(encoded), all_other_keys_preserved=True, protected=protected, new_credit=0))
    assert ledger_path.read_bytes() == before
    for entry, (path, content) in zip(plan, updates.items(), strict=True):
        assert (sha(path.read_bytes()) if path.exists() else None) == entry['before_sha256']
        path.write_text(content, encoding='utf-8', newline='\n')
        assert sha(path.read_bytes()) == entry['after_sha256']
    # work/ can be a junction to another volume. Stage beside the destination
    # so the final replacement remains atomic on Windows.
    staged = ledger_path.with_name(ledger_path.stem + '.pending_' + mutation.name + '.json')
    assert not staged.exists()
    staged.write_bytes(encoded)
    os.replace(staged, ledger_path)
    assert sha(ledger_path.read_bytes()) == sha(encoded)
    for path, digest in protected.items():
        assert sha(Path(path).read_bytes()) == digest, path
    save(mutation / 'verified_mutations.json', dict(ledger_sha256=sha(encoded), completed=completed,
        all_other_keys_preserved=True, protected_release_identities_unchanged=True, new_credit=0, full_goal_complete=False))
