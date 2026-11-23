"""Remove unneeded replay captures after the Square evidence is verified."""

from argparse import ArgumentParser
from pathlib import Path
import re

from scripts import verify_seville_square_gameplay_20261121 as verify


FRAME = re.compile(r'frame_\d{6}_(cold_boot|navigation|final)\.png')
SNAPSHOT = re.compile(r'frame_\d{6}_arm9_ram\.bin')


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--town', choices=verify.EXCHANGES, default='seville')
    city = parser.parse_args().town
    runs, base = verify.runs, verify.base
    folder = runs.VOYAGES[city][0]
    capture = (folder / 'capture').resolve()
    proof_file = folder / f'verified_{city}_square.json'
    report_file = folder / 'capture/capture_report.json'
    receipt = folder / 'checkpoint_cleanup.json'
    assert not receipt.exists()
    proof, report, release = map(base.load, (proof_file, report_file, runs.active.RELEASE))
    assert proof['original_ordinary_Square_activation'] and len(proof['panels']) == verify.EXCHANGES[city].count
    assert base.digest(runs.active.ROM) == release['candidate_sha256'] == proof['candidate_sha256']
    assert base.digest(runs.active.PATCH) == release['patch_sha256'] and release['clean_input_patch_byte_exact']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(report_file) == proof['evidence'][str(report_file)]
    assert capture.is_relative_to(folder.resolve()) and not capture.is_symlink()
    photos = [p['observed'] for p in proof['panels']] + list(proof['observations'].values())
    states = list(proof['retained_read_only_snapshots'].values()) + [proof['completion']['read_only_snapshot']]
    sheets = list(proof['screenshots'])
    if city == 'hamburg':
        battle = base.load(folder / 'verified_speyer_tutorial.json')
        trade = base.load(folder / 'hodram_baltic_trade_contextual_review.json')
        assert battle['candidate_sha256'] == trade['candidate_sha256'] == proof['candidate_sha256']
        assert battle['ordinary_voyage_trigger'] and len(battle['panels']) == 32
        assert trade['ordinary_port_trigger'] and len(trade['records']) == 9
        assert all(item['evidence'][str(report_file)] == base.digest(report_file) for item in (battle, trade))
        photos.extend(p['observed'] for p in battle['panels'])
        photos.extend(battle['observations'].values())
        photos.extend(r['observed_current_english']['observed'] for r in trade['records'])
        photos.append(trade['after_dialogue'])
        sheets.extend(battle['screenshots'])
        sheets.extend(trade['screenshots'])
    keep = {Path(row['path']).resolve(): row['PNG_sha256'] for row in photos}
    keep.update((Path(row['path']).resolve(), row['sha256']) for row in states + sheets)
    for path, checksum in keep.items():
        assert path.is_relative_to(folder.resolve()) and base.digest(path) == checksum
    redundant = {}
    for rows, pattern, key in (
        (report['frames_captured'], FRAME, 'PNG_sha256'),
        (report['read_only_pause_RAM_snapshots'], SNAPSHOT, 'sha256'),
    ):
        for row in rows:
            path = Path(row['path'])
            assert path.resolve().parent == capture and pattern.fullmatch(path.name)
            if path.resolve() not in keep:
                redundant[path] = row[key]
    donor = report['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256']
    clone = Path(donor['destination'])
    assert clone.resolve().parent == capture / 'saves' and clone.suffix.lower() == '.dsv'
    if base.digest(clone) == donor['source_sha256']:
        redundant[clone] = donor['source_sha256']
    files = []
    for path, checksum in redundant.items():
        assert path.is_file() and not path.is_symlink() and not path.is_junction()
        assert path.suffix.lower() in {'.png', '.bin', '.dsv'} and base.digest(path) == checksum
        files.append(dict(path=str(path), sha256=checksum, bytes=path.stat().st_size))
    for path in redundant:
        path.unlink()
    assert all(base.digest(path) == checksum for path, checksum in keep.items())
    assert base.digest(donor['source']) == donor['source_sha256']
    reclaimed = sum(row['bytes'] for row in files)
    base.save(receipt, dict(candidate_sha256=release['candidate_sha256'],
        verified_retained_files=len(keep), reclaimed_bytes=reclaimed, removed=files))
    print(f'Removed {len(files)} redundant captures and reclaimed {reclaimed:,} bytes.')


if __name__ == '__main__':
    main()
