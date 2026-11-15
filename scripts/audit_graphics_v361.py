"""Refresh full preservation and reconcile current evidence without dropping backlog."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import audit_current_graphics_v313 as preservation

ROOT = Path('work/analysis/current_graphics_v361')
ROM = Path('out/all_routes_combined_v360_candidate.nds')


def main():
    preservation.ROOT = ROOT
    preservation.ROM = ROM
    preservation.main()
    proof_path = ROOT / 'preservation_proof.json'
    proof = json.loads(proof_path.read_text())
    release = json.loads(Path('work/analysis/commodity_release_v360/release_proof.json').read_text())
    assert proof['candidate_sha256'] == release['candidate_sha256'] == sha(ROM.read_bytes())
    ledger_path = Path('translations/graphics_completion_requirements_v313.json')
    ledger = json.loads(ledger_path.read_text(encoding='utf-8'))
    assert len(ledger['historical_pending_items_retained']) == 22
    ledger['candidate'] = str(ROM)
    ledger['candidate_sha256'] = proof['candidate_sha256']
    ledger['source_preservation_proof'] = str(proof_path)
    ledger['preservation_proof_sha256'] = sha(proof_path.read_bytes())
    ledger['all921_preservation_invariants_current'] = True
    row = next(r for r in ledger['historical_pending_items_retained'] if r['historical_item'] == 7)
    row['current_evidence_and_remaining_work'] = (
        'V360 preserves all470 inherited batches and native stages, integrates complete commodity names '
        'and scoped Town/market/Cargo/Price layouts, passes actual production checks and exact clean patch. '
        'Full-goal contexts and user cold-boot acceptance/canonical promotion remain pending.')
    row['additional_V360_release_evidence'] = 'work/analysis/commodity_release_v360/release_proof.json'
    ledger['current_inventory_v361'] = {'preservation': str(proof_path),
                                       'all921_checked_against_clean': True,
                                       'no_translation_or_gameplay_completion_inferred': True}
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for name in ['graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json']:
        p = Path('translations') / name
        d = json.loads(p.read_text(encoding='utf-8'))
        plaques = d['plaque_style_v247']['ongoing_plaque_inventory']
        assert len(plaques) == 18 and all(not r['fully_completed'] for r in plaques)
        d['current_inventory_v361'] = {'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
                                      'candidate_sha256': proof['candidate_sha256'],
                                      'all921_entries_preserved': True, 'changed_graphics_entries': proof['changed_entries'],
                                      'all22_historical_requirements_retained': True,
                                      'all18_plaques_incomplete': True, 'full_goal_complete': False}
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Current921-entry preservation refreshed; V360 inheritance recorded and all22 backlog items retained.')


if __name__ == '__main__':
    main()
