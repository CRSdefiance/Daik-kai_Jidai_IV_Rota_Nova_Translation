"""Compare the four utility items and 25 weapons against the clean catalogue."""
from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save, wide_letters
from scripts.checkpoint_sailing_alert_review_v1 import branch_target
from scripts.register_source_item_cards_and_coin_v1 import RELEASE, base
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_source_item_cards_and_coin_v1 import (
    ARM, CLEAN, COMMON, FIRST, GETTER, LOOKUP, PAINT, PAINTER, ROOT, WIDE_ASCII, item_paragraph, item_table, reference,
)

OUTPUT = ROOT / 'utility_weapon_item_cards_context_v1.json'
IDS = tuple(range(2835, 2864))
DATA = {
    2835: (
        'This golden-furred cat loves to eat, and mice are its favorite.',
        'Its fur is golden all over. It is a glutton and especially loves mice.',
        'Give the cat an appetite in ordinary English and keep mice as its favorite food.',
    ),
    2836: (
        'No matter how often you squeeze it, this magic lime yields juice to quench the crew’s thirst at sea.',
        'A magical lime gives drops however often it is squeezed, relieving the navigators’ thirst on voyages.',
        'Make the repeated squeezing and the benefit at sea clear in one sentence.',
    ),
    2837: (
        'This ring holds the soul of Hermes, one of the twelve Olympians and god of travel. It’s said to keep sailors safe in storms.',
        'A mysterious ring contains the soul of Hermes, god of travel and one of the twelve Olympians. It supposedly protects sailors in storms.',
        'Restore Hermes’s place among the Twelve and the ring’s protection in storms generally.',
    ),
    2838: (
        'A tiny dose is said to cure any contagious disease. The famed physician Hua Tuo devised it in China’s Three Kingdoms era.',
        'This medicine is said to work against any contagious disease, even in a tiny dose. It is made by the method of Hua Tuo, a famed physician of China’s Three Kingdoms era.',
        'Keep the claim attributed to the catalogue and restore both contagious disease and Hua Tuo’s renown.',
    ),
    2839: (
        'A slender sword with a blade and hilt painted glossy black.',
        'A thin sword with its blade and hilt painted a shiny black.',
        'Use a single descriptive phrase and keep both black-painted parts.',
    ),
    2840: (
        'A broadsword supposedly used by Laocoon, priest of ancient Troy.',
        'A broad-bladed sword said to have been used by Laocoon, a priest of Troy in ancient times.',
        'Retain the concise item-card style, the priest and the traditional attribution.',
    ),
    2841: (
        'The legendary knight Lohengrin is said to have carried this saber. Its blade is longer and sharper than most.',
        'A saber said to have been used by the legendary knight Lohengrin, longer and sharper than an ordinary saber.',
        'Keep the legend qualified and make the two comparisons flow as a separate sentence.',
    ),
    2842: (
        'The S-shaped blade shines like a golden crescent moon.',
        'A sword with an S-shaped blade whose cutting edge gleams gold and looks like a crescent moon.',
        'Keep the shape, golden gleam and crescent comparison in a single natural image.',
    ),
    2843: (
        'This ornate curved sword is worn as a mark of heroism.',
        'An elaborately decorated curved sword regarded as proof that its bearer is a hero.',
        'Keep the sword’s meaning as a recognized symbol and its ornate decoration.',
    ),
    2844: (
        'A very heavy military sword made entirely of gold.',
        'A very heavy military sword made of gold in every part.',
        'Retain the natural catalogue phrase, the weight and the all-gold construction.',
    ),
    2845: (
        'Plain and practical, this sword is easy to wield and mysteriously fills its holder with courage.',
        'A mysterious sword that fills its holder with courage. It is plain and unadorned, practical in battle and easy to handle.',
        'Retain the contrast between the plain, practical blade and its mysterious effect.',
    ),
    2846: (
        'An Indian saber with countless lapis beads, said to be ancient.',
        'An Indian saber studded with countless lapis lazuli beads, believed to have been made in antiquity.',
        'Retain the natural wording and replace the full-width capital I with the matching ASCII glyph.',
    ),
    2847: (
        'It looks like any old sword, but it was supposedly prized by an admiral who cleared the nearby seas of pirates.',
        'At first glance it looks like an ordinary old sword, but this fine piece was said to be favored by an admiral who wiped out pirates in nearby waters.',
        'Restore the first impression and the admiral’s attachment to the sword.',
    ),
    2848: (
        'A wide, crescent blade. A deputy is said to have struck down a sailor on the spot for urging betrayal of the admiral.',
        'A wide crescent blade said to have been used when a fleet deputy struck down a sailor on the spot for urging betrayal of the admiral.',
        'Keep the sudden response and preserve the source’s silence about whom the sailor tried to persuade.',
    ),
    2849: (
        'A dagger with an H-shaped hilt, strange colors and unusual ornaments. Its origins are unknown.',
        'A dagger with a distinctive H-shaped hilt, unusual coloring and decoration, and no known origin.',
        'Preserve the unusual decorations, the H shape and the unknown origin in natural catalogue prose.',
    ),
    2850: (
        'A two-handed blade that glows white for no known reason.',
        'A two-handed sword gives off a white light for an unknown reason.',
        'Retain the clear, concise description and the source’s uncertainty.',
    ),
    2851: (
        'The red tint of this crescent blade calls to mind all the blood it must have shed.',
        'The reddish blade of this crescent sword brings to mind the blood it has taken in the past.',
        'Keep the ominous association as an impression prompted by the blade’s color.',
    ),
    2852: (
        'Known as the Betrayer’s Sword, it has an eerie air, as though an evil spirit possessed it.',
        'Nicknamed the Betrayer’s Sword, it has an eerie presence like that of a blade possessed by an evil spirit.',
        'Preserve the nickname and the impression of possession in one complete sentence.',
    ),
    2853: (
        'Said to have belonged to Zhao Yun, a renowned general of Shu in the Three Kingdoms era. He excelled with the spear.',
        'The spear is said to have been used by Zhao Yun, a renowned Shu general of the Three Kingdoms era. The spear was his best weapon.',
        'Restore his role and keep the skill tied to the weapon type.',
    ),
    2854: (
        'A general’s blunder cost a dear ally their life. He gave the ally’s family this superb sword in apology.',
        'A general made a mistake in his plans that caused the death of a dear ally. He gave the bereaved family this fine sword to express his apology.',
        'Keep the general’s responsibility, the gift to the family and its purpose clear.',
    ),
    2855: (
        'This sword belonged to a red-haired woman pirate renowned for her beauty. Prized as a treasure, it has a keen edge.',
        'A renowned red-haired woman pirate, known for her beauty, used this blade. It is famously sharp and highly prized as a treasure.',
        'Restore the pirate’s identity and preserve both reasons the sword is remarkable.',
    ),
    2856: (
        'The mythical bull-headed Minotaur supposedly wielded this huge, mighty axe.',
        'A large and powerful axe said to have been wielded by the legendary bull-headed Minotaur.',
        'Retain the concise wording, size, strength and qualified attribution.',
    ),
    2857: (
        'This strange cooking knife becomes a powerful weapon in the hands of someone who’s angry.',
        'A mysterious kitchen knife that quickly turns into a powerful weapon when held by an angry person.',
        'Make the knife the subject of its sudden transformation.',
    ),
    2858: (
        'A vivid sky-blue knife said to grant Aztec water god Tlaloc’s protection.',
        'A bright sky-blue knife that is said to confer the protection of Tlaloc, the Aztec water god.',
        'Retain the vivid color and the clear, qualified claim of protection.',
    ),
    2859: (
        'A fine yet eerie axe with a black handle and twisted tip.',
        'A high-quality weapon with a black handle and a twisted tip, and an oddly eerie air.',
        'Retain the measured contrast and both visual details.',
    ),
    2860: (
        'This superb greatsword was wielded by the Mongol hero Kublai Khan. It strikes with tremendous force from above.',
        'A fine greatsword used by the Mongol hero Kublai Khan, especially formidable in a downward strike.',
        'Keep the named owner and the catalogue’s two observations about the sword.',
    ),
    2861: (
        'A legendary spear with a fiery gleam. Ares, god of war and one of the twelve Olympians, is said to have wielded it.',
        'A legendary spear with a gleam reminiscent of flame, supposedly held by Ares, god of war and one of the twelve Olympians.',
        'Restore the Twelve and keep the fiery resemblance and attribution distinct.',
    ),
    2862: (
        'This holy sword is said to have been carried by Britain’s legendary King Arthur. Its blade is strong enough to split rock.',
        'A sacred sword with a sturdy blade capable of breaking rock, said to have hung at the side of Britain’s legendary King Arthur.',
        'Keep the legendary attribution and use a full second sentence for the blade’s strength.',
    ),
    2863: (
        'This Japanese sword has an eerie aura and an edge second to none. Legend says something will befall its owner.',
        'A Japanese sword with an ominous aura and exceptional sharpness. Tradition says something will happen to its owner.',
        'Restore the blade’s superlative sharpness and keep the legend’s outcome unspecified.',
    ),
}
ASCII = str.maketrans({'’': "'"})


