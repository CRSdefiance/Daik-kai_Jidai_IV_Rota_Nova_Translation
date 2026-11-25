"""Record exact current builder inverse and why the fixed late-story hook is ineligible."""
import ast
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v6 import validate_builder_bytes, STAGE_V6, STAGE_B49_V3, STAGE_B50
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_builder_inspection_v8594')
BUILDER = Path('scripts/build_integrated_release.py')
REGISTRY = Path('translations/release_stack.json')
LATE = Path('dk4tool/patch/late_story_editorial.py')

if __name__ == '__main__':
    assert not ROOT.exists()
    raw, late = BUILDER.read_bytes(), LATE.read_text('utf-8')
    text, tree = raw.decode('utf-8'), ast.parse(raw)
    original = Path('translations/hodram_outcomes_native_contract_v1.json')
    digest = read(original)['dependencies'][str(BUILDER.resolve())]
    proof = validate_builder_bytes(raw, digest)
    assert all(raw.count(stage.encode()) == 1 for stage in [STAGE_V6, STAGE_B49_V3, STAGE_B50])
    inverse = raw
    for stage in [STAGE_V6, STAGE_B49_V3, STAGE_B50]:
        inverse = inverse.replace(stage.encode(), b'', 1)
    assert sha(inverse) == digest
    accesses, dynamic = [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == 'profile_config' and node.func.attr == 'get':
            if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                accesses.append(dict(key=node.args[0].value, line=node.lineno))
            else:
                dynamic.append(dict(expression=ast.unparse(node), line=node.lineno))
    profile = read(REGISTRY)['profiles']['all-routes-unified-v8543']
    assert Path(profile['hodram_outcomes_editorial']).as_posix() == 'translations/hodram_outcomes_editorial_release_v6.json'
    assert Path(profile['hodram_B49_editorial']).as_posix() == 'translations/hodram_B49_editorial_release_v4.json'
    assert Path(profile['hodram_B50_editorial']).as_posix() == 'translations/hodram_B50_editorial_release_v1.json'
    boundary = text.index('    # Lexically valid "% o"')
    assert text.index(STAGE_V6) < text.index(STAGE_B49_V3) < text.index(STAGE_B50) < boundary
    late_get = next(a for a in accesses if a['key'] == 'late_story_editorial_release')
    b50_get = next(a for a in accesses if a['key'] == 'hodram_B50_editorial')
    assert late_get['line'] < b50_get['line'] and "header.get('encoder') != 'dialogue-fixed-v1'" in late
    assert 'len(after) != len(before)' in late and 'following_command_address_exact=True' in late
    assert not dynamic and not any(a['key'] == 'hodram_B51_editorial' for a in accesses)
    ROOT.mkdir(parents=True)
    (ROOT / 'current_builder.before.py').write_bytes(raw)
    (ROOT / 'original_guarded_builder_inverse.py').write_bytes(inverse)
    save(ROOT / 'builder_inspection.json', dict(builder=str(BUILDER), builder_sha256=sha(raw), registry=str(REGISTRY), registry_sha256=sha(REGISTRY.read_bytes()),
        profile='all-routes-unified-v8543', profile_value=profile, original_frozen_dependency_source=str(original),
        original_frozen_dependency_source_sha256=sha(original.read_bytes()), original_builder_sha256=digest, guarded_current_builder_inverse=proof,
        all_literal_profile_get_accesses=accesses, dynamic_profile_get_accesses=dynamic,
        existing_shared_late_story_hook=dict(key=late_get['key'], line=late_get['line'], module=str(LATE), module_sha256=sha(LATE.read_bytes()),
            supports_fixed_allocation_only=True, executes_before_required_complete_B50_stack=True,
            ineligible_reason='B51 is a relocatable400-byte block replacing340 bytes with eight mapped relative targets, and must follow the full V8543 stack. The existing hook requires dialogue-fixed-v1/equal allocations and runs before the later frozen route stages. Its contract is preserved.'),
        no_suitable_existing_registered_hook_for_this_relocatable_late_B51_contract=True,
        current_outcomesv6_B49v3_B50v1_order_andentire_original_builder_inverse_exact=True,
        new_additive_stage_compatible_predecessors_wholeV8543_equivalence_andchanged_builder_tests_required=True,
        no_builder_registry_ROM_orledger_mutation=True, new_credit=0, full_goal_complete=False, producer_sha256=sha(Path(__file__).read_bytes())))
    print('Inspected current builder: exact outcomesv6/B49v3/B50v1 order andwhole frozen original inverse pass. Existing late-story hook is fixed-allocation/too early for B51. No builder/registry/ROM change.')
