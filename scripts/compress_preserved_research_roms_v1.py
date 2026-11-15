"""Losslessly compress preserved workspace research ROMs without moving or deleting them."""
import hashlib
import argparse
import os
import shutil
import subprocess
from pathlib import Path
from scripts.audit_story_glyph_consistency import save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path, default=Path('work/Hodram_B251_B280_clean_20261107/lossless_space_recovery_v1.json'))
    parser.add_argument('--target-free', type=int, default=700_000_000)
    parser.add_argument('--count', type=int, default=32)
    args = parser.parse_args()
    workspace = Path.cwd().resolve()
    receipt = args.receipt
    assert not receipt.exists()
    assert receipt.resolve().is_relative_to(workspace) and 0 < args.count <= 128
    candidates = []
    for directory, dirs, files in os.walk('work', followlinks=False):
        dirs[:] = [name for name in dirs if not (Path(directory) / name).is_junction()]
        for name in files:
            if not name.endswith('_RESEARCH_ONLY.nds'):
                continue
            path = Path(directory) / name
            stat = path.stat()
            if not stat.st_file_attributes & 2048:
                assert path.resolve().is_relative_to(workspace)
                candidates.append(path)
    rows = []
    before_free = shutil.disk_usage(workspace).free
    for path in sorted(candidates)[:args.count]:
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        result = subprocess.run(['compact.exe', '/C', '/I', '/A', '/Q', str(path.resolve())],
                                capture_output=True, text=True)
        after = hashlib.sha256(path.read_bytes()).hexdigest()
        compressed = bool(path.stat().st_file_attributes & 2048)
        row = dict(path=str(path), before_sha256=before, after_sha256=after,
                   bytes=path.stat().st_size, compressed=compressed, native_exit=result.returncode,
                   native_output=result.stdout, native_error=result.stderr)
        rows.append(row)
        save(receipt, dict(before_free=before_free, after_free=shutil.disk_usage(workspace).free,
            files=rows, all_logical_bytes_paths_preserved=all(r['before_sha256']==r['after_sha256'] for r in rows),
            no_file_deleted_or_moved=True))
        assert result.returncode == 0 and compressed and before == after, row
        if shutil.disk_usage(workspace).free > args.target_free:
            break
    print(dict(files=len(rows), before_free=before_free, after_free=shutil.disk_usage(workspace).free,
               receipt=str(receipt), all_bytes_preserved=True))


if __name__ == '__main__':
    main()
