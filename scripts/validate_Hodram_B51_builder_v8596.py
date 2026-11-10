"""Test exact historical/compatible/additive forms and genuinely changed builders."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v7 import BUILDER, STAGE_V6, STAGE_B49_V3, STAGE_B50, STAGE_V7, STAGE_B49_V4, STAGE_B50_V2, STAGE_B51, validate_builder_bytes
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_builder_validation_v8596')
if __name__ == '__main__':
    assert not ROOT.exists()
    inspection = read('work/analysis/Hodram_B51_builder_inspection_v8594/builder_inspection.json')
    current = BUILDER.read_bytes()
    assert sha(current) == inspection['builder_sha256']
    digest = inspection['original_builder_sha256']
    original = Path('work/analysis/Hodram_B51_builder_inspection_v8594/original_guarded_builder_inverse.py').read_bytes()
    compatible = current.replace(STAGE_V6.encode(), STAGE_V7.encode(), 1).replace(STAGE_B49_V3.encode(), STAGE_B49_V4.encode(), 1).replace(STAGE_B50.encode(), STAGE_B50_V2.encode(), 1)
    planned = compatible.replace(STAGE_B50_V2.encode(), (STAGE_B50_V2 + STAGE_B51).encode(), 1)
    positives = []
    for label, raw in [('whole-original', original), ('historical-before-B50', current.replace(STAGE_B50.encode(), b'', 1)),
            ('current-V8543', current), ('compatible-without-B51', compatible), ('additive-B51', planned)]:
        proof = validate_builder_bytes(raw, digest)
        positives.append(dict(case=label, sha256=sha(raw), proof=proof))
    pre, p49, p50, add = STAGE_V7.encode(), STAGE_B49_V4.encode(), STAGE_B50_V2.encode(), STAGE_B51.encode()
    cases = [
        ('unowned-comment', planned + b'\n# unapproved mutation\n', digest),
        ('only-new-outcomes', current.replace(STAGE_V6.encode(), pre), digest),
        ('only-new-B49', current.replace(STAGE_B49_V3.encode(), p49), digest),
        ('only-new-B50', current.replace(STAGE_B50.encode(), p50), digest),
        ('B51-with-old-predecessors', current + add, digest),
        ('B51-missing-complete-B50', planned.replace(p50, b'', 1), digest),
        ('duplicate-outcomes', planned.replace(pre, pre + pre, 1), digest),
        ('duplicate-B49', planned.replace(p49, p49 + p49, 1), digest),
        ('duplicate-B50', planned.replace(p50, p50 + p50, 1), digest),
        ('duplicate-B51', planned.replace(add, add + add, 1), digest),
        ('mixed-outcomes-version', planned + STAGE_V6.encode(), digest),
        ('mixed-B49-version', planned + STAGE_B49_V3.encode(), digest),
        ('mixed-B50-version', planned + STAGE_B50.encode(), digest),
        ('B51-before-B50', compatible.replace(p50, add + p50, 1), digest),
        ('B51-before-B49', compatible.replace(p49, add + p49, 1), digest),
        ('B51-before-outcomes', compatible.replace(pre, add + pre, 1), digest),
        ('B51-after-percent-safety', compatible + add, digest),
        ('wrong-B51-module', planned.replace(b'hodram_B51_editorial_v1', b'hodram_B51_editorial_v999'), digest),
        ('wrong-B50-alias', planned.replace(b'hodram_B50_editorial_v2', b'hodram_B50_editorial_v999'), digest),
        ('wrong-B49-alias', planned.replace(b'hodram_B49_editorial_v4', b'hodram_B49_editorial_v999'), digest),
        ('wrong-outcomes-alias', planned.replace(b'hodram_outcomes_editorial_v7', b'hodram_outcomes_editorial_v999'), digest),
        ('wrong-B51-input', planned.replace(b'apply_hodram_B51_editorial(candidate, baseline', b'apply_hodram_B51_editorial(baseline, candidate'), digest),
        ('wrong-B51-profile-key', planned.replace(b"get('hodram_B51_editorial')", b"get('unowned_B51_editorial')"), digest),
        ('missing-percent-boundary', planned.replace(b'    # Lexically valid "% o"', b'    # Altered safety boundary'), digest),
        ('wrong-original-hash', planned, '0' * 64),
    ]
    assert len(cases) == 25
    negatives = []
    for label, raw, wanted in cases:
        assert raw != planned or wanted != digest
        try:
            validate_builder_bytes(raw, wanted)
        except ValueError as error:
            negatives.append(dict(case=label, actual_changed_input=True, sha256=sha(raw), requested_original_digest=wanted, rejected=True, error=str(error)))
        else:
            raise AssertionError('Changed builder accepted: ' + label)
    ROOT.mkdir(parents=True)
    for name, raw in [('current_builder.bin', current), ('compatible_builder.bin', compatible), ('planned_builder.bin', planned)]:
        (ROOT / name).write_bytes(raw)
    assert BUILDER.read_bytes() == current
    save(ROOT / 'exact_builder_inverse_cases.json', dict(positives=positives, negative_cases=negatives, negative_count=len(negatives),
        full_original_source_inverse_sha256=digest, current_builder_sha256=sha(current), planned_builder_sha256=sha(planned),
        all_owned_stages_once_original_order_before_final_percent_safety=True, all_unowned_original_builder_bytes_invert_exactly=True,
        no_live_builder_registry_ROM_orcredit_change=True, new_credit=0, full_goal_complete=False, producer_sha256=sha(Path(__file__).read_bytes())))
    print('Builderv7:five exact historical/compatible/additive forms andtwenty-five real changed builders tested;whole original inverse exact. No live builder edit.')
