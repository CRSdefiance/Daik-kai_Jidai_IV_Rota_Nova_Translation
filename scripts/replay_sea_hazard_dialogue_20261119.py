"""Exercise the staged shared hazard dialogue using the original sailing dispatcher."""

from argparse import ArgumentParser
from struct import pack_into, unpack_from
from types import FunctionType

from scripts import replay_fleet_encounter_dialogue_20261119 as encounter
from scripts import replay_sea_event_dialogue_followup_20261118 as previous
from scripts import stage_sea_hazard_dialogue_20261119 as build
from scripts import verify_sea_event_dialogue_followup_20261118 as previous_verify

STARTUP = build.ROOT / "startup_fixture"
EVENTS = {"whirlpool": 13}

choose_event = FunctionType(encounter.set_condition.__code__, vars(encounter) | {
    "build": build, "EVENTS": EVENTS,
})


def set_condition(arm, raw, request):
    if request != {"event": "whirlpool", "mode": "place_first_contact_zone"}:
        return choose_event(arm, raw, request)

    assert arm == build.base.NdsImage.open(build.ROM).read_file(build.ARM)
    clean = build.base.NdsImage.open(build.CLEAN).read_file(build.ARM)
    assert arm[0x72BDC:0x7313C] == clean[0x72BDC:0x7313C]
    assert arm[0xCB19C:0xCB1B4] == clean[0xCB19C:0xCB1B4]
    world, fleet, session = (unpack_from("<I", arm, at)[0] - encounter.earlier.BASE
                             for at in (0xCB1A4, 0xCB1B0, 0x2E598))
    player = unpack_from("<I", raw, session + 0x48)[0]
    lead_ship = raw[fleet + 4 + 0x84 * player + 0x11]
    assert player == 1 and lead_ship == 0
    assert raw[fleet + 0x2090 + 0x2C] == 17 and raw[world + 0xE64] & 1
    ship_position = unpack_from("<2i", raw, world + 4 + 0x1C * lead_ship + 0x10)
    zone = world + 0xE68
    old_position = unpack_from("<2i", raw, zone)
    assert old_position != ship_position
    edited = bytearray(raw)
    pack_into("<2i", edited, zone, *ship_position)
    changes = [dict(address=encounter.earlier.BASE+i, before=raw[i], after=edited[i])
               for i in range(zone, zone+8) if raw[i] != edited[i]]
    return bytes(edited), dict(event=request["event"], mode=request["mode"],
        area_slot=0, changes=changes, old_position=old_position, ship_position=ship_position,
        game_initialized_existing_whirlpool=True, only_one_contact_zone_position_changed=True,
        natural_random_selection_verified=False)


def schedule(event):
    commands = [
        dict(until=9627, condition_fixture={"event": event, "mode": "choose"},
             buttons=["UP"], duration=400),
        dict(until=9827, condition_fixture={"event": event, "mode": "restore"},
             buttons=["A"], duration=8),
        dict(until=10027, buttons=["A"], duration=8),
        dict(until=10227, buttons=["A"], duration=8),
        dict(until=10627, buttons=["UP"], duration=400),
        dict(until=11027, buttons=["UP"], duration=400),
        dict(until=11227, buttons=["A"], duration=8),
        dict(until=11427, buttons=["A"], duration=8),
        dict(until=11627),
        dict(stop=True),
    ]
    return 11627, commands


def contact_schedule(event):
    _, commands = schedule(event)
    return 11227, commands[:3] + [
        dict(until=10427, condition_fixture={"event": event, "mode": "place_first_contact_zone"},
             buttons=["A"], duration=8),
        dict(until=10627, buttons=["RIGHT"], duration=200),
        dict(until=10827, buttons=["A"], duration=8),
        dict(until=11027, buttons=["RIGHT"], duration=200),
        dict(until=11227),
        dict(stop=True),
    ]


def startup():
    replay = FunctionType(previous.startup.__code__, vars(previous) | {"stage": build, "STARTUP": STARTUP})
    replay()
    verify = FunctionType(previous_verify.startup.__code__, vars(previous_verify) | {
        "stage": build, "replay": type("Startup", (), {"STARTUP": STARTUP}),
        "STARTUP": build.ROOT / "own_startup_verification.json",
    })
    verify()


def gameplay(with_contact=False):
    replay = FunctionType(encounter.run.__code__, vars(encounter) | {
        "build": build, "ROOT": build.ROOT / ("replays_contact" if with_contact else "replays"),
        "schedule": contact_schedule if with_contact else schedule,
        "set_condition": set_condition,
    })
    replay("whirlpool")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("gameplay", "contact", "startup"))
    action = parser.parse_args().action
    if action == "startup":
        startup()
    else:
        gameplay(with_contact=action == "contact")
