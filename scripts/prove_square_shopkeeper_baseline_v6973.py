"""Read the current original name consumers and both complete literal-owner ranges.

This is an offline baseline from the exact retained V6956 startup snapshot. It
does not change a name, visit a catalogue screen or add editorial credit.
"""
import contextlib
import inspect
import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_shrines_voices_v3167 import names as catalogue_names
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/square_shopkeeper_baseline_v6973')
SCOPE = Path('work/analysis/square_shopkeeper_scope_v6972/ten_source_identical_roles_current_owners_alias_fields_and_whole_clean_story_contexts.json')
INPUT = Path('work/analysis/current_V6956_native_v6966/current_native_input.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    scope, inp = read(SCOPE), read(INPUT)
    assert inp['current_ROM_sha256'] == scope['current_ROM_sha256']
    image = NdsImage.open(inp['current_ROM'])
    assert sha(Path(inp['current_ROM']).read_bytes()) == inp['current_ROM_sha256']
    arm = image.read_file('/__arm9__.bin')
    assert sha(arm) == scope['current_ARM9_sha256']
    owners = scope['current_literal_owners']
    assert len(owners) == 2 and all(o['bytes'] == 18 for o in owners)
    needles = {struct.pack('<I', o['pointer'] + delta): (o, delta)
               for o in owners for delta in range(o['bytes'])}
    pointer_hits = []
    components = []
    for component, data in [('ARM9', arm), *[(n, d) for n, d in image.iter_components() if n != '/__arm9__.bin']]:
        components.append(dict(component=component, bytes=len(data), sha256=sha(data)))
        for needle, (owner, delta) in needles.items():
            at = data.find(needle)
            while at >= 0:
                pointer_hits.append(dict(component=component, offset=at,
                    owner_pointer=owner['pointer'], pointer=owner['pointer'] + delta,
                    interior_delta=delta))
                at = data.find(needle, at + 1)
    actual = {(r['component'], r['offset'], r['pointer']) for r in pointer_hits}
    expected = {('ARM9', r['pointer_field'], r['pointer'])
                for r in scope['current_declared_name_field_aliases']}
    assert len(actual) == len(pointer_hits) == 10 and actual == expected
    assert all(r['interior_delta'] == 0 for r in pointer_hits)
    adapter = checked_text(inspect.getsource(names), {
        'for ident in [2,4,13,23,109]:': 'for ident in range(207):',
        'actor = root+4+32*ident': 'actor = root+0x19E4 if ident==2 else root+4+32*ident',
        'all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact':
            'all414_original_consumers_and_owned_or_readonly_memory_paths_exact'})
    env = dict(names.__globals__)
    exec(compile(adapter, __file__ + '::all-original-name-getters', 'exec'), env)
    ROOT.mkdir(parents=True)
    ctx = CurrentContext(INPUT, 'unused-no-historical-ROM', ROOT / 'current_context')
    with (ROOT / 'all414_getter_log.txt').open('w', encoding='utf-8') as log, contextlib.redirect_stdout(log):
        native = ctx.execute(env['names'])
        ctx.machines.pop()
        catalogue = ctx.execute(catalogue_names)
        ctx.machines.pop()
    assert not ctx.machines and len(native['rows']) == 414 and len(catalogue['rows']) == 207
    assert {r['original_voice_class'] for r in catalogue['rows']} == set(range(8))
    affected = [r for r in native['rows'] if 82 <= r['actor_ID'] <= 91]
    assert len(affected) == 20
    role_fields = {r['actor_ID']: r['fields'][0] for r in scope['actors']}
    for row in affected:
        assert row['text'] == 'Square Shopkeeper'
        assert row['pointer'] == role_fields[row['actor_ID']]['current_pointer']
        assert row['ownership_mode'] == 'original-read-only-name-pointer-without-scratch-ring'
        assert not row['original_scratch_rings'] and not row['original_getter_writes']
    complete_labels = {164: 'Man', 165: 'Woman', 172: 'Stranger', 173: 'Shady Man'}
    for row in native['rows']:
        if row['actor_ID'] in complete_labels:
            assert row['text'] == complete_labels[row['actor_ID']]
    save(ROOT / 'all414_current_getters207_voices_and_all36_owner_pointer_values.json', dict(
        current_ROM=inp['current_ROM'], current_ROM_sha256=inp['current_ROM_sha256'],
        current_ARM9_sha256=sha(arm), original_name_consumers=native,
        catalogue_and_original_voices=catalogue, ten_role_twenty_getters=affected,
        current_completed_generic_labels=complete_labels,
        all36_owner_base_and_interior_pointer_values_scanned_in_every_component=True,
        component_hashes=components, exact_pointer_hits=pointer_hits,
        only_ten_declared_fields_reference_either_complete_owner_range=True,
        no_interior_pointers_found=True,
        all414_getters_restore_all4MiB_with_original_owned_scratch_or_readonly_paths=True,
        all207_voices_eight_groups_and_actual_captain_object_preserved=True,
        shared_dynamic_caller_and_complete_source_context_review_pending=True,
        native_catalogue_getter_is_not_actual_catalogue_UI_visit=True,
        source_owned_getter_adapter=adapter,
        native_context_plan=str(ctx.proof_path),
        native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p): sha(p.read_bytes()) for p in [SCOPE, INPUT,
            Path(names.__code__.co_filename), Path(catalogue_names.__code__.co_filename), Path(__file__)]},
        new_emulator_runs=0, new_review_credit=0, no_ROM_or_registry_or_ledger_changes=True,
        Shopkeeper_candidate_not_approved_or_integrated=True, full_goal_complete=False))
    print(dict(original_getters=414, catalogue_voices=207, role_getters=20,
        scanned_pointer_values=36, exact_pointer_fields=10, interior_hits=0,
        completed_labels=complete_labels, new_credit=0))
