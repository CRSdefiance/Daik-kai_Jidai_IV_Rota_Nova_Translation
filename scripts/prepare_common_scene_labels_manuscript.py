"""Source-reviewed prose for every remaining COMMON scene/artwork/name label.

COMMON renderer/visibility remains unclassified; this cannot approve insertion.
"""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

EXTRA = {
    3394: ('港町２（大）', 'Port Town 2 (Large)'),
    3397: ('３人と船（大）', 'Three People and a Ship (Large)'),
    3401: ('ハンスとアルカディウス', 'Hans and Arcadius'),
    3410: ('月下のバイオリンとラファエル１（大）', 'Raphael and a Violin in the Moonlight 1 (Large)'),
    3412: ('弾いているラファエルのアップ', 'Raphael Playing, Up Close'),
    3438: ('傷ついたホドラム', 'A Wounded Hodram'),
    3456: ('走るリルとカミル', 'Lil and Kamil Running'),
    3462: ('がっかりリルとお出迎えクリフォード', 'A Disappointed Lil and a Welcoming Clifford'),
    3480: ('チューリップが咲き乱れる風景（大）', 'Tulips in Full Bloom (Large)'),
    3490: ('マリアとクリフォード', 'Maria and Clifford'),
    3497: ('総見算のマリアたち', 'Maria and Her Companions at the Grand Review'),
    3500: ('アンジェロ現る', 'Angelo Appears'),
    3515: ('えっへんサムウェル', 'A Proud Samwell'),
    3527: ('酒場', 'Tavern'),
    3528: ('宿屋', 'Inn'),
    3529: ('執務室', 'Office'),
    3530: ('応接室', 'Reception Room'),
    3531: ('船の甲板１', "Ship's Deck 1"),
    3532: ('船の甲板２', "Ship's Deck 2"),
    3563: ('共同洞窟', 'Shared Cave'),
    3564: ('砂漠01', 'Desert 01'),
    3565: ('砂漠02', 'Desert 02'),
    3566: ('砂漠03', 'Desert 03'),
    3567: ('砂漠04オアシス', 'Desert 04: Oasis'),
    3568: ('砂漠05流砂', 'Desert 05: Quicksand'),
    3569: ('砂漠06砂嵐', 'Desert 06: Sandstorm'),
    3570: ('ＯＰ最後', 'Opening: Final Scene'),
    3571: ('海と太陽', 'Sea and Sun'),
    3572: ('ラファエルとトマト', 'Raphael and a Tomato'),
    3573: ('ＯＰ最後２', 'Opening: Final Scene 2'),
    3574: ('ＯＰホドラム１', 'Opening: Hodram 1'),
    3575: ('ＯＰリル１', 'Opening: Lil 1'),
    3576: ('ＯＰリル２', 'Opening: Lil 2'),
    3577: ('港による奴隷船', 'A Slave Ship Calls at Port'),
    3578: ('のどかな風景', 'A Peaceful Landscape'),
    3579: ('村を襲う奴隷商人', 'Slave Traders Attack the Village'),
    3580: ('意味ありげなセラ', "Sera's Meaningful Look"),
    3581: ('マリアと薔薇１', 'Maria and a Rose 1'),
    3582: ('マリアと薔薇２', 'Maria and a Rose 2'),
    3583: ('敵キャラたち', 'Enemy Characters'),
    3584: ('書斎のエイレネ', 'Irene in the Study'),
    3585: ('ナイフ１', 'Knife 1'),
    3586: ('地図', 'Map'),
    3587: ('碇を上げろ', 'Weigh Anchor'),
    3588: ('帆を張れ', 'Set the Sails'),
    3589: ('出航', 'Set Sail'),
    3590: ('夕方', 'Evening'),
    3591: ('夜', 'Night'),
    3592: ('ＯＰホドラム２', 'Opening: Hodram 2'),
    3593: ('ラファエルとトマト', 'Raphael and a Tomato'),
    3594: ('つなぎ１Ａ', 'Transition 1A'),
    3595: ('つなぎ１Ｂ', 'Transition 1B'),
    3596: ('つなぎ２Ａ', 'Transition 2A'),
    3597: ('つなぎ２Ｂ', 'Transition 2B'),
    3598: ('タイトル', 'Title'),
    3599: ('タイトル２', 'Title 2'),
    3600: ('タイトル３', 'Title 3'),
    3601: ('ラファエル名前１', 'Raphael: Name 1'),
    3602: ('ラファエル名前２', 'Raphael: Name 2'),
    3603: ('ホドラム名前１', 'Hodram: Name 1'),
    3604: ('ホドラム名前２', 'Hodram: Name 2'),
    3605: ('リル名前', 'Lil: Name'),
    3606: ('意味ありげなセラ２', "Sera's Meaningful Look 2"),
}
PATHS = [
    ('01直', '01: Straight Ahead'), ('02直', '02: Straight Ahead'),
    ('03右折', '03: Right Turn'), ('04左折', '04: Left Turn'),
    ('05左細右太', '05: Narrow Left Path, Wide Right Path'),
    ('06左太右細', '06: Wide Left Path, Narrow Right Path'),
    ('07直左', '07: Straight Ahead or Left'), ('08直右', '08: Straight Ahead or Right'),
    ('09崖', '09: Cliff'), ('10行止', '10: Dead End'), ('11河', '11: River'),
    ('12沼', '12: Swamp'), ('13濃霧', '13: Dense Fog'), ('14洞窟', '14: Cave'),
]
for start, japanese, english in ((3535, '森', 'Forest'), (3549, 'ジャングル', 'Jungle')):
    for number, (source_suffix, suffix) in enumerate(PATHS):
        EXTRA[start + number] = (japanese + source_suffix, english + ' ' + suffix)
