"""Current-ROM bindings for retained bounded battle/church test prerequisites."""

import argparse
import io
import json
from pathlib import Path
import sys
from types import FunctionType, SimpleNamespace

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts.run_patch_interaction_audit_20261027 import ROOT, ROM, DIGEST, read, save


def battle_adapter(arm):
    from scripts import native_ship_sinking_fixture_v1351 as initial
    from scripts import native_ship_sinking_fixture_v1352 as loaded_position

    def bound_read(path):
        value = read(path)
        if str(path).replace('\\', '/') == 'work/analysis/ship_sinking_release_v1343/registered_release_verification.json':
            # This is an explicitly new test binding, not a historical release
            # claim. The original fixture still verifies every original native
            # consumer against the clean ROM and bounds its forty model bytes.
            value = dict(value, ARM9_sha256=sha(arm), candidate_sha256=DIGEST,
                audit_ROM_binding_20261027=True)
        return value

    water = FunctionType(initial.water.__code__, {**initial.__dict__, 'ROM': ROM})
    env = {**initial.__dict__, 'ROM': ROM, 'water': water, 'read': bound_read}
    prior = SimpleNamespace(**env)
    prior.apply_fixture = FunctionType(initial.apply_fixture.__code__, env)
    function = FunctionType(loaded_position.apply_fixture.__code__, {**loaded_position.__dict__, 'previous': prior})

    def apply(actual_arm, raw, request):
        assert actual_arm == arm and sha(ROM.read_bytes()) == DIGEST
        after, receipt = function(actual_arm, raw, request)
        assert len(receipt['owned_bytes']) == 40
        receipt.update(audit_target_ROM_sha256=DIGEST,
            retained_native_fixture_sources=[str(Path(initial.__file__)),str(Path(loaded_position.__file__))],
            original_clean_consumer_and_terrain_and40_byte_bounds_checks_retained=True,
            prepared_fleet_and_position_prerequisite_not_earned=True)
        return after, receipt
    return apply


def church_adapter(arm):
    from scripts import native_ceremony_family_fixture_v815 as original

    def bound_read(path):
        value = read(path)
        if str(path).replace('\\','/') == 'translations/ceremony_editorial_release_v1.json':
            value = dict(value, source_arm9_sha256=sha(arm), target_arm9_sha256=sha(arm))
        return value

    function = FunctionType(original.set_condition.__code__, {**original.__dict__, 'read': bound_read})

    def apply(actual_arm, raw, request):
        assert actual_arm == arm and sha(ROM.read_bytes()) == DIGEST
        after, receipt = function(actual_arm, raw, request)
        assert receipt['only_calendar_word_and_facility_mask_owned']
        receipt.update(audit_target_ROM_sha256=DIGEST,
            original_clean_native_consumer_and8_byte_bounds_checks_retained=True,
            prepared_calendar_and_facility_prerequisite_not_earned=True)
        return after, receipt
    return apply


def battle_menu_adapter(arm):
    from scripts import native_battle_fixture_v620 as original
    function = FunctionType(original.apply_fixture.__code__,
        {**original.__dict__, 'ARM':sha(arm), 'REFERENCE':ROM})
    def apply(actual_arm, raw, request):
        assert actual_arm == arm and sha(ROM.read_bytes()) == DIGEST
        after, receipt = function(actual_arm, raw, request)
        assert len(receipt['owned_bytes']) <= 12
        receipt.update(audit_target_ROM_sha256=DIGEST,
            original_clean_consumers_identity_terrain_and_bounds_checks_retained=True,
            prepared_recovery_or_position_prerequisite_not_earned=True)
        return after, receipt
    return apply


def aftermath_adapter(arm):
    from scripts import native_duel_contact_v1169 as contact
    from scripts import native_duel_long_fixture_v1239 as low
    from scripts import native_duel_long_fixture_v1242 as long
    from dk4tool.patch import duel_editorial as parser
    from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET

    common = NdsImage.open(ROM).read_file('/COMMON/MESFILE.DK4')
    directory = sha(arm[DIRECTORY_OFFSET:TABLE_OFFSET])
    # Keep the original current-message/component/cache/code/bounds parser; bind
    # only its exact target hashes to this explicitly separate audit fixture.
    parser.owned_entries(common, arm, directory)
    def bound_read(path):
        value = read(path)
        if str(path).replace('\\','/') in ('translations/duel_editorial_release_v1.json',
                'translations/sighting_grammar_editorial_release_v1.json'):
            value = dict(value, target_arm9_sha256=sha(arm), target_common_sha256=sha(common),
                directory_sha256=directory, audit_ROM_binding_20261027=True)
        return value
    parser.current_entries = FunctionType(parser.current_entries.__code__,{**parser.__dict__,'read':bound_read})
    previous = contact.previous
    water = FunctionType(previous.water.__code__,{**previous.__dict__,'ROM':ROM})
    bound_previous = SimpleNamespace(**{**previous.__dict__,'ROM':ROM,'water':water,'read':bound_read})
    parent = FunctionType(contact.apply_fixture.__code__,{**contact.__dict__,
        'ROM':ROM,'read':bound_read,'previous':bound_previous,'water':water})
    low_bound = FunctionType(low.apply_fixture.__code__,{**low.__dict__,'ROM':ROM,'prior':parent})
    function = FunctionType(long.apply_fixture.__code__,{**long.__dict__,'ROM':ROM,'prior':low_bound})
    def apply(actual_arm,raw,request):
        assert actual_arm == arm and sha(ROM.read_bytes()) == DIGEST
        after,receipt = function(actual_arm,raw,request)
        assert len(receipt['owned_bytes']) <= 100
        assert all(0x02180000 <= address < 0x02387A20 for address in receipt['owned_bytes'])
        receipt.update(audit_target_ROM_sha256=DIGEST,
            original_clean_native_consumers_bounded_fields_and_no_during_duel_mutation_guards_retained=True,
            original_current_message_component_cache_code_and_directory_bounds_guards_retained=True,
            original_actor_ID_RNG_eligibility_and_result_exclusions_retained=True,
            source_modules=[str(Path(module.__file__)) for module in (contact,previous,low,long)],
            prepared_diplomacy_position_positive_health_attributes_equipment_not_earned=True)
        return after,receipt
    return apply


