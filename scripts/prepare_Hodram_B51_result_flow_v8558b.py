"""Correct only the fragment runner's end sentinel; retain the stopped producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_result_flow_tools_v8558b')
    assert not root.exists()
    result = derive('scripts/prove_Hodram_B51_result_flow_v8558.py', 'scripts/prove_Hodram_B51_result_flow_v8558b.py', {
        "Path('work/analysis/Hodram_B51_result_flow_v8558')": "Path('work/analysis/Hodram_B51_result_flow_v8558b')",
        'cpu.emu_start(BASE + 0x24074, stop + 4, count=100)': 'cpu.emu_start(BASE + 0x24074, 0, count=100)',
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(derivation=result,
        reason='The old end address equalled the entry PC, so Unicorn correctly executed no instructions. Use an unreachable end sentinel with the same original-PC hook and instruction bound. All native addresses, guards, test cases and expected results remain exact.',
        original_failure_preserved=True, no_ROM_orcredit_change=True))
