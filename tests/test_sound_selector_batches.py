from scripts.build_sound_selector_batches import BGM_RECORDS, record_starts, repack_bgm_records


def test_bgm_packer_remaps_every_title_without_changing_record_sizes():
    records = [b"unused"] * 64
    original_by_index: dict[int, bytes] = {}
    for spec in BGM_RECORDS:
        original = b" " + b"".join(japanese.encode("cp932") for japanese, _ in spec.titles)
        if spec.preserve_after_offset is not None:
            original += b"protected tail"
        records[spec.record_index] = original
        original_by_index[spec.record_index] = original

    starts = record_starts(records)
    batch_records, old_pointers, new_pointers = repack_bgm_records(records, starts)

    assert len(old_pointers) == len(new_pointers) == 38
    assert new_pointers == sorted(new_pointers)
    assert old_pointers != new_pointers

    for spec, batch_record in zip(BGM_RECORDS, batch_records, strict=True):
        replacement = bytes.fromhex(str(batch_record["replacement_hex"]))
        original = original_by_index[spec.record_index]
        assert len(replacement) == len(original)
        assert replacement.endswith(b"protected tail") == original.endswith(b"protected tail")

    expected_titles = [english.encode("ascii") for spec in BGM_RECORDS for _, english in spec.titles]
    packed = b"".join(
        bytes.fromhex(str(record["replacement_hex"])) for record in batch_records
    )
    for title in expected_titles:
        assert title in packed