def main(case, interactive=False):
    assert sha(ROM.read_bytes()) == DIGEST
    folder = {'battle':'battle_victory_v1409_1404', 'battle_menu':'battle_paints_v673_baseline',
              'battle_aftermath':'aftermath_victory_v1270_1266',
              'church':'ceremony_v803_church_prayer_control'}[case]
    source = Path('work/emulation_v193') / folder
    old = read(source / 'capture_report.json')
    journal = read(source / 'navigation_command_journal.json')
    rows = journal['commands_received']
    assert all(row['validation_passed'] for row in rows)
    first = rows[0]['frame']
    suffix = '_timing_followup' if interactive and case=='battle_menu' else ('_followup' if interactive else '_controlled')
    case_root = ROOT / 'cases' / (case + suffix)
    case_root.mkdir(exist_ok=True)
    output = case_root / 'capture'
    assert not output.exists()
    battery = old['battery_save_preloaded']
    assert sha(Path(battery['source']).read_bytes()) == battery['source_sha256']
    inputs = [event for event in old['scripted_input_schedule'] if event['start'] <= first]
    input_path = case_root / 'inputs.json'
    save(input_path, inputs)
    commands = [row['command'] for row in rows if not interactive or row['frame'] < (first if case=='battle_menu' else 8300)]
    candidates = sorted({row['frame'] for row in old['frames_captured'] if row['frame'] >= 2000})
    captures = sorted({first, old['frames'], *[candidates[(len(candidates)-1)*i//18] for i in range(19)]})
    native = sorted({first, old['frames'], *[captures[(len(captures)-1)*i//5] for i in range(6)]})
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    if case.startswith('battle'):
        from scripts import native_battle_fixture_v620 as dispatch
        dispatch.apply_fixture = {'battle':battle_adapter,'battle_menu':battle_menu_adapter,
                                  'battle_aftermath':aftermath_adapter}[case](arm)
        allow = ['--allow-battle-fixtures']
    else:
        from scripts import native_condition_fixture_v520 as dispatch
        dispatch.set_condition = church_adapter(arm)
        allow = ['--allow-condition-fixtures']
    save(case_root / 'plan.json', dict(case=case+'_controlled', target_ROM_sha256=DIGEST,
        scope='Battle approach, engagement and ordinary follow-up controls; outcomes require screenshot review' if case.startswith('battle') else 'Church prayer and return',
        source_report=str(source/'capture_report.json'), source_report_sha256=sha((source/'capture_report.json').read_bytes()),
        source_journal=str(source/'navigation_command_journal.json'), source_journal_sha256=sha((source/'navigation_command_journal.json').read_bytes()),
        inherited_battery=battery, controlled_prerequisite=True, no_earned_progress_claim=True,
        ROM_and_game_code_and_savestate_unchanged=True, adapter_sha256=sha(Path(__file__).read_bytes())))
    save(case_root / 'commands.json', commands)
    previous = sys.stdin
    prefix = io.StringIO(''.join(json.dumps(command)+'\n' for command in commands))
    class PrefixedInput:
        def readline(self):
            return prefix.readline() or previous.readline()
    sys.stdin = PrefixedInput() if interactive else prefix
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(output),
        '--frames', str(60000 if interactive else old['frames']+1), '--inputs-json', str(input_path), '--battery-save', battery['source'],
        '--pause-at', str(first), '--touchscreen', '--capture-every', '999999',
        '--capture-at', *map(str,captures), '--capture-native-state-at', *map(str,native), '--dump-capture-ram', *allow]
    if interactive:
        sys.argv.extend(['--dump-pause-ram'])
    try:
        harness.main()
    finally:
        sys.stdin = previous
    report = read(output/'capture_report.json')
    assert (interactive or report['frames'] == old['frames']) and report['ROM_sha256'] == DIGEST
    assert not report['callback_errors'] and not report['savestate_loaded']
    assert sha(Path(battery['source']).read_bytes()) == battery['source_sha256']
    save(case_root/'terminal.json',dict(status='executed_pending_visual_and_memory_review',frames=report['frames'],
        target_ROM_sha256=DIGEST, donor_preserved=True, controlled_fixture=True, actual_outcome_requires_visual_review=True))
    print(case,'controlled replay completed',flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',choices=['battle','battle_menu','battle_aftermath','church'],required=True)
    parser.add_argument('--interactive',action='store_true')
    args=parser.parse_args()
    assert not args.interactive or args.case in ('battle','battle_menu')
    main(args.case,args.interactive)
