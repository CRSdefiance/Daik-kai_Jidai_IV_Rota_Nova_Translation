"""Review the coin response and all twenty Source Item descriptions."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save, wide_letters
from scripts.checkpoint_sailing_alert_review_v1 import branch_target, caller_binding
from scripts.register_faction_aftermath_portraits_v1 import RELEASE, base
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, ROOT, reference


OUTPUT = ROOT / 'source_item_cards_and_coin_context_v1.json'
COIN, FIRST, COUNT = 2814, 2815, 20
IDS = tuple(range(COIN, FIRST + COUNT))
GETTER, PAINTER = 0x0238C5C4, 0x0238C5F4
LOOKUP, PAINT = (0x4D834, 0x4E50C), (0x4D840, 0x4E518)
DATA = {
    2814: ("Pick at least one coin or we can't keep playing.",
           'The opponent says the game cannot proceed unless the player chooses at least one coin.',
           'Use a short, conversational correction that tells the player exactly how to continue.'),
    2815: ('A New World crop. Locals eat its fruit and seeds as a staple food.',
           'A plant grown in the New World. Its fruit and seeds are edible and are a staple for the people there.',
           'Retain the readable entry and both edible parts. The card title supplies the crop name.'),
    2816: ('A New World vegetable whose ripe fruit turns vivid red.',
           'A vegetable grown in the New World whose fruit turns bright red when ripe.',
           'Retain the concise description, the place where it is grown and the color of the ripe fruit.'),
    2817: ('This Southeast Asian tree bears sweet, fragrant fruit that turns yellow when ripe and ready to eat.',
           'A tree found in Southeast Asia. Its fruit turns yellow when ripe and edible, and is fragrant and sweet.',
           'Use a complete sentence and keep ripeness linked to color and edibility.'),
    2818: ('Honeybees build this hive with care. It is packed with nourishing nectar they gather from flowers.',
           'A carefully built honeybee hive full of nutritious nectar collected from flowers.',
           'Keep the construction and the origin of the nectar clear in two sentences.'),
    2819: ('A fierce fish that sometimes attacks people. Its fins and eggs are prized for their flavor.',
           'A fierce fish that can attack people. Its fins and eggs are prized because they taste good.',
           'Restore a complete first sentence and give the reason for prizing both fins and eggs.'),
    2820: ('Known as the king of spices, this fruit grows on tropical plants 5 to 9 meters tall. India produces it in abundance.',
           'The fruit of a tropical plant that reaches 5 to 9 meters, produced in large quantities in India and known as the king of spices.',
           'Keep the metric height, country and nickname. Use the ordinary I in India in both stored versions.'),
    2821: ('Native to Southeast Asia, cloves are dark brown and shaped like nails. Their strong, sweet scent comes with a tongue-numbing bite.',
           'The dark brown, nail-shaped fruit also called cloves is native to Southeast Asia. It has a strong, sweet smell and a tongue-numbing bite.',
           'Use the source’s common name and keep both the sweet aroma and the physical sensation.'),
    2822: ('This tree grows from India to Southeast Asia. Its dried bark has a distinctive sweet scent and is used as a flavoring.',
           'The tree grows from India to Southeast Asia. Its dried bark has a distinctive sweet aroma and is used as an aromatic.',
           'Separate the geographic range from the use of the dried bark. Preserve the established trade meaning and ordinary capital I.'),
    2823: ('A New World chili with round or oblong fruit that has a powerful bite when chewed.',
           'A kind of chili native to the New World. Its fruit is round or oblong and has a strong bite.',
           'Retain the clear description and both possible fruit shapes.'),
    2824: ('A tree from East Africa with pure white, jasmine-scented flowers. Its dried fruit is roasted to make a drink.',
           'A tree native to East Africa whose pure white flowers smell of jasmine. Its dried fruit is roasted to make a drink.',
           'Replace catalogue fragments with readable sentences and preserve the plant part named in the game.'),
    2825: ('A tree from southern China with long oval leaves fermented for tea. Flavor varies by the parts used and degree of fermentation.',
           'A tree native to southern China. Its long oval leaves are fermented for a drink. Flavor varies with the parts used and the degree of fermentation.',
           'Keep the preparation step and both reasons for differences in flavor.'),
    2826: ('This tall New World tree bears large fruit right on its trunk. The seeds are removed, fermented, and dried for food.',
           'A tall tree native to the New World, with large fruit growing directly on its trunk. The seeds are removed, fermented and dried to eat.',
           'Keep the unusual placement of the fruit and all three steps of seed preparation.'),
    2827: ('A New World plant. The dried leaves are shredded and wrapped in paper or similar material for smoking.',
           'A plant native to the New World whose dried leaves are finely cut, wrapped in paper or the like, lit, and smoked.',
           'Keep the plant’s origin and flexible wrapping material. “For smoking” supplies lighting and inhalation in ordinary English.'),
    2828: ('A book of secrets from alchemy, the study of what matter is made of. It explains how to turn one substance into another.',
           'A book containing the secrets of alchemy, which seeks to understand the structure of matter. It describes changing one substance into another.',
           'Keep the two ideas in sequence. The first sentence explains alchemy and the second identifies the method the book describes.'),
    2829: ('A detailed guide to making glassware.',
           'A book that explains in careful detail how to make glasswork.',
           'Retain the concise, accurate title description and the emphasis on detail.'),
    2830: ('As these moth larvae mature, their bodies turn clear and they spin cocoons. The silk they spin is used to make clothing.',
           'Moth larvae that turn transparent as they mature. They spin cocoons with silk that becomes material for clothing.',
           'Describe the cocoon and silk together and preserve the use in clothing.'),
    2831: ('This loom weaves fabric by crossing threads. It is worked by hand and foot.',
           'A machine that interlaces threads lengthwise and crosswise to weave cloth. It is operated with the hands and feet.',
           'Keep both the method of weaving and the way the loom is operated.'),
    2832: ('This bivalve lives off Japan and produces pearls. Its shell is almost square and blackish brown.',
           'A bivalve in Japanese coastal waters, with a nearly square blackish brown shell. It is the host in which pearls form.',
           'Restore the kind of shellfish and keep the source’s approximate shell shape and color.'),
    2833: ('An Eastern medical text of unknown authorship. It describes how to make medicines from herbs and bark.',
           'An Eastern medical book of unknown authorship that describes making medicines from plants and tree bark.',
           'Keep the unknown author explicit and use the tone of a catalogue entry.'),
    2834: ("A round, dark purple fruit from Southeast Asia with juicy, delicious flesh. It's known as the queen of fruits.",
           'A Southeast Asian fruit with a round, dark purple exterior and juicy, delicious flesh. It is also called the queen of fruits.',
           'Retain the nickname and link the description of the flesh to the fruit.'),
}
WIDE_ASCII = str.maketrans({chr(i + 0xFEE0): chr(i) for i in range(0x21, 0x7F)})


def item_table(arm):
    code = MainCodeFile(arm, BASE)
    assert len(code.sections) == 6
    payload = bytes(code.sections[3].data[:-48])
    assert all(branch_target(arm, pc) == GETTER for pc in LOOKUP)
    assert all(branch_target(arm, pc) == PAINTER for pc in PAINT)
    offset = GETTER - POOL
    assert unpack_from('<I', payload, offset + 20)[0] == 0xE35400DA
    table = unpack_from('<I', payload, offset + 44)[0]
    pointers = unpack_from('<218I', payload, table - POOL)
    assert all(POOL <= pointer < POOL + len(payload) - 64 for pointer in pointers)
    return payload, table, pointers


def item_paragraph(payload, pointer):
    at = pointer - POOL
    end = payload.index(b'\0\0', at)
    raw = payload[at:end + 2]
    lines = raw[:-2].decode('ascii').split('\0')
    assert 1 <= len(lines) <= 3 and all(0 < len(line) <= 47 for line in lines)
    return raw, lines


def main():
    assert not OUTPUT.exists()
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
    coin_call = caller_binding(clean, arm, 0x63CA0, 0x63CA4, 0x63DCC, COIN, 0x53FE4)
    descriptions = []
    for offset, paint, literal in zip(LOOKUP, PAINT, (0x4D890, 0x4E53C), strict=True):
        assert unpack_from('<I', clean, literal)[0] == unpack_from('<I', arm, literal)[0] == FIRST
        assert branch_target(clean, offset) == BASE + 0x5528C and branch_target(clean, paint) == BASE + 0xD5404
        descriptions.append(dict(lookup=BASE + offset, paint=BASE + paint, literal=BASE + literal,
                                 current_lookup=GETTER, current_paint=PAINTER))
    payload, table, pointers = item_table(arm)
    assert tuple(DATA) == IDS
    records = []
    for n, (english, meaning, note) in DATA.items():
        jp, en = japanese[n], current[n]
        identifier = f'COMMON_MESSAGE_{n}'
        assert (COMMON, identifier) not in credited
        assert not any(token in english for token in ('%', '\0', '\n'))
        old = ' '.join(en.text.decode('cp932').translate(WIDE_ASCII).split())
        if n == COIN:
            context = 'The opponent replies when the player attempts to confirm a turn with zero selected coins. The game waits for the player to select a coin.'
            extra = dict(speaker='Coin game opponent', original_consumer=0x02053FE4, native_callers=[coin_call])
        else:
            ident = n - FIRST
            field = 0x11E210 + 24 * ident
            assert clean[field + 16] == arm[field + 16] == 0
            jp_name, name = (unpack_from('<I', code, field)[0] for code in (clean, arm))
            def name_at(code, pointer):
                raw, address = (payload, POOL) if POOL <= pointer < POOL + len(payload) else (code, BASE)
                return raw[pointer - address:].split(b'\0', 1)[0]
            compiled, lines = item_paragraph(payload, pointers[ident])
            assert ' '.join(lines) == old
            context = 'Source Item catalogue description under the item title. Both the standalone card and the item detail screen show the same description.'
            extra = dict(speaker='Item catalogue', item_ID=ident, name_field=field,
                clean_name_pointer=jp_name, current_name_pointer=name, clean_name_hex=name_at(clean, jp_name).hex(),
                current_name_hex=name_at(arm, name).hex(), item_name=name_at(arm, name).decode('cp932'),
                prior_private_pointer=pointers[ident], prior_private_rows=lines, prior_private_hex=compiled.hex(),
                private_pointer_field=table + 4 * ident, native_callers=descriptions)
        records.append(dict(id=identifier, message_ID=n, file_path=COMMON, clean_Japanese=jp.text.decode('cp932'),
            current_English=en.text.decode('cp932'), source_hex=jp.text.hex(), current_hex=en.text.hex(),
            source_reference=reference(jp), current_reference=reference(en), english=english, source_meaning=meaning,
            localization_note=note, context=context, decision='retention' if english == old else 'revision',
            current_wide_glyphs=wide_letters(en.text.decode('cp932')), original_substitutions=[],
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False), **extra))
    save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'], records=records,
        registered_input=runtime.receipt(), active_description_table=table, source_rom_sha256=release['clean_input_sha256'],
        prior_context_sealed=True, new_completion_credit=0, full_goal_complete=False,
        evidence={str(path): base.digest(path) for path in (RELEASE, Path(__file__))}))
    print('Reviewed the coin-game correction and twenty source-item descriptions.')


if __name__ == '__main__':
    main()

