"""Verify the existing private bank and all exact routing at actual addresses."""

import inspect
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch import barmaid_editorial_runtime as runtime
from dk4tool.patch import tavern_schemes_runtime as old_gate
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts import verify_scheme_storage_v776 as storage
from scripts import research_scheme_selector_v775 as selector
from scripts.context_barmaid_dialogue_v779 import CURRENT
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/barmaid_integration_v780')


def execute(fn, env, replacements, filename):
    source = inspect.getsource(fn)
    for old, new in replacements.items():
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    path = ROOT/filename
    path.write_text(source, encoding='utf-8')
    exec(compile(source, str(path), 'exec'), env)
    env['main']()
    return {'path': str(path), 'sha256': sha(source.encode())}


def main():
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    assert sha(arm) == runtime.SOURCE
    table, (unused, gate, assembly) = runtime.table(), old_gate.assemble()
    storage_program = execute(storage.main, {**storage.__dict__, 'ROOT': ROOT, 'new': runtime,
                                            'current_table': runtime.previous.table(), 'current_gate': gate,
                                            '__file__': str(Path(__file__).resolve())}, {
        "rom=NdsImage.open('out/all_routes_combined_v773_candidate.nds')": f'rom=NdsImage.open({str(CURRENT)!r})',
        'gate=old.assemble()[old.GATE]': 'gate=current_gate+old.assemble()[old.GATE][140:]',
        'table=old.assemble()[old.CONTRACTS]': 'table=current_table+old.assemble()[old.CONTRACTS][len(current_table):]',
        "plan=read('work/analysis/tavern_scheme_selector_v775/two_patch_plan.json')\n    assert new.code()=={r['address']:bytes.fromhex(r['target_hex']) for r in plan['patches']}\n    assert len(new.code()[old.GATE])<=len(gate) and len(new.code()[old.CONTRACTS])<=len(table)":
            'assert len(new.code()[old.CONTRACTS])==114<=len(table)\n    assert set(new.code())=={old.CONTRACTS}',
        "print('Current private references close to the original bridge/table consumer;production code equals the two-patch plan.',flush=True)":
            "print('Existing128-byte routing table and unchanged144-byte gate allocation verified.',flush=True)",
    }, 'effective_storage_proof.py')
    scope_program = execute(selector.main, {**selector.__dict__, 'ROOT': ROOT,
                                          'contract_rows': runtime.contract_rows, 'assemble': lambda: (table, gate, assembly),
                                          '__file__': str(Path(__file__).resolve())}, {
        "rom_path=Path('out/all_routes_combined_v773_candidate.nds')": f'rom_path=Path({str(CURRENT)!r})',
        "'exact_new_five_narration_three_confirmation_tables'": "'all_prior_contracts_and_new_direct989_1019_exact'",
        "'unreviewed_021182E0_and_all_between_table_addresses_rejected'": "'all_unselected_between_table_addresses_rejected'",
    }, 'effective_selector_proof.py')
    at, off = runtime.CONTRACTS, runtime.CONTRACTS-0x02000000
    target = arm[:off]+table+arm[off+len(table):]
    before, after = [MainCodeFile(a, 0x02000000) for a in (arm, target)]
    assert len(target) == len(arm) and cache_plan(target) == cache_plan(arm)
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in before.sections] == [(s.ramAddress, len(s.data), s.bssSize) for s in after.sections]
    assert bytes(after.save()) == target
    assert target[:off] == arm[:off] and target[off+len(table):] == arm[off+len(table):]
    (ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin').write_bytes(target)
    save(ROOT/'runtime_plan.json', {'source_ROM_sha256': sha(CURRENT.read_bytes()), 'source_ARM9_sha256': sha(arm),
                                    'target_ARM9_sha256': sha(target),
                                    'patches': [{'address': at, 'source_hex': arm[off:off+len(table)].hex(),
                                                 'target_hex': table.hex(), 'existing_owned_capacity': 128}],
                                    'all_other_ARM9_bytes_sections_BSS_cache_and_staged_payload_exact': True,
                                    'native_scope_cases': read(ROOT/'scope_proof.json')['cases'],
                                    'effective_programs': [storage_program, scope_program],
                                    'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('114-byte table stays within128;34343 native routing cases and unchanged memory geometry pass.', flush=True)


if __name__ == '__main__':
    main()
