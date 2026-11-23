"""Trace stored attack-message requests through the original Madeira attack controls."""

from argparse import ArgumentParser
from inspect import getsource
from io import StringIO
from json import dumps
from pathlib import Path
import sys
from types import FunctionType

from scripts import native_aftermath_battle_fixture_v1269 as terrain
from scripts import native_aftermath_city_fixture_v1285 as location
from scripts import native_battle_fixture_v620 as fixtures
from scripts import observe_online_gallery_common_v1 as observer
from scripts import observe_setup_save_common_v1 as common_observer
from scripts import register_all_routes_final_flagged_wraps_20261118 as parent
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_personal_gameplay_v841 import get_machine

base, native = parent.base, parent.native
ROOT = Path("work/attack_display_ownership_20261118")
REFERENCE = Path("E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_city_v1286_1266/capture_report.json")
FOCUS = {300, 304}


def schedule(_case):
    earlier = base.load(REFERENCE)
    assert earlier["cold_boot"] and earlier["frames"] == 6940
    assert not earlier["callback_errors"] and not earlier["savestate_loaded"]
    donor = earlier["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"] == "2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1"
    fixtures, = earlier["synthetic_battle_recovery_proximity_fixtures"]
    assert fixtures["frame"] == 5000 and fixtures["context"] == "Madeira_neutral_location_only"
    frames = [4800, 5000, 5920, 6020, 6120, 6220, 6320, 6420, 6520, 6620, 6740, 6940]
    return earlier["scripted_input_schedule"], frames, 6940, REFERENCE, donor


def ally_town(arm, raw):
    cpu, get = get_machine(arm, raw)
    companies, towns = get(0xCB160), get(0xCB178)
    town = towns + 4 + 30 * 108
    assert [(i, get(0xB4AA8, town, i)) for i in range(21) if get(0xB4AA8, town, i)] == [(6, 57)]
    player, occupant = [companies + 4 + i * 76 for i in (2, 6)]
    assert get(0x3D030, player) == 2 and get(0x3D030, occupant) == 6
    assert get(0x3CB30, occupant, 2) == get(0x3CB30, player, 6) == 0
    get(0x3C8F4, occupant, 2, 1, 21)
    assert get(0x3CB30, occupant, 2) == get(0x3CB30, player, 6) == 1
    start = location.BASE
    owned = {player + 0x1F + 6}
    result = bytes(cpu.mem_read(start, len(raw)))
    changed = {start + i for i, (a, b) in enumerate(zip(raw, result, strict=True)) if a != b}
    assert changed == owned
    return result, dict(player_company=2, allied_occupant=6, town_id=30,
        changed_addresses=sorted(changed), both_native_relation_getters_allied=True, only_relation_byte_changed=True)


def run(case):
    release = base.load(parent.RELEASE)
    image = base.NdsImage.open(parent.ROM)
    arm = image.read_file(native.ARM)
    original = base.NdsImage.open(native.CLEAN).read_file(native.ARM)
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert native.digest(arm) == release["target_ARM9_sha256"]
    assert all(arm[lo:hi] == original[lo:hi] for lo, hi in ((0x6ED34, 0x6EE90), (0x6F4D4, 0x6F7A4)))
    if case == "allied_v2":
        assert all(arm[lo:hi] == original[lo:hi] for lo, hi in ((0x3C8F4, 0x3CB30), (0x3CB30, 0x3CBF0)))

    location_source = checked_text(getsource(location.apply_fixture), {
        "read('translations/battle_aftermath_editorial_release_v1.json')['target_arm9_sha256']":
            'release["target_ARM9_sha256"]',
    })
    rebound_water = FunctionType(terrain.water.__code__, vars(terrain) | {"ROM": parent.ROM})
    local = vars(location) | {"release": release, "water": rebound_water}
    exec(compile(location_source, __file__ + "::same-Madeira-location", "exec"), local)

    def location_fixture(actual, raw, request):
        result, receipt = local["apply_fixture"](actual, raw, request)
        if case == "allied_v2":
            prior = result
            result, relation = ally_town(actual, prior)
            for address in relation["changed_addresses"]:
                offset = address - location.BASE
                receipt["owned_bytes"].append(address)
                receipt["changes"].append(dict(address=address, before=prior[offset], after=result[offset]))
            receipt.update(context="Madeira_with_allied_occupant", relationship_fixture=relation,
                after_RAM_sha256=native.digest(result), only_own_cached_and_live_position_changed=False,
                diplomacy_actors_IDs_defender_defenses_shares_health_RNG_and_events_unchanged=False)
        return result, receipt

    source = checked_text(getsource(observer.main), {
        "    installed = []": '''    argv.extend(["--pause-at", "5000", "--allow-battle-fixtures", "--dump-capture-ram"])
    commands = (dict(until=end, duration=1, battle_fixture={"city_context":"MadeiraNeutral"}), dict(stop=True))
    prior_fixture, prior_input = fixtures.apply_fixture, sys.stdin
    fixtures.apply_fixture, sys.stdin = location_fixture, StringIO("".join(dumps(c) + "\\n" for c in commands))
    installed = []''',
        "        harness.ct, sys.argv = native, original_argv": '''        harness.ct, sys.argv = native, original_argv
        fixtures.apply_fixture, sys.stdin = prior_fixture, prior_input''',
        "    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))": '''    fixture, = report["synthetic_battle_recovery_proximity_fixtures"]
    assert fixture["frame"] == 5000
    if case == "allied_v2":
        assert fixture["relationship_fixture"]["only_relation_byte_changed"]
    else:
        assert fixture["only_own_cached_and_live_position_changed"]
        assert fixture["diplomacy_actors_IDs_defender_defenses_shares_health_RNG_and_events_unchanged"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_")
        and key != "synthetic_battle_recovery_proximity_fixtures")
    assert report["scripted_input_schedule"] == events
    assert all({r["message_ID"] for r in trace.requests if r["PC"] == pc} for pc in common_observer.REQUESTS)''',
        "prepared_gallery_save=bool(donor)": "preloaded_existing_save=bool(donor), location_fixture=fixture",
    })
    scope = vars(observer) | globals() | dict(observer=common_observer.scoped_observer,
        get_schedule=schedule, location_fixture=location_fixture)
    exec(compile(source, __file__ + "::original-attack-request-capture", "exec"), scope)
    scope["main"](case)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("neutral_v2", "allied_v2"))
    run(parser.parse_args().case)