EXTRA[3537] = ('森03右折ｔ', 'Forest 03: Right Turn t')


def build():
    clean = NdsImage.open('work/clean.nds')
    current = NdsImage.open('out/all_routes_combined_v150_candidate.nds')
    source_common, source_arm9 = [clean.read_file(p) for p in ('/COMMON/MESFILE.DK4', '/__arm9__.bin')]
    if sha(source_common) != '4ba2b09e6c4032d6466ab1ec77f6ce2eea2edf58ae50a6b2f0dcb91037e269bc':
        raise ValueError('Clean COMMON source differs')
    entries = common_message_entries(source_common, source_arm9)
    native = common_message_entries(current.read_file('/COMMON/MESFILE.DK4'), current.read_file('/__arm9__.bin'), clean=False)
    caption_path = Path('translations/scene_caption_manuscript_v2.json')
    captions = json.loads(caption_path.read_text(encoding='utf-8'))['records']
    by_japanese = {}
    for row in captions:
        if not all(row['review'].values()):
            raise ValueError('Inline caption prose is not reviewed')
        previous = by_japanese.setdefault(row['japanese'], row)
        if previous['english'] != row['english']:
            raise ValueError('Duplicate caption English differs; explicit review required')
    records, exact = [], 0
    for entry in entries[3393:3607]:
        mid, japanese = entry.message_id, entry.text.decode('cp932')
        if native[mid].text != entry.text:
            raise ValueError('Remaining COMMON label changed before source review')
        match = by_japanese.get(japanese)
        if match:
            english = match['english'].removesuffix('{PAD}') + '{PAD}'
            meaning = match['source_meaning']
            basis = {'kind': 'exact-reviewed-inline-caption', 'caption_id': match['id'],
                     'caption_pointer_field': match['pointer_field']}
            exact += 1
        else:
            expected, text = EXTRA[mid]
            if japanese != expected:
                raise ValueError(f'Explicit COMMON label source differs: {mid}')
            english = text + '{PAD}'
            meaning = 'Scene/artwork label: ' + text + '.'
            basis = {'kind': 'fresh-clean-label-localization'}
        note = ('Complete natural American English preserves the clean label, character spelling, '
                'scene details and variant markers. Authored prose contains no layout spaces/breaks. '
                'Separate COMMON visibility/consumer/layout are not established by the inline caption.')
        if mid == 3497:
            note += (' COMMON has 総見算 while the corresponding reviewed ARM9 scene says 総見式; '
                     'Grand Review follows that scene context rather than inventing an arithmetic event.')
            basis['source_variant_context'] = '総見式のマリアたち'
            siblings = {r['japanese']: r for r in captions}
            if (entries[mid - 1].text.decode('cp932') != 'マリアのくつろいだ笑顔'
                    or entries[mid + 1].text.decode('cp932') != 'マリア'
                    or siblings['総見式のマリアたち']['route_index'] != 3
                    or siblings['総見式のマリアたち']['index'] != 35
                    or siblings['マリアのくつろいだ笑顔']['index'] != 34
                    or siblings['マリア']['index'] != 36):
                raise ValueError('Grand Review source variant lacks matching adjacent scene context')
            basis['matching_neighbor_context'] = {'route': 3, 'indices': [34, 35, 36],
                                                  'common_ids': [3496, 3497, 3498]}
        if mid == 3537:
            note += ' The unexplained trailing full-width t marker is retained as ASCII t; its role remains open.'
        records.append({'id': f'COMMON_MESSAGE_{mid}', 'message_id': mid,
                        'block': entry.block, 'record': entry.record_index,
                        'source_hex': entry.text.hex(), 'japanese': japanese,
                        'previous_japanese': entries[mid - 1].text.decode('cp932'),
                        'next_japanese': entries[mid + 1].text.decode('cp932'),
                        'english': english, 'speaker': 'Scene/artwork/resource label',
                        'source_meaning': meaning,
                        'context': f'Clean native COMMON selection {mid}, B{entry.block} R{entry.record_index}; neighboring source labels retained. Separate from inline gallery captions; COMMON consumer unclassified.',
                        'localization_note': note, 'localization_basis': basis,
                        'review': {'source': True, 'context': True, 'localization': True,
                                   'naturalness': True, 'formatting': False},
                        'presentation': 'common-scene-artwork-name-unclassified'})
    if exact != 123 or len(EXTRA) != 91 or len(records) != 214:
        raise ValueError('Complete 123 exact/91 fresh label inventory differs')
    return {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
            'target_locale': 'en-US', 'encoder': 'dialogue-fixed-v1',
            'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
            'status': 'source-reviewed-draft-common-consumer-and-layout-pending',
            'source_common_sha256': sha(source_common), 'source_arm9_sha256': sha(source_arm9),
            'reviewed_caption_manuscript_sha256': sha(caption_path.read_bytes()),
            'exact_reviewed_caption_labels': exact, 'fresh_label_localizations': 91,
            'records': records,
            'limits': ['No COMMON insertion or formatting approval follows from inline caption correspondence.',
                       'Unknown resource-name/visible-caption roles, source variant typos and unexplained t marker need consumer/scene mapping.',
                       'Preserve complete labels; do not shorten to fit an assumed dialogue box.']}


def main():
    document = build()
    destination = Path('translations/common_scene_labels_manuscript_v1.json')
    destination.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('214 remaining COMMON scene/artwork/name labels source-reviewed: 123 exact caption matches and 91 fresh localizations. COMMON formatting/integration pending.')


if __name__ == '__main__':
    main()
