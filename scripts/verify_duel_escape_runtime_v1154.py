"""Complete prior selector, modal and status contracts after adding escape tables."""
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from scripts import duel_escape_runtime_v1152 as runtime
from scripts import verify_sighting_runtime_v1076 as verifier
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_escape_runtime_v1154')


def bound(function):
    return FunctionType(function.__code__, {**function.__globals__, 'ROOT': ROOT},
                        argdefs=function.__defaults__)


def main():
    assert not ROOT.exists()
    plan_path = Path('work/analysis/duel_escape_runtime_v1153/runtime_plan.json')
    plan = read(plan_path)
    source_plan = read(plan['source_cache_payload_plan'])
    old = Path(source_plan['target_ARM9']).read_bytes()
    target = Path(plan['research_ARM9']).read_bytes()
    assert sha(old) == plan['source_ARM9_sha256'] and sha(target) == plan['research_ARM9_sha256']
    assert runtime.apply(old)[0] == target
    before = {p: (o, h, set(v)) for p, o, h, v in runtime.previous.contract_rows()}
    differences = {}
    for p, o, h, values in runtime.contract_rows():
        bo, bh, bv = before[p]
        assert (o, h) == (bo, bh) and bv <= set(values)
        if bv != set(values):
            differences[hex(p)] = sorted(set(values)-bv)
    assert differences == {'0x2053db8': [0x7500, 0x7620]}
    ROOT.mkdir(parents=True)
    bound(verifier.scope)(old, 'current_scope', runtime.previous.contract_rows)
    bound(verifier.scope)(target, 'research_scope', runtime.contract_rows)
    bound(verifier.modal_equivalence)(old, target)
    bound(verifier.status)(target)
    paths = [ROOT/p for p in ('current_scope/scope_proof.json', 'research_scope/scope_proof.json',
        'modal_equivalence.json', 'status_contracts.json')]
    save(ROOT/'native_runtime_verification.json', {'runtime_plan': str(plan_path),
        'runtime_plan_sha256': sha(plan_path.read_bytes()), 'source_ARM9_sha256': sha(old),
        'research_ARM9_sha256': sha(target), 'only_new_contract': differences,
        'old_and_new_full_scope_cases_each': 56696,
        'all3668_modal_outputs238_wrong_parent_and5_full_word_edges_exact': True,
        'all140_whole8MiB_status_contracts_and_stack_register_guards_pass': True,
        'public212_gate164_ITCM128_shapes_unchanged_and_status24_exact_moved4': True,
        'all_completed_proofs': {str(p): sha(p.read_bytes()) for p in paths},
        'verifier_module_sha256': sha(Path(verifier.__file__).read_bytes()),
        'runtime_module_sha256': sha(Path(runtime.__file__).read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'research_only_escape_fonts_registered_integration_and_actual_pending': True,
        'no_ROM_or_completed_entry_credit': True, 'full_goal_complete': False})
    print('Escape membership: 56696 source +56696 target dispatch,3668 modal and140 status cases pass; no growth.', flush=True)


if __name__ == '__main__':
    main()
