"""Clear redundant Lisbon replay scratch after verifying the retained evidence."""

from pathlib import Path
import re

from scripts import verify_rafael_sailing_lisbon_gameplay_20261121 as verified


def main():
    base, root, active = verified.base, verified.ROOT, verified.active
    capture = (root / 'capture').resolve()
    report_path = root / 'capture/capture_report.json'
    receipt = root / 'checkpoint_cleanup.json'
    assert not receipt.exists()
    proof, report, release = map(base.load, (verified.PROOF, report_path, active.RELEASE))
    assert base.digest(active.ROM) == release['candidate_sha256'] == proof['candidate_sha256']
    assert base.digest(active.PATCH) == release['patch_sha256'] and base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(report_path) == proof['evidence'][str(report_path)]
    assert proof['natural_activation'] and len(proof['panels']) >= 40
    assert capture.is_relative_to(root.resolve())
    pictures = [r['observed'] for r in proof['panels']]
    pictures.extend(proof[k] for k in ('departure_screen', 'original_departure_notice', 'final_screen'))
    snapshots = [proof[k]['snapshot'] for k in ('before_departure', 'first_lesson_panel', 'departure_return')]
    snapshots.append(report['read_only_RAM_snapshot'])
    keep = {Path(row['path']).resolve(): row['PNG_sha256'] for row in pictures}
    keep.update({Path(row['path']).resolve(): row['sha256'] for row in snapshots + proof['sheets']})
    assert all(p.is_relative_to(root.resolve()) and base.digest(p) == sha for p, sha in keep.items())

    delete = {}
    for rows, filename, key in (
        (report['frames_captured'], r'frame_\d{6}_(cold_boot|navigation|final)\.png', 'PNG_sha256'),
        (report['read_only_pause_RAM_snapshots'], r'frame_\d{6}_arm9_ram\.bin', 'sha256'),
    ):
        for row in rows:
            path = Path(row['path'])
            assert path.resolve().parent == capture and re.fullmatch(filename, path.name)
            if path.resolve() not in keep:
                delete[path] = row[key]
    donor = report['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256']
    copy = Path(donor['destination'])
    assert copy.resolve().parent == capture / 'saves' and copy.suffix == '.dsv'
    if base.digest(copy) == donor['source_sha256']:
        delete[copy] = donor['source_sha256']
    receipts = []
    for path, digest in delete.items():
        assert not path.is_symlink() and not path.is_junction() and base.digest(path) == digest
        receipts.append(dict(path=str(path), sha256=digest, bytes=path.stat().st_size))
    for path in delete:
        path.unlink()
    assert all(base.digest(p) == sha for p, sha in keep.items())
    freed = sum(row['bytes'] for row in receipts)
    base.save(receipt, dict(candidate_sha256=proof['candidate_sha256'], removed=receipts,
        reclaimed_bytes=freed, verified_retained_files=len(keep)))
    print(f'Removed {len(receipts)} redundant replay files and reclaimed {freed:,} bytes.')


if __name__ == '__main__':
    main()
