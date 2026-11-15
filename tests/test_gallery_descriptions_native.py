"""Guard actual Gallery first letters, route selection and compiled row tails."""

import json
import struct
from pathlib import Path

import pytest

from dk4tool.patch.gallery_description_release import compile_rows
from dk4tool.rom.nds import NdsImage
from scripts.probe_gallery_parent_composition import composition
from scripts.verify_gallery_descriptions_research import verify_page


@pytest.fixture(scope='module')
def sources():
    return (Path('work/analysis/gallery_description_research_arm9.bin').read_bytes(),
            json.loads(Path('work/analysis/gallery_description_plan.json').read_text(encoding='utf-8')),
            NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT'))


def test_logical_paragraph_has_complete_words_no_weak_end_and_pair_safe_rows():
    text = "View the ruins and churches you've discovered."
    rows = compile_rows(text, 2, 40)
    assert ' '.join(row.rstrip() for row in rows) == text
    assert rows[0].rstrip().endswith('churches')
    assert all(len(row) % 2 == 0 and not row.startswith(' ') for row in rows)
    with pytest.raises(ValueError, match='does not fit'):
        compile_rows('This whole paragraph must remain complete.', 2, 4)


def test_native_initial_page_and_all_captain_selections_are_complete(sources):
    source, plan, font = sources
    verify_page(source, plan, 'events', font, 4)
    for index in range(4):
        verify_page(source, plan, 'event-' + str(index), font, 16)
    parent = composition(source)
    assert parent['draw_requests'][0]['size'] == [256, 192]
    assert parent['nonzero_canvas_seed_cleared_and_object_canaries_preserved']


def test_shifted_title_pointer_drops_first_letter_and_is_rejected(sources):
    source, plan, font = sources
    changed = bytearray(source)
    pointer = struct.unpack_from('<I', source, 0x432C8)[0]
    struct.pack_into('<I', changed, 0x432C8, pointer + 1)
    with pytest.raises(ValueError, match='loses text'):
        verify_page(bytes(changed), plan, 'events', font, 4)


def test_wrong_captain_description_is_rejected(sources):
    source, plan, font = sources
    changed = bytearray(source)
    changed[0x115678:0x11567C] = source[0x11567C:0x115680]
    with pytest.raises(ValueError, match='loses text'):
        verify_page(bytes(changed), plan, 'event-0', font, 16)
