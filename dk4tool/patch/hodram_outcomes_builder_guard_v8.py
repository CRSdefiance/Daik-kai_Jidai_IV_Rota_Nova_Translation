"""Accept exact compatibility namespaces and one shared late hook; recover whole V7 builder."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v7 import BUILDER, STAGE_V7, STAGE_B49_V4, STAGE_B50_V2, STAGE_B51, validate_builder_bytes as previous_validate
from dk4tool.patch.late_editorial_extensions_v1 import BUILDER_STAGE
from scripts.source_locked_derivation_v5118 import checked_text

STAGE_V8 = checked_text('if True:\n' + STAGE_V7, {'hodram_outcomes_editorial_v7': 'hodram_outcomes_editorial_v8'}).split('\n', 1)[1]
STAGE_B49_V5 = checked_text('if True:\n' + STAGE_B49_V4, {'hodram_B49_editorial_v4': 'hodram_B49_editorial_v5'}).split('\n', 1)[1]
STAGE_B50_V3 = checked_text('if True:\n' + STAGE_B50_V2, {'hodram_B50_editorial_v2': 'hodram_B50_editorial_v3'}).split('\n', 1)[1]
STAGE_B51_V2 = checked_text('if True:\n' + STAGE_B51, {'hodram_B51_editorial_v1': 'hodram_B51_editorial_v2'}).split('\n', 1)[1]


def validate_builder_bytes(raw, digest):
    if not isinstance(raw, bytes):
        raise ValueError('Hodram builder guard: complete builder bytes required')
    current = [s.encode() for s in [STAGE_V8, STAGE_B49_V5, STAGE_B50_V3, STAGE_B51_V2]]
    old = [s.encode() for s in [STAGE_V7, STAGE_B49_V4, STAGE_B50_V2, STAGE_B51]]
    addition, boundary = BUILDER_STAGE.encode(), b'    # Lexically valid "% o"'
    present = any(s in raw for s in [*current, addition])
    normalized = raw
    if present:
        if any(raw.count(s) != 1 for s in current) or raw.count(addition) > 1 or any(s in raw for s in old):
            raise ValueError('Hodram builder guard: exact compatible V8/B49V5/B50V3/B51V2 chain once required')
        if raw.count(boundary) != 1 or not raw.index(current[0]) < raw.index(current[1]) < raw.index(current[2]) < raw.index(current[3]) < raw.index(boundary):
            raise ValueError('Hodram builder guard: complete predecessor order before final guards required')
        if addition in raw:
            if not raw.index(current[3]) + len(current[3]) <= raw.index(addition) < raw.index(boundary):
                raise ValueError('Hodram builder guard: shared late extension must follow complete B51 before final guards')
            normalized = normalized.replace(addition, b'', 1)
        for new, prior in zip(current, old, strict=True):
            normalized = normalized.replace(new, prior, 1)
    proof = previous_validate(normalized, digest)
    compile(raw, str(BUILDER), 'exec')
    return {**proof, 'compatible_v8_chain': present, 'shared_late_editorial_hook_present': addition in raw,
            'whole_original_builder_inverse_preserved': True}


def checked_dependency(path, digest):
    path = Path(path)
    if path.resolve() == BUILDER:
        validate_builder_bytes(path.read_bytes(), digest)
    elif sha(path.read_bytes()) != digest:
        raise ValueError('Native dependency changed:' + str(path))
    return True
