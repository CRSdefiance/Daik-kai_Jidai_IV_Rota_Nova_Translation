"""Full original input/RAM/save audit with exact48-byte locations/20-byte supplies."""
import inspect
from pathlib import Path
from scripts import verify_fatigue_shore_pilots_v1597d as previous
from scripts import native_hot_spring_provisions_v1642 as fixture
from scripts.verify_village_wrap_v608 import read

def audit(terminal_frame):
    source=inspect.getsource(previous.audit)
    for old,new in [("assert len(proof['owned_bytes'])==40 and all(p['address'] in proof['owned_bytes'] for p in proof['changes'])",
        "assert len(proof['owned_bytes'])==(20 if c['battle_fixture']==module.REQUEST else 48) and all(p['address'] in proof['owned_bytes'] for p in proof['changes'])"),
        ("assert proof['all_other4MiB_bytes_including_fatigue_RNG_actors_roles_health_and_event_choices_exact']",
         "assert proof.get('all_other4MiB_bytes_including_fatigue_RNG_actors_roles_health_and_event_choices_exact',proof.get('all_other4MiB_bytes_including_positions_health_fatigue_actor_skills_RNG_and_event_choices_exact',False))"),
        ('all40_coordinate_byte_changes_and_other4MiB_bytes_audited','all48_location_and20_provision_owned_bytes_and_other4MiB_audited'),
        ('no_309_recovery_or_editorial_completion_credit','no_editorial_completion_credit_from_preservation_audit_alone'),
        ('only_location_fixtures_no_fatigue_actor_RNG_state_event_or_outcome_forcing','only_declared_location_and_supply_fixtures_no_fatigue_actor_skill_RNG_or_outcome_forcing')]:
        assert source.count(old)==1,old;source=source.replace(old,new)
    env={**previous.__dict__};exec(compile(source,__file__,'exec'),env)
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_supplied_v1643_1637')
    journal=read(cap/'navigation_command_journal.json')['commands_received'];frames=[r['frame'] for r in journal if 'battle_fixture' in r['command']]
    supply=[r['frame'] for r in journal if r['command'].get('battle_fixture')==fixture.REQUEST];assert supply==[20700]
    result=env['audit']('hot_spring_notice_supplied_v1643',1637,fixture,terminal_frame,frames)
    result['source_proven_supply20_fixture_frames']=supply
    result['all_other_declared_fixtures_are_source_proven48_byte_locations']=True
    return result
