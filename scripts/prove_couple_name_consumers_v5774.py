"""Bind both reopened role labels to current native getters and exact staged owners."""
import inspect
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/couple_name_consumers_v5774')
SOURCE = Path('work/analysis/lil_B199_source_v5767/all31_clean_current_complete_context.json')
CATALOG = Path('work/analysis/lil_B199_voices_v5768/current207_catalog_eight_voices_and_three_source_selectors.json')
CENSUS = Path('work/analysis/couple_speaker_uses_v5773b/all_four_routes_direct_role_speech_census_and_complete_native_exchanges.json')
BASE, POOL = 0x02000000, 0x02387A20

if __name__ == '__main__':
    assert not ROOT.exists()
    packet, catalog, census = map(read, [SOURCE, CATALOG, CENSUS])
    assert census['source_blocks_scanned'] == 1307
    assert sum(len(b['direct_couple_speech_records']) for b in census['selected_native_blocks']) == 96
    image = NdsImage.open(packet['current_ROM'])
    arm = image.read_file('/__arm9__.bin')
    sections = MainCodeFile(arm, BASE).sections
    payload = bytes(sections[3].data[:-48])
    assert sections[3].ramAddress == 0x023A7200 and len(payload) == 123040
    adapted = inspect.getsource(names)
    assert adapted.count('for ident in [2,4,13,23,109]:') == 1
    adapted = adapted.replace('for ident in [2,4,13,23,109]:', 'for ident in [164,165]:')
    adapted = adapted.replace('all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact',
                              'all_four_original_consumers_and_owned_or_readonly_memory_paths_exact')
    env = dict(names.__globals__)
    exec(compile(adapted, __file__ + '::source-bound-role-consumers', 'exec'), env)
    ROOT.mkdir(parents=True)
    ctx = CurrentContext('work/analysis/lil_B199_voices_v5768/current_native_input.json',
                         packet['historical_snapshot_ROM'], ROOT / 'current_context')
    native = ctx.execute(env['names'])
    ctx.machines.pop()
    assert not ctx.machines
    expected = {164: 'Man in a Couple', 165: 'Woman in a Couple'}
    assert len(native['rows']) == 4
    owners = []
    for ident, text in expected.items():
        field = 0x120B80 + ident * 32
        pointer = struct.unpack_from('<I', arm, field)[0]
        data = text.encode('ascii') + b'\0'
        at = pointer - POOL
        assert payload[at:at+len(data)] == data
        hits = [i for i in range(len(arm)-3) if arm[i:i+4] == struct.pack('<I', pointer)]
        assert hits == [field], (ident, hits)
        table_aliases = []
        for actor in range(207):
            for delta in [0, 4, 8]:
                f = 0x120B80 + actor*32 + delta
                p = struct.unpack_from('<I', arm, f)[0]
                if pointer <= p < pointer + len(data):
                    table_aliases.append(dict(actor_ID=actor, field=f, pointer=p, interior_delta=p-pointer))
        assert table_aliases == [dict(actor_ID=ident, field=field, pointer=pointer, interior_delta=0)]
        rows = [r for r in native['rows'] if r['actor_ID'] == ident]
        assert len(rows) == 2 and all(r['text'] == text and r['pointer'] == pointer and
            r['ownership_mode'] == 'original-read-only-name-pointer-without-scratch-ring' and
            r['all_actor_models_and_unowned4MiB_exact'] for r in rows)
        cat = next(r for r in catalog['catalog']['rows'] if r['actor_ID'] == ident)
        assert cat['current_catalog_name'] == text and cat['pointer'] == pointer
        owners.append(dict(actor_ID=ident, source_file='/__arm9__.bin', pointer_field=field,
            runtime_pointer=pointer, current_English=text, terminated_hex=data.hex(),
            staged_payload_offset=at, staged_payload_bytes=len(data),
            exact_ARM9_literal_pointer_occurrences=hits, all207_primary_secondary_middle_table_aliases=table_aliases,
            current_catalog_reference=f'{CATALOG}#/catalog/rows/{catalog["catalog"]["rows"].index(cat)}',
            no_unknown_literal_ARM9_pointer_or_name_table_interior_alias=True))
    save(ROOT/'four_current_native_role_getters_and_exact_staged_owners.json', dict(
        candidate=packet['current_ROM'], candidate_sha256=packet['current_ROM_sha256'],
        ARM9_sha256=sha(arm), original_native_cases=native, current_exact_owners=owners,
        original_source_owned_adapter=adapted, context_plan=str(ctx.proof_path),
        context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        literal_name_table_and_ARM9_pointer_census_not_exhaustive_dynamic_consumer_proof=True,
        proposed_Man_Woman_not_applied_or_display_approved=True,
        actual_couple_scene_capture_not_performed=True, previous_tea_screenshot_is_user_evidence_only=True,
        no_current_ROM_registry_ledger_or_manuscript_changed=True,
        new_ROMs=0, new_emulator_runs=0, new_editorial_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in [SOURCE, CATALOG, CENSUS, Path(__file__)]},
        full_goal_complete=False))
    print('Four current read-only name consumers and two sole staged name-table owners exact; no label revision applied.')
