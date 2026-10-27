"""Exhaustive original-entry native dispatch/ABI and unchanged historical exits."""
import inspect
from pathlib import Path
from types import FunctionType, SimpleNamespace
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import powder_fire_runtime_v1307 as runtime
from scripts import battle_aftermath_runtime_v1253 as old_runtime
from scripts import verify_battle_aftermath_runtime_v1254 as previous
from scripts.audit_item_runtime_storage_v785 import census
from scripts.verify_escape_direct_runtime_v1184b import literal_accesses
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/powder_fire_runtime_v1308')
ROM = Path('out/all_routes_combined_v1266_candidate.nds')


def main():
    assert not ROOT.exists()
    assert sha(ROM.read_bytes()) == 'cac04b66961829b42b3d54bd69d901926434ff1ed24d1be0b2f96665020e8da5'
    rom = NdsImage.open(ROM)
    old = rom.read_file('/__arm9__.bin')
    target,plan = runtime.apply(old)
    prior = {p:(o,h,set(values)) for p,o,h,values in old_runtime.contract_rows()}
    added = {}
    for parent,offset,high,values in runtime.contract_rows():
        po,ph,pv = prior[parent]
        assert (offset,high) == (po,ph) and pv <= set(values)
        if pv != set(values):
            added[hex(parent)] = sorted(set(values)-pv)
    assert added == {'0x2053f40':[0x7980]}
    owned = read('work/analysis/escape_direct_runtime_v1184c/runtime_plan.json')['private_spans']
    assert all(any(lo <= a and b <= hi for lo,hi in owned) for a,b in plan['private_spans'])
    other = NdsImage.open(ROM)
    other.rom.arm9 = target
    refs = [census(r,plan['private_spans'],plan['private_spans']) for r in [rom,other]]
    external = lambda rows:sorted(row for row in rows if not row[-1])
    assert external(refs[0]) == external(refs[1])
    accesses = [literal_accesses(r,plan['private_spans']) for r in [rom,other]]
    outside = lambda rows:sorted(row for row in rows if not any(lo <= row[2] < hi for lo,hi in plan['private_spans']))
    assert outside(accesses[0]) == outside(accesses[1]) == []
    assert all(row[3] in [runtime.CONTRACTS,runtime.GATE,runtime.GATE|1] for row in external(refs[0]))
    ROOT.mkdir(parents=True)
    output = ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin'
    output.write_bytes(target)
    save(ROOT/'runtime_plan.json',{**plan,'research_ARM9':str(output),'new_memberships':added,
        'source_ROM_sha256':sha(ROM.read_bytes()),'source_owned_spans':owned,
        'source_target_absolute_branch_ADR_reference_census':refs,'source_target_PC_relative_load_store_census':accesses,
        'all_external_references_exact_no_internal_row_or_gate_tail_references':True,
        'runtime_module_sha256':sha(Path(runtime.__file__).read_bytes())})
    scope = inspect.getsource(previous.scope)
    old_assert = 'assert cpu.reg_read(UC_ARM_REG_R12) == bank.GATE|1'
    assert scope.count(old_assert) == 1
    scope = scope.replace(old_assert,'assert cpu.reg_read(UC_ARM_REG_R12) == ((bank.STATUS if route == bank.STATUS else bank.GATE)|1)')
    scope = scope.replace('source_and_target_only13_exact_new_memberships','source_and_target_only_one_exact_new_membership')
    env = {**previous.__dict__,'__file__':__file__,'ROOT':ROOT,'runtime':runtime,
        'bank':SimpleNamespace(**{**previous.bank.__dict__,'STATUS':0x021479D4})}
    exec(compile(scope,__file__,'exec'),env)
    env['scope'](target)
    for fn in [previous.historical.modal_equivalence,previous.historical.status]:
        bound = FunctionType(fn.__code__,{**fn.__globals__,'ROOT':ROOT},argdefs=fn.__defaults__)
        bound(old,target) if fn is previous.historical.modal_equivalence else bound(target)
    files = [ROOT/name for name in ['runtime_plan.json','scope_proof.json','modal_equivalence.json','status_contracts.json']]
    save(ROOT/'native_runtime_verification.json',{'source_ROM':str(ROM),'source_ROM_sha256':sha(ROM.read_bytes()),
        'source_ARM9_sha256':sha(old),'target_ARM9_sha256':sha(target),'proofs':{str(path):sha(path.read_bytes()) for path in files},
        'native_exact_dispatch_ABI_memory_and_external_reference_proven':True,
        'only_one_proven_direct_parent_table_membership_added':True,
        'all3668_modal238_parent5_edge_and140_whole_memory_status_regressions_pass':True,
        'no_section_BSS_cache_ITCM_arena_or123040_staged_growth':True,
        'font_native_source_pipelines_registered_release_and_revised_gameplay_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Single fire-table membership,exhaustive native dispatch/ABI and historical modal/status regressions pass.',flush=True)


if __name__ == '__main__':
    main()
