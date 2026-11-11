"""Reach the ship assignment modal through ordinary crew attrition on the isolated fleet save."""

import json
import sys
from pathlib import Path

from scripts import headless_desmume_v193 as harness
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_ship_command_research_v1 import PROOF, ROM, WORK
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands


RUN = WORK / 'actual_attrition_run_v3'


def main():
    assert not RUN.exists()
    research = load(PROOF)
    assert digest(ROM) == research['ROM_sha256']
    old_plan = Path('work/analysis/battle_cooking_livestock_v911/GerhardLivestock_run_plan.json')
    prior = load(old_plan)
    donor, inputs = Path(prior['source_donor']), Path(prior['inputs'])
    assert digest(donor) == prior['source_donor_sha256']
    assert digest(inputs) == prior['inputs_sha256']
    RUN.mkdir()
    journal = RUN / 'navigation_inputs.jsonl'
    journal.write_text(json.dumps(dict(until=7000, buttons=['A'], duration=8))+'\n', encoding='utf-8')
    argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(RUN/'capture'), '--frames', '24000',
        '--inputs-json', str(inputs), '--battery-save', str(donor), '--touchscreen',
        '--capture-every', '999999', '--pause-at', '4800', '--dump-ram']
    plan_path = RUN / 'run_plan.json'
    save(plan_path, dict(ROM=str(ROM), ROM_sha256=digest(ROM), argv=argv, donor=str(donor), donor_sha256=digest(donor),
        initial_input_schedule=str(inputs), initial_input_schedule_sha256=digest(inputs),
        journal=str(journal), initial_journal_sha256=digest(journal), source_plan=str(old_plan),
        no_approach_coordinates_room_assignments_or_gameplay_state_override=True,
        inherited_isolated_fleet_save_no_earned_progression_claim=True, no_savestate=True,
        no_destructive_confirmation_intended=True, research_only=True, new_credit=0))
    saved = sys.argv, sys.stdin
    stream = GrowingCommands(journal)
    try:
        sys.argv, sys.stdin = argv, stream
        harness.main()
    finally:
        sys.argv, sys.stdin = saved
        stream.close()
    assert digest(donor) == prior['source_donor_sha256']
    report = RUN/'capture/capture_report.json'
    data = load(report)
    assert data['cold_boot'] and not data['savestate_loaded']
    assert data['ROM_sha256'] == research['ROM_sha256']
    assert not any(v for k,v in data.items() if k.startswith('synthetic_'))
    save(RUN/'terminal.json', dict(report=str(report), report_sha256=digest(report),
        run_plan=str(plan_path), run_plan_sha256=digest(plan_path), final_journal_sha256=digest(journal),
        original_donor_hash_preserved=True, terminal_exit_code=0, direct_visual_approval_pending=True, new_credit=0))


if __name__ == '__main__':
    main()
