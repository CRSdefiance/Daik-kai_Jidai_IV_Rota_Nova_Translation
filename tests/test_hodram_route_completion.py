from __future__ import annotations

from pathlib import Path

from scripts.audit_hodram_route_completion import audit


def test_hodram_v32_completion_audit_proves_route_scope() -> None:
    report = audit(
        Path("out/hodram_deep_route_v32_candidate.nds"),
        Path("out/raphael_natural_v2_accepted_base.nds"),
        Path("out/hodram_deep_route_v32_candidate.manifest.json"),
        Path("out/hodram_deep_route_v32_layout_audit.json"),
        Path("out/hodram_deep_route_v32_interface_audit.json"),
    )
    assert report["status"] == "pass"
    assert report["blocking_issue_count"] == 0
    assert report["translated_record_count"] == 5004
    assert report["speaker_state_count"] == 152
    assert report["interface_profile_record_count"] == 852
    assert report["all_residuals_explicitly_excluded"] is True
    assert report["all_excluded_controls_unchanged"] is True
    assert report["all_translations_exact_allocation"] is True
    assert report["manifest_checks_pass"] is True
    assert report["layout_audit_pass"] is True
    assert report["interface_audit_pass"] is True
    assert report["residual_japanese_decode_count"] == 51
    assert all(record["excluded"] for record in report["residual_controls"])
    assert all(3 <= record["length"] <= 12 for record in report["residual_controls"])
