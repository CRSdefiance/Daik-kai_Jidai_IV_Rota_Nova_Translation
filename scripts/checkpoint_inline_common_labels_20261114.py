"""Qualify the three extra clean ARM9 matches outside the Gallery caption arrays."""

from hashlib import sha256
from pathlib import Path
from struct import pack, unpack_from

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_name_or_words_confirmation_20261114 as current
from scripts.inventory_common_scene_caption_duplicates import captions
from scripts.review_sound_bgm_titles_v1 import reference


base, stage = current.base, current.stage
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/'
              'remaining_inline_label_scope_20261114_v1.json')
RAM_BASE = 0x02000000
LABEL_OWNERS = {
    3527: {0x156A9C: (0x11A900, 'City location button', 'Tavern'),
           0x16EDD8: (0x16F1FC, 'Sound Setup sound effect 9', 'Tavern')},
    3528: {0x156ABC: (0x11A910, 'City location button', 'Inn')},
    3586: {},
}
MAP_MENU_SUFFIX = 0x138600
MAP_MENU_START = 0x1385FC


def matches(data, needle):
    cursor = 0
    while (where := data.find(needle, cursor)) != -1:
        yield where
        cursor = where + 1


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256']
    assert base.digest(stage.CLEAN) == release['clean_input_sha256']
    clean, candidate = map(base.NdsImage.open, (stage.CLEAN, current.ROM))
    source_arm, arm = clean.read_file(stage.ARM), candidate.read_file(stage.ARM)
    common = candidate.read_file(stage.COMMON)
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(common).hexdigest() == release['target_COMMON_sha256']
    clean_rows = common_message_entries(clean.read_file(stage.COMMON), source_arm)
    current_rows = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    caption_text = {row['source_hex'] for row in captions(source_arm)}
    rows = []
    for n, owners in LABEL_OWNERS.items():
        text = clean_rows[n].text
        assert text == current_rows[n].text and text.hex() not in caption_text
        inline = list(matches(source_arm, text + b'\0'))
        direct, suffixes = {}, []
        for offset in inline:
            references = [at for at in matches(source_arm, pack('<I', RAM_BASE + offset)) if at % 4 == 0]
            if offset in owners:
                field, role, english = owners[offset]
                assert references == [field]
                assert unpack_from('<I', arm, field)[0] == RAM_BASE + offset
                assert arm[offset:offset + len(english) + 1] == english.encode('ascii') + b'\0'
                direct[offset] = dict(clean_text_offset=offset, pointer_field=field, current_text=english, role=role)
            else:
                if offset == MAP_MENU_SUFFIX:
                    containing_start = MAP_MENU_START
                    assert source_arm[containing_start:offset] == '古の'.encode('cp932')
                else:
                    containing_start = source_arm.rindex(b'\0', offset - 64, offset) + 1
                assert not references and containing_start < offset
                context = source_arm[containing_start:offset + len(text)].decode('cp932')
                assert context.endswith(text.decode('cp932'))
                suffixes.append(dict(offset=offset, containing_start=containing_start, containing_text=context))
        assert direct.keys() == owners.keys() and len(suffixes) == (25 if n == 3586 else 0)
        rows.append(dict(message_ID=n, Japanese=text.decode('cp932'), text_hex=text.hex(),
                         clean_reference=reference(clean_rows[n]), current_reference=reference(current_rows[n]),
                         independent_ARM9_owners=list(direct.values()), ARM9_suffixes_without_aligned_pointers=suffixes,
                         COMMON_consumer_status='open'))
    lookups = Path('work/current_amsterdam_square_20261114_v1')
    register_path = lookups / 'legacy_register_flow_exploration.json'
    table_path = lookups / 'legacy_voice_table_producers.json'
    registers, tables = map(base.load, (register_path, table_path))
    for data in (registers, tables):
        assert data['clean_sha256'] == release['clean_input_sha256']
        assert data['candidate_sha256'] == release['candidate_sha256']
    assert len(registers['pending_ids']) == 276 and not tables['pending_key_hits']
    assert len(registers['confirmed_positive_control_296_callers']) == 3
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        records=rows, offline=True, new_editorial_credit=0,
        bounded_caller_scan=dict(
            pending_ids=len(registers['pending_ids']), local_constants=len(registers['new_local_constants']),
            unresolved_register_sites=len(registers['unresolved_candidate_calls']),
            matched_table_sites=len(tables['matched_table_producer_candidates']),
            unresolved_table_sites=len(tables['unresolved_candidates']),
            register_limits=registers['limitations'], table_limits=tables['limitations']),
        evidence={str(path): base.digest(path) for path in (
            current.RELEASE, register_path, table_path, Path(__file__))}))
    print('Verified three independent ARM9 labels and 25 Map suffix matches; COMMON consumers remain open.')


if __name__ == '__main__':
    main()
