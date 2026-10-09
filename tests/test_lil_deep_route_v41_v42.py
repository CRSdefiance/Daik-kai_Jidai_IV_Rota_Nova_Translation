from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments


def test_lil_b127_b132_exact_changes_states_choices_and_macros() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    all_rows = []
    choices = {}
    seen_states = set()
    seen_macros = set()
    for version, blocks in ((41, {127: 38}), (42, {128: 53}), (43, {129: 26}), (44, {130: 7, 131: 13, 132: 8})):
        count = sum(blocks.values())
        batch = json.loads(Path(f"translations/lil_deep_route_v{version}.json").read_text(encoding="utf-8"))
        assert batch["inventory"]["translated_records"] == count
        assert batch["inventory"]["blocks"] == {str(block): amount for block, amount in blocks.items()}
        if version == 44:
            assert batch["inventory"]["identified_records"] == count + 1
            assert set(batch["excluded_records"]) == {"DK4_MES_B131_R0080"}
        else:
            assert batch["inventory"]["identified_records"] == count
        assert batch["translation_policy"] == "natural-dialogue-v2"
        profile = get_dialogue_profile(batch["dialogue_profile"])
        assert profile.guard_linebreaks and profile.pair_phase_safe_breaks
        assert {0x1D, 0x5C, 0x5F, 0x97} <= profile.leading_speaker_bytes
        rows = materialize_translation_batch(batch, source)
        assert len(rows) == count
        for row in rows:
            raw = bytes.fromhex(row["source_hex"])
            english = row["english"]
            number = int(row["id"].rsplit("R", 1)[1])
            issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
            assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
            encoded = encode_fixed_dialogue(raw, english, profile).encoded
            if version == 42 and number in {214, 216}:
                assert raw[0] in {0x82, 0x83}
                assert not english.startswith("{SPEAKER:")
                assert encoded[0] == ord(english[0])
                choices[number] = chr(encoded[0])
            else:
                assert english.startswith(f"{{SPEAKER:{raw[0]:02X}}}")
                assert encoded[0] == raw[0]
                assert encoded[1] not in {10, 32}
                seen_states.add(raw[0])
            for macro in (b"FI", b"FO"):
                assert raw.count(macro) == encoded.count(macro)
                if macro in raw:
                    seen_macros.add(macro)
        all_rows.extend(rows)
    assert choices == {214: "S", 216: "D"}
    assert {0x09, 0x14, 0x1D, 0x5C, 0x5F, 0x97} <= seen_states
    assert seen_macros == {b"FI", b"FO"}
    expected = {
        (int(row["id"].split("_B")[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in all_rows
    }
    assert len(expected) == 145
    assert (131, 80) not in expected
    assert changed_segments(source, rebuild_mesfile(source, all_rows)) == expected


def test_lil_v123_and_unified_v89_extend_registered_stacks() -> None:
    profiles = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))["profiles"]
    for version in range(41, 124):
        batch = f"translations/lil_deep_route_v{version}.json"
        lil = profiles[f"lil-deep-route-v{version}"]["batches"]
        unified = profiles[f"all-routes-unified-v{version - 34}"]["batches"]
        assert lil[:-1] == profiles[f"lil-deep-route-v{version - 1}"]["batches"]
        assert unified[:-1] == profiles[f"all-routes-unified-v{version - 35}"]["batches"]
        assert lil[-1] == unified[-1] == batch
        assert len(lil) == version + 10
        assert len(unified) == version + 267


def test_lil_final_scenes_heads_macro_and_opening_controls() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v123.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 77
    assert set(batch["excluded_records"]) == {f"DK4_MES_B22_R{n:04d}" for n in (77, 88, 124)}
    expected = set()
    bare = set()
    macros = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        assert raw.count(b"FA") == encoded.count(b"FA")
        macros += raw.count(b"FA")
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert {f"DK4_MES_B333_R{n:04d}" for n in (17, 19, 21, 23, 25)} == bare
    assert macros == 1
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b325_b329_sea_crossing_tomato_macros_and_events() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v122.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 54
    assert set(batch["excluded_records"]) == {f"DK4_MES_B325_R{n:04d}" for n in (23, 69, 79)}
    expected = set()
    macros = {macro: 0 for macro in (b"FI", b"FA")}
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
        assert len(encoded) == len(raw)
        for macro in macros:
            assert raw.count(macro) == encoded.count(macro)
            macros[macro] += raw.count(macro)
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert set(macros.values()) == {1}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b324_jungle_choices_companion_states_and_events() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v121.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 59
    assert set(batch["excluded_records"]) == {f"DK4_MES_B324_R{n:04d}" for n in (37, 143, 217)}
    expected = set()
    bare = set()
    states = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
            states.add(raw[0])
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        assert not any(m in encoded for m in (b"FI", b"FA", b"FO"))
        expected.add((324, int(row["id"].rsplit("R", 1)[1])))
    assert {f"DK4_MES_B324_R{n:04d}" for n in (99, 101, 159, 196, 229)} <= bare
    assert {0x16, 0xCF, 0xD6} <= states
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b323_fog_choices_bare_variants_and_packed_events() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v120.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 66
    assert set(batch["excluded_records"]) == {f"DK4_MES_B323_R{n:04d}" for n in (38, 66, 106, 179)}
    expected = set()
    bare = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        assert not any(m in encoded for m in (b"FI", b"FA", b"FO"))
        expected.add((323, int(row["id"].rsplit("R", 1)[1])))
    assert {f"DK4_MES_B323_R{n:04d}" for n in (21, 95, 97, 135, 137, 204)} <= bare
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b317_b319_bare_heads_states_and_trade_macros() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v119.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 35 and not batch["excluded_records"]
    expected = set()
    bare = set()
    states = set()
    macros = {macro: 0 for macro in (b"FI", b"FO")}
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
            states.add(raw[0])
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        for macro in macros:
            assert raw.count(macro) == encoded.count(macro)
            macros[macro] += raw.count(macro)
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert bare == {"DK4_MES_B317_R0031", "DK4_MES_B317_R0044"}
    assert states == {0x02, 0x68, 0xCC} and set(macros.values()) == {1}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b316_scorpion_choices_states_and_treatment_macro() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v118.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 94 and not batch["excluded_records"]
    expected = set()
    bare = set()
    macros = 0
    encoded_rows = {}
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        encoded_rows[row["id"]] = encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        assert raw.count(b"FI") == encoded.count(b"FI")
        macros += raw.count(b"FI")
        expected.add((316, int(row["id"].rsplit("R", 1)[1])))
    assert {f"DK4_MES_B316_R{n:04d}" for n in (104, 106, 108, 282)} <= bare
    assert not {f"DK4_MES_B316_R{n:04d}" for n in (69, 97, 334, 358, 410)} & bare
    assert encoded_rows["DK4_MES_B316_R0166"] == encoded_rows["DK4_MES_B316_R0268"]
    assert macros == 1
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b314_b315_forest_choices_states_and_map_macro() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v117.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 38
    assert set(batch["excluded_records"]) == {"DK4_MES_B314_R0036", "DK4_MES_B314_R0063"}
    expected = set()
    bare = set()
    macros = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        assert raw.count(b"FI") == encoded.count(b"FI")
        macros += raw.count(b"FI")
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert {f"DK4_MES_B314_R{n:04d}" for n in (49, 57, 61, 75, 77)} <= bare
    assert not {f"DK4_MES_B314_R{n:04d}" for n in (109, 113)} & bare
    assert macros == 1 and not {(314, 36), (314, 63)} & expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b312_b313_wolf_choices_injuries_and_macros() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v116.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 84
    assert set(batch["excluded_records"]) == {"DK4_MES_B312_R0038", "DK4_MES_B312_R0316"}
    expected = set()
    bare = set()
    macros = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        assert raw.count(b"FI") == encoded.count(b"FI")
        macros += raw.count(b"FI")
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert {f"DK4_MES_B312_R{n:04d}" for n in (105, 107, 109)} <= bare
    assert not {f"DK4_MES_B312_R{n:04d}" for n in (89, 98, 196, 217, 242, 260)} & bare
    assert macros == 2
    assert not {(312, 38), (312, 316)} & expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b307_b311_temple_and_bare_97ac_river_variant() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v115.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 44 and not batch["excluded_records"]
    expected = set()
    bare = set()
    macros = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        assert raw.count(b"FI") == encoded.count(b"FI")
        macros += raw.count(b"FI")
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert "DK4_MES_B306_R0081" in bare and macros == 1
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b306_river_choices_and_state_97() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v114.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 39
    assert set(batch["excluded_records"]) == {"DK4_MES_B306_R0028", "DK4_MES_B306_R0063"}
    expected = set()
    bare = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        expected.add((306, int(row["id"].rsplit("R", 1)[1])))
    assert {"DK4_MES_B306_R0095", "DK4_MES_B306_R0097"} <= bare
    assert "DK4_MES_B306_R0159" not in bare
    assert not {(306, 28), (306, 63), (306, 81)} & expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b301_b305_desert_choices_guild_heads_and_macros() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v113.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 85 and not batch["excluded_records"]
    expected = set()
    bare = set()
    macros = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        assert raw.count(b"FI") == encoded.count(b"FI")
        macros += raw.count(b"FI")
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert {"DK4_MES_B301_R0118", "DK4_MES_B301_R0120"} <= bare
    assert not {f"DK4_MES_B301_R{n:04d}" for n in (78, 109, 128, 136, 145)} & bare
    assert macros == 1
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b299_b300_snake_bog_states_choices_and_macros() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v112.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 103
    assert set(batch["excluded_records"]) == {"DK4_MES_B299_R0038"}
    expected = set()
    bare = set()
    macros = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        assert raw.count(b"FI") == encoded.count(b"FI")
        macros += raw.count(b"FI")
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert {"DK4_MES_B299_R0101", "DK4_MES_B299_R0103"} <= bare
    assert not {f"DK4_MES_B299_R{n:04d}" for n in (57, 114, 175)} & bare
    assert macros == 7 and (299, 38) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b133_b135_exact_changes_and_leading_glyphs() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    all_rows = []
    for version, blocks in ((45, {133: 47}), (46, {134: 27, 135: 27})):
        batch = json.loads(Path(f"translations/lil_deep_route_v{version}.json").read_text(encoding="utf-8"))
        assert batch["inventory"]["translated_records"] == sum(blocks.values())
        assert batch["inventory"]["blocks"] == {str(block): amount for block, amount in blocks.items()}
        profile = get_dialogue_profile(batch["dialogue_profile"])
        rows = materialize_translation_batch(batch, source)
        assert len(rows) == sum(blocks.values())
        for row in rows:
            raw = bytes.fromhex(row["source_hex"])
            english = row["english"]
            issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
            assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
            encoded = encode_fixed_dialogue(raw, english, profile).encoded
            bare_text = not english.startswith("{SPEAKER:")
            if bare_text:
                if english.startswith("{MACRO:FO}"):
                    assert encoded.startswith(b"FO"), row["id"]
                else:
                    assert encoded[0] == ord(english[0]), row["id"]
            else:
                assert encoded[0] == raw[0]
                assert encoded[1] not in {10, 32}, row["id"]
            for macro in (b"FI", b"FO"):
                assert raw.count(macro) == encoded.count(macro), row["id"]
        all_rows.extend(rows)
    expected = {
        (int(row["id"].split("_B")[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in all_rows
    }
    assert len(expected) == 101
    assert changed_segments(source, rebuild_mesfile(source, all_rows)) == expected


def test_lil_b140_b143_polder_and_shipyard_exact_changes_and_leading_glyphs() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    all_rows = []
    seen_macros = set()
    for version, blocks in (
        (51, {140: 49}),
        (52, {141: 14, 142: 13}),
        (53, {143: 9}),
    ):
        batch = json.loads(Path(f"translations/lil_deep_route_v{version}.json").read_text(encoding="utf-8"))
        count = sum(blocks.values())
        assert batch["inventory"] == {
            "identified_records": count,
            "translated_records": count,
            "blocks": {str(block): amount for block, amount in blocks.items()},
        }
        assert batch["translation_policy"] == "natural-dialogue-v2"
        profile = get_dialogue_profile(batch["dialogue_profile"])
        assert profile.guard_linebreaks and profile.pair_phase_safe_breaks
        rows = materialize_translation_batch(batch, source)
        assert len(rows) == count
        for row in rows:
            raw = bytes.fromhex(row["source_hex"])
            english = row["english"]
            assert "I" not in english.replace("{MACRO:FI}", "")
            assert "F" not in english.replace("{MACRO:FI}", "")
            issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
            assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
            encoded = encode_fixed_dialogue(raw, english, profile).encoded
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
            for macro in (b"FI", b"FO"):
                assert raw.count(macro) == encoded.count(macro), row["id"]
                if macro in raw:
                    seen_macros.add(macro)
        all_rows.extend(rows)
    expected = {
        (int(row["id"].split("_B")[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in all_rows
    }
    assert len(expected) == 85
    assert seen_macros == {b"FI"}
    assert changed_segments(source, rebuild_mesfile(source, all_rows)) == expected


def test_lil_b144_b145_armor_unlock_map_and_control_exclusion() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v54.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 17,
        "translated_records": 16,
        "blocks": {"144": 10, "145": 6},
    }
    assert set(batch["excluded_records"]) == {"DK4_MES_B145_R0021"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 16
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
    expected = {
        (int(row["id"].split("_B")[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 16 and (145, 21) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b146_kamil_hodram_leads_macros_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v55.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 35, "translated_records": 35, "blocks": {"146": 35}}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert {0x01, 0x02, 0x09, 0x14, 0x97, 0xFE} <= profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 35
    seen_leads = set()
    seen_macros = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        seen_leads.add(raw[0])
        seen_macros += raw.count(b"FI")
    assert seen_leads == {0x01, 0x02, 0x09, 0x14, 0x97, 0xFE}
    assert seen_macros == 2
    expected = {(146, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 35
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b147_maria_reveal_controls_macros_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v56.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 69, "translated_records": 68, "blocks": {"147": 68}}
    assert set(batch["excluded_records"]) == {"DK4_MES_B147_R0129"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 68
    authored = {record["id"]: record for record in batch["records"]}
    source_breaks = set()
    retained_breaks = set()
    fi_count = fa_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1] if english.startswith("{SPEAKER:") else english
        prose = prose.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        waivers = set(authored[row["id"]].get("qa_waivers", []))
        assert not [
            issue for issue in issues
            if issue["severity"] in {"error", "warning"} and issue["code"] not in waivers
        ], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        if raw[0] == 0x0A:
            source_breaks.add(row["id"])
            if row["id"].endswith("R0021"):
                assert english.startswith("Admiral,")
                assert encoded[0] == ord("A")
            else:
                assert english.startswith("{LB}")
                assert encoded.startswith(b" \n ")
                assert encoded[3] not in {10, 32}
                assert {"manual-break", "source-leading-linebreak"} <= waivers
                retained_breaks.add(row["id"])
        else:
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        assert raw.count(b"FA") == encoded.count(b"FA"), row["id"]
        fi_count += raw.count(b"FI")
        fa_count += raw.count(b"FA")
    assert len(source_breaks) == 6 and len(retained_breaks) == 5
    assert (fi_count, fa_count) == (3, 2)
    expected = {(147, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 68 and (147, 129) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b148_b149_identity_and_bamboo_branches_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v57.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 45, "translated_records": 45, "blocks": {"148": 24, "149": 21}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 45
    seen_leads = set()
    fi_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        seen_leads.add(raw[0])
        fi_count += raw.count(b"FI")
    assert seen_leads == {0x02, 0x09, 0x0E, 0x14, 0x5C}
    assert fi_count == 1
    expected = {
        (int(row["id"].split("_B")[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 45
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b150_clifford_strategy_speakers_macro_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v58.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 22, "translated_records": 22, "blocks": {"150": 22}}
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 22
    seen_leads = set()
    fo_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FO}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FO") == encoded.count(b"FO"), row["id"]
        seen_leads.add(raw[0])
        fo_count += raw.count(b"FO")
    assert seen_leads == {0x02, 0x09, 0x10, 0x12, 0x14, 0x1C}
    assert fo_count == 1
    expected = {(150, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 22
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b151_maldonado_tavern_branches_macros_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v59.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 55, "translated_records": 55, "blocks": {"151": 55}}
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert 0x2A in profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 55
    seen_leads = set()
    macros = {b"FI": 0, b"FA": 0, b"FO": 0}
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        for macro in ("FI", "FA", "FO"):
            prose = prose.replace(f"{{MACRO:{macro}}}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        for macro in macros:
            assert raw.count(macro) == encoded.count(macro), row["id"]
            macros[macro] += raw.count(macro)
        seen_leads.add(raw[0])
    assert seen_leads == {0x02, 0x09, 0x0B, 0x0C, 0x0E, 0x10, 0x11, 0x14,
                          0x15, 0x16, 0x1B, 0x2A, 0x5C, 0xFE}
    assert macros == {b"FI": 2, b"FA": 1, b"FO": 2}
    expected = {(151, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 55
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b152_b153_coin_map_macro_control_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v60.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 16, "translated_records": 15, "blocks": {"152": 6, "153": 9}
    }
    assert set(batch["excluded_records"]) == {"DK4_MES_B153_R0024"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 15
    seen_leads = set()
    fi_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        seen_leads.add(raw[0])
        fi_count += raw.count(b"FI")
    assert seen_leads == {0x02, 0x09, 0x5C}
    assert fi_count == 1
    expected = {
        (int(row["id"].split("_B")[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 15 and (153, 24) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b154_al_recruitment_exact_changes_and_leading_glyphs() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v61.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 41, "translated_records": 40, "blocks": {"154": 40}
    }
    assert set(batch["excluded_records"]) == {"DK4_MES_B154_R0003"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert {0x73, 0x94} <= profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 40
    leads = set()
    macros = {b"FI": 0, b"FA": 0}
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "").replace("{MACRO:FA}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        for macro in macros:
            assert raw.count(macro) == encoded.count(macro), row["id"]
            macros[macro] += raw.count(macro)
        leads.add(raw[0])
    assert leads == {0x02, 0x09, 0x0E, 0x11, 0x14, 0x73, 0x94}
    assert macros == {b"FI": 2, b"FA": 1}
    expected = {(154, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 40 and (154, 3) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b155_angelo_recruitment_trade_and_event_exclusion() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v62.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 49, "translated_records": 48, "blocks": {"155": 48}
    }
    assert set(batch["excluded_records"]) == {"DK4_MES_B155_R0059"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 48
    leads = set()
    macros = {b"FI": 0, b"FA": 0}
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "").replace("{MACRO:FA}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        for macro in macros:
            assert raw.count(macro) == encoded.count(macro), row["id"]
            macros[macro] += raw.count(macro)
        leads.add(raw[0])
    assert leads == {0x02, 0x06, 0x09, 0x0F, 0x14}
    assert macros == {b"FI": 5, b"FA": 1}
    expected = {(155, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 48 and (155, 59) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b156_ian_recruitment_patron_states_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v63.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 69, "translated_records": 69, "blocks": {"156": 69}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert {0xA4, 0xA5} <= profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 69
    leads = set()
    fi_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        fi_count += raw.count(b"FI")
        leads.add(raw[0])
    assert leads == {0x02, 0x09, 0x0E, 0x14, 0x15, 0x5C, 0x60, 0xA4, 0xA5}
    assert fi_count == 2
    expected = {(156, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 69
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b157_carlo_recruitment_merchant_wife_and_narration() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v64.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 70, "translated_records": 70, "blocks": {"157": 70}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert {0x69, 0x8E} <= profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 70
    leads = set()
    fi_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        fi_count += raw.count(b"FI")
        leads.add(raw[0])
    assert leads == {0x02, 0x09, 0x0E, 0x13, 0x14, 0x69, 0x8E, 0xFE}
    assert fi_count == 2
    expected = {(157, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 70
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b158_christina_dance_audience_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v65.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 19, "translated_records": 19, "blocks": {"158": 19}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 19
    leads = set()
    fi_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        fi_count += raw.count(b"FI")
        leads.add(raw[0])
    assert leads == {0x02, 0x07, 0x09, 0x0E, 0xFE}
    assert fi_count == 1
    expected = {(158, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 19
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b159_samwell_cooking_macros_and_market_event() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v66.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 42, "translated_records": 41, "blocks": {"159": 41}
    }
    assert set(batch["excluded_records"]) == {"DK4_MES_B159_R0045"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 41
    leads = set()
    fi_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        fi_count += raw.count(b"FI")
        leads.add(raw[0])
    assert leads == {0x02, 0x09, 0x0E, 0x14, 0x16}
    assert fi_count == 4
    expected = {(159, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 41 and (159, 45) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b160_b162_stolen_ship_leads_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v67.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 23,
        "translated_records": 23,
        "blocks": {"160": 21, "161": 1, "162": 1},
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 23
    leads = set()
    fi_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        fi_count += raw.count(b"FI")
        leads.add(raw[0])
    assert leads == {0x02, 0x09, 0x0E, 0x0F, 0x74, 0x97}
    assert fi_count == 1
    expected = {
        (int(row["id"].split("_B")[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 23
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b163_ship_return_jam_recruitment_and_event_exclusion() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v68.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 44, "translated_records": 43, "blocks": {"163": 43}
    }
    assert set(batch["excluded_records"]) == {"DK4_MES_B163_R0034"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 43
    leads = set()
    fi_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        fi_count += raw.count(b"FI")
        leads.add(raw[0])
    assert leads == {0x02, 0x09, 0x0B, 0x0F, 0x14, 0x74}
    assert fi_count == 1
    expected = {(163, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 43 and (163, 34) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b168_mikhail_recruitment_names_and_item_tutorial() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v69.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 52, "translated_records": 52, "blocks": {"168": 52}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 52
    leads = set()
    macro_counts = {macro: 0 for macro in (b"FI", b"FA", b"FO")}
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        for macro in ("FI", "FA", "FO"):
            prose = prose.replace(f"{{MACRO:{macro}}}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        for macro in macro_counts:
            assert raw.count(macro) == encoded.count(macro), row["id"]
            macro_counts[macro] += raw.count(macro)
        leads.add(raw[0])
    assert leads == {0x02, 0x06, 0x09, 0x14, 0x4C, 0x57, 0xA5, 0xA6, 0xFE}
    assert macro_counts == {b"FI": 7, b"FA": 1, b"FO": 1}
    expected = {(168, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 52
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b169_proof_explanation_macros_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v70.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 36, "translated_records": 36, "blocks": {"169": 36}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 36
    leads = set()
    macro_counts = {macro: 0 for macro in (b"FI", b"FO")}
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        for macro in ("FI", "FO"):
            prose = prose.replace(f"{{MACRO:{macro}}}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        for macro in macro_counts:
            assert raw.count(macro) == encoded.count(macro), row["id"]
            macro_counts[macro] += raw.count(macro)
        leads.add(raw[0])
    assert leads == {0x02, 0x06, 0x09, 0x14, 0x15, 0x4C}
    assert macro_counts == {b"FI": 5, b"FO": 2}
    expected = {(169, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 36
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b170_yifa_recruitment_macros_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v71.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 33, "translated_records": 33, "blocks": {"170": 33}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 33
    leads = set()
    macro_counts = {macro: 0 for macro in (b"FI", b"FO")}
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        for macro in ("FI", "FO"):
            prose = prose.replace(f"{{MACRO:{macro}}}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        for macro in macro_counts:
            assert raw.count(macro) == encoded.count(macro), row["id"]
            macro_counts[macro] += raw.count(macro)
        leads.add(raw[0])
    assert leads == {0x02, 0x19}
    assert macro_counts == {b"FI": 1, b"FO": 1}
    expected = {(170, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 33
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b171_sanghyeon_dream_lead_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v72.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 35, "translated_records": 35, "blocks": {"171": 35}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 35
    leads = set()
    fi_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        fi_count += raw.count(b"FI")
        leads.add(raw[0])
    assert leads == {0x02, 0x19, 0x51}
    assert fi_count == 1
    expected = {(171, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 35
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b172_golden_crown_lead_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v73.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 27, "translated_records": 27, "blocks": {"172": 27}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 27
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x02, 0x1A, 0xC9}
    expected = {(172, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 27
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b173_b174_golden_crown_julian_recruitment_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v74.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 44, "translated_records": 44, "blocks": {"173": 11, "174": 33}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 44
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x02, 0x0E, 0x1A, 0xC9, 0xCA}
    expected = {
        (int(row["id"].split("_B")[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 44
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b175_aziza_confrontation_macros_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v75.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 33, "translated_records": 32, "blocks": {"175": 32}
    }
    assert set(batch["excluded_records"]) == {"DK4_MES_B175_R0012"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 32
    leads = set()
    fi_count = fa_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "").replace("{MACRO:FA}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        assert raw.count(b"FA") == encoded.count(b"FA"), row["id"]
        fi_count += raw.count(b"FI")
        fa_count += raw.count(b"FA")
        leads.add(raw[0])
    assert leads == {0x02, 0x09, 0xFE, 0xB7, 0xB8, 0xB9}
    assert (fi_count, fa_count) == (4, 1)
    expected = {(175, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 32 and (175, 12) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b176_seville_banana_boom_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v76.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 10, "translated_records": 10, "blocks": {"176": 10}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 10
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0xAE, 0xAF, 0xFE}
    expected = {(176, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 10
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b177_genoa_tomato_boom_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v77.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 10, "translated_records": 10, "blocks": {"177": 10}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 10
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0xAE, 0xAF, 0xFE}
    expected = {(177, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 10
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b178_amsterdam_wheat_boom_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v78.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 13, "translated_records": 13, "blocks": {"178": 13}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 13
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0xA6, 0xA7, 0xA8, 0xFE}
    expected = {(178, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 13
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b179_san_jorge_wine_boom_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v79.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 8, "translated_records": 8, "blocks": {"179": 8}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 8
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x60, 0x5C, 0xFE}
    expected = {(179, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 8
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b180_b182_market_rumors_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v80.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 29, "translated_records": 29,
        "blocks": {"180": 11, "181": 10, "182": 8}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 29
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0xA6, 0xA7, 0xA8, 0xFE}
    expected = {
        (int(row["id"].split("_B")[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 29
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b183_basra_painting_craze_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v81.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 25, "translated_records": 25, "blocks": {"183": 25}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 25
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x55, 0x6E, 0x84, 0x94, 0x99, 0xFE}
    expected = {(183, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 25
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b184_b186_market_rumors_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v82.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 29, "translated_records": 29,
        "blocks": {"184": 9, "185": 8, "186": 12}
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 29
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0xA4, 0xA5, 0xAE, 0xAF, 0xFE}
    expected = {
        (int(row["id"].split("_B")[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 29
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b187_malacca_almond_rumor_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v83.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 16, "translated_records": 16, "blocks": {"187": 16}}
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 16
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x57, 0x9B, 0xFE}
    expected = {(187, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b188_osaka_glass_rumor_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v84.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 11, "translated_records": 11, "blocks": {"188": 11}}
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert 0x82 not in profile.leading_speaker_bytes and 0x96 not in profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 11
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1] if english.startswith("{SPEAKER:") else english
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        if raw[0] == 0xFE:
            assert encoded[0] == 0xFE and encoded[1] not in {10, 32}
        else:
            assert raw[0] in {0x82, 0x96}
            assert encoded[0] != raw[0]
        leads.add(raw[0])
    assert leads == {0x82, 0x96, 0xFE}
    expected = {(188, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b189_hamburg_ceramics_rumor_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v85.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 17, "translated_records": 17, "blocks": {"189": 17}}
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 17
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x52, 0x68, 0x71, 0x93, 0xFE}
    expected = {(189, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b190_havana_medicine_rumor_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v86.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 17, "translated_records": 17, "blocks": {"190": 17}}
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 17
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x77, 0x9F, 0xFE}
    expected = {(190, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b191_calicut_dye_rumor_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v87.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 13, "translated_records": 13, "blocks": {"191": 13}}
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 13
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x56, 0x9A, 0xFE}
    expected = {(191, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b192_b194_market_rumors_exact_changes_and_fi_macro() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v88.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 33, "translated_records": 33,
        "blocks": {"192": 8, "193": 14, "194": 11},
    }
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 33
    leads = set()
    fi_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        if row["id"] == "DK4_MES_B192_R0030":
            assert "Constantinople" in prose and "Ｉ" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        fi_count += raw.count(b"FI")
        leads.add(raw[0])
    assert fi_count == 1
    assert leads == {0x06, 0x73, 0x75, 0x99, 0x9C, 0xA6, 0xA7, 0xA8, 0xFE}
    expected = {
        (int(row["id"].split("_B")[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b195_veracruz_cheese_scene_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v89.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 20, "translated_records": 20, "blocks": {"195": 20}}
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 20
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x5C, 0x67, 0x77, 0xFE}
    expected = {(195, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b196_haggling_choices_and_fi_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v90.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 35, "translated_records": 35, "blocks": {"196": 35}}
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert 0x94 not in profile.leading_speaker_bytes and 0xAD in profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 35
    choices = {32, 34, 82, 84, 126, 128, 187, 189, 232, 234, 277, 279}
    found_choices = set()
    fi_count = 0
    leads = set()
    for row in rows:
        number = int(row["id"].rsplit("R", 1)[1])
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1] if english.startswith("{SPEAKER:") else english
        prose = prose.replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        fi_count += raw.count(b"FI")
        if number in choices:
            found_choices.add(number)
            assert raw[0] == 0x94 and encoded[0] in {ord("B"), ord("P")}, row["id"]
            assert english in {"Buy{PAD}", "Pass{PAD}"}
        else:
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert found_choices == choices and fi_count == 1
    assert leads == {0x06, 0x13, 0x14, 0x19, 0x94, 0xAD, 0xFE}
    expected = {(196, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b197_celestial_maiden_choices_and_payload() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v91.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 25, "translated_records": 24, "blocks": {"197": 24}}
    assert set(batch["excluded_records"]) == {"DK4_MES_B197_R0022"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert 0x94 not in profile.leading_speaker_bytes and 0xA9 in profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 24
    choices = {31, 33, 35}
    found_choices = set()
    leads = set()
    for row in rows:
        number = int(row["id"].rsplit("R", 1)[1])
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1] if english.startswith("{SPEAKER:") else english
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        if number in choices:
            found_choices.add(number)
            assert raw[0] == 0x94 and encoded[0] in {ord("B"), ord("P"), ord("T")}
        else:
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert found_choices == choices
    assert leads == {0x15, 0x94, 0xA9, 0xFE}
    expected = {(197, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert (197, 22) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b198_namahage_dream_exact_changes_and_first_glyphs() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v92.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 15, "translated_records": 15, "blocks": {"198": 15}}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 15
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x0C, 0x0F, 0xFE}
    expected = {(198, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b199_portrait_book_macro_and_packed_event() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v93.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 32, "translated_records": 31, "blocks": {"199": 31}}
    assert set(batch["excluded_records"]) == {"DK4_MES_B199_R0086"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 31
    leads = set()
    fi_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = english.split("}", 1)[1].replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        fi_count += raw.count(b"FI")
        leads.add(raw[0])
    assert leads == {0x02, 0x09, 0x16, 0xFE} and fi_count == 1
    expected = {(199, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert (199, 86) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b200_carlo_traveler_and_charm_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v94.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 19, "translated_records": 19, "blocks": {"200": 19}}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert 0xAC in profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 19
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        prose = row["english"].split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, row["english"], profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, row["english"], profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x13, 0xAC, 0xFE}
    expected = {(200, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b201_rope_choices_prices_and_name_macros() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v95.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 25, "translated_records": 25, "blocks": {"201": 25}}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert 0x94 not in profile.leading_speaker_bytes and 0x69 in profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 25
    leads = set()
    fi_count = 0
    choices = set()
    for row in rows:
        number = int(row["id"].rsplit("R", 1)[1])
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        prose = (english.split("}", 1)[1] if english.startswith("{SPEAKER:") else english)
        prose = prose.replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        fi_count += raw.count(b"FI")
        if number in {50, 52}:
            choices.add(number)
            assert raw[0] == 0x94 and encoded[0] in {ord("B"), ord("P")}
        else:
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert choices == {50, 52} and fi_count == 2
    assert leads == {0x02, 0x13, 0x69, 0x94, 0xFE}
    expected = {(201, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b202_glassmaking_guide_handoff_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v96.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 19, "translated_records": 19, "blocks": {"202": 19}}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert 0x9D in profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 19
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        prose = row["english"].split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, row["english"], profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, row["english"], profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x02, 0x12, 0x93, 0x9D}
    assert next(row for row in rows if row["id"].endswith("R0055"))["english"].startswith(
        "{SPEAKER:12}Glassmaking Guide"
    )
    expected = {(202, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b203_medicine_book_prices_and_reward() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v97.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 21, "translated_records": 21, "blocks": {"203": 21}}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 21
    leads = set()
    fi_count = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        prose = row["english"].split("}", 1)[1].replace("{MACRO:FI}", "")
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, row["english"], profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, row["english"], profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        fi_count += raw.count(b"FI")
        leads.add(raw[0])
    assert leads == {0x02, 0x4C, 0xAA, 0xFE} and fi_count == 1
    assert "1,000" in next(row for row in rows if row["id"].endswith("R0074"))["english"]
    assert "100" in next(row for row in rows if row["id"].endswith("R0077"))["english"]
    expected = {(203, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b204_shachihoko_letter_and_lord_states() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v98.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 20, "translated_records": 20, "blocks": {"204": 20}}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert {0x91, 0x7C, 0x82} <= profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 20
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        prose = row["english"].split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, row["english"], profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, row["english"], profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x02, 0x0B, 0x7C, 0x82, 0x91, 0xFE}
    assert "Jam Jack Ludwyan" in next(row for row in rows if row["id"].endswith("R0072"))["english"]
    expected = {(204, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b205_parrot_echoes_and_packed_event() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v99.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 18, "translated_records": 17, "blocks": {"205": 17}}
    assert set(batch["excluded_records"]) == {"DK4_MES_B205_R0007"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 17
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        prose = row["english"].split("}", 1)[1]
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, row["english"], profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, row["english"], profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        leads.add(raw[0])
    assert leads == {0x02, 0x0F, 0xFE}
    by_id = {row["id"]: row["english"] for row in rows}
    assert "You can talk?!" in by_id["DK4_MES_B205_R0017"]
    assert "YOU CAN TALK" in by_id["DK4_MES_B205_R0020"]
    assert "STOP THAT" in by_id["DK4_MES_B205_R0040"]
    assert "SURRENDER NOW?" in by_id["DK4_MES_B205_R0063"]
    expected = {(205, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert (205, 7) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b206_earrings_choices_and_packed_item() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v100.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 29, "translated_records": 28, "blocks": {"206": 28}}
    assert set(batch["excluded_records"]) == {"DK4_MES_B206_R0015"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert {0x02, 0x07, 0xAD} <= profile.leading_speaker_bytes
    assert not ({0x82, 0x94, 0x8D} & profile.leading_speaker_bytes)
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 28
    choices = {59: "G", 61: "S", 80: "B", 82: "P"}
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        number = int(row["id"].rsplit("R", 1)[1])
        prose = english.split("}", 1)[1] if english.startswith("{SPEAKER:") else english
        assert "I" not in prose and "F" not in prose
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        if number in choices:
            assert raw[0] in {0x82, 0x94, 0x8D}
            assert encoded[0] == ord(choices[number])
        else:
            assert raw[0] in {0x02, 0x07, 0xAD}
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
    expected = {(206, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert (206, 15) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b207_b214_bare_letters_choices_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v101.json").read_text(encoding="utf-8"))
    assert batch["inventory"]["identified_records"] == 127
    assert batch["inventory"]["translated_records"] == 126
    assert batch["inventory"]["blocks"] == {"207": 13, "208": 24, "209": 20, "210": 10, "211": 12, "212": 13, "213": 17, "214": 17}
    assert set(batch["excluded_records"]) == {"DK4_MES_B213_R0022"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert 0x95 in profile.leading_speaker_bytes
    assert not ({0x82, 0x92, 0x93, 0x8A, 0x8F, 0xE6} & profile.leading_speaker_bytes)
    rows = materialize_translation_batch(batch, source)
    bare_count = macro_count = 0
    expected = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        if english.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        else:
            assert raw[0] in {0x82, 0x92, 0x93, 0x8A, 0x8F, 0xE6}
            assert encoded[0] == ord(english[0]), row["id"]
            bare_count += 1
        assert raw.count(b"FI") == encoded.count(b"FI")
        macro_count += raw.count(b"FI")
        block = int(row["id"].split("_B")[1].split("_")[0])
        expected.add((block, int(row["id"].rsplit("R", 1)[1])))
    assert bare_count == 24 and macro_count == 2
    assert len(expected) == 126 and (213, 22) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b215_b226_states_bare_entries_and_exact_changes() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v102.json").read_text(encoding="utf-8"))
    assert batch["inventory"]["identified_records"] == 155
    assert batch["inventory"]["translated_records"] == 155
    assert not batch["excluded_records"]
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert profile.balanced_wrapping
    assert {0x78, 0xC5, 0xC7} <= profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    bare_count = macro_count = 0
    expected = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        qa = audit_fixed_dialogue_record(raw, english, profile)
        assert not [i for i in qa["issues"] if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        if english.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}, row["id"]
        else:
            assert raw[0] in {0x82, 0x92}
            assert encoded[0] == ord(english[0]), row["id"]
            bare_count += 1
        assert raw.count(b"FA") == encoded.count(b"FA")
        macro_count += raw.count(b"FA")
        assert len(encoded) == len(raw)
        block = int(row["id"].split("_B")[1].split("_")[0])
        expected.add((block, int(row["id"].rsplit("R", 1)[1])))
    assert bare_count == 8 and macro_count == 2
    assert len(expected) == 155
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b136_tablet_map_and_event_exclusion() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v47.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 9, "translated_records": 8, "blocks": {"136": 8}}
    assert set(batch["excluded_records"]) == {"DK4_MES_B136_R0020"}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 8
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        assert raw[0] in {0x02, 0x0E}
        issues = audit_fixed_dialogue_record(raw, row["english"], profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}]
        encoded = encode_fixed_dialogue(raw, row["english"], profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
    expected = {(136, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert (136, 20) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b137_nagalpur_scene_exact_changes_and_macros() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v48.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 47, "translated_records": 47, "blocks": {"137": 47}}
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert 0x26 in profile.leading_speaker_bytes
    rows = materialize_translation_batch(batch, source)
    seen_states = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        issues = audit_fixed_dialogue_record(raw, row["english"], profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, row["english"], profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        assert raw.count(b"FI") == encoded.count(b"FI")
        seen_states.add(raw[0])
    assert {0x02, 0x09, 0x0E, 0x10, 0x11, 0x14, 0x16, 0x17, 0x26, 0x5C, 0xC6} <= seen_states
    expected = {(137, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 47
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b138_b139_afterword_map_branches_and_event_exclusion() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    all_rows = []
    for version, block, count in ((49, 138, 42), (50, 139, 13)):
        batch = json.loads(Path(f"translations/lil_deep_route_v{version}.json").read_text(encoding="utf-8"))
        assert batch["inventory"]["translated_records"] == count
        assert batch["inventory"]["blocks"] == {str(block): count}
        if version == 50:
            assert batch["inventory"]["identified_records"] == 14
            assert set(batch["excluded_records"]) == {"DK4_MES_B139_R0035"}
        else:
            assert batch["inventory"]["identified_records"] == 42
        profile = get_dialogue_profile(batch["dialogue_profile"])
        rows = materialize_translation_batch(batch, source)
        assert len(rows) == count
        for row in rows:
            raw = bytes.fromhex(row["source_hex"])
            issues = audit_fixed_dialogue_record(raw, row["english"], profile)["issues"]
            assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
            encoded = encode_fixed_dialogue(raw, row["english"], profile).encoded
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
            assert raw.count(b"FO") == encoded.count(b"FO")
        all_rows.extend(rows)
    expected = {
        (int(row["id"].split("_B")[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in all_rows
    }
    assert len(expected) == 55 and (139, 35) not in expected
    assert changed_segments(source, rebuild_mesfile(source, all_rows)) == expected


def test_lil_b227_b238_complete_clues_letters_and_safe_heads() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v103.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 166 and not batch["excluded_records"]
    assert {0x68, 0x71} <= profile.leading_speaker_bytes
    bare = set()
    expected = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert bare == {f"DK4_MES_B{b}_R{n:04d}" for b in (235, 236) for n in range(15, 21)}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b239_b249_choices_macros_and_packed_event() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v104.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 135
    assert set(batch["excluded_records"]) == {"DK4_MES_B242_R0097"}
    bare = set()
    expected = set()
    macros = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        assert raw.count(b"FI") == encoded.count(b"FI")
        macros += raw.count(b"FI")
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert bare == {"DK4_MES_B239_R0057", "DK4_MES_B239_R0059", "DK4_MES_B242_R0068", "DK4_MES_B242_R0070"}
    assert macros == 3
    assert (242, 97) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b295_b298_wristband_quest_safe_heads() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v111.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 23 and not batch["excluded_records"]
    expected = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        assert len(encoded) == len(raw)
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b293_b294_fog_choices_and_guide_controls() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v110.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 98
    assert set(batch["excluded_records"]) == {"DK4_MES_B293_R0029", "DK4_MES_B293_R0109"}
    expected = set()
    bare = set()
    macros = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        assert raw.count(b"FI") == encoded.count(b"FI")
        macros += raw.count(b"FI")
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert {"DK4_MES_B293_R0199", "DK4_MES_B293_R0201"} <= bare
    assert macros == 4
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b289_b292_platinum_clue_and_packed_events() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v109.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 51
    assert set(batch["excluded_records"]) == {"DK4_MES_B292_R0003", "DK4_MES_B292_R0047"}
    expected = set()
    macros = 0
    by_id = {row["id"]: row for row in rows}
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        assert len(encoded) == len(raw)
        assert raw.count(b"FI") == encoded.count(b"FI")
        macros += raw.count(b"FI")
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert macros == 3
    for row_id in ("DK4_MES_B290_R0009", "DK4_MES_B291_R0008", "DK4_MES_B292_R0013"):
        assert "Adorn me in a new star's pure glow" in by_id[row_id]["english"]
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b288_tiger_branches_preserve_heads_and_names() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v108.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 82 and not batch["excluded_records"]
    expected = set()
    bare = set()
    macros = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        assert raw.count(b"FI") == encoded.count(b"FI")
        macros += raw.count(b"FI")
        expected.add((288, int(row["id"].rsplit("R", 1)[1])))
    assert {"DK4_MES_B288_R0220", "DK4_MES_B288_R0222"} <= bare
    assert not {"DK4_MES_B288_R0237", "DK4_MES_B288_R0325"} & bare
    assert macros == 3
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b283_b287_bare_variants_choices_and_forest_control() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v107.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 104
    assert set(batch["excluded_records"]) == {"DK4_MES_B283_R0038"}
    expected = set()
    bare = set()
    macros = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare.add(row["id"])
        assert len(encoded) == len(raw)
        assert raw.count(b"FA") == encoded.count(b"FA")
        macros += raw.count(b"FA")
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert {f"DK4_MES_B283_R{n:04d}" for n in (103, 105, 107, 239, 241)} <= bare
    assert macros == 1 and (283, 38) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b255_b282_guild_quests_preserve_heads_and_macros() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v106.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 154 and not batch["excluded_records"]
    expected = set()
    macros = {macro: 0 for macro in (b"FI", b"FA", b"FO")}
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        assert len(encoded) == len(raw)
        for macro in macros:
            assert raw.count(macro) == encoded.count(macro)
            macros[macro] += raw.count(macro)
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert set(macros.values()) == {1}
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_b250_b254_puzzle_variants_and_curse_control() -> None:
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    batch = json.loads(Path("translations/lil_deep_route_v105.json").read_text(encoding="utf-8"))
    profile = get_dialogue_profile(batch["dialogue_profile"])
    rows = materialize_translation_batch(batch, source)
    assert len(rows) == 83
    assert set(batch["excluded_records"]) == {"DK4_MES_B251_R0183"}
    bare = 0
    expected = set()
    macros = 0
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        markup = row["english"]
        issues = audit_fixed_dialogue_record(raw, markup, profile)["issues"]
        assert not [i for i in issues if i["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, markup, profile).encoded
        if markup.startswith("{SPEAKER:"):
            assert encoded[0] == raw[0] and encoded[1] not in {10, 32}
        else:
            assert encoded[0] == ord(markup[0])
            bare += 1
        assert len(encoded) == len(raw)
        assert raw.count(b"FI") == encoded.count(b"FI")
        macros += raw.count(b"FI")
        expected.add((int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1])))
    assert bare == 21 and macros == 5
    assert (251, 183) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected
