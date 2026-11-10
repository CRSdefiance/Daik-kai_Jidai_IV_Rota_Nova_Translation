"""Project exact approved menu receipts and run the unchanged live interval guards."""
import argparse
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['approved', 'fixture', 'terminal', 'body-proof', 'out', 'aliases']:
        parser.add_argument('--'+key, type=Path, required=True)
    args = parser.parse_args()
    parent = load(args.approved)
    assert parent['offline_visual_approved'] and not parent['direct_view_pending']
    if args.aliases.exists():
        projected = load(args.aliases)
        assert projected['complete_native_parent_receipt_sha256'] == digest(args.approved)
    else:
        projected = deepcopy(parent)
        for row in projected['menus']:
            assert digest(row['proof']) == row['proof_sha256']
            proof = load(row['proof'])
            assert proof['runtime'] == parent['runtime']
            assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
            row.update(native_receipt=row['proof'], native_receipt_sha256=row['proof_sha256'])
        projected.update(complete_native_parent_receipt=str(args.approved),
            complete_native_parent_receipt_sha256=digest(args.approved),
            exact_metadata_alias_only_no_provider_pixels_orobject_bytes_replayed=True,
            actual_menu_pixels_still_pending=True, new_credit=0)
        args.aliases.parent.mkdir(parents=True, exist_ok=True)
        save(args.aliases, projected)
    lookup = {(r['block'], r['source_command_offset']):r for r in projected['menus']}
    fixture = load(args.fixture)
    proofs = [lookup[r['block'], r['source_command_offset']]['native_receipt'] for r in fixture['menus']]
    command = [sys.executable, '-m', 'scripts.analyze_maria390_menu_actual_v1',
        '--fixture', str(args.fixture), '--terminal', str(args.terminal), '--body-proof', str(args.body_proof),
        '--menu-proof', str(args.aliases), '--out', str(args.out), '--proofs', *proofs]
    subprocess.run(command, check=True)


if __name__ == '__main__':
    main()
