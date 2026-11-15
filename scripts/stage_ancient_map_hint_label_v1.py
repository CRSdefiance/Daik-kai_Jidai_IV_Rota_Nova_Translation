"""Stage the source-owned Ancient Map Y-button text without altering artwork."""

from hashlib import sha256
from pathlib import Path
from struct import pack, unpack_from

from scripts import register_sound_bgm_titles_v1 as parent


base = parent.base
ARM, COMMON, CLEAN = parent.stage.ARM, parent.stage.COMMON, parent.stage.review.CLEAN
ROOT = Path('out/ancient_map_hint_label_staged_20261111_v1')
ROM = ROOT / 'ancient_map_hint_label_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
BASE = 0x02000000
SLOT, TABLE = 0x0216BD78, 0x0212F6CC
ORIGINAL = bytes.fromhex('8371839383670000')
ENGLISH = b'Hint\0\0\0\0'
SOURCE_SPANS = {
    (0x02101618, 0x02101648): '2759583adb7de926057db73993430058c15818d41f81b43517c264382b87f3ca',
    (0x021019D4, 0x021019E4): 'ef7f617d235872dde84425de2a56d372426617f676a3dd1c756205cdf3fbc23e',
    (0x0212F6CC, 0x0212F6E4): 'cfc0b84f221c76d5ac3aa0c636a5950ef323a3fa7bf56a641ad7526e0cb455eb',
}


def transform(original, clean):
    for (start, end), expected in SOURCE_SPANS.items():
        data = original[start - BASE:end - BASE]
        assert data == clean[start - BASE:end - BASE] and sha256(data).hexdigest() == expected
    at = SLOT - BASE
    assert original[at:at + 8] == clean[at:at + 8] == ORIGINAL
    assert [i + BASE for i in range(0, len(original) - 3, 4) if original[i:i + 4] == pack('<I', SLOT)] == [TABLE + 12]
    assert unpack_from('<I', original, TABLE - BASE + 16)[0] == 0x0211B50C
    assert original[0x11B50C:0x11B511] == b'Back\0'
    assert original[at + 8:at + 16] == b'Cursed\0\0'
    target = original[:at] + ENGLISH + original[at + 8:]
    assert target[:at] + ORIGINAL + target[at + 8:] == original
    return target


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    image, clean = (base.NdsImage.open(path) for path in (parent.ROM, CLEAN))
    arm = image.read_file(ARM)
    revised = transform(arm, clean.read_file(ARM))
    image.replace_file(ARM, revised)
    target = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(target)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), parent_sha256=release['candidate_sha256'],
        parent_ARM9_sha256=release['target_ARM9_sha256'], target_ARM9_sha256=sha256(revised).hexdigest(),
        original_COMMON_sha256=release['target_COMMON_sha256'], whole_parent_inverse_exact=True,
        record=dict(id='DK4_ANCIENT_MAP_Y_HINT_LABEL', arm9_RAM=SLOT, file_offset=SLOT-BASE, width=8,
            clean_Japanese=ORIGINAL.rstrip(b'\0').decode('cp932'), original_hex=ORIGINAL.hex(),
            localized_English='Hint', target_hex=ENGLISH.hex(), original_footer_table=TABLE,
            original_Y_entry=TABLE+12, original_Back_entry=TABLE+16, draw_call=0x02101634, painter=0x020CA890,
            context='Y opens the selected map’s inscription and location clues.',
            localization_note='Hint is the direct, natural action label for this optional clue view.',
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)),
        source_spans=[dict(start=start, end=end, sha256=sha) for (start,end), sha in SOURCE_SPANS.items()],
        display_verification_pending=True, artwork_and_runtime_code_unchanged=True, new_dialogue_credit=0))
    print('Staged the source-owned Ancient Map Y label. The original Hint and Back pointers are preserved.')


if __name__ == '__main__':
    main()
