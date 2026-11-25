"""Explicitly qualify historical source-only inputs against the own-current context.

Read both original cold-boot snapshots independently. Never transplant historical
RAM or treat equal actor/code inputs as equality of the complete snapshots.
"""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B52_profile_v1 import contract
from scripts.probe_escape_direct_source_v1186 import machine


def qualify_source_context(source, parent, current_input, load, require):
    frozen = contract()
    old_path = Path(source['current_native_input'])
    require(sha(old_path.read_bytes()) == source['current_native_input_sha256'] == frozen['dependencies'][str(old_path.resolve())], 'exact historical source-only input identity')
    old, current = load(old_path), load(current_input)
    require(old['registered_profile'] == 'all-routes-unified-v8543' and current['registered_profile'] == 'all-routes-unified-v8609', 'explicit historical/current registered contexts')
    require(source['candidate_sha256'] == old['current_ROM_sha256'] and current['current_ROM_sha256'] == sha(bytes(parent.rom.save())), 'separate historical source/current parent identities')
    images = [NdsImage.open(old['current_ROM']), parent]
    require(sha(Path(old['current_ROM']).read_bytes()) == old['current_ROM_sha256'], 'complete historical source ROM')
    for path in ['/__arm9__.bin', '/COMMON/MESFILE.DK4', '/GRP/KANJI.FNT', '/data/EV1.DK4']:
        require(images[0].read_file(path) == parent.read_file(path), 'complete unchanged source/current consumer input:' + path)
    snapshots, actor_tables, bindings = [], [], []
    for doc, image in zip([old, current], images, strict=True):
        context = load(doc['native_context_proof'])
        report = load(context['capture_report'])
        require(sha(Path(context['capture_report']).read_bytes()) == context['capture_report_sha256'], 'original cold-boot report hash')
        require(report['ROM_sha256'] == doc['current_ROM_sha256'] and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'], 'each original own-ROM cold boot')
        snap = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == context['frame'])
        raw = Path(snap['path']).read_bytes()
        require(snap['read_only_export'] and sha(raw) == snap['sha256'] == context['snapshot_sha256'], 'each original readonly snapshot')
        cpu, get, unused = machine(image.read_file('/__arm9__.bin'), image.read_file('/COMMON/MESFILE.DK4'), raw, dict(patches=[]))
        require(get(0x7F244) == doc['expected_original_captain_ID'] == 1, 'same original captain1')
        actors = bytes(cpu.mem_read(get(0xCB184), 0x1A04))
        actor_tables.append(actors)
        snapshots.append(raw)
        bindings.append(dict(profile=doc['registered_profile'], input=str(old_path if doc is old else current_input),
             ROM_sha256=doc['current_ROM_sha256'], snapshot_sha256=sha(raw), frame=snap['frame'], whole_actor_table_sha256=sha(actors)))
    require(actor_tables[0] == actor_tables[1], 'complete actor tables exactly equal')
    return dict(bindings=bindings, original_source_context_is_V8543_not_V8609=True,
         complete_ARM9_COMMON_font_EV1_andwhole_actors_equal=True, whole_RAM_snapshots_equal=snapshots[0] == snapshots[1],
         no_historical_RAM_overlay_orcode_patch=True,
         event_getter_results_andsource_control_consumers_require_separate_current_native_execution=True,
         no_natural_event_activation_orfull_simulation_equivalence_claim=True)
