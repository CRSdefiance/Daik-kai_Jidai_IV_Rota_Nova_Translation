"""Revalidate private storage and exact native routing;write a CPU research patch."""

import inspect
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch import scheme_followup_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts import verify_scheme_storage_v776 as storage
from scripts import research_scheme_selector_v775 as selector
from scripts.review_scheme_followup_v777 import CURRENT
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/scheme_followup_integration_v778')


def execute(fn, env, replacements, filename):
    source = inspect.getsource(fn)
    for before, after in replacements.items():
        assert source.count(before) == 1, before
        source = source.replace(before, after)
    path = ROOT/filename
    path.write_text(source, encoding='utf-8')
    exec(compile(source, str(path), 'exec'), env)
    env['main']()
    return {'path': str(path), 'sha256': sha(source.encode())}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    assert sha(arm) == runtime.SOURCE
    replacement = {
        "rom=NdsImage.open('out/all_routes_combined_v773_candidate.nds')": f'rom=NdsImage.open({str(CURRENT)!r})',
        'gate=old.assemble()[old.GATE]': 'gate=new.previous.assemble()[1]+old.assemble()[old.GATE][140:]',
        'table=old.assemble()[old.CONTRACTS]': 'table=new.previous.assemble()[0]+old.assemble()[old.CONTRACTS][100:]',
        "plan=read('work/analysis/tavern_scheme_selector_v775/two_patch_plan.json')\n    assert new.code()=={r['address']:bytes.fromhex(r['target_hex']) for r in plan['patches']}\n    assert len(new.code()[old.GATE])<=len(gate) and len(new.code()[old.CONTRACTS])<=len(table)":
            'assert len(new.code()[old.CONTRACTS])==110<=len(table)\n    assert set(new.code())=={old.CONTRACTS}',
        "print('Current private references close to the original bridge/table consumer;production code equals the two-patch plan.',flush=True)":
            "print('Current128/144-byte private spans and all incoming references verified;only110 table bytes will change.',flush=True)",
    }
    storage_env = {**storage.__dict__, 'ROOT': ROOT, 'new': runtime, '__file__': str(Path(__file__).resolve())}
    storage_program = execute(storage.main, storage_env, replacement, 'effective_storage_proof.py')
    table = runtime.table()
    _, gate, assembly = runtime.previous.assemble()
    selector_env = {**selector.__dict__, 'ROOT': ROOT, 'contract_rows': runtime.contract_rows,
                    'assemble': lambda: (table, gate, assembly), '__file__': str(Path(__file__).resolve())}
    scope_program = execute(selector.main, selector_env, {
        "rom_path=Path('out/all_routes_combined_v773_candidate.nds')": f'rom_path=Path({str(CURRENT)!r})',
        "'exact_new_five_narration_three_confirmation_tables'": "'all_prior_and_four_new_voice_tables_plus_numeric972_exact'",
        "'unreviewed_021182E0_and_all_between_table_addresses_rejected'": "'all_unselected_between_table_addresses_rejected'",
    }, 'effective_selector_proof.py')
    at = runtime.CONTRACTS
    off = at-0x02000000
    before = arm[off:off+len(table)]
    target = arm[:off]+table+arm[off+len(table):]
    code, result = [MainCodeFile(a, 0x02000000) for a in (arm, target)]
    assert len(target) == len(arm) and cache_plan(target) == cache_plan(arm)
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in code.sections] == [(s.ramAddress, len(s.data), s.bssSize) for s in result.sections]
    assert bytes(result.save()) == target
    assert arm[:off] == target[:off] and arm[off+len(table):] == target[off+len(table):]
    for address, length in ((runtime.GATE, 144), (runtime.previous.prior.STATUS_CONSTANTS, 24),
                            (runtime.previous.prior.PACKED_PHRASES, 24)):
        position = address-0x02000000
        assert arm[position:position+length] == target[position:position+length]
    assert read(ROOT/'scope_proof.json')['cases'] == 34343
    (ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin').write_bytes(target)
    save(ROOT/'runtime_plan.json', {
        'source_ROM_sha256': sha(CURRENT.read_bytes()), 'source_ARM9_sha256': sha(arm),
        'target_ARM9_sha256': sha(target),
        'patches': [{'address': at, 'source_hex': before.hex(), 'target_hex': table.hex(), 'existing_owned_capacity': 128}],
        'unchanged140_byte_gate_within144_and_all_other_ARM9_bytes_exact': True,
        'all_section_BSS_cache_and_staged_payload_geometry_exact': True,
        'native_scope_cases': 34343, 'effective_programs': [storage_program, scope_program],
        'original_producers': {str(Path(m.__file__)): sha(Path(m.__file__).read_bytes()) for m in (storage, selector)},
        'producer_sha256': sha(Path(__file__).read_bytes()), 'no_playable_ROM_claim': True,
        'full_goal_complete': False})
    print('One110-byte table patch verified;gate and every other ARM9 byte exact. No allocation growth.', flush=True)


if __name__ == '__main__':
    main()
