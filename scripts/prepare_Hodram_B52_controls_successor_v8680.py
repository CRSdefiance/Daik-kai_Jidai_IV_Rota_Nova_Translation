"""Keep rejected V1 context binding; explicitly qualify old source-only provenance."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B52_controls_tools_v8680')
    assert not root.exists()
    module = derive('dk4tool/patch/hodram_B52_controls_v1.py', 'dk4tool/patch/hodram_B52_controls_v2.py', {
        'from scripts.Hodram_B51_registered_route_context_v8612 import RouteCurrentContext': 'from scripts.Hodram_B51_registered_route_context_v8612 import RouteCurrentContext\nfrom dk4tool.patch.hodram_B52_context_qualification_v1 import qualify_source_context',
        "require(source['current_native_input_sha256'] == sha(INPUT.read_bytes()) and stored['relocation_sha256'] == sha(MAP.read_bytes()), 'own current context and original relocation identity')": "source_context=qualify_source_context(source,parent,INPUT,load,require)\n    require(stored['relocation_sha256']==sha(MAP.read_bytes()),'original relocation identity')",
        'original_current_native_context=context_binding,': 'original_current_native_context=context_binding, source_context_qualification=source_context,',
    })
    runner = derive('scripts/validate_Hodram_B52_controls_v8679.py', 'scripts/validate_Hodram_B52_controls_v8679b.py', {
        'hodram_B52_controls_v1': 'hodram_B52_controls_v2',
        'work/analysis/Hodram_B52_controls_production_v8679': 'work/analysis/Hodram_B52_controls_production_v8679b',
        'caller_image_unchanged_andzero_atomic_commits=True': 'historical_source_V8543_provenance_andunequal_whole_RAM_snapshots_explicit=True,caller_image_unchanged_andzero_atomic_commits=True',
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(module=module, runner=runner,
         original_failure='Original source controls8620 used registeredV8543 own context. Current stored/display usesV8609. Reject equating input descriptor hashes; preserve both separate cold-boot snapshots and explicitly compare complete consumer inputs and actors before fresh ownV8609 native controls.',
         original_V1_andstopped_runner_preserved=True, no_historical_overlay_orfrozen_guard_bypass=True))
