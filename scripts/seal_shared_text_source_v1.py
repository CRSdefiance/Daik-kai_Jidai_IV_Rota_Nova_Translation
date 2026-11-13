"""Seal the next shared-text drafts against the exact clean Japanese source."""

from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.audit_story_glyph_consistency import save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


CLEAN = Path('work/clean.nds')
ROOT = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
DRAFTS = ROOT / 'source_first_drafts.tsv'
SOURCE = ROOT / 'clean_source_packet.json'
COMMON = '/COMMON/MESFILE.DK4'
ARM = '/__arm9__.bin'
GROUPS = [range(85, 97), range(98, 108), range(108, 125), range(125, 137), range(750, 753)]


def reference(row):
    return dict(block=row.block, offset=row.block_offset, copy_end=row.copy_end, bytes=len(row.text),
        record_index=row.record_index, table_offset=row.table_offset, start_in_record=row.start)


def main():
    assert not SOURCE.exists()
    assert digest(CLEAN) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    clean = NdsImage.open(CLEAN)
    common, arm = clean.read_file(COMMON), clean.read_file(ARM)
    rows = common_message_entries(common, arm)
    drafts = {}
    for line in DRAFTS.read_text(encoding='utf-8').splitlines()[1:]:
        ident, english, finding = line.split('\t')
        number = int(ident)
        assert number not in drafts and english and finding
        drafts[number] = (english.replace('\\n', '\n'), finding)
    ids = {number for group in GROUPS for number in group}
    assert set(drafts) == ids and len(ids) == 54
    records = []
    for number, (draft, finding) in sorted(drafts.items()):
        source = rows[number]
        assert source.text.count(b'%s') == draft.count('%s')
        records.append(dict(id=f'COMMON_MESSAGE_{number}', file_path=COMMON, message_ID=number,
            source_reference=reference(source), source_hex=source.text.hex(), clean_Japanese=source.text.decode('cp932'),
            independent_English=draft, finding=finding, consumer_and_display_pending=True, new_credit=0))
    context = []
    for number in [*range(80, 138), *range(744, 756)]:
        row = rows[number]
        context.append(dict(message_ID=number, source_reference=reference(row), source_hex=row.text.hex(),
            clean_Japanese=row.text.decode('cp932'), draft_in_scope=number in ids))
    offset = 0x134E54
    end = arm.index(0, offset)
    raw = arm[offset:end]
    assert raw.decode('cp932') == '船を捨てる' and end - offset == 10
    save(SOURCE, dict(source_ROM=str(CLEAN), source_ROM_sha256=digest(CLEAN),
        drafts=str(DRAFTS), drafts_sha256=digest(DRAFTS), group_record_ids=[list(g) for g in GROUPS],
        records=records, clean_context=context, raw_command=dict(file_path=ARM, offset=offset,
            byte_length=len(raw), terminated_hex=(raw + b'\0').hex(), clean_Japanese=raw.decode('cp932'),
            independent_English='Abandon Ship', finding='An action on the ship selected in the fleet menu. The clean verb means to abandon or discard it. Check the current menu pointer and confirmation before deciding storage or fitting.',
            source_neighbor_window_offset=offset-12, source_neighbor_window_hex=arm[offset-12:end+14].hex(),
            consumer_and_display_pending=True, new_credit=0),
        initial_drafts_precede_registered_English_comparison=True, source_prose_or_completion_credit_added=0,
        full_goal_complete=False))
    print('Sealed 54 COMMON drafts and one raw command against the clean Japanese.')


if __name__ == '__main__':
    main()
