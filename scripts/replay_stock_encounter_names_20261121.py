"""Replay the source-bound Ghost Ship inspection on the staged candidate."""

from inspect import getsource

from scripts import replay_special_target_labels_20261115 as historical
from scripts import stage_stock_encounter_names_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    source = checked_text(getsource(historical.special_target), {
        "'EXPECTED_LABEL': '化魚'.encode('cp932') if model == 149 else b'Ghost',":
            "'EXPECTED_LABEL': b'Monster Fish' if model == 149 else b'Ghost Ship',",
    })
    settings = historical.__dict__ | {"ROOT": stage.ROOT, "__file__": __file__, "stage": stage}
    exec(compile(source, __file__ + "::preserved-fixture", "exec"), settings)
    source = checked_text(getsource(historical.replay), {
        "if candidate:\n        from scripts import stage_special_target_labels_20261115 as stage\n        data = base.load(stage.STORED)\n        assert rom == stage.ROM and base.digest(rom) == data['candidate_sha256']\n        assert data['previous_sha256'] == parent_receipt['candidate_sha256']\n        expected_arm = data['target_ARM9_sha256']\n    else:\n        expected_arm = parent_receipt['target_ARM9_sha256']":
            "assert candidate is not None\n    data = base.load(stage.PROOF)\n    assert rom == stage.ROM and base.digest(rom) == data['candidate_sha256']\n    expected_arm = data['target_ARM9_sha256']",
        "'--pause-at', '4800', '--dump-pause-ram', '--allow-condition-fixtures'":
            "'--pause-at', '4800', '--dump-pause-ram', '--dump-capture-ram', '--allow-condition-fixtures'",
    })
    exec(compile(source, __file__ + "::native-inspection", "exec"), settings)
    settings["replay"]("ghost", stage.ROM, settled=True)


if __name__ == "__main__":
    main()
