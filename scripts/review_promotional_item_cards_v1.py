"""Review the ten promotional relics and twenty generated map descriptions."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.reviewed_item_cards import item_table
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save, wide_letters
from scripts.probe_promotional_item_defaults import OWNER
from scripts.probe_promotional_item_full import verify as initialize
from scripts.register_relic_map_item_cards_v1 import RELEASE, base
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_source_item_cards_and_coin_v1 import (
    ARM, CLEAN, COMMON, FIRST, GETTER, LOOKUP, PAINT, PAINTER, ROOT, WIDE_ASCII, item_paragraph, reference,
)

OUTPUT = ROOT / 'promotional_item_cards_context_v1.json'
IDS = tuple(range(3003, 3033))
SEEDS = (0, 2, 3)
FRAGMENT = (
    'One of four pieces of an ancient map.',
    'A fragment of an ancient map. Four fragments make up a complete map.',
    'Restore the map’s age and the four-piece set. All twenty generated fragment slots use the same description.',
)
DATA = {
    3003: (
        'A fiery red gemstone.',
        'A red gemstone that shines as if it were on fire.',
        'Retain the concise description and the visual comparison to fire.',
    ),
    3004: (
        "A dagger engraved with ancient writing. It's said to ward off evil and to have been used in rites of exorcism.",
        'A dagger with ancient writing engraved on it. It has the power to drive away evil and was said to be used in exorcism rites.',
        'Restore both the reputed power and the ritual use.',
    ),
    3005: (
        'A stone mask with two serpents carved in relief. Ancient priests are said to have used it in rituals.',
        'A stone mask with two serpents in relief, said to have been used by priests in ancient rituals.',
        'Restore the relief work and the ritual context. Keep the claim qualified.',
    ),
    3006: (
        'Rose quartz with a six-rayed star. Its clarity and the sharpness of the star make it a rare specimen.',
        'Rose quartz with a six-rayed star. Its transparency and the sharply defined star make it an unusually fine specimen.',
        'Keep the material and explain what makes this specimen rare.',
    ),
    3007: (
        "A rare phantom crystal with a diamond inside, said to have grown again. It's also said to improve concentration.",
        'An uncommon phantom crystal containing a diamond, formed when the quartz grew again. It is said to improve concentration.',
        'Restore the second growth and retain the reported effect on concentration.',
    ),
    3008: (
        "A treasured sword from a small island nation in the East. It's said to be sharp enough to cut without touching.",
        'A treasured sword from a small eastern island nation. Its legendary sharpness is such that it can cut even what it does not touch.',
        'Keep the island nation and the supernatural claim without recasting it as ordinary range.',
    ),
    3009: (
        'A figurehead of a siren whose song wrecks ships. No one knows why a siren was chosen.',
        'A figurehead based on a siren whose singing wrecks ships. It is unknown why that likeness was chosen.',
        'Keep the shipwrecks part of the siren legend and restore the unexplained choice of design.',
    ),
    3010: (
        "A tightly twisted horn. No one knows if it really came from a dragon, but it's said to cure every illness.",
        'An intricately twisted horn. Whether it is truly a dragon’s horn is unknown. It is said to cure every illness.',
        'Name the disputed origin explicitly and keep the cure attributed to the in-game tradition.',
    ),
    3011: (
        "A great king's shield bearing a goddess. Legend says it served as a ship. Sailors long to have it as a good-luck charm.",
        'A great king’s shield depicting a goddess. According to legend it was used as a ship. Sailors long to have it as a talisman.',
        'Restore both the story of its use as a ship and what makes sailors seek it.',
    ),
    3012: (
        'A giant red spear said to ward off evil and protect its bearer.',
        'A huge red spear with the power to ward off evil, said to protect whoever carries it against every kind of evil.',
        'Retain the direct description and the qualified protective power.',
    ),
} | dict.fromkeys(range(3013, 3033), FRAGMENT)


def main():
    assert not OUTPUT.exists() and tuple(DATA) == IDS
    release = load(RELEASE)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    clean_image = NdsImage.open(CLEAN)
    clean, arm = clean_image.read_file(ARM), runtime.arm
    assert base.digest(CLEAN) == release['clean_input_sha256']
    japanese = common_message_entries(clean_image.read_file(COMMON), clean)
    current = owned_entries(runtime.common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    ledger = load(base.LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    credited = {(r['file_path'], r['id']) for r in ledger[base.CONTEXT]['integrated_record_keys']}
    payload, table, pointers = item_table(arm)
    assert len(set(pointers[198:])) == 1

    initializers = []
    for seed in SEEDS:
        old, new = (initialize(data, seed) for data in (clean, arm))
        assert old['selected_default_indices'] == new['selected_default_indices']
        for a, b in zip(old['names'], new['names'], strict=True):
            assert a['index'] == b['index'] and a['metadata_hex'] == b['metadata_hex']
        initializers.append(dict(seed=seed, selected_default_indices=new['selected_default_indices'],
                                 clean=old['names'], current=new['names']))
    assert {i for run in initializers for i in run['selected_default_indices']} == set(range(188, 198))

    consumers = []
    for lookup, paint, literal in zip(LOOKUP, PAINT, (0x4D890, 0x4E53C), strict=True):
        assert unpack_from('<I', clean, literal)[0] == unpack_from('<I', arm, literal)[0] == FIRST
        consumers.append(dict(lookup=0x02000000 + lookup, paint=0x02000000 + paint, literal=0x02000000 + literal,
                              current_lookup=GETTER, current_paint=PAINTER))
    records = []
    for n, (english, meaning, note) in DATA.items():
        identifier = f'COMMON_MESSAGE_{n}'
        assert (COMMON, identifier) not in credited
        assert english.isascii() and not any(token in english for token in ('%', '\0', '\n'))
        jp, en = japanese[n], current[n]
        current_text = en.text.decode('cp932')
        old = ' '.join(current_text.translate(WIDE_ASCII).split())
        ident = n - FIRST
        text, lines = item_paragraph(payload, pointers[ident])
        assert ' '.join(lines) == old
        offset = ident - 188
        prior_name, name = (initializers[0][side][offset] for side in ('clean', 'current'))
        generated = ident >= 198
        if generated:
            assert bytes.fromhex(name['metadata_hex'])[16:20] == bytes((12, 1, 24, 0))
        variants = []
        for run in initializers if generated else initializers[:1]:
            a, b = (run[side][offset] for side in ('clean', 'current'))
            variants.append(dict(seed=run['seed'], clean_name=a['name'], current_name=b['name'],
                clean_name_hex=a['name_hex'], current_name_hex=b['name_hex']))
        records.append(dict(
            id=identifier, message_ID=n, file_path=COMMON, item_ID=ident,
            runtime_name_pointer=OWNER + 0x22 + 32 * offset,
            runtime_metadata_pointer=OWNER + 0x3E4 + 24 * offset, runtime_metadata_hex=name['metadata_hex'],
            name_variants=variants, source_item_name=prior_name['name'], item_name=name['name'],
            clean_Japanese=jp.text.decode('cp932'), current_English=current_text, source_hex=jp.text.hex(),
            current_hex=en.text.hex(), source_reference=reference(jp), current_reference=reference(en),
            prior_private_pointer=pointers[ident], prior_private_rows=lines, prior_private_hex=text.hex(),
            private_pointer_field=table + 4 * ident, native_callers=consumers,
            source_meaning=meaning, localization_note=note, english=english, speaker='Item catalogue',
            context=('One of four map-fragment slots in a generated set. Its title is initialized from the selected relic.'
                     if generated else 'Promotional relic catalogue description below its runtime-initialized title.'),
            original_substitutions=[], decision='retention' if english == old else 'revision',
            current_wide_glyphs=wide_letters(current_text),
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
        ))
    save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'], records=records,
        registered_input=runtime.receipt(), native_initializers=initializers, active_description_table=table,
        source_rom_sha256=release['clean_input_sha256'], prior_context_sealed=True,
        new_completion_credit=0, full_goal_complete=False,
        evidence={str(path): base.digest(path) for path in (RELEASE, Path(__file__))}))
    print(f'{len(records)} promotional cards. {sum(r["decision"] == "revision" for r in records)} revisions.')


if __name__ == '__main__':
    main()
