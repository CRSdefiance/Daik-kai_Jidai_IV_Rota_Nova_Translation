"""Trace shared requests during fleet targeting, declaration, and return to sailing."""

from inspect import getsource
from io import StringIO
from json import dumps
from pathlib import Path
import sys

from scripts import native_battle_fixture_v620 as adapter
from scripts import native_stronger_fleet_location_v1471 as approach
from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as common_trace
from scripts import register_map_cluster_suffix_20261121 as current
from scripts.source_locked_derivation_v5118 import checked_text


base, native = current.base, current.native
ROOT = Path("work/fleet_attack_shared_20261121")
HISTORICAL = Path("work/emulation_v193/declaration_responses_v1546_1542/capture_report.json")
CENSUS = Path("work/analysis/original_fleet_guns_v1469/original_fleet_census.json")
FOCUS = {300, 304}
PAUSE = 4800


def schedule(_case):
    report = base.load(HISTORICAL)
    fixture, = report["synthetic_battle_recovery_proximity_fixtures"]
    assert fixture["frame"] == PAUSE and fixture["context"] == "existing_stronger_fleet4_location_only"
    frames = [4800, 5300, 5355, 5450, 5550, 5650, 5750, 5850, 5918,
              6010, 6120, 6800, 6950, 8200, 8400, 8600, 8800, 9100, 9200]
    assert report["frames"] == 9200 and report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    return report["scripted_input_schedule"], frames, report["frames"], HISTORICAL, report["battery_save_preloaded"]


def main():
    assert not ROOT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release["candidate_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    arm = base.NdsImage.open(current.ROM).read_file(native.ARM)
    assert native.digest(arm) == release["target_ARM9_sha256"]
    clean = base.NdsImage.open(native.CLEAN).read_file(native.ARM)
    census = base.load(CENSUS)
    spans = [*census["original_getter_spans"], (0x69B5C, 0x69E00), (0x6ED34, 0x6EE90), (0x6F4D4, 0x6F7A4)]
    assert all(arm[lo:hi] == clean[lo:hi] for lo, hi in spans)
    apply = checked_text(getsource(approach.apply_fixture), {
        "    release=read('work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json')\n"
        "    assert sha(arm)==release['ARM9_sha256']": "    assert arm == expected_arm",
        "    assert census['candidate_sha256']==release['candidate_sha256']": "    assert census == source_census",
        "    assert not get(0x36C70,enemy+12)": """    assert not get(0x36C70,enemy+12)
    for ship in target['ships']:
        model=get(model_getter,enemy+12+8*ship['slot'])
        assert model==ship['model'] and get(0x1856C,model)==ship['original_cannon_type']
        assert [get(0x183A0,model),get(0x181BC,model)]==ship['stored_Hull_Crew']""",
    })
    fixture_context = vars(approach) | dict(ROM=current.ROM, expected_arm=arm, source_census=census,
        model_getter=0x36C94, __file__=__file__)
    exec(compile(apply, __file__ + "::stock-approach", "exec"), fixture_context)

    observe = checked_text(getsource(playback.main), {
        "    installed = []": """    argv.extend(['--pause-at', str(PAUSE), '--allow-battle-fixtures'])
    local_commands = [dict(until=end, battle_fixture={'ship_sinking_context':'five_ship_approach'}), dict(stop=True)]
    fallback, input_stream = adapter.apply_fixture, sys.stdin
    adapter.apply_fixture = approach_fixture
    sys.stdin = StringIO(''.join(dumps(command) + '\\n' for command in local_commands))
    installed = []""",
        "        harness.ct, sys.argv = native, original_argv": """        harness.ct, sys.argv = native, original_argv
        adapter.apply_fixture, sys.stdin = fallback, input_stream""",
        "    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))": """    fixtures, = report['synthetic_battle_recovery_proximity_fixtures']
    assert fixtures['frame']==PAUSE and fixtures['original_existing_enemy_fleet']==4
    assert len(fixtures['owned_bytes'])==40 and fixtures['all_other4MiB_enemy_health_crew_equipment_actors_IDs_RNG_eligibility_and_results_exact']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_')
        and key != 'synthetic_battle_recovery_proximity_fixtures')
    assert report['scripted_input_schedule']==events
    assert trace.header[2]==len(trace.requests)>0""",
    })
    scope = vars(playback) | globals() | dict(parent=current, observer=common_trace.scoped_observer,
        get_schedule=schedule, approach_fixture=fixture_context["apply_fixture"])
    exec(compile(observe, __file__ + "::shared-fleet-attack-replay", "exec"), scope)
    scope["main"]("attack")


if __name__ == "__main__":
    main()
