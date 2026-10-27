from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_release_translation_integrity import (
    build_report,
    common_native_source_spans,
    has_text,
    native_entry_was_erased,
)


def test_repacked_silent_question_uses_its_native_source_not_old_byte_position():
    clean = NdsImage.open('work/clean.nds')
    candidate = NdsImage.open('out/all_routes_combined_v117_candidate.nds')
    source = common_native_source_spans(clean, candidate)[(23, 20, 15, 19)]
    assert source.decode('cp932') == '…？'
    old_record = IlnkContainer.parse(clean.read_file('/COMMON/MESFILE.DK4')).blocks[23].split(b'\0')[20]
    assert has_text(old_record[15:19])
    assert not native_entry_was_erased(b'...?', source)
    assert native_entry_was_erased(b'    ', source)
    assert native_entry_was_erased(b' \n\r', '水夫'.encode('cp932'))


def test_reviewed_v117_silent_question_does_not_trigger_false_erasure():
    report = build_report(Path('out/all_routes_combined_v117_candidate.nds'),
                          Path('work/clean.nds'), 'all-routes-unified-v117')
    assert report['blocking_issue_count'] == 0
    assert report['unsafe_percent_record_count'] == 0
