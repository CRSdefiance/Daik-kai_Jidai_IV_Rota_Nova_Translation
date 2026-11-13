"""Replay the earlier Assign Sailors navigation against the text-only research ROM."""

import inspect
import json
import sys
from pathlib import Path

from scripts import native_battle_cooking_livestock_fixture_v911 as crew
from scripts import native_battle_fixture_v620 as dispatch
from scripts import native_battle_standoff_v911 as approach
from scripts import run_battle_cooking_livestock_adapter_v911 as adapter
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_ship_command_research_v1 import PROOF, ROM, WORK
from scripts.source_locked_derivation_v5118 import checked_text


OLD = Path('work/analysis/battle_cooking_livestock_v911')
RUN = WORK / 'actual_menu_run'
CAP = RUN / 'capture'


def qualify(fn, name, arm_sha):
    source = checked_text(inspect.getsource(fn), {
        "config=read('translations/battle_cooking_livestock_editorial_release_v2.json')":
            "config={'target_arm9_sha256': QUALIFIED_RESEARCH_ARM9}",
    })
    env = {**fn.__globals__, 'ROM': ROM, 'QUALIFIED_RESEARCH_ARM9': arm_sha}
    exec(compile(source, __file__ + '::' + name, 'exec'), env)
    return env[fn.__name__]


def main():
    assert not RUN.exists()
    research = load(PROOF)
    assert digest(ROM) == research['ROM_sha256']
    proof = load(WORK / 'native_menu/native_ship_menu.json')
    assert proof['complete_english_planes_centering_leading_trailing_glyphs_bounds_andguards_pass']
    old_plan = load(OLD / 'GerhardLivestock_run_plan.json')
    old_terminal = load(OLD / 'GerhardLivestock_terminal_source_preservation.json')
    journal = Path(old_plan['append_only_navigation'])
    assert digest(journal) == old_terminal['final_navigation_sha256']
    commands = [json.loads(line) for line in journal.read_text(encoding='utf-8').splitlines()]
    commands = [row for row in commands if row.get('until', 999999) <= 14100]
    assert commands[-2]['until'] == 13900 and commands[-1] == dict(until=14100, buttons=['B'], duration=8)
    commands.extend([dict(until=14300, duration=1), dict(stop=True)])
    donor = Path(old_plan['source_donor'])
    inputs = Path(old_plan['inputs'])
    assert digest(donor) == old_plan['source_donor_sha256'] == old_terminal['source_donor_sha256']
    assert digest(inputs) == old_plan['inputs_sha256']

    RUN.mkdir()
    new_journal = RUN / 'navigation_inputs.jsonl'
    new_journal.write_text(''.join(json.dumps(row)+'\n' for row in commands), encoding='utf-8')
    argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(CAP), '--frames', '14500',
        '--inputs-json', str(inputs), '--touchscreen', '--capture-every', '999999',
        '--capture-at', '13700', '13900', '14100', '14300', '--dump-capture-ram',
        '--battery-save', str(donor), '--pause-at', '4800',
        '--allow-battle-fixtures', '--allow-battle-cooking-livestock-fixtures']
    save(RUN / 'run_plan.json', dict(ROM=str(ROM), ROM_sha256=digest(ROM), argv=argv, source_donor=str(donor),
        source_donor_sha256=digest(donor), replay_journal=str(new_journal), replay_journal_sha256=digest(new_journal),
        original_navigation=str(journal), original_navigation_sha256=digest(journal), terminal_frame=14300,
        intended_battle_coordinate_and_existing_crew_room_only_fixture=True, original_user_save_unchanged_required=True,
        native_combat_no_mode_or_outcome_injection=True, no_state_file_load=True,
        no_destructive_confirmation_input=True, no_earned_progression_claim=True, research_only=True,
        evidence={str(p):digest(p) for p in [PROOF, Path(crew.__file__), Path(approach.__file__),
            Path(adapter.__file__), Path(__file__)]}))
    originals = dispatch.apply_fixture, crew.assign, sys.stdin, sys.argv
    try:
        dispatch.apply_fixture = qualify(approach.apply_fixture, 'coordinate-approach', research['target_ARM9_sha256'])
        crew.assign = qualify(crew.assign, 'crew-room', research['target_ARM9_sha256'])
        sys.argv = argv
        with new_journal.open(encoding='utf-8') as stream:
            sys.stdin = stream
            adapter.main()
    finally:
        dispatch.apply_fixture, crew.assign, sys.stdin, sys.argv = originals
    assert digest(donor) == old_plan['source_donor_sha256']
    report = CAP / 'capture_report.json'
    capture = load(report)
    assert capture['cold_boot'] and not capture['savestate_loaded']
    save(RUN / 'terminal.json', dict(capture_report=str(report), capture_report_sha256=digest(report),
        run_plan=str(RUN/'run_plan.json'), run_plan_sha256=digest(RUN/'run_plan.json'),
        terminal_exit_code=0, original_donor_hash_preserved=True, visual_and_transition_approval_pending=True,
        new_credit=0))
    print('Assign Sailors focused replay terminated. Review exact menu frames and returns.')


if __name__ == '__main__':
    main()
