"""Keep the c serialization failure; hash native byte spans losslessly in d."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B170_repeat_verifier_tools_v4296d')

if __name__ == '__main__':
    assert not ROOT.exists()
    tool = derive('scripts/verify_lil_B170_repeat_v4296c.py', 'scripts/verify_lil_B170_repeat_v4296d.py', {
        'repeat_verification_v4296c': 'repeat_verification_v4296d',
        'def trace_pairs(trace, fixture):': "def native_json(value):\n    assert isinstance(value, bytes), type(value)\n    return {'native_byte_span_hex': value.hex()}\n\n\ndef trace_pairs(trace, fixture):",
        'json.dumps(value, sort_keys=True)': 'json.dumps(value, sort_keys=True, default=native_json)',
    })
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tool=tool,
        correction='The c reader completed native comparisons but its JSON hashing could not serialize the native byte spans returned by models. Encode those spans explicitly and losslessly; no state or timing requirement changes.',
        original_strict_gate_and_b_c_producers_preserved=True, new_emulator_runs=0, full_goal_complete=False))
