"""Project completed native journals to readable block sheets during the render."""

import argparse
from pathlib import Path
import subprocess
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--blocks', type=int, nargs='+', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    run_path = args.native / 'native_run_inputs.json'
    run = load(run_path)
    run_hash = digest(run_path)
    manuscript = Path(run['manuscript'])
    plan_path = Path(run['plan'])
    assert digest(manuscript) == run['manuscript_sha256'] and digest(plan_path) == run['plan_sha256']
    source = load(manuscript)
    plans = {row['id']: row for row in load(plan_path)['records']}
    assert not args.out.exists()
    outputs = {}
    for block in args.blocks:
        rows, evidence = [], {}
        for original in source['records']:
            if original['block'] != block or original['id'] not in plans:
                continue
            path = args.native / f"complete_{original['id']}.json"
            proof = load(path)
            assert proof['native_run_inputs_sha256'] == run_hash
            assert proof['four_native_alignment_cases_pass']
            assert proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
            row = proof['record']
            assert row['id'] == original['id'] and row['compiled_hex'] == plans[row['id']]['encoded_hex']
            assert all(row[key] == original[key] for key in ('source_reference', 'current_reference'))
            evidence[str(path)] = digest(path)
            rows.append(row)
        assert rows and block not in outputs
        outputs[block] = dict(records=rows, native_run_inputs_sha256=run_hash, evidence=evidence)
    projections = args.out / 'projections'
    projections.mkdir(parents=True)
    for block, output in outputs.items():
        save(projections / f'B{block}_checked.json', output)
    subprocess.run([sys.executable, '-m', 'scripts.prepare_native_block_contact_sheets_v1',
                    '--native-root', str(projections), '--blocks', *map(str, args.blocks),
                    '--out', str(args.out / 'contacts')], check=True)


if __name__ == '__main__':
    main()
