import struct

from scripts.inventory_arm9_text import pointer_references, scan


def test_single_character_and_low_address():
    rows = scan(b'\0' + '金'.encode('cp932') + b'\0')
    assert rows[0]['offset'] == 1 and rows[0]['text'] == '金'
    assert rows[0]['japanese_character_count'] == 1


def test_long_and_multiline_text_is_not_cut_off():
    text = 'これは長い説明です。' * 12 + '\n終わり'
    row = scan(text.encode('cp932') + b'\0')[0]
    assert row['text'] == text and row['length'] > 64


def test_halfwidth_kana_is_reported():
    row = scan('ｾｰﾌﾞ'.encode('cp932') + b'\0')[0]
    assert row['text'] == 'ｾｰﾌﾞ' and row['halfwidth_kana_only']


def test_island_after_binary_control_and_unterminated_tail():
    rows = scan(b'\x01' + '保存'.encode('cp932'))
    assert len(rows) == 1 and rows[0]['text'] == '保存'
    assert not rows[0]['nul_terminated']


def test_ascii_and_invalid_cp932_do_not_become_japanese():
    assert not scan(b'English\0\x81\0')


def test_pointer_reference_including_interior_byte():
    rows = scan('港町'.encode('cp932') + b'\0')
    raw = struct.pack('<II', 0x02000000, 0x02000002)
    pointer_references(rows, [('arm9', 0x02000000, raw)], 0x02000000)
    refs = rows[0]['aligned_pointer_candidates']
    assert [r['interior_byte_offset'] for r in refs] == [0, 2]


def test_ideographic_space_does_not_hide_wireless_heading():
    text = '親機\u3000ステージ選択'
    row = scan(text.encode('cp932') + b'\0')[0]
    assert row['text'] == text
    assert row['current_hex'] == text.encode('cp932').hex().upper()
    assert row['nul_terminated']


def test_fullwidth_player_labels_are_retained_without_claiming_japanese_words():
    rows = scan('１Ｐ'.encode('cp932') + b'\0' + '－'.encode('cp932') + b'\0')
    assert [row['text'] for row in rows] == ['１Ｐ', '－']
    assert rows[0]['japanese_character_count'] == 0
    assert rows[0]['fullwidth_character_count'] == 2
    assert not rows[0]['halfwidth_kana_only']
    assert rows[1]['fullwidth_character_count'] == 1


def test_ideographic_space_alone_is_not_a_translation_candidate():
    assert not scan('\u3000'.encode('cp932') + b'\0')
