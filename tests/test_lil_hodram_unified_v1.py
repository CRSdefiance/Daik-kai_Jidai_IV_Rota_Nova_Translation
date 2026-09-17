import json
from pathlib import Path


STACK = Path("translations/release_stack.json")


def test_unified_profile_preserves_lil_guild_and_current_port_layers() -> None:
    profiles = json.loads(STACK.read_text(encoding="utf-8"))["profiles"]
    unified = profiles["lil-hodram-unified-v1"]["batches"]
    current = profiles["hodram-market-inn-sea-v2"]["batches"]
    lil = profiles["lil-b22-intro-all-items-v5"]["batches"]

    expected = (
        (set(current) - {"translations/innkeeper_nameplates_arm9_v1.json"})
        | (set(lil) - {"translations/common_crew_join_leading_guard_v2.json"})
    )

    assert len(unified) == len(set(unified))
    assert set(unified) == expected
    assert "translations/common_crew_join_wrap_v3.json" in unified
    assert "translations/guild_inn_ui_arm9_v2.json" in unified
    assert "translations/lil_sc2_b22_intro_natural_v2.json" in unified
    assert "translations/all_item_names_arm9_v1.json" in unified


def test_legacy_packed_guild_descriptions_document_their_guard_exception() -> None:
    batch = json.loads(
        Path("translations/guild_amsterdam_item_descriptions_v2.json").read_text(
            encoding="utf-8"
        )
    )
    assert batch["ascii_guard_exemption"]
