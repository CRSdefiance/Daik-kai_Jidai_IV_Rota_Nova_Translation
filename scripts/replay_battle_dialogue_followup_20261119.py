"""Verify the original Madeira confirmation with an existing crew member."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import observe_attack_display_ownership_20261118 as earlier
from scripts import replay_sea_hazard_dialogue_20261119 as startup_entry
from scripts import stage_battle_dialogue_followup_20261119 as build
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "madeira_observation_current"
STARTUP = build.ROOT / "startup_fixture"


def schedule(case):
    events, frames, end, origin, donor = earlier.schedule(case)
    assert events[-2]["start"] == 6621 and events[-1]["start"] == 6741
    events = events[:-2] + [events[-2] | {"buttons": ["B"]}]
    return events, frames, end, origin, donor


def assign_first_mate(arm, raw):
    cpu, get = earlier.get_machine(arm, raw)
    roster, fleets, companies = [get(f) for f in (0xCB184, 0xCB1A8, 0xCB160)]
    active = get(0x397D8, companies)
    assert active == 2 and get(0x7F244) == get(0x2E58C) == 1
    duty, actor_id, first_mate_slot = fleets + 0x2090, 23, 15
    actor = roster + 4 + 32*actor_id
    assert get(0x7E958, actor) == active and get(0x7EE08, actor) == actor_id and get(0x7E988, actor) == 7
    assert get(0x132C0, get(0x82E04, duty), first_mate_slot) == 6
    assert get(0x82BC4, duty, first_mate_slot) == 208
    assert actor_id not in [get(0x82BC4, duty, index) for index in range(31)]
    assert get(0x82478, duty, 1) == 18
    get(0x82BB8, duty, first_mate_slot, actor_id)
    assert get(0x82478, duty, 1) == actor_id and get(0x82428, duty, 1) == actor
    result = bytes(cpu.mem_read(earlier.location.BASE, len(raw)))
    address = duty + 6 + first_mate_slot
    difference = address-earlier.location.BASE
    assert result == raw[:difference] + bytes((actor_id,)) + raw[difference+1:]
    row = dict(existing_actor=actor_id, original_actor_company=active, voice_class=7, first_mate_slot=first_mate_slot,
        native_setter=0x02082BB8, assignment_address=address, before=208, after=actor_id,
        only_one_assignment_byte_changed=True)
    return result, row


def neutral_town(get, companies, towns, defender_location, defender_company):
    assert 0 <= defender_location <= 115 and defender_company == 6
    assert get(0xB4AA8, towns+4+30*108, defender_company) > 0
    assert get(0x3CB30, companies+4+2*76, defender_company) == 0
    return True


def gameplay():
    proof = base.load(build.PROOF)
    staged = SimpleNamespace(ROM=build.ROM, RELEASE=build.PROOF)
    source = checked_text(getsource(earlier.run), {
        'assert base.digest(base.REGISTRY) == release["registry_sha256"]':
            'assert base.load(build.parent.RELEASE)["registry_sha256"] == base.digest(base.REGISTRY)',
        "    rebound_water = FunctionType": """    location_source = checked_text(location_source, {
        "assert get(0x34674, defender) == 30 and get(0x35320, defender) == 6":
            "assert neutral_town(get, companies, towns, get(0x34674, defender), get(0x35320, defender))",
    })
    rebound_water = FunctionType""",
        '''"release": release, "water": rebound_water''':
            '''"release": release, "water": rebound_water, "neutral_town": neutral_town''',
        '''        return result, receipt

    source =''': '''        result, assignment = assign_first_mate(actual, result)
        receipt["owned_bytes"].append(assignment["assignment_address"])
        receipt["changes"].append(dict(address=assignment["assignment_address"], before=assignment["before"], after=assignment["after"]))
        receipt.update(context="Madeira_neutral_and_existing_First_Mate",
                       first_mate_fixture=assignment, after_RAM_sha256=native.digest(result),
                       only_own_cached_and_live_position_changed=False)
        return result, receipt

    source =''',
        '''        assert fixture["only_own_cached_and_live_position_changed"]''':
            '''        assert fixture["first_mate_fixture"]["only_one_assignment_byte_changed"]''',
    })
    assert proof["parent_sha256"] == base.digest(build.parent.ROM)
    env = vars(earlier) | dict(__file__=__file__, parent=staged, build=build, ROOT=ROOT, schedule=schedule,
        FOCUS={300, 304, 2129}, assign_first_mate=assign_first_mate, neutral_town=neutral_town)
    exec(compile(source, __file__+"::madeira-first-mate", "exec"), env)
    env["run"]("first_mate")


def startup():
    run = FunctionType(startup_entry.startup.__code__, vars(startup_entry) | {"build": build, "STARTUP": STARTUP})
    run()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("gameplay", "startup"))
    globals()[parser.parse_args().action]()
