"""Stage source-bound labels and date format in the original character editor."""

from pathlib import Path
import re
from struct import pack, unpack_from

from dk4tool.patch.village_promised_words_release import resident_components
from scripts import register_cristina_recruitment_name_20261115 as parent
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.verify_release_baseline import files


base, ARM, CLEAN = parent.base, parent.stage.ARM, parent.stage.CLEAN
ROOT = Path('work/rafael_setup_labels_20261115_v2')
ROM = ROOT / 'Rafael_Setup_Labels_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
GATES = ['source', 'context', 'localization', 'naturalness', 'formatting']
BASE = 0x02000000
HEADINGS = (
    ('EDIT_FIRST_NAME', 0x14FC28, 0x14FCA0, '名', 'Name: Edit', 'Edit First Name', 'Name alongside the middle and last names refers to the first name.'),
    ('EDIT_MIDDLE_NAME', 0x14FC3C, 0x14FCA4, 'ミドルネーム', 'Middle: Edit', 'Edit Middle Name', 'Name makes the selected field explicit.'),
    ('EDIT_LAST_NAME', 0x14FC50, 0x14FCA8, '姓', 'Last: Edit', 'Edit Last Name', 'Last Name is the usual American English label for the family name.'),
    ('EDIT_COMPANY', 0x14FC64, 0x14FCAC, '勢力名', 'Company: Edit', 'Edit Company', 'Company matches the field label and keeps it distinct from a personal name.'),
    ('EDIT_BIRTHDAY', 0x14FC78, 0x14FCB0, '誕生日', 'Birthday: Edit', 'Edit Birthday', 'The command opens the birthday calendar when the field is selected.'),
)
CALENDAR = (
    ('BIRTHDAY_DATE_VALUE', 0x1502BC, 0x9E6F0, 20, '%2d月%2d日　生まれ', '%2d/%2d Born', '%d/%d',
     'The Birth row already identifies the date. Use standard American numeric month/day order without spaces or a redundant Born suffix.'),
    ('BIRTHDAY_MONTH_NUMBER_SUFFIX', 0x150378, 0xA0674, 4, '月\n', 'M\n', ' \n',
     'The Month heading identifies the number. Preserve the original calendar line feed and replace the redundant M with its blank cell.'),
    ('BIRTHDAY_MONTH_HEADING', 0x15037C, 0xA0678, 8, '誕生日', 'Date', 'Month',
     'The editor header already says Edit Birthday. Month now identifies the arrow-controlled number above the day grid.'),
)


def digest(data):
    return parent.stage.digest(data)


def install(source, current, release):
    clean_arm, arm = [image.read_file(ARM) for image in (source, current)]
    components = resident_components(current)
    assert digest(arm) == release['target_ARM9_sha256']
    edited = bytearray(arm)
    result = []
    for ident, pos, field, capacity, exact_Japanese, old, target, reason in (
        *((i, a, f, 20, j, o, t, r) for i, a, f, j, o, t, r in HEADINGS), *CALENDAR,
    ):
        assert unpack_from('<I', clean_arm, field) == unpack_from('<I', arm, field) == (BASE + pos,)
        original = clean_arm[pos:pos + capacity]
        previous = arm[pos:pos + capacity]
        japanese = original.split(b'\0', 1)[0].decode('cp932')
        current_text = previous.split(b'\0', 1)[0].decode('ascii')
        assert japanese.startswith(exact_Japanese) and current_text.rstrip(' ') == old
        # Adjacent headings redraw the same surface without clearing its last
        # cells. Draw blanks through the longest heading's full cell extent.
        display = target.ljust(16) if ident.startswith('EDIT_') else target
        raw = display.encode('ascii') + b'\0'
        assert len(raw) <= capacity
        expected = (BASE + field, BASE + pos)
        references = []
        for _, resident, data in components:
            for ptr in range(BASE + pos, BASE + pos + capacity):
                references.extend((resident + m.start(), ptr) for m in re.finditer(re.escape(pack('<I', ptr)), data))
        assert references == [expected], (ident, references)
        stored = raw.ljust(capacity, b'\0')
        edited[pos:pos + capacity] = stored
        is_suffix = ident == 'BIRTHDAY_MONTH_NUMBER_SUFFIX'
        assert raw.count(b'\n') == original.count(b'\n') == int(is_suffix)
        own = dict(ARM9_offset=pos, pointer_field=field, allocation=capacity)
        result.append(dict(id=ident, file_path=ARM, speaker='New Game character editor', Japanese=japanese,
            source_meaning=exact_Japanese.rstrip('\n') if is_suffix else (target if ident.startswith('EDIT_') else
                ('The date of birth in month/day order.' if '%' in target else 'The heading for the birthday date picker.')),
            context='The player edits the five starting fields and chooses month and day separately in the birthday calendar.',
            previous_English=current_text, english='Month number' if is_suffix else target, decision='revision',
            localization_note=reason, source_reference=own | dict(raw_hex=original.hex()),
            current_reference=own | dict(raw_hex=previous.hex()), registered_reference=own | dict(raw_hex=stored.hex()),
            review=dict.fromkeys(GATES, True), runtime_substitutions=2 if '%' in target else 0,
            layout_line_feed_preserved=is_suffix, heading_clear_cells=16 if ident.startswith('EDIT_') else None))
    changed = bytes(edited)
    for row in result:
        own = row['current_reference']
        off, size = own['ARM9_offset'], own['allocation']
        edited[off:off + size] = bytes.fromhex(own['raw_hex'])
        if row['runtime_substitutions']:
            assert re.findall(rb'%\d*d', bytes.fromhex(row['source_reference']['raw_hex'])) == [b'%2d', b'%2d']
            assert re.findall(rb'%\d*d', bytes.fromhex(row['registered_reference']['raw_hex'])) == [b'%d', b'%d']
    assert bytes(edited) == arm
    verify_runtime(changed, release)
    return changed, result


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(parent.MANIFEST) == release['manifest_sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256'] and base.digest(CLEAN) == release['clean_input_sha256']
    source, current = map(base.NdsImage.open, (CLEAN, parent.ROM))
    before = files(current)
    arm, rows = install(source, current, release)
    current.replace_file(ARM, arm)
    after = files(current)
    assert before.keys() == after.keys() and [p for p in before if before[p] != after[p]] == [ARM]
    ROOT.mkdir()
    current.save(ROM)
    current.replace_file(ARM, before[ARM])
    assert bytes(current.rom.save()) == parent.ROM.read_bytes()
    base.save(STORED, dict(candidate_sha256=base.digest(ROM), previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=digest(arm), fields=rows, whole_parent_inverse_exact=True))
    print('Eight source-bound fields staged with complete parent inverse and preserved ASCII right bound.')


if __name__ == '__main__':
    main()
