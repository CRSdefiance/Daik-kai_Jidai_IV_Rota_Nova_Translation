from __future__ import annotations

from pathlib import Path

from scripts.audit_raphael_route_completion import audit


def test_raphael_v93_completion_audit_proves_route_scope() -> None:
    report = audit(
        Path("out/raphael_deep_route_v93_candidate.nds"),
        Path("out/raphael_natural_v2_accepted_base.nds"),
        Path("out/raphael_deep_route_v93_manifest.json"),
        Path("out/qa_raphael_v93_release.json"),
        Path("out/raphael_deep_route_v93_interface_audit.json"),
    )
    assert report["status"] == "pass"
    assert report["blocking_issue_count"] == 0
    assert report["translated_record_count"] == 5801
    assert report["speaker_state_count"] == 154
    assert report["interface_profile_record_count"] == 852
    assert report["all_residuals_explicitly_excluded"] is True
    assert report["all_excluded_controls_unchanged"] is True
    assert report["all_translations_exact_allocation"] is True
    assert report["manifest_checks_pass"] is True
    assert report["layout_audit_pass"] is True
    assert report["interface_audit_pass"] is True
    assert report["residual_japanese_decode_count"] == 63
    assert all(record["excluded"] for record in report["residual_controls"])
