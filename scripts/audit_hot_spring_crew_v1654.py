"""Full input,PNG,RAM,save audit;48 coordinates,20 supplies,10 live-crew bytes."""
import inspect
from pathlib import Path
from scripts import verify_fatigue_shore_pilots_v1597d as original
from scripts import native_hot_spring_crew_v1650 as fixture
from scripts.verify_village_wrap_v608 import read


def audit(terminal_frame):
    source = inspect.getsource(original.audit)
    old = "assert len(proof['owned_bytes'])==40 and all(p['address'] in proof['owned_bytes'] for p in proof['changes'])"
    new = "assert len(proof['owned_bytes'])==(10 if c['battle_fixture']==module.REQUEST else 20 if c['battle_fixture']==module.previous.REQUEST else 48) and all(p['address'] in proof['owned_bytes'] for p in proof['changes'])"
    assert source.count(old) == 1
    source = source.replace(old, new)
    old = "assert proof['all_other4MiB_bytes_including_fatigue_RNG_actors_roles_health_and_event_choices_exact']"
    new = "assert proof['all_other4MiB_including_positions_fatigue_actor_skills_RNG_and_event_outcomes_exact'] if c['battle_fixture']==module.REQUEST else proof['all_other4MiB_bytes_including_positions_health_fatigue_actor_skills_RNG_and_event_choices_exact'] if c['battle_fixture']==module.previous.REQUEST else proof['all_other4MiB_bytes_including_fatigue_RNG_actors_roles_health_and_event_choices_exact']"
    assert source.count(old) == 1
    source = source.replace(old, new)
    for a, b in [('all40_coordinate_byte_changes_and_other4MiB_bytes_audited', 'all48_location20_supply10_crew_owned_bytes_and_all_other4MiB_audited'),
                 ('only_location_fixtures_no_fatigue_actor_RNG_state_event_or_outcome_forcing', 'only_declared_location_supply_crew_fixtures_no_fatigue_actor_skill_RNG_or_outcome_forcing'),
                 ('no_309_recovery_or_editorial_completion_credit', 'no_editorial_completion_credit_from_preservation_audit_alone')]:
        assert source.count(a) == 1
        source = source.replace(a, b)
    env = {**original.__dict__}
    exec(compile(source, __file__, 'exec'), env)
    cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_crew_v1651_1637')
    journal = read(cap / 'navigation_command_journal.json')['commands_received']
    frames = [r['frame'] for r in journal if 'battle_fixture' in r['command']]
    result = env['audit']('hot_spring_crew_v1651', 1637, fixture, terminal_frame, frames)
    result['source_proven_crew10_fixture_frames'] = [r['frame'] for r in journal if r['command'].get('battle_fixture') == fixture.REQUEST]
    result['source_proven_supply20_fixture_frames'] = [r['frame'] for r in journal if r['command'].get('battle_fixture') == fixture.previous.REQUEST]
    assert result['source_proven_crew10_fixture_frames'][0] == 42673
    assert result['source_proven_supply20_fixture_frames'][0] == 20700
    result['artificial_crew_and_provisions_are_not_earned_recruitment_resupply_or_route_progress'] = True
    return result
