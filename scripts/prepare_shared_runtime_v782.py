"""Research-only source ownership and exact CPU routing for the shared batch."""

import inspect
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch import shared_dialogue_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts import research_scheme_selector_v775 as selector
from scripts import verify_scheme_storage_v776 as storage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shared_integration_v782')
CURRENT = Path('out/all_routes_combined_v780_candidate.nds')


def execute(fn, env, replacements, filename):
    source = inspect.getsource(fn)
    for old, new in replacements.items():
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    path = ROOT / filename
    path.write_text(source, encoding='utf-8')
    exec(compile(source, str(path), 'exec'), env)
    env['main']()
    return {'path': str(path), 'sha256': sha(source.encode())}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    assert sha(arm) == runtime.SOURCE
    table, gate, assembly = runtime.assemble()
    old_gate = runtime.previous_gate.assemble()[1]
    old_table = runtime.previous.table()
    storage_program = execute(storage.main, {
        **storage.__dict__, 'ROOT': ROOT, 'new': runtime,
        'current_table': old_table, 'current_gate': old_gate,
        '__file__': str(Path(__file__).resolve())}, {
        "rom=NdsImage.open('out/all_routes_combined_v773_candidate.nds')": f'rom=NdsImage.open({str(CURRENT)!r})',
        'gate=old.assemble()[old.GATE]': 'gate=current_gate+old.assemble()[old.GATE][len(current_gate):]',
        'table=old.assemble()[old.CONTRACTS]': 'table=current_table+old.assemble()[old.CONTRACTS][len(current_table):]',
        "plan=read('work/analysis/tavern_scheme_selector_v775/two_patch_plan.json')\n    assert new.code()=={r['address']:bytes.fromhex(r['target_hex']) for r in plan['patches']}\n    assert len(new.code()[old.GATE])<=len(gate) and len(new.code()[old.CONTRACTS])<=len(table)":
            'assert len(new.code()[old.CONTRACTS])==128==len(table)\n    assert len(new.code()[old.GATE])==144==len(gate)\n    assert set(new.code())=={old.CONTRACTS,old.GATE}',
        "print('Current private references close to the original bridge/table consumer;production code equals the two-patch plan.',flush=True)":
            "print('Existing128-byte table and144-byte gate ownership and incoming references verified.',flush=True)",
    }, 'effective_storage_proof.py')
    scope_program = execute(selector.main, {
        **selector.__dict__, 'ROOT': ROOT, 'contract_rows': runtime.contract_rows,
        'assemble': runtime.assemble, '__file__': str(Path(__file__).resolve())}, {
        "rom_path=Path('out/all_routes_combined_v773_candidate.nds')": f'rom_path=Path({str(CURRENT)!r})',
        'prior.COORD if low==842 else': 'prior.COORD if low in (842,1028,1029) else',
        "'exact_new_five_narration_three_confirmation_tables'": "'all_prior_and_shared1020_1069_exact_consumer_contracts'",
        "'unreviewed_021182E0_and_all_between_table_addresses_rejected'": "'all_unselected_between_table_addresses_rejected'",
    }, 'effective_selector_proof.py')
    target = bytearray(arm)
    patches = []
    for at, blob in runtime.code().items():
        offset = at - 0x02000000
        patches.append({'address': at, 'source_hex': arm[offset:offset+len(blob)].hex(), 'target_hex': blob.hex(),
                        'existing_owned_capacity': len(blob)})
        target[offset:offset+len(blob)] = blob
    target = bytes(target)
    before, after = [MainCodeFile(a, 0x02000000) for a in (arm, target)]
    assert len(target) == len(arm) and cache_plan(target) == cache_plan(arm)
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in before.sections] == [(s.ramAddress, len(s.data), s.bssSize) for s in after.sections]
    assert bytes(after.save()) == target
    owned = {i for at, blob in runtime.code().items() for i in range(at-0x02000000, at-0x02000000+len(blob))}
    assert all(a == b or i in owned for i, (a, b) in enumerate(zip(arm, target)))
    (ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin').write_bytes(target)
    save(ROOT/'runtime_plan.json', {
        'source_ROM_sha256': sha(CURRENT.read_bytes()), 'source_ARM9_sha256': sha(arm), 'target_ARM9_sha256': sha(target),
        'patches': patches, 'all_other_ARM9_bytes_sections_BSS_cache_and_staged_payload_exact': True,
        'native_scope_cases': read(ROOT/'scope_proof.json')['cases'], 'effective_programs': [storage_program, scope_program],
        'runtime_module_sha256': sha(Path(runtime.__file__).read_bytes()),
        'consumer_eligibility_and_production_integration_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('128-byte table and144-byte gate fit without growth;exact native routing passes. Research only.', flush=True)


if __name__ == '__main__':
    main()