def main():
    assert not OUTPUT.exists() and tuple(DATA) == IDS
    release = load(RELEASE)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    source = NdsImage.open(CLEAN)
    clean, arm = source.read_file(ARM), runtime.arm
    assert base.digest(CLEAN) == release['clean_input_sha256']
    japanese = common_message_entries(source.read_file(COMMON), clean)
    directory = sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    current = owned_entries(runtime.common, arm, directory)
    ledger = load(base.LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    credited = {(row['file_path'], row['id']) for row in ledger[base.CONTEXT]['integrated_record_keys']}
    payload, table, pointers = item_table(arm)
    consumers = []
    for lookup, paint, literal in zip(LOOKUP, PAINT, (0x4D890, 0x4E53C), strict=True):
        assert unpack_from('<I', clean, literal)[0] == unpack_from('<I', arm, literal)[0] == FIRST
        assert branch_target(clean, lookup) == BASE + 0x5528C
        assert branch_target(clean, paint) == BASE + 0xD5404
        consumers.append(dict(lookup=BASE + lookup, paint=BASE + paint, literal=BASE + literal,
                              current_lookup=GETTER, current_paint=PAINTER))

    def name_at(code, pointer):
        raw, address = (payload, POOL) if POOL <= pointer < POOL + len(payload) else (code, BASE)
        return raw[pointer - address:].split(b'\0', 1)[0]

    records = []
    for n, (draft, meaning, note) in DATA.items():
        jp, en = japanese[n], current[n]
        identifier = f'COMMON_MESSAGE_{n}'
        assert (COMMON, identifier) not in credited
        english = draft.translate(ASCII)
        current_text = en.text.decode('cp932')
        old = ' '.join(current_text.translate(WIDE_ASCII).split())
        ident = n - FIRST
        field = 0x11E210 + 24 * ident
        category = 1 if ident < 24 else 2
        assert clean[field + 16] == arm[field + 16] == category
        jp_name, name = (unpack_from('<I', code, field)[0] for code in (clean, arm))
        original_name = name_at(clean, jp_name)
        current_name = name_at(arm, name)
        compiled, lines = item_paragraph(payload, pointers[ident])
        assert ' '.join(lines) == old
        assert english.isascii() and not any(token in english for token in ('%', '\0', '\n'))
        kind = 'Utility item' if category == 1 else 'Weapon'
        records.append(dict(
            id=identifier, message_ID=n, file_path=COMMON, item_ID=ident, name_field=field,
            clean_name_pointer=jp_name, current_name_pointer=name,
            clean_name_hex=original_name.hex(), current_name_hex=current_name.hex(),
            source_item_name=original_name.decode('cp932'), item_name=current_name.decode('cp932'),
            clean_Japanese=jp.text.decode('cp932'), current_English=current_text,
            source_hex=jp.text.hex(), current_hex=en.text.hex(), source_reference=reference(jp), current_reference=reference(en),
            prior_private_pointer=pointers[ident], prior_private_rows=lines, prior_private_hex=compiled.hex(),
            private_pointer_field=table + 4 * ident, native_callers=consumers,
            speaker='Item catalogue', context=f'{kind} description read under the item title in the standalone card and main detail screen.',
            english=english, source_meaning=meaning, localization_note=note, original_substitutions=[],
            decision='retention' if english == old else 'revision', current_wide_glyphs=wide_letters(current_text),
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
        ))
    save(OUTPUT, dict(
        translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], records=records,
        registered_input=runtime.receipt(), active_description_table=table, source_rom_sha256=release['clean_input_sha256'],
        prior_context_sealed=True, new_completion_credit=0, full_goal_complete=False,
        evidence={str(path): base.digest(path) for path in (RELEASE, Path(__file__))},
    ))
    print(f'{len(records)} utility and weapon cards. {sum(r["decision"] == "revision" for r in records)} revisions.')


if __name__ == '__main__':
    main()
