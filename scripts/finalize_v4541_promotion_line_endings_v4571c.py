"""Keep established CRLF metadata storage while preserving the sealed promotion."""
import os
from pathlib import Path

from scripts.promote_v4541_checkpoint_b import AUDIT, PACKAGE, ROOT, read, save, sha, verify


def main():
    verify()
    root = AUDIT/'storage_successor_v4571c'
    assert not root.exists()
    root.mkdir()
    plan_path = AUDIT/'mutation_plan.json'
    plan = read(plan_path)
    (root/'mutation_plan.before.json').write_bytes(plan_path.read_bytes())
    changes = []
    for row in plan:
        path = Path(row['target'])
        if path.relative_to(ROOT).as_posix() not in {
            'translations/release_stack.json', 'translations/rom_retention_pins.json'}:
            continue
        old = path.read_bytes()
        assert b'\r' not in old and sha(old) == row['planned_sha256']
        new = old.replace(b'\n', b'\r\n')
        assert read(path) == __import__('json').loads(new)
        (root/(path.name+'.LF.before')).write_bytes(old)
        changes.append((row, path, old, new))
    assert len(changes) == 2
    for row, path, old, new in changes:
        assert path.read_bytes() == old and Path(row['planned']).read_bytes() == old
    for row, path, old, new in changes:
        Path(row['planned']).write_bytes(new)
        with path.open('r+b') as stream:
            stream.write(new)
            stream.truncate(len(new))
            stream.flush()
            os.fsync(stream.fileno())
        row['planned_sha256'] = sha(new)
    save(plan_path, plan)
    receipt = {'reason': 'Preserve the existing CRLF convention and avoid unrelated whole-file Git churn.',
               'no_JSON_value_changes': True, 'producer_sha256': sha(Path(__file__).read_bytes()),
               'predecessor_producer_sha256': sha((ROOT/'scripts/promote_v4541_checkpoint_b.py').read_bytes()),
               'changes': [{'file': path.relative_to(ROOT).as_posix(), 'before_sha256': sha(old),
                            'after_sha256': sha(new)} for _, path, old, new in changes]}
    save(root/'receipt.json', receipt)
    save(PACKAGE/'verification/promotion_storage_successor.json', receipt)
    verify()


if __name__ == '__main__':
    main()
